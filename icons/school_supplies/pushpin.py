import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, polyline, rrect, save

save(canvas(
    rrect(196, 40, 120, 70, 16),
    polyline([(216, 110), (296, 110), (330, 230), (182, 230)], closed=True),
    rrect(142, 230, 228, 40, 14),
    line(256, 270, 256, 474),
    line(226, 150, 232, 190),
), __file__)
