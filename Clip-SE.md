---
theme: seriph
background: /image/slides/image.png
title: 'An Efficient and Privacy-Preserving Cross-Modal Retrieval Scheme for Encrypted Data in the Cloud'
info: |
  ## 高效隐私保护的云端加密数据跨模态检索方案
  基于CLIP和可搜索加密的创新方法
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

# An Efficient and Privacy-Preserving Cross-Modal Retrieval Scheme for Encrypted Data in the Cloud

## 高效隐私保护的云端加密数据跨模态检索方案

<div class="pt-12">
  <span class="px-2 py-1 font-semibold">汇报人: Your Name</span>
</div>

<div class="pt-8 text-sm">
  Wei Jiang et al. (Chinese Academy of Sciences, 2024)
</div>

<!--
大家好，今天我要分享的论文是《An Efficient and Privacy-Preserving Cross-Modal Retrieval Scheme for Encrypted Data in the Cloud》，这是中科院信工所2024年发表的一篇关于云端加密数据隐私保护跨模态检索的重要论文。
-->

---
layout: default
hideInToc: true
---

# 研究意义：隐私保护与智能检索的完美结合

- **云计算的普及**：企业和个人越来越多地将多媒体数据外包到云平台，享受强大的存储和计算能力。
- **隐私泄露风险**：传统明文跨模态检索在云环境中不可避免地导致隐私泄露。
- **技术空白**：现有可搜索加密方案主要解决文本到文本或图像到图像检索，跨模态检索的隐私保护研究相对空白。
- **CLIP的启发**：CLIP模型的成功为跨模态理解提供了强大的特征提取能力。
- **创新结合**：本论文首次将CLIP、局部敏感哈希(LSH)和对称可搜索加密(SSE)相结合，实现了安全高效的跨模态检索。

<!--
在正式开始介绍论文之前，我想先解释一下这项研究的重要意义。随着云计算的普及，越来越多的企业和个人选择将数据外包到云平台。但这也带来了隐私泄露的风险。虽然CLIP等明文跨模态检索技术已经非常成熟，但直接应用到云环境中会暴露用户的隐私数据。现有的可搜索加密技术主要针对单模态检索，跨模态检索的隐私保护还是一个相对空白的领域。这篇论文的创新之处在于，它首次将CLIP的强大特征提取能力与多种密码学技术相结合，为云端跨模态检索提供了一个既安全又高效的解决方案。
-->

---
layout: default
hideInToc: true

---

# 目录
<Toc :columns='2'/>

<!--
今天我的分享将围绕这六个部分展开。首先我们会了解研究背景和面临的挑战，然后深入解析这个创新方案的核心方法，包括如何结合CLIP、LSH和SSE。接着介绍系统模型和威胁模型。之后分析方案的安全性和实验结果。最后进行总结与展望。
-->

---
layout: section
---

# 研究背景与挑战

---
layout: two-cols-header
---
## 云端跨模态检索面临的挑战

::left::

### 隐私保护的迫切需求

- **数据外包风险**：用户将图像和文本数据外包到云端，面临隐私泄露风险
- **检索过程暴露**：传统检索会暴露用户查询意图和数据内容
- **法律法规要求**：GDPR等法规对数据隐私保护提出严格要求
- **用户信任危机**：隐私泄露事件频发，用户对云服务的信任度下降

*云端数据处理的便利性与隐私保护之间存在根本性矛盾。*

::right::

### 技术挑战与局限

- **现有方案局限**：大多数可搜索加密方案仅支持单模态检索
- **效率与准确性平衡**：加密处理往往导致检索效率和准确性下降
- **密钥管理复杂**：多用户环境下的密钥管理负担沉重
- **语义对齐困难**：加密状态下难以实现跨模态语义对齐

*需要一种既能保护隐私又能保持高效准确检索的创新方案。*

