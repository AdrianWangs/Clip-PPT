---
theme: seriph
background: /image/slides/image.png
title: 'Verifiable Cross-Modal Searchable Encryption via Hierarchical Spherical Tree with Beam Search'
info: |
  ## 基于层次球面树与束搜索的可验证跨模态可搜索加密
  一种高效且可验证的加密数据检索方案
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

## 基于层次球面树与束搜索的可验证跨模态可搜索加密

<div class="pt-12">
  <span class="px-2 py-1 font-semibold">汇报人: 王宇哲</span>
</div>

<div class="pt-6 text-sm">
  Yuzhe Wang (East China Normal University, 2025)
  <br>
  IEEE Transactions on Services Computing
</div>

<!--
大家好，今天我要分享的论文是《基于层次球面树与束搜索的可验证跨模态可搜索加密》，这是华东师范大学2025年投稿到IEEE TSC的一篇关于云端加密数据可验证检索的重要论文。
-->

---
layout: two-cols-header
---

# 研究背景与动机

::left::

### 云计算时代的隐私挑战

- **数据外包趋势**：海量多媒体数据（图像、文本）存储在云端
- **隐私保护需求**：用户不信任云服务器，需要加密数据
- **检索需求**：加密后仍需高效检索
- **跨模态检索**：支持图文互搜（如用文本搜图片）

*CLIP等预训练模型为跨模态检索提供了强大的语义理解能力。*

::right::

### 现有方案的不足

- **LSH方案问题**：
  - 内存开销大（需64个哈希表）
  - 查询延迟高（需探测多表）

- **二叉树方案问题**：
  - 树深度过深（$O(\log_2 n)$）
  - 语义划分粗糙（每层仅2分支）
  - 贪心搜索易陷入局部最优

- **可验证性缺失**：云服务器可能偷懒返回不完整结果

*本文旨在设计一个高效、准确且可验证的跨模态加密检索方案。*

<!--
在云计算时代，越来越多的企业和个人将多媒体数据外包到云端。但这带来了隐私问题：我们不完全信任云服务器。解决方案是加密数据，但加密后如何高效检索成为难题。

现有方案存在诸多不足。LSH方法需要维护大量哈希表，内存和延迟开销大。二叉树方案虽然能剪枝，但树太深、分支太少，贪心搜索容易错过最优结果。更重要的是，现有方案缺乏可验证性——云服务器可能为了省钱，返回不完整的搜索结果，但用户无法察觉。

因此，本文的目标是设计一个高效、准确且可验证的跨模态加密检索方案。
-->

---
layout: default
---

## 相关工作

<br>

### 可搜索加密（SSE）领域

- **ML-RKS方案**（Miao et al.）：使用k-means聚类和二叉树实现亚线性搜索，但二叉树深度过深，语义划分粗糙。
- **VRFMS方案**（Li et al.）：使用同态MAC验证得分正确性，但未验证搜索执行的完整性。

### 隐私保护跨模态检索（PPCMR）

- **PITR方案**（Zhang et al.）：使用HNSW图索引和适配器增强零样本性能。
- **Cross-Model-SE**（Yang et al.）：基于LSH的量子安全方案，需64个哈希表，内存开销大。
- **MU-TEIR方案**（Yang et al.）：支持多用户场景，但检索效率较低。

<div class="mt-8 p-4 bg-yellow-50 rounded-lg text-center">
  <p><strong>现有方案的共同问题</strong>：LSH方法效率高但准确率受限；树方法准确但效率低；缺乏执行完整性验证。</p>
</div>

<!--
在可搜索加密领域，Miao等人的ML-RKS方案使用k-means和二叉树实现了亚线性搜索复杂度，但二叉树的深度问题和粗糙的语义划分限制了其性能。Li等人的VRFMS虽然提供了得分正确性验证，但没有验证搜索算法本身是否被完整执行。

在隐私保护跨模态检索方面，Yang等人的Cross-Model-SE基于LSH技术，虽然达到了90%的Recall@1，但需要64个哈希表，内存和查询延迟开销都很大。

总的来说，现有方案面临一个共同的挑战：LSH方法虽然快但准确率受哈希近似影响；树方法虽然准但深度问题导致效率低；更重要的是，现有方案都缺乏对搜索执行完整性的验证机制。
-->

---
layout: default
---

## 系统整体架构

<div class="mt-6">
  <img src="/figures/system_model.png" alt="系统模型" class="w-5/12 mx-auto">
  <div class="text-center text-sm text-gray-500 mt-2">图1：VCSE-HST系统架构模型</div>
</div>

<div class="grid grid-cols-3 gap-6 mt-4">
  <div class="bg-gray-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-gray-800 mb-3">数据所有者 (DO)</h3>
    <ul class="text-sm space-y-2">
      <li>生成密钥 $SK=(\mathbf{s}, \mathbf{M}, \alpha, K_{\text{rule}})$</li>
      <li>使用CLIP提取512维特征</li>
      <li>构建层次球面树索引</li>
      <li>加密数据和索引上传云端</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-gray-800 mb-3">数据用户 (DU)</h3>
    <ul class="text-sm space-y-2">
      <li>从DO获取密钥</li>
      <li>使用CLIP提取查询特征</li>
      <li>生成加密陷阱门</li>
      <li>验证并解密检索结果</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-gray-800 mb-3">云服务器 (CS)</h3>
    <ul class="text-sm space-y-2">
      <li>存储加密索引和数据</li>
      <li>接收用户陷阱门</li>
      <li>执行束搜索算法</li>
      <li>返回Top-k加密结果</li>
    </ul>
  </div>
