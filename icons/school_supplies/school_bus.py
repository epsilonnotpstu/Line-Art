import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, line, path, rrect, save

save(canvas(
    path("M102 390 L70 390 Q40 390 40 360 L40 150 Q40 120 70 120 L442 120 "
         "Q472 120 472 150 L472 360 Q472 390 442 390 L410 390"),
    line(178, 390, 334, 390),
    *[rrect(x, 160, 70, 70, 8) for x in (64, 154, 244, 334)],
    line(40, 290, 472, 290),
    circle(140, 390, 38), circle(372, 390, 38),
), __file__)
