#!/usr/bin/env python
"""Update the publication list and citation counts from Google Scholar.

Run by the "Update publications and citations" workflow
(.github/workflows/citations.yml), which then runs bin/update_coauthors.py.

New papers: papers on the Google Scholar profile that are not yet in
_bibliography/papers.bib are added to it (at most MAX_NEW_PAPERS per run), in the
same BibTeX style as a Scholar export, with the DOI and full author list taken
from OpenAlex when it has the same title. _data/scholar_sync.yml remembers every
profile paper already handled, so a paper deleted from papers.bib by hand is not
added again.

Citation counts (_data/citations.yml), sources in this order:

Sources, in this order:
1. Google Scholar: the profile whose ID is `scholar_userid` in _data/socials.yml.
   Gives total citations, h-index and i10-index, and each paper's "Cited by"
   count. Papers are matched to _bibliography/papers.bib by title (the .bib is
   exported from the same profile, so the titles agree).
2. OpenAlex (https://openalex.org), used only when Google Scholar can't be
   reached (it often blocks automated requests). Papers are matched by DOI, or
   by title among the works linked to `orcid_id` in _data/socials.yml. The
   totals are then worked out from the matched papers.

When Google Scholar can't be reached but the saved counts came from Google
Scholar within the last KEEP_SCHOLAR_DAYS days, they are kept as they are rather
than replaced by (lower) OpenAlex numbers. If no source works, the files are left
unchanged and the script exits with an error.

--dry-run prints the results without writing any file; --preview-new N (with
--dry-run) also builds the BibTeX of the N newest profile papers as if they were
new, to test that part on pull requests.
"""

import argparse
import json
import re
import signal
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone

import bibtexparser
import yaml

BIB_FILE = "_bibliography/papers.bib"
SOCIALS_FILE = "_data/socials.yml"
OUTPUT_FILE = "_data/citations.yml"
SYNC_FILE = "_data/scholar_sync.yml"
MAX_NEW_PAPERS = 5  # per run: each new paper costs one more Google Scholar request
KEEP_SCHOLAR_DAYS = 60
USER_AGENT = "civil-liangfu.github.io citation updater (GitHub Actions)"
SCHOLAR_TIME_LIMIT = 150  # seconds; Google Scholar can hang when it blocks a request

HEADER = """\
# Citation counts for the papers in _bibliography/papers.bib.
# Filled in AUTOMATICALLY twice a week by the "Update publications and citations"
# workflow (bin/update_citations.py). There is no need to edit this file.
"""

SYNC_HEADER = """\
# Google Scholar papers already handled by the "Update publications and citations"
# workflow (bin/update_citations.py): each is in papers.bib, or was added and later
# deleted on purpose, so it is not added again. Filled in automatically.
"""


# --------------------------------------------------------------------------- helpers


def normalise_title(title):
    """Lower-case letters and digits only, without accents or LaTeX markup."""
    title = re.sub(r"\\[a-zA-Z]+\s*", "", title)  # \textit, \emph, …
    title = re.sub(r'\\[\'"`^~=.]', "", title)  # accent commands such as \"u
    title = unicodedata.normalize("NFKD", title)
    title = "".join(c for c in title if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", title.lower())


def normalise_doi(doi):
    doi = (doi or "").strip().lower()
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi)


def titles_match(a, b):
    """Same title, or one is the start of the other (Scholar sometimes shortens titles)."""
    if not a or not b:
        return False
    if a == b:
        return True
    shorter, longer = sorted((a, b), key=len)
    return len(shorter) >= 30 and longer.startswith(shorter)


def h_index(counts):
    counts = sorted(counts, reverse=True)
    return sum(1 for i, c in enumerate(counts, start=1) if c >= i)


def load_papers():
    with open(BIB_FILE, encoding="utf-8") as f:
        bib = bibtexparser.load(f)
    papers = []
    for entry in bib.entries:
        papers.append(
            {
                "key": entry["ID"],
                "title": normalise_title(entry.get("title", "")),
                "doi": normalise_doi(entry.get("doi")),
            }
        )
    return papers