</div>

<!--
VCSE-HST系统由三个实体组成。数据所有者负责密钥生成、特征提取、索引构建和加密。数据用户从DO获取密钥后，可以生成加密查询并验证返回结果。云服务器存储所有加密数据，并在密文上执行束搜索算法。

整个流程分为四步：首先DO构建加密索引并上传；然后DU生成加密陷阱门；CS在加密树上执行束搜索并返回结果；最后DU验证结果的正确性和完整性。所有操作都保证云服务器无法获知明文内容。
-->

---
layout: default
---

## 核心创新点

<br>

<div class="grid grid-cols-2 gap-6">
  <div class="bg-blue-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-blue-800 mb-2">1. 层次k叉球面树</h3>
    <p class="text-sm">使用$k=10$分支的球面$k$-means聚类递归构建索引树，将树深度降至3-4层（二叉树需$\log_2 50000 \approx 16$层），提供更细粒度的语义划分。</p>
  </div>

  <div class="bg-green-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-green-800 mb-2">2. 束搜索算法</h3>
    <p class="text-sm">在每层维护$\beta$个候选路径（而非贪心搜索的1个），通过全局剪枝避免局部最优。束大小可调：$\beta=3$时19.7倍加速，$\beta=10$时匹配LSH准确率且快7.5倍。</p>
  </div>

  <div class="bg-purple-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-purple-800 mb-2">3. 得分正确性验证</h3>
    <p class="text-sm">使用双线性验证机制，为每个文档和查询生成认证向量，客户端可验证云服务器返回的相似度得分是否被篡改（详见后续页面）。</p>
  </div>

  <div class="bg-orange-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-orange-800 mb-2">4. Merkle树完整性验证</h3>
    <p class="text-sm">对加密索引树构建Merkle承诺，搜索时逐层提供包含证明，确保云服务器执行了完整的束搜索，未跳过节点或伪造结果（详见后续页面）。</p>
  </div>
</div>

<div class="mt-6 p-4 bg-gray-50 rounded-lg text-center">
  <p class="font-bold">实验结果：CIFAR-100 (50,000图像) 上达到90% Recall@1，比Cross-Model-SE快7.5倍</p>
</div>

<!--
本文的四大核心创新点是：

第一，层次k叉球面树。我们使用10分支的球面k-means递归构建索引，将树深度从二叉树的16层降至3-4层，大幅减少累积误差，同时提供更细粒度的语义聚类。

第二，束搜索算法。不同于贪心搜索只保留1条路径，我们在每层维护多个候选路径，通过全局剪枝避免局部最优。束大小是可调的：小束快但略损失精度，大束准确但稍慢。

第三，得分正确性验证。我们设计了双线性验证机制，让客户端能检验云服务器返回的相似度得分是否被篡改。

第四，Merkle树完整性验证。我们对整个索引树构建Merkle承诺，搜索时逐层提供证明，确保云服务器没有偷懒跳过节点。

这四项创新共同实现了效率和可验证性的平衡。
-->

---
layout: two-cols-header
---

## 层次球面树构建

::left::

### 球面$k$-Means聚类

**核心思想**：CLIP特征归一化到单位球面后，使用球面距离（内积）进行聚类。

**算法流程**：
1. 随机初始化$k$个中心向量
2. 分配：将每个向量分配给内积最大的中心
3. 更新：重新计算每簇的中心并归一化
4. 重复直到收敛

**递归构建**：
- 设置$k=10$（分支因子）和$s_{\min}=20$（最小簇大小）
- 对每个节点的数据递归聚类，直到叶节点
- 最终树深度：3-4层（CIFAR-100: 50,000图像）

::right::

<div class="mt-4">
  <img src="/figures/hierarchical_tree_structure.pdf" alt="层次球面树结构" class="w-full">
  <div class="text-xs text-gray-500 text-center mt-2">图2：单位球面上的层次树结构（示意图显示k=6分支）。蓝色标记为L1层中心，橙色三角为L2子节点，通过大圆弧连接。实验中k=10，深度3-4层。</div>
</div>

<div class="mt-4 p-3 bg-blue-50 rounded text-sm">
<strong>关键优势</strong>：相比二叉树，k叉树深度浅、语义划分细、累积误差小。
</div>

<!--
层次球面树是本文的第一个核心创新。我们使用球面k-means算法递归构建索引树。

由于CLIP提取的特征向量都归一化到了单位球面上，因此我们使用内积（即余弦相似度）作为距离度量。算法流程很简单：先随机初始化k个中心，然后迭代地分配向量到最近的中心，并重新计算每簇的中心向量并归一化。

我们设置k=10，也就是每个节点有10个子节点，并设置最小簇大小为20。对每个节点的数据递归应用球面k-means，直到数据量小于20或达到最大深度。

右图展示了单位球面上的层次树结构。虽然示意图显示的是k=6的情况，但实际实验中我们用k=10。在CIFAR-100的50,000张图像上，最终树深度只有3-4层，远远浅于二叉树的16层。

这种浅树设计带来三个优势：深度浅减少了累积误差，10分支提供了更细粒度的语义划分，搜索时也能更快触达叶节点。
-->

---
layout: default
---

## 束搜索算法

<br>

### 核心思想：避免贪心搜索的局部最优问题

