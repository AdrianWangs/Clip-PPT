"""
Generate a cosine/angle/chord equivalence SVG (no text labels).
Draws a unit circle with two direction vectors, the arc between them,
and the chord, visualizing spherical k-means geometry without labels.

Output: figures/spherical_kmeans_equivalence_python.svg
"""

from __future__ import annotations

import math
import os
from typing import Tuple, List


def rotate2(theta: float, v: Tuple[float, float]) -> Tuple[float, float]:
    c, s = math.cos(theta), math.sin(theta)
    x, y = v
    return (c * x - s * y, s * x + c * y)


def polyline(points: List[Tuple[float, float]], stroke: str, width: float = 2.5) -> str:
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f"<polyline fill='none' stroke='{stroke}' stroke-width='{width}' points='{pts}' />"


def arc_points(center: Tuple[float, float], r: float, a0: float, a1: float, steps: int = 64) -> List[Tuple[float, float]]:
    cx, cy = center
    pts = []
    for i in range(steps + 1):
        t = a0 + (a1 - a0) * i / steps
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts


def to_svg() -> str:
    W, H = 600, 600
    cx, cy, r = W / 2, H / 2, 220

    # Two unit vectors with angle theta
    theta = math.radians(60.0)
    u = (1.0, 0.0)
    v = rotate2(theta, u)

    # Scale to circle radius for drawing
    U = (cx + r * u[0], cy - r * u[1])
    V = (cx + r * v[0], cy - r * v[1])

    # Arrow heads helper
    def arrow(x0, y0, x1, y1, color: str) -> str:
        seg = f"<line x1='{x0:.2f}' y1='{y0:.2f}' x2='{x1:.2f}' y2='{y1:.2f}' stroke='{color}' stroke-width='3' />"
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1.0
        ux, uy = dx / L, dy / L
        px, py = -uy, ux
        ah, aw = 12.0, 6.0
        hx, hy = x1 - ah * ux, y1 - ah * uy
        p1x, p1y = hx + aw * px, hy + aw * py
        p2x, p2y = hx - aw * px, hy - aw * py
        head = f"<polygon points='{x1:.2f},{y1:.2f} {p1x:.2f},{p1y:.2f} {p2x:.2f},{p2y:.2f}' fill='{color}' />"
        return seg + head

    svg: List[str] = []
    svg.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>")
    svg.append("<rect x='0' y='0' width='100%' height='100%' fill='white' />")

    # Unit circle
    svg.append(f"<circle cx='{cx:.2f}' cy='{cy:.2f}' r='{r:.2f}' fill='none' stroke='#999' stroke-width='1.5' />")

    # Two arrows from center to U and V
    svg.append(arrow(cx, cy, U[0], U[1], '#1f77b4'))
    svg.append(arrow(cx, cy, V[0], V[1], '#ff7f0e'))

    # Arc between u and v (angle theta)
    arc_pts = arc_points((cx, cy), r, 0.0, -theta, steps=72)  # negative y points up
    svg.append(polyline(arc_pts, stroke='#2ca02c', width=3))

    # Chord between endpoints
    svg.append(f"<line x1='{U[0]:.2f}' y1='{U[1]:.2f}' x2='{V[0]:.2f}' y2='{V[1]:.2f}' stroke='#d62728' stroke-width='3' />")

    svg.append("</svg>")
    return "\n".join(svg)


def main() -> None:
    os.makedirs("figures", exist_ok=True)
    out = os.path.join("figures", "spherical_kmeans_equivalence_python.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(to_svg())
    print(out)


if __name__ == "__main__":
    main()