<!--
在介绍具体方案之前，我们先来看看云端跨模态检索面临的主要挑战。一方面，随着云计算的普及，用户享受到了强大的存储和计算能力，但同时也面临着隐私泄露的风险。无论是用户的查询内容还是存储的数据，都可能被云服务提供商获取。另一方面，现有的技术方案也存在局限性。大多数可搜索加密方案只能处理单模态数据，而跨模态检索需要在保持语义对齐的同时进行加密处理，这在技术上极具挑战性。此外，如何在保护隐私的前提下保持检索的效率和准确性，也是一个需要解决的关键问题。
-->

---
layout: default
---

## 现有方案的不足

<br>

### 主要问题分析

- **SCMR方案**：使用Paillier同态加密，但服务器端匹配过程引入的随机性导致查询结果准确性较低
- **PPCMR方案**：采用转置密码加密，但密钥数量等于用户文件数量，密钥管理负担沉重；难以在加密状态下对齐图文语义
- **PITR方案**：使用HNSW算法生成多层图结构索引，用户本地计算负担大，不适用于大数据场景

<br>

**本文目标：** <u>设计一个高效、安全、实用的云端跨模态检索方案，在保护隐私的同时实现准确快速的检索。</u>

<!--
现有的隐私保护跨模态检索方案虽然在一定程度上解决了隐私问题，但都存在明显的不足。SCMR方案虽然使用了Paillier同态加密来保护隐私，但由于加密过程中引入的随机性，导致最终的查询结果准确性不高。PPCMR方案的问题在于密钥管理复杂，每个用户文件都需要一个单独的密钥，这在大规模应用中是不现实的。PITR方案虽然精度较高，但其多层图结构索引需要用户在本地生成，计算负担太重。基于这些问题，本文的目标是设计一个既高效又安全的跨模态检索方案。
-->

---
layout: section
---

# 核心方法：创新的三层加密架构

---
layout: default
---

## 系统整体架构

<div class="mt-6">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2025-09-20/14d62f6a-cd31-4ba1-8559-004c76699681/4b54b44966dbcab05f40169586f9e8c021d1bd9c36eab15cfea84a35a2224e82.jpg" alt="系统模型" class="w-5/12 mx-auto">
  <div class="text-center text-sm text-gray-500 mt-2">图1：系统架构模型</div>
</div>

<div class="grid grid-cols-3 gap-6 mt-4">
  <div class="bg-blue-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-blue-800 mb-3">数据所有者 (DO)</h3>
    <ul class="text-sm space-y-2">
      <li>生成方案所需的密钥</li>
      <li>使用CLIP提取特征</li>
      <li>构建两层安全索引</li>
      <li>加密数据并外包到云端</li>
    </ul>
  </div>

  <div class="bg-green-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-green-800 mb-3">数据用户 (DU)</h3>
    <ul class="text-sm space-y-2">
      <li>从DO获取密钥</li>
      <li>使用CLIP提取查询特征</li>
      <li>生成加密陷阱门</li>
      <li>解密并获取检索结果</li>
    </ul>
  </div>

  <div class="bg-orange-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-orange-800 mb-3">云服务器 (CS)</h3>
    <ul class="text-sm space-y-2">
      <li>存储加密索引和数据</li>
      <li>接收用户陷阱门</li>
      <li>执行加密检索算法</li>
      <li>返回加密检索结果</li>
    </ul>
  </div>
</div>

<!--
让我们来看看这个方案的整体架构。系统模型包含三个主要实体：数据所有者、数据用户和云服务器。数据所有者负责整个系统的初始化，生成各种密钥，使用CLIP提取数据特征，构建两层安全索引，并将加密后的数据上传到云端。数据用户从数据所有者那里获得必要的密钥，可以对云端的加密数据进行搜索。云服务器提供存储和计算服务，但在整个过程中只能看到加密后的数据，无法获取任何明文信息。这种三方架构设计既保证了数据的安全性，又充分利用了云计算的强大能力。
-->

---
layout: two-cols-header
---

## 核心技术组件

给定用户图像集 $X = \{x_i\}_{i=1}^n$ 和查询文本 $q$：

::left::