<div class="grid grid-cols-2 gap-6 mt-4">
  <div class="bg-red-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-red-800 mb-2">贪心搜索的问题</h3>
    <ul class="text-sm space-y-2">
      <li>每层只保留<strong>1条</strong>最优路径</li>
      <li>无法回溯，易陷入局部最优</li>
      <li>例如：第1层选择了次优分支，后续无法纠正</li>
      <li>准确率损失明显</li>
    </ul>
  </div>

  <div class="bg-green-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-green-800 mb-2">束搜索的改进</h3>
    <ul class="text-sm space-y-2">
      <li>每层维护<strong>$\beta$条</strong>候选路径</li>
      <li>全局剪枝，保留top-$\beta$节点</li>
      <li>平衡探索和效率</li>
      <li>$\beta$可调：小值快速，大值准确</li>
    </ul>
  </div>
</div>

### 算法流程（束大小$\beta$）

1. **初始化**：从根节点开始，初始束$\mathcal{B}_0 = \{\text{root}\}$
2. **扩展**：对当前束中每个非叶节点，计算其所有子节点与查询的相似度
3. **剪枝**：在**全局范围**选择top-$\beta$个得分最高的节点作为下一层的束
4. **重复**：直到束中只有叶节点
5. **返回**：在叶节点包含的文档中计算精确得分，返回top-$k$结果

<div class="mt-4 p-4 bg-yellow-50 rounded-lg text-center">
  <p><strong>复杂度</strong>：$O(\beta k \log_k n)$，其中$k=10$、$h=\log_k n$。实验中$\beta=10$时仅访问极小部分数据。</p>
</div>

<!--
束搜索是本文的第二个核心创新，用于解决贪心搜索的局部最优问题。

贪心搜索的问题在于：每层只保留1条最优路径。一旦在某层选错了分支，后续就无法纠正。比如第1层有10个分支，如果真正的最优结果在第2优的分支下，贪心搜索会直接错过。

束搜索的改进是：每层维护$\beta$条候选路径，而不是1条。具体做法是，在全局范围内选择得分最高的top-$\beta$个节点，作为下一层的搜索候选。这样就能同时探索多条路径，大大降低陷入局部最优的风险。

算法流程很简单：从根节点开始，逐层扩展束中所有节点的子节点，然后全局剪枝保留top-$\beta$，直到到达叶节点。最后在叶节点包含的文档中计算精确得分并排序。

束大小$\beta$是一个可调参数。小的$\beta$搜索快但可能损失精度，大的$\beta$更准确但稍慢。实验显示$\beta=10$时达到90%准确率，$\beta=3$时仍有83%准确率但快19.7倍。

复杂度分析：访问节点数约为$O(\beta k h)$，其中$h=\log_k n$是树深度。在50,000图像的数据集上，$\beta=10$时仅访问极小部分数据，远优于线性扫描。
-->

---
layout: two-cols-header
---

## 得分正确性验证

::left::

### 验证机制：双线性认证

**问题**：如何验证云服务器返回的相似度得分$s=\langle \mathbf{E}, \mathbf{T}\rangle$是否正确？

**方案**：为每个文档和查询生成认证向量

- **文档侧**（DO生成）：随机标签$\mathbf{t}$，计算$\mathbf{E}^{\text{auth}}=(\mathbf{t}-\mathbf{E})/\alpha$
- **查询侧**（DU生成）：随机标签$\mathbf{r}$，计算$\mathbf{T}^{\text{auth}}=(\mathbf{r}-\mathbf{T})/\alpha$

**服务器返回**：$(s, c_1, c_2)$，其中
- $s = \langle \mathbf{T}, \mathbf{E}\rangle$（相似度得分）
- $c_1 = \langle \mathbf{T}, \mathbf{E}^{\text{auth}}\rangle + \langle \mathbf{T}^{\text{auth}}, \mathbf{E}\rangle$
- $c_2 = \langle \mathbf{T}^{\text{auth}}, \mathbf{E}^{\text{auth}}\rangle$

**客户端验证**：检查 $\langle \mathbf{r}, \mathbf{t}\rangle = \alpha^2 c_2 + \alpha c_1 + s$

::right::

### 具体验证例子

**场景**：用户搜索"猫"，服务器返回图像ID=42的得分$s=0.85$

**步骤1（索引构建时）**：DO为图像42生成
- 加密向量$\mathbf{E}_{42}$
- 随机标签$\mathbf{t}_{42} = [0.3, -0.7, 0.2, \ldots]$
- 认证向量$\mathbf{E}_{42}^{\text{auth}} = (\mathbf{t}_{42} - \mathbf{E}_{42})/\alpha$

**步骤2（查询时）**：DU生成
- 加密查询$\mathbf{T}_{\text{猫}}$
- 随机标签$\mathbf{r} = [0.5, 0.1, -0.4, \ldots]$
- 认证向量$\mathbf{T}^{\text{auth}} = (\mathbf{r} - \mathbf{T}_{\text{猫}})/\alpha$

**步骤3（服务器计算）**：返回$(s=0.85, c_1, c_2)$

**步骤4（客户端验证）**：
- 计算$\mathbf{r} \cdot \mathbf{t}_{42} = 0.15 - 0.07 - 0.08 + \ldots = \text{val}$
- 检查 $\text{val} \stackrel{?}{=} \alpha^2 c_2 + \alpha c_1 + 0.85$
- ✅ 若相等，得分正确；❌ 若不等，服务器篡改了得分

