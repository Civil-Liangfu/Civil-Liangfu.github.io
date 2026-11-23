#!/usr/bin/env python
"""Fill in the map position of the collaborations in _data/collaborations.yml.

Run by the "Place collaborations on the map" workflow
(.github/workflows/collaboration-places.yml) whenever that file changes on main.
For my institution (`home`) and each collaboration that has no `coordinates`, it
looks the institution up and writes "latitude, longitude" right after `place`. When
`place` ("City, Country") is empty too, it fills that in as well. Entries that
already have coordinates are never changed, so coordinates typed in by hand win.

Lookup, in this order:
1. OpenAlex institutions (https://openalex.org): research institutions with their
   location. When `place` is given, the result's city or country must appear in it,
   so a same-named university elsewhere is skipped.
2. OpenStreetMap Nominatim (https://nominatim.openstreetmap.org): "institution,
   place", then "place" alone (the city centre). At most one request per second,
   as its usage policy asks; results are saved, so each place is looked up once.

The file is edited with ruamel.yaml, which keeps its comments, quotes and key order.
Options: --dry-run prints the changes without saving; --check looks every entry up
again (ignoring the saved coordinates) and reports how far the result is from the
saved position, to test the lookup on pull requests without changing anything.
"""

import argparse
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

DATA_FILE = "_data/collaborations.yml"
USER_AGENT = "civil-liangfu.github.io collaboration map (GitHub Actions; https://civil-liangfu.github.io)"
_last_nominatim = [0.0]


def get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))


def text(value):
    return str(value or "").strip()


# --------------------------------------------------------------------------- sources


def from_openalex(institution, place):
    url = "https://api.openalex.org/institutions?" + urllib.parse.urlencode({"search": institution, "per-page": 8})
    for result in get_json(url).get("results", []):
        geo = result.get("geo") or {}
        lat, lon = geo.get("latitude"), geo.get("longitude")
        if lat is None or lon is None:
            continue
        city, country = text(geo.get("city")), text(geo.get("country"))
        if place:
            wanted = place.lower()
            if not ((city and city.lower() in wanted) or (country and country.lower() in wanted)):
                continue
        return float(lat), float(lon), ", ".join(x for x in (city, country) if x), result.get("display_name")
    return None


def from_nominatim(query):
    wait = 1.1 - (time.time() - _last_nominatim[0])  # at most one request per second
    if wait > 0:
        time.sleep(wait)
    _last_nominatim[0] = time.time()
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": query, "format": "jsonv2", "limit": 1, "addressdetails": 1, "accept-language": "en"}
    )
    results = get_json(url)
    if not results:
        return None
    hit = results[0]
    address = hit.get("address") or {}
    city = text(address.get("city") or address.get("town") or address.get("village") or address.get("state"))
    country = text(address.get("country"))
    return float(hit["lat"]), float(hit["lon"]), ", ".join(x for x in (city, country) if x), hit.get("display_name")


def locate(institution, place):
    """Returns (source, (lat, lon, "City, Country", matched name)) or (None, None)."""
    attempts = []
    if institution:
        attempts.append(("OpenAlex", lambda: from_openalex(institution, place)))
        attempts.append(("OpenStreetMap", lambda: from_nominatim(f"{institution}, {place}" if place else institution)))
    if place:
        attempts.append(("OpenStreetMap (city centre)", lambda: from_nominatim(place)))
    for name, fetch in attempts:
        try:
            hit = fetch()
        except Exception as e:  # noqa: BLE001 — any failure means "try the next source"
            print(f"    {name} failed: {type(e).__name__}: {e}")
            continue
        if hit:
            return name, hit
    return None, None


# --------------------------------------------------------------------------- the file


def entries(data):
    """(label, mapping) for `home` and every collaboration."""
    found = []
    if isinstance(data.get("home"), dict):
        found.append(("home", data["home"]))
    for i, item in enumerate(data.get("collaborations") or [], start=1):
        if isinstance(item, dict):
            found.append((f"collaboration {i}", item))
    return found


def put_after(mapping, key, value, after):
    """Set mapping[key], inserting it right after the first existing key in `after`."""
    if key in mapping:
        mapping[key] = value
        return
    keys = list(mapping.keys())
    position = next((keys.index(k) + 1 for k in after if k in mapping), len(keys))
    mapping.insert(position, key, value)


def distance_km(a, b):
    (lat1, lon1), (lat2, lon2) = [(math.radians(x), math.radians(y)) for x, y in (a, b)]
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def parse_coordinates(value):
    try:
        lat, lon = [float(x) for x in text(value).split(",")]
        return lat, lon
    except ValueError:
        return None


def summary(line):
    print(line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(line + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="print the changes, don't save")
    parser.add_argument("--check", action="store_true", help="look every entry up again and compare")
    parser.add_argument("--file", default=DATA_FILE)
    args = parser.parse_args()

    yaml = YAML()  # round-trip mode: keeps comments, quotes and key order
    yaml.preserve_quotes = True
    yaml.width = 4096  # never wrap long descriptions
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(args.file, encoding="utf-8") as f:
        data = yaml.load(f)

    if args.check:
        found = 0
        for label, item in entries(data):
            name, place = text(item.get("institution")), text(item.get("place"))
            source, hit = locate(name, place)
            saved = parse_coordinates(item.get("coordinates"))
            if hit:
                found += 1
                off = f"{distance_km(saved, hit[:2]):.1f} km from the saved position" if saved else "no saved position"
                summary(f"- {name}: {source} → {hit[0]:.4f}, {hit[1]:.4f} ({hit[2]}); {off}")
            else:
                summary(f"- {name}: not found")
        return 0 if found else 1

    changed, missing = [], []
    for label, item in entries(data):
        if parse_coordinates(item.get("coordinates")):
            continue  # already placed (by hand or by an earlier run)
        name, place = text(item.get("institution")), text(item.get("place"))
        print(f"Looking up {name or label} ({place or 'no place given'}) …")
        source, hit = locate(name, place)
        if not hit:
            missing.append(name or label)
            continue
        lat, lon, found_place, matched = hit
        if not place and found_place:
            put_after(item, "place", DoubleQuotedScalarString(found_place), ["institution"])
        put_after(item, "coordinates", DoubleQuotedScalarString(f"{lat:.4f}, {lon:.4f}"), ["place", "institution"])
        changed.append(f"- {name or label}: {lat:.4f}, {lon:.4f} ({found_place or place}), via {source} ({matched})")

    for line in changed:
        summary(line)
    for name in missing:
        # a warning in the Actions log; the entry stays in the list, without a marker
        print(f"::warning::Could not find '{name}' on the map. In the editing panel, add its city and country, or paste coordinates from Google Maps.")
        summary(f"- {name}: not found. Add its city and country, or paste coordinates.")
    if not changed:
        print("Nothing to add: every entry already has coordinates." if not missing else "No new positions found.")
        return 0
    if args.dry_run:
        print(f"--- {args.file} (dry run, not saved) ---")
        yaml.dump(data, sys.stdout)
    else:
        with open(args.file, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
        print(f"Saved {args.file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
