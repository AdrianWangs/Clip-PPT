---
theme: seriph
background: /image/slides/image.png
title: "RemoteRAG: A Privacy-Preserving LLM Cloud RAG Service"
info: |
  ## 一种隐私保护的LLM云端RAG服务
  在保护查询隐私的同时实现高效准确的检索
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

# RemoteRAG: A Privacy-Preserving LLM Cloud RAG Service

## 一种隐私保护的LLM云端RAG服务

<div class="pt-12">
  <span class="px-2 py-1 font-semibold">汇报人: [你的名字]</span>
</div>

<!--
大家好，今天我要分享的论文是《RemoteRAG: A Privacy-Preserving LLM Cloud RAG Service》，这是一篇关于保护用户查询隐私的云端RAG服务方案。
-->

---
layout: two-cols-header
---

# 研究背景与动机

::left::

### RAG技术的兴起

- 大语言模型（LLM）存在幻觉问题
- 检索增强生成（RAG）提供可信外部知识
- 云端RAG服务（RaaS）方便用户查询
- **隐私问题**：用户查询明文上传到云端

::right::

### 现有方案的局限

**隐私忽略方案：**
- 用户查询直接暴露给云服务器
- 敏感信息（健康、财务等）泄露风险

**完全隐私方案：**
- 计算和通信开销巨大（2.72小时/1.43GB）
- 实用性受限

**我们的目标：**
- 在隐私、效率、准确性之间找到平衡

<!--
随着大语言模型的发展，RAG技术越来越重要。RAG通过检索相关文档来增强LLM的回答，减少幻觉。现在出现了云端RAG服务，用户可以很方便地提交查询获得结果。
但是，现有的方案都要求用户把查询明文上传到云端，这就带来了严重的隐私泄露风险。比如用户查询健康问题、财务状况等敏感信息。

现有的方案要么完全忽略隐私，直接把查询发给云端；要么追求完全隐私，但代价是巨大的计算和通信开销，根本无法实际使用。
所以我们需要一个方案，既能保护用户隐私，又能保证效率和准确性。
-->

---
layout: default
---

## 本文主要创新点

**(n,ε)-DistanceDP隐私定义**：首次提出在n维嵌入空间中定义的差分隐私，用隐私预算ε控制查询泄露。

**高效搜索范围限制**：通过扰动嵌入将搜索范围从全部N个文档缩小到k'个，大幅节省计算和通信成本。

**双重检索机制**：
  - **同态加密排序**：在加密域计算余弦距离
  - **两种文档获取方式**：直接检索或不经意传输（OT），根据泄露情况选择

**理论保证**：严格证明k'的选择能确保包含目标文档。

<div class="mt-3 p-2 bg-gray-50 rounded text-center text-sm">
  10^6文档规模：仅需0.67秒 + 46.66KB数据传输
  <br>
  检索准确率100%，可抵抗现有嵌入反转攻击
</div>

<!--
针对前面的问题，本文提出了RemoteRAG方案，主要有四大创新：

第一个是**隐私定义**。我们提出了(n,ε)-DistanceDP，在n维嵌入空间中定义差分隐私，用户可以通过隐私预算ε来控制查询信息的泄露程度。

第二个是**搜索范围限制**。我们不是直接在全部N个文档上做加密计算，而是先通过一个扰动后的嵌入把搜索范围缩小到k'个文档，这样后续的加密计算开销就小多了。

第三个是**双重检索机制**。先用同态加密在加密域计算余弦距离排序，然后根据泄露情况选择直接返回索引或者用不经意传输来获取文档，进一步保护隐私。

第四个是**理论保证**。我们从数学上证明了k'应该选多大，能保证目标文档一定包含在k'个文档里。

实验结果：在100万文档规模下，只需要0.67秒和46.66KB数据传输，检索准确率100%，还能抵抗现有的嵌入反转攻击。
-->

---
layout: default
---

## 系统模型

<div class="grid grid-cols-2 gap-8 items-start mt-20">
<div>

- **云服务器 (Cloud)**: 托管大量文档，提供RAG检索服务，但对半诚实好奇。
- **用户 (User)**: 提交查询，需要保护查询语义信息不泄露。
- **共享嵌入模型**: 用户和云端使用相同的嵌入模型。

威胁模型：
- 云服务器是半诚实的（遵守协议但好奇）
- 需要保护：查询嵌入、top-k文档索引

