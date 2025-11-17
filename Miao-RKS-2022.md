---
theme: seriph
background: /image/slides/image.png
title: 'Ranked Keyword Search Over Encrypted Cloud Data Through Machine Learning Method'
info: |
  ## 基于机器学习的加密云数据排序关键词搜索
  高效、安全、支持动态更新的云端加密数据检索方案
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
highlighter: shiki
lineNumbers: false
katex: true
hideInToc: true

---

# Ranked Keyword Search Over Encrypted Cloud Data Through Machine Learning Method

## 基于机器学习的加密云数据排序关键词搜索

<div class="pt-12">
  <span class="px-2 py-1 font-semibold">汇报人: 王宇哲</span>
</div>

<div class="pt-6 text-sm">
  Yinbin Miao, Wei Zheng, Xiaohua Jia, et al.
  <br>
  IEEE Transactions on Services Computing, 2022
</div>

<!--
大家好，今天我要分享的论文是《基于机器学习的加密云数据排序关键词搜索》，这是Yinbin Miao等人2022年发表在IEEE Transactions on Services Computing上的一篇关于云端加密数据高效检索的研究工作。

这篇论文主要解决了加密数据上的多关键词排序搜索问题，同时实现了高效的搜索性能和前向安全性。
-->

---
layout: two-cols-header
---

# 研究背景与动机

::left::

### 云数据加密搜索的重要性

- 云计算普及，数据外包成趋势
- 隐私泄露风险：明文存储不安全
- **加密数据搜索**成为刚需
- 排序搜索：返回最相关的Top-k结果
  - 避免返回全部匹配结果
  - 节省带宽和计算资源

::right::

### 实际应用场景

**医疗数据共享：**
- 医院将加密病历存储在云端
- 医生搜索"糖尿病+高血压"患者
- 返回最相关的Top-10病历

**企业文档管理：**
- 加密的文档库外包到云端
- 员工搜索关键词"合同+2022"
- 快速获取最相关的文档

<!--
我们先来看研究背景。随着云计算的普及，越来越多的个人和企业将数据外包到云端，以减少本地存储和计算负担。但是，明文存储数据会带来严重的隐私泄露风险。因此，加密数据搜索成为一个非常重要的研究课题。

传统的搜索会返回所有匹配的结果，但这样会浪费带宽和计算资源。排序搜索的目标是只返回最相关的Top-k个结果，比如最相关的10个文档。

右边是两个实际应用场景。第一个是医疗数据共享，医院把加密的病历存储在云端，医生可以搜索特定疾病的患者，快速获取最相关的病历。第二个是企业文档管理，员工可以在加密的文档库中搜索关键词，快速找到需要的文档。

这些应用都需要高效的加密数据排序搜索技术。
-->

---
layout: two-cols-header
---

# 现有方案的局限性

::left::

### 倒排索引方案的问题

**代表方案：** MRSE [Cao et al. 2013]

- 结构：关键词 → 文件列表映射
- 多关键词搜索：需要搜索每个关键词
- 然后对所有结果求交集
- **搜索复杂度：** $O(nm)$
  - $n$：文件数量
  - $m$：关键词数量
- **问题：** 线性复杂度，大规模数据集效率低

::right::

### 树索引方案的问题

**代表方案：** DMRS [Xia et al. 2015]

- 结构：平衡二叉树索引
- 搜索复杂度：$O(mz\log n)$
  - $z$：包含查询关键词的叶节点数
  - 当 $z \approx n$ 时，复杂度接近 $O(mn\log n)$
- **问题1：** 仍然较高的搜索开销
- **问题2：** 动态更新需要修改大量中间节点
- **问题3：** 缺乏前向安全性保护

<!--
现在我们来看现有方案的局限性。目前主流的方案可以分为两类。

第一类是基于倒排索引的方案，比如Cao等人2013年提出的MRSE方案。倒排索引存储从关键词到文件列表的映射。当搜索多个关键词时，需要分别搜索每个关键词，然后对所有结果求交集。这样的搜索复杂度是O(nm)，也就是说复杂度随文件数和关键词数线性增长。在大规模数据集上，这个线性复杂度会导致很高的搜索延迟。

第二类是基于树索引的方案，比如Xia等人2015年提出的DMRS方案。它使用平衡二叉树来构建索引，搜索复杂度是O(mz log n)，其中z是包含查询关键词的叶节点数量。虽然这个复杂度看起来比倒排索引好，但当z接近n时，复杂度会接近O(mn log n)，仍然很高。

除了搜索效率问题，树索引方案还有两个问题。第一是动态更新时需要修改大量中间节点，开销很大。第二是缺乏前向安全性保护，容易受到文件注入攻击。

因此，我们需要一个全新的方案来解决这些问题。
-->

---
layout: two-cols-header
---

## 本文核心贡献

::left::

### ML-RKS：基础方案

- **k-means聚类 + 平衡二叉树**
  - 将文件向量聚类成 $p$ 个簇
  - 每个簇构建独立的二叉树
  - 搜索复杂度：$O(mz\log L_y)$，其中 $n \gg L_y$

- **搜索策略**
  - 先选择分数最高的簇
  - 在该簇的树中搜索Top-k
  - 检查其他簇，确保结果准确

::right::

### ML-RKS+：增强方案

- **置换矩阵机制**
  - 基于版本号生成置换矩阵 $\mathbf{P}_{ver}$
  - 每次更新后，版本号递增
  - 历史查询token无法搜索新文件

- **前向安全性**
  - 防止文件注入攻击
  - 云服务器无法使用旧token搜索新数据

<div class="mt-4 p-1 bg-blue-50 rounded text-sm">
  <span class="font-semibold">实验结果（20Newsgroups数据集）：</span><br>
  <span class="text-xs mt-1">• 搜索时间 &lt; 100ms</span><br>
  <span class="text-xs">• 搜索准确率与RKS相当</span><br>
  <span class="text-xs">• 支持高效动态更新</span>
</div>

<!--
针对现有方案的不足，本文提出了两个方案：ML-RKS基础方案和ML-RKS+增强方案。

先看ML-RKS基础方案。它的核心思想是结合k-means聚类算法和平衡二叉树。具体来说，先用k-means将所有文件向量聚类成p个簇，比如5个簇。然后为每个簇单独构建一个平衡二叉树索引。这样做的好处是，搜索时只需要在选中的簇中搜索，而不是在全部文件中搜索。搜索复杂度降低到O(mz log Ly)，其中Ly是选中簇的文件数量，远小于总文件数n。

搜索策略是这样的：首先计算查询向量与每个簇中心的相似度分数，选择分数最高的簇。然后在该簇的二叉树中搜索Top-k结果。为了保证准确性，还需要检查其他簇，确保返回的结果确实是全局的Top-k。

ML-RKS在静态场景下很高效，但在动态场景下存在前向安全性问题。因此我们提出了ML-RKS+增强方案。

ML-RKS+的核心创新是引入了置换矩阵机制。系统维护一个版本号ver，每次文件更新时版本号递增。基于版本号，数据拥有者会生成一个新的置换矩阵Pver，并用它更新所有的加密索引。用户查询时，也需要使用当前版本号生成对应的置换矩阵。这样，历史的查询token就无法搜索新添加的文件，从而实现了前向安全性，防止了文件注入攻击。

右下角是在20Newsgroups数据集上的实验结果。搜索时间小于100毫秒，搜索准确率与基准方案RKS相当，同时支持高效的动态更新。
-->

---
layout: default
---

## 系统模型与威胁模型

<div class="grid grid-cols-2 gap-8 items-start mt-1">
<div>

