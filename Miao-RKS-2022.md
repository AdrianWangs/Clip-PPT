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

<!--TODO 这一节只需要相似度分数，说明一下这个系统架构中相似度分数是怎么定义的就行了，另外两个部分之前报告都讲过可以-->

## 相似度计算与Top-k搜索

<div class="mt-8">

### 相似度分数

文件 $f_i$ 与查询 $q$ 的相似度：

$$
\mathcal{S}(\mathbf{d}_i, \mathbf{q}) = \mathbf{d}_i \cdot \mathbf{q} = \sum_{w_j \in q} v_{i,j} \cdot \omega_j = \sum_{w_j \in q} TF_{i,j} \cdot IDF_j \cdot \omega_j
$$

**内积计算：** 分数越高，文件与查询越相关

</div>

<div class="mt-8 grid grid-cols-2 gap-8">
<div>

### Top-k搜索目标

找出相似度分数最高的k个文件：

1. 计算所有文件的相似度分数 $\mathcal{S}(\mathbf{d}_i, \mathbf{q})$
2. 按分数降序排列
3. 返回前k个文件

**挑战：** 在加密数据上高效计算相似度

</div>
<div>

### Secure k-NN技术

使用安全k近邻计算保持内积：

- 加密文件向量 $\widehat{\mathbf{d}}_i$
- 加密查询向量 $\widehat{\mathbf{q}}$
- **关键性质：**
  $$\widehat{\mathbf{d}}_i \cdot \widehat{\mathbf{q}} = \mathbf{d}_i \cdot \mathbf{q}$$

在密文上计算内积 = 在明文上计算内积

</div>
</div>

<!--
有了向量表示，我们就可以计算相似度了。

文件和查询的相似度通过内积来计算，也就是d_i点乘q。展开后就是对所有查询关键词，累加它们的TF-IDF值乘以权重。这个内积值越高，说明文件与查询越相关。

Top-k搜索的目标是找出相似度分数最高的k个文件。理论上，我们需要计算所有文件的相似度分数，然后按降序排列，返回前k个。但在加密数据上，这个过程很困难，因为云服务器看不到明文数据，如何计算相似度呢？

这就需要用到Secure k-NN技术，也就是安全k近邻计算。这个技术的核心思想是，通过特殊的加密方式，让加密向量的内积等于明文向量的内积。具体来说，我们把文件向量d_i加密成d̂_i，把查询向量q加密成q̂。关键性质是，d̂_i点乘q̂等于d_i点乘q。这样，云服务器就可以在密文上计算内积，得到的结果和在明文上计算是一样的。

虽然这个加密机制会使密文空间翻倍，安全性也不是最强的，但在效率和功能性上有很好的平衡，是目前多关键词排序搜索中常用的技术。
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

<div class="flex justify-center items-center mt-8">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/f82c7f1d63131f0742d8ef6f2319562d43404ab1ed9b00f9d4a4e6908b490e76.jpg" alt="二叉树搜索示例" class="w-9/12">
</div>

<div class="mt-6 text-sm">

**场景：** 关键词集合 $\{w_1, w_2, w_3\}$，查询向量 $\mathbf{q} = (0.1, 0.5, 0.2)$，搜索Top-2

**步骤：**
1. 根节点 $\mathbf{n}_{ro} = (0.6, 0.7, 0.7)$，计算左右子节点分数：$\mathcal{S}(\mathbf{n}_{1,0}, \mathbf{q}) > \mathcal{S}(\mathbf{n}_{1,1}, \mathbf{q})$，选择左子树
2. 继续向下：$\mathcal{S}(\mathbf{n}_{2,0}, \mathbf{q}) > \mathcal{S}(\mathbf{n}_{2,1}, \mathbf{q})$，选择左子树
3. 计算叶节点：$\mathcal{S}(\mathbf{d}_1, \mathbf{q}) = 0.46$，$\mathcal{S}(\mathbf{d}_2, \mathbf{q}) = 0.39$
4. **剪枝：** $\mathcal{S}(\mathbf{n}_{2,1}, \mathbf{q}) = 0.22 < 0.39$，跳过 $\mathbf{d}_3, \mathbf{d}_4$
5. 检查右侧：$\mathcal{S}(\mathbf{n}_{1,1}, \mathbf{q}) = 0.40 > 0.39$，需要计算 $\mathbf{d}_5, \mathbf{d}_6$
6. 最终结果：$\mathbf{d}_1$ (0.46)、$\mathbf{d}_6$ (0.40)

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
layout: default
---

