import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches

# Set style for academic look
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

OUTPUT_DIR = '../'

def draw_sphere(ax, alpha=0.1):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b', alpha=alpha, shade=False)
    # Draw equator and meridians for reference
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 0, color='gray', alpha=0.3, linestyle='--')
    ax.plot(np.zeros_like(theta), np.cos(theta), np.sin(theta), color='gray', alpha=0.3, linestyle='--')
    ax.plot(np.cos(theta), np.zeros_like(theta), np.sin(theta), color='gray', alpha=0.3, linestyle='--')

def plot_vector(ax, v, color, label=None, linestyle='-'):
    ax.quiver(0, 0, 0, v[0], v[1], v[2], color=color, arrow_length_ratio=0.1, linestyle=linestyle, label=label)
    if label:
        ax.text(v[0]*1.1, v[1]*1.1, v[2]*1.1, label, color=color)

def fig1_magnitude_bias():
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    draw_sphere(ax)
    
    # Data points: 2 short vectors, 1 very long vector
    # They point in roughly the same direction (e.g., [1, 1, 1])
    base_dir = np.array([1, 1, 1]) / np.sqrt(3)
    
    # Perturb them slightly
    v1 = (base_dir + np.array([0.1, -0.1, 0])) 
    v1 = v1 / np.linalg.norm(v1) * 0.8 # Short
    
    v2 = (base_dir + np.array([-0.1, 0.1, 0]))
    v2 = v2 / np.linalg.norm(v2) * 0.9 # Short
    
    v3 = (base_dir + np.array([0.2, 0.2, 0]))
    v3 = v3 / np.linalg.norm(v3) * 2.5 # Long!
    
    plot_vector(ax, v1, 'blue', 'v1')
    plot_vector(ax, v2, 'blue', 'v2')
    plot_vector(ax, v3, 'blue', 'v3 (Long)')
    
    # Euclidean Mean (Center of Gravity)
    mean_euclidean = (v1 + v2 + v3) / 3
    ax.scatter(mean_euclidean[0], mean_euclidean[1], mean_euclidean[2], color='red', s=100, marker='x', label='Euclidean Mean')
    
    # Spherical Mean (Normalized Sum)
    sum_vec = v1 + v2 + v3
    mean_spherical = sum_vec / np.linalg.norm(sum_vec)
    ax.scatter(mean_spherical[0], mean_spherical[1], mean_spherical[2], color='green', s=100, marker='*', label='Spherical Mean')
    
    # Draw line from origin to spherical mean
    ax.plot([0, mean_spherical[0]], [0, mean_spherical[1]], [0, mean_spherical[2]], color='green', linestyle='--')

    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.set_title('Magnitude Bias in Euclidean K-Means')
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'kmeans_magnitude_bias.png', dpi=300, bbox_inches='tight')
    plt.close()

def fig2_distance_equivalence():
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Draw unit circle
    circle = plt.Circle((0, 0), 1, color='blue', fill=False, linestyle='--', alpha=0.5)
    ax.add_artist(circle)
    
    # Two points on circle
    theta1 = np.pi / 6 # 30 deg
    theta2 = np.pi / 2 # 90 deg
    
    p1 = np.array([np.cos(theta1), np.sin(theta1)])
    p2 = np.array([np.cos(theta2), np.sin(theta2)])
    
    ax.plot([0, p1[0]], [0, p1[1]], 'k-', alpha=0.5)
    ax.plot([0, p2[0]], [0, p2[1]], 'k-', alpha=0.5)
    
    ax.scatter(p1[0], p1[1], color='red', s=50, label='x')
    ax.scatter(p2[0], p2[1], color='red', s=50, label='y')
    
    ax.text(p1[0]*1.1, p1[1]*1.1, 'x', fontsize=12)
    ax.text(p2[0]*1.1, p2[1]*1.1, 'y', fontsize=12)
    
    # Chord (Euclidean Distance)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-', label='Chord (Euclidean)')
    
    # Arc (Angle)
    arc = patches.Arc((0, 0), 0.4, 0.4, theta1=np.degrees(theta1), theta2=np.degrees(theta2), color='green', linewidth=2, label='Angle (Cosine)')
    ax.add_patch(arc)
    ax.text(0.1, 0.1, r'$\theta$', fontsize=14, color='green')
    
    ax.set_xlim([-0.1, 1.2])
    ax.set_ylim([-0.1, 1.2])
    ax.set_aspect('equal')
    ax.set_title('Euclidean Distance vs Cosine Similarity')
    ax.legend(loc='lower left')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'distance_equivalence.png', dpi=300, bbox_inches='tight')
    plt.close()

