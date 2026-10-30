#!/usr/bin/env bash
# Accept an icons/<collection> name or an explicit collection directory.
set -euo pipefail
[[ $# == 1 ]] || { echo 'Usage: tools/export.sh <collection>' >&2; exit 2; }
root=$(cd "$(dirname "$0")/.." && pwd)
source=$1
[[ -d "$source" ]] || source="$root/icons/$1"
name=$(basename "$source")
[[ -d "$source" && "$name" =~ ^[a-z][a-z0-9]*(_[a-z0-9]+)*$ ]] || {
    echo 'Invalid collection directory/name' >&2; exit 2;
}
for tool in python3 npx inkscape; do
    command -v "$tool" >/dev/null || { echo "Missing: $tool" >&2; exit 1; }
done
shopt -s nullglob
files=("$source"/*.svg)
[[ ${#files[@]} -gt 0 ]] || { echo 'Collection has no top-level SVG files' >&2; exit 1; }
python3 "$root/tools/qa.py" "$source"
if ! npx --offline --no-install svgo --version >/dev/null 2>&1; then
    echo 'SVGO unavailable locally via npx; export requires SVGO.' >&2
    exit 1
fi
mkdir -p "$root/export/$name"
for file in "${files[@]}"; do
    stem=$(basename "$file" .svg)
    target="$root/export/$name/$stem"
    npx --offline --no-install svgo --config "$root/tools/svgo.config.mjs" \
        --input "$file" --output "$target.svg" --quiet
    python3 "$root/tools/qa.py" "$target.svg"
    inkscape "$target.svg" --export-area-page --export-width=1024 --export-height=1024 \
        --export-background-opacity=0 --export-filename="$target.png" >/dev/null 2>&1
    inkscape "$target.svg" --export-area-page --export-type=eps \
        --export-filename="$target.eps" >/dev/null 2>&1
    printf 'Exported %s (SVG, PNG, EPS)\n' "$stem"
done