<!--TODO 这部分最好拆成两页，因为目前看起来页面只能显示密钥生成和索引生成两个部分-->
## ML-RKS方案构建

<div class="grid grid-cols-2 gap-6 mt-6">

<div class="border-2 border-blue-200 rounded p-4">

### 1. 密钥生成 (KeyGen)

**输入：** 安全参数 $\kappa$

**输出：**
- $\mathbf{S} \in \{0,1\}^{\widetilde{m}}$
- $\mathbf{M}_1, \mathbf{M}_2 \in \mathbb{R}^{\widetilde{m} \times \widetilde{m}}$
- $k_e$：对称加密密钥（AES/DES）

**扩展：** $\widetilde{m} = m + U + 2$
- $m$：关键词数量
- $U$：虚拟关键词数量
- $+2$：token不可区分性 + 前向安全

</div>

<div class="border-2 border-green-200 rounded p-4">

### 2. 索引生成 (BuildIndex)

**文件向量构建：**
$$\mathbf{d}_i = \{v_{i,1}, \ldots, v_{i,m}, \varepsilon_{i,m+1}, \ldots, \varepsilon_{i,m+U}, 1, 1\}$$
- 前 $m$ 维：TF-IDF值
- 中间 $U$ 维：随机虚拟值 $\sim N(\mu, \sigma^2)$
- 最后2维：固定为1

**k-means聚类：** 分成 $p$ 个簇

**树构建：** 每个簇构建平衡二叉树

**加密：** 所有节点向量用Secure k-NN加密

</div>

<div class="border-2 border-yellow-200 rounded p-4">

### 3. 查询生成 (Trapdoor)

**查询向量构建：**
$$\mathbf{q} = (\alpha\omega_1, \ldots, \alpha\omega_m, \alpha, 0, \ldots, \alpha, \beta, 1)$$
- 前 $m$ 维：$\alpha \omega_j$（关键词权重乘随机数）
- 中间 $U$ 维：随机选 $V$ 个设为 $\alpha$，其余为0
- 倒数第2维：随机数 $\beta$
- 最后1维：固定为1

**加密：** $\widehat{\mathbf{q}} = (\mathbf{M}_1^{-1}\mathbf{q}_1, \mathbf{M}_2^{-1}\mathbf{q}_2)$

</div>

<div class="border-2 border-red-200 rounded p-4">

### 4. 密文搜索 (Search)

**步骤：**

1. 计算每个簇中心与查询的分数 $\mathcal{S}(\widehat{\mathbf{c}}_y, \widehat{\mathbf{q}})$
2. 选择分数最高的簇
3. 在该簇的二叉树中搜索Top-k
4. **检查：**
   - Case 1: 若第k个结果分数 ≥ 其他簇，直接返回
   - Case 2: 若有其他簇分数更高，继续搜索该簇并更新Top-k

**最终分数：**
$$\mathcal{S}(\widehat{\mathbf{d}}_i, \widehat{\mathbf{q}}) = \alpha\left(\sum_{j=1}^m v_{i,j}\omega_j + \sum_{j=m+1}^{m+U} \varepsilon_{i,j}\right) + \beta + 1$$

</div>

</div>

<!--
现在我们把ML-RKS方案的四个阶段整合在一起看。

左上角是密钥生成阶段。DO输入一个安全参数κ，生成密钥。密钥包含分裂向量S、两个可逆矩阵M1和M2，以及对称加密密钥ke。这里有个重要的扩展，向量维度从m扩展到m+U+2。m是原始关键词数量，U是虚拟关键词数量，加2是为了实现token不可区分性和前向安全。

右上角是索引生成阶段。首先构建文件向量，前m维是TF-IDF值，中间U维是随机的虚拟值，服从正态分布，最后2维固定为1。然后用k-means算法把所有文件向量聚类成p个簇，比如5个簇。接下来，为每个簇构建一个平衡二叉树。最后，用Secure k-NN算法加密所有节点向量，包括根节点、中间节点和叶节点，得到加密索引。

左下角是查询生成阶段。用户首先构建查询向量，前m维是关键词权重乘以一个随机数α，这个α是为了隐藏真实的权重值。中间U维中，随机选V个设为α，其余为0。倒数第二维是另一个随机数β，最后一维固定为1。然后用密钥对查询向量进行分裂和加密，得到加密的查询token。