- **数据拥有者 (DO)**
  - 生成密钥，管理用户权限
  - 构建加密索引和加密文件
  - 执行动态更新操作

- **数据用户 (DU)**
  - 从DO获取密钥
  - 生成加密查询token
  - 解密搜索结果

- **云服务器 (CS)**
  - 存储加密索引和加密文件
  - 执行搜索操作
  - 返回Top-k加密结果

</div>
<div>

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/1fcf8300fb08de6368af2d42a638858855eef936384a1c336cc5790ec3882d31.jpg" alt="系统模型" class="w-11/12 mx-auto">
<div class="text-center text-xs text-gray-500 mt-1">图1：系统架构模型</div>

### 威胁模型

**Known Ciphertext Model（已知密文模型）：**
- CS只能访问加密索引、加密文件、加密查询token

**Known Background Model（已知背景模型）：**
- CS额外拥有统计信息、查询相关性等背景知识

</div>
</div>

<!--
现在我们来看系统模型和威胁模型。

系统包含三个实体。第一是数据拥有者DO，他负责生成密钥，管理用户的访问权限。在离线阶段，DO构建加密的索引和加密的文件，上传到云端。在动态场景下，DO还负责执行文件的添加、删除、修改等更新操作。

第二是数据用户DU。当DU想要搜索时，他先从DO那里获取密钥，然后生成加密的查询token发送给云服务器。收到搜索结果后，DU在本地解密得到明文结果。

第三是云服务器CS。CS存储加密的索引和加密的文件，执行搜索操作，返回加密的Top-k结果。

右边这张图展示了整个交互流程。第一步，DO上传加密索引和文件到CS。第二步，DU从DO获取密钥。第三步，DU发送加密查询token给CS。第四步，CS返回Top-k加密结果给DU。

关于威胁模型，本文考虑了两种。第一种是已知密文模型，在这个模型下，CS只能访问加密的索引、加密的文件和加密的查询token，无法获得明文信息。

第二种是已知背景模型，这是一个更强的威胁模型。在这个模型下，CS除了密文数据，还拥有一些背景知识，比如数据集的统计信息、查询之间的相关性等。本文的方案在这两种威胁模型下都能保护索引和查询的隐私。
-->

---
layout: two-cols-header
---

## 问题定义：VSM与TF-IDF

::left::

### 向量空间模型 (VSM)

给定：
- 文件集合 $\mathcal{F} = \{f_1, \ldots, f_n\}$
- 关键词集合 $\mathcal{W} = \{w_1, \ldots, w_m\}$

每个文件 $f_i$ 表示为向量：
$$\mathbf{d}_i = (v_{i,1}, \ldots, v_{i,m})$$

其中 $v_{i,j}$ 是关键词 $w_j$ 在文件 $f_i$ 中的TF-IDF值

查询 $q$ 表示为向量：
$$\mathbf{q} = (\omega_1, \ldots, \omega_m)$$

其中 $\omega_j$ 是关键词 $w_j$ 的权重

::right::

### TF-IDF计算

**词频 (TF)：**
$$TF_{i,j} = \frac{1 + \ln m_{i,j}}{|f_i|}$$
- $m_{i,j}$：关键词 $w_j$ 在文件 $f_i$ 中的出现次数
- $|f_i|$：文件 $f_i$ 的大小

**逆文档频率 (IDF)：**
$$IDF_j = \ln\left(1 + \frac{n}{n_j}\right)$$
- $n_j$：包含关键词 $w_j$ 的文件数量

**TF-IDF值：**
$$v_{i,j} = TF_{i,j} \cdot IDF_j$$

<!--
现在我们来看问题定义。本文使用向量空间模型VSM和TF-IDF规则来表示文件和查询。

在向量空间模型中，给定n个文件和m个关键词，我们把每个文件表示成一个m维向量。向量的每个元素对应一个关键词的TF-IDF值。同样，查询也表示成一个m维向量，每个元素是对应关键词的权重。这样，文件和查询都在同一个向量空间中，可以用向量运算来计算相似度。

右边是TF-IDF的计算方法。TF是词频，表示一个关键词在文件中的重要性。公式是(1+ln m_ij)/|f_i|，其中m_ij是关键词在文件中的出现次数，|f_i|是文件大小。加1和取对数是为了平滑处理，避免词频过大或过小。

IDF是逆文档频率，表示一个关键词在整个数据集中的区分度。公式是ln(1+n/n_j)，其中n是总文件数，n_j是包含该关键词的文件数。如果一个关键词在很多文件中都出现，那么它的IDF值就小，说明它的区分度低。反之，如果只在少数文件中出现，IDF值就大，说明它更有区分性。

最后，TF-IDF值就是TF乘以IDF。这个值综合考虑了关键词在单个文件中的重要性和在整个数据集中的区分度，能够很好地衡量关键词对文件的代表性。
-->

---
layout: default
---

## 相似度分数定义

<div class="mt-12">

文件 $f_i$ 与查询 $q$ 的相似度分数通过**内积计算**：

$$
\mathcal{S}(\mathbf{d}_i, \mathbf{q}) = \mathbf{d}_i \cdot \mathbf{q} = \sum_{w_j \in q} v_{i,j} \cdot \omega_j = \sum_{w_j \in q} TF_{i,j} \cdot IDF_j \cdot \omega_j
$$

</div>

<div class="mt-12 grid grid-cols-2 gap-12">
<div>

### 排序机制

- 计算所有文件的相似度分数
- 按分数**降序排列**
- 返回Top-k个最相关文件

</div>
<div>

### 加密挑战

- 云服务器存储的是**加密数据**
- 需要在密文上计算相似度
- 使用Secure k-NN技术保持内积：
  $$\widehat{\mathbf{d}}_i \cdot \widehat{\mathbf{q}} = \mathbf{d}_i \cdot \mathbf{q}$$

</div>
</div>

<!--
现在我们来看相似度分数是如何定义的。

在我们的系统中，文件和查询的相似度通过内积来计算。具体来说，就是文件向量d_i和查询向量q的点积。展开后，就是对所有查询关键词，累加它们的TF-IDF值乘以用户指定的权重。这个内积值越高，说明文件与查询越相关。

左边是排序机制。系统会计算所有文件的相似度分数，按降序排列，然后返回Top-k个最相关的文件给用户。

右边是加密带来的挑战。由于云服务器存储的是加密数据，我们需要在密文上计算相似度。这就用到了Secure k-NN技术，它的核心思想是通过特殊的加密方式，让加密向量的内积等于明文向量的内积。这样云服务器就可以在不知道明文的情况下，正确计算相似度分数。
-->

---
layout: two-cols-header
---

## k-means聚类与平衡二叉树

::left::

### k-means聚类

**目标：** 将 $n$ 个文件向量分成 $p$ 个簇

**算法流程：**
1. 随机选择 $p$ 个初始簇中心 $\{\mathbf{c}_1, \ldots, \mathbf{c}_p\}$
2. 将每个文件向量 $\mathbf{d}_i$ 分配到最近的簇：
   $$y = \arg\max_j \mathcal{S}(\mathbf{d}_i, \mathbf{c}_j)$$
3. 重新计算簇中心（簇内所有向量的平均）
4. 重复步骤2-3直到收敛

**优势：**
- 减少搜索空间：只需在选中的簇中搜索
- $L_y \ll n$，其中 $L_y$ 是簇 $y$ 的文件数

::right::

### 平衡二叉树构建

**对每个簇构建独立的二叉树：**

1. **叶节点：** 存储文件向量 $\{\mathbf{d}_1, \ldots, \mathbf{d}_{L_y}\}$