### CLIP特征提取
- **图像特征**：$f_i = \text{CLIP.Extract}(x_i)$
- **文本特征**：$f_q = \text{CLIP.Extract}(q)$
- **语义对齐**：映射到统一向量空间
- **维度**：512维归一化特征向量

### LSH哈希分桶
- **哈希函数**：$H(f) = \lfloor\frac{A \times f + b}{r}\rfloor$
- **参数设置**：$A \in \mathbb{R}^{B \times D}$，$B=128$
- **分桶策略**：将128位哈希码分为64段
- **快速过滤**：大幅减少候选集规模

::right::

### 两层加密索引
- **第一层**：SSE加密倒排索引
- **第二层**：Secure kNN加密特征
- **并行检索**：多个SSE索引并行搜索
- **精确排序**：kNN计算加密内积

### 工作流程
**工作流程：** CLIP特征提取 → LSH哈希分桶 → SSE加密索引生成 → Secure kNN特征加密 → 云端上传 → 加密检索 → 结果解密

<!--
现在我们来详细看看这个方案的核心技术组件。整个方案巧妙地结合了三种关键技术：首先是CLIP特征提取。我们使用预训练的CLIP模型在本地提取图像和文本的512维特征向量，这确保了跨模态语义的对齐。接下来是LSH哈希分桶。我们使用E2LSH算法将特征向量映射到128位的哈希码，然后将这个哈希码分成64段，每段作为一个独立的关键字。这种设计可以快速过滤掉大量不相关的数据。最后是两层加密索引的构建。第一层使用SSE对每个哈希段构建加密的倒排索引，第二层使用Secure kNN对原始特征进行加密。检索时，先通过第一层快速筛选候选集，再通过第二层进行精确排序。这种多层架构设计的精妙之处在于，它在保护隐私的同时，还能保持高效的检索性能。
-->

---
layout: two-cols-header
---

## 局部敏感哈希 (LSH) 详解

::left::

### E2LSH算法原理

**哈希函数：**
$$H(f) = \left\lfloor\frac{A \times f + b}{r}\right\rfloor$$

**参数说明：**
- $A \in \mathbb{R}^{B \times D}$：标准正态分布矩阵
- $b$：$[0,r]$内均匀分布的随机向量
- $r$：分桶宽度参数
- $B=128$：哈希码长度

::right::

### 分桶策略

**哈希码分段：**
- 128位哈希码 → 64个独立段
- 每段长度：$\lfloor\frac{128}{64}\rfloor = 2$位
- 生成64个倒排索引：$I = \{I_j\}_{j=1}^{64}$
- 关键字：第j段的哈希值
- 值：具有相同哈希值的图像ID集合

<div class="mt-4">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2025-09-20/14d62f6a-cd31-4ba1-8559-004c76699681/475b42ab9a31f455b022231eafdedf63a75db122d4d14964ea1ac3f0d997b7fe.jpg" alt="LSH倒排索引示例" class="w-8/12 mx-auto">
  <div class="text-xs text-gray-500 text-center mt-2">图2：LSH倒排索引构建示例</div>
</div>

<!--
让我们深入了解LSH在这个方案中的关键作用。LSH是解决高维数据近似最近邻搜索问题的经典算法，它的核心思想是将相似的向量映射到同一个哈希桶中。在我们的方案中，使用E2LSH算法将CLIP提取的512维特征向量映射为128位的整数哈希码。这个过程通过一个随机投影矩阵A和偏移向量b来实现，参数r控制分桶的粒度。更重要的创新在于哈希码的分段策略。我们将128位的哈希码分成64个独立的段，每段2位。每个段都构建一个独立的倒排索引，其中关键字是该段的哈希值，值是具有相同哈希值的所有图像ID。这种设计的优势在于：第一，可以并行搜索多个索引，提高检索效率；第二，即使部分段不匹配，其他段仍可能匹配，提高了召回率；第三，为后续的SSE加密奠定了基础。
-->

---
layout: two-cols-header
---

## 对称可搜索加密 (SSE) 与安全kNN

::left::

### SSE第一层索引