右下角是密文搜索阶段。CS首先计算查询向量与每个簇中心的相似度分数，选择分数最高的簇。然后在该簇的二叉树中搜索Top-k结果。这里有两种情况需要处理。Case 1，如果第k个结果的分数已经大于等于其他所有簇的分数，那么可以直接返回这Top-k结果。Case 2，如果有其他簇的分数更高，说明那个簇中可能有更相关的文件，需要继续搜索该簇并更新Top-k结果。

最终的相似度分数公式在底部。它包含三部分：第一部分是TF-IDF值与权重的乘积之和，乘以α；第二部分是虚拟关键词的贡献，也乘以α；第三部分是β+1。由于α和虚拟值是随机的，CS无法从分数中推断出真实的TF-IDF值和权重，从而保护了隐私。
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

<!--TODO 这部分想办法分成两页，不然下面根本看不到-->
## 动态更新操作

<div class="flex justify-center items-center mt-4">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/a36c1fb24cd44737174aa7a79c2efd5fc45555bcfe70cbe97a400bb2d4abee53.jpg" alt="文件更新示例" class="w-9/27">
</div>

<div class="mt-2 grid grid-cols-3 gap-4 text-sm">

<div class="border-2 border-blue-200 rounded p-3">


**修改场景：** 将 $\mathbf{d}_1$ 修改为 $\mathbf{d}_1'$
1. 更新受影响节点：$\mathbf{n}_1, \mathbf{c}_1$
2. 版本号更新：$ver' = ver + 1 = 1$
3. 生成 $\widehat{\mathbf{P}}_1$
4. 乘以所有节点向量
5. 上传更新后的索引

**复杂度：** $O(\log L_y)$ 个节点

</div>

<div class="border-2 border-green-200 rounded p-3">


**删除场景：** 删除 $\mathbf{d}_2$

1. 设置 $\mathbf{d}_2 = \{0, \ldots, 0\}$
2. 更新受影响节点：$\mathbf{n}_1, \mathbf{c}_1$
3. 版本号更新：$ver' = 1 + 1 = 2$
4. 生成 $\widehat{\mathbf{P}}_2$
5. 乘以所有节点向量
6. 上传更新后的索引

**复杂度：** $O(\log L_y)$ 个节点

</div>

<div class="border-2 border-red-200 rounded p-3">


**添加场景：** 添加 $\mathbf{d}_5$

1. 将 $\mathbf{d}_4, \mathbf{d}_5$ 放到下一层
2. 更新受影响节点：$\mathbf{c}_1, \mathbf{n}_2, \mathbf{n}_3$
3. 版本号更新：$ver' = 2 + 1 = 3$
4. 生成 $\widehat{\mathbf{P}}_3$
5. 乘以所有节点向量
6. 上传更新后的索引

**复杂度：** $O(\log L_y)$ 个节点

</div>

</div>

<div class="mt-4 p-3 bg-yellow-50 rounded text-sm">
  <p class="font-semibold">关键优势：</p>
  <p class="text-xs mt-1">• 只需更新选中簇的树，而非全部簇（$L_y \ll n$）</p>
  <p class="text-xs">• 置换矩阵更新强制历史token失效</p>
  <p class="text-xs">• 理论更新复杂度：修改/删除 $O(\log L_y + 1)$，添加 $O(\log L_y + 2)$</p>
</div>

<!--
现在我们来看ML-RKS+如何处理动态更新操作。上面这张图展示了一个簇c1的二叉树，包含4个文件d1到d4。我们来看三种更新操作。

第一种是文件修改。假设我们要把d1修改成d1'。首先，需要更新受影响的节点，也就是d1到根节点路径上的所有节点，包括n1和c1。然后，版本号从0更新为1。基于新的版本号，生成新的置换矩阵P̂_1。接下来，用P̂_1乘以簇c1中所有节点的向量，更新整个加密索引。最后，上传更新后的索引到云端。

修改操作只影响从叶节点到根节点的路径，路径长度是树的高度O(log Ly)，所以复杂度是O(log Ly)。

第二种是文件删除。假设我们要删除d2。删除的处理方式是把d2的向量设置为全0向量。这样，它在搜索时的分数会是0，不会被返回。然后，同样更新受影响的节点n1和c1，版本号递增到2，生成新的置换矩阵P̂_2，更新所有节点向量，上传到云端。

删除操作的复杂度也是O(log Ly)，因为只需要更新一条路径。

第三种是文件添加。假设我们要添加d5。由于原来的叶节点层已经满了，需要在下一层创建新的叶节点。具体来说，把原来的叶节点d4移到下一层，并在它旁边放置新的d5。然后，创建新的父节点n3。接下来，更新受影响的节点，包括c1、n2和新创建的n3。版本号递增到3，生成P̂_3，更新所有节点向量，上传到云端。

