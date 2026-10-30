import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, polyline, rrect, save

save(canvas(
    rrect(50, 70, 412, 300, 16),
    rrect(80, 100, 352, 240, 6),
    rrect(70, 370, 372, 30, 8),
    line(130, 400, 100, 474), line(382, 400, 412, 474),
    polyline([(130, 240), (170, 170), (210, 240), (250, 170)]),
    line(300, 170, 380, 170), line(300, 240, 350, 240),
), __file__)