**算法流程：**
- **密钥生成：** $k_{SSE} = \{k_{SSE,j}\}_{j=1}^{64}$
- **索引加密：** $\tilde{I}_j^1 = \text{SSE.BuildIndex}(I_j, k_{SSE,j})$
- **陷阱门生成：** $\tilde{T}_j^1 = \text{SSE.GenTrapdoor}(h_{q,j}, k_{SSE,j})$
- **并行搜索：** 64个索引并行查询

**安全保证：**
只泄露搜索模式，不泄露语义信息

::right::

### Secure kNN第二层

**密钥生成：**
$$k_{kNN} = \{M_1, M_2, s\}$$

**特征加密：**
$$\tilde{f}_i = \{M_1^T f_{i,1}, M_2^T f_{i,2}\}$$

**查询加密：**
$$\tilde{q} = \{M_1^{-1} q_1, M_2^{-1} q_2\}$$

**相似度计算：**
$$\text{Sim} = \tilde{f}_i \cdot \tilde{q} = f_i \cdot q$$

<div class="mt-4 p-3 bg-gray-100 rounded text-sm">
<strong>两层协同工作：</strong>第一层SSE快速筛选候选集，第二层Secure kNN在候选集内精确排序，实现了效率与准确性的平衡。
</div>

<!--
现在我们来看看两层加密索引的具体实现。第一层使用对称可搜索加密（SSE）。对于LSH生成的64个倒排索引，我们使用64个独立的SSE密钥分别进行加密。用户查询时，需要为每个哈希段生成相应的陷阱门，然后云服务器可以并行搜索这64个加密索引。SSE的优势在于它只泄露搜索模式，也就是哪些查询是相同的，但不会泄露查询的具体内容。第二层使用安全k近邻（Secure kNN）算法。这个算法通过随机矩阵分裂技术来保护向量的隐私。具体来说，每个原始特征向量会被分裂成两个随机向量，然后分别用两个可逆矩阵进行加密。查询向量也经过类似的处理。最精妙的是，这种加密方式保持了内积的不变性。也就是说，两个加密向量的内积等于原始向量的内积，这使得我们可以在加密状态下直接计算相似度，而不需要解密。两层索引协同工作：第一层快速过滤掉大量无关数据，第二层在较小的候选集内进行精确排序。这种设计既保证了效率，又保证了准确性。
-->

---
layout: two-cols-header
---

## 完整的检索流程

::left::

### 索引构建阶段
1. **特征提取**：使用CLIP提取图像特征
2. **LSH哈希**：生成128位哈希码并分成64段
3. **倒排索引**：为每段构建倒排索引
4. **SSE加密**：加密64个倒排索引
5. **kNN加密**：加密原始特征向量
6. **数据上传**：将加密索引和数据上传云端

### 查询检索阶段
1. **特征提取**：使用CLIP提取查询文本特征
2. **LSH哈希**：生成查询的哈希码并分段
3. **陷阱门生成**：为每段生成SSE陷阱门和kNN查询
4. **第一轮检索**：并行搜索64个SSE索引
5. **候选集合并**：合并所有匹配的图像ID
6. **第二轮排序**：使用Secure kNN计算相似度
7. **Top-k返回**：返回最相似的k个加密图像

::right::

<div class="mt-4">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2025-09-20/14d62f6a-cd31-4ba1-8559-004c76699681/ddd96773dc9c28616e142faccbdf633a96f462b7c008308877cc5e282ee845cd.jpg" alt="检索流程示例" class="w-full">
  <div class="text-xs text-gray-500 text-center">图3：完整检索流程示例</div>
</div>

<!--
让我们通过一个完整的例子来理解整个检索流程。在索引构建阶段，数据所有者首先使用CLIP提取所有图像的特征向量，然后使用LSH算法生成哈希码。这些哈希码被分成64段，每段构建一个倒排索引。接下来，使用64个独立的SSE密钥对这些倒排索引进行加密，同时使用Secure kNN算法对原始特征向量进行加密。最后，将所有加密后的索引和数据上传到云端。在查询检索阶段，用户首先提取查询文本的CLIP特征，生成相应的哈希码。然后为每个哈希段生成SSE陷阱门，并为原始特征生成kNN查询向量。云服务器接收到这些加密查询后，并行搜索64个SSE索引，获得第一轮的候选结果。最后，使用Secure kNN算法计算候选结果与查询的相似度，返回Top-k个最相似的结果。这个流程的关键在于，整个过程中云服务器只能看到加密后的数据和查询，无法获取任何明文信息，从而保护了用户的隐私。
-->