添加操作需要创建新节点，所以复杂度略高一点，是O(log Ly + 2)，但仍然是对数级别。

底部总结了ML-RKS+的关键优势。第一，由于使用了k-means聚类，每次更新只需要修改选中簇的树，而不需要修改全部簇。簇的大小Ly远小于总文件数n，所以更新开销小。第二，每次更新后，置换矩阵会变化，强制历史的查询token失效，无法搜索新数据，实现了前向安全。第三，理论更新复杂度是对数级别，远优于线性复杂度的方案。
-->

---
layout: two-cols-header
---

<!--TODO 拆成两页最好，不然内容太多了-->

## 安全分析

::left::

### Theorem 1: 索引与查询保密性

ML-RKS和ML-RKS+在两种威胁模型下都能保证索引和查询的保密性（前提：CS不获得密钥）

**证明思路：**
- 加密索引：$2nm$ 个方程，$2nm + 2m^2$ 个未知数
- 加密查询：$2m$ 个方程，$2m^2$ 个未知数
- 未知数数量 $>$ 方程数量 $\Rightarrow$ 无法求解

### Theorem 2: Token不可区分性

同一查询的多次token不可区分

**证明思路：**
- 查询向量分裂时引入随机性
- 两次查询 $\mathbf{q}', \mathbf{q}''$ 相同的概率 $\approx \gamma^\epsilon$
- $\gamma \ll \frac{1}{2}$，$\epsilon$ 是分裂向量中0的数量
- 概率接近0 $\Rightarrow$ 不可区分

::right::

### Theorem 3: 关键词隐私

ML-RKS和ML-RKS+保护关键词隐私

**Known Ciphertext Model：**
- 索引和查询保密 $\Rightarrow$ 关键词隐私
- CS只能做内积运算，无法推断关键词

**Known Background Model：**
- 引入虚拟关键词：文件向量增加 $U$ 维
- 查询向量中随机选 $V$ 个虚拟维度
- 设置 $U = 2\varrho, V = \varrho$（$\varrho$ 为安全参数）
- 通过调节 $\sigma$（虚拟值方差）平衡安全性

### Theorem 4: 前向安全性

ML-RKS+在动态设置下实现前向安全

**证明思路：**
- 旧token使用旧版本的置换矩阵
- 新索引使用新版本的置换矩阵
- 版本不匹配 $\Rightarrow$ 搜索结果错误
- CS无法通过统计分析识别置换矩阵

<!--
现在我们来看安全分析。本文证明了四个主要定理。

Theorem 1是关于索引和查询的保密性。它声称，只要CS没有获得密钥，ML-RKS和ML-RKS+在两种威胁模型下都能保护索引和查询的隐私。证明的思路是从线性代数的角度。对于加密索引，有2nm个方程，但有2nm+2m²个未知数，因为分裂向量S和矩阵M1、M2都是未知的。对于加密查询，有2m个方程，但有2m²个未知数。在这两种情况下，未知数的数量都大于方程数，所以CS无法通过求解线性方程组来推断出明文信息。这保证了保密性。

Theorem 2是关于token的不可区分性。它声称，同一个查询的多次提交生成的token是不可区分的。证明的思路是，查询向量在分裂时引入了随机性。如果S的某一位是0，那么q1和q2在该位是随机分裂的。两次查询q'和q''得到相同分裂的概率大约是γ的ε次方，其中ε是S中0的数量，γ远小于1/2。当ε足够大时，这个概率接近0，所以CS无法区分两次查询是否来自同一个原始查询。

Theorem 3是关于关键词隐私。在已知密文模型下，由于索引和查询都是保密的，CS只能做内积运算，无法推断出具体的关键词。在更强的已知背景模型下，本文引入了虚拟关键词。文件向量增加U维虚拟值，查询向量中随机选V个虚拟维度。通过设置U=2ϱ、V=ϱ，其中ϱ是安全参数，可以有效抵抗统计分析攻击。虚拟值的方差σ是一个可调参数，可以在安全性和搜索准确率之间取得平衡。

Theorem 4是关于前向安全性。它声称ML-RKS+在动态设置下实现了前向安全。证明的思路是，旧的查询token使用旧版本的置换矩阵，而新添加的文件使用新版本的置换矩阵。版本不匹配会导致搜索结果错误，CS无法用旧token正确搜索新文件。而且，由于置换矩阵是独立的，CS无法通过统计分析来识别不同版本的置换矩阵是否相同，从而无法绕过前向安全保护。
-->

