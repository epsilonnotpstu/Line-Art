import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, line, path, polyline, rrect, save

save(canvas(
    path("M60 340 L60 290 Q60 250 110 240 L430 190 Q470 184 470 220 L470 340 Z"),
    circle(100, 295, 14),
    line(150, 270, 420, 232),
    rrect(40, 340, 432, 70, 14),
    polyline([(350, 440), (350, 468), (430, 468), (430, 440)]),
), __file__)
