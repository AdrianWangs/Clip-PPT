---
theme: seriph
background: /image/slides/image.png
title: 'Verifiable Cross-Modal Searchable Encryption via Hierarchical Spherical Tree with Beam Search'
info: |
  ## 基于分层球形树与束搜索的可验证跨模态可搜索加密
  高效、安全、可验证的云端加密数据检索方案
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

# Verifiable Cross-Modal Searchable Encryption via Hierarchical Spherical Tree with Beam Search

## 基于分层球形树与束搜索的可验证跨模态可搜索加密

<div class="pt-12">
  <span class="px-2 py-1 font-semibold">汇报人: 王宇哲</span>
</div>

<div class="pt-6 text-sm">
  Yuzhe Wang (华东师范大学, 2025)
  <br>
  IEEE Transactions on Services Computing
</div>

<!--
大家好，今天我要分享的论文是《基于分层球形树与束搜索的可验证跨模态可搜索加密》，这是我在华东师范大学期间完成的一篇关于云端加密数据隐私保护跨模态检索的研究工作，将发表在IEEE Transactions on Services Computing上。
-->

---
layout: two-cols-header
---

# 研究背景与动机

::left::

### 跨模态检索的挑战

- 多媒体数据快速增长
- 跨模态检索成为刚需（以文搜图、以图搜文）
- CLIP实现零样本检索
- **隐私问题**：数据明文上传到云端

::right::

### 现有方案的局限

**LSH方法：**
- 需要64个哈希表，内存开销大
- 查询延迟高

**树索引方法：**
- 二叉树过深
- 贪婪搜索易陷入局部最优

**可验证性缺失：**
- 服务器可能偷懒
- 用户无法验证结果

<!--
在开始之前，我想先和大家聊聊这项研究的背景。

随着云计算的普及，越来越多的多媒体数据被存储在云端。这些数据包括图像、文本、音频、视频等多种模态。跨模态检索，比如"以文搜图"或"以图搜文"，已经成为一个非常重要的应用需求。2021年，OpenAI推出了CLIP模型，通过对比学习实现了零样本跨模态检索，准确率有了质的飞跃。但是，现有的方案都要求用户把数据明文上传到云端，这就带来了严重的隐私泄露风险。

那么，我们能不能在保护数据隐私的同时，实现高效准确的跨模态检索呢？这就是我们的研究动机。

目前主流的隐私保护检索方案可以分为两类。第一类是基于LSH的方法，比如Cross-Model-SE。它虽然能达到90%的召回率，但需要维护64个哈希表，内存开销巨大，而且查询时要探测多个表，延迟很高。第二类是基于树索引的方法。但现有的树方案都使用二叉树，树的深度太深，而且每个节点只能分两支，语义划分很粗糙。更重要的是，它们都使用贪婪搜索，很容易陷入局部最优。

此外，还有一个被忽视但非常重要的问题：可验证性。云服务器为了节省计算资源，可能会偷懒，执行不完整的搜索，但依然向用户收取全额费用。用户却无法验证返回的结果是否正确、是否完整。

因此，我们需要一个全新的方案来解决这些问题。
-->

---
layout: default
---

## 我们的方案：VCSE-HST

### 核心创新点

<div class="grid grid-cols-2 gap-4 mt-4">
  <div class="bg-gray-50 p-3 rounded">
    <h4 class="font-bold mb-2">分层k-叉球形树</h4>
    <ul class="text-sm space-y-1">
      <li>- 使用球形k-means递归聚类（k=10）</li>
      <li>- 树深度仅3-4层</li>
      <li>- 语义划分更细致</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-3 rounded">
    <h4 class="font-bold mb-2">束搜索算法</h4>
    <ul class="text-sm space-y-1">
      <li>- 每层保持top-β个候选路径</li>
      <li>- 避免局部最优问题</li>
      <li>- 灵活的准确率-效率权衡</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-3 rounded">
    <h4 class="font-bold mb-2">分数正确性验证</h4>
    <ul class="text-sm space-y-1">
      <li>- 基于双线性恒等式</li>
      <li>- 验证分数计算正确性</li>
      <li>- 轻量级验证机制</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-3 rounded">
    <h4 class="font-bold mb-2">Merkle完整性验证</h4>
    <ul class="text-sm space-y-1">
      <li>- 验证执行完整性</li>
      <li>- 确保路径完整性</li>
      <li>- 每查询仅增加几毫秒</li>
    </ul>
  </div>
</div>

<div class="mt-4 p-3 bg-gray-50 rounded text-center">
  <p class="font-semibold">CIFAR-100: 90% Recall@1, 速度比LSH快7.5倍</p>
</div>

<!--
针对前面提到的问题，我们提出了VCSE-HST方案，全称是"基于分层球形树与束搜索的可验证跨模态可搜索加密"。我们的方案有四大核心创新点。

第一个创新是分层k-叉球形树。我们不再使用二叉树，而是使用k-叉树，每个节点有k=10个分支。我们通过球形k-means递归聚类来构建这棵树。这样一来，在CIFAR-100和Caltech256这样的数据集上，树的深度只有3到4层，远远浅于二叉树。而且每个节点有10个分支，语义划分更加细致，每个子树代表的语义更加紧凑。