---
layout: section
---

# 系统模型与威胁分析

---
layout: default
---

## 威胁模型与安全目标

<div class="grid grid-cols-2 gap-6 mt-4">
  <div class="bg-red-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-red-800 mb-3">威胁模型假设</h3>
    <ul class="text-sm space-y-2">
      <li><strong>诚实但好奇的云服务器</strong>：忠实执行协议但试图推断隐私信息</li>
      <li><strong>完全诚实的DO和DU</strong>：不会向云服务器泄露密钥</li>
      <li><strong>安全通信信道</strong>：DO和DU之间的通信是安全可靠的</li>
      <li><strong>密文攻击模型</strong>：攻击者只能获得密文数据和陷阱门</li>
    </ul>
  </div>

  <div class="bg-green-50 p-4 rounded-lg">
    <h3 class="text-lg font-bold text-green-800 mb-3">安全目标</h3>
    <ul class="text-sm space-y-2">
      <li><strong>文件隐私</strong>：保护外包到云端的加密文件内容</li>
      <li><strong>陷阱门隐私</strong>：防止从陷阱门推断用户查询语义</li>
      <li><strong>索引隐私</strong>：保护加密索引中的语义内容</li>
      <li><strong>查询隐私</strong>：隐藏用户的查询模式和意图</li>
    </ul>
  </div>
</div>

<div class="mt-6 p-4 bg-blue-50 rounded-lg">
  <h3 class="font-bold text-blue-800 mb-2">安全分析总结</h3>
  <div class="text-sm">
    <p><strong>文件隐私：</strong>使用AES加密保护，密钥sk由DO和DU保管，云服务器无法解密。</p>
    <p><strong>陷阱门隐私：</strong>基于Secure kNN和SSE的安全性，在密文攻击模型下，云服务器无法从陷阱门推断原始查询语义。</p>
    <p><strong>索引隐私：</strong>SSE只泄露访问模式（查询的文件及其数量），但难以从中提取有意义的语义信息。</p>
  </div>
</div>

<!--
在威胁模型方面，我们采用了广泛接受的"诚实但好奇"假设。这意味着云服务器会忠实地执行协议，但同时会尝试从接收到的数据中推断用户的隐私信息。我们假设数据所有者和数据用户是完全诚实的，不会与云服务器串通泄露密钥。我们的安全目标包括四个方面的隐私保护：首先是文件隐私。所有上传到云端的图像文件都使用AES算法进行加密，只要密钥不泄露，云服务器就无法获取文件内容。其次是陷阱门隐私。由于我们使用了Secure kNN和SSE这两种密码学技术，在密文攻击模型下，云服务器无法从接收到的陷阱门推断用户的原始查询内容。然后是索引隐私。虽然SSE会泄露一些访问模式，比如哪些文件被查询以及查询的次数，但云服务器很难从这些模式中提取有意义的语义信息。最后是查询隐私。整个检索过程都在加密状态下进行，用户的查询意图得到了有效保护。这些安全保证为用户在不可信的云环境中进行跨模态检索提供了坚实的隐私保护基础。
-->

---
layout: section
---

# 实验评估与分析

---
layout: two-cols-header
---

## 实验设置与数据集

::left::

### 实验环境
- **系统**：Ubuntu 22.04
- **CPU**：Intel Xeon Silver 4214R @2.40GHz
- **GPU**：GeForce RTX 3090
- **编程语言**：Python
- **CLIP模型**：ViT-B/32预训练模型

### 参数配置
- **哈希码维度**：B = 128
- **哈希桶大小**：r = 1.6
- **比特位数**：l = 8
- **索引分段数**：m = 64

