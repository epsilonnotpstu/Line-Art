import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, line, path, polyline, rrect, save

save(canvas(
    line(256, 40, 256, 66),
    circle(256, 86, 20),
    line(246, 104, 150, 380), line(150, 380, 130, 462),
    line(266, 104, 365, 340),
    rrect(340, 340, 50, 60, 6),
    polyline([(340, 400), (390, 400), (365, 462)], closed=True),
    path("M195 250 Q261 300 327 250"),
), __file__)