第二个创新是束搜索算法。我们不再使用贪婪搜索只保留一条路径，而是在每一层都保持top-β个候选路径，其中β就是beam size。这样就能有效避免贪婪搜索容易陷入局部最优的问题。而且通过调整β的大小，我们可以在准确率和效率之间灵活权衡。

第三个创新是分数正确性验证。我们设计了一个基于双线性身份的轻量级验证机制。用户可以验证云服务器返回的相似度分数是否计算正确，确保服务器没有篡改或伪造分数。

第四个创新是Merkle完整性验证。我们基于Merkle树实现了对束搜索执行过程的完整性验证。这确保了服务器真的按照算法要求扩展了所有该扩展的节点，没有偷工减料。而且这个验证开销非常小，每个查询只增加几毫秒。

最终，在CIFAR-100和Caltech256数据集上，当beam size等于10时，我们的方案达到了90%的Recall@1，与最先进的LSH方法持平，但速度快了7.5倍！当beam size等于3时，速度甚至能快19.7倍，准确率仅下降7%左右。
-->

---
layout: default
---

## 系统模型

<div class="mt-4">
  <img src="./figures/system_model.png" alt="系统架构模型" class="w-5/12 mx-auto">
  <div class="text-center text-sm text-gray-500 mt-2">图1：系统架构模型</div>
</div>

<div class="grid grid-cols-3 gap-4 mt-4">
  <div class="bg-gray-50 p-3 rounded">
    <h3 class="text-lg font-bold mb-2">数据所有者 (DO)</h3>
    <ul class="text-sm space-y-1">
      <li>生成密钥</li>
      <li>CLIP提取特征</li>
      <li>构建球形树索引</li>
      <li>加密并上传</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-3 rounded">
    <h3 class="text-lg font-bold mb-2">数据用户 (DU)</h3>
    <ul class="text-sm space-y-1">
      <li>获取密钥</li>
      <li>生成加密陷阱门</li>
      <li>验证结果</li>
      <li>解密top-k结果</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-3 rounded">
    <h3 class="text-lg font-bold mb-2">云服务器 (CS)</h3>
    <ul class="text-sm space-y-1">
      <li>存储加密数据</li>
      <li>执行束搜索</li>
      <li>计算密文相似度</li>
      <li>返回结果+证明</li>
    </ul>
  </div>
</div>

<!--
现在我们来看一下系统的整体架构。VCSE-HST是一个经典的三方模型，包括数据所有者、数据用户和云服务器。

首先看数据所有者DO。他的职责是准备加密数据。第一步，他生成整个方案需要的密钥，包括两个可逆矩阵M和M的逆、一个随机二进制向量s、验证参数α，以及一个AES密钥K_rule用于加密压缩规则。第二步，他使用预训练的CLIP模型，把所有的图像提取成512维的特征向量。第三步，基于这些特征向量，通过球形k-means递归聚类，构建一棵分层的k-叉球形树。第四步，使用密钥加密所有的索引节点和文档向量。第五步，计算整棵树的Merkle根哈希，作为索引的承诺。最后，把所有加密的数据和索引上传到云端。

接下来看数据用户DU。他的目标是搜索加密数据。首先，他从数据所有者那里获得密钥。当他想要搜索时，比如输入一段文本，他也用CLIP模型提取查询特征，然后使用密钥生成加密的查询陷阱门，提交给云服务器。云服务器返回加密结果和相应的验证证明后，用户首先验证分数的正确性和执行的完整性，确认没有问题后，再解密得到最终的top-k结果。

最后看云服务器CS。它的任务很明确：存储加密数据，执行加密检索。具体来说，它接收用户的陷阱门，然后在加密的分层树上执行束搜索算法。在搜索过程中，它在完全不知道明文的情况下，计算密文的相似度分数，并生成每一层的Merkle验证路径。最后，它返回top-k个加密结果以及完整的验证证明。

这个架构的关键特点是：端到端加密，云服务器始终接触不到明文；可验证计算，用户可以检验云服务器有没有偷懒；高效检索，浅层树加上束搜索，搜索复杂度只有O(β·k·log_k n)。
-->

---
layout: two-cols-header
---

## 核心技术1：分层球形树构建

::left::

### 球形k-Means聚类

**为什么用球形k-means？**
- CLIP特征向量已归一化到单位球面
- 球面距离用内积度量
- 直接在球面上聚类

**算法步骤：**
1. 初始化k个中心
2. 分配：$\text{cluster}(i) = \arg\max_j \mathbf{d}_i^T \mathbf{c}_j$
3. 更新：$\mathbf{c}_j = \frac{\sum_{i \in C_j} \mathbf{d}_i}{\|\sum_{i \in C_j} \mathbf{d}_i\|_2}$
4. 迭代直到收敛

::right::

<div class="mt-2">
  <img src="./figures/hierarchical_spherical_tree.png" alt="分层球形树结构" class="w-full">
  <div class="text-center text-xs text-gray-500 mt-1">图2：分层球形树结构示意</div>
</div>

**树的特性：**
- 分支因子 k = 10
- 深度：3-4层（CIFAR-100: 50k图像）
- 每个节点存储加密的球心向量

<!--
现在我们深入第一个核心技术：分层球形树的构建。

