import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, rrect, save

btn = [circle(x, y, 8) for y in (270, 340, 410) for x in (180, 256, 332)]
save(canvas(
    rrect(106, 46, 300, 420, 32),
    rrect(150, 90, 212, 76, 12),
    *btn,
), __file__)
