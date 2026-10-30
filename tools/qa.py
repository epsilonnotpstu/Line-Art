#!/usr/bin/env python3
"""Check outline or traced SVG style and visible bounds; never echo SVG data."""
import argparse
import math
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET

from common import NAME, run

SHAPES = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}
ALLOWED = SHAPES | {"svg", "g", "title", "desc"}
DEFAULTS = {"fill": "black", "stroke": "none", "stroke-width": "1",
            "stroke-linecap": "butt", "stroke-linejoin": "miter"}
NUMBER = r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?"


def number(value):
    return float(value.removesuffix("px"))


def path_draws(data):
    if re.search(r"[LlHhVvCcSsQqTtAa]", data):
        return True
    # Extra coordinate pairs after moveto are implicit lineto segments.
    moves = re.finditer(r"[Mm]([^MmLlHhVvCcSsQqTtAaZz]*)", data)
    return any(len(re.findall(NUMBER, move[1])) >= 4 for move in moves)


def check(path, profile, traced=False):
    errors = []
    if not NAME.fullmatch(path.stem):
        errors.append("filename must be snake_case")
    try:
        data = path.read_bytes()
        if any(token in data.upper() for token in (b"<!DOCTYPE", b"<!ENTITY", b"<?XML-STYLESHEET")):
            return errors + ["DOCTYPE, entities and XML stylesheets are forbidden"]
        root = ET.fromstring(data)
    except (OSError, ET.ParseError):
        return errors + ["cannot read valid XML"]
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        errors.append("root must be an SVG in the SVG namespace")
    try:
        if [float(n) for n in root.get("viewBox", "").replace(",", " ").split()] != [0, 0, 512, 512]:
            errors.append("viewBox must be 0 0 512 512")
    except ValueError:
        errors.append("invalid viewBox")
    if sum(child.tag == "{http://www.w3.org/2000/svg}g" for child in root) != 1:
        errors.append("exactly one top-level g is required")
    if any(child.tag.rsplit("}", 1)[-1] not in {"g", "title", "desc"} for child in root):
        errors.append("all drawing elements must be inside the top-level g")

    def visit(node, inherited):
        tag = node.tag.rsplit("}", 1)[-1]
        if tag not in ALLOWED or not node.tag.startswith("{http://www.w3.org/2000/svg}"):
            errors.append(f"forbidden element: {tag}")
        if tag == "svg" and node is not root:
            errors.append("nested SVG viewports are forbidden")
        style = dict(inherited)
        style.update({key: value.strip() for key, value in node.attrib.items()})
        for declaration in node.get("style", "").split(";"):
            if declaration.strip():
                key, separator, value = declaration.partition(":")
                if not separator:
                    errors.append("invalid inline style")
                style[key.strip()] = value.strip()
        if any("base64" in v.lower() or "url(" in v.lower() for v in node.attrib.values()):
            errors.append("base64 and URL references are forbidden")
        if any(k.rsplit("}", 1)[-1] in {"href", "class"} or k.startswith("on") for k in node.attrib):
            errors.append("references, CSS classes and event handlers are forbidden")
        if any(k in style and style[k] != "none" for k in ("filter", "clip-path", "mask")):
            errors.append("filter, clip-path and mask are forbidden")
        if any(k in style and style[k] != "1" for k in ("opacity", "stroke-opacity", "fill-opacity")) or style.get("display", "inline") == "none" or style.get("visibility", "visible") != "visible":
            errors.append("hidden or translucent elements are forbidden")
        if tag in SHAPES:
            expected = {} if traced else {"fill": "none", "stroke": "#000000",
                        "stroke-linecap": "round", "stroke-linejoin": "round"}
            for key, value in expected.items():
                if style.get(key) != value:
                    errors.append(f"{tag}: {key} must be {value}")
            if traced:
                for key in ("fill", "stroke"):
                    if style.get(key) not in {"none", "#000000"}:
                        errors.append(f"{tag}: traced {key} must be #000000 or none")
                if style.get("fill") == style.get("stroke") == "none":
                    errors.append(f"invisible {tag}")
            else:
                try:
                    if number(style["stroke-width"]) != 12:
                        raise ValueError
                except (ValueError, KeyError):
                    errors.append(f"{tag}: stroke-width must be 12")
            if not traced and any(key in style for key in ("transform", "vector-effect")):
                errors.append("transforms/vector-effect can alter the 12px stroke; bake geometry instead")
            empty = tag == "path" and not path_draws(node.get("d", ""))
            if tag in {"polygon", "polyline"}:
                empty = len(re.findall(NUMBER, node.get("points", ""))) < (6 if tag == "polygon" else 4)
            dimensions = {"rect": ("width", "height"), "circle": ("r",), "ellipse": ("rx", "ry")}
            try:
                empty |= any(number(node.get(k, "0")) <= 0 for k in dimensions.get(tag, ()))
            except ValueError:
                empty = True
            if tag == "line":
                empty = all(node.get(a, "0") == node.get(b, "0") for a, b in (("x1", "x2"), ("y1", "y2")))
            if empty:
                errors.append(f"empty or degenerate {tag}")
        elif tag in {"g", "svg"}:
            if not traced and "transform" in style:
                errors.append("group/root transforms must be baked into geometry")
            if not any(n.tag.rsplit("}", 1)[-1] in SHAPES for n in node.iter()):
                errors.append(f"empty {tag}")
        elif tag in {"title", "desc"} and not "".join(node.itertext()).strip():
            errors.append(f"empty {tag}")
        for child in node:
            visit(child, style)

    visit(root, DEFAULTS)
    if not errors:
        try:
            # Query in viewBox units even when the source uses a different page size.
            root.set("width", "512")
            root.set("height", "512")
            query_file = Path(profile) / "query.svg"
            ET.ElementTree(root).write(query_file, encoding="utf-8", xml_declaration=True)
            output = run(["inkscape", query_file, "--query-all"], profile)
            boxes = [list(map(float, row.rsplit(",", 4)[1:])) for row in output.splitlines() if row.strip()]
            if not boxes or any(len(b) != 4 or not all(map(math.isfinite, b)) for b in boxes):
                raise ValueError
            if any(x < 31.99 or y < 31.99 or x + w > 480.01 or y + h > 480.01 for x, y, w, h in boxes):
                errors.append("visible bounds violate the 32px safe margin")
        except (OSError, ValueError):
            errors.append("Inkscape bounding-box query failed")
    return list(dict.fromkeys(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traced", action="store_true", help="allow filled black traces and transforms; retain content and margin checks")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    files, failed, passed = set(), 0, 0
    for path in args.paths:
        found = list(path.rglob("*.svg")) if path.is_dir() else [path]
        if not found:
            print(f"FAIL {path}: no SVG files found")
            failed += 1
        files.update(found)
    with tempfile.TemporaryDirectory(prefix="line-art-qa-") as profile:
        for path in sorted(files):
            errors = check(path, profile, args.traced) if path.suffix.lower() == ".svg" else ["expected an SVG file"]
            for error in errors:
                print(f"FAIL {path}: {error}")
            failed += bool(errors)
            passed += not errors
    print(f"PASS: {passed} FAIL: {failed} (files/inputs)")
    return int(bool(failed))


if __name__ == "__main__":
    raise SystemExit(main())