首先，为什么要用球形k-means而不是普通的k-means？关键原因是CLIP模型输出的特征向量都是已经归一化到单位球面上的，它们的长度都是1。在单位球面上，两个向量的相似度是用内积来度量的，也就是余弦相似度。因此，我们直接在球面上进行聚类，更符合这个几何结构。

球形k-means的算法步骤很简单。首先随机初始化k个中心。然后在分配步骤，我们把每个向量分配给与它内积最大的中心，也就是球面距离最近的中心。在更新步骤，我们重新计算每个簇的中心。注意这里有一个关键操作：计算完平均向量后，我们要再归一化，把它投影回单位球面。然后不断迭代直到收敛。

有了球形k-means，我们就可以递归构建树了。我们设置分支因子k等于10，也就是每个内部节点有10个子节点。最小簇大小s_min等于20，也就是当一个节点的向量少于20个时，就变成叶节点。虽然我们设置最大深度为10，但实际上在CIFAR-100这样5万张图的数据集上，树的深度只有3到4层。

递归构建的流程很简单。对于当前的一组向量，我们先计算它们的球心。如果向量数量小于等于20，或者已经达到最大深度，我们就创建一个叶节点，存储这些文档的ID。否则，我们运行球形k-means，把这些向量分成10个簇，然后对每个簇递归调用BuildTree，最后返回一个有10个子节点的内部节点。

这样构建出的树有非常好的特性。深度只有3到4层，远远浅于二叉树。每个内部节点有10个子节点，语义划分更细致。每个节点存储一个加密的球心向量，用来在搜索时计算相似度。
-->

---
layout: default
---

## 核心技术2：束搜索算法

<div class="grid grid-cols-2 gap-4 mt-4">
  <div class="bg-gray-50 p-3 rounded">
    <h3 class="font-bold mb-2">贪婪搜索的问题</h3>
    <ul class="text-sm">
      <li>- 每层只保留1条路径</li>
      <li>- 容易陷入局部最优</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-3 rounded">
    <h3 class="font-bold mb-2">束搜索的优势</h3>
    <ul class="text-sm">
      <li>- 每层保留top-β条路径</li>
      <li>- 全局剪枝</li>
    </ul>
  </div>
</div>

<div class="mt-4 p-3 bg-gray-50 rounded">
  <h4 class="font-bold mb-2">算法流程</h4>
  <p class="text-sm">初始化 Beam = {根节点}</p>
  <p class="text-sm">每层：扩展Beam中所有节点 → 全局排序 → 保留top-β</p>
  <p class="text-sm">返回：最后一层的文档</p>
</div>

<div class="mt-3 text-center p-2 bg-gray-100 rounded">
  <p class="text-sm">复杂度：O(β · k · log_k n)</p>
</div>

<!--
现在我们来看第二个核心技术：束搜索算法。要理解束搜索，我们首先要知道贪婪搜索的问题在哪里。

贪婪搜索是现有树索引方案的标准做法。它在每一层只保留一条最优路径，也就是选择分数最高的那个节点。这种策略的问题是：一旦在某一层选错了，就没有回头路了，整个搜索就偏离了正确方向。举个具体例子：假设在第1层，节点A的分数是0.9，节点B的分数是0.85。贪婪搜索会选择A。但是到了第2层，可能A的最好子节点分数只有0.7，而B的某个子节点分数高达0.95！这时候贪婪搜索已经来不及了，它已经放弃了B，错过了真正的最优结果。这就是局部最优问题。

束搜索完美地解决了这个问题。它不是每层只保留1条路径，而是保留top-β条路径，其中β就是beam size。这样，我们就在多条候选路径上并行探索，进行全局剪枝。还是刚才的例子，假设β等于3。在第1层，我们保留节点A、B、C这前3名。到了第2层，我们把A的10个子节点、B的10个子节点、C的10个子节点全部扩展出来，一共30个候选节点。然后，我们从这30个节点中，全局排序，选择分数最高的前3个进入下一层。这样一来，即使第1层的A不是最终的最优路径，B的那个优秀子节点依然有机会在第2层被选中！束搜索有纠错能力。

算法流程很简单。我们从根节点开始。在每一层，对于beam中的每个节点，如果是叶节点就保留，如果是内部节点就扩展它的所有子节点。然后计算所有候选节点与查询的加密相似度分数，全局排序，保留top-β个节点进入下一层的beam。最后，返回最后一层beam中的叶节点里的所有文档。

这个算法的复杂度是O(β·k·h)，也就是O(β·k·log_k n)。在我们的设置下，β一般是3到10，k等于10，h只有3到4层，所以访问的节点数量远远小于线性搜索的O(n)。这就是我们能达到巨大加速的原因。
-->

---
layout: two-cols-header
---

## 核心技术3：ASPE加密

::left::

### 加密方案

**密钥：** SK = (M, M⁻¹, s, α)

**向量分裂规则：**
- 文档向量：按s[j]分裂为(d₁, d₂)
- 查询向量：按相反规则分裂为(q₁, q₂)

**加密变换：**
- Ê = M^T · [d₁; d₂]
- T̂ = M⁻ᵀ · [q₁; q₂]

::right::

### 内积保持性

**关键性质：**
$$\langle \tilde{T}, \tilde{E}\rangle = \langle q, d \rangle$$

密文内积 = 明文内积

