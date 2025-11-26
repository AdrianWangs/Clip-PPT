import matplotlib.pyplot as plt
import numpy as np

def setup_plot():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    
    # Remove axes spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig, ax

def draw_unit_circle(ax):
    theta = np.linspace(0, np.pi/2 + 0.2, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(x, y, 'k--', alpha=0.3, label='Unit Sphere (Surface)')
    
    # Draw origin
    ax.scatter([0], [0], color='black', s=50)
    ax.text(-0.05, -0.05, 'Origin', fontsize=12)

def generate_cluster_points():
    # Drastically increase spread to pull the Euclidean mean inward
    # Spread from 10 degrees to 80 degrees (70 degrees spread)
    angles = np.array([np.pi/18, np.pi/4, 4*np.pi/9]) 
    points = np.array([[np.cos(a), np.sin(a)] for a in angles])
    return points

def plot_vectors(ax, points):
    # Plot data points
    ax.scatter(points[:, 0], points[:, 1], c='#3B82F6', s=150, zorder=10, label='Data Points')
    
    # Draw vectors to data points
    for p in points:
        ax.arrow(0, 0, p[0]-0.03, p[1]-0.03, head_width=0.03, head_length=0.03, fc='#3B82F6', ec='#3B82F6', alpha=0.2)

def plot_means(ax, points):
    # Euclidean Mean (Arithmetic Average)
    euclidean_mean = np.mean(points, axis=0)
    
    # Spherical Mean (Normalized Sum)
    vector_sum = np.sum(points, axis=0)
    spherical_mean = vector_sum / np.linalg.norm(vector_sum)
    
    # Plot Euclidean Mean - MASSIVE SIZE
    # Add a large white background circle to clear clutter
    ax.scatter(euclidean_mean[0], euclidean_mean[1], c='white', s=600, marker='o', zorder=9, alpha=0.8)
    ax.scatter(euclidean_mean[0], euclidean_mean[1], c='#EF4444', s=500, marker='x', zorder=10, linewidth=6)
    ax.arrow(0, 0, euclidean_mean[0]-0.04, euclidean_mean[1]-0.04, head_width=0, head_length=0, fc='#EF4444', ec='#EF4444', linestyle='--', alpha=0.5, linewidth=2)
    
    # Plot Spherical Mean
    ax.scatter(spherical_mean[0], spherical_mean[1], c='white', s=600, marker='o', zorder=9, alpha=0.8)
    ax.scatter(spherical_mean[0], spherical_mean[1], c='#10B981', s=500, marker='*', zorder=10)
    ax.arrow(0, 0, spherical_mean[0]-0.03, spherical_mean[1]-0.03, head_width=0.03, head_length=0.03, fc='#10B981', ec='#10B981', linewidth=3)
    
    # Draw projection arrow from Euclidean to Spherical
    ax.annotate("", xy=spherical_mean, xytext=euclidean_mean,
                arrowprops=dict(arrowstyle="->", color="gray", linestyle="dashed", linewidth=2))
    
    return euclidean_mean, spherical_mean

def add_annotations(ax, e_mean, s_mean):
    # Annotate Euclidean Mean
    ax.text(e_mean[0] + 0.05, e_mean[1] - 0.1, 
            'Euclidean Mean\n(Inside Sphere)', 
            color='#EF4444', fontsize=12, fontweight='bold')
            
    # Annotate Spherical Mean
    ax.text(s_mean[0] + 0.05, s_mean[1] + 0.05, 
            'Spherical Mean\n(On Surface)', 
            color='#10B981', fontsize=12, fontweight='bold')
            
    # Annotate Normalization
    ax.text(0.6, 0.65, 'Normalization', color='gray', fontsize=10, rotation=45)

def main():
    fig, ax = setup_plot()
    draw_unit_circle(ax)
    points = generate_cluster_points()
    plot_vectors(ax, points)
    e_mean, s_mean = plot_means(ax, points)
    add_annotations(ax, e_mean, s_mean)
    
    # Legend
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color='#3B82F6', lw=0, marker='o'),
                    Line2D([0], [0], color='#EF4444', lw=0, marker='x'),
                    Line2D([0], [0], color='#10B981', lw=0, marker='*')]
    ax.legend(custom_lines, ['Data Points (Features)', 'Standard k-Means Center', 'Spherical k-Means Center'], loc='upper left', frameon=False)
    
    plt.tight_layout()
    plt.savefig('/Users/bytedance/Documents/Slidev-PPT/Clip/figures/spherical_kmeans_demo_v2.png', dpi=300, bbox_inches='tight')
    print("Image saved to /Users/bytedance/Documents/Slidev-PPT/Clip/figures/spherical_kmeans_demo_v2.png")

if __name__ == "__main__":
    main()
