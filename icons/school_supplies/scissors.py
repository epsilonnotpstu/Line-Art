import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, line, save

save(canvas(
    line(352, 46, 197, 341), line(160, 46, 315, 341),
    circle(150, 388, 66), circle(362, 388, 66), circle(256, 229, 6),
), __file__)