**原理：**
- 矩阵M和M⁻¹相互抵消
- 分裂规则"相反"设计确保内积保持

<!--
现在我们来看第三个核心技术：加密方案与内积保持。这是整个隐私保护的基础。

我们采用的加密方案叫做ASPE，全称是非对称标量积保持加密。它的核心思想是通过向量分裂和矩阵变换来加密，同时保持内积不变。

首先看密钥。我们需要一个随机可逆矩阵M和它的逆，一个随机二进制向量s，一个验证参数α，以及一个AES密钥用于加密可选的压缩规则。

加密文档向量时，我们首先对其L2归一化并填充到长度ℓ。然后根据随机向量s进行分裂。关键规则是：如果s的第j位是0，我们就复制，让d1[j]和d2[j]都等于d[j]。如果s的第j位是1，我们就随机分裂，随机选两个数让它们的和等于d[j]。分裂完后，我们把这两个向量拼接起来，用M的转置矩阵加密，得到加密向量Ê。

加密查询向量的规则恰好相反。如果s的第j位是1，我们就复制。如果s的第j位是0，我们就随机分裂。然后用M的逆转置矩阵加密，得到加密查询T̂。注意这个"相反"的设计非常关键，这正是内积保持的秘密。

现在我们来证明内积保持性。加密后的内积等于加密查询和加密文档的内积。我们把定义展开，利用矩阵性质，M的逆乘以M的转置会约掉。最终化简为分裂后向量的内积和。

现在分情况验证。当s[j]=0时，文档是复制的，d1[j]=d2[j]=d[j]；查询是分裂的，q1[j]+q2[j]=q[j]。那么这一维的贡献就是d[j]乘以(q1[j]+q2[j])，正好等于d[j]q[j]。当s[j]=1时恰好相反，文档是分裂的，查询是复制的，结果也等于d[j]q[j]。

所以无论随机向量s如何取值，每一维的贡献都严格等于原始内积的对应维度贡献。把所有维度加起来，加密向量的内积就等于原始向量的内积！这个性质让我们可以在完全加密的状态下，准确计算相似度，实现隐私保护的检索。
-->

---
layout: default
---

## 核心技术4：分数正确性验证 - 原理

<br>

### 为什么需要分数验证？

云服务器可能会：
- 篡改相似度分数（虚高或虚低）
- 伪造分数来减少计算开销
- 返回错误的排序结果

**我们的目标：** 让用户能够验证服务器返回的每个分数是否计算正确

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="bg-gray-50 p-4 rounded-lg">
    <h4 class="font-bold text-blue-800 mb-3">双线性验证机制</h4>
    <p class="text-sm mb-2"><strong>核心思想：</strong>利用随机标签和秘密参数构建不可伪造的验证等式</p>

    <div class="bg-white p-3 rounded mt-3 text-sm">
      <p class="font-semibold mb-2">索引构建阶段（DO）：</p>
      <p class="mb-1">为每个文档生成：</p>
      <ul class="text-xs space-y-1 ml-4">
        <li>加密向量 Ê</li>
        <li>随机标签 t ∈ ℝ²ˡ</li>
        <li>认证向量：α · E^auth + Ê = t</li>
      </ul>
      <p class="text-xs mt-2 text-gray-600">其中α是秘密参数，只有DO和DU知道</p>
    </div>

    <div class="bg-white p-3 rounded mt-3 text-sm">
      <p class="font-semibold mb-2">查询阶段（DU）：</p>
      <p class="mb-1">为查询生成：</p>
      <ul class="text-xs space-y-1 ml-4">
        <li>加密查询 T̂</li>
        <li>随机标签 r ∈ ℝ²ˡ</li>
        <li>认证向量：α · T^auth + T̂ = r</li>
      </ul>
    </div>
  </div>

  <div class="bg-gray-50 p-4 rounded-lg">
    <h4 class="font-bold text-gray-800 mb-3">验证流程</h4>

    <div class="bg-white p-3 rounded text-sm">
      <p class="font-semibold mb-2">1️⃣ 服务器计算并返回：</p>
      <ul class="text-xs space-y-1 ml-4">
        <li>s = ⟨T̂, Ê⟩ （相似度分数）</li>
        <li>c₁ = ⟨T̂, E^auth⟩ + ⟨T^auth, Ê⟩</li>
        <li>c₂ = ⟨T^auth, E^auth⟩</li>
      </ul>
    </div>

    <div class="bg-white p-3 rounded mt-3 text-sm">
      <p class="font-semibold mb-2">2️⃣ 用户验证双线性等式：</p>
      <div class="bg-gray-50 p-2 rounded font-mono text-xs text-center my-2">
        ⟨r, t⟩ = α² · c₂ + α · c₁ + s
      </div>
      <ul class="text-xs space-y-1">
        <li>等式成立 分数正确</li>
        <li>等式不成立 服务器作弊！</li>
      </ul>
    </div>

    <div class="bg-yellow-50 p-3 rounded mt-3 text-xs">
      <p class="font-semibold mb-1">🔒 安全性保证：</p>
      <ul class="space-y-1">
        <li>服务器不知道 α、t、r</li>
        <li>无法伪造满足等式的 (s, c₁, c₂)</li>
        <li>任何篡改都会破坏等式</li>
      </ul>
    </div>
  </div>
</div>

