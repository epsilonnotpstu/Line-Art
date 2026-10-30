import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, polyline, save

save(canvas(
    polyline([(56, 56), (56, 456), (456, 456)], closed=True),
    polyline([(136, 230), (136, 376), (282, 376)], closed=True),
    *[line(56, y, 86, y) for y in (130, 190, 250, 310, 370)],
    *[line(x, 456, x, 426) for x in (130, 190, 250, 310, 370)],
), __file__)