def load_socials():
    with open(SOCIALS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class TimeLimit(BaseException):
    """Raised by the alarm; a BaseException so the scholarly library can't swallow it."""


def _on_alarm(signum, frame):
    raise TimeLimit()


# --------------------------------------------------------------------------- sources


def with_time_limit(seconds, fn):
    signal.signal(signal.SIGALRM, _on_alarm)
    signal.alarm(seconds)
    try:
        return fn()
    finally:
        signal.alarm(0)


def scholar_profile(scholar_id):
    """The Google Scholar profile with its totals and list of papers."""
    from scholarly import scholarly  # imported here so OpenAlex still works without it

    scholarly.set_timeout(20)
    scholarly.set_retries(2)
    author = with_time_limit(SCHOLAR_TIME_LIMIT, lambda: scholarly.search_author_id(scholar_id))
    author = with_time_limit(
        SCHOLAR_TIME_LIMIT, lambda: scholarly.fill(author, sections=["basics", "indices", "publications"])
    )
    if not author.get("publications"):
        raise RuntimeError("the Google Scholar profile returned no publications")
    return author


def scholar_counts(papers, author, scholar_id):
    profile_url = f"https://scholar.google.com/citations?user={scholar_id}"
    scholar_pubs = []
    for pub in author.get("publications", []):
        pub_id = pub.get("author_pub_id") or ""
        scholar_pubs.append(
            {
                "title": normalise_title(pub.get("bib", {}).get("title", "")),
                "citations": int(pub.get("num_citations") or 0),
                "url": (
                    "https://scholar.google.com/citations?view_op=view_citation"
                    f"&user={scholar_id}&citation_for_view={pub_id}"
                    if pub_id
                    else profile_url
                ),
            }
        )

    matched = {}
    for paper in papers:
        for pub in scholar_pubs:
            if titles_match(paper["title"], pub["title"]):
                matched[paper["key"]] = {"citations": pub["citations"], "url": pub["url"]}
                break

    totals = {
        "citations": int(author.get("citedby") or 0),
        "h_index": int(author.get("hindex") or 0),
        "i10_index": int(author.get("i10index") or 0),
    }
    return "Google Scholar", profile_url, totals, matched


def ascii_word(text):
    text = unicodedata.normalize("NFKD", text)
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in text if not unicodedata.combining(c)).lower())


def last_first(name):
    """ "Liangfu Ge" → "Ge, Liangfu" (the form used in papers.bib)."""
    name = re.sub(r"\s+", " ", name).strip()
    if "," in name or " " not in name:
        return name
    given, surname = name.rsplit(" ", 1)
    return f"{surname}, {given}"


STOPWORDS = {"a", "an", "the", "on", "of", "for", "in", "to", "and", "with", "via", "using", "by", "from", "at", "as", "toward", "towards"}


def bib_key(first_author, year, title, taken):
    """Google Scholar's key style: surname + year + first word of the title, e.g. ge2025deep."""
    surname = ascii_word(first_author.split(",")[0]) or "paper"
    words = [ascii_word(w) for w in re.split(r"[\s\-:/]+", title)]
    word = next((w for w in words if w and w not in STOPWORDS), "")
    base = f"{surname}{year or ''}{word}"
    key, n = base, 1
    while key in taken:
        key, n = base + "bcdefghijklmnopqrstuvwxyz"[n - 1], n + 1
    return key


def openalex_by_title(title):
    """The OpenAlex work with the same title, if any."""
    try:
        data = openalex_get("works", {"search": title, "per-page": 5})
    except Exception as e:  # noqa: BLE001
        print(f"    OpenAlex title search failed: {e}")
        return None
    wanted = normalise_title(title)
    return next((w for w in data.get("results", []) if titles_match(wanted, normalise_title(w.get("title") or ""))), None)


def make_bibtex(bib, work, taken):
    """One BibTeX entry from Google Scholar's fields, completed with OpenAlex's."""
    work = work or {}
    source = ((work.get("primary_location") or {}).get("source")) or {}
    biblio = work.get("biblio") or {}
    title = (bib.get("title") or work.get("title") or "").strip()

    authors = bib.get("author") or ""
    if (not authors or "…" in authors or "..." in authors) and work.get("authorships"):
        authors = " and ".join(a["author"]["display_name"] for a in work["authorships"])  # Scholar shortens long lists
    authors = " and ".join(last_first(a) for a in authors.split(" and ") if a.strip())

    year = bib.get("pub_year") or work.get("publication_year") or ""
    journal = bib.get("journal")
    conference = bib.get("conference")
    venue = source.get("display_name")
    if journal or (not conference and source.get("type") == "journal"):
        kind, fields = "article", [("journal", journal or venue)]
    elif conference or source.get("type") == "conference" or "proceedings" in (venue or "").lower():
        kind, fields = "inproceedings", [("booktitle", conference or venue)]
    elif work.get("type") == "book-chapter":
        kind, fields = "incollection", [("booktitle", venue)]
    else:
        kind, fields = "misc", [("howpublished", venue)]

    pages = bib.get("pages")
    if not pages and biblio.get("first_page"):
        pages = biblio["first_page"] + (f"--{biblio['last_page']}" if biblio.get("last_page") not in (None, biblio["first_page"]) else "")
    doi = normalise_doi(work.get("doi"))
    fields = [("title", title), ("author", authors)] + fields + [
        ("volume", bib.get("volume") or biblio.get("volume")),
        ("number", bib.get("number") or biblio.get("issue")),
        ("pages", pages),
        ("year", str(year)),
        ("doi", doi),
        ("publisher", bib.get("publisher")),
    ]
    key = bib_key(authors.split(" and ")[0] if authors else "", year, title, taken)
    body = ",\n".join(f"  {name}={{{value}}}" for name, value in fields if value)
    return key, f"@{kind}{{{key},\n{body}\n}}\n"