</div>
<div>

<img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/7b3742de9032533bdf003a33af174ac76f27f31794f1985999e4699f25313a87.jpg" alt="系统架构模型" class="w-10/12 mx-auto">
<div class="text-center text-xs text-gray-500 mt-1">图1：RemoteRAG流程图</div>

</div>
</div>

<!--
好的，我们来看一下RemoteRAG的系统模型。

它包含两个核心实体：**云服务器**和**用户**。

首先，**云服务器**托管了大量的文档作为RAG服务。它是半诚实的——也就是说，它会遵守我们的协议，但它会好奇用户的查询内容。

然后是**用户**，用户有一个查询，他想从云端检索相关的文档，但不想让云端知道查询的具体内容。

双方共享同一个嵌入模型，这样用户可以在本地计算查询嵌入。

在这个威胁模型下，我们需要保护两个东西：
第一，查询嵌入本身——因为现有攻击可以从嵌入恢复出原始查询文本。
第二，top-k文档的索引——因为这些文档的平均 embedding 可能很接近查询 embedding，也会泄露信息。
-->

---
layout: center
---

# 具体方案

---
layout: two-cols-header
---

## (n,ε)-DistanceDP 隐私定义

::left::

### 为什么需要新的隐私定义？

- 传统差分隐私（DP）在n维空间中不方便直接应用
- 我们需要在嵌入空间中度量隐私泄露
- 灵感来自Geo-indistinguishability

### (n,ε)-DistanceDP定义