---
layout: default
---

<!--TODO 实验环境不需要，对比方案列成表格，尽量减少多余的表述-->
## 实验设置与对比方案

<div class="grid grid-cols-2 gap-8 mt-8">

<div>

### 数据集与参数

**数据集：** 20Newsgroups
- 约20,000个新闻组文档
- 均匀分布在20个类别

**实验参数：**
- 关键词数量 $m \in [1, 1000]$
- 文件数量 $n \in [1, 10000]$
- 查询关键词数 $t \in [1, 50]$
- Top-k结果数 $k \in [1, 50]$
- 簇数量 $p = 5$
- 虚拟关键词 $U = V = 1$

**实验环境：**
- Windows 10, Intel i7-8565 CPU, 8GB RAM
- Java实现

</div>

<div>

### 对比方案

**RKS（Ranked Keyword Search）：**
- 不使用k-means聚类
- 直接在全部文件上构建单棵二叉树
- 搜索复杂度：$O(mz\log n)$

**ML-RKS：**
- 使用k-means聚类
- 为每个簇构建独立二叉树
- 搜索复杂度：$O(mz\log L_y)$

**RKS+：**
- RKS + 置换矩阵
- 支持动态更新，实现前向安全

**ML-RKS+：**
- ML-RKS + 置换矩阵
- 支持动态更新，实现前向安全

</div>

</div>

<div class="mt-6 p-4 bg-blue-50 rounded">
  <p class="font-semibold text-sm">评估指标：</p>
  <div class="grid grid-cols-3 gap-4 mt-2 text-xs">
    <div>• 文件聚类时间</div>
    <div>• 索引生成时间</div>
    <div>• 查询token生成时间</div>
    <div>• 密文搜索时间</div>
    <div>• 文件更新时间</div>
    <div>• 搜索准确率 $P_k = k'/k$</div>
    <div>• 排名隐私 $\widetilde{P}_k = \sum |r_i - r_i'| / k$</div>
  </div>
</div>

<!--
现在我们来看实验评估。首先介绍实验设置。

数据集使用的是20Newsgroups，这是一个经典的文本数据集，包含大约2万个新闻组文档，均匀分布在20个不同的类别中。

实验参数设置如下。关键词数量m从1到1000变化，文件数量n从1到10000变化，查询中的关键词数t从1到50，Top-k结果数k也从1到50。簇的数量p设为5，虚拟关键词的数量U和V都设为1。实验环境是Windows 10系统，Intel i7 CPU，8GB内存，用Java实现。

对比方案有四个。第一个是RKS，它不使用k-means聚类，直接在全部文件上构建一棵二叉树，搜索复杂度是O(mz log n)。第二个是ML-RKS，这是本文提出的基础方案，使用k-means聚类，为每个簇构建独立的二叉树，搜索复杂度降低到O(mz log Ly)。第三个是RKS+，它在RKS的基础上加入了置换矩阵机制，支持动态更新和前向安全。第四个是ML-RKS+，这是本文的完整方案，结合了聚类和置换矩阵，既高效又安全。

底部列出了评估指标。我们会测量文件聚类时间、索引生成时间、查询token生成时间、密文搜索时间、文件更新时间。此外，还会评估搜索准确率Pk，它等于返回的真实Top-k结果数k'除以k。还有排名隐私P̃k，它衡量返回结果的排名扰动程度，计算每个文件的真实排名和返回排名的差值之和除以k。

通过这些指标，我们可以全面评估方案的效率、准确性和隐私保护能力。
-->

---
layout: two-cols-header
---
<!--TODO 拆成两页最好，不然内容太多了-->
## 实验结果：搜索效率

::left::

### 文件聚类时间

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/76b441327ed780f996c09d0d928ede87d1f9cd783a11748f93db88226dbed15a.jpg" alt="聚类时间" class="w-full">

- 聚类是预处理阶段，一次性开销
- 时间随 $n, m, p$ 增长
- 为后续搜索和更新带来显著加速

### 索引生成时间

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/6b43812655f558776e0af5d5008a255392a56e6c1e08978dd37c1139723be30e.jpg" alt="索引生成" class="w-full">

- ML-RKS和ML-RKS+优于RKS和RKS+
- 聚类减少了每个树的构建规模

::right::

### 查询token生成时间

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/6ebc17e9509e944558f390624afd6130b6a191451dc2e7d8ffeebc2d95b4a131.jpg" alt="查询生成" class="w-full">