<!--
得分正确性验证是第三个核心创新，确保云服务器返回的相似度得分是真实的。

验证机制基于双线性认证。核心思想是：为每个文档和查询生成额外的认证向量，利用双线性性质构造一个只有正确得分才能满足的验证等式。

具体来说，DO在索引构建时为每个文档生成随机标签$\mathbf{t}$和认证向量。DU在查询时生成随机标签$\mathbf{r}$和查询认证向量。服务器不仅要返回得分$s$，还要返回两个辅助系数$c_1$和$c_2$。客户端用本地的标签验证双线性等式。

让我们看一个具体例子。假设用户搜索"猫"，服务器返回图像42的得分0.85。

在索引构建时，DO已经为图像42生成了随机标签向量$\mathbf{t}_{42}$和对应的认证向量。查询时，DU为"猫"生成了随机标签$\mathbf{r}$和查询认证向量。服务器返回得分0.85和两个辅助系数。客户端计算两个标签的内积，检查是否等于右边的验证公式。

如果服务器篡改了得分，比如本应是0.85但报告成0.90，那么验证等式就会不成立，客户端立即能发现。这是因为服务器不知道秘密标签$\mathbf{t}$和$\mathbf{r}$，无法伪造一致的辅助系数。

这个机制保证了返回结果的得分正确性。
-->

---
layout: two-cols-header
---

## Merkle树完整性验证

::left::

### 验证机制：Merkle承诺

**问题**：得分正确性只验证返回结果的数值，但如何确保服务器没有偷懒跳过节点？

**方案**：对整个加密索引树构建Merkle哈希树

**索引构建时（DO）**：
- 叶节点：$H(u) = \text{Hash}(\text{id}(u) \| \widehat{\mathbf{c}}_u \| \text{Docs}(u) \| \text{LEAF})$
- 内部节点：$H(u) = \text{Hash}(\text{id}(u) \| \widehat{\mathbf{c}}_u \| H(v_1) \| \cdots \| H(v_k) \| \text{INTERNAL})$
- 发布Merkle根$H(\text{root})$

**搜索时（CS）**：每层返回
1. 当前束中所有节点的ID
2. 每个节点的**所有子节点**及其得分
3. 每个访问节点的Merkle包含证明（兄弟哈希）

**验证时（DU）**：检查
1. 所有访问节点的Merkle路径是否合法
2. 服务器是否扩展了所有束节点的子节点
3. 全局top-$\beta$剪枝是否正确
4. 返回文档是否在最终叶节点中

::right::

<div class="mt-2">
  <img src="/figures/merkle_beam_verification.png" alt="Merkle验证示意" class="w-full">
  <div class="text-xs text-gray-500 text-center mt-1">图3：k=3树深度2的Merkle验证。验证叶节点L1：提供路径L1→A→Root和兄弟哈希{L2,L3,B,C}，客户端重算哈希验证根。</div>
</div>

### 具体验证例子

**场景**：束大小$\beta=2$，在3叉树上搜索

**第1层**：服务器声称扩展Root的3个子节点{A,B,C}，得分[0.9, 0.7, 0.6]，保留top-2={A,B}
- **验证**：检查A,B,C的Merkle路径，重算全局top-2确认是{A,B}

**第2层**：服务器声称扩展A的子节点{L1,L2,L3}（得分[0.85,0.80,0.75]）和B的子节点{L4,L5,L6}（得分[0.72,0.68,0.65]），保留top-2={L1,L2}
- **验证**：检查所有叶节点Merkle路径，重算全局top-2确认是{L1,L2}

**最终**：服务器返回L1,L2中的文档
- **验证**：检查文档ID确实属于L1,L2

✅ 若服务器跳过节点B或伪造L7，Merkle验证会失败！

<!--
Merkle树完整性验证是第四个核心创新，解决了执行完整性问题。

得分正确性验证只能确认返回结果的数值准确，但无法保证服务器执行了完整的搜索。比如服务器可能为了省钱，只扩展了部分节点，或者跳过了某些束路径。

我们的方案是对整个加密索引树构建Merkle哈希树。DO在索引构建时，自底向上计算每个节点的哈希值，叶节点哈希包含节点ID、加密中心和文档列表，内部节点哈希包含节点ID、加密中心和所有子节点的哈希。最后发布Merkle根。

搜索时，服务器在每层不仅要返回束节点和它们的子节点，还要为每个访问的节点提供Merkle包含证明，也就是从该节点到根的路径上所有兄弟节点的哈希值。

客户端验证时检查四件事：一是所有访问节点的Merkle路径是否能重算出正确的根哈希；二是服务器是否真的扩展了所有束节点的子节点；三是全局剪枝是否正确；四是返回文档是否真的在最终叶节点中。

让我们看右图的具体例子。假设k=3、深度2、束大小2。第1层，服务器扩展根节点的3个子节点A,B,C，得分分别是0.9,0.7,0.6，保留top-2就是A和B。客户端检查A,B,C的Merkle路径，并重新计算全局top-2，确认确实是A和B。第2层，服务器扩展A的3个叶节点和B的3个叶节点，一共6个叶节点，保留top-2是L1和L2。客户端同样检查所有叶节点的Merkle路径，重算top-2。最终验证返回的文档确实在L1,L2中。

如果服务器偷懒跳过了节点B，或者伪造了一个不存在的节点L7，Merkle验证都会失败，因为无法提供有效的包含证明。

这个机制保证了搜索执行的完整性，开销仅几毫秒。
-->

