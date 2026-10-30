"""Small shared helpers for collection paths and quiet external commands."""
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*")


def collection(value):
    source = Path(value)
    if not source.is_dir():
        source = ROOT / "icons" / value
    if not source.is_dir() or not NAME.fullmatch(source.name):
        raise ValueError("collection must be a directory with a snake_case name")
    files = sorted(source.glob("*.svg"))
    if not files:
        raise ValueError("collection contains no SVG files")
    return source.name, files


def run(args, profile):
    env = dict(os.environ, INKSCAPE_PROFILE_DIR=str(profile))
    result = subprocess.run([str(a) for a in args], capture_output=True, env=env)
    if result.returncode:
        raise ValueError(f"{Path(args[0]).name} failed (exit {result.returncode})")
    return result.stdout.decode("utf-8")
