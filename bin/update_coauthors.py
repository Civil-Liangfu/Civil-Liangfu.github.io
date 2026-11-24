#!/usr/bin/env python
"""Build _data/coauthor_network.yml: my co-authors' institutions, from OpenAlex.

Run by the "Update publications and citations" workflow
(.github/workflows/citations.yml) after bin/update_citations.py, so papers just
added from Google Scholar are included. The collaboration map on the home page
(_includes/collaboration_map.liquid) shows these institutions next to the
collaborations entered by hand in _data/collaborations.yml (which always win, and
which can hide any automatic one).

For every paper in _bibliography/papers.bib, OpenAlex (https://openalex.org) is
asked for its authors and their institutions: by DOI, or by title among the works
linked to my ORCID iD (conference papers often have no DOI). My own authorship is
recognised by my ORCID iD or my name (scholar.last_name / first_name in
_config.yml). Each other author's institutions are collected with the papers we
share; then each institution's position (OpenAlex `geo`) is looked up.

If OpenAlex can't be reached, the existing file is kept and the script exits 0
with a warning. --dry-run prints the result without writing the file.
"""

import argparse
import os
import sys
from datetime import datetime, timezone

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_citations import (  # noqa: E402 — shared helpers
    load_papers,
    load_socials,
    normalise_doi,
    normalise_title,
    openalex_get,
    q,
    titles_match,
)

OUTPUT_FILE = "_data/coauthor_network.yml"
CONFIG_FILE = "_config.yml"
MAX_PEOPLE_SHOWN = 3

HEADER = """\
# Institutions of my co-authors, found AUTOMATICALLY twice a week from OpenAlex by
# the "Update publications and citations" workflow (bin/update_coauthors.py). Shown
# on the home page's collaboration map next to the collaborations entered by hand.
# Don't edit this file: to hide a wrong institution, add its name under
# "Hide these co-author institutions" in the editing panel (Collaborations).
"""


def owner_names():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        scholar = (yaml.safe_load(f) or {}).get("scholar") or {}
    last = [str(x).lower() for x in scholar.get("last_name") or []]
    first = [str(x).lower().rstrip(".") for x in scholar.get("first_name") or []]
    return last, first


def is_owner(authorship, orcid, last_names, first_names):
    author = authorship.get("author") or {}
    if orcid and (author.get("orcid") or "").endswith(orcid):
        return True
    words = (author.get("display_name") or "").lower().replace(".", " ").split()
    if len(words) < 2 or words[-1] not in last_names:
        return False
    given = words[0]
    # "Liangfu Ge" or "L Ge", but not another Ge such as "Lei Ge"
    return any(given == f or (len(given) == 1 and f.startswith(given)) for f in first_names)


def bib_name(display_name):
    """ "Danhui Dan" → "Dan, Danhui" (the form used in papers.bib and the map cards)."""
    words = display_name.split()
    return display_name if len(words) < 2 else f"{words[-1]}, {' '.join(words[:-1])}"


def fetch_works(papers, orcid):
    fields = "id,doi,title,authorships"
    works = []
    dois = sorted({p["doi"] for p in papers if p["doi"]})
    for i in range(0, len(dois), 40):
        batch = "|".join("https://doi.org/" + d for d in dois[i : i + 40])
        works += openalex_get("works", {"filter": "doi:" + batch, "per-page": 50, "select": fields}).get("results", [])
    if orcid:
        works += openalex_get(
            "works", {"filter": "author.orcid:https://orcid.org/" + orcid, "per-page": 200, "select": fields}
        ).get("results", [])
    for w in works:
        w["_doi"] = normalise_doi(w.get("doi"))
        w["_title"] = normalise_title(w.get("title") or "")
    return works


