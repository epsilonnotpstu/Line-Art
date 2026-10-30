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
for tool in python3 inkscape; do
    command -v "$tool" >/dev/null || { echo "Missing: $tool" >&2; exit 1; }
done
shopt -s nullglob
files=("$source"/*.svg)
[[ ${#files[@]} -gt 0 ]] || { echo 'Collection has no top-level SVG files' >&2; exit 1; }
svgo="$root/node_modules/.bin/svgo"
if [[ ! -x "$svgo" ]] || ! "$svgo" --version >/dev/null 2>&1; then
    echo 'SVGO unavailable: expected executable node_modules/.bin/svgo.' >&2
    exit 1
fi
mkdir -p "$root/export/$name"
for file in "${files[@]}"; do
    qa_flags=()
    if python3 -c 'import sys, xml.etree.ElementTree as E; sys.exit(E.parse(sys.argv[1]).getroot().get("data-traced") != "true")' "$file" 2>/dev/null; then
        qa_flags=(--traced)
    fi
    python3 "$root/tools/qa.py" "${qa_flags[@]}" "$file"
    stem=$(basename "$file" .svg)
    target="$root/export/$name/$stem"
    "$svgo" --config "$root/tools/svgo.config.mjs" \
        --input "$file" --output "$target.svg" --quiet
    python3 "$root/tools/qa.py" "${qa_flags[@]}" "$target.svg"
    inkscape "$target.svg" --export-area-page --export-width=1024 --export-height=1024 \
        --export-background-opacity=0 --export-filename="$target.png" >/dev/null 2>&1
    inkscape "$target.svg" --export-area-page --export-type=eps \
        --export-filename="$target.eps" >/dev/null 2>&1
    printf 'Exported %s (SVG, PNG, EPS)\n' "$stem"
done
