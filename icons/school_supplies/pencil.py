import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from style import canvas, polyline, save

A, S = math.radians(45), 1.2


def P(u, v):
    """Pencil-local (length, width) -> canvas coords, rotated 45 deg."""
    u, v = u * S, v * S
    return (256 + u * math.cos(A) + v * math.sin(A), 256 - u * math.sin(A) + v * math.cos(A))


def seg(u1, v1, u2, v2):
    return polyline([P(u1, v1), P(u2, v2)])


svg = canvas(
    polyline([P(-200, 0), P(-130, -44), P(200, -44), P(200, 44), P(-130, 44)], closed=True),
    seg(-130, -44, -130, 44),
    seg(-200, 0, -165, 0),
    seg(120, -44, 120, 44),
    seg(160, -44, 160, 44),
)
save(svg, __file__)
