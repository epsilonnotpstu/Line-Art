import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, path, save

save(canvas(
    path("M230 300 L230 160 A40 40 0 0 1 310 160 L310 380 A60 60 0 0 1 190 380 "
         "L190 120 A80 80 0 0 1 350 120 L350 400"),
), __file__)