2. **中间节点：** 自底向上生成
   - 每个节点向量 $\mathbf{d}_x[j] = \max\{\mathbf{d}_l[j], \mathbf{d}_r[j]\}$
   - $\mathbf{d}_l$、$\mathbf{d}_r$ 是左右子节点向量

3. **根节点：** 替换簇中心 $\mathbf{c}_y$

**优势：**
- 树高度 $O(\log L_y)$
- 搜索时可以剪枝，避免遍历所有叶节点

<!--
现在我们来看ML-RKS方案的核心技术：k-means聚类和平衡二叉树。

k-means聚类的目标是将n个文件向量分成p个簇，比如分成5个簇。算法流程很经典。首先随机选择p个初始簇中心。然后，将每个文件向量分配到与它相似度最高的簇中心。接下来，重新计算每个簇的中心，也就是簇内所有向量的平均值。重复这个分配和更新的过程，直到簇中心不再变化。

k-means聚类的优势是减少了搜索空间。原本需要在全部n个文件中搜索，现在只需要在选中的簇中搜索。而簇的文件数Ly远小于总文件数n，这样就大大降低了搜索复杂度。

有了聚类结果，接下来为每个簇构建一个平衡二叉树。右边是树的构建方法。

首先，叶节点存储簇内的所有文件向量。然后，自底向上生成中间节点。每个中间节点的向量是怎么得到的呢？对于向量的每一维，取左右子节点在该维度上的最大值。这样，中间节点的向量在每一维都不小于它的子节点。最后，根节点的向量会替换原来的簇中心。

平衡二叉树的优势是树的高度只有O(log Ly)，远小于线性高度。而且在搜索时，我们可以利用节点向量进行剪枝。如果一个节点的分数已经小于当前的Top-k结果，就不需要继续搜索它的子树了，这样可以避免遍历所有叶节点，进一步提高搜索效率。
-->

---
layout: default
---


## 二叉树搜索示例
<div class="grid grid-cols-5 gap-0 h-full place-items-center">

<div class="col-span-3 flex justify-center items-center mt-8">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/f82c7f1d63131f0742d8ef6f2319562d43404ab1ed9b00f9d4a4e6908b490e76.jpg" alt="二叉树搜索示例" class="w-9/12">
</div>


<div class="col-span-2 mt-6 text-sm">

**场景：** 关键词集合 $\{w_1, w_2, w_3\}$，查询向量 $\mathbf{q} = (0.1, 0.5, 0.2)$，搜索Top-2

**步骤：**
1. 根节点 $\mathbf{n}_{ro} = (0.6, 0.7, 0.7)$，计算左右子节点分数：$\mathcal{S}(\mathbf{n}_{1,0}, \mathbf{q}) > \mathcal{S}(\mathbf{n}_{1,1}, \mathbf{q})$，选择左子树
2. 继续向下：$\mathcal{S}(\mathbf{n}_{2,0}, \mathbf{q}) > \mathcal{S}(\mathbf{n}_{2,1}, \mathbf{q})$，选择左子树
3. 计算叶节点：$\mathcal{S}(\mathbf{d}_1, \mathbf{q}) = 0.46$，$\mathcal{S}(\mathbf{d}_2, \mathbf{q}) = 0.39$
4. **剪枝：** $\mathcal{S}(\mathbf{n}_{2,1}, \mathbf{q}) = 0.22 < 0.39$，跳过 $\mathbf{d}_3, \mathbf{d}_4$
5. 检查右侧：$\mathcal{S}(\mathbf{n}_{1,1}, \mathbf{q}) = 0.40 > 0.39$，需要计算 $\mathbf{d}_5, \mathbf{d}_6$
6. 最终结果：$\mathbf{d}_1$ (0.46)、$\mathbf{d}_6$ (0.40)

</div>
</div>
<!--
现在我们通过一个具体的例子来理解二叉树搜索的过程。

假设我们有3个关键词w1、w2、w3，查询向量是(0.1, 0.5, 0.2)，我们要搜索Top-2结果。上面这张图展示了一个平衡二叉树，包含6个文件向量d1到d6。

搜索步骤如下。第一步，从根节点n_ro出发，它的向量是(0.6, 0.7, 0.7)。我们计算左右两个子节点与查询向量的相似度分数，发现左子节点n_1,0的分数更高，所以选择左子树继续搜索。

第二步，在n_1,0节点，继续比较它的左右子节点，发现n_2,0的分数更高，继续选择左子树。

第三步，到达叶节点层。我们计算d1和d2的分数，得到0.46和0.39。现在我们有两个候选结果了。

第四步是关键的剪枝操作。我们看n_2,1节点，它的分数是0.22，小于当前的第二名0.39。这意味着n_2,1的子树中不可能有比0.39更高的分数，因为子节点的分数不会超过父节点。所以我们可以跳过d3和d4，不需要计算它们的分数。

第五步，回到上一层，检查右侧的n_1,1节点。它的分数是0.40，大于当前的第二名0.39，说明它的子树中可能有更高分的结果。所以我们需要计算d5和d6的分数。

最后，我们得到Top-2结果：d1的分数是0.46，d6的分数是0.40。

这个例子展示了二叉树搜索的优势。我们只计算了4个叶节点的分数（d1、d2、d5、d6），跳过了d3和d4，减少了计算量。如果文件数量很多，剪枝带来的效率提升会更明显。
-->

---
layout: two-cols-header
---

## Secure k-NN加密机制

::left::

### 向量分裂与加密

**密钥：** $SK = (\mathbf{S}, \mathbf{M}_1, \mathbf{M}_2)$
- $\mathbf{S} \in \{0,1\}^{\widetilde{m}}$：分裂向量
- $\mathbf{M}_1, \mathbf{M}_2 \in \mathbb{R}^{\widetilde{m} \times \widetilde{m}}$：可逆矩阵

**文件向量分裂：** $\mathbf{d}_i \to (\mathbf{d}_{i,1}, \mathbf{d}_{i,2})$
- 若 $\mathbf{S}[j] = 0$：$\mathbf{d}_{i,1}[j] = \mathbf{d}_{i,2}[j] = \mathbf{d}_i[j]$
- 若 $\mathbf{S}[j] = 1$：$\mathbf{d}_{i,1}[j] + \mathbf{d}_{i,2}[j] = \mathbf{d}_i[j]$

**查询向量分裂：** $\mathbf{q} \to (\mathbf{q}_1, \mathbf{q}_2)$
- 若 $\mathbf{S}[j] = 0$：$\mathbf{q}_1[j] + \mathbf{q}_2[j] = \mathbf{q}[j]$
- 若 $\mathbf{S}[j] = 1$：$\mathbf{q}_1[j] = \mathbf{q}_2[j] = \mathbf{q}[j]$

::right::

### 加密与内积保持

**文件向量加密：**
$$\widehat{\mathbf{d}}_i = (\mathbf{M}_1^\top \mathbf{d}_{i,1}, \mathbf{M}_2^\top \mathbf{d}_{i,2})$$

**查询向量加密：**
$$\widehat{\mathbf{q}} = (\mathbf{M}_1^{-1} \mathbf{q}_1, \mathbf{M}_2^{-1} \mathbf{q}_2)$$

**内积保持性：**
$$
\begin{align}
\widehat{\mathbf{d}}_i \cdot \widehat{\mathbf{q}} &= \mathbf{M}_1^\top \mathbf{d}_{i,1} \cdot \mathbf{M}_1^{-1} \mathbf{q}_1 + \mathbf{M}_2^\top \mathbf{d}_{i,2} \cdot \mathbf{M}_2^{-1} \mathbf{q}_2 \\
&= \mathbf{d}_{i,1} \cdot \mathbf{q}_1 + \mathbf{d}_{i,2} \cdot \mathbf{q}_2 \\
&= \mathbf{d}_i \cdot \mathbf{q}
\end{align}
$$

