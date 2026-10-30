import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, path, save

save(canvas(
    path("M256 120 C200 80 120 80 56 100 L56 400 C120 380 200 380 256 420 Z"),
    path("M256 120 C312 80 392 80 456 100 L456 400 C392 380 312 380 256 420 Z"),
    line(100, 170, 210, 170), line(100, 230, 210, 230),
    line(302, 170, 412, 170), line(302, 230, 412, 230),
), __file__)
