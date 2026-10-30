#!/usr/bin/env python3
"""Render one labeled PNG grid for a collection."""
import argparse
import math
import tempfile

from PIL import Image, ImageDraw, ImageFont

from common import ROOT, collection, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection")
    args = parser.parse_args()
    try:
        name, files = collection(args.collection)
        columns = min(5, math.ceil(math.sqrt(len(files))))
        cell = 224
        label_height = max(48, 16 * math.ceil(max(len(f.name) for f in files) / 24) + 8)
        sheet = Image.new("RGB", (columns * cell, math.ceil(len(files) / columns) * (cell + label_height)), "white")
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.load_default(size=14)
        with tempfile.TemporaryDirectory(prefix="line-art-sheet-") as work:
            for index, file in enumerate(files):
                png = f"{work}/{index}.png"
                run(["inkscape", file.resolve(), "--export-area-page", "--export-width=200",
                     "--export-background-opacity=0", f"--export-filename={png}"], work)
                with Image.open(png) as opened:
                    icon = opened.convert("RGBA")
                icon.thumbnail((200, 200))
                x, y = index % columns * cell, index // columns * (cell + label_height)
                sheet.paste(icon, (x + (cell - icon.width) // 2, y + 12), icon)
                label = file.name
                # Wrap long filenames without dropping characters.
                lines = [label[i:i + 24] for i in range(0, len(label), 24)]
                for row, line in enumerate(lines):
                    draw.text((x + cell // 2, y + cell + row * 16), line, fill="black", font=font, anchor="mt")
        output = ROOT / "previews" / f"{name}_sheet.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(output)
        print(f"Contact sheet: {output}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Contact sheet failed: {error}\n")


if __name__ == "__main__":
    main()
