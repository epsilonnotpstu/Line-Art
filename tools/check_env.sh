#!/usr/bin/env bash
# Report only: never fetch packages or install anything.
set -u
report() {
    local label=$1
    shift
    if command -v "$1" >/dev/null 2>&1; then
        local version
        if version=$("$@" 2>/dev/null); then
            printf '%s: %s\n' "$label" "${version%%$'\n'*}"
        else
            printf '%s: present, version unavailable\n' "$label"
        fi
    else
        printf '%s: MISSING\n' "$label"
    fi
}
report inkscape inkscape --version
report potrace potrace --version
report rsvg-convert rsvg-convert --version
report npx npx --version
if command -v npx >/dev/null 2>&1; then
    if version=$(npx --offline --no-install svgo --version 2>/dev/null); then
        printf 'svgo: %s\n' "$version"
    else
        printf 'svgo: MISSING (not available locally via npx)\n'
    fi
else
    printf 'svgo: MISSING (requires npx)\n'
fi
report python3 python3 --version
if command -v python3 >/dev/null 2>&1; then
    if version=$(python3 -c 'import PIL; print(PIL.__version__)' 2>/dev/null); then
        printf 'PIL: %s\n' "$version"
    else
        printf 'PIL: MISSING\n'
    fi
else
    printf 'PIL: unavailable (requires python3)\n'
fi
if command -v zip >/dev/null 2>&1; then
    version=$(zip -v 2>/dev/null)
    while IFS= read -r line; do
        if [[ "$line" == *'This is Zip '* ]]; then
            printf 'zip: %s\n' "$line"
            break
        fi
    done <<< "$version"
else
    printf 'zip: MISSING\n'
fi
