import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, circle, ellipse, line, path, save

save(canvas(
    circle(256, 220, 170),
    ellipse(256, 220, 70, 170),
    line(86, 220, 426, 220),
    path("M110 130 C200 160 312 160 402 130"),
    path("M110 310 C200 280 312 280 402 310"),
    path("M256 390 L256 440"), path("M176 450 L336 450"),
), __file__)
