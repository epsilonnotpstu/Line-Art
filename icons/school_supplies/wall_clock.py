import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, line, save

save(canvas(
    circle(256, 256, 210),
    line(256, 70, 256, 100), line(256, 412, 256, 442),
    line(70, 256, 100, 256), line(412, 256, 442, 256),
    line(256, 256, 256, 140), line(256, 256, 340, 300),
    circle(256, 256, 8),
), __file__)
