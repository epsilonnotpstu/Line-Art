# Collection tools

Run from the repository root. Use Python 3 plus Pillow, Inkscape, potrace,
and a locally available `npx svgo`. No tool installs packages. Environment
reporting uses offline npx; exports also fail clearly if SVGO is unavailable.

```sh
tools/check_env.sh
python3 tools/qa.py icons/school_supplies
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
Packaging regenerates exports and the sheet, preserves an existing LICENSE.txt,
and includes only current collection items. Replace the license stub before sale.

QA reports failures and counts files passed/failed, with a nonzero failure exit.
It checks effective inherited/inline styles and queries Inkscape's visible bounds
in 512-unit coordinates. Bake transforms into geometry to keep 12px strokes.
External styles, references, hidden geometry and nested viewports are rejected.

Trace reads `raw/*.png` by default, or explicit PNG paths. It composites alpha
over white, thresholds, crops to ink, and runs potrace. Output defaults to
`export/traced/` (override with `--output`). It never writes raw/, icons/ or lib/.
Threshold (1–255) changes which pixels become ink; scale (>0, ≤1) adjusts the
centered artwork within a 448px box. Match line weight visually. Traces are
filled shapes, so outline QA intentionally rejects them; stroke icons use
12px outlines. Traces need manual outline conversion before the outline pipeline.

Tests isolate outputs under temporary `tests/fixtures/` directories. Real
Inkscape/Pillow/potrace verify rendering and tracing. When SVGO is unavailable,
an explicitly named stand-in tests orchestration and the real optimizer test
is skipped. No production icons are used.
