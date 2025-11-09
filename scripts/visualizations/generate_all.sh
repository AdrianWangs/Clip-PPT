#!/bin/bash
# 批量运行所有可视化脚本

echo "====== 开始生成球面k-Means可视化图片 ======"
echo ""

# 激活conda环境
eval "$(conda shell.bash hook)"
conda activate sse-tree

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 运行所有脚本
echo "[1/4] 生成图1: 两点与归一化中心..."
python "$SCRIPT_DIR/fig1_two_points_center.py"

echo ""
echo "[2/4] 生成图2: 四点向量和归一化..."
python "$SCRIPT_DIR/fig2_four_points_sum.py"

echo ""
echo "[3/4] 生成图3: 弦距与角距关系..."
python "$SCRIPT_DIR/fig3_chord_arc_distance.py"

echo ""
echo "[4/4] 生成图4: 3D球面聚类..."
python "$SCRIPT_DIR/fig4_spherical_clustering_3d.py"

echo ""
echo "====== 所有图片生成完成! ======"
echo "生成的图片位于: $SCRIPT_DIR/../../figures/"
ls -lh "$SCRIPT_DIR/../../figures/"spherical*.png "$SCRIPT_DIR/../../figures/"chord*.png 2>/dev/null
