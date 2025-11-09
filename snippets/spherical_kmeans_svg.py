"""
Generate a spherical k-means intuition SVG (no text labels).
Creates three clusters on the unit sphere and draws an orthographic
projection after a fixed rotation, plus center direction arrows.

Output: figures/spherical_kmeans_python_demo.svg
"""

from __future__ import annotations

import math
import os
import random
from typing import List, Tuple


def normalize(v: Tuple[float, float, float]) -> Tuple[float, float, float]:
    x, y, z = v
    n = (x * x + y * y + z * z) ** 0.5
    if n == 0:
        return (0.0, 0.0, 0.0)
    return (x / n, y / n, z / n)


def matmul3(R: List[List[float]], v: Tuple[float, float, float]) -> Tuple[float, float, float]:
    x = R[0][0] * v[0] + R[0][1] * v[1] + R[0][2] * v[2]
    y = R[1][0] * v[0] + R[1][1] * v[1] + R[1][2] * v[2]
    z = R[2][0] * v[0] + R[2][1] * v[1] + R[2][2] * v[2]
    return (x, y, z)


def rotation_matrix(rx_deg: float, ry_deg: float, rz_deg: float) -> List[List[float]]:
    rx, ry, rz = [math.radians(a) for a in (rx_deg, ry_deg, rz_deg)]
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    Rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]
    Ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]
    Rz = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]
    # R = Rz * Ry * Rx
    def mm(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mm(mm(Rz, Ry), Rx)


def sample_on_sphere(mu: Tuple[float, float, float], n: int, noise: float) -> List[Tuple[float, float, float]]:
    pts = []
    for _ in range(n):
        # Gaussian noise around direction vector
        nx, ny, nz = (random.gauss(0, noise), random.gauss(0, noise), random.gauss(0, noise))
        p = normalize((mu[0] + nx, mu[1] + ny, mu[2] + nz))
        pts.append(p)
    return pts


def project_points(R: List[List[float]], pts: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
    # Rotate then drop z for orthographic projection; return (x, y, zrot) for depth
    out = []
    for p in pts:
        xr, yr, zr = matmul3(R, p)
        out.append((xr, yr, zr))
    return out


def to_svg(points_groups: List[List[Tuple[float, float, float]]], centers_rot: List[Tuple[float, float, float]],
           width: int = 600, height: int = 600, margin: int = 40) -> str:
    # Map x,y in [-1.2, 1.2] to canvas
    def map_to_canvas(x: float, y: float) -> Tuple[float, float]:
        s = min(width, height) / (2.4)
        cx, cy = width / 2, height / 2
        return (cx + s * x, cy - s * y)

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    # Depth-sort all points by rotated z (back to front)
    all_pts = []
    for gi, grp in enumerate(points_groups):
        for (x, y, z) in grp:
            all_pts.append((z, gi, x, y))
    all_pts.sort(key=lambda t: t[0])  # back to front

    # Start SVG
    svg = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>"]
    svg.append("<rect x='0' y='0' width='100%' height='100%' fill='white' />")

    # Draw points
    for z, gi, x, y in all_pts:
        px, py = map_to_canvas(x, y)
        color = colors[gi % len(colors)]
        svg.append(f"<circle cx='{px:.2f}' cy='{py:.2f}' r='2.2' fill='{color}' fill-opacity='0.85' />")

    # Draw center arrows from origin
    ox, oy = map_to_canvas(0.0, 0.0)
    for (xr, yr, zr), color in zip(centers_rot, colors):
        tx, ty = map_to_canvas(xr * 0.9, yr * 0.9)
        svg.append(f"<line x1='{ox:.2f}' y1='{oy:.2f}' x2='{tx:.2f}' y2='{ty:.2f}' stroke='{color}' stroke-width='3' />")
        # arrow head
        # small triangle near target
        dx, dy = tx - ox, ty - oy
        L = (dx * dx + dy * dy) ** 0.5 or 1.0
        ux, uy = dx / L, dy / L
        # perpendicular
        px_, py_ = -uy, ux
        ah = 10.0
        aw = 5.0
        hx, hy = tx - ah * ux, ty - ah * uy
        p1x, p1y = hx + aw * px_, hy + aw * py_
        p2x, p2y = hx - aw * px_, hy - aw * py_
        svg.append(
            f"<polygon points='{tx:.2f},{ty:.2f} {p1x:.2f},{p1y:.2f} {p2x:.2f},{p2y:.2f}' fill='{color}' />"
        )

    svg.append("</svg>")
    return "\n".join(svg)


def main() -> None:
    random.seed(0)
    centers = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
    centers = [normalize(c) for c in centers]
    clusters = [sample_on_sphere(mu=c, n=220, noise=0.2) for c in centers]

    R = rotation_matrix(rx_deg=25.0, ry_deg=-35.0, rz_deg=25.0)
    clusters_rot = [project_points(R, grp) for grp in clusters]
    centers_rot = [matmul3(R, c) for c in centers]

    svg = to_svg(clusters_rot, centers_rot)
    os.makedirs("figures", exist_ok=True)
    out = os.path.join("figures", "spherical_kmeans_python_demo.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(out)


if __name__ == "__main__":
    main()

