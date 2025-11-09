#!/usr/bin/env python3
"""
图3: 3D球面上弦距与角距的几何关系
展示余弦距离与欧氏距离的等价性
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform

# 设置学术风格
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 13
plt.rcParams['mathtext.fontset'] = 'cm'

# 配色
COLOR_SPHERE = '#1f77b4'
COLOR_POINTS = '#d62728'
COLOR_ARC = '#2ca02c'
COLOR_CHORD = '#ff7f0e'

class Arrow3D(FancyArrowPatch):
    """3D箭头类"""
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)

    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs)

def plot_chord_arc_distance():
    fig = plt.figure(figsize=(11, 9), dpi=300)
    ax = fig.add_subplot(111, projection='3d')

    # 定义两个单位向量
    theta_A = np.radians(35)
    phi_A = np.radians(45)
    theta_B = np.radians(70)
    phi_B = np.radians(50)

    # 球面坐标转笛卡尔坐标
    A = np.array([
        np.sin(phi_A) * np.cos(theta_A),
        np.sin(phi_A) * np.sin(theta_A),
        np.cos(phi_A)
    ])

    B = np.array([
        np.sin(phi_B) * np.cos(theta_B),
        np.sin(phi_B) * np.sin(theta_B),
        np.cos(phi_B)
    ])

    # 绘制单位球面(透明网格)
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x_sphere, y_sphere, z_sphere,
                    color=COLOR_SPHERE, alpha=0.15, linewidth=0)
    ax.plot_wireframe(x_sphere, y_sphere, z_sphere,
                      color=COLOR_SPHERE, alpha=0.1, linewidth=0.3)

    # 绘制坐标原点
    ax.scatter([0], [0], [0], color='black', s=50, marker='o', alpha=0.6)

    # 绘制点A和B
    ax.scatter(*A, color=COLOR_POINTS, s=200, marker='o',
               edgecolors='black', linewidths=1.5, zorder=10)
    ax.scatter(*B, color=COLOR_POINTS, s=200, marker='o',
               edgecolors='black', linewidths=1.5, zorder=10)

    # 绘制从原点到点的向量
    arrow_A = Arrow3D(0, 0, 0, A[0]*0.9, A[1]*0.9, A[2]*0.9,
                      mutation_scale=20, lw=2, arrowstyle='-|>',
                      color=COLOR_POINTS, alpha=0.6)
    arrow_B = Arrow3D(0, 0, 0, B[0]*0.9, B[1]*0.9, B[2]*0.9,
                      mutation_scale=20, lw=2, arrowstyle='-|>',
                      color=COLOR_POINTS, alpha=0.6)
    ax.add_artist(arrow_A)
    ax.add_artist(arrow_B)

    # 绘制弦(欧氏距离)
    ax.plot([A[0], B[0]], [A[1], B[1]], [A[2], B[2]],
            color=COLOR_CHORD, linewidth=3.5, linestyle='--',
            zorder=5)

    # 绘制弧线(角距)
    # 在大圆上插值
    n_arc_points = 50
    t_arc = np.linspace(0, 1, n_arc_points)
    arc_points = np.array([A * (1 - t) + B * t for t in t_arc])
    # 投影到单位球面
    arc_points = arc_points / np.linalg.norm(arc_points, axis=1, keepdims=True)

    ax.plot(arc_points[:, 0], arc_points[:, 1], arc_points[:, 2],
            color=COLOR_ARC, linewidth=4, linestyle='-',
            zorder=8)

    # 计算实际值
    cos_theta = np.dot(A, B)
    theta_rad = np.arccos(np.clip(cos_theta, -1, 1))
    theta_deg = np.degrees(theta_rad)
    chord_dist = np.linalg.norm(A - B)

    # 添加点标注
    ax.text(A[0]*1.15, A[1]*1.15, A[2]*1.15, '$\\mathbf{x}_i$',
            fontsize=18, color=COLOR_POINTS, weight='bold')
    ax.text(B[0]*1.15, B[1]*1.15, B[2]*1.15, '$\\mathbf{x}_j$',
            fontsize=18, color=COLOR_POINTS, weight='bold')

    # 角度标注
    mid_arc = arc_points[len(arc_points)//2]
    ax.text(mid_arc[0]*1.3, mid_arc[1]*1.3, mid_arc[2]*1.3,
            f'$\\theta$',
            fontsize=16, color=COLOR_ARC, weight='bold')

    # 设置图形属性
    ax.set_xlabel('$x_1$', fontsize=13, labelpad=8)
    ax.set_ylabel('$x_2$', fontsize=13, labelpad=8)
    ax.set_zlabel('$x_3$', fontsize=13, labelpad=8)

    # 设置视角
    ax.view_init(elev=20, azim=45)

    # 设置坐标轴范围
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)

    # 网格
    ax.grid(True, alpha=0.2, linestyle=':')

    plt.tight_layout()

    # 保存图片
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '../../figures/chord_arc_distance_3d.png')
    output_path = os.path.abspath(output_path)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 图片已保存至: {output_path}")

    return fig

if __name__ == '__main__':
    plot_chord_arc_distance()
    # plt.show()
