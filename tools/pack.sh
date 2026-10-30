#!/usr/bin/env bash
set -euo pipefail
[[ $# == 1 ]] || { echo 'Usage: tools/pack.sh <collection>' >&2; exit 2; }
root=$(cd "$(dirname "$0")/.." && pwd)
"$root/tools/export.sh" "$1"
python3 "$root/tools/contact_sheet.py" "$1"
name=$(basename "$1")
out="$root/export/$name"
# Keep an edited license; the default stub clearly requires seller review.
if [[ ! -f "$out/LICENSE.txt" ]]; then
    cat > "$out/LICENSE.txt" <<'LICENSE'
LICENSE STUB — REPLACE BEFORE DISTRIBUTION
Copyright holder: [SELLER NAME]
Permitted use: [DEFINE PERSONAL / COMMERCIAL USE]
Restrictions: [DEFINE REDISTRIBUTION / RESALE TERMS]
AI assistance: [DISCLOSE PER THE TARGET MARKETPLACE'S CURRENT POLICY]
This placeholder grants no license. Complete and review before selling.
LICENSE
fi
mkdir -p "$root/dist"
# A fresh archive avoids retaining files removed from the collection.
python3 - "$root" "$1" "$out" "$root/previews/${name}_sheet.png" "$root/dist/$name.zip" <<'PY'
from pathlib import Path
import sys
import zipfile

root, collection, source, preview, target = map(Path, sys.argv[1:])
if not collection.is_dir():
    collection = root / 'icons' / collection
files = [source / 'LICENSE.txt', preview]
for svg in sorted(collection.glob('*.svg')):
    files.extend((source / svg.name).with_suffix(suffix) for suffix in ('.svg', '.png', '.eps'))
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for file in files:
        archive.write(file, file.name)
print(f'Bundle: {target}')
PY
