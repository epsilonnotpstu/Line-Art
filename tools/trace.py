#!/usr/bin/env python3
"""Threshold PNGs and trace filled shapes; raw/ is always read-only."""
import argparse
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image

from common import NAME, ROOT, run

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path, help="default: raw/*.png")
    parser.add_argument("--output", type=Path, default=ROOT / "export" / "traced",
                        help="destination; use icons/ only with explicit ownership authorization")
    parser.add_argument("--threshold", type=int, default=128, help="black cutoff, 1..255")
    parser.add_argument("--scale", type=float, default=1.0, help="centered scale, >0 and <=1; artwork fits within 448px")
    args = parser.parse_args()
    if not 1 <= args.threshold <= 255 or not 0 < args.scale <= 1:
        parser.error("threshold must be 1..255 and scale must be >0 and <=1")
    files = args.files or sorted((ROOT / "raw").glob("*.png"))
    if not files:
        parser.error("no PNG inputs found")
    output = args.output.resolve()
    protected = [(ROOT / directory).resolve() for directory in ("raw", "lib")]
    if any(output == p or p in output.parents for p in protected):
        parser.error("output must be outside raw/ and lib/")
    try:
        for file in files:
            if not NAME.fullmatch(file.stem):
                raise ValueError("input filenames must be snake_case")
            with tempfile.TemporaryDirectory(prefix="line-art-trace-") as work:
                bitmap, traced = Path(work) / "input.pbm", Path(work) / "trace.svg"
                with Image.open(file) as opened:
                    rgba = opened.convert("RGBA")
                    white = Image.new("RGBA", rgba.size, "white")
                    gray = Image.alpha_composite(white, rgba).convert("L")
                binary = gray.point(lambda value: 0 if value < args.threshold else 255, mode="1")
                # Crop to the ink so differently padded raw images have equal scale.
                bounds = binary.convert("L").point(lambda value: 255 - value).getbbox()
                if bounds is None:
                    raise ValueError(f"{file.name}: threshold produced no black pixels")
                binary = binary.crop(bounds)
                binary.save(bitmap)
                run(["potrace", bitmap, "--svg", "--output", traced], work)
                source = ET.parse(traced).getroot()
                if not source.findall(f".//{{{SVG}}}path"):
                    raise ValueError(f"{file.name}: potrace produced no paths")
                _, _, width, height = map(float, source.get("viewBox").split())
                factor = 448 * args.scale / max(width, height)
                x, y = (512 - width * factor) / 2, (512 - height * factor) / 2
                root = ET.Element(f"{{{SVG}}}svg", viewBox="0 0 512 512", width="512", height="512")
                root.set("data-traced", "true")
                group = ET.SubElement(root, f"{{{SVG}}}g", fill="#000000", stroke="none",
                                      transform=f"translate({x:g} {y:g}) scale({factor:g})")
                for child in source:
                    if child.tag == f"{{{SVG}}}g":
                        child.attrib.pop("fill", None)
                        child.attrib.pop("stroke", None)
                        group.append(child)
                output.mkdir(parents=True, exist_ok=True)
                ET.ElementTree(root).write(output / f"{file.stem}.svg", encoding="utf-8", xml_declaration=True)
                print(f"Traced {file.name}: filled black SVG (threshold={args.threshold}, scale={args.scale:g})")
    except (OSError, ValueError, ET.ParseError) as error:
        parser.exit(1, f"Trace failed: {error}\n")


if __name__ == "__main__":
    main()
