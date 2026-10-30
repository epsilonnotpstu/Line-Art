import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, path, rrect, save

save(canvas(
    rrect(206, 40, 100, 50, 10),
    line(236, 55, 236, 75), line(276, 55, 276, 75),
    path("M216 90 L216 130 Q160 160 160 220 L160 450 Q160 474 184 474 "
         "L328 474 Q352 474 352 450 L352 220 Q352 160 296 130 L296 90 Z"),
    line(160, 270, 352, 270), line(160, 390, 352, 390),
), __file__)