<!--
现在我们来看Secure k-NN加密机制，这是保证在密文上正确计算相似度的关键技术。

首先看密钥的组成。密钥包含三部分：一个分裂向量S，它的每个元素是0或1；两个可逆矩阵M1和M2。这些都是DO生成的秘密密钥。

向量分裂是这样的。对于文件向量，我们根据分裂向量S把它分成两部分d_i,1和d_i,2。如果S的第j位是0，那么d_i,1和d_i,2在第j维都等于原向量d_i的值。如果S的第j位是1，那么d_i,1和d_i,2在第j维的和等于原向量。

查询向量的分裂规则正好相反。如果S的第j位是0，q1和q2的和等于原向量。如果S的第j位是1，q1和q2都等于原向量。这个相反的规则很关键，是保证内积不变的核心。

有了分裂后的向量，接下来进行加密。文件向量的加密是用矩阵M1的转置乘以d_i,1，用M2的转置乘以d_i,2，得到一个加密向量对。查询向量的加密是用M1的逆矩阵乘以q1，用M2的逆矩阵乘以q2。

右边是内积保持性的证明。加密向量的内积等于M1转置d_i,1点乘M1逆q1，加上M2转置d_i,2点乘M2逆q2。矩阵的转置和逆相消，得到d_i,1点乘q1加上d_i,2点乘q2。根据分裂规则，这个和恰好等于原向量d_i点乘q。

所以，加密后的向量在计算内积时，结果和明文向量的内积完全一样。这就是Secure k-NN的核心性质。云服务器可以在密文上正确计算相似度分数，但无法从密文中恢复出明文向量。
-->

---
layout: two-cols-header
---

## ML-RKS方案构建（一）

::left::

### 密钥生成 (KeyGen)

**输入：** 安全参数 $\kappa$

**输出：**
- $\mathbf{S} \in \{0,1\}^{\widetilde{m}}$：分裂向量
- $\mathbf{M}_1, \mathbf{M}_2 \in \mathbb{R}^{\widetilde{m} \times \widetilde{m}}$：可逆矩阵
- $k_e$：对称加密密钥（AES/DES）

**维度扩展：** $\widetilde{m} = m + U + 2$
- $m$：关键词数量
- $U$：虚拟关键词数量
- $+2$：token不可区分性 + 前向安全

::right::

### 索引生成 (BuildIndex)

**文件向量构建：**
$$\mathbf{d}_i = \{v_{i,1}, \ldots, v_{i,m}, \varepsilon_{i,m+1}, \ldots, \varepsilon_{i,m+U}, 1, 1\}$$
- 前 $m$ 维：TF-IDF值
- 中间 $U$ 维：随机虚拟值 $\sim N(\mu, \sigma^2)$
- 最后2维：固定为1

**构建步骤：**
1. k-means聚类 → 分成 $p$ 个簇
2. 每个簇构建平衡二叉树
3. 用Secure k-NN加密所有节点向量
4. 上传加密索引到云端

<!--
现在我们来看ML-RKS方案的构建过程。这一页介绍前两个阶段：密钥生成和索引生成。

左边是密钥生成阶段。数据拥有者DO输入一个安全参数κ，生成密钥。密钥包含三个部分：分裂向量S，它的每个元素是0或1；两个可逆矩阵M1和M2；以及对称加密密钥ke用于加密文件本身。

这里有个重要的维度扩展。原始向量维度是m（关键词数量），但我们把它扩展到m+U+2。U是虚拟关键词数量，用来增强隐私保护。加2是为了实现token的不可区分性和支持前向安全。

右边是索引生成阶段。首先构建文件向量，它有m+U+2维。前m维是我们之前讲的TF-IDF值。中间U维是随机的虚拟值，服从正态分布，用来混淆真实的TF-IDF值。最后2维固定为1，用于特殊目的。

构建步骤分四步。第一步用k-means算法把所有文件向量聚类成p个簇，比如5个簇。第二步为每个簇构建一个平衡二叉树索引。第三步用Secure k-NN算法加密所有节点向量，包括根节点、中间节点和叶节点。第四步把加密索引上传到云端。

通过聚类，我们把搜索空间从全部n个文件缩减到单个簇的Ly个文件，大大提高了搜索效率。
-->

---
layout: two-cols-header
---

## ML-RKS方案构建（二）

::left::

### 查询生成 (Trapdoor)

**查询向量构建：**
$$\mathbf{q} = (\alpha\omega_1, \ldots, \alpha\omega_m, \alpha, 0, \ldots, \alpha, \beta, 1)$$

**各部分说明：**
- 前 $m$ 维：$\alpha \omega_j$（关键词权重 × 随机数）
- 中间 $U$ 维：随机选 $V$ 个设为 $\alpha$，其余为0
- 倒数第2维：随机数 $\beta$
- 最后1维：固定为1

**加密：**
$$\widehat{\mathbf{q}} = (\mathbf{M}_1^{-1}\mathbf{q}_1, \mathbf{M}_2^{-1}\mathbf{q}_2)$$

::right::

### 密文搜索 (Search)

**搜索步骤：**
1. 计算每个簇中心与查询的分数 $\mathcal{S}(\widehat{\mathbf{c}}_y, \widehat{\mathbf{q}})$
2. 选择分数最高的簇
3. 在该簇的二叉树中搜索Top-k

**检查机制：**
- **Case 1:** 第k个结果分数 ≥ 其他簇 → 直接返回
- **Case 2:** 有其他簇分数更高 → 继续搜索并更新

**最终分数：**
$$\mathcal{S}(\widehat{\mathbf{d}}_i, \widehat{\mathbf{q}}) = \alpha\left(\sum_{j=1}^m v_{i,j}\omega_j + \sum_{j=m+1}^{m+U} \varepsilon_{i,j}\right) + \beta + 1$$

<!--
继续看ML-RKS方案的后两个阶段：查询生成和密文搜索。

左边是查询生成阶段。用户首先构建查询向量，它也是m+U+2维。前m维是关键词权重ω_j乘以一个随机数α。这个α很关键，它隐藏了真实的权重值，防止服务器推断出用户对哪些关键词更感兴趣。

中间U维是虚拟关键词部分。用户随机选V个维度设为α，其余为0。这样做是为了和文件向量的虚拟部分匹配，同时增加随机性。倒数第二维是另一个随机数β，最后一维固定为1。

然后用密钥对查询向量进行分裂和加密，得到加密的查询token发送给云服务器。

右边是密文搜索阶段。云服务器收到加密查询后，首先计算查询向量与每个簇中心的相似度分数，选择分数最高的簇。然后在该簇的二叉树中搜索Top-k结果。

这里有个检查机制确保准确性。Case 1，如果第k个结果的分数已经大于等于其他所有簇的分数，说明Top-k结果肯定在这个簇里，可以直接返回。Case 2，如果有其他簇的分数更高，说明那个簇中可能有更相关的文件，需要继续搜索该簇并更新Top-k结果。

最终的相似度分数公式在底部。它包含三部分：真实TF-IDF的贡献、虚拟关键词的贡献、以及随机数β+1。由于α、β和虚拟值都是随机的，云服务器无法从分数中推断出真实的TF-IDF值和权重，从而保护了隐私。
-->

---
layout: two-cols-header
---

## 前向安全问题

::left::

### 威胁场景：文件注入攻击

**攻击步骤：**

