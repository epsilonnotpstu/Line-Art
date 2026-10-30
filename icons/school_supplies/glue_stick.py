import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, rrect, save

save(canvas(
    rrect(186, 40, 140, 100, 20),
    line(216, 70, 216, 110), line(256, 70, 256, 110), line(296, 70, 296, 110),
    rrect(166, 140, 180, 280, 16),
    line(166, 230, 346, 230), line(166, 330, 346, 330),
    rrect(186, 420, 140, 54, 12),
    line(226, 436, 226, 458), line(286, 436, 286, 458),
), __file__)
