import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, line, rrect, save

save(canvas(
    rrect(112, 52, 288, 408, 24),
    line(168, 52, 168, 460),
    line(100, 130, 124, 130), line(100, 220, 124, 220),
    line(100, 310, 124, 310), line(100, 400, 124, 400),
    rrect(224, 120, 120, 80, 12),
    line(224, 270, 344, 270), line(224, 330, 320, 330),
), __file__)
