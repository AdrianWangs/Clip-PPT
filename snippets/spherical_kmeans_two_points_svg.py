"""
Spherical k-means: two points + spherical centroid (no labels).

Draws a unit circle, two unit vectors (data points), and their centroid
direction c = (u+v)/||u+v||, with arrows only. Also shows the chord
between u and v to hint cosine↔Euclidean (chord) mapping.

Output: figures/spherical_kmeans_two_points.svg
"""

from __future__ import annotations

import math
import os
from typing import Tuple, List


def normalize2(v: Tuple[float, float]) -> Tuple[float, float]:
    x, y = v
    n = math.hypot(x, y)
    if n == 0:
        return (0.0, 0.0)
    return (x / n, y / n)


def arrow(x0: float, y0: float, x1: float, y1: float, color: str, w: float = 3.0) -> str:
    seg = f"<line x1='{x0:.2f}' y1='{y0:.2f}' x2='{x1:.2f}' y2='{y1:.2f}' stroke='{color}' stroke-width='{w}' />"
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


def arc_points(cx: float, cy: float, r: float, a0: float, a1: float, steps: int = 64) -> List[Tuple[float, float]]:
    pts = []
    for i in range(steps + 1):
        t = a0 + (a1 - a0) * i / steps
        pts.append((cx + r * math.cos(t), cy - r * math.sin(t)))
    return pts


def polyline(points: List[Tuple[float, float]], color: str, w: float = 2.5) -> str:
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f"<polyline fill='none' stroke='{color}' stroke-width='{w}' points='{pts}' />"


def main() -> None:
    W, H = 600, 600
    cx, cy, r = W / 2, H / 2, 230

    # Two unit vectors with moderate angle
    theta = math.radians(40.0)
    u = (1.0, 0.0)
    v = (math.cos(theta), math.sin(theta))
    # Spherical centroid direction (normalized mean)
    m = normalize2((u[0] + v[0], u[1] + v[1]))

    # Scale to circle radius
    U = (cx + r * u[0], cy - r * u[1])
    V = (cx + r * v[0], cy - r * v[1])
    M = (cx + r * m[0], cy - r * m[1])

    svg: List[str] = []
    svg.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>")
    svg.append("<rect x='0' y='0' width='100%' height='100%' fill='white' />")
    # Unit circle
    svg.append(f"<circle cx='{cx:.2f}' cy='{cy:.2f}' r='{r:.2f}' fill='none' stroke='#999' stroke-width='1.5' />")
    # Cosine↔Euclidean hint: draw geodesic arc (green) and chord (red)
    arc = arc_points(cx, cy, r, 0.0, theta)
    svg.append(polyline(arc, '#2ca02c', 3.0))
    svg.append(f"<line x1='{U[0]:.2f}' y1='{U[1]:.2f}' x2='{V[0]:.2f}' y2='{V[1]:.2f}' stroke='#d62728' stroke-width='3' />")
    # Two data points (arrows)
    svg.append(arrow(cx, cy, U[0], U[1], '#1f77b4', 3.0))
    svg.append(arrow(cx, cy, V[0], V[1], '#ff7f0e', 3.0))
    # Spherical centroid direction (normalized mean)
    svg.append(arrow(cx, cy, M[0], M[1], '#9467bd', 4.0))
    svg.append("</svg>")

    os.makedirs("figures", exist_ok=True)
    out = os.path.join("figures", "spherical_kmeans_two_points.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(out)


if __name__ == "__main__":
    main()