- ML-RKS与RKS相当，ML-RKS+与RKS+相当
- 聚类不影响查询生成性能
- 置换矩阵略增开销

### 密文搜索与更新时间

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/ff5d83e8c92f14357e7fddfafbf5c885188a274a832f6c362099dc07466d8c84.jpg" alt="搜索和更新" class="w-full">

- **搜索：** ML-RKS和ML-RKS+显著快于RKS和RKS+
- **更新：** ML-RKS+优于RKS+，只需更新选中簇

<!--
现在我们来看实验结果，首先是搜索效率。

左上角是文件聚类时间。聚类是预处理阶段的一次性开销，在数据上传前完成。图中显示，聚类时间随着文件数n、关键词数m和簇数p的增长而增长。虽然聚类会增加初始的计算开销，但它为后续的搜索和更新带来了显著的加速，是值得的投资。

左下角是索引生成时间。从图中可以看出，ML-RKS和ML-RKS+的索引生成时间明显少于RKS和RKS+。这是因为聚类后，每个簇的文件数量减少了，构建每棵树的规模更小，所以总的索引生成时间也更短。ML-RKS+略高于ML-RKS，是因为需要额外生成和应用置换矩阵。

右上角是查询token生成时间。图中显示，ML-RKS与RKS的时间相当，ML-RKS+与RKS+也相当。这说明聚类不会影响查询生成的性能，因为查询向量的维度和加密方式都是一样的。ML-RKS+和RKS+略高于基础版本，是因为需要额外计算置换矩阵的幂。

右下角最重要，展示了密文搜索时间和文件更新时间。从搜索时间来看，ML-RKS和ML-RKS+显著快于RKS和RKS+。这是核心优势。由于聚类，搜索只需在选中的簇中进行，搜索空间大大减小。而且四个方案的搜索时间都小于100毫秒，说明都适合实际应用。

从更新时间来看，ML-RKS+明显优于RKS+。这是因为ML-RKS+只需要更新选中簇的树，而RKS+需要更新整棵大树。文件修改和删除的更新时间相近，文件添加稍高，因为可能需要创建新节点。

总的来说，ML-RKS和ML-RKS+在保证功能的同时，显著提升了搜索和更新效率。
-->

---
layout: two-cols-header
---

<!--TODO 拆成两页最好，不然内容太多了-->
## 实验结果：准确率与隐私

::left::

### 搜索准确率

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/37a1b300aa569043756e754f8e480d41bbca50c1a4614598f3ee312f6358add1.jpg" alt="搜索准确率" class="w-11/12">

**ML-RKS/ML-RKS+ (1)：** 只从选中簇返回Top-k
- 准确率略低于RKS/RKS+

**ML-RKS/ML-RKS+ (5)：** 从所有簇检查并返回Top-k
- 准确率与RKS/RKS+相当
- 虚拟值方差 $\sigma$ 越小，准确率越高

::right::

### 排名隐私

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/527688e7177b24b6a0e8bf25cda442a923493cd82b7796294e5756381690a238.jpg" alt="排名隐私" class="w-11/12">

**ML-RKS/ML-RKS+ (1)：** 排名扰动更大
- 隐私保护更强

**ML-RKS/ML-RKS+ (5)：** 排名扰动与RKS/RKS+相近
- 虚拟值方差 $\sigma$ 越大，排名扰动越大，隐私越好

**权衡：** $\sigma$ 是准确率与隐私的平衡参数

<!--
现在我们来看搜索准确率和排名隐私的实验结果。

左边是搜索准确率。横轴是Top-k的k值，纵轴是准确率Pk。图中有三条曲线组。RKS/RKS+是基准方案，准确率最高。ML-RKS/ML-RKS+ (1)表示只从选中的簇中返回Top-k结果，不检查其他簇。可以看到，它的准确率略低于基准，因为可能遗漏了其他簇中的高分结果。ML-RKS/ML-RKS+ (5)表示从所有簇中检查并返回全局的Top-k结果，它的准确率与RKS/RKS+相当，说明我们的检查机制是有效的。

图中还对比了不同虚拟值方差σ的影响。σ越小，虚拟值对分数的扰动越小，准确率越高。但σ太小会降低隐私保护，所以需要权衡。

右边是排名隐私。横轴是k值，纵轴是排名扰动P̃k。扰动越大，说明返回结果的排名与真实排名差异越大，隐私保护越好。从图中可以看出，ML-RKS/ML-RKS+ (1)的排名扰动最大，隐私保护最强。这是因为只从选中簇返回结果，排名会有较大的随机性。ML-RKS/ML-RKS+ (5)的排名扰动与RKS/RKS+相近，因为都返回全局Top-k。