def fig3_spherical_kmeans_step():
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    draw_sphere(ax)
    
    # Cluster of points on sphere
    center_dir = np.array([0, 1, 1]) / np.sqrt(2)
    points = []
    for _ in range(10):
        noise = np.random.normal(0, 0.1, 3)
        p = center_dir + noise
        p = p / np.linalg.norm(p)
        points.append(p)
        ax.scatter(p[0], p[1], p[2], color='blue', alpha=0.6, s=20)
    
    points = np.array(points)
    
    # Sum vector (long)
    sum_vec = np.sum(points, axis=0)
    # Scale down slightly for visualization if too huge, but keep it outside sphere
    sum_vec_vis = sum_vec / np.linalg.norm(sum_vec) * 1.8 
    
    plot_vector(ax, sum_vec_vis, 'orange', 'Sum Vector', linestyle='--')
    
    # Normalized Center
    center = sum_vec / np.linalg.norm(sum_vec)
    ax.scatter(center[0], center[1], center[2], color='green', s=150, marker='*', label='New Center (Normalized)')
    
    # Arrow from Sum to Center
    ax.quiver(sum_vec_vis[0], sum_vec_vis[1], sum_vec_vis[2], 
              center[0]-sum_vec_vis[0], center[1]-sum_vec_vis[1], center[2]-sum_vec_vis[2], 
              color='purple', arrow_length_ratio=0.1, label='Normalize')

    ax.set_xlim([-0.5, 1.5])
    ax.set_ylim([-0.5, 1.5])
    ax.set_zlim([-0.5, 1.5])
    ax.set_title('Spherical K-Means Update Step')
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'spherical_kmeans_step.png', dpi=300, bbox_inches='tight')
    plt.close()

def fig4_hst_structure():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw Tree
    # Root
    ax.scatter(0, 3, s=500, c='red', edgecolors='black', zorder=10)
    ax.text(0, 3, 'Root', ha='center', va='center', color='white', fontweight='bold')
    
    # Level 1
    for i in range(-2, 3):
        x = i * 2
        y = 2
        ax.scatter(x, y, s=300, c='blue', edgecolors='black', zorder=10)
        ax.plot([0, x], [3, y], 'k-', alpha=0.5, zorder=1)
        
        # Level 2 (only for one branch to keep it clean)
        if i == 0:
            for j in range(-1, 2):
                xx = x + j * 0.8
                yy = 1
                ax.scatter(xx, yy, s=150, c='green', edgecolors='black', zorder=10)
                ax.plot([x, xx], [y, yy], 'k-', alpha=0.5, zorder=1)
                
                # Level 3 (Leaves)
                if j == 0:
                     for k in range(-1, 2):
                        xxx = xx + k * 0.3
                        yyy = 0
                        ax.scatter(xxx, yyy, s=50, c='gray', edgecolors='black', zorder=10)
                        ax.plot([xx, xxx], [yy, yyy], 'k-', alpha=0.5, zorder=1)

    ax.text(4, 3, 'Layer 0: Root', va='center')
    ax.text(4, 2, 'Layer 1: k Clusters', va='center')
    ax.text(4, 1, 'Layer 2: k^2 Clusters', va='center')
    ax.text(4, 0, 'Layer 3: Leaves (Data)', va='center')

    ax.set_xlim([-5, 6])
    ax.set_ylim([-0.5, 3.5])
    ax.axis('off')
    ax.set_title('Hierarchical Spherical Tree (k=10, Depth=3-4)')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR + 'hst_structure.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating figures...")
    fig1_magnitude_bias()
    print("Generated kmeans_magnitude_bias.png")
    fig2_distance_equivalence()
    print("Generated distance_equivalence.png")
    fig3_spherical_kmeans_step()
    print("Generated spherical_kmeans_step.png")
    fig4_hst_structure()
    print("Generated hst_structure.png")
    print("Done.")
