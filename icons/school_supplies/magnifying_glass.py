import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, path, polyline, save

save(canvas(
    circle(210, 210, 150),
    path("M130 190 A85 85 0 0 1 190 130"),
    polyline([(312, 340), (340, 312), (454, 426), (426, 454)], closed=True),
), __file__)
