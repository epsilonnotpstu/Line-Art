import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, polyline, save

save(canvas(
    polyline([(150, 130), (440, 270), (362, 410), (72, 270)], closed=True),
    line(295, 200, 217, 340),
    line(230, 450, 440, 450),
), __file__)