::right::

### 数据集介绍
- **Caltech256**：
  - 257个类别，30,607张图像
  - 涵盖自然场景到人工物体
  - 广泛使用的真实世界图像数据集

- **CIFAR-100**：
  - 100个不同类别
  - 图像检索领域常用数据集
  - 对CLIP来说是零样本数据集

### 评估指标
- **效率指标**：索引构建时间、检索时间
- **准确性指标**：Top-k精确率、平均精确率(mAP)
- **对比方案**：PITR、MU-TEIR

<!--
我们的实验在标准的硬件环境下进行，使用了两个广泛认可的数据集。Caltech256包含257个类别，涵盖了从自然场景到人工物体的多种图像类型，是一个真实世界的图像数据集。CIFAR-100包含100个不同的类别，也是图像检索领域的常用数据集。这两个数据集对于CLIP来说都是零样本数据集，能够很好地测试我们方案的泛化能力。在参数设置上，我们使用128维的LSH哈希码，分成64个独立的段，每段2位。这种配置在效率和准确性之间取得了良好的平衡。我们将我们的方案与现有的PITR和MU-TEIR方案进行了全面的对比评估。
-->

---
layout: two-cols-header
---

## 效率对比分析

::left::

### 索引构建效率

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-09-20/14d62f6a-cd31-4ba1-8559-004c76699681/ef5c8c32cb97341042e77a6fb1e0e4e009ee7f9eea83b2e0b9655c3a1fef5667.jpg" alt="索引构建时间对比" class="w-full">

- **线性增长**：索引构建时间随文件数量线性增长
- **性能优势**：比PITR方案快约10%
- **并行优化**：独立倒排索引支持并行构建

::right::

### 检索效率

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-09-20/14d62f6a-cd31-4ba1-8559-004c76699681/6e793d3320d400f18704d9c2e859527bc0f7008492219fc8a22b4cec5dc43491.jpg" alt="检索时间对比" class="w-full">

- **检索速度**：比PITR快约10%
- **极大优势**：比MU-TEIR快两个数量级
- **第一层过滤**：LSH+SSE有效过滤无关图像

<div class="mt-4 p-3 bg-blue-50 rounded text-sm">
<strong>效率分析：</strong>第一层索引的并行搜索和有效过滤是性能提升的关键因素。
</div>

<!--
在效率方面，我们的方案表现出色。在索引构建阶段，我们的方案比PITR快约10%。这主要归功于我们更简单高效的索引结构和并行构建机制。64个独立的倒排索引可以并行生成加密索引，大大提高了构建速度。在检索阶段，我们的优势更加明显。与PITR相比，我们的方案快约10%，这得益于第一层LSH+SSE索引的有效过滤机制。与MU-TEIR相比，我们的优势是压倒性的，快了两个数量级。MU-TEIR在1000张图像的数据集上返回Top-5结果需要12.57秒，而我们的方案只需要几十毫秒。这种巨大的性能差异主要源于不同的技术路径。MU-TEIR使用DT-PKC技术，计算开销非常大，而我们的方案通过智能的两层索引设计，既保证了安全性，又大大提高了效率。
-->

---
layout: two-cols-header
---

## 检索精确度评估

::left::

### Top-k精确率对比

<img src="https://cdn-mineru.openxlab.org.cn/result/2025-09-20/14d62f6a-cd31-4ba1-8559-004c76699681/f20a1479e62ff19ef828bd670c3a140bc66eb5d43b614a5c4467f4bb488fe25a.jpg" alt="Top-k精确率对比" class="w-full">

- **整体优势**：在各个Top-k值上都优于MU-TEIR
- **高精确率**：即使Top-20仍保持较高精确率
- **跨模态能力**：支持文本到图像检索，MU-TEIR仅支持图像到图像

::right::

### 数据集表现

<div class="bg-green-50 p-4 rounded-lg mb-4">
<h4 class="font-bold text-green-800 mb-2">平均精确率(mAP)</h4>
<ul class="text-sm space-y-1">
<li><strong>Caltech256</strong>: 0.853</li>
<li><strong>CIFAR-100</strong>: 0.649</li>
</ul>
</div>