def fetch_places(ids):
    """OpenAlex institution id → (latitude, longitude, "City, Country")."""
    places = {}
    for i in range(0, len(ids), 50):
        batch = ids[i : i + 50]
        results = openalex_get(
            "institutions", {"filter": "openalex:" + "|".join(batch), "per-page": 50, "select": "id,geo"}
        ).get("results", [])
        for inst in results:
            geo = inst.get("geo") or {}
            if geo.get("latitude") is None or geo.get("longitude") is None:
                continue
            city, country = geo.get("city"), geo.get("country")
            place = ", ".join(x for x in (city, country if country != city else None) if x)  # not "Singapore, Singapore"
            places[inst["id"].rsplit("/", 1)[-1]] = (float(geo["latitude"]), float(geo["longitude"]), place)
    return places


def build(papers, socials):
    orcid = str(socials.get("orcid_id") or "")
    last_names, first_names = owner_names()
    works = fetch_works(papers, orcid)
    institutions = {}  # id → {"name", "papers": [keys], "people": {display name: set(keys)}}
    found = 0
    for paper in papers:
        work = next((w for w in works if paper["doi"] and w["_doi"] == paper["doi"]), None)
        work = work or next((w for w in works if titles_match(paper["title"], w["_title"])), None)
        if not work:
            continue
        found += 1
        for authorship in work.get("authorships") or []:
            if is_owner(authorship, orcid, last_names, first_names):
                continue
            person = ((authorship.get("author") or {}).get("display_name") or "").strip()
            for inst in authorship.get("institutions") or []:
                if not inst.get("id") or not inst.get("display_name"):
                    continue
                entry = institutions.setdefault(
                    inst["id"].rsplit("/", 1)[-1], {"name": inst["display_name"], "papers": [], "people": {}}
                )
                if paper["key"] not in entry["papers"]:
                    entry["papers"].append(paper["key"])
                if person:
                    entry["people"].setdefault(person, set()).add(paper["key"])

    places = fetch_places(sorted(institutions)) if institutions else {}
    result = []
    for inst_id, entry in institutions.items():
        if inst_id not in places:
            continue  # no position known: can't be put on the map
        lat, lon, place = places[inst_id]
        people = sorted(entry["people"], key=lambda name: (-len(entry["people"][name]), name))
        shown = ", ".join(people[:MAX_PEOPLE_SHOWN])
        if len(people) > MAX_PEOPLE_SHOWN:
            shown += f" and {len(people) - MAX_PEOPLE_SHOWN} more"
        result.append(
            {
                "institution": entry["name"],
                "place": place,
                "coordinates": f"{lat:.4f}, {lon:.4f}",
                "openalex": inst_id,
                "people": shown,
                "coauthors": [bib_name(p) for p in people],
                "papers": [p["key"] for p in papers if p["key"] in entry["papers"]],
            }
        )
    result.sort(key=lambda r: (-len(r["papers"]), r["institution"]))
    return result, found


def render(institutions, found, total):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [HEADER.rstrip("\n"), "metadata:", f"  last_updated: {q(today)}", '  source: "OpenAlex"']
    lines += [f"  papers_found: {found}", f"  papers_total: {total}"]
    if not institutions:
        return "\n".join(lines + ["institutions: []"]) + "\n"
    lines.append("institutions:")
    for inst in institutions:
        lines.append(f"  - institution: {q(inst['institution'])}")
        for key in ("place", "coordinates", "openalex", "people"):
            lines.append(f"    {key}: {q(inst[key])}")
        for key in ("coauthors", "papers"):
            lines.append(f"    {key}:")
            lines += [f"      - {q(v)}" for v in inst[key]]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="print the result, don't write the file")
    args = parser.parse_args()

    papers = load_papers()
    try:
        institutions, found = build(papers, load_socials())
    except Exception as e:  # noqa: BLE001 — keep the old file
        print(f"::warning::OpenAlex could not be reached ({type(e).__name__}: {e}); {OUTPUT_FILE} was kept.")
        return 0
    print(f"OpenAlex knows {found} of {len(papers)} papers; {len(institutions)} co-author institutions with a position:")
    for inst in institutions:
        print(f"  {len(inst['papers']):2} joint papers  {inst['institution']} ({inst['place']}) — {inst['people']}")
    text = render(institutions, found, len(papers))
    if args.dry_run:
        print(f"--- {OUTPUT_FILE} (dry run, not written) ---\n{text}")
    else:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