<!--
现在我们来看第四个核心技术：分数正确性验证。

首先，为什么需要分数验证？云服务器为了节省计算资源，可能会篡改相似度分数，比如虚高或虚低分数。它也可能伪造分数来减少计算开销，或者返回错误的排序结果。我们的目标是让用户能够验证服务器返回的每个分数是否计算正确。

我们采用的是双线性验证机制。核心思想是利用随机标签和秘密参数构建一个不可伪造的验证等式。

在索引构建阶段，数据所有者为每个文档生成三样东西：加密向量Ê、一个随机标签t、以及一个认证向量。认证向量满足这样一个关系：α乘以认证向量加上Ê等于t。这里α是一个秘密参数，只有数据所有者和数据用户知道，云服务器完全不知道。

在查询阶段，数据用户也类似地为查询生成加密查询T̂、随机标签r、以及查询侧的认证向量。

验证流程分两步。第一步，服务器计算并返回三个值：相似度分数s，以及两个辅助系数c1和c2。c1是查询与文档认证向量的两个交叉内积之和，c2是两个认证向量的内积。

第二步，用户用这个双线性等式来验证：标签r和t的内积应该等于α平方乘以c2，加上α乘以c1，再加上s。如果等式成立，说明分数是正确的。如果等式不成立，说明服务器作弊了！

这个机制的安全性在于：服务器不知道α、t、r这三个秘密，所以它无法伪造一组满足等式的(s, c1, c2)。任何对分数的篡改都会破坏这个等式。
-->

---
layout: default
---

## 核心技术5：Merkle完整性验证

### Merkle树承诺机制

<div class="grid grid-cols-2 gap-4 mt-4">
  <div class="bg-gray-50 p-3 rounded">
    <h4 class="font-bold mb-2">构建Merkle树</h4>
    <ul class="text-sm">
      <li>- 叶节点：H(ID || Ê || DocIDs)</li>
      <li>- 内部节点：H(ID || Ê || H(children))</li>
      <li>- 根哈希H(root)公开发布</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-3 rounded">
    <h4 class="font-bold mb-2">验证流程</h4>
    <ul class="text-sm">
      <li>- 验证Merkle路径追溯到根</li>
      <li>- 验证所有beam节点被扩展</li>
      <li>- 验证top-β全局排序</li>
    </ul>
  </div>
</div>

<div class="mt-3 p-2 bg-gray-100 rounded text-sm text-center">
  确保服务器按算法完整执行，无法偷工减料
</div>

<!--
Merkle完整性验证确保服务器真的按照束搜索算法执行了完整的搜索，保证路径完整性。
-->

---
layout: two-cols-header
---

## 完整流程回顾

::left::

### 索引构建（数据所有者）

<div class="bg-gray-50 p-3 rounded text-sm">
  <p>- CLIP提取特征 → L2归一化</p>
  <p>- 球形k-means聚类 → 构建k-叉树</p>
  <p>- ASPE加密所有向量</p>
  <p>- 生成Merkle树，上传密文+根哈希</p>
</div>

### 查询检索（数据用户）

<div class="bg-gray-50 p-3 rounded text-sm mt-3">
  <p>- CLIP提取查询特征 → 生成陷阱门</p>
  <p>- 云端执行束搜索</p>
  <p>- 验证分数+路径完整性</p>
  <p>- 解密获取top-k结果</p>
</div>

::right::

<div class="mt-6">
  <p class="text-sm font-semibold mb-2">示例流程</p>
  <div class="bg-gray-50 p-3 rounded text-xs">
    <p>查询："cat"</p>
    <p>Beam size: 3</p>
    <p class="mt-2">层1: 扩展根节点 → 保留top-3</p>
    <p>层2: 扩展3个节点 → 保留top-3</p>
    <p>层3: 扩展到叶子 → 返回文档</p>
    <p class="mt-2">验证通过 → 解密结果</p>
  </div>
</div>

<!--
好了，在理解了所有技术细节之后，我们最后来完整地回顾一下整个VCSE-HST流程，并用一个直观的例子把所有知识点串起来。

整个流程分为两个阶段。首先是数据所有者的索引构建阶段。他在本地用CLIP提取所有图片的512维特征，然后进行L2归一化。接下来用球形k-means聚类算法构建一棵k-叉球形树，在我们的设置中k等于10，树的深度是3到4层。然后用ASPE方案对所有节点向量和文档向量进行加密，保持内积关系。同时构建Merkle树，为每个节点生成哈希承诺。最后把加密的树索引和根哈希上传到云端。

然后是数据用户的查询检索阶段。用户在本地用CLIP提取查询的特征并归一化，然后用ASPE加密查询向量，生成陷阱门。云端收到陷阱门后，执行束搜索算法。从根节点开始，逐层扩展beam中的所有节点，每层保留top-β个分数最高的候选节点，这样可以避免局部最优。最后返回top-k文档以及所有节点的验证证明。用户收到结果后，首先验证所有节点的分数是否正确，用双线性验证机制。然后验证所有节点的Merkle路径能否追溯到根哈希，确保服务器没有伪造节点。最后验证每层的beam节点是否都被完整扩展，确保服务器没有偷工减料。所有验证都通过后，用户解密得到最终的top-k文档ID。