---
layout: default
---

## 安全分析

<br>

<div class="grid grid-cols-2 gap-6">
  <div class="bg-gray-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-gray-800 mb-3">威胁模型</h3>
    <ul class="text-sm space-y-2">
      <li><strong>诚实但好奇的云服务器</strong>：试图推断加密数据内容</li>
      <li><strong>恶意云服务器</strong>：可能篡改得分或跳过搜索步骤</li>
      <li><strong>已知密文攻击</strong>：攻击者仅能观察加密数据和陷阱门</li>
      <li><strong>泄露范围</strong>：访问模式（返回哪些文档）和搜索模式（访问哪些节点）</li>
    </ul>
  </div>

  <div class="bg-gray-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-gray-800 mb-3">安全保证</h3>
    <ul class="text-sm space-y-2">
      <li><strong>索引机密性</strong>：加密向量$\mathbf{E}_i=\mathbf{M}^{\top}\mathbf{I}_i$在不知道$\mathbf{M}$和$\mathbf{s}$时计算上不可区分于随机向量</li>
      <li><strong>查询机密性</strong>：随机分裂机制保证同一查询的陷阱门不可关联</li>
      <li><strong>得分正确性</strong>：篡改得分会以压倒性概率被双线性验证检测</li>
      <li><strong>执行完整性</strong>：Merkle承诺保证路径完整性和结果包含性</li>
    </ul>
  </div>
</div>

### 主要安全定理

<div class="mt-4 p-4 bg-blue-50 rounded-lg">
  <p class="text-sm"><strong>定理1（索引和查询机密性）</strong>：在已知密文模型下，假设CS不获得密钥$(\mathbf{M}, \mathbf{s})$，VCSE-HST保证索引和查询机密性。证明基于高熵填充和ASPE式变换的不可区分性。</p>
</div>

<div class="mt-4 p-4 bg-green-50 rounded-lg">
  <p class="text-sm"><strong>定理2（陷阱门不可关联性）</strong>：对同一查询生成的两个陷阱门$\widehat{\mathbf{q}}'$和$\widehat{\mathbf{q}}''$，由于随机分裂和填充使用独立随机数，碰撞概率可忽略不计。</p>
</div>

<div class="mt-4 p-4 bg-purple-50 rounded-lg">
  <p class="text-sm"><strong>定理3（得分正确性）</strong>：在随机标签$(\mathbf{t},\mathbf{r})$和秘密$\alpha$未泄露的情况下，任何对得分$s$的修改都会以压倒性概率违反验证等式。</p>
</div>

<div class="mt-4 p-4 bg-orange-50 rounded-lg">
  <p class="text-sm"><strong>定理4（执行完整性）</strong>：在哈希函数抗碰撞的假设下，服务器任何偏离束搜索协议的行为（跳过子节点、注入虚假节点、误报剪枝）都会被客户端检测到。</p>
</div>

<!--
现在我们来分析VCSE-HST的安全性。

威胁模型考虑两种攻击者：诚实但好奇的服务器会试图推断数据内容；恶意服务器可能篡改结果或偷工减料。我们假设攻击者只能进行已知密文攻击，无法获取密钥。方案会泄露访问模式和搜索模式，这是大多数实用SSE方案的共同限制。

安全保证涵盖四个方面。第一，索引机密性：加密向量在不知道变换矩阵和分裂向量的情况下，计算上不可区分于随机向量。第二，查询机密性：由于每次查询都使用独立的随机分裂，同一查询的陷阱门无法被关联。第三，得分正确性：双线性验证保证任何篡改都会被检测。第四，执行完整性：Merkle树保证服务器执行了完整的束搜索。

论文给出了四个主要安全定理。定理1保证索引和查询的机密性，基于高熵填充和变换的不可区分性。定理2保证陷阱门的不可关联性，因为随机分裂使碰撞概率可忽略。定理3保证得分正确性，任何篡改都会违反验证等式。定理4保证执行完整性，基于哈希函数的抗碰撞性。

这些定理共同保证了方案的全面安全性。
-->

---
layout: two-cols-header
---

## 实验评估：准确率对比

::left::

### 实验设置

**数据集**：
- CIFAR-100：50,000张图像，100个文本查询
- Caltech256：30,607张图像，257个文本查询

**特征提取**：CLIP (ViT-B/32)，512维特征，单位球面归一化

**参数**：
- 树参数：$k=10$，$s_{\min}=20$
- 束大小：$\beta \in \{1, 3, 7, 10\}$
- 无压缩（$k_{\text{ratio}}=0$）

**基线方法**：
- Cross-Model-SE：LSH方案（64表，128维哈希）
- Linear Search：暴力线性扫描
- MU-TEIR、PITR：仅比较时间（特征不同）

::right::

<div class="mt-2">
  <img src="/figures/paper_accuracy_comparison.png" alt="准确率对比" class="w-full">
  <div class="text-xs text-gray-500 text-center mt-1">图4：不同方案的Recall@1/5/10对比。VCSE-HST (β=10)匹配Cross-Model-SE的90% R@1。</div>
</div>

### 主要结果（CIFAR-100）

| 方案 | R@1 | R@5 | R@10 | 搜索时间 |
|------|-----|-----|------|---------|
| Cross-Model-SE | 90% | 97% | 98% | 57.5ms |
| Linear Search | 90% | 97% | 98% | 144.4ms |
| **VCSE-HST (β=3)** | **83%** | **96%** | **97%** | **2.9ms** |
| **VCSE-HST (β=7)** | **89%** | **97%** | **98%** | **6.4ms** |
| **VCSE-HST (β=10)** | **90%** | **97%** | **99%** | **7.7ms** |

