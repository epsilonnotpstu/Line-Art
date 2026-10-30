# AGENTS.md

## Goal
Black-and-white outline clipart (educational), sold as SVG/PNG/EPS bundles on stock and digital-product marketplaces.
Collections: school_supplies, farm_animals, science_stem, food, daily_routine.

## Style spec (do not change without asking)
- viewBox `0 0 512 512`; transparent background; `fill="none"`
- stroke `#000000`, stroke-width `12`, stroke-linecap/linejoin `round`
- 32px safe margin on all sides
- No gradients, filters, clip-paths, text, embedded raster or base64
- Real editable paths/shapes only; exactly one top-level `<g>`
- snake_case file names; single clear subject per icon

## Ownership
- claude owns `lib/` and `icons/`.
- codex owns `tools/`, export pipeline (`export/`), `listing/`, `tests/`.
- `raw/` is user input: read-only for agents.
- Never edit the other agent's folders; ask via the Handoff queue in LOG.md.

## Token rules
- Read script output (pass/fail), not SVG files, unless QA fails.
- View `previews/*_sheet.png` at most once per batch.
- Prefer one batch request over many single ones.
- Keep answers short.

## Logging protocol
After every task append one entry to LOG.md in this exact format:

    ## YYYY-MM-DD HH:MM | <claude|codex> | effort: <level> | <task>
    - files: ...
    - result: ...
    - usage: (user fills from /cost or /status)
    - handoff: <none | request for the other agent>

Then commit with message "[claude] ..." or "[codex] ...".

## Listing rule
AI-assisted assets must be disclosed per each marketplace's current policy; never claim hand-drawn if AI-assisted.

## Stop and ask first
sudo, installs, network uploads, deleting files, changing the style spec.
