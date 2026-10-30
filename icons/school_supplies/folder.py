import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, polyline, save

save(canvas(
    polyline([(50, 110), (200, 110), (240, 160), (462, 160), (462, 420), (50, 420)], closed=True),
    line(50, 230, 462, 230),
), __file__)
