#!/usr/bin/env python3
"""Convert collection JSON to UTF-8 CSV; adapt column mapping at marketplace import."""
import argparse
import csv
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DISCLOSURE = "Created with AI-assisted tools and edited by the seller. Disclose per marketplace AI policy."


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
        entries = [(item, "item") for item in items]
        if isinstance(data, dict) and "bundle" in data:
            entries.append((data["bundle"], "bundle"))
        rows, filenames, titles = [], set(), set()
        for item, kind in entries:
            filename = item["filename"]
            extension = "svg" if kind == "item" else "zip"
            if not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\." + extension, filename) or filename in filenames:
                raise ValueError("filenames must be unique snake_case SVG/ZIP names")
            filenames.add(filename)
            title, description, keywords = item["title"], item["description"], item["keywords"]
            if not all(isinstance(v, str) and v.strip() for v in (title, description)):
                raise ValueError("title and description must be nonempty strings")
            title = title.strip()
            if len(title) > 60 or title.casefold() in titles:
                raise ValueError("titles must be unique and at most 60 characters")
            titles.add(title.casefold())
            if not isinstance(keywords, list) or not keywords or not all(isinstance(k, str) and k.strip() and "," not in k for k in keywords):
                raise ValueError("keywords must be a nonempty list of strings without commas")
            keywords = [k.strip() for k in keywords]
            if len({k.casefold() for k in keywords}) != len(keywords):
                raise ValueError("keywords must not contain duplicates")
            if not 25 <= len(keywords) <= 40 or kind == "bundle" and len(keywords) != 30:
                raise ValueError("items need 25–40 keywords; bundles need exactly 30")
            assisted = item.get("ai_assisted", True)
            if not isinstance(assisted, bool):
                raise ValueError("ai_assisted must be a JSON boolean")
            if re.search(r"hand(?:[\s-]*drawn|made)", title + " " + description + " " + " ".join(keywords), re.I):
                raise ValueError("listings must not claim manual creation")
            # A blank line separates the body from the centrally managed disclosure.
            description = description.partition("\n\n")[0].strip() + "\n\n" + DISCLOSURE
            contents = item.get("contents", "1 SVG file, 1 PNG file, 1 EPS file" if kind == "item" else "")
            if not isinstance(contents, str) or not contents.strip() or "\n" in contents:
                raise ValueError("contents must be one nonempty line")
            row = [filename, title, description, ", ".join(keywords), str(assisted).lower(), kind, contents]
            if any(v.lstrip().startswith(("=", "+", "-", "@")) for v in row):
                raise ValueError("CSV values must not start with spreadsheet formula characters")
            rows.append(row)
        output = source.with_suffix(".csv")
        with output.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["filename", "title", "description", "keywords", "ai_assisted", "type", "contents"])
            writer.writerows(rows)
        print(f"CSV: {output} ({len(rows)} rows); map disclosure to the marketplace's upload controls")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Listing failed: {error}\n")


if __name__ == "__main__":
    main()