我们来看一个具体的例子。假设用户想检索"猫"的图片，参数是beam等于3，每节点3个子节点，返回top-3结果。

首先在离线阶段，数据所有者有1000张图片，用CLIP提取特征后构建了一棵3层球形树。用ASPE加密所有向量，计算Merkle树，然后上传加密树和根哈希到云端。

用户查询"cat"时，在本地提取CLIP特征并用ASPE加密，生成陷阱门发送给云端。

云端执行束搜索。第1层，beam只有根节点R，扩展后返回3个子节点：A的分数是0.9，B是0.85，C是0.7。第2层，beam是{A,B,C}，扩展所有3个节点得到9个子节点，保留top-3：A1、A2、B1。第3层，beam是{A1,A2,B1}，扩展到叶子得到9个文档，保留top-3：Doc42、Doc17、Doc89。云端返回这些加密的文档ID以及所有节点的验证证明。

用户收到后进行验证。首先用双线性验证检查所有节点的分数是否正确。然后验证所有节点的Merkle路径能否追溯到根哈希。最后确认每层的beam节点都被完整扩展了。所有验证都通过后，用户解密得到：Doc42是猫躺着，Doc17是猫跳跃，Doc89是猫玩耍。完美地找到了最相关的三张猫的图片！

整个过程，云端自始至终都不知道查询的内容是什么，也不知道文档内容是什么，同时用户可以验证服务器返回的结果是正确和完整的。这就是VCSE-HST的完整流程。
-->

---
layout: default
---

## 实验结果

### 数据集与设置

<div class="grid grid-cols-3 gap-4 text-sm mb-4">
  <div class="bg-gray-50 p-3 rounded">
    <p class="font-semibold">数据集</p>
    <p>CIFAR-100: 50,000图像, 100查询</p>
    <p>Caltech256: 30,607图像, 257查询</p>
  </div>
  <div class="bg-gray-50 p-3 rounded">
    <p class="font-semibold">特征提取</p>
    <p>CLIP ViT-B/32</p>
    <p>512维特征向量</p>
    <p>L2归一化</p>
  </div>
  <div class="bg-gray-50 p-3 rounded">
    <p class="font-semibold">参数</p>
    <p>分支因子 k=10</p>
    <p>Beam size β∈{3,7,10}</p>
    <p>树深度: 3-4层</p>
  </div>
</div>

### 性能对比（CIFAR-100）

<div class="grid grid-cols-2 gap-4 mt-2">
  <div>
    <img src="./figures/paper_accuracy_comparison.png" alt="准确率对比" class="w-full">
    <div class="text-center text-xs text-gray-500 mt-1">准确率对比</div>
  </div>
  <div>
    <img src="./figures/paper_search_time_comparison.png" alt="搜索时间对比" class="w-full">
    <div class="text-center text-xs text-gray-500 mt-1">搜索时间对比</div>
  </div>
</div>

### 关键发现

<div class="grid grid-cols-2 gap-4 mt-4 text-sm">
  <div class="bg-yellow-50 p-3 rounded">
    <p class="font-semibold mb-2">准确率-效率权衡</p>
    <p>β=10: 90% R@1，7.5×加速</p>
    <p>β=3: 83% R@1，19.7×加速</p>
    <p>灵活可调，适应不同场景</p>
  </div>
  <div class="bg-gray-50 p-3 rounded">
    <p class="font-semibold mb-2">验证开销</p>
    <p>Merkle验证：几毫秒/查询</p>
    <p>随beam size线性增长</p>
    <p>可实用的完整性保证</p>
  </div>
</div>

<!--
现在我们来看实验结果，验证我们的方案是否真的有效。

我们在两个大规模数据集上进行了实验。CIFAR-100包含5万张图像和100个查询，Caltech256包含3万多张图像和257个查询。我们使用CLIP模型的ViT-B/32版本提取512维特征向量，并进行L2归一化。主要参数是：分支因子k等于10，beam size我们测试了3、7、10三个值，最终树的深度是3到4层。

我们来看CIFAR-100上的性能对比。这张表非常关键。第一行是Cross-Model-SE，这是目前最先进的LSH方法。它达到90%的Recall@1，但每次查询需要57.47毫秒。第二行是线性搜索，准确率和LSH一样都是90%，因为它们都基于CLIP，但是速度更慢，需要144毫秒。

接下来看我们的方案。当beam size等于3时，Recall@1是83%，比LSH稍低7个百分点，但是速度只要2.91毫秒，是LSH的19.7倍快！当beam size等于7时，Recall@1恢复到89%，速度是6.39毫秒，依然是LSH的9倍快。当beam size等于10时，Recall@1达到90%，与LSH持平，速度是7.66毫秒，还是LSH的7.5倍快！

这个结果非常令人振奋。我们实现了准确率和效率的灵活权衡。如果你的应用对准确率要求极高，可以用beam=10，达到最先进水平，同时速度还快7.5倍。如果你的应用对速度要求更高，可以接受略低的准确率，那就用beam=3，速度快近20倍，准确率只降低7%。

关于验证开销，我们测试了Merkle完整性验证的时间。结果显示，每个查询只增加几毫秒的验证时间，而且这个开销随beam size线性增长。这说明我们的可验证机制是实用的，不会成为系统的瓶颈。
-->

---
layout: default
---

