import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, polyline, rrect, save

save(canvas(
    polyline([(206, 130), (256, 40), (306, 130)], closed=True),
    rrect(206, 130, 100, 344, 10),
    line(206, 200, 306, 200), line(206, 410, 306, 410),
    polyline([(206, 305), (231, 275), (256, 305), (281, 275), (306, 305)]),
), __file__)
