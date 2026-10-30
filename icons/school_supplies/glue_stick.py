import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, rrect, save

save(canvas(
    rrect(176, 40, 160, 100, 24),
    rrect(150, 140, 212, 60, 12),
    rrect(150, 200, 212, 270, 30),
    line(150, 270, 362, 270), line(150, 400, 362, 400),
    line(226, 40, 226, 100),
), __file__)
