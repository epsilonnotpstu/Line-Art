import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, path, rrect, save

save(canvas(
    path("M170 170 L170 110 Q170 80 200 80 L312 80 Q342 80 342 110 L342 170"),
    rrect(50, 170, 412, 280, 30),
    line(50, 290, 462, 290),
    rrect(216, 265, 80, 50, 8),
), __file__)