<div class="mt-3 p-3 bg-green-50 rounded text-sm">
<strong>关键发现</strong>：β=10时匹配最佳准确率且快7.5倍；β=3时仅损失7%准确率但快19.7倍！
</div>

<!--
现在我们来看实验评估。首先是准确率对比。

实验在两个大规模数据集上进行：CIFAR-100有50,000张图像和100个文本查询，Caltech256有30,607张图像和257个查询。我们使用CLIP的ViT-B/32模型提取512维特征，并归一化到单位球面。

树参数设置为k=10分支、最小簇大小20。我们测试了不同的束大小，从1到10。实验中不使用维度压缩，以聚焦于索引和搜索算法本身。

基线方法包括Cross-Model-SE（LSH方案，需要64个哈希表）、线性扫描，以及MU-TEIR和PITR（仅比较时间，因为特征提取方法不同）。

右图展示了不同方案在Recall@1、Recall@5和Recall@10上的表现。可以看到，VCSE-HST在束大小为10时，完全匹配了Cross-Model-SE的90% Recall@1，在Recall@5和Recall@10上甚至略优。

表格展示了详细数据。Cross-Model-SE达到90% R@1，但搜索时间是57.5毫秒。线性扫描准确率相同但更慢，需要144.4毫秒。

VCSE-HST的表现非常出色。束大小为3时，R@1是83%，虽然比基线低7个百分点，但搜索时间只有2.9毫秒，实现了19.7倍加速！束大小为7时，R@1恢复到89%，时间6.4毫秒，9倍加速。束大小为10时，R@1达到90%，完全匹配基线，时间7.7毫秒，7.5倍加速。

这个结果证明了束大小提供了灵活的精度-效率权衡。对于高吞吐场景，可以用小束快速检索；对于高精度场景，可以用大束匹配最佳性能。
-->

---
layout: two-cols-header
---

## 束大小权衡分析

::left::

<div class="mt-2">
  <img src="/figures/paper_beam_accuracy.png" alt="束大小与准确率" class="w-full">
  <div class="text-xs text-gray-500 text-center mt-1">图5：Top-1一致率随束大小增长（无压缩设置）</div>
</div>

<div class="mt-4">
  <img src="/figures/paper_beam_time.png" alt="束大小与搜索时间" class="w-full">
  <div class="text-xs text-gray-500 text-center mt-1">图6：搜索时间随束大小亚线性增长（对数尺度）</div>
</div>

::right::

### 关键观察

**准确率边际递减**：
- $\beta=1 \to 3$：一致率从~45%跳升至70%（+25%）
- $\beta=3 \to 7$：一致率从70%升至86%（+16%）
- $\beta=7 \to 10$：一致率从86%升至90%（+4%）

边际收益递减明显，$\beta=10$后继续增大意义不大。

**时间亚线性增长**：
- $\beta=3$：2.9ms
- $\beta=7$：6.4ms（2.2倍）
- $\beta=10$：7.7ms（1.2倍）

由于早停机制（到达叶节点），时间增长慢于束大小增长。

### 最佳配置建议

<div class="mt-4 p-3 bg-blue-50 rounded text-sm">
<strong>高吞吐场景</strong>：使用$\beta=3$，2.9ms/查询，83% R@1
</div>

<div class="mt-3 p-3 bg-green-50 rounded text-sm">
<strong>高精度场景</strong>：使用$\beta=10$，7.7ms/查询，90% R@1
</div>

<div class="mt-3 p-3 bg-purple-50 rounded text-sm">
<strong>平衡场景</strong>：使用$\beta=7$，6.4ms/查询，89% R@1
</div>

<!--
束大小是VCSE-HST最重要的可调参数。左侧两张图分别展示了束大小对准确率和搜索时间的影响。

上图显示top-1一致率（与Cross-Model-SE的一致程度）随束大小的变化。我们观察到明显的边际递减效应。从束大小1到3，一致率从约45%跳升至70%，增加了25个百分点，收益巨大。从3到7，增加16个百分点至86%，收益仍然显著。但从7到10，只增加了4个百分点至90%。这说明束大小10基本达到了饱和，继续增大意义不大。

下图展示搜索时间的亚线性增长。束大小3时只需2.9毫秒，增加到7时需要6.4毫秒，大约2.2倍。但从7增加到10，时间只增加了1.2倍至7.7毫秒。这种亚线性增长得益于早停机制：当束中的节点都到达叶节点时，搜索就会提前终止，不需要继续扩展。

基于这些观察，我们给出最佳配置建议。对于高吞吐场景，比如实时推荐系统，建议使用束大小3，每次查询只需2.9毫秒，虽然R@1是83%，但对于召回阶段已经足够。对于高精度场景，比如医学图像检索，建议使用束大小10，虽然时间增加到7.7毫秒，但R@1达到90%，完全匹配最佳性能。对于平衡场景，束大小7是一个很好的中间选择，6.4毫秒时间获得89%准确率。

这种灵活的参数化设计使VCSE-HST能够适应不同应用场景的需求。
-->

---
layout: two-cols-header
---

## 验证开销分析

::left::

<div class="mt-2">
  <img src="/figures/paper_merkle_time_breakdown.png" alt="验证时间分解" class="w-full">
  <div class="text-xs text-gray-500 text-center mt-1">图7：每查询延迟分解（搜索+验证）。验证开销占总时间的小部分。</div>
