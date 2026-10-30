import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, polyline, rrect, save

save(canvas(
    polyline([(236, 40), (276, 40), (296, 100), (216, 100)], closed=True),
    rrect(196, 100, 120, 40, 8),
    rrect(176, 140, 160, 334, 24),
    line(176, 250, 336, 250), line(176, 400, 336, 400),
), __file__)
