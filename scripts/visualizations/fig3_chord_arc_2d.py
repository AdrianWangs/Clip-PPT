#!/usr/bin/env python3
"""
图3 (2D版本): 单位圆上弦距与角距的关系
在2D平面上清晰展示欧氏距离与余弦相似度的等价性
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch
import matplotlib.patches as mpatches

# 设置学术风格
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 14
plt.rcParams['mathtext.fontset'] = 'cm'

# 配色
COLOR_POINTS = '#d62728'   # 红色 - 点
COLOR_ARC = '#2ca02c'      # 绿色 - 弧线
COLOR_CHORD = '#ff7f0e'    # 橙色 - 弦
COLOR_CIRCLE = '#000000'   # 黑色 - 圆

def plot_chord_arc_2d():
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    # 定义两个单位向量(角度)
    angle1 = np.radians(30)
    angle2 = np.radians(100)

    x1 = np.array([np.cos(angle1), np.sin(angle1)])
    x2 = np.array([np.cos(angle2), np.sin(angle2)])

    # 绘制单位圆
    circle = plt.Circle((0, 0), 1, fill=False, edgecolor=COLOR_CIRCLE,
                        linewidth=3, linestyle='-')
    ax.add_patch(circle)

    # 绘制坐标轴
    ax.axhline(y=0, color='gray', linewidth=1, linestyle='--', alpha=0.3)
    ax.axvline(x=0, color='gray', linewidth=1, linestyle='--', alpha=0.3)

    # 绘制从原点到两点的向量
    ax.arrow(0, 0, x1[0]*0.92, x1[1]*0.92,
             head_width=0.06, head_length=0.08,
             fc=COLOR_POINTS, ec=COLOR_POINTS, linewidth=2.5, alpha=0.6)
    ax.arrow(0, 0, x2[0]*0.92, x2[1]*0.92,
             head_width=0.06, head_length=0.08,
             fc=COLOR_POINTS, ec=COLOR_POINTS, linewidth=2.5, alpha=0.6)

    # 绘制两个点
    ax.plot(x1[0], x1[1], 'o', color=COLOR_POINTS, markersize=16,
            markeredgecolor='black', markeredgewidth=1.5, zorder=10)
    ax.plot(x2[0], x2[1], 'o', color=COLOR_POINTS, markersize=16,
            markeredgecolor='black', markeredgewidth=1.5, zorder=10)

    # 绘制弦（欧氏距离）
    ax.plot([x1[0], x2[0]], [x1[1], x2[1]],
            color=COLOR_CHORD, linewidth=4, linestyle='--',
            label='欧氏距离（弦）', zorder=5)

    # 绘制弧线（角距）
    theta_deg1 = np.degrees(angle1)
    theta_deg2 = np.degrees(angle2)
    arc = Arc((0, 0), 2, 2, angle=0, theta1=theta_deg1, theta2=theta_deg2,
              color=COLOR_ARC, linewidth=5, zorder=8)
    ax.add_patch(arc)

    # 计算数值
    cos_theta = np.dot(x1, x2)
    theta_rad = np.arccos(np.clip(cos_theta, -1, 1))
    theta_deg = np.degrees(theta_rad)
    chord_dist = np.linalg.norm(x1 - x2)

    # 标注点
    ax.text(x1[0]*1.25, x1[1]*1.25, '$\\mathbf{x}_i$',
            fontsize=20, color=COLOR_POINTS, weight='bold',
            ha='center', va='center')
    ax.text(x2[0]*1.25, x2[1]*1.25, '$\\mathbf{x}_j$',
            fontsize=20, color=COLOR_POINTS, weight='bold',
            ha='center', va='center')

    # 标注角度（在圆心附近）
    mid_angle = (angle1 + angle2) / 2
    label_r = 0.4
    ax.text(label_r*np.cos(mid_angle), label_r*np.sin(mid_angle),
            f'$\\theta = {theta_deg:.0f}°$',
            fontsize=16, color=COLOR_ARC, weight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                     edgecolor=COLOR_ARC, linewidth=1.5, alpha=0.9))

    # 标注弦距（在弦的中点）
    mid_chord = (x1 + x2) / 2
    ax.text(mid_chord[0], mid_chord[1]-0.15,
            f'$d = {chord_dist:.2f}$',
            fontsize=16, color=COLOR_CHORD, weight='bold',
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                     edgecolor=COLOR_CHORD, linewidth=1.5, alpha=0.9))

    # 标注余弦值
    ax.text(0.5, -1.55,
            f'$\\cos\\theta = {cos_theta:.3f}$',
            fontsize=15, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan',
                     edgecolor='blue', linewidth=1.2, alpha=0.9))

    # 添加等价关系公式
    formula = f'$d^2 = 2(1 - \\cos\\theta) = 2(1 - {cos_theta:.3f}) = {chord_dist**2:.3f}$'
    ax.text(0, -1.8,
            formula,
            fontsize=14, ha='center', color='black',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='lightyellow',
                     edgecolor='gray', linewidth=1.5, alpha=0.95))

    # 设置图形属性
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-2.0, 1.6)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle=':')

    ax.set_xlabel('$x_1$', fontsize=14)
    ax.set_ylabel('$x_2$', fontsize=14)

    plt.tight_layout()

    # 保存图片
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '../../figures/chord_arc_distance_2d.png')
    output_path = os.path.abspath(output_path)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 图片已保存至: {output_path}")

    return fig

if __name__ == '__main__':
    plot_chord_arc_2d()