<div class="bg-orange-50 p-4 rounded-lg">
<h4 class="font-bold text-orange-800 mb-2">精确率下降分析</h4>
<p class="text-sm">
由于两层索引结构，LSH第一轮过滤在去除无关图像的同时，也可能过滤掉部分相关图像，导致随着k增大精确率下降速度比MU-TEIR快。
</p>
<p class="text-sm mt-2">
<strong>改进方向：</strong>增加更多SSE实例可以缓解这个问题，但需要在精确率和效率间取得平衡。
</p>
</div>

<!--
在检索精确度方面，我们的方案也表现出了很好的性能。与MU-TEIR的对比显示，我们的方案在所有Top-k值上都取得了更好的精确率。特别值得注意的是，我们的方案支持真正的跨模态检索（文本到图像），而MU-TEIR只支持图像到图像检索。在两个数据集上，我们的方案都取得了令人满意的平均精确率：Caltech256上达到0.853，CIFAR-100上达到0.649。这些结果证明了我们方案的有效性。不过，我们也观察到一个现象：随着k值的增加，我们的精确率下降速度比MU-TEIR要快一些。这是因为我们的两层索引设计导致的。LSH第一层在快速过滤大量无关图像的同时，也可能会意外地过滤掉一些相关图像，从而减少了第二层可以排序的候选集大小。这个问题可以通过增加更多的SSE实例来缓解，但这会增加计算开销。如何在精确率和效率之间找到最佳平衡点，是我们未来研究的一个重要方向。
-->

---
layout: section
---

# 总结与展望

---
layout: default
---

## 主要贡献与创新点

<div class="grid grid-cols-2 gap-8 mt-4">
  <div>
    <h3 class="text-xl font-bold text-blue-600 mb-3">技术创新</h3>
    <ul class="space-y-2">
      <li class="flex items-start">
        <span class="text-green-500 mr-2">✓</span>
        <div>
          <span class="text-sm text-gray-600">创新性地将局部敏感哈希与对称可搜索加密结合，解决跨模态检索问题</span>
        </div>
      </li>
      <li class="flex items-start">
        <span class="text-green-500 mr-2">✓</span>
        <div>
          <span class="text-sm text-gray-600">LSH+SSE快速过滤配合Secure kNN精确排序，平衡效率与准确性</span>
        </div>
      </li>
      <li class="flex items-start">
        <span class="text-green-500 mr-2">✓</span>
        <div>
          <span class="text-sm text-gray-600">充分利用CLIP的跨模态语义对齐能力，在加密状态下保持语义关系</span>
        </div>
      </li>
    </ul>
  </div>

  <div>
    <h3 class="text-xl font-bold text-green-600 mb-3">实用价值</h3>
    <ul class="space-y-2">
      <li class="flex items-start">
        <span class="text-blue-500 mr-2">★</span>
        <div>
          <span class="text-sm text-gray-600">文件、索引、查询全程加密，满足严格的隐私保护需求</span>
        </div>
      </li>
      <li class="flex items-start">
        <span class="text-blue-500 mr-2">★</span>
        <div>
          <span class="text-sm text-gray-600">支持大规模外包数据场景，具有良好的可扩展性</span>
        </div>
      </li>
      <li class="flex items-start">
        <span class="text-blue-500 mr-2">★</span>
        <div>
          <span class="text-sm text-gray-600">效率与安全性并重，具备实际部署的可行性</span>
        </div>
      </li>
    </ul>
  </div>
</div>

<div class="mt-6 p-3 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg">
  <h3 class="font-bold text-lg mb-1">核心价值</h3>
  <p class="text-sm">
    本文提出的方案是首个将CLIP、LSH和SSE技术相结合的隐私保护跨模态检索方案，
    为云计算环境下的多媒体数据隐私保护提供了一个高效、安全、实用的解决方案，
    具有重要的理论意义和实用价值。
  </p>
</div>