</div>

<div class="mt-4">
  <img src="/figures/paper_merkle_index_time.png" alt="索引构建时间" class="w-full">
  <div class="text-xs text-gray-500 text-center mt-1">图8：Cross-Model-SE vs VCSE-HST+Merkle索引构建时间（ms）。Merkle哈希增加适度开销。</div>
</div>

::right::

### Merkle验证开销

**查询时验证**：
- $\beta=1$：~0.5ms验证开销
- $\beta=3$：~1.5ms验证开销
- $\beta=10$：~4ms验证开销

验证时间随束大小近线性增长，因为需要验证的节点数正比于$\beta$。

**索引构建开销**：
- CIFAR-100：Merkle哈希计算增加约8%构建时间
- Caltech256：增加约6%构建时间

自底向上哈希计算是一次性开销，后续查询可重复使用。

### 得分验证开销

**双线性验证**：
- 每个返回文档需要3次内积计算（$c_1, c_2$和验证）
- Top-10结果验证总计<1ms（向量维度512）

**总验证开销**：得分验证 + Merkle验证 = ~5ms (@$\beta=10$)

<div class="mt-4 p-3 bg-yellow-50 rounded text-sm">
<strong>结论</strong>：即使加上双重验证机制，VCSE-HST (β=10)总时间~12ms，仍比Cross-Model-SE (57.5ms)快4.8倍！验证的安全收益远超其开销成本。
</div>

<!--
可验证性是本文的重要贡献，但我们也需要评估验证机制的开销。

左侧两张图分别展示了查询时和索引构建时的开销分解。

上图展示了每次查询的延迟分解，分为搜索时间和验证时间两部分。可以看到，验证时间随束大小增长，但始终占总时间的较小部分。束大小1时验证只需约0.5毫秒，束大小10时验证需要约4毫秒。这是因为需要验证的节点数正比于束大小。

下图比较了Cross-Model-SE和VCSE-HST加Merkle的索引构建时间。在CIFAR-100上，增加Merkle哈希计算使构建时间增加约8%，在Caltech256上增加约6%。这个开销是可以接受的，因为索引构建是一次性的，而查询是重复的。

对于得分验证，双线性验证机制为每个返回文档增加了3次内积计算：两次计算c1和c2，一次计算验证等式。但由于向量维度只有512，这个开销很小，Top-10结果的得分验证总计不到1毫秒。

综合来看，总验证开销约5毫秒（束大小10时）。即使加上这个开销，VCSE-HST的总时间约12毫秒，仍然比Cross-Model-SE的57.5毫秒快4.8倍！

这个结果非常重要：它表明我们可以在几乎不牺牲效率的前提下，获得强大的可验证性保证。验证机制带来的安全收益远远超过其开销成本，使VCSE-HST成为一个兼具效率和安全性的实用方案。
-->

---
layout: two-cols-header
---

## 局限性与未来工作

::left::

### 当前局限性

<div class="space-y-3">
  <div class="bg-red-50 p-3 rounded">
    <h4 class="font-semibold text-red-800 text-sm mb-1">1. 模式泄露</h4>
    <p class="text-xs">方案泄露访问模式（返回哪些文档）和搜索模式（访问哪些节点）。保护需要ORAM等技术，开销巨大。</p>
  </div>

  <div class="bg-orange-50 p-3 rounded">
    <h4 class="font-semibold text-orange-800 text-sm mb-1">2. 静态索引</h4>
    <p class="text-xs">当前方案仅支持静态数据，不支持动态更新。添加/删除文档需要重建索引树。</p>
  </div>

  <div class="bg-yellow-50 p-3 rounded">
    <h4 class="font-semibold text-yellow-800 text-sm mb-1">3. 束搜索近似性</h4>
    <p class="text-xs">Merkle验证仅保证束搜索被正确执行，不保证全局最优。束大小小时可能错过真正top-k结果。</p>
  </div>

  <div class="bg-purple-50 p-3 rounded">
    <h4 class="font-semibold text-purple-800 text-sm mb-1">4. 依赖CLIP模型</h4>
    <p class="text-xs">检索准确率受限于CLIP的零样本能力。模型更新需要重新提取特征和重建索引。</p>
  </div>
</div>

::right::

### 未来研究方向

<div class="space-y-3">
  <div class="bg-blue-50 p-3 rounded">
    <h4 class="font-semibold text-blue-800 text-sm mb-1">1. 动态更新支持</h4>
    <p class="text-xs">扩展方案支持前向安全的动态更新，允许增量插入/删除文档而无需重建整树。探索局部重平衡策略。</p>
  </div>

  <div class="bg-green-50 p-3 rounded">
    <h4 class="font-semibold text-green-800 text-sm mb-1">2. 自适应束搜索</h4>
    <p class="text-xs">根据查询难度自动调整束大小：简单查询用小束，困难查询用大束。基于置信度或多样性指标动态决策。</p>
  </div>

  <div class="bg-indigo-50 p-3 rounded">
    <h4 class="font-semibold text-indigo-800 text-sm mb-1">3. 混合索引结构</h4>
    <p class="text-xs">结合层次树与LSH的优势：顶层用树提供粗粒度划分，底层用LSH加速精确匹配。在超大规模数据集（100K+）上验证。</p>
  </div>

  <div class="bg-pink-50 p-3 rounded">
    <h4 class="font-semibold text-pink-800 text-sm mb-1">4. 多模态扩展</h4>
    <p class="text-xs">扩展至音频、视频等更多模态。探索模态特定的索引优化和统一的可验证检索框架。</p>
  </div>

  <div class="bg-teal-50 p-3 rounded">
    <h4 class="font-semibold text-teal-800 text-sm mb-1">5. 隐私增强技术</h4>
    <p class="text-xs">研究轻量级访问模式隐藏技术，在可接受开销下减少泄露。探索差分隐私与可搜索加密的结合。</p>
  </div>