虚拟值方差σ也影响排名隐私。σ越大，虚拟值对分数的扰动越大，排名的随机性越强，隐私保护越好。但σ太大会降低搜索准确率。

所以，σ是一个平衡参数。用户可以根据实际需求，在准确率和隐私之间灵活调节。如果对准确率要求高，可以选择较小的σ；如果对隐私要求高，可以选择较大的σ。

总的来说，ML-RKS和ML-RKS+在保证高效搜索的同时，也能达到与基准方案相当的准确率，并提供可调节的隐私保护。
-->

---
layout: default
---

<!--TODO 改成markdown格式的表格，不然公式显示不出来，符号说明改成markdown格式的引用，注意字体大小-->

<div class="mt-0">

<table class="text-xs w-full">
<thead>
<tr class="bg-blue-100">
  <th class="border px-2 py-2">方案</th>
  <th class="border px-2 py-2">搜索类型</th>
  <th class="border px-2 py-2">索引结构</th>
  <th class="border px-2 py-2">搜索复杂度</th>
  <th class="border px-2 py-2">支持场景</th>
  <th class="border px-2 py-2">前向安全</th>
</tr>
</thead>
<tbody>
<tr>
  <td class="border px-2 py-1">[4] Wang 2011</td>
  <td class="border px-2 py-1">单关键词</td>
  <td class="border px-2 py-1">倒排索引</td>
  <td class="border px-2 py-1">$O(n)$</td>
  <td class="border px-2 py-1">静态</td>
  <td class="border px-2 py-1 text-center">✗</td>
</tr>
<tr class="bg-gray-50">
  <td class="border px-2 py-1">[5] Cao 2013</td>
  <td class="border px-2 py-1">多关键词</td>
  <td class="border px-2 py-1">—</td>
  <td class="border px-2 py-1">$O(nm)$</td>
  <td class="border px-2 py-1">静态</td>
  <td class="border px-2 py-1 text-center">✗</td>
</tr>
<tr>
  <td class="border px-2 py-1">[14] Wang 2014</td>
  <td class="border px-2 py-1">模糊搜索</td>
  <td class="border px-2 py-1">Bloom filter</td>
  <td class="border px-2 py-1">$O(nm)$</td>
  <td class="border px-2 py-1">静态</td>
  <td class="border px-2 py-1 text-center">✗</td>
</tr>
<tr class="bg-gray-50">
  <td class="border px-2 py-1">[8] Fu 2014</td>
  <td class="border px-2 py-1">同义词搜索</td>
  <td class="border px-2 py-1">二叉树</td>
  <td class="border px-2 py-1">$O(mz\log n)$</td>
  <td class="border px-2 py-1">静态</td>
  <td class="border px-2 py-1 text-center">✗</td>
</tr>
<tr>
  <td class="border px-2 py-1">[18] Guo 2017</td>
  <td class="border px-2 py-1">短语搜索</td>
  <td class="border px-2 py-1">倒排索引</td>
  <td class="border px-2 py-1">$O(nm)$</td>
  <td class="border px-2 py-1">动态</td>
  <td class="border px-2 py-1 text-center">✗</td>
</tr>
<tr class="bg-gray-50">
  <td class="border px-2 py-1">[9] Xia 2015</td>
  <td class="border px-2 py-1">多关键词</td>
  <td class="border px-2 py-1">二叉树</td>
  <td class="border px-2 py-1">$O(mz\log n)$</td>
  <td class="border px-2 py-1">动态</td>
  <td class="border px-2 py-1 text-center">✗</td>
</tr>
<tr>
  <td class="border px-2 py-1">[23] Li 2014</td>
  <td class="border px-2 py-1">多关键词</td>
  <td class="border px-2 py-1">倒排索引</td>
  <td class="border px-2 py-1">$O(nm)$</td>
  <td class="border px-2 py-1">静态</td>
  <td class="border px-2 py-1 text-center">✗</td>
</tr>
<tr class="bg-gray-50">
  <td class="border px-2 py-1">[30] Najafi 2019</td>
  <td class="border px-2 py-1">多关键词</td>
  <td class="border px-2 py-1">—</td>
  <td class="border px-2 py-1">$O(nm)$</td>
  <td class="border px-2 py-1">动态</td>
  <td class="border px-2 py-1 text-center">✓</td>
