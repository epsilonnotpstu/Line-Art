# Listing CSV

Save `listing/<collection>.json` as an array of items, or an object with `items`
and an optional `bundle`. Each entry has filename, title, description, keywords,
and ai_assisted. Item filenames end in `.svg`; the bundle filename ends in `.zip`.
Use actual collection filenames. See `school_supplies.json` for a complete example.

Run `python3 listing/make_csv.py <collection>` to write `listing/<collection>.csv`.
Columns: filename, title, description, keywords, ai_assisted, type, contents.
CSV uses UTF-8 with a BOM and standard quoting. Titles must be unique and at most
60 characters. Items require 25–40 unique keywords; the bundle requires exactly 30.
The bundle needs a one-line contents list; item contents default to SVG/PNG/EPS.
AI assistance defaults to true. Descriptions use a two-sentence body, a blank line,
and the disclosure managed by `DISCLOSURE` in `make_csv.py`. CSV generation replaces
the disclosure section from that constant, so future wording changes need one edit.
Map these portable columns to the selected marketplace's import fields and set
its required AI disclosure controls according to its current policy. The CSV
does not submit assets or claim compliance with any particular marketplace.