1. 用户提交查询token $\widehat{\mathbf{q}}_1$，CS返回结果集 $\mathcal{R}_1$
2. 攻击者（或恶意CS）注入新文件 $f_{new}$
3. CS用旧token $\widehat{\mathbf{q}}_1$ 重新搜索，得到 $\mathcal{R}_2$
4. 对比 $\mathcal{R}_1$ 和 $\mathcal{R}_2$：
   - 若 $f_{new} \in \mathcal{R}_2$ 但 $f_{new} \notin \mathcal{R}_1$
   - 推断：$f_{new}$ 包含查询关键词

**隐私泄露：**
- 攻击者可以通过注入大量文件，逐步推断出查询关键词
- 知道历史查询的关键词信息

::right::

### 前向安全定义

**目标：** 防止CS用历史token搜索新添加的文件

**形式化定义：**
- 设 $t_1$ 时刻提交查询 $q_1$，返回结果集 $\mathcal{R}_1$
- 设 $t_2$ 时刻添加文件 $f_{new}$（$t_2 > t_1$）
- CS不能用 $q_1$ 的token确定 $f_{new}$ 是否满足 $q_1$

**ML-RKS的问题：**
- 静态设置下没有前向安全问题
- 动态更新时，旧token仍能搜索新文件
- 需要引入版本控制机制

<!--
ML-RKS在静态场景下很高效，但在动态场景下存在前向安全问题。我们来详细看一下这个威胁。

左边是文件注入攻击的场景。假设用户在t1时刻提交了一个查询token q̂1，CS返回了结果集R1。之后，攻击者或者恶意的CS在t2时刻注入了一个新文件f_new。然后，CS用旧的token q̂1重新搜索，得到新的结果集R2。

对比R1和R2，如果f_new出现在R2中但不在R1中，那么攻击者就可以推断出f_new包含了查询q1的关键词。更严重的是，攻击者可以通过注入大量精心构造的文件，逐步推断出历史查询的关键词信息。这就是文件注入攻击，它会导致查询隐私的泄露。

右边是前向安全的形式化定义。前向安全的目标是防止CS用历史的token搜索新添加的文件。具体来说，如果t1时刻提交了查询q1，t2时刻添加了文件f_new（t2晚于t1），那么CS不能用q1的token来判断f_new是否满足q1。

ML-RKS在静态设置下没有这个问题，因为文件集合是固定的。但在动态更新时，旧的token仍然能够搜索新添加的文件，这就违反了前向安全。为了解决这个问题，我们需要引入版本控制机制，让每次更新后，历史的token失效。这就是ML-RKS+要解决的问题。
-->

---
layout: two-cols-header
---

## ML-RKS+：置换矩阵机制

::left::

### 版本控制与置换矩阵

**密钥扩展：** $SK^* = (SK, \mathcal{H}, \mathbf{P})$
- $\mathcal{H}$：哈希函数
- $\mathbf{P} \in \mathbb{R}^{m \times m}$：置换矩阵（每行每列恰有一个1）

**版本号生成：**
$$\delta_{ver} = \mathcal{H}(\det(\mathbf{M}_1) \mid \det(\mathbf{M}_2) \mid ver)$$

**置换矩阵生成：**
1. 计算 $\mathbf{P}^{\delta_{ver}}$（矩阵的 $\delta_{ver}$ 次幂）
2. 将最后一行的"1"替换为：
   $$\theta = \frac{\delta_{ver}+1}{\delta_{ver}} + \frac{\delta_{ver}}{\delta_{ver}+1}$$
3. 得到 $\mathbf{P}_{ver}$

::right::

### 索引与查询更新

**加密置换矩阵：**
$$\widehat{\mathbf{P}}_{ver} = (\mathbf{M}_1^{-1}\mathbf{P}_{ver}\mathbf{M}_2^\top, \mathbf{M}_2^{-1}\mathbf{P}_{ver}\mathbf{M}_1^\top)$$

**索引更新：**
- 每个节点向量乘以 $\widehat{\mathbf{P}}_{ver}$
- 例如：$\widehat{\mathbf{c}}_y \to \widehat{\mathbf{c}}_y \cdot \widehat{\mathbf{P}}_{ver}$

**查询token生成：**
$$\widehat{\mathbf{q}}' = (\mathbf{M}_2^{-1}\mathbf{P}^{\delta_{ver}}\mathbf{q}_1, \mathbf{M}_1^{-1}\mathbf{P}^{\delta_{ver}}\mathbf{q}_2)$$

