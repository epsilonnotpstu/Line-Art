import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, path, rrect, save

save(canvas(
    circle(256, 64, 22),
    path("M130 330 C130 160 190 90 256 90 C322 90 382 160 382 330 Z"),
    rrect(90, 330, 332, 40, 16),
    circle(256, 418, 32),
), __file__)
