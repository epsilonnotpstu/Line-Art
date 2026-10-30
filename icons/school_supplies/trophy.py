import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from math import cos, sin, pi
from style import canvas, line, path, polyline, rrect, save

star = [(256 + (46 if i % 2 == 0 else 20) * cos(-pi / 2 + i * pi / 5),
         160 + (46 if i % 2 == 0 else 20) * sin(-pi / 2 + i * pi / 5)) for i in range(10)]

save(canvas(
    path("M160 70 L352 70 L352 200 Q352 290 256 290 Q160 290 160 200 Z"),
    path("M160 110 H100 Q90 110 90 120 Q90 200 170 230"),
    path("M352 110 H412 Q422 110 422 120 Q422 200 342 230"),
    line(256, 290, 256, 380),
    rrect(176, 380, 160, 40, 10), rrect(136, 420, 240, 54, 10),
    polyline(star, closed=True),
), __file__)