## 维度降低分析：意外的发现

<div class="grid grid-cols-2 gap-6 mt-4">
  <div class="bg-gray-50 p-4 rounded-lg text-sm">
    <h4 class="font-bold text-blue-800 mb-2">方差引导的维度降低</h4>
    <p class="mb-2">核心思想：去除低方差维度</p>
    <ul class="space-y-1">
      <li>计算每个维度的方差</li>
      <li>选择方差最小的k个维度删除</li>
      <li>k = ⌊d × k_ratio⌋</li>
      <li>用AES加密压缩规则，确保客户端和服务器一致</li>
    </ul>
    <br>
    <p class="font-semibold mb-1">动机：</p>
    <p>减少内存和通信开销</p>
    <p>低方差维度鉴别能力弱，可能是噪声</p>
  </div>

  <div class="bg-gray-50 p-4 rounded-lg text-sm">
    <h4 class="font-bold text-gray-800 mb-2">非单调的准确率曲线</h4>
    <p class="mb-2 font-semibold">CIFAR-100上的Recall@1（beam=10）：</p>
    <ul class="space-y-1 text-xs">
      <li>0% 压缩: 90% R@1 （基线）</li>
      <li>2.5% 压缩: <span class="text-green-600 font-semibold">92% R@1 ↑</span></li>
      <li>5% 压缩: <span class="text-green-600 font-semibold">93% R@1 ↑</span> (峰值！)</li>
      <li>7.5% 压缩: 90% R@1</li>
      <li>10% 压缩: 88% R@1 ↓</li>
      <li>15% 压缩: 84% R@1 ↓</li>
      <li>20% 压缩: 82% R@1 ↓</li>
    </ul>
    <br>
    <p class="font-semibold text-green-700">意外发现：适度压缩（5%）反而提升3%准确率！</p>
  </div>
</div>

<div class="mt-4 p-4 bg-yellow-50 rounded-lg text-sm">
  <h4 class="font-bold text-gray-800 mb-2">理论解释：信号-噪声分解</h4>
  <p class="mb-2">归一化向量 <strong>d = s + η</strong>，其中s是信号，η是噪声</p>
  <p class="mb-2">余弦相似度近似：</p>
  <p class="font-mono text-xs mb-2">cos(q,d) ≈ ⟨s_q, s_d⟩ + ⟨η_q, η_d⟩ / √[(‖s_q‖²+‖η_q‖²)(‖s_d‖²+‖η_d‖²)]</p>
  <ul class="space-y-1">
    <li>去除低方差维度 减少分母和η项方差</li>
    <li>提升信噪比 改善聚类质量和球心稳定性</li>
    <li>过度压缩 开始丢失有用信号 准确率下降</li>
  </ul>
  <p class="mt-2 font-semibold">结论：5%压缩是最优点，平衡了噪声消除和信号保留</p>
</div>

<!--
现在我们来看一个有趣的发现：维度降低分析。

我们的方案包含一个可选的方差引导的维度降低模块。核心思想很简单：计算每个维度的方差，然后选择方差最小的k个维度删除。这里k等于维度数d乘以压缩比例。我们用AES加密这个压缩规则，确保客户端和服务器使用相同的规则，同时不泄露具体哪些维度被删除了。

最初的动机是为了减少内存和通信开销。我们认为低方差的维度鉴别能力弱，可能主要是噪声。但实验结果却给了我们一个意外的惊喜。

我们在CIFAR-100上测试了不同压缩比例下的准确率，beam size固定为10。看右边的结果，非常有意思。当我们不压缩时，Recall@1是90%，这是基线。当我们压缩2.5%的维度时，准确率不降反升，达到92%！当压缩5%时，准确率达到峰值93%，比基线还高了3个百分点！然后随着压缩比例继续增加，准确率开始下降。7.5%压缩时回到90%，10%压缩时降到88%，之后继续下滑。

这个非单调的曲线非常违反直觉。为什么删除维度反而能提升准确率？

我们通过信号-噪声分解来解释这个现象。我们把归一化向量分解为信号s加上噪声η。余弦相似度可以近似为信号内积加上噪声内积，除以一个包含信号和噪声范数的分母。当我们去除低方差维度时，我们主要删除的是噪声维度。这样做有两个效果：第一，减少了分母；第二，减少了噪声项的方差。两者共同作用，提升了信噪比。信噪比提高后，聚类质量变好，球心更稳定，搜索时更不容易走错方向。但是如果压缩过度，我们就开始丢失有用的信号维度，准确率自然就下降了。

所以5%压缩是一个最优点，它完美平衡了噪声消除和信号保留。这个发现告诉我们，并不是所有的特征维度都是有用的，适度的维度选择反而能提升检索性能。
-->

---
layout: two-cols-header
---

## 总结、局限性与未来工作

::left::

### 📌 核心贡献总结

<div class="bg-gray-50 p-3 rounded-lg text-sm mb-3">
  <p class="font-semibold mb-2">技术创新：</p>
  <ul class="space-y-1 text-xs">
    <li>分层k-叉球形树（k=10，深度3-4层）</li>
    <li>束搜索算法（避免局部最优）</li>
    <li>ASPE加密（内积保持）</li>
    <li>分数正确性验证（双线性验证）</li>
    <li>Merkle完整性验证（路径完整性）</li>
  </ul>
