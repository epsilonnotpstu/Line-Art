import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, polyline, save

save(canvas(
    polyline([(330, 46), (374, 66), (222, 345), (190, 330)], closed=True),
    polyline([(182, 46), (138, 66), (290, 345), (322, 330)], closed=True),
    circle(150, 400, 58), circle(362, 400, 58), circle(256, 236, 6),
), __file__)
