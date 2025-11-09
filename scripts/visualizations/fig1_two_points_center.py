#!/usr/bin/env python3
"""
图1: 单位圆上两点与归一化中心的几何关系
展示球面k-Means中心计算的核心思想
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import matplotlib.patches as mpatches

# 设置学术风格
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 14
plt.rcParams['mathtext.fontset'] = 'cm'

# 定义配色方案(学术风格)
COLOR_VECTORS = '#1f77b4'  # 蓝色 - 数据点
COLOR_CENTER = '#d62728'   # 红色 - 中心点
COLOR_SUM = '#ff7f0e'      # 橙色 - 向量和
COLOR_GRID = '#cccccc'     # 灰色 - 辅助线
COLOR_CIRCLE = '#000000'   # 黑色 - 单位圆

def normalize(v):
    """归一化向量到单位长度"""
    return v / np.linalg.norm(v)

def plot_two_points_center():
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

    # 定义两个单位向量(角度分别为30度和60度)
    angle1 = np.radians(40)
    angle2 = np.radians(80)

    x1 = np.array([np.cos(angle1), np.sin(angle1)])
    x2 = np.array([np.cos(angle2), np.sin(angle2)])

    # 计算向量和与归一化中心
    vector_sum = x1 + x2
    center = normalize(vector_sum)

    # 绘制单位圆
    circle = Circle((0, 0), 1, fill=False, edgecolor=COLOR_CIRCLE,
                    linewidth=2, linestyle='-', label='单位圆 $\\mathbb{S}^1$')
    ax.add_patch(circle)

    # 绘制坐标轴
    ax.axhline(y=0, color=COLOR_GRID, linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axvline(x=0, color=COLOR_GRID, linewidth=0.8, linestyle='--', alpha=0.5)

    # 绘制两个数据向量(从原点出发)
    ax.arrow(0, 0, x1[0]*0.95, x1[1]*0.95, head_width=0.06, head_length=0.08,
             fc=COLOR_VECTORS, ec=COLOR_VECTORS, linewidth=2.5, label='数据点 $\\mathbf{x}_1, \\mathbf{x}_2$')
    ax.arrow(0, 0, x2[0]*0.95, x2[1]*0.95, head_width=0.06, head_length=0.08,
             fc=COLOR_VECTORS, ec=COLOR_VECTORS, linewidth=2.5)

    # 绘制向量和(虚线,可能超出单位圆)
    ax.arrow(0, 0, vector_sum[0]*0.95, vector_sum[1]*0.95,
             head_width=0.06, head_length=0.08,
             fc=COLOR_SUM, ec=COLOR_SUM, linewidth=2, linestyle='--',
             alpha=0.7, label='向量和 $\\mathbf{x}_1 + \\mathbf{x}_2$')

    # 绘制归一化后的中心
    ax.arrow(0, 0, center[0]*0.95, center[1]*0.95,
             head_width=0.08, head_length=0.1,
             fc=COLOR_CENTER, ec=COLOR_CENTER, linewidth=3,
             label='归一化中心 $\\mathbf{c}$')

    # 标注点
    ax.plot(x1[0], x1[1], 'o', color=COLOR_VECTORS, markersize=10)
    ax.plot(x2[0], x2[1], 'o', color=COLOR_VECTORS, markersize=10)
    ax.plot(center[0], center[1], '*', color=COLOR_CENTER, markersize=18,
            markeredgecolor='black', markeredgewidth=0.5)

    # 添加数学符号标注
    offset = 0.15
    ax.text(x1[0]+offset, x1[1], '$\\mathbf{x}_1$', fontsize=18,
            ha='left', va='bottom', color=COLOR_VECTORS, weight='bold')
    ax.text(x2[0]-offset*0.5, x2[1]+offset, '$\\mathbf{x}_2$', fontsize=18,
            ha='right', va='bottom', color=COLOR_VECTORS, weight='bold')
    ax.text(center[0]+offset, center[1], '$\\mathbf{c}$', fontsize=20,
            ha='left', va='bottom', color=COLOR_CENTER, weight='bold')

    # 标注向量和
    ax.text(vector_sum[0]+0.1, vector_sum[1]+0.1,
            '$\\sum\\mathbf{x}_i$', fontsize=16,
            ha='left', va='bottom', color=COLOR_SUM, weight='bold')

    # 绘制归一化操作的箭头
    from matplotlib.patches import FancyArrowPatch
    arrow = FancyArrowPatch(
        (vector_sum[0]*0.85, vector_sum[1]*0.85),
        (center[0]*0.9, center[1]*0.9),
        arrowstyle='->', mutation_scale=20, linewidth=1.5,
        color='green', linestyle=':', alpha=0.6
    )
    ax.add_patch(arrow)

    # 设置图形属性
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle=':')

    ax.set_xlabel('$x_1$', fontsize=14)
    ax.set_ylabel('$x_2$', fontsize=14)

    plt.tight_layout()

    # 保存图片
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '../../figures/spherical_kmeans_two_points_new.png')
    output_path = os.path.abspath(output_path)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 图片已保存至: {output_path}")

    return fig

if __name__ == '__main__':
    plot_two_points_center()
    # plt.show()  # 可选: 显示图片
