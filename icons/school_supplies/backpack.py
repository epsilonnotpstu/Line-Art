import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, path, rrect, save

save(canvas(
    path("M150 170 C150 90 362 90 362 170"),
    rrect(116, 150, 280, 320, 60),
    rrect(176, 320, 160, 110, 20),
    line(176, 370, 336, 370),
    path("M210 150 C210 120 302 120 302 150"),
    line(116, 260, 80, 260), line(396, 260, 432, 260),
), __file__)