</div>

<div class="bg-gray-50 p-3 rounded-lg text-sm">
  <p class="font-semibold mb-2">实验成果：</p>
  <ul class="space-y-1 text-xs">
    <li>CIFAR-100: 90% R@1，7.5×加速</li>
    <li>灵活的准确率-效率权衡（β∈{3,7,10}）</li>
    <li>轻量级验证（几毫秒/查询）</li>
  </ul>
</div>

### 局限性

<ul class="text-xs space-y-1 mt-3">
  <li><strong>访问模式泄露</strong>：无法隐藏哪些文档被返回（需ORAM）</li>
  <li><strong>搜索模式泄露</strong>：无法隐藏访问了哪些树节点</li>
  <li><strong>静态设置</strong>：不支持动态更新，需要重建索引</li>
  <li><strong>Beam搜索近似</strong>：不保证全局top-k最优</li>
</ul>

::right::

### 未来研究方向

<div class="bg-gray-50 p-3 rounded-lg text-sm mb-3">
  <p class="font-semibold mb-2">1. 动态更新支持</p>
  <p class="text-xs">支持增删改操作，无需重建整棵树</p>
  <p class="text-xs">研究前向/后向安全性</p>
</div>

<div class="bg-gray-50 p-3 rounded-lg text-sm mb-3">
  <p class="font-semibold mb-2">2. 自适应束搜索</p>
  <p class="text-xs">根据查询特征动态调整beam size</p>
  <p class="text-xs">简单查询用小beam，复杂查询用大beam</p>
</div>

<div class="bg-yellow-50 p-3 rounded-lg text-sm mb-3">
  <p class="font-semibold mb-2">3. 隐藏访问模式</p>
  <p class="text-xs">结合ORAM技术隐藏访问模式</p>
  <p class="text-xs">探索效率与隐私的折中方案</p>
</div>

<div class="bg-pink-50 p-3 rounded-lg text-sm">
  <p class="font-semibold mb-2">4. 更大规模数据集</p>
  <p class="text-xs">扩展到百万级图像数据集</p>
  <p class="text-xs">研究混合索引结构（树+LSH）</p>
</div>

<!--
最后，让我们总结一下这项工作，并展望未来的研究方向。

在技术创新方面，我们提出了五大核心技术。第一是分层k-叉球形树，使用k等于10的分支因子，树深度只有3到4层。第二是束搜索算法，通过维护多条候选路径有效避免局部最优。第三是ASPE加密方案，实现了内积保持，让我们能在密文上准确计算相似度。第四是分数正确性验证，基于双线性恒等式，确保服务器返回的分数没有被篡改。第五是Merkle完整性验证，确保服务器真的按照算法执行了完整的搜索，保证了路径完整性。

在实验成果方面，我们在CIFAR-100数据集上达到了90%的Recall@1，同时速度比最先进的LSH方法快7.5倍。我们实现了灵活的准确率-效率权衡，通过调整beam size从3到10，可以在不同应用场景下选择最优配置。而且我们的验证机制非常轻量，每个查询只增加几毫秒的开销。

当然，我们的方案也有一些局限性。首先是访问模式泄露，我们无法隐藏哪些文档被返回给用户，要解决这个问题需要引入ORAM等技术。其次是搜索模式泄露，我们无法隐藏访问了哪些树节点。第三，我们目前只支持静态设置，如果数据更新，需要重建整棵树。第四，束搜索本身是一个近似算法，不保证找到全局top-k最优解。

未来的研究可以从四个方向展开。第一是支持动态更新，让系统能够支持增删改操作，无需每次都重建整棵树，并研究前向和后向安全性。第二是自适应束搜索，根据查询的特征动态调整beam size，简单查询用小beam节省资源，复杂查询用大beam提高准确率。第三是隐藏访问模式，结合ORAM等技术进一步提升隐私保护水平，探索效率与隐私的最佳折中。第四是扩展到更大规模的数据集，比如百万级的图像库，并研究树索引和LSH的混合结构，结合两者的优势。
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
    <div class="text-4xl mb-2">🌳</div>
    <p class="font-semibold">分层k-叉球形树</p>
    <p class="text-xs text-gray-600">深度3-4层，k=10</p>
  </div>
  <div class="text-center">
    <div class="text-4xl mb-2">🔍</div>
    <p class="font-semibold">束搜索算法</p>
    <p class="text-xs text-gray-600">避免局部最优</p>
  </div>
  <div class="text-center">
    <div class="text-4xl mb-2">🔐</div>
    <p class="font-semibold">可验证性</p>
    <p class="text-xs text-gray-600">分数+完整性验证</p>
  </div>
</div>

<div class="mt-12 text-center p-6 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg">
  <p class="text-2xl font-bold mb-4">VCSE-HST</p>
  <p class="text-xl mb-2">90% Recall@1 + 7.5× 加速</p>
  <p class="text-sm text-gray-600">高效 · 安全 · 可验证的跨模态可搜索加密</p>
</div>

<div class="mt-8 text-center text-sm text-gray-500">
  <p>Yuzhe Wang · 华东师范大学</p>
  <p>IEEE Transactions on Services Computing</p>
</div>

<!--
我的分享就到这里，感谢大家的聆听！欢迎大家提问和讨论。
-->
