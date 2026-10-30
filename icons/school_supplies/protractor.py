import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from math import cos, sin, radians
from style import canvas, line, path, save

CX, CY = 256, 370
ticks = [line(CX + 216 * cos(radians(a)), CY - 216 * sin(radians(a)),
              CX + 176 * cos(radians(a)), CY - 176 * sin(radians(a)))
         for a in (30, 60, 90, 120, 150)]

save(canvas(
    path("M40 370 A216 216 0 0 1 472 370 Z"),
    path("M116 370 A140 140 0 0 1 396 370"),
    *ticks,
), __file__)
