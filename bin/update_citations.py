#!/usr/bin/env python
"""Update _data/citations.yml with citation counts for the papers in papers.bib.

Run by the "Update citation counts" workflow (.github/workflows/citations.yml).

Sources, in this order:
1. Google Scholar: the profile whose ID is `scholar_userid` in _data/socials.yml.
   Gives total citations, h-index and i10-index, and each paper's "Cited by"
   count. Papers are matched to _bibliography/papers.bib by title (the .bib is
   exported from the same profile, so the titles agree).
2. OpenAlex (https://openalex.org), used only when Google Scholar can't be
   reached (it often blocks automated requests). Papers are matched by DOI, or
   by title among the works linked to `orcid_id` in _data/socials.yml. The
   totals are then worked out from the matched papers.

If both fail, the existing file is left unchanged and the script exits with an
error. `--dry-run` prints the result without writing the file.
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
from datetime import datetime, timezone

import bibtexparser
import yaml

BIB_FILE = "_bibliography/papers.bib"
SOCIALS_FILE = "_data/socials.yml"
OUTPUT_FILE = "_data/citations.yml"
USER_AGENT = "civil-liangfu.github.io citation updater (GitHub Actions)"
SCHOLAR_TIME_LIMIT = 150  # seconds; Google Scholar can hang when it blocks a request

HEADER = """\
# Citation counts for the papers in _bibliography/papers.bib.
# Filled in AUTOMATICALLY every Monday by the "Update citation counts" workflow
# (bin/update_citations.py). There is no need to edit this file.
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


def from_google_scholar(papers, scholar_id):
    from scholarly import scholarly  # imported here so OpenAlex still works without it

    scholarly.set_timeout(20)
    scholarly.set_retries(2)
    signal.signal(signal.SIGALRM, _on_alarm)
    signal.alarm(SCHOLAR_TIME_LIMIT)
    try:
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author, sections=["basics", "indices", "publications"])
    finally:
        signal.alarm(0)

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
    if not scholar_pubs:
        raise RuntimeError("the Google Scholar profile returned no publications")

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
    parser.add_argument("--dry-run", action="store_true", help="print the result, don't write the file")
    parser.add_argument(
        "--source", choices=["auto", "scholar", "openalex"], default="auto", help="which source to use"
    )
    args = parser.parse_args()

    papers = load_papers()
    socials = load_socials()
    print(f"{len(papers)} papers in {BIB_FILE}")

    attempts = []
    if args.source in ("auto", "scholar") and socials.get("scholar_userid"):
        attempts.append(("Google Scholar", lambda: from_google_scholar(papers, str(socials["scholar_userid"]))))
    if args.source in ("auto", "openalex"):
        attempts.append(("OpenAlex", lambda: from_openalex(papers, str(socials.get("orcid_id") or ""))))

    for name, fetch in attempts:
        print(f"Trying {name} …")
        try:
            source, source_url, totals, matched = fetch()
        except (Exception, TimeLimit) as e:  # noqa: BLE001 — any failure means "try the next source"
            print(f"  {name} failed: {type(e).__name__}: {e}")
            continue
        print(f"  {name}: matched {len(matched)} of {len(papers)} papers; totals {totals}")
        unmatched = [p["key"] for p in papers if p["key"] not in matched]
        if unmatched:
            print("  not found: " + ", ".join(unmatched))
        if not matched:
            print(f"  {name} matched no papers, so it is not used.")
            continue
        text = render(source, source_url, totals, matched, papers)
        if args.dry_run:
            print("--- " + OUTPUT_FILE + " (dry run, not written) ---\n" + text)
        else:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved {OUTPUT_FILE}")
        return 0

    print("No source worked; " + OUTPUT_FILE + " was left unchanged.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