def load_sync():
    try:
        with open(SYNC_FILE, encoding="utf-8") as f:
            return set((yaml.safe_load(f) or {}).get("known") or [])
    except FileNotFoundError:
        return set()


def save_sync(known):
    lines = [SYNC_HEADER.rstrip("\n"), "known:"] + [f"  - {q(k)}" for k in sorted(known)]
    with open(SYNC_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def add_new_papers(author, papers, dry_run, preview_new=0):
    """Adds profile papers that are missing from papers.bib. Returns the new keys."""
    from scholarly import scholarly

    known = load_sync()
    pubs = author.get("publications", [])
    in_bib = lambda pub: any(titles_match(p["title"], normalise_title(pub["bib"].get("title", ""))) for p in papers)
    present = [p for p in pubs if in_bib(p)]
    missing = [p for p in pubs if not in_bib(p) and p.get("author_pub_id") not in known]
    print(f"  {len(pubs)} papers on the profile: {len(present)} in papers.bib, {len(missing)} new")
    for pub in missing:
        print(f"    new: {pub['bib'].get('title', '?')} ({pub['bib'].get('pub_year', 'no year')})")
    if preview_new:  # test run: pretend the newest profile papers are new
        missing = sorted(pubs, key=lambda p: int(p["bib"].get("pub_year") or 0), reverse=True)[:preview_new]
        print(f"  preview: building BibTeX for the {preview_new} newest profile papers as if they were new")

    taken = {p["key"] for p in papers}
    entries, handled = [], {p.get("author_pub_id") for p in present}
    for pub in missing[:MAX_NEW_PAPERS]:
        title = pub["bib"].get("title", "")
        bib = None
        try:
            bib = with_time_limit(60, lambda: scholarly.fill(pub))["bib"]
        except (Exception, TimeLimit) as e:  # noqa: BLE001 — OpenAlex may still know the paper
            print(f"  Google Scholar gave no details for '{title}' ({type(e).__name__}: {e}); trying OpenAlex")
        work = openalex_by_title((bib or {}).get("title") or title)
        if not bib and not work:
            print(f"  '{title}' is not on OpenAlex either; trying again next run")
            continue
        # without Scholar's details, the authors, venue, volume, pages and DOI come from OpenAlex
        key, entry = make_bibtex(bib or {"title": title, "pub_year": pub["bib"].get("pub_year")}, work, taken)
        taken.add(key)
        entries.append(entry)
        handled.add(pub.get("author_pub_id"))
        print(f"  new paper: {key} — {title}")
    if len(missing) > MAX_NEW_PAPERS:
        print(f"  {len(missing) - MAX_NEW_PAPERS} more will be added on the next runs")

    if dry_run or preview_new:
        for entry in entries:
            print(entry)
        return []
    if entries:
        with open(BIB_FILE, encoding="utf-8") as f:
            current = f.read()
        with open(BIB_FILE, "a", encoding="utf-8") as f:
            f.write(("" if current.endswith("\n") else "\n") + "\n" + "\n".join(entries))
    save_sync(known | {h for h in handled if h})
    return [re.match(r"@\w+\{([^,]+),", e).group(1) for e in entries]


def recent_scholar_data():
    """True if citations.yml holds Google Scholar counts from the last KEEP_SCHOLAR_DAYS days."""
    try:
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            meta = (yaml.safe_load(f) or {}).get("metadata") or {}
        age = (date.today() - date.fromisoformat(str(meta.get("last_updated")))).days
        return meta.get("source") == "Google Scholar" and age <= KEEP_SCHOLAR_DAYS
    except (FileNotFoundError, ValueError, TypeError):
        return False


def openalex_get(path, params):
    url = "https://api.openalex.org/" + path + "?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))


def from_openalex(papers, orcid):
    works = []
    # 1. every paper that has a DOI, 40 DOIs per request
    dois = sorted({p["doi"] for p in papers if p["doi"]})
    for i in range(0, len(dois), 40):
        batch = "|".join("https://doi.org/" + d for d in dois[i : i + 40])
        data = openalex_get("works", {"filter": "doi:" + batch, "per-page": 50})
        works += data.get("results", [])
    # 2. works linked to my ORCID iD (finds conference papers without a DOI)
    if orcid:
        data = openalex_get(
            "works", {"filter": "author.orcid:https://orcid.org/" + orcid, "per-page": 200}
        )
        works += data.get("results", [])

    for w in works:
        w["_doi"] = normalise_doi(w.get("doi"))
        w["_title"] = normalise_title(w.get("title") or w.get("display_name") or "")
    if not works:
        raise RuntimeError("OpenAlex returned no works")

    matched = {}
    for paper in papers:
        found = None
        if paper["doi"]:
            found = next((w for w in works if w["_doi"] == paper["doi"]), None)
        if not found:
            found = next((w for w in works if titles_match(paper["title"], w["_title"])), None)
        if found:
            work_id = (found.get("id") or "").rsplit("/", 1)[-1]
            matched[paper["key"]] = {
                "citations": int(found.get("cited_by_count") or 0),
                "url": f"https://openalex.org/works/{work_id}" if work_id else "https://openalex.org",
            }

    counts = [m["citations"] for m in matched.values()]
    totals = {
        "citations": sum(counts),
        "h_index": h_index(counts),
        "i10_index": sum(1 for c in counts if c >= 10),
    }
    url = f"https://orcid.org/{orcid}" if orcid else "https://openalex.org"
    return "OpenAlex", url, totals, matched


# --------------------------------------------------------------------------- output


def q(text):
    """A double-quoted YAML string (the style the site's Prettier check expects)."""
    return json.dumps(str(text), ensure_ascii=False)


def yaml_key(key):
    return key if re.fullmatch(r"[A-Za-z0-9_.-]+", key) else q(key)


def render(source, source_url, totals, matched, papers):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [HEADER.rstrip("\n"), "metadata:"]
    lines += [f"  last_updated: {q(today)}", f"  source: {q(source)}", f"  source_url: {q(source_url)}"]
    lines += ["totals:"] + [f"  {k}: {v}" for k, v in totals.items()]
    order = [p["key"] for p in papers if p["key"] in matched]
    if order:
        lines.append("papers:")
        for key in order:
            lines += [
                f"  {yaml_key(key)}:",
                f"    citations: {matched[key]['citations']}",
                f"    url: {q(matched[key]['url'])}",
            ]
    else:
        lines.append("papers: {}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="print the results, don't write any file")
    parser.add_argument("--preview-new", type=int, default=0, help="with --dry-run: treat the N newest papers as new")
    parser.add_argument(
        "--source", choices=["auto", "scholar", "openalex"], default="auto", help="which source to use"
    )
    args = parser.parse_args()

    papers = load_papers()
    socials = load_socials()
    scholar_id = str(socials.get("scholar_userid") or "")
    print(f"{len(papers)} papers in {BIB_FILE}")

    result = None
    if args.source in ("auto", "scholar") and scholar_id:
        print("Trying Google Scholar …")
        try:
            author = scholar_profile(scholar_id)
            added = add_new_papers(author, papers, args.dry_run, args.preview_new)
            if added:
                papers = load_papers()  # count the new papers too
            result = scholar_counts(papers, author, scholar_id)
        except (Exception, TimeLimit) as e:  # noqa: BLE001 — any failure means "try the next source"
            print(f"  Google Scholar failed: {type(e).__name__}: {e}")
        if result and not result[3]:
            print("  Google Scholar matched no papers, so it is not used.")
            result = None
        if not result and args.source == "auto" and recent_scholar_data():
            print(f"Keeping the Google Scholar counts saved within the last {KEEP_SCHOLAR_DAYS} days.")
            return 0

    if not result and args.source in ("auto", "openalex"):
        print("Trying OpenAlex …")
        try:
            result = from_openalex(papers, str(socials.get("orcid_id") or ""))
        except Exception as e:  # noqa: BLE001
            print(f"  OpenAlex failed: {type(e).__name__}: {e}")
        if result and not result[3]:
            print("  OpenAlex matched no papers, so it is not used.")
            result = None

    if not result:
        print("No source worked; " + OUTPUT_FILE + " was left unchanged.")
        return 1
    source, source_url, totals, matched = result
    print(f"  {source}: matched {len(matched)} of {len(papers)} papers; totals {totals}")
    unmatched = [p["key"] for p in papers if p["key"] not in matched]
    if unmatched:
        print("  not found: " + ", ".join(unmatched))
    text = render(source, source_url, totals, matched, papers)
    if args.dry_run:
        print("--- " + OUTPUT_FILE + " (dry run, not written) ---\n" + text)
    else:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
