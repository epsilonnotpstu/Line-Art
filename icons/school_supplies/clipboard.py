import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, polyline, rrect, save

save(canvas(
    rrect(100, 70, 312, 404, 24),
    rrect(196, 40, 120, 60, 12),
    polyline([(150, 200), (170, 220), (205, 180)]),
    line(240, 200, 362, 200),
    polyline([(150, 290), (170, 310), (205, 270)]),
    line(240, 290, 362, 290),
    line(150, 390, 362, 390),
), __file__)
