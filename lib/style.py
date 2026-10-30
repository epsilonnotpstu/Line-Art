"""Shared outline-icon style. Every icon is built through these helpers.

Style lives on the single top-level <g>; shapes carry geometry only.
No transforms are emitted (QA rejects them): bake geometry instead.
Strokes are centered on geometry, so keep geometry inside LO..HI to
satisfy the 32px safe margin for the visible bounds.
"""
from pathlib import Path

SIZE = 512
STROKE = 12
MARGIN = 32
LO = MARGIN + STROKE / 2          # 38: min geometry coordinate
HI = SIZE - LO                    # 474: max geometry coordinate

_G_ATTRS = (f'fill="none" stroke="#000000" stroke-width="{STROKE}" '
            'stroke-linecap="round" stroke-linejoin="round"')


def _n(v):
    """Compact number: 12.0 -> '12', 12.345678 -> '12.3457'."""
    s = f"{float(v):.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _pts(points):
    return " ".join(f"{_n(x)},{_n(y)}" for x, y in points)


def canvas(*shapes):
    """Full SVG document wrapping the shapes in one styled top-level <g>."""
    inner = "\n".join(f"    {s}" for s in shapes)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {SIZE} {SIZE}" width="{SIZE}" height="{SIZE}">\n'
            f'  <g {_G_ATTRS}>\n{inner}\n  </g>\n</svg>\n')


def line(x1, y1, x2, y2):
    return f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}"/>'


def rect(x, y, w, h):
    return f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}"/>'


def rrect(x, y, w, h, r):
    return (f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" '
            f'rx="{_n(r)}" ry="{_n(r)}"/>')


def circle(cx, cy, r):
    return f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(r)}"/>'


def ellipse(cx, cy, rx, ry):
    return f'<ellipse cx="{_n(cx)}" cy="{_n(cy)}" rx="{_n(rx)}" ry="{_n(ry)}"/>'


def polyline(points, closed=False):
    tag = "polygon" if closed else "polyline"
    return f'<{tag} points="{_pts(points)}"/>'


def path(d):
    return f'<path d="{" ".join(d.split())}"/>'


def group(*shapes):
    """Plain nested <g> for organising shapes (no attributes, no transform).

    Returned as a single string; canvas() still emits the one styled top-level <g>.
    """
    return "<g>" + "".join(shapes) + "</g>"


def save(svg, script_file, name=None):
    """Write svg next to the calling script: save(svg, __file__)."""
    script = Path(script_file)
    out = script.with_name((name or script.stem) + ".svg")
    out.write_text(svg, encoding="utf-8")
    return out
