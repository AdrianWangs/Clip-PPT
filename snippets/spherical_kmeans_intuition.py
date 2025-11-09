
import numpy as np
import matplotlib.pyplot as plt

def main():
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'aspect': 'equal'})
    
    # Draw unit circle
    circle = plt.Circle((0, 0), 1, color='#CCCCCC', fill=False, linewidth=1.5, linestyle='--')
    ax.add_artist(circle)

    # Data points on the unit circle
    angles = np.array([30, 70, 50, 90]) * np.pi / 180
    points = np.array([np.cos(angles), np.sin(angles)]).T
    
    # Plot data points as vectors
    for i, p in enumerate(points):
        ax.arrow(0, 0, p[0]*0.95, p[1]*0.95, head_width=0.04, head_length=0.06, fc=f'C{i}', ec=f'C{i}', length_includes_head=True)
        ax.text(p[0]*1.1, p[1]*1.1, f'$x_{i+1}$', fontsize=16, ha='center', va='center')

    # Sum vector
    sum_vec = points.sum(axis=0)
    ax.arrow(0, 0, sum_vec[0], sum_vec[1], head_width=0.04, head_length=0.06, fc='#333333', ec='#333333', length_includes_head=True, linestyle='-')
    ax.text(sum_vec[0] * 1.05, sum_vec[1] * 0.95, r'$\sum x_i$', fontsize=18, ha='center', va='bottom')

    # Centroid (normalized sum vector)
    centroid = sum_vec / np.linalg.norm(sum_vec)
    ax.arrow(0, 0, centroid[0]*0.95, centroid[1]*0.95, head_width=0.05, head_length=0.07, fc='red', ec='red', length_includes_head=True, linewidth=2)
    ax.text(centroid[0] * 1.15, centroid[1] * 1.1, 'c', fontsize=20, color='red', ha='center', va='center', weight='bold')

    # Dashed lines from origin to points
    for p in points:
        ax.plot([0, p[0]], [0, p[1]], linestyle=':', color='gray', linewidth=0.8)
    
    # Hide axes and ticks
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(False)

    plt.savefig('./figures/spherical_kmeans_intuition.svg', format='svg', bbox_inches='tight', pad_inches=0.1)
    plt.close()

if __name__ == "__main__":
    main()