**内积保持：**
$$\mathcal{S}(\widehat{\mathbf{c}}_y \cdot \widehat{\mathbf{P}}_{ver}, \widehat{\mathbf{q}}') = \mathbf{c}_y \mathbf{P}_{ver} \mathbf{P}^{\delta_{ver}} \mathbf{q}$$

<!--
现在我们来看ML-RKS+如何通过置换矩阵机制实现前向安全。

首先是密钥扩展。在原来的密钥基础上，增加了一个哈希函数H和一个置换矩阵P。置换矩阵的特点是每行每列恰好有一个1，其余都是0。

版本控制是这样的。系统维护一个版本号ver，初始值是0。每次文件更新时，版本号递增。基于版本号，我们计算δ_ver，它是M1和M2的行列式以及版本号ver的哈希值。这个δ_ver会随着版本号的变化而变化。

接下来生成置换矩阵P_ver。首先计算P的δ_ver次幂，得到P^δ_ver。由于P是置换矩阵，它的幂仍然是置换矩阵。然后，我们做一个特殊的修改，把最后一行的"1"替换成θ，θ的值是(δ_ver+1)/δ_ver加上δ_ver/(δ_ver+1)。这个θ是一个与版本号相关的特殊值，用于区分不同版本。

有了P_ver，我们需要对它进行加密，得到P̂_ver。加密方式和查询向量类似，用密钥矩阵的逆和转置进行变换。

索引更新很简单。每次版本号更新后，DO用新的P̂_ver乘以所有节点向量，更新整个加密索引。比如簇中心从ĉ_y更新为ĉ_y点乘P̂_ver。

查询token的生成也要相应调整。用户需要用当前的版本号计算P^δ_ver，然后用它来加密查询向量。这样，查询token也带上了版本信息。

右下角是内积保持性的验证。更新后的索引与更新后的查询token计算内积，经过矩阵运算的展开和化简，最终等于明文向量c_y乘以P_ver、再乘以P^δ_ver、再乘以q。关键是，P_ver和P^δ_ver的组合与版本号相关。如果使用旧版本的查询token，这个组合就对不上，计算出的分数就是错误的，无法得到正确的搜索结果。

这就是置换矩阵机制实现前向安全的原理。每次更新后，版本号变化，置换矩阵也变化，历史的查询token无法在新的索引上正确搜索。
-->

---
layout: default
---

<!--TODO 这一块文字部分不要花里胡哨的，直接markdown，防止无法渲染公式，在右半页自上而下排版就行-->
## 动态更新操作示例

<div class="grid grid-cols-5 gap-0 h-full place-items-center">

<div class="col-span-3 flex justify-center items-center mt-6">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/a36c1fb24cd44737174aa7a79c2efd5fc45555bcfe70cbe97a400bb2d4abee53.jpg" alt="文件更新示例" class="w-10/12">
</div>

<div class="col-span-2 mt-6 grid grid-cols-3 gap-6">

<div class="text-center p-4 bg-blue-50 rounded">
  <p class="font-semibold text-blue-700">文件修改</p>
  <p class="text-sm mt-2">$\mathbf{d}_1 \to \mathbf{d}_1'$</p>
  <p class="text-xs mt-2 text-gray-600">更新路径节点</p>
  <p class="text-xs text-gray-600">版本号 $ver' = 1$</p>
  <p class="text-xs mt-2 font-semibold">复杂度: $O(\log L_y)$</p>
</div>

<div class="text-center p-4 bg-green-50 rounded">
  <p class="font-semibold text-green-700">文件删除</p>
  <p class="text-sm mt-2">删除 $\mathbf{d}_2$</p>
  <p class="text-xs mt-2 text-gray-600">设置为零向量</p>
  <p class="text-xs text-gray-600">版本号 $ver' = 2$</p>
  <p class="text-xs mt-2 font-semibold">复杂度: $O(\log L_y)$</p>
</div>

<div class="text-center p-4 bg-red-50 rounded">
  <p class="font-semibold text-red-700">文件添加</p>
  <p class="text-sm mt-2">添加 $\mathbf{d}_5$</p>
  <p class="text-xs mt-2 text-gray-600">创建新节点</p>
  <p class="text-xs text-gray-600">版本号 $ver' = 3$</p>
  <p class="text-xs mt-2 font-semibold">复杂度: $O(\log L_y)$</p>
</div>

</div>
</div>

<!--
现在我们来看ML-RKS+如何处理动态更新操作。上面这张图展示了一个簇c1的二叉树，初始包含4个文件d1到d4，版本号为0。

三种更新操作的核心流程类似：首先更新受影响的节点，然后版本号递增，生成新的置换矩阵，用它更新所有节点向量，最后上传到云端。

文件修改是把d1改成d1'，只需要更新从d1到根节点的路径，版本号更新为1。文件删除是把d2设为零向量，这样它的分数为0不会被搜索到，版本号更新为2。文件添加是添加d5，需要创建新的叶节点和父节点，版本号更新为3。

三种操作的复杂度都是对数级别O(log Ly)，因为只需要更新树的一条路径或少量节点。
-->

---
layout: two-cols-header
---

## 动态更新机制详解

::left::

### 更新步骤（以文件修改为例）

1. **更新节点向量**
   - 修改叶节点 $\mathbf{d}_1 \to \mathbf{d}_1'$
   - 更新路径节点 $\mathbf{n}_1, \mathbf{c}_1$

2. **版本号递增**
   - $ver' = ver + 1$
   - 计算 $\delta_{ver'} = \mathcal{H}(\det(\mathbf{M}_1)|\det(\mathbf{M}_2)|ver')$

3. **生成置换矩阵**
   - 计算 $\mathbf{P}^{\delta_{ver'}}$
   - 替换最后一行元素为 $\theta'$
   - 加密得到 $\widehat{\mathbf{P}}_{ver'}$

::right::

### 关键优势

**效率优势：**
- 只更新选中簇的树（$L_y \ll n$）
- 不影响其他簇，开销小
- 复杂度：修改/删除 $O(\log L_y)$，添加 $O(\log L_y + 2)$

**安全优势：**
- 版本号变化 → 置换矩阵变化
- 旧token使用旧 $\mathbf{P}^{\delta_{ver}}$，新索引使用新 $\mathbf{P}_{ver'}$
- 版本不匹配 → 搜索结果错误
- **实现前向安全**

<!--
现在详细看一下动态更新的机制。

左边是更新步骤，以文件修改为例。第一步是更新节点向量，把叶节点d1改成d1'，然后自底向上更新路径上的所有节点，包括n1和c1。

第二步是版本号递增。版本号从ver更新为ver'，比如从0更新到1。然后基于新的版本号和密钥矩阵的行列式，用哈希函数计算δ_ver'。

第三步是生成新的置换矩阵。首先计算P的δ_ver'次幂，得到P^δ_ver'。然后把最后一行的元素"1"替换成一个与版本号相关的特殊值θ'，得到P_ver'。最后用密钥对它加密，得到P̂_ver'。

有了新的置换矩阵，DO用它乘以簇中所有节点的向量，更新整个加密索引，然后上传到云端。

右边是关键优势。从效率角度看，由于使用了聚类，每次只需要更新选中簇的树，而不是全部文件。簇的大小Ly远小于总文件数n，所以更新开销很小。修改和删除的复杂度是O(log Ly)，添加稍高一点是O(log Ly +2)，但都是对数级别。

从安全角度看，每次更新后版本号变化，置换矩阵也变化。旧的查询token使用旧版本的置换矩阵P^δ_ver，而新的索引使用新版本的P_ver'。版本不匹配会导致内积计算出的分数是错误的，无法得到正确的搜索结果。这样就实现了前向安全，防止历史查询token搜索新添加的文件。
-->

---
layout: two-cols-header
---

## 安全分析（一）

::left::

### Theorem 1: 索引与查询保密性

ML-RKS和ML-RKS+保证索引和查询的保密性

**证明思路：**
- 加密索引：$2nm$ 个方程，$2nm + 2m^2$ 个未知数
- 加密查询：$2m$ 个方程，$2m^2$ 个未知数
- **未知数数量 > 方程数量 → 无法求解**

::right::

### Theorem 2: Token不可区分性

同一查询的多次token不可区分

**证明思路：**
- 查询向量分裂时引入随机性
- 两次查询相同的概率 $\approx \gamma^\epsilon$
  - $\gamma \ll \frac{1}{2}$
  - $\epsilon$ 是分裂向量中0的数量
- **概率接近0 → 不可区分**

<!--
现在我们来看安全分析的前两个定理。

Theorem 1是关于索引和查询的保密性。证明的思路是从线性代数的角度。对于加密索引，虽然有2nm个方程，但有2nm+2m²个未知数。对于加密查询，有2m个方程，但有2m²个未知数。未知数数量大于方程数，所以云服务器无法通过求解线性方程组来推断出明文信息。

Theorem 2是关于token的不可区分性。查询向量在分裂时引入了随机性，两次查询得到相同分裂的概率接近0，所以云服务器无法区分两次查询是否来自同一个原始查询。
-->

---
layout: two-cols-header
---

## 安全分析（二）

::left::

### Theorem 3: 关键词隐私

**Known Ciphertext Model：**
- 索引和查询保密 → 关键词隐私
- CS只能做内积运算，无法推断关键词

**Known Background Model：**
- 引入虚拟关键词：文件向量增加 $U$ 维
- 查询向量中随机选 $V$ 个虚拟维度
- 设置 $U = 2\varrho, V = \varrho$
- 调节 $\sigma$ 平衡安全性和准确率

::right::

### Theorem 4: 前向安全性

ML-RKS+在动态设置下实现前向安全

**证明思路：**
- 旧token使用 $\mathbf{P}^{\delta_{ver}}$
- 新索引使用 $\mathbf{P}_{ver'}$
- **版本不匹配 → 搜索结果错误**
- CS无法识别不同版本的置换矩阵

<!--
继续看后两个定理。

Theorem 3是关于关键词隐私。在已知密文模型下，由于索引和查询都是保密的，云服务器只能做内积运算，无法推断出具体的关键词。在更强的已知背景模型下，通过引入虚拟关键词，可以有效抵抗统计分析攻击。

Theorem 4是关于前向安全性。ML-RKS+通过置换矩阵机制实现了前向安全。旧的查询token使用旧版本的置换矩阵，而新添加的文件使用新版本的置换矩阵。版本不匹配会导致搜索结果错误，从而防止历史查询token搜索新添加的文件。
-->

---
layout: two-cols-header
---

## 实验设置与对比方案

::left::

### 数据集与参数

**数据集：** 20Newsgroups（~20,000文档，20类别）

**参数设置：**
- 关键词数 $m \in [1, 1000]$，文件数 $n \in [1, 10000]$
- 查询词数 $t \in [1, 50]$，Top-k $k \in [1, 50]$
- 簇数量 $p = 5$，虚拟词 $U = V = 1$

**评估指标：**
- 时间：聚类、索引、查询、搜索、更新
- 准确率：$P_k = k'/k$
- 排名隐私：$\widetilde{P}_k = \sum |r_i - r_i'| / k$

::right::

### 对比方案

| 方案 | 聚类 | 前向安全 | 搜索复杂度 |
|------|------|----------|-----------|
| RKS | ✗ | ✗ | $O(mz\log n)$ |
| ML-RKS | ✓ | ✗ | $O(mz\log L_y)$ |
| RKS+ | ✗ | ✓ | $O(mz\log n)$ |
| ML-RKS+ | ✓ | ✓ | $O(mz\log L_y)$ |

**核心对比：**
- **RKS：** 基准方案，全局二叉树
- **ML-RKS：** 本文方案，聚类加速
- **RKS+/ML-RKS+：** 加入置换矩阵，支持动态更新

<!--
实验评估部分。数据集使用20Newsgroups，包含约2万个文档。参数设置涵盖了不同规模的关键词、文件和查询场景。评估指标包括各阶段的时间开销、搜索准确率和排名隐私。

对比方案有四个。RKS是基准方案，ML-RKS是本文的聚类优化方案，RKS+和ML-RKS+是加入前向安全机制的版本。从表格可以看到，ML-RKS通过聚类将搜索复杂度从O(log n)降到O(log Ly)，ML-RKS+在此基础上实现了前向安全。
-->

---
layout: two-cols-header
---

## 实验结果：搜索效率（一）

::left::

### 文件聚类时间

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/76b441327ed780f996c09d0d928ede87d1f9cd783a11748f93db88226dbed15a.jpg" alt="聚类时间" class="w-full">

**特点：**
- 预处理阶段，一次性开销
- 时间随 $n, m, p$ 增长
- 为后续搜索和更新带来显著加速

::right::

### 索引生成时间

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/6b43812655f558776e0af5d5008a255392a56e6c1e08978dd37c1139723be30e.jpg" alt="索引生成" class="w-5/7">

**性能对比：**
- **ML-RKS/ML-RKS+** 明显优于 RKS/RKS+
- 聚类减少了每个树的构建规模
- ML-RKS+略高于ML-RKS（置换矩阵开销）

<!--
实验结果第一部分：聚类和索引生成时间。

左侧是文件聚类时间。这是预处理阶段的一次性开销，在数据上传前完成。图中显示，聚类时间随着文件数n、关键词数m和簇数p的增长而增长。虽然聚类增加了初始开销，但为后续的搜索和更新带来了显著加速。

右侧是索引生成时间。从图中可以看出，ML-RKS和ML-RKS+明显少于RKS和RKS+。这是因为聚类后每个簇的文件数减少，构建树的规模更小。ML-RKS+略高于ML-RKS是因为需要额外生成置换矩阵。
-->

---
layout: two-cols-header
---

## 实验结果：搜索效率（二）

::left::

### 查询token生成时间

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/6ebc17e9509e944558f390624afd6130b6a191451dc2e7d8ffeebc2d95b4a131.jpg" alt="查询生成" class="w-5/7">

**性能对比：**
- ML-RKS ≈ RKS，ML-RKS+ ≈ RKS+
- 聚类不影响查询生成
- 置换矩阵略增开销

::right::

### 密文搜索与更新时间

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/ff5d83e8c92f14357e7fddfafbf5c885188a274a832f6c362099dc07466d8c84.jpg" alt="搜索和更新" class="w-5/7">

**核心优势：**
- **搜索：** ML-RKS/ML-RKS+ 显著快于 RKS/RKS+
- **更新：** ML-RKS+ 优于 RKS+（只更新选中簇）
- 所有方案搜索时间均 < 100ms

<!--
实验结果第二部分：查询生成和搜索更新时间。

左侧是查询token生成时间。ML-RKS与RKS相当，ML-RKS+与RKS+也相当。这说明聚类不影响查询生成性能，因为查询向量的维度和加密方式相同。ML-RKS+和RKS+略高是因为需要计算置换矩阵的幂。

右侧最重要，展示了密文搜索和文件更新时间。搜索时间方面，ML-RKS和ML-RKS+显著快于RKS和RKS+，这是核心优势。由于聚类，搜索只需在选中簇中进行，搜索空间大大减小。四个方案的搜索时间都小于100毫秒，适合实际应用。更新时间方面，ML-RKS+明显优于RKS+，因为ML-RKS+只需更新选中簇的树。
-->



---
layout: default
---

<!--TODO 这里要重新布局，因为文字展示不全-->

## 实验结果：搜索准确率

<div class="grid grid-cols-2 gap-8 items-start">

<div>

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/37a1b300aa569043756e754f8e480d41bbca50c1a4614598f3ee312f6358add1.jpg" alt="搜索准确率" class="w-full">

</div>

<div>

### 方案对比

**ML-RKS/ML-RKS+ (1)：**
- 只从选中簇返回Top-k
- 准确率略低于RKS/RKS+
- 效率最高

**ML-RKS/ML-RKS+ (5)：**
- 从所有簇检查并返回Top-k
- 准确率与RKS/RKS+相当
- 检查机制有效

### 参数影响

虚拟值方差 $\sigma$ 对准确率的影响：
- $\sigma$ ↓ → 扰动 ↓ → 准确率 ↑
- 但 $\sigma$ 太小会降低隐私保护

</div>

</div>

<!--
搜索准确率实验结果。横轴是Top-k的k值，纵轴是准确率Pk。

图中有三组曲线。RKS/RKS+是基准方案，准确率最高。ML-RKS/ML-RKS+ (1)只从选中簇返回Top-k，准确率略低于基准，因为可能遗漏其他簇的高分结果，但效率最高。ML-RKS/ML-RKS+ (5)从所有簇检查并返回全局Top-k，准确率与RKS/RKS+相当，说明检查机制有效。

虚拟值方差σ影响准确率。σ越小，虚拟值扰动越小，准确率越高。但σ太小会降低隐私保护。
-->

---
layout: default
---

<!--TODO 这里要重新布局，因为文字展示不全-->
## 实验结果：排名隐私

<div class="grid grid-cols-2 gap-8 items-start">

<div>

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/527688e7177b24b6a0e8bf25cda442a923493cd82b7796294e5756381690a238.jpg" alt="排名隐私" class="w-full">

</div>

<div>

### 隐私对比

**ML-RKS/ML-RKS+ (1)：**
- 排名扰动最大
- 隐私保护最强
- 只返回选中簇结果

**ML-RKS/ML-RKS+ (5)：**
- 排名扰动与RKS/RKS+相近
- 返回全局Top-k

### 参数权衡

虚拟值方差 $\sigma$ 的作用：
- $\sigma$ ↑ → 扰动 ↑ → 隐私 ↑
- 但 $\sigma$ 太大会降低准确率

**结论：** $\sigma$ 是准确率与隐私的平衡参数，用户可根据需求灵活调节

</div>

</div>

<!--
排名隐私实验结果。横轴是k值，纵轴是排名扰动P̃k。扰动越大，说明返回结果排名与真实排名差异越大，隐私保护越好。

ML-RKS/ML-RKS+ (1)的排名扰动最大，隐私保护最强，因为只从选中簇返回结果，排名随机性较大。ML-RKS/ML-RKS+ (5)的排名扰动与RKS/RKS+相近，因为都返回全局Top-k。

虚拟值方差σ也影响排名隐私。σ越大，虚拟值扰动越大，排名随机性越强，隐私保护越好。但σ太大会降低搜索准确率。

σ是准确率与隐私的平衡参数。用户可以根据实际需求灵活调节：准确率优先选小σ，隐私优先选大σ。
-->

---
layout: default
---

## 方案对比

<style>
.comparison-table {
  font-size: 1rem;
}
.comparison-table th {
  background-color: #DBEAFE;
  padding: 0.5rem;
}
.comparison-table td {
  padding: 0.25rem 0.5rem;
}
.highlight-row {
  background-color: #D1FAE5;
  font-weight: 600;
}
</style>

<div class="comparison-table">

| 方案 | 搜索类型 | 索引结构 | 搜索复杂度 | 支持场景 | 前向安全 |
|------|----------|----------|------------|----------|----------|
| [4] Wang 2011 | 单关键词 | 倒排索引 | $O(n)$ | 静态 | ✗ |
| [5] Cao 2013 | 多关键词 | — | $O(nm)$ | 静态 | ✗ |
| [14] Wang 2014 | 模糊搜索 | Bloom filter | $O(nm)$ | 静态 | ✗ |
| [8] Fu 2014 | 同义词搜索 | 二叉树 | $O(mz\log n)$ | 静态 | ✗ |
| [18] Guo 2017 | 短语搜索 | 倒排索引 | $O(nm)$ | 动态 | ✗ |
| [9] Xia 2015 | 多关键词 | 二叉树 | $O(mz\log n)$ | 动态 | ✗ |
| [23] Li 2014 | 多关键词 | 倒排索引 | $O(nm)$ | 静态 | ✗ |
| [30] Najafi 2019 | 多关键词 | — | $O(nm)$ | 动态 | ✓ |
| **ML-RKS** | 多关键词 | 二叉树 | $O(mz\log L_y)$ | 静态 | ✗ |
| **ML-RKS+** | 多关键词 | 二叉树 | $O(mz\log L_y)$ | 动态 | **✓** |

</div>

> **符号说明：** $n$ = 文件数，$m$ = 关键词数，$z$ = 包含查询关键词的叶节点数（$z \leq n$），$L_y$ = 簇 $y$ 的文件数（$L_y \ll n$）

<!--
现在我们通过一个对比表来全面比较本文方案与现有方案。

这个表列出了9个代表性的方案，包括本文提出的ML-RKS和ML-RKS+。我们从五个维度进行对比：搜索类型、索引结构、搜索复杂度、支持的场景（静态或动态），以及是否支持前向安全。

首先看搜索类型。早期的方案如Wang 2011只支持单关键词搜索，功能比较有限。后来的方案大多支持多关键词搜索，还有些支持模糊搜索、同义词搜索或短语搜索。本文的ML-RKS和ML-RKS+支持多关键词排序搜索，这是最常用的功能。

索引结构主要有两类。一类是倒排索引，比如Cao 2013、Guo 2017。另一类是二叉树索引，比如Fu 2014、Xia 2015。本文也使用二叉树索引，但结合了k-means聚类。

搜索复杂度是关键指标。倒排索引方案的复杂度通常是O(nm)，与文件数和关键词数都线性相关。二叉树方案改进到O(mz log n)，是次线性的，但当z接近n时仍然很高。Najafi 2019虽然支持前向安全，但复杂度仍是O(nm)。

本文的ML-RKS和ML-RKS+通过k-means聚类，将复杂度降低到O(mz log Ly)。关键是Ly远小于n，因为Ly是单个簇的文件数，而n是总文件数。这带来了显著的效率提升。

支持场景方面，早期的方案大多是静态的，不支持动态更新。后来的方案开始支持动态更新，但前向安全性往往缺失。Najafi 2019是第一个同时支持动态更新和前向安全的方案，但效率较低。本文的ML-RKS+也支持动态更新和前向安全，且效率更高。

最后一列是前向安全。大部分方案都不支持，只有Najafi 2019和本文的ML-RKS+支持。前向安全是动态场景下的重要安全需求，能够防止文件注入攻击。

底部是符号说明。z是包含查询关键词的叶节点数，它小于等于n。Ly是簇y的文件数量，由于聚类，Ly远小于n，这是我们方案效率提升的关键。

综合来看，ML-RKS+在功能、效率和安全性三个维度都达到了很好的平衡，是目前最先进的方案之一。
-->

---
layout: two-cols-header
---

## 总结与未来工作

::left::

### 主要成果

**ML-RKS：** k-means聚类 + 平衡二叉树
- 搜索复杂度：$O(mz\log L_y)$，$L_y \ll n$
- 保证索引、查询、关键词隐私

**ML-RKS+：** 置换矩阵实现前向安全
- 动态更新：$O(\log L_y)$
- 防止文件注入攻击

**实验结果：**
- 搜索效率显著优于RKS/RKS+
- 准确率与基准方案相当

::right::

### 局限性与未来方向

**当前局限：**
- 访问模式泄露（需ORAM保护）
- 搜索模式泄露（统计分析风险）
- 静态簇划分（需定期重聚类）

**未来工作：**
- **隐私增强：** 结合ORAM，完全不可区分token
- **自适应簇：** 动态调整簇划分，自动重聚类
- **多用户：** 支持多数据拥有者，细粒度访问控制

<!--
总结部分。ML-RKS通过k-means聚类和平衡二叉树，将搜索复杂度降低到O(mz log Ly)，带来显著效率提升。ML-RKS+通过置换矩阵实现前向安全和高效动态更新。实验验证了搜索效率优于基准方案，准确率相当。

当前局限包括访问模式泄露、搜索模式泄露和静态簇划分。未来可以从三个方向改进：隐私增强（结合ORAM），自适应簇管理（动态调整），多用户支持（细粒度访问控制）。
-->

---
layout: end
---

# 谢谢！

## 欢迎提问与讨论

<br>

### 核心要点回顾

<div class="grid grid-cols-3 gap-6 mt-8 text-sm">
  <div class="text-center">
    <div class="text-4xl mb-2">🔍</div>
    <p class="font-semibold">k-means + 二叉树</p>
    <p class="text-xs text-gray-600">搜索复杂度 $O(mz\log L_y)$</p>
  </div>
  <div class="text-center">
    <div class="text-4xl mb-2">🔐</div>
    <p class="font-semibold">置换矩阵机制</p>
    <p class="text-xs text-gray-600">实现前向安全</p>
  </div>
  <div class="text-center">
    <div class="text-4xl mb-2">⚡</div>
    <p class="font-semibold">高效动态更新</p>
    <p class="text-xs text-gray-600">只需更新选中簇</p>
  </div>
</div>

<div class="mt-8 text-center text-sm text-gray-500">
  <p>Yinbin Miao, Wei Zheng, Xiaohua Jia, et al.</p>
  <p>IEEE Transactions on Services Computing, 2022</p>
</div>

<!--
我的分享就到这里，感谢大家的聆听！欢迎大家提问和讨论。

下面是这篇论文的核心要点回顾。第一是k-means聚类结合平衡二叉树，将搜索复杂度降低到O(mz log Ly)，显著提升了搜索效率。第二是置换矩阵机制，通过版本控制实现了前向安全性，防止文件注入攻击。第三是高效的动态更新，由于使用了聚类，每次更新只需要修改选中的簇，而不需要修改全部索引，大大降低了更新开销。

这篇论文为加密数据上的排序关键词搜索提供了一个高效、安全、实用的解决方案，在学术和工业界都有重要的应用价值。欢迎大家提问！
-->
