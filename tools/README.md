# Collection tools

Run from the repository root. Use Python 3 plus Pillow, Inkscape, potrace,
and local `node_modules/.bin/svgo`. No tool downloads or installs packages.
Environment reporting and exports invoke that executable directly, independent
of the working directory, and report a missing local SVGO clearly.

```sh
tools/check_env.sh
python3 tools/qa.py icons/school_supplies
python3 tools/qa.py --traced icons/farm_animals icons/food
tools/export.sh school_supplies
python3 tools/contact_sheet.py school_supplies
python3 tools/trace.py --threshold 128 --scale 0.9
tools/pack.sh school_supplies
python3 listing/make_csv.py school_supplies
python3 -m unittest discover -s tests -v
```

Export, contact sheet and pack also accept an explicit flat collection directory,
such as `tests/fixtures`. Its basename determines the output collection name.
SVG/PNG/EPS go in `export/<collection>/`; the single labeled sheet goes in
`previews/<collection>_sheet.png`; the ZIP goes in `dist/<collection>.zip`.
PNG exports are transparent 1024 × 1024. EPS uses the page bounds.
SVGO preserves groups and explicit black stroke styling; exported SVGs pass QA.
New traces carry `data-traced="true"` on the SVG root. Export selects `--traced`
for each marked file before and after optimization; unmarked files use strict
outline QA. This allows mixed collections without weakening outline checks.
Packaging regenerates exports and the sheet, preserves an existing LICENSE.txt,
and includes only current collection items. Replace the license stub before sale.

QA reports failures and counts files passed/failed, with a nonzero failure exit.
It checks effective inherited/inline styles and queries Inkscape's visible bounds
in 512-unit coordinates. Bake transforms into geometry to keep 12px strokes.
External styles, references, hidden geometry and nested viewports are rejected.
The explicit `--traced` profile allows black fills, arbitrary stroke width and
tracing transforms. It retains the viewBox, one top-level group, editable shapes,
32px visible margin, black color, transparency, forbidden content and stray-element
checks. A marker alone does not change standalone QA: pass `--traced` explicitly.

Trace reads `raw/*.png` by default, or explicit PNG paths. It composites alpha
over white, thresholds, crops to ink, and runs potrace. Output defaults to
`export/traced/` (override with `--output`). It never writes raw/ or lib/.
Writing to icons/ requires explicit user authorization under the ownership rules.
Threshold (1–255) changes which pixels become ink; scale (>0, ≤1) adjusts the
centered artwork within a 448px box. Match line weight visually. Traced icons
are filled shapes while stroke icons are 12px outlines; use the traced QA profile
and root marker to preserve this distinction through the export pipeline.

Tests isolate outputs under temporary `tests/fixtures/` directories. Real
Inkscape/Pillow/potrace verify rendering and tracing. Real local SVGO is required:
tests verify comment removal, mixed-profile SVG/PNG/EPS exports, and ZIP contents.
No production icons are used.