机制K满足(n,ε)-DistanceDP当且仅当：
$$ L(K(x), K(x')) \leq \epsilon \|x - x'\| $$

其中：
- $L(\cdot,\cdot)$ 是分布间的距离
- $\|x - x'\|$ 是L2距离
- $\epsilon$ 是隐私预算

::right::

<div class="flex flex-col justify-center items-center h-full pl-2">
  <div class="mt-8 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
    <h4 class="text-blue-800 font-bold mb-2 text-sm">直观理解</h4>
    <ul class="text-sm space-y-2 text-gray-700">
      <li class="flex items-center">
        <span class="w-2 h-2 bg-gray-400 rounded-full mr-2"></span>
        <span>从扰动后的点看，真实查询和随机查询的概率差异被控制</span>
      </li>
      <li class="flex items-center">
        <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
        <span>ε越小，扰动越大，隐私保护越强</span>
      </li>
      <li class="flex items-center">
        <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
        <span>ε越大，扰动越小，可用性越好</span>
      </li>
    </ul>
  </div>
</div>

<!--
接下来介绍第一个关键技术：(n,ε)-DistanceDP。

传统的差分隐私不太方便直接用在n维嵌入空间里。我们借鉴了Geo-indistinguishability的思想，提出了(n,ε)-DistanceDP。

简单来说，这个定义保证了：从扰动后的嵌入点来看，真实的查询嵌入和另一个随机的嵌入点，它们生成这个扰动的概率差异被控制在e^(ε·距离)倍以内。

这样用户就可以通过调节隐私预算ε来平衡隐私和可用性。ε越小，扰动越大，隐私保护越强，但可能影响检索准确率；ε越大，扰动越小，可用性越好，但隐私保护弱一些。
-->

---
layout: two-cols-header
---

## 扰动生成：如何在n维空间中采样？

::left::

### 概率分布

我们使用n维拉普拉斯分布，概率密度函数：
$$ D_{n,\epsilon}(x | x_0) \propto e^{-\epsilon \|x - x_0\|} $$

### 实际采样方法（分解为两部分）

1. **径向分量 r**：
   - $r = \|x - x_0\|$，距离真实点的距离
   - 服从Gamma分布：$r \sim \text{Gamma}(n, \frac{1}{\epsilon})$
   - 期望：$\bar{r} = \frac{n}{\epsilon}$

2. **方向向量 v**：
   - 从n维单位球面上均匀采样
   - 通过独立采样标准正态分布再归一化得到

::right::

<div class="flex flex-col justify-center items-center h-full pl-4">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/8fd237ff91d62f68800c3f662d4a01ec970e6c2ccf4890b49a5a5673aa7f638b.jpg" alt="Gamma分布PDF" class="w-10/12 shadow-lg rounded-lg border border-gray-100">
  <div class="text-center text-xs text-gray-500 mt-3">图2：不同Gamma分布的概率密度函数</div>
  
  <div class="mt-4 w-10/12 bg-gray-50 p-3 rounded-lg border border-gray-200 text-sm">
    <div class="flex items-center mb-2">
      <span class="text-green-600 font-bold mr-2">关键观察</span>
    </div>
    <div class="text-gray-600 text-xs">
      维度n越高，Gamma分布越陡峭，r越集中在$\bar{r}=n/\epsilon$附近
      <br><br>
      因此可以用 $\epsilon \approx \frac{n}{r}$ 从扰动r反推隐私预算ε
    </div>
  </div>
</div>

<!--
知道了隐私定义，接下来看具体怎么生成扰动。

直接在n维空间按这个分布采样有点难，所以我们把它分解成径向分量和方向向量两部分分别采样。

径向分量r，也就是扰动点离真实点的距离，它服从Gamma分布，形状参数是n，尺度参数是1/ε。期望是n/ε。

方向向量v，就是从真实点指向扰动点的方向，从n维单位球面上均匀采样就行。

大家看右边的图，维度n越高，Gamma分布越陡峭，也就是说r越集中在期望值附近。所以实际中，我们可以近似地用ε≈n/r来从扰动大小r反推出对应的隐私预算ε。
-->

---
layout: two-cols-header
---

## 搜索范围k'的计算：如何保证不丢目标文档？

::left::

### 问题

我们用扰动后的嵌入$e_{k'}$去检索top-$k'$个文档，怎么确保这$k'$个文档里包含了原始查询$e_k$的top-$k$个目标文档？

### 几何直观

在单位球面上：
- $\alpha_k$：原始查询top-$k$文档对应的极角
- $\Delta\alpha_k$：$e_k$和$e_{k'}$之间的扰动角（≈r）
- 需要 $\alpha_{k'} = \alpha_k + \Delta\alpha_k$

::right::

<div class="flex flex-col justify-center items-center h-full">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/dc5b386358244399c87829cd96fd7ec99207108fe6cdc07ccf4f711711580e5a.jpg" alt="斜投影示意" class="w-6/12 mb-4">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/ec27a8d63be19970558bdff01ca16b3ce7e9bd7256eb301a20080fdaf478f33c.jpg" alt="正投影示意" class="w-6/12">
  <div class="text-center text-xs text-gray-500 mt-2">图3：3维投影示意</div>
</div>

<!--
现在有了扰动后的嵌入，我们用它去云端检索k'个文档。但问题是，怎么选k'才能保证原始查询的top-k目标文档一定包含在这k'个文档里？

大家看右边的图。假设原始查询是ek，扰动后的查询是ek'，它们之间的夹角是Δαk。原始查询的top-k文档对应一个极角αk。为了让这些文档都包含在ek'的检索结果里，我们需要把ek'的检索范围扩大到αk' = αk + Δαk。

这样即使查询被扰动了，目标文档也不会漏。
-->

---
layout: default
---

## 理论保证：引理1和定理1

### 引理1（k与$α_k$的关系）

假设N个嵌入均匀分布在n维单位球面上，top-k个文档对应的极角$α_k$满足：

$$ k = N \cdot \frac{\Omega_{n-1}(\pi)}{\Omega_n(\pi)} \cdot \int_0^{\alpha_k} \sin^{n-2} \theta \, d\theta $$

其中 $\Omega_n(\pi) = \frac{2\pi^{n/2}}{\Gamma(n/2)}$ 是n维单位球面的表面积。

### 定理1（k'的选择）

在引理1条件下，给定ek和ek'，扰动角为Δα_k，要确保ek'的top-k'包含ek的top-k，则：

$$ \Delta k = k' - k = N \cdot \frac{\Omega_{n-1}(\pi)}{\Omega_n(\pi)} \cdot \int_{\alpha_k}^{\alpha_{k'}} \sin^{n-2} \theta \, d\theta $$

其中 $\alpha_{k'} = \alpha_k + \Delta\alpha_k$。

<!--
把几何直观变成严谨的数学公式，就是引理1和定理1。

引理1告诉我们，在单位球面上均匀分布的假设下，给定k，怎么算出对应的极角α_k。

定理1告诉我们，加上扰动角Δα_k之后，需要多检索多少个文档（Δk），才能保证不丢目标文档。

有了这两个定理，我们就可以根据用户选择的扰动大小r（也就是Δα_k≈r），精确地计算出k'应该取多少。
-->

---
layout: two-cols-header
---

## 隐私预算ε的选择：在隐私和成本间权衡

::left::

### 两个阈值

用户通常有两个明确的阈值：

1. **隐私阈值（上界）**：
   - 随着扰动r增大，攻击效果逐渐降低（下图）
   - 当攻击效果低于用户可接受的阈值时，得到最小的r
   - 因为 $\epsilon \approx n/r$，所以这确定了**ε的最大值**

2. **成本阈值（下界）**：
   - 计算和通信成本随k'增大而增加
   - 最大可接受的k'确定了最大的Δα_k（即r）
   - 这确定了**ε的最小值**

::right::

<div class="flex flex-col justify-center items-center h-full pl-4">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/a2d2a267d5cbed6508d4b5cf1d2ad153e67003072872420e0c2bdde1beb9d907.jpg" alt="SacreBLEU-r" class="w-8/12 shadow-lg rounded-lg border border-gray-100 mb-4">
  <img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/19e2dcf1d872041679fd356c88cee2f3f16f5714dc028d9a229623af44b607ef.jpg" alt="SacreBLEU-ε" class="w-8/12 shadow-lg rounded-lg border border-gray-100">
  <div class="text-center text-xs text-gray-500 mt-2">图4：扰动r和隐私预算ε对应的SacreBLEU指标</div>
</div>

<!--
实际中用户怎么选ε呢？通常用户有两个阈值。

第一个是隐私阈值。用户能接受的最大攻击效果是多少？比如右边的图(a)，当扰动r增大，攻击效果（SacreBLEU）从50降到10。用户可以设置一个阈值，比如攻击效果必须低于30，这就对应了一个最小的r，从而确定了ε的最大值。

第二个是成本阈值。用户能接受的最大计算和通信开销是多少？这对应了一个最大的k'，从而确定了ε的最小值。

最终ε就在这两个值之间选，用户可以根据自己的偏好权衡。
-->

---
layout: two-cols-header
---

## 模块2：同态加密进行排序

::left::

### 为什么选同态加密？

- 安全多方计算通常需要三个非合谋方或可信第三方
- 全同态加密（FHE）计算开销太大
- 余弦距离只涉及线性运算，部分同态加密（PHE）就够了

### 距离度量

归一化嵌入的L2距离和余弦距离：
$$ d_{l2}(e_a, e_b) = \|e_a - e_b\| $$
$$ d_{\cos}(e_a, e_b) = 1 - \langle e_a, e_b \rangle $$

**定理2**：对于归一化向量，L2距离和余弦距离排序一致：
$$ d_{l2}(e_a, e_b) = \sqrt{2 d_{\cos}(e_a, e_b)} $$

所以只用考虑余弦距离。

::right::

### 具体流程

<div style="line-height: 1.4;">
  <div style="margin-bottom: 8px;"><strong>1. 用户端</strong>：</div>
  <ul style="margin-top: 4px; margin-bottom: 8px; padding-left: 24px;">

  - 用PHE加密查询嵌入 $e_k$，得到 $[[e_k]]$
  - 发送 $[[e_k]]$ 到云端

  </ul>
  
  <div style="margin-bottom: 8px;"><strong>2. 云端</strong>：</div>
  <ul style="margin-top: 4px; margin-bottom: 8px; padding-left: 24px;">

  - 对k'个文档中的每个嵌入e，计算加密的余弦距离：
  - $[[d_{\cos}(e_k, e)]] = 1 - \langle [[e_k]], e \rangle$
  - （因为PHE支持线性运算，可以直接算）
  - 返回所有 $[[d_{\cos}]]$ 给用户

  </ul>
  
  <div style="margin-bottom: 8px;"><strong>3. 用户端</strong>：</div>
  <ul style="margin-top: 4px; padding-left: 24px;">

  - 解密所有距离
  - 排序得到top-k文档的索引

  </ul>
</div>

<!--
好，现在我们有了k'个候选文档，接下来要在这k'个里面找出真正和原始查询最相关的k个。

但我们不能把原始查询发给云端，所以这里用同态加密。

为什么选部分同态加密？因为安全多方计算通常需要第三方，全同态加密又太慢。而余弦距离只涉及内积这种线性运算，用部分同态加密就够了。

大家看定理2，对于归一化后的向量，L2距离和余弦距离的排序是完全一致的，所以我们只需要考虑余弦距离就行。

具体流程是：用户把查询加密了发给云端，云端在加密域计算和k'个文档的余弦距离，返回给用户，用户解密后自己排序。
-->

---
layout: two-cols-header
---

## 文档获取：直接检索 vs 不经意传输

::left::

### 问题：索引安全吗？

用户拿到top-k文档的索引后，可以直接发给云端要文档吗？

**风险**：云端知道了哪k个文档最相关，可以平均它们的嵌入得到$\bar{e}$，这个$\bar{e}$可能很接近查询嵌入$e_k$！

### 定理3：平均嵌入有多接近？

给定查询嵌入$e_k$和top-k相关文档的平均嵌入$\bar{e}$，它们之间的平均角ω满足：

$$ \tan \omega = \frac{\tan \alpha_k}{\sqrt{k}} $$

其中α_k从引理1算出。

::right::

### 两种选择

比较ω和扰动角Δα_k（≈r）：

1. **直接检索**（如果 $\omega \geq \Delta\alpha_k$）：
   - $\bar{e}$在隐私预算保护范围内
   - 直接把索引发给云端
   - 通信开销小

2. **不经意传输（OT）**（如果 $\omega < \Delta\alpha_k$）：
   - $\bar{e}$比扰动后的嵌入$e_{k'}$还接近$e_k$，需要额外保护
   - 使用k-out-of-k' OT协议
   - 云端有k'个文档，用户取k个，但云端不知道取了哪k个

<!--
拿到了top-k文档的索引，接下来要获取文档本身。这里有个问题：我们能直接把索引发给云端吗？

不行，因为云端拿到索引后，知道哪k个文档最相关，它可以把这k个文档的嵌入平均一下，得到的平均嵌入可能很接近真实的查询嵌入！

定理3给出了这个平均嵌入和真实查询之间的夹角ω。

所以我们有两种选择：

第一种，如果ω ≥ Δα_k，说明这个平均嵌入的泄露在隐私预算的保护范围内，那直接把索引发给云端要文档就行。

第二种，如果ω < Δα_k，说明这个平均嵌入比我们的扰动嵌入还接近真实查询，泄露太多了。这时候我们用不经意传输（OT）协议。OT可以让用户从k'个文档里取k个，但云端不知道用户取了哪k个。
-->

---
layout: default
---

## 整体流程回顾

<div style="line-height: 1.4;">
让我们把所有模块串起来：

<div style="margin-top: 8px; margin-bottom: 4px;"><strong>模块1（隐私保护+范围限制）</strong>：</div>
<ol style="margin-top: 4px; margin-bottom: 8px; padding-left: 24px;">

  - 用户本地计算查询嵌入 $e_k$
  - 生成扰动嵌入 $e_{k'}$（满足 $(n,\epsilon)$-DistanceDP）
  - 用户发送 $e_{k'}$ 和 k' 到云端
  - 云端返回与 $e_{k'}$ 最相关的 k' 个文档

</ol>

<div style="margin-bottom: 4px;"><strong>模块2（加密检索）</strong>：</div>
<ol style="margin-top: 4px; margin-bottom: 8px; padding-left: 24px;">

  - 用户加密查询嵌入 $[[e_k]]$ 发送到云端
  - 云端在 k' 个文档上计算加密余弦距离返回
  - 用户解密排序得到 top-k 索引
  
</ol>

<div style="margin-bottom: 4px;"><strong>模块3（文档获取）</strong>：</div>
<ol style="margin-top: 4px; padding-left: 24px;">

  - 若 $\omega \geq \Delta\alpha_k$：直接发索引获取文档 
  - 若 $\omega < \Delta\alpha_k$：用 k-out-of-k' OT 获取文档

</ol>
</div>

<!--
好，现在我们把所有模块串起来回顾一遍整个RemoteRAG的流程。

首先是模块1，用户在本地计算查询嵌入，生成一个扰动后的嵌入发给云端。云端返回和这个扰动嵌入最相关的k'个文档。这一步既保护了隐私，又缩小了后续计算的范围。

然后是模块2，用户把真实查询加密了发给云端，云端在刚才那k'个文档上计算加密的余弦距离返回。用户解密后自己排序，得到真正的top-k索引。

最后是模块3，根据泄露情况选择是直接发索引要文档，还是用不经意传输来获取文档。

这样整个流程就完成了，用户拿到了相关文档，云端却不知道查询是什么。
-->

---
layout: default
---

## 安全性与通信分析

<div style="display: grid; grid-template-columns: 3fr 7fr; gap: 24px;">
<div>

### 安全性分析

**模块1**：扰动嵌入满足 $(n,\epsilon)$-DistanceDP，隐私预算 $\epsilon$ 控制泄露。

**模块2(a)**：加密查询嵌入，没有私钥云端无法破解；PHE计算不泄露信息。

**模块2(b)**（直接检索）：若 $\omega \geq \Delta\alpha_k$，平均嵌入的泄露在隐私预算内。

**模块2(c)**（OT）：OT协议保证索引对云端不可见。

**结论**：用户在给定隐私预算约束下获得top-k文档，不泄露查询信息。

</div>
<div>

### 通信开销对比

| | 安全性 | 通信轮数 | 通信量 |
|---|---|---|---|
| 隐私忽略方案 | ✗ | 1 | nβ + kη |
| 完全隐私方案 | ✓ | 2 | (n+2N+1)β + Nη |
| RemoteRAG (直接) | $(n,\epsilon)$-DistanceDP | 2 | (2n+k+k'+1)β + kη |
| RemoteRAG (OT) | $(n,\epsilon)$-DistanceDP | 2 | 2(n+k'+1)β + k'η |

**优化**：可以合并消息，进一步减少轮数。

</div>
</div>

<!--
现在分析安全性和通信开销。

安全性方面，每个模块都有对应的保护：模块1用(n,ε)-DistanceDP，模块2用同态加密，模块3根据情况选择直接检索或OT。整体保证在隐私预算内不泄露查询信息。

通信开销方面，大家看右边的表格。隐私忽略方案最快，但完全没有隐私。完全隐私方案虽然安全，但通信量是N个文档级别的，根本没法用。RemoteRAG把搜索范围缩小到k'个，通信量就小多了。

实际中还可以优化，比如把扰动嵌入和加密查询合并成一条消息发，进一步减少通信轮数。
-->

---
layout: center
---

# 实验结果

---
layout: two-cols-header
---

## 实验评估：隐私保护效果

::left::

- **攻击方法**：GEIA、Vec2Text
- **评价指标**：SacreBLEU（衡量原始查询和恢复查询的差异）
- **嵌入模型**：T5（768维）
- **关键观察**：
  - 随着扰动r增大，攻击效果从50降到10
  - 当r=0.2时，攻击完全失效
  - 随着ε增大，攻击效果变好（因为扰动变小）

::right::

<img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/a2d2a267d5cbed6508d4b5cf1d2ad153e67003072872420e0c2bdde1beb9d907.jpg" alt="SacreBLEU-r" class="w-7/12 mx-auto mb-4">
<img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/19e2dcf1d872041679fd356c88cee2f3f16f5714dc028d9a229623af44b607ef.jpg" alt="SacreBLEU-ε" class="w-7/12 mx-auto">
<div class="text-center text-xs text-gray-500 mt-1">图4：扰动r和隐私预算ε对应的SacreBLEU指标</div>

<!--
现在看实验结果，首先是隐私保护效果。

我们用现有的嵌入反转攻击方法GEIA和Vec2Text来测试，用SacreBLEU指标衡量攻击能不能恢复原始查询。

大家看右边的图，随着扰动r增大，攻击效果从50降到10。当r=0.2时，攻击完全失效了。

另一个图是攻击效果随ε变化，ε越大，扰动越小，攻击效果越好，这符合我们的预期。

用户可以根据自己的需求，选择合适的ε来平衡隐私和可用性。
-->

---
layout: two-cols-header
---

## 实验评估：检索准确率

::left::

- **数据集**：MS MARCO（10^4/10^5/10^6）、NQ、TQA
- **嵌入模型**：MiniLM、MPNet、T5、OpenAI-1、OpenAI-2
- **参数**：k=5/10/15/20，r=0.03/0.05/0.07/0.1
- **评价指标**：Recall（top-k是否包含在k'中）
- **结果**：**所有设置下Recall=100%**！

理论保证得到验证！

::right::

<div class="mt-10 p-4 bg-green-50 rounded-lg border-2 border-green-200">
  <h4 class="text-green-800 font-bold mb-4 text-lg text-center">表6：各设置下检索准确率</h4>
  <table class="w-full text-sm">
    <thead>
      <tr class="border-b border-green-300">
        <th class="py-2">N</th>
        <th class="py-2">k</th>
        <th class="py-2">r</th>
        <th class="py-2">嵌入模型</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-b border-green-100">
        <td class="py-2">10^4/10^5/10^6</td>
        <td class="py-2">5/10/15/20</td>
        <td class="py-2">0.03/0.05/0.07/0.1</td>
        <td class="py-2">全部5种</td>
      </tr>
    </tbody>
  </table>
  <div class="mt-4 text-center text-green-700 font-bold text-xl">
    Recall = 100% ✓
  </div>
</div>

<!--
接下来是检索准确率。

我们在各种设置下做实验：不同的文档规模N，不同的k，不同的扰动大小r，不同的嵌入模型。

评价指标是Recall——原始查询的top-k文档有没有包含在k'个文档里。

结果是，所有设置下Recall都是100%！这验证了我们的理论分析是正确的，只要按照定理1选k'，就一定不会丢目标文档。
-->

---
layout: two-cols
---

## 实验评估：效率

<br>

**设置**：k'=160, r=0.03（攻击效果约30，中等保护）

**指标**：计算时间、通信量

**对比**：
- 隐私忽略方案：3.15ms，8.00KB
- 完全隐私方案：2.72小时，1.43GB ❌
- RemoteRAG (直接)：0.67秒，46.66KB ✓
- RemoteRAG (OT)：0.68秒，108.24KB ✓

**开销分解**：模块2(a)（同态加密）占95%以上计算量

::right::

<div class="flex items-center justify-center h-full">
<img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/532a08a235f189fcabfb4039dfb8d47885a603e3bfa92e8c3e39039cb092956d.jpg" alt="开销分解" class="w-full">
</div>

---
layout: default
---

## 实验评估：效率（续）

<br>

<div class="grid grid-cols-2 gap-8 px-10">

<div class="text-center">
<img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/8c3f5de2ca88a072c79260c66ddd91d33f6bc385e4efaf576c1f5c93cfead114.jpg" alt="计算成本" class="w-full mx-auto">
<div class="text-sm text-gray-600 mt-3 font-bold">计算成本对比</div>
</div>

<div class="text-center">
<img src="https://cdn-mineru.openxlab.org.cn/result/2026-02-26/852dd719-21ca-431b-b470-b0cf004e7bc2/f987c387ab48168f1d2c45fa24d53a5462a3b38df722057c01e07969561e8e24.jpg" alt="通信成本" class="w-full mx-auto">
<div class="text-sm text-gray-600 mt-3 font-bold">通信成本对比</div>
</div>

</div>

<!--
最后是效率评估。

我们看k'=160，r=0.03这个设置，此时攻击效果约30，是个中等程度的隐私保护。

对比三个方案：
- 隐私忽略方案最快，3.15毫秒，8KB，但不安全。
- 完全隐私方案要2.72小时，1.43GB，根本没法用。
- RemoteRAG直接模式只要0.67秒，46.66KB；OT模式0.68秒，108.24KB。

开销分解看，主要计算量在模块2(a)的同态加密部分，占95%以上。但因为我们把范围缩小到k'=160，而不是全部N个文档，所以总体还是很快的。
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
    <div class="text-4xl mb-2">🔒</div>
    <p class="font-semibold">(n,ε)-DistanceDP</p>
    <p class="text-xs text-gray-600">n维嵌入空间的隐私定义</p>
  </div>
  <div class="text-center">
    <div class="text-4xl mb-2">⚡</div>
    <p class="font-semibold">搜索范围限制</p>
    <p class="text-xs text-gray-600">从N缩小到k'，大幅提升效率</p>
  </div>
  <div class="text-center">
    <div class="text-4xl mb-2">✅</div>
    <p class="font-semibold">理论保证+实验验证</p>
    <p class="text-xs text-gray-600">100%准确率，高效实用</p>
  </div>
</div>

<div class="mt-8 text-center text-sm text-gray-500">
  <p>Yihang Cheng et al. · USTC</p>
</div>

<!--
我的分享就到这里，感谢大家的聆听！欢迎大家提问和讨论。

总结一下RemoteRAG的核心贡献：
第一，提出了(n,ε)-DistanceDP，在n维嵌入空间中定义差分隐私。
第二，通过扰动嵌入把搜索范围从N缩小到k'，大幅提高了效率。
第三，有严谨的理论保证，而且实验验证了准确率100%，效率也很实用。
-->
