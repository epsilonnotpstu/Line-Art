import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, rrect, save

ticks = [line(x, 150, x, 150 + (64 if i % 2 == 0 else 38))
         for i, x in enumerate(range(84, 440, 44))]
save(canvas(rrect(40, 150, 432, 212, 24), *ticks), __file__)
