import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, line, rrect, save

save(canvas(
    rrect(50, 150, 412, 220, 28),
    circle(160, 260, 55),
    circle(160, 260, 22),
    rrect(280, 215, 130, 90, 8),
    circle(310, 260, 8), circle(380, 260, 8),
    line(215, 260, 280, 260),
), __file__)