</tr>
<tr class="bg-green-100">
  <td class="border px-2 py-1 font-semibold">ML-RKS</td>
  <td class="border px-2 py-1">多关键词</td>
  <td class="border px-2 py-1">二叉树</td>
  <td class="border px-2 py-1 font-semibold">$O(mz\log L_y)$</td>
  <td class="border px-2 py-1">静态</td>
  <td class="border px-2 py-1 text-center">✗</td>
</tr>
<tr class="bg-green-200">
  <td class="border px-2 py-1 font-semibold">ML-RKS+</td>
  <td class="border px-2 py-1">多关键词</td>
  <td class="border px-2 py-1">二叉树</td>
  <td class="border px-2 py-1 font-semibold">$O(mz\log L_y)$</td>
  <td class="border px-2 py-1">动态</td>
  <td class="border px-2 py-1 text-center font-semibold">✓</td>
</tr>
</tbody>
</table>

<div class="mt-4 text-xs">
  <p><strong>符号说明：</strong> $n$ = 文件数量，$m$ = 关键词数量，$z$ = 包含查询关键词的叶节点数（$z \leq n$），$L_y$ = 簇 $y$ 的文件数量（$L_y \ll n$），$p$ = 簇数量</p>
</div>

</div>

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

<!--TODO 内容太多了，没必要说这么详细-->
## 总结与未来工作

::left::

### 主要成果

**ML-RKS：**
- k-means聚类 + 平衡二叉树
- 搜索复杂度：$O(mz\log L_y)$，$L_y \ll n$
- 保证索引、查询、关键词隐私
- 搜索时间 < 100ms

**ML-RKS+：**
- 置换矩阵机制实现前向安全
- 高效动态更新：$O(\log L_y)$
- 只需更新选中簇，开销小
- 防止文件注入攻击

**实验验证：**
- 20Newsgroups数据集
- 搜索效率显著优于RKS/RKS+
- 准确率与基准方案相当

::right::

### 局限性

- **访问模式泄露**
  - 返回的文件ID可能泄露信息
  - 需要ORAM等技术保护

- **搜索模式泄露**
  - Token不可区分性有限
  - 统计分析可能推断查询相关性

- **静态簇划分**
  - 大量更新后，簇的平衡性可能变差
  - 需要定期重新聚类

### 未来方向

- **更强的隐私保护**
  - 结合ORAM隐藏访问模式
  - 探索完全不可区分的token生成

- **自适应簇管理**
  - 动态调整簇的数量和划分
  - 根据更新模式自动重聚类

- **多用户场景**
  - 支持多数据拥有者
  - 细粒度的访问控制

<!--
最后，我们来总结一下本文的主要成果、局限性和未来工作方向。

先看主要成果。ML-RKS方案结合k-means聚类和平衡二叉树，将搜索复杂度从O(mz log n)降低到O(mz log Ly)，其中Ly远小于n，带来了显著的效率提升。方案保证了索引、查询和关键词的隐私，在20Newsgroups数据集上的搜索时间小于100毫秒，适合实际应用。

ML-RKS+通过引入置换矩阵机制，实现了前向安全性，能够防止文件注入攻击。动态更新的复杂度是O(log Ly)，而且只需要更新选中的簇，开销很小。实验验证了ML-RKS+的搜索效率显著优于不使用聚类的基准方案，准确率也与基准相当。

当然，本文的方案也有一些局限性。第一是访问模式泄露。虽然我们加密了索引和查询，但返回的文件ID是明文的，可能泄露哪些文件被访问了。要解决这个问题，需要引入ORAM等技术，但这会带来额外的开销。

第二是搜索模式泄露。虽然我们实现了token的不可区分性，但保护程度有限。通过统计分析，CS可能推断出查询之间的相关性，比如判断两次查询是否来自同一个用户。

第三是静态簇划分。我们的聚类是在初始阶段一次性完成的。如果后续有大量的文件更新，簇的平衡性可能会变差，影响搜索效率。这时需要定期重新聚类，带来额外的开销。

未来的研究可以从三个方向展开。第一是更强的隐私保护。可以结合ORAM技术来隐藏访问模式，或者探索完全不可区分的token生成方法，进一步提升隐私保护水平。

第二是自适应簇管理。设计动态调整簇数量和划分的算法，根据文件的更新模式自动进行重聚类，保持簇的平衡性和搜索效率。

第三是支持多用户场景。扩展方案以支持多个数据拥有者，实现细粒度的访问控制，允许不同用户有不同的访问权限。

这些方向都很有研究价值，可以进一步提升加密数据搜索的实用性和安全性。
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
