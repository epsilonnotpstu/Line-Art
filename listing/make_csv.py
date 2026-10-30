#!/usr/bin/env python3
"""Convert collection JSON to UTF-8 CSV; adapt column mapping at marketplace import."""
import argparse
import csv
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection", help="listing/<collection>.json basename")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", args.collection):
        parser.error("collection must be snake_case")
    source = ROOT / "listing" / f"{args.collection}.json"
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
        items = data["items"] if isinstance(data, dict) else data
        if not isinstance(items, list) or not items:
            raise ValueError("expected a nonempty items array")
        rows, filenames = [], set()
        for item in items:
            filename = item["filename"]
            if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\.svg", filename) or filename in filenames:
                raise ValueError("filenames must be unique snake_case SVG names")
            filenames.add(filename)
            title, description, keywords = item["title"], item["description"], item["keywords"]
            if not all(isinstance(v, str) and v.strip() for v in (title, description)):
                raise ValueError("title and description must be nonempty strings")
            if not isinstance(keywords, list) or not keywords or not all(isinstance(k, str) and k.strip() and "," not in k for k in keywords):
                raise ValueError("keywords must be a nonempty list of strings without commas")
            assisted = item.get("ai_assisted", True)
            if not isinstance(assisted, bool):
                raise ValueError("ai_assisted must be a JSON boolean")
            if assisted and re.search(r"hand[\s-]*drawn", title + " " + description + " " + " ".join(keywords), re.I):
                raise ValueError("AI-assisted items must not claim to be hand-drawn")
            row = [filename, title, description, ", ".join(dict.fromkeys(k.strip() for k in keywords)), str(assisted).lower()]
            if any(v.lstrip().startswith(("=", "+", "-", "@")) for v in row):
                raise ValueError("CSV values must not start with spreadsheet formula characters")
            rows.append(row)
        output = source.with_suffix(".csv")
        with output.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["filename", "title", "description", "keywords", "ai_assisted"])
            writer.writerows(rows)
        print(f"CSV: {output} ({len(rows)} items); map disclosure to the marketplace's upload controls")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Listing failed: {error}\n")


if __name__ == "__main__":
    main()