<!--
让我们总结一下这篇论文的主要贡献和创新点。从技术创新的角度来看，这篇论文最大的贡献是首次将局部敏感哈希与对称可搜索加密相结合来解决跨模态检索问题。这种结合不是简单的技术堆叠，而是一个精心设计的两层架构：第一层使用LSH+SSE实现快速过滤，第二层使用Secure kNN实现精确排序。更重要的是，整个方案充分利用了CLIP的强大语义对齐能力，在保护隐私的同时保持了跨模态语义关系。从实用价值的角度来看，这个方案提供了完整的隐私保护，从文件加密到索引加密再到查询加密，形成了一个完整的安全体系。它适用于大规模数据场景，具有良好的可扩展性。更重要的是，它在效率和安全性之间取得了很好的平衡，具备了实际部署的可行性。这个方案的核心价值在于，它为云计算环境下的多媒体数据隐私保护提供了一个既高效又安全的解决方案，填补了跨模态检索隐私保护领域的技术空白。
-->

---
layout: two-cols-header
---

## 局限性与未来工作

::left::

<h3>当前局限性</h3>

<div class="mt-2">
<h4 class="font-semibold text-red-800 mb-1">精确率衰减问题</h4>
<p class="text-sm mb-3">LSH第一层过滤可能误过滤相关图像，随着Top-k增大精确率下降较快</p>

<h4 class="font-semibold text-orange-800 mb-1">参数调优复杂</h4>
<p class="text-sm mb-3">LSH参数(B, r, m)的选择需要在效率和精确率间权衡，调优复杂</p>

<h4 class="font-semibold text-yellow-800 mb-1">CLIP模型依赖</h4>
<p class="text-sm">方案性能受限于CLIP模型的特征提取质量，难以适应特定领域</p>
</div>

::right::

<h3>未来研究方向</h3>

<div class="mt-2">
<h4 class="font-semibold text-green-800 mb-1">自适应参数优化</h4>
<p class="text-sm mb-3">研究自动调优LSH参数的算法，根据数据特性动态优化配置</p>

<h4 class="font-semibold text-blue-800 mb-1">多模态扩展</h4>
<p class="text-sm mb-3">扩展到音频、视频等多模态数据，构建更通用的隐私保护检索系统</p>

<h4 class="font-semibold text-purple-800 mb-1">联邦学习结合</h4>
<p class="text-sm mb-3">与联邦学习技术结合，在保护隐私的同时持续改进模型性能</p>

<h4 class="font-semibold text-indigo-800 mb-1">实际部署验证</h4>
<p class="text-sm">在真实云环境中验证方案的实用性，并针对实际需求进行优化</p>
</div>

<!--
当然，这个方案也存在一些局限性，这为未来的研究指出了方向。当前的主要局限性包括：首先是精确率衰减问题，LSH第一层过滤在提高效率的同时，可能会误过滤一些相关图像，导致随着Top-k值增大，精确率下降得比较快。其次是参数调优的复杂性，LSH的各种参数需要根据具体的数据特性进行精细调优，这增加了系统部署的复杂度。最后，方案的性能很大程度上依赖于CLIP模型的质量，对于一些特定领域的数据可能效果不够理想。基于这些局限性，我们提出了几个重要的未来研究方向：首先是自适应参数优化，研究能够根据数据特性自动调优LSH参数的算法，降低系统部署的复杂度。其次是多模态扩展，将方案扩展到音频、视频等更多模态的数据，构建一个更加通用的隐私保护检索系统。再次是与联邦学习技术的结合，这样可以在保护隐私的同时，持续改进模型的性能。最后是实际部署验证，在真实的云环境中测试方案的实用性，并根据实际需求进行进一步的优化。
-->

---
layout: end
---

# 谢谢！

## 欢迎提问与讨论

<!--
我的分享就到这里，感谢大家的聆听。这篇论文展示了一个创新的隐私保护跨模态检索方案，它巧妙地结合了CLIP、LSH和可搜索加密等技术，为云计算环境下的多媒体数据检索提供了一个既安全又高效的解决方案。欢迎大家提问和交流！
-->