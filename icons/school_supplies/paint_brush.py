import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, path, polyline, rect, save

save(canvas(
    path("M256 40 C200 120 190 170 206 210 L306 210 C322 170 312 120 256 40 Z"),
    rect(206, 210, 100, 80),
    line(206, 250, 306, 250),
    polyline([(222, 290), (290, 290), (272, 474), (240, 474)], closed=True),
), __file__)
