#!/usr/bin/env python3
"""
图2: 四点向量和的归一化过程
展示多个点聚类时中心的计算过程
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as mpatches

# 设置学术风格
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 13
plt.rcParams['mathtext.fontset'] = 'cm'

# 定义配色方案
COLOR_VECTORS = '#1f77b4'  # 蓝色 - 数据点
COLOR_CENTER = '#d62728'   # 红色 - 中心点
COLOR_SUM = '#ff7f0e'      # 橙色 - 向量和
COLOR_GRID = '#cccccc'     # 灰色 - 辅助线
COLOR_CIRCLE = '#000000'   # 黑色 - 单位圆

def normalize(v):
    """归一化向量到单位长度"""
    norm = np.linalg.norm(v)
    return v / norm, norm

def plot_four_points_sum():
    fig, ax = plt.subplots(figsize=(9, 8), dpi=300)

    # 定义四个单位向量(聚集在第一象限,模拟一个簇)
    angles = [np.radians(a) for a in [25, 35, 50, 65]]
    points = np.array([[np.cos(a), np.sin(a)] for a in angles])

    # 计算向量和与归一化中心
    vector_sum = points.sum(axis=0)
    center, sum_norm = normalize(vector_sum)

    # 绘制单位圆
    circle = Circle((0, 0), 1, fill=False, edgecolor=COLOR_CIRCLE,
                    linewidth=2.5, linestyle='-', zorder=1)
    ax.add_patch(circle)

    # 绘制坐标轴
    ax.axhline(y=0, color=COLOR_GRID, linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(x=0, color=COLOR_GRID, linewidth=0.8, linestyle='--', alpha=0.5)

    # 绘制四个数据向量
    for i, pt in enumerate(points):
        ax.arrow(0, 0, pt[0]*0.93, pt[1]*0.93,
                 head_width=0.05, head_length=0.07,
                 fc=COLOR_VECTORS, ec=COLOR_VECTORS,
                 linewidth=2, alpha=0.8, zorder=3)
        ax.plot(pt[0], pt[1], 'o', color=COLOR_VECTORS,
                markersize=9, zorder=4)

    # 绘制向量和(超出单位圆)
    ax.arrow(0, 0, vector_sum[0]*0.9, vector_sum[1]*0.9,
             head_width=0.08, head_length=0.1,
             fc=COLOR_SUM, ec=COLOR_SUM, linewidth=2.5,
             linestyle='--', alpha=0.8, zorder=2)

    # 标注向量和
    ax.plot(vector_sum[0], vector_sum[1], 's',
            color=COLOR_SUM, markersize=11, zorder=4,
            markeredgecolor='black', markeredgewidth=0.8)
    ax.text(vector_sum[0]+0.15, vector_sum[1]+0.1,
            f'$\\sum\\mathbf{{x}}_i$',
            fontsize=16, color=COLOR_SUM, weight='bold',
            ha='left', va='bottom')

    # 绘制归一化后的中心
    ax.arrow(0, 0, center[0]*0.93, center[1]*0.93,
             head_width=0.08, head_length=0.1,
             fc=COLOR_CENTER, ec=COLOR_CENTER, linewidth=3.5, zorder=5)
    ax.plot(center[0], center[1], '*',
            color=COLOR_CENTER, markersize=20, zorder=6,
            markeredgecolor='black', markeredgewidth=0.6)

    # 归一化操作箭头
    from matplotlib.patches import FancyArrowPatch
    arrow = FancyArrowPatch(
        (vector_sum[0]*0.75, vector_sum[1]*0.75),
        (center[0]*0.88, center[1]*0.88),
        arrowstyle='->', mutation_scale=25, linewidth=2,
        color='green', linestyle=':', alpha=0.7, zorder=3
    )
    ax.add_patch(arrow)

    # 标注中心
    ax.text(center[0]+0.12, center[1]+0.15,
            '$\\mathbf{c}$', fontsize=20,
            ha='left', va='bottom', color=COLOR_CENTER, weight='bold')

    # 设置图形属性
    ax.set_xlim(-1.6, 2.2)
    ax.set_ylim(-1.6, 1.8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.25, linestyle=':')

    ax.set_xlabel('$x_1$', fontsize=14)
    ax.set_ylabel('$x_2$', fontsize=14)

    plt.tight_layout()

    # 保存图片
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '../../figures/spherical_kmeans_four_points_sum.png')
    output_path = os.path.abspath(output_path)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 图片已保存至: {output_path}")

    return fig

if __name__ == '__main__':
    plot_four_points_sum()
    # plt.show()