</div>

<!--
任何研究工作都有其局限性。VCSE-HST也不例外。让我们诚实地讨论当前的局限和未来的改进方向。

首先是模式泄露问题。和大多数实用SSE方案一样，我们的方案会泄露访问模式和搜索模式。云服务器知道返回了哪些文档、访问了哪些树节点。要完全隐藏这些模式需要ORAM技术，但开销非常大。这是效率和隐私的权衡。

第二，当前方案仅支持静态索引。如果要添加或删除文档，需要重建索引树。这在数据频繁变化的场景下不太实用。支持动态更新需要精心设计。

第三，束搜索本身是近似算法。Merkle验证只能保证束搜索被正确执行，不能保证全局最优。当束大小较小时，可能会错过真正的top-k结果。这是设计上的取舍。

第四，方案的准确率依赖于CLIP模型的零样本能力。如果CLIP更新了，需要重新提取所有特征并重建索引。

针对这些局限，我们提出五个未来研究方向。

第一，支持动态更新。研究前向安全的增量更新机制，允许插入删除文档而无需重建整树。可以探索局部重平衡策略，只更新受影响的子树。

第二，自适应束搜索。根据查询难度动态调整束大小。简单查询用小束快速返回，困难查询用大束保证准确率。可以基于置信度分数或候选多样性来决策。

第三，混合索引结构。结合树和LSH的优势：顶层用树做粗粒度划分，底层用LSH加速。在超大规模数据集上可能更有效。

第四，多模态扩展。将方案扩展到音频、视频等更多模态，研究模态特定的优化和统一的可验证框架。

第五，增强隐私保护。研究轻量级的访问模式隐藏技术，在可接受开销下减少泄露。也可以探索差分隐私与可搜索加密的结合。

这些方向都很有挑战性，也很有意义。
-->

---
layout: default
---

## 总结

<br>

### VCSE-HST核心贡献

<div class="grid grid-cols-2 gap-6 mt-4">
  <div class="bg-blue-50 p-4 rounded-lg">
    <h4 class="font-semibold text-blue-800 mb-2">1. 高效索引结构</h4>
    <p class="text-sm">层次k叉球面树（k=10）将树深度降至3-4层，提供细粒度语义划分，显著优于二叉树（16层）。</p>
  </div>

  <div class="bg-green-50 p-4 rounded-lg">
    <h4 class="font-semibold text-green-800 mb-2">2. 灵活束搜索</h4>
    <p class="text-sm">束搜索避免贪心搜索的局部最优，提供可调的精度-效率权衡。β=10时90% R@1，β=3时83% R@1但快19.7倍。</p>
  </div>

  <div class="bg-purple-50 p-4 rounded-lg">
    <h4 class="font-semibold text-purple-800 mb-2">3. 双重验证机制</h4>
    <p class="text-sm">双线性认证保证得分正确性，Merkle树承诺保证执行完整性。验证开销仅~5ms，安全收益远超成本。</p>
  </div>

  <div class="bg-orange-50 p-4 rounded-lg">
    <h4 class="font-semibold text-orange-800 mb-2">4. 卓越实验性能</h4>
    <p class="text-sm">CIFAR-100（50K图像）：90% R@1，比Cross-Model-SE快7.5倍。Caltech256（30K图像）：同样性能优势。</p>
  </div>
</div>

<div class="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg text-center">
  <p class="text-lg font-bold text-gray-800 mb-2">VCSE-HST：首个同时实现高效率和强可验证性的跨模态可搜索加密方案</p>
  <p class="text-sm text-gray-600">为云端加密多媒体数据的安全检索提供了实用解决方案</p>
</div>

<!--
让我总结一下VCSE-HST的核心贡献。

第一，我们提出了层次k叉球面树索引结构。通过k=10分支的球面k-means递归构建，将树深度从二叉树的16层降至3-4层，大幅减少累积误差，提供了细粒度的语义划分。

第二，我们设计了束搜索算法。通过维护多条候选路径，避免了贪心搜索的局部最优问题，并提供了灵活的精度-效率权衡。束大小10时达到90%准确率，束大小3时仅损失7%准确率但实现19.7倍加速。

第三，我们实现了双重验证机制。双线性认证保证返回得分的数值正确性，Merkle树承诺保证搜索执行的完整性。两者结合提供了全面的可验证性保证，而开销仅约5毫秒。

第四，实验验证了方案的卓越性能。在CIFAR-100的50,000张图像和Caltech256的30,000张图像上，我们达到了90%的Recall@1，比最先进的LSH方案快7.5倍。

综合来看，VCSE-HST是首个同时实现高效率和强可验证性的跨模态可搜索加密方案，为云端加密多媒体数据的安全检索提供了实用的解决方案。
-->

---
layout: end
---

# 谢谢！

## 欢迎提问与讨论

<!--
我的分享就到这里，感谢大家的聆听！欢迎提问和讨论。
-->
