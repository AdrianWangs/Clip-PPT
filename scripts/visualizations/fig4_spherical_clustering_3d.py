#!/usr/bin/env python3
"""
图4: 3D球面上的三簇聚类可视化
展示球面k-Means的最终聚类效果
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 设置学术风格
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'cm'

# 配色方案(3个簇)
CLUSTER_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 蓝、橙、绿
CENTER_COLOR = '#d62728'  # 红色中心
SPHERE_COLOR = '#cccccc'  # 灰色球面

def sample_vmf(mu, kappa, n_samples):
    """
    从von Mises-Fisher分布采样
    mu: 方向向量(3D,已归一化)
    kappa: 浓度参数(越大越集中)
    n_samples: 样本数量
    """
    dim = len(mu)

    # 采样w(从一维分布)
    w_samples = []
    for _ in range(n_samples):
        # 使用rejection sampling
        while True:
            xi = np.random.beta((dim - 1) / 2, (dim - 1) / 2)
            w = 1 + (np.log(xi) + np.log(1 - xi + 1e-10)) / kappa
            if -1 <= w <= 1:
                break
        w_samples.append(w)

    w_samples = np.array(w_samples)

    # 采样v(从球面均匀分布)
    v_samples = np.random.randn(n_samples, dim)
    v_samples = v_samples / np.linalg.norm(v_samples, axis=1, keepdims=True)

    # 构造正交基
    mu = mu / np.linalg.norm(mu)
    # 找一个与mu不平行的向量
    if abs(mu[0]) < 0.9:
        u = np.array([1.0, 0.0, 0.0])
    else:
        u = np.array([0.0, 1.0, 0.0])

    # Gram-Schmidt正交化
    u = u - np.dot(u, mu) * mu
    u = u / np.linalg.norm(u)
    v_perp = np.cross(mu, u)

    # 生成样本
    samples = []
    for i in range(n_samples):
        w = w_samples[i]
        v = v_samples[i]
        # 将v投影到垂直于mu的平面
        v_proj = v - np.dot(v, mu) * mu
        v_proj = v_proj / (np.linalg.norm(v_proj) + 1e-10)

        # 构造最终样本
        x = np.sqrt(1 - w**2) * v_proj + w * mu
        x = x / np.linalg.norm(x)  # 归一化到单位球面
        samples.append(x)

    return np.array(samples)

def spherical_kmeans(X, centers, max_iter=20):
    """
    简单的球面k-means实现
    X: 数据点(N, 3)
    centers: 初始中心(k, 3)
    """
    k = len(centers)
    centers = centers / np.linalg.norm(centers, axis=1, keepdims=True)

    for iteration in range(max_iter):
        # E-step: 分配
        similarities = X @ centers.T  # (N, k)
        labels = np.argmax(similarities, axis=1)

        # M-step: 更新中心
        new_centers = np.zeros_like(centers)
        for j in range(k):
            cluster_points = X[labels == j]
            if len(cluster_points) > 0:
                new_centers[j] = cluster_points.sum(axis=0)
                new_centers[j] /= np.linalg.norm(new_centers[j])

        # 检查收敛
        if np.allclose(centers, new_centers, atol=1e-6):
            break

        centers = new_centers

    return centers, labels

def plot_spherical_clustering():
    fig = plt.figure(figsize=(12, 10), dpi=300)
    ax = fig.add_subplot(111, projection='3d')

    # 设置随机种子以保证可重复性
    np.random.seed(42)

    # 定义3个簇的真实中心
    true_centers = np.array([
        [1, 0, 0.5],      # 簇1中心
        [-0.5, 1, 0],     # 簇2中心
        [0, -0.5, 1]      # 簇3中心
    ])
    true_centers = true_centers / np.linalg.norm(true_centers, axis=1, keepdims=True)

    # 从von Mises-Fisher分布采样
    kappa = 15  # 浓度参数
    n_per_cluster = 40

    all_points = []
    true_labels = []

    for i, center in enumerate(true_centers):
        cluster_points = sample_vmf(center, kappa, n_per_cluster)
        all_points.append(cluster_points)
        true_labels.extend([i] * n_per_cluster)

    X = np.vstack(all_points)
    true_labels = np.array(true_labels)

    # 运行球面k-means
    initial_centers = np.random.randn(3, 3)
    final_centers, pred_labels = spherical_kmeans(X, initial_centers)

    # 绘制单位球面(透明)
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 40)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x_sphere, y_sphere, z_sphere,
                    color=SPHERE_COLOR, alpha=0.08, linewidth=0)
    ax.plot_wireframe(x_sphere, y_sphere, z_sphere,
                      color=SPHERE_COLOR, alpha=0.12, linewidth=0.3)

    # 绘制数据点(按簇分配着色)
    for i in range(3):
        cluster_points = X[pred_labels == i]
        ax.scatter(cluster_points[:, 0],
                  cluster_points[:, 1],
                  cluster_points[:, 2],
                  c=[CLUSTER_COLORS[i]],
                  s=50, alpha=0.7,
                  edgecolors='white', linewidths=0.5)

    # 绘制计算得到的中心(大红星)
    ax.scatter(final_centers[:, 0],
              final_centers[:, 1],
              final_centers[:, 2],
              c=CENTER_COLOR, s=400, marker='*',
              edgecolors='black', linewidths=2,
              zorder=100)

    # 绘制从原点到中心的向量
    for i, center in enumerate(final_centers):
        ax.plot([0, center[0]], [0, center[1]], [0, center[2]],
                color=CENTER_COLOR, linewidth=2.5, linestyle='--',
                alpha=0.5, zorder=50)

    # 添加中心标注
    for i, center in enumerate(final_centers):
        ax.text(center[0]*1.25, center[1]*1.25, center[2]*1.25,
                f'$\\mathbf{{c}}_{i+1}$',
                fontsize=16, color=CENTER_COLOR, weight='bold',
                ha='center', va='center')

    # 坐标原点
    ax.scatter([0], [0], [0], color='black', s=80, marker='o', alpha=0.7)

    # 设置图形属性
    ax.set_xlabel('$x_1$', fontsize=13, labelpad=10)
    ax.set_ylabel('$x_2$', fontsize=13, labelpad=10)
    ax.set_zlabel('$x_3$', fontsize=13, labelpad=10)

    # 设置视角
    ax.view_init(elev=15, azim=35)

    # 设置坐标轴范围
    limit = 1.3
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)

    # 网格
    ax.grid(True, alpha=0.2, linestyle=':')

    # 隐藏坐标轴背景
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('gray')
    ax.yaxis.pane.set_edgecolor('gray')
    ax.zaxis.pane.set_edgecolor('gray')
    ax.xaxis.pane.set_alpha(0.1)
    ax.yaxis.pane.set_alpha(0.1)
    ax.zaxis.pane.set_alpha(0.1)

    plt.tight_layout()

    # 保存图片
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '../../figures/spherical_clustering_demo.png')
    output_path = os.path.abspath(output_path)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 图片已保存至: {output_path}")

    return fig

if __name__ == '__main__':
    plot_spherical_clustering()
    # plt.show()
