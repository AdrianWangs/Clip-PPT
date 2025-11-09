
import numpy as np
import matplotlib.pyplot as plt

def spherical_kmeans_step(X, C):
    S = X @ C.T
    z = S.argmax(axis=1)
    
    C_new = []
    for j in range(C.shape[0]):
        cluster_points = X[z == j]
        if len(cluster_points) > 0:
            M = cluster_points.sum(axis=0)
            c = M / (np.linalg.norm(M) + 1e-12)
            C_new.append(c)
        else:
            # Re-initialize empty clusters
            C_new.append(X[np.random.choice(len(X))]) 
    return np.stack(C_new), z

def plot_state(ax, X, C, z, title, show_z=False):
    ax.add_artist(plt.Circle((0, 0), 1, color='#CCCCCC', fill=False, linewidth=1, linestyle='--'))
    
    # Plot points
    if show_z and z is not None:
        ax.scatter(X[:, 0], X[:, 1], c=[f'C{i}' for i in z], alpha=0.7)
    else:
        ax.scatter(X[:, 0], X[:, 1], c='gray', alpha=0.7)

    # Plot centroids
    ax.scatter(C[:, 0], C[:, 1], c=[f'C{i}' for i in range(len(C))], marker='X', s=150, edgecolor='black', linewidth=1.5)

    ax.set_title(title, fontsize=14)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

def main():
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    np.random.seed(42)
    
    # Generate synthetic data on a circle
    angles = np.concatenate([
        np.random.uniform(0, np.pi/2, 50),
        np.random.uniform(np.pi*3/4, np.pi*5/4, 50),
        np.random.uniform(np.pi*3/2, np.pi*2, 50)
    ])
    X = np.array([np.cos(angles), np.sin(angles)]).T
    
    # Initial centroids
    k = 3
    init_indices = np.random.choice(len(X), k, replace=False)
    C0 = X[init_indices]
    C0 /= np.linalg.norm(C0, axis=1)[:, np.newaxis]

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()

    # (a) Initial state
    plot_state(axes[0], X, C0, None, "(a) 初始状态 (t=0)")

    # (b) Iteration 1: Assignment
    _, z1 = spherical_kmeans_step(X, C0)
    plot_state(axes[1], X, C0, z1, "(b) 第一次分配", show_z=True)

    # (c) Iteration 1: Update
    C1, _ = spherical_kmeans_step(X, C0)
    plot_state(axes[2], X, C1, z1, "(c) 第一次更新", show_z=True)

    # (d) Final state (run a few more iterations)
    C_final, z_final = C1, z1
    for _ in range(5):
        C_final, z_final = spherical_kmeans_step(X, C_final)
    plot_state(axes[3], X, C_final, z_final, "(d) 最终收敛 (t=5)", show_z=True)
    
    plt.tight_layout(pad=2.0)
    plt.savefig('./figures/spherical_kmeans_demo.svg', format='svg', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
