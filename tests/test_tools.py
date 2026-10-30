"""Run with python3 -m unittest discover -s tests -v. No production icons used."""
import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from qa import check

SVG = "{http://www.w3.org/2000/svg}"
FIXTURE = ROOT / "tests/fixtures/outline_box.svg"


class ToolsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "tests/fixtures", prefix="tool_test_")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        shutil.copytree(ROOT / "tools", self.work / "tools", ignore=shutil.ignore_patterns("__pycache__"))
        (self.work / "listing").mkdir()
        shutil.copy(ROOT / "listing/make_csv.py", self.work / "listing")
        self.source = self.work / "fixtures"
        self.source.mkdir()
        self.svg = self.source / "outline_box.svg"
        shutil.copy(FIXTURE, self.svg)
        self.env = dict(os.environ)

    def run_tool(self, name, *args, success=True):
        script = self.work / name
        runner = ["bash"] if script.suffix == ".sh" else [sys.executable]
        result = subprocess.run([*runner, str(script), *map(str, args)], cwd=self.work,
                                env=self.env, capture_output=True, text=True, timeout=60)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def write_svg(self, mutate):
        root = ET.parse(FIXTURE).getroot()
        mutate(root)
        ET.ElementTree(root).write(self.svg, encoding="utf-8")

    def local_svgo(self):
        self.assertTrue((ROOT / "node_modules/.bin/svgo").is_file(), "local SVGO is required")
        (self.work / "node_modules").symlink_to(ROOT / "node_modules", target_is_directory=True)

    def test_environment_report(self):
        report = self.run_tool("tools/check_env.sh").stdout
        for name in ("inkscape", "potrace", "rsvg-convert", "npx", "svgo", "python3", "PIL", "zip"):
            self.assertIn(name + ":", report)

    def test_qa_valid_inheritance_and_page_units(self):
        self.assertEqual(check(self.svg, self.work), [])
        self.write_svg(lambda root: root.set("width", "1024"))
        self.assertEqual(check(self.svg, self.work), [])
        result = self.run_tool("tools/qa.py", self.source)
        self.assertIn("PASS: 1 FAIL: 0", result.stdout)

    def test_qa_rejections(self):
        mutations = {
            "viewBox": lambda r: r.set("viewBox", "0 0 100 100"),
            "stroke-width": lambda r: r.set("stroke-width", "10"),
            "stroke must": lambda r: r.set("stroke", "red"),
            "fill must": lambda r: r.set("fill", "white"),
            "stroke-linecap": lambda r: r.set("stroke-linecap", "square"),
            "stroke-linejoin": lambda r: r.set("stroke-linejoin", "bevel"),
            "safe margin": lambda r: r.find(f".//{SVG}rect").set("x", "32"),
            "empty g": lambda r: ET.SubElement(r.find(SVG + "g"), SVG + "g"),
            "empty or degenerate path": lambda r: ET.SubElement(r.find(SVG + "g"), SVG + "path", d="M 50 50"),
            "top-level g": lambda r: ET.SubElement(r, SVG + "g"),
            "transforms": lambda r: r.find(SVG + "g").set("transform", "scale(2)"),
            "base64": lambda r: r.find(SVG + "g").set("data-source", "data:;base64,SECRET_SENTINEL"),
            "stroke must be #000000": lambda r: r.find(SVG + "g").set("style", "stroke:red"),
        }
        for tag in ("image", "text", "filter", "clipPath", "linearGradient", "radialGradient", "style", "use"):
            mutations[f"forbidden element: {tag}"] = lambda r, tag=tag: ET.SubElement(r.find(SVG + "g"), SVG + tag)
        for expected, mutate in mutations.items():
            with self.subTest(expected=expected):
                self.write_svg(mutate)
                self.assertTrue(any(expected in error for error in check(self.svg, self.work)))
        result = self.run_tool("tools/qa.py", self.svg, success=False)
        self.assertIn("FAIL: 1", result.stdout)
        self.assertNotIn("<svg", result.stdout)
        self.svg.write_text("<svg>SECRET_SENTINEL")
        result = self.run_tool("tools/qa.py", self.svg, success=False)
        self.assertNotIn("SECRET_SENTINEL", result.stdout + result.stderr)
        self.run_tool("tools/qa.py", self.work / "missing.svg", success=False)
        empty = self.work / "empty"
        empty.mkdir()
        self.run_tool("tools/qa.py", empty, success=False)

    def test_traced_profile_retains_safety_checks(self):
        def filled(root):
            root.set("fill", "#000000")
            root.set("stroke", "none")
            root.set("data-traced", "true")
            root.find(SVG + "g").set("transform", "translate(0 0)")

        self.write_svg(filled)
        self.assertEqual(check(self.svg, self.work, traced=True), [])
        self.run_tool("tools/qa.py", self.svg, success=False)
        mutations = {
            "viewBox": lambda r: r.set("viewBox", "0 0 256 256"),
            "safe margin": lambda r: r.find(SVG + "g").set("transform", "translate(-40 0)"),
            "empty g": lambda r: ET.SubElement(r.find(SVG + "g"), SVG + "g"),
            "empty or degenerate path": lambda r: ET.SubElement(r.find(SVG + "g"), SVG + "path"),
            "top-level g": lambda r: ET.SubElement(r, SVG + "g"),
            "base64": lambda r: r.set("data-source", "data:;base64,PRIVATE"),
            "traced fill": lambda r: r.set("fill", "red"),
        }
        for tag in ("image", "text", "filter", "clipPath", "linearGradient", "radialGradient"):
            mutations[f"forbidden element: {tag}"] = lambda r, tag=tag: ET.SubElement(r.find(SVG + "g"), SVG + tag)
        for expected, mutate in mutations.items():
            with self.subTest(expected=expected):
                def change(root):
                    filled(root)
                    mutate(root)
                self.write_svg(change)
                self.assertTrue(any(expected in error for error in check(self.svg, self.work, traced=True)))

    def assert_exports(self):
        output = self.work / "export/fixtures"
        self.assertTrue((output / "outline_box.svg").is_file())
        with Image.open(output / "outline_box.png") as image:
            self.assertEqual(image.size, (1024, 1024))
            self.assertEqual(image.mode, "RGBA")
            self.assertEqual(image.getpixel((0, 0))[3], 0)
            self.assertEqual(image.getchannel("A").getextrema(), (0, 255))
        self.assertTrue((output / "outline_box.eps").read_bytes().startswith(b"%!PS-Adobe"))
        self.assertEqual(check(output / "outline_box.svg", self.work), [])

    def test_export_and_pack_local_svgo(self):
        self.local_svgo()
        self.run_tool("tools/export.sh", self.source)
        self.assert_exports()
        output = self.work / "export/fixtures"
        # Old exports must not leak into a new package.
        (output / "stale.svg").write_text("stale")
        self.run_tool("tools/pack.sh", self.source)
        with zipfile.ZipFile(self.work / "dist/fixtures.zip") as archive:
            self.assertEqual(set(archive.namelist()), {"outline_box.svg", "outline_box.png", "outline_box.eps", "fixtures_sheet.png", "LICENSE.txt"})
            self.assertIsNone(archive.testzip())
            self.assertIn(b"REPLACE BEFORE DISTRIBUTION", archive.read("LICENSE.txt"))
        (output / "LICENSE.txt").write_text("Seller reviewed terms")
        self.run_tool("tools/pack.sh", self.source)
        with zipfile.ZipFile(self.work / "dist/fixtures.zip") as archive:
            self.assertEqual(archive.read("LICENSE.txt"), b"Seller reviewed terms")

    def test_real_svgo(self):
        self.local_svgo()
        # Prove that optimization really runs rather than just copying the input.
        with self.svg.open("a") as stream:
            stream.write("<!--svgo_removable_comment-->")
        self.run_tool("tools/export.sh", self.source)
        self.assert_exports()
        self.assertNotIn(b"svgo_removable_comment", (self.work / "export/fixtures/outline_box.svg").read_bytes())

    def test_export_dependency_failure(self):
        result = self.run_tool("tools/export.sh", self.source, success=False)
        self.assertIn("SVGO unavailable", result.stderr)
        self.assertFalse((self.work / "export").exists())

    def test_contact_sheet(self):
        shutil.copy(self.svg, self.source / "second_box.svg")
        self.run_tool("tools/contact_sheet.py", self.source)
        with Image.open(self.work / "previews/fixtures_sheet.png") as image:
            self.assertEqual(image.size, (448, 272))
            self.assertIsNotNone(image.crop((0, 224, 224, 272)).convert("L").point(lambda p: 255 - p).getbbox())

    def test_trace_options_and_transparency(self):
        raw = self.work / "raw"
        raw.mkdir()
        png = raw / "trace_box.png"
        image = Image.new("RGBA", (120, 100), (0, 0, 0, 0))
        ImageDraw.Draw(image).rectangle((30, 20, 90, 80), fill=(100, 100, 100, 255))
        image.save(png)
        original = png.read_bytes()
        self.run_tool("tools/trace.py", "--threshold", "90", success=False)
        self.run_tool("tools/trace.py", "--threshold", "128", "--scale", "0.8")
        traced = self.work / "export/traced/trace_box.svg"
        root = ET.parse(traced).getroot()
        self.assertEqual(root.get("viewBox"), "0 0 512 512")
        self.assertEqual(root.find(SVG + "g").get("fill"), "#000000")
        self.assertTrue(root.findall(f".//{SVG}path"))
        self.assertTrue(any("fill must be none" in e for e in check(traced, self.work)))
        self.assertEqual(check(traced, self.work, traced=True), [])
        self.run_tool("tools/qa.py", "--traced", traced)
        self.assertEqual(root.get("data-traced"), "true")
        # One collection can contain both traced fills and strict outline icons.
        shutil.copy(traced, self.source / traced.name)
        self.local_svgo()
        self.run_tool("tools/export.sh", self.source)
        optimized = self.work / "export/fixtures/trace_box.svg"
        self.assertEqual(ET.parse(optimized).getroot().get("data-traced"), "true")
        self.assertEqual(check(optimized, self.work, traced=True), [])
        self.assert_exports()
        rendered = self.work / "traced.png"
        subprocess.run(["inkscape", str(traced), f"--export-filename={rendered}"], capture_output=True, check=True)
        with Image.open(rendered) as image:
            alpha = image.getchannel("A")
            left, top, right, bottom = alpha.getbbox()
            self.assertTrue(75 <= left <= 78 and 434 <= right <= 437)
            self.assertEqual(image.getpixel((256, 256)), (0, 0, 0, 255))
            self.assertEqual(image.getpixel((0, 0))[3], 0)
        self.assertEqual(png.read_bytes(), original)
        self.run_tool("tools/trace.py", "--output", raw, success=False)
        self.run_tool("tools/trace.py", "--output", self.work / "lib", success=False)
        # Explicitly authorized icon destinations are supported; defaults stay in export/.
        for collection in ("farm_animals", "food"):
            destination = self.work / "icons" / collection
            self.run_tool("tools/trace.py", png, "--output", destination)
            self.assertTrue((destination / "trace_box.svg").is_file())
        self.run_tool("tools/trace.py", "--scale", "2", success=False)

    def test_listing_csv(self):
        source = self.work / "listing/fixtures.json"
        item = {"filename": "outline_box.svg", "title": 'Box, "outline"',
                "description": "A box.\nEducational outline.", "keywords": ["box", "school", "box"]}
        source.write_text(json.dumps({"items": [item]}))
        self.run_tool("listing/make_csv.py", "fixtures")
        with source.with_suffix(".csv").open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(rows[0]["title"], item["title"])
        self.assertEqual(rows[0]["description"], item["description"])
        self.assertEqual(rows[0]["keywords"], "box, school")
        self.assertEqual(rows[0]["ai_assisted"], "true")
        for key, value in (("title", "hand-drawn box"), ("description", "=formula"), ("keywords", [])):
            with self.subTest(key=key):
                source.write_text(json.dumps([dict(item, **{key: value})]))
                self.run_tool("listing/make_csv.py", "fixtures", success=False)


if __name__ == "__main__":
    unittest.main()
