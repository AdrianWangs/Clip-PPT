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

# RemoteRAG
## A Privacy-Preserving LLM Cloud RAG Service

<div class="mt-6 text-sm">

**作者：** Yihang Cheng, Lan Zhang, Junyang Wang, Mu Yuan, Yunhao Yao

**单位：** University of Science and Technology of China · The Chinese University of Hong Kong

**会议：** ACL 2025

</div>

<div class="absolute bottom-8 right-8">
  <p class="text-sm">主讲人：王宇哲</p>
</div>

<!--
大家好。今天想和大家聊聊RemoteRAG这篇论文，它解决了云端RAG服务的隐私保护问题：

其实这个场景大家应该都能理解——我们都希望用云端的强大检索能力，但同时又不太想把那些敏感的查询，比如健康、财务相关的问题，直接暴露给服务器。这个矛盾是真实存在的。
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
先看看背景。RAG技术最近很火，主要是因为它能帮LLM减少幻觉，给出更靠谱的答案。但问题来了：现在的云端RAG服务，用户查询基本都是明文上传的。想想看，如果你问的是健康问题或者财务状况，这些信息全都直接暴露给服务器了。

那现有的解决方案呢？说实话，走了两个极端。要么就是完全不管隐私，直接明文查询；要么就上全套密码学保护，结果是处理一次查询要2.72小时，这显然不现实。

所以核心问题就变成了：我们能不能在隐私、效率、准确性这三者之间找到一个真正可行的平衡点？这就是RemoteRAG想要解决的问题。


## 数据来源备注

### "2.72小时"数据出处

**来源：** Section 4.3 "Special Cases" + Section 5.4 "Efficiency Study" + Table 7

**Privacy-conscious Service定义：**
论文Section 4.3定义了"privacy-conscious cloud RAG service"作为baseline，它追求完全保护用户查询隐私。这相当于RemoteRAG在ε→0的特殊情况，即对所有N个文档进行加密计算（k'=N）。

**实验数据：**
Table 7（效率对比，k'=160配置）显示：
- Privacy-ignorant Service: 3.15ms, 8.00KB（无隐私保护）
- Privacy-conscious Service: 2.72hr, 1.43GB（完全隐私保护）
- RemoteRAG (Direct): 0.67s, 46.66KB
- RemoteRAG (OT): 0.68s, 108.24KB

**原文描述：**
"As indicated in Table 7, the privacy-conscious service requires 2.72 hours in total to process a single user request, which is considered unacceptable."

**计算瓶颈：**
主要开销在module 2(a)的同态加密计算，占总计算量的95%以上。由于需要对所有N个文档计算加密余弦距离，在大规模文档集上变得不可行。RemoteRAG通过module 1的范围限制（从N降到k'），将计算时间降低到1秒以下。

**实验配置：**
- 文档规模：10^6
- 配置：k'=160, r=0.03（攻击效果约30，中等隐私保护）
-->

---
layout: default
---

## 本文创新点

**(n,ε)-DistanceDP隐私定义**：在n维嵌入空间中定义差分隐私，用ε控制查询泄露程度。

**搜索范围限制**：通过扰动嵌入将搜索范围从N个文档缩小到k'个，节省计算和通信成本。

**双重检索机制**：
  - 同态加密排序：在加密域计算余弦距离
  - 两种文档获取方式：直接检索或不经意传输（OT），根据泄露情况选择

**理论保证**：证明k'的选择能确保包含目标文档。

<div class="mt-4 text-center text-sm">
10^6文档规模：仅需0.67秒 + 46.66KB数据传输<br>
检索准确率100%，可抵抗现有嵌入反转攻击
</div>

<!--
RemoteRAG解决的核心问题：现有方案要么完全不保护隐私（明文查询），要么隐私保护太强导致完全不可用（2.72小时处理一次查询）。RemoteRAG的策略是在隐私保护和实用效率之间找到可部署的平衡点。

具体有四步。

第一，定义$(n,\epsilon)$-DistanceDP，把隐私泄露量参数化，用户可以按场景选择$\epsilon$。

第二，用扰动查询先筛出$k'$个候选，把计算规模从$N$降到$k'$。

第三，在候选集合上用同态加密做精排，再按泄露条件在直接检索和OT之间切换。

第四，用定理给出$k'$的选取规则，保证召回不掉点。

补充一下不经意传输(OT)：这是个密码学协议，服务器有$k'$个文档，用户想取其中$k$个，但不想让服务器知道取了哪几个。OT能保证服务器无法知道用户的选择。后面会专门讲。

这套设计的关键不是“最强隐私”，而是“可控风险 + 可接受成本 + 可验证正确性”。

结果也支持这个判断：$10^6$文档规模下，Direct模式0.67秒、46.66KB，召回率100%。
-->

---
layout: default
---

## 系统模型

<div class="grid grid-cols-2 gap-8 items-start mt-20">

<div>

**云服务器 (Cloud)**: 托管大量文档，提供RAG检索服务，但对半诚实好奇。

**用户 (User)**: 提交查询，需要保护查询语义信息不泄露。

**共享嵌入模型**: 用户和云端使用相同的嵌入模型。

**威胁模型**：
- 云服务器是半诚实的（遵守协议但好奇）
- 需要保护：查询嵌入、top-k文档索引

</div>

<div>

<img src="/image/RemoteRAG/7b3742de9032533bdf003a33af174ac76f27f31794f1985999e4699f25313a87.jpg" alt="系统架构模型" class="w-10/12 mx-auto">

<div class="text-center text-xs text-gray-500 mt-1">图1：RemoteRAG流程图</div>

</div>

</div>

<!--
我们来看看系统模型。这里有两个角色：云服务器和用户。

云服务器的定位是"半诚实"——它会按协议办事，但同时也会尽可能推测用户在查什么。用户呢，想用检索服务，但又不想暴露查询内容。双方使用同一个嵌入模型，所以用户可以在本地计算嵌入。

那需要保护什么呢？主要是两样东西。第一是查询嵌入本身，因为现有的攻击手段可以从嵌入向量反推出原始文本。第二是top-k文档的索引，因为这些文档的平均embedding往往很接近查询embedding，泄露了索引就相当于泄露了查询的大致方向。

我觉得这个威胁模型设计得挺实际的，不是那种过于理想化的假设。
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

- 传统DP更适合离散数据，不直接适配连续向量空间
- 查询是嵌入向量，泄露强弱和“距离远近”直接相关
- 所以借鉴Geo-indistinguishability：越远的点，越容易区分；越近的点，越难区分

### (n,ε)-DistanceDP定义

机制K满足(n,ε)-DistanceDP当且仅当：
$$ L(K(x), K(x')) \leq \epsilon \|x - x'\| $$

其中：
- $L(\cdot,\cdot)$ 是分布间的距离
- $\|x - x'\|$ 是L2距离
- $\epsilon$ 是隐私预算

::right::

### 直观理解

- 目标是让云端只能判断“查询大概在哪个语义区域”，看不准具体问题
- 任意两个查询$x,x'$之间，距离越小，扰动后越难区分
- $\epsilon$越小，隐私越强但精度会降；$\epsilon$越大，精度更好但泄露更多

<!--
接下来讲第一个关键技术：(n,ε)-DistanceDP。

先说问题。传统差分隐私常用“相邻数据集”来定义保护强度，这在表格数据里很好用，但在嵌入空间里不够直观。因为向量空间是连续的，语义泄露本质上就是“离真实查询有多近”。

所以论文借鉴了Geo-indistinguishability。它的核心很简单：如果两个查询本来就很近，那扰动后应该更难区分；如果两个查询本来很远，那允许更容易区分。公式$L(K(x),K(x')) \leq \epsilon \|x-x'\|$就是在表达这个约束。

这条公式可以直接按“左边和右边”来读：左边$L(K(x),K(x'))$是“扰动后看起来有多不一样”，右边$\epsilon\|x-x'\|$是“在当前隐私预算下，最多允许不一样到什么程度”。左边不能超过右边，所以近查询会被强制做得更像，远查询才有更大区分空间。

第三，看参数含义。$\epsilon$是旋钮：调小，扰动更强，别人更难猜到你问了什么；调大，结果更准，但泄露也会上升。这个设计把选择权交给用户：你更重视隐私，还是更重视可用性，可以自己定。

如果有同学追问“传统差分隐私到底是什么”，可以这样补一句：

传统DP保护的是“单个样本是否在数据集中”。它要求：把一个人的数据放进去或拿出来，查询结果分布不能变化太大。形式上常写成：$\Pr[M(D)\in S] \le e^\epsilon \Pr[M(D')\in S]$（$D,D'$是相邻数据集）。

这句话的直观含义是：攻击者即使看到输出，也很难确定某个人到底在不在数据里。换句话说，参与与不参与，风险差别被$\epsilon$限制住了。

为什么这里不直接照搬？因为RemoteRAG要保护的对象不是“某条记录是否存在”，而是“这次查询语义离真实意图有多近”。所以它把“相邻关系”换成“向量距离”，更贴合嵌入检索这个场景。

再补一个常见问题：L2距离就是欧氏距离，也就是“直线距离”。如果两个向量是$x=(x_1,\dots,x_n),y=(y_1,\dots,y_n)$，那$\|x-y\|_2=\sqrt{\sum_i(x_i-y_i)^2}$。值越小，语义越接近；值越大，语义越远。
-->

---
layout: two-cols-header
---

## 扰动生成：如何在n维空间中采样？

::left::

### 概率分布

我们使用n维拉普拉斯分布：
$$ D_{n,\epsilon}(x | x_0) \propto e^{-\epsilon \|x - x_0\|} $$

### 实际采样方法

1. **输入**：$x_0$（真实查询嵌入）、$n$（向量维度）、$\epsilon$（隐私预算，控制扰动强度）
2. **采样距离**：$r\sim\text{Gamma}(n,\frac{1}{\epsilon})$，且$\mathbb{E}[r]=\frac{n}{\epsilon}$
3. **采样方向并合成**：$v\sim\text{Unif}(\mathbb{S}^{n-1})$，$x=x_0+r\cdot v$
4. **输出**：$x$（扰动后嵌入，上传云端做粗筛检索）

::right::

<div class="flex flex-col justify-center items-center h-full pl-4">

<img src="/image/RemoteRAG/8fd237ff91d62f68800c3f662d4a01ec970e6c2ccf4890b49a5a5673aa7f638b.jpg" alt="Gamma分布PDF" class="w-10/12 shadow-lg rounded-lg border border-gray-100">

<div class="text-center text-xs text-gray-500 mt-3">图2：不同Gamma分布的概率密度函数</div>

<div class="mt-6 text-sm">

n越高时，r更集中在 $\bar{r}=n/\epsilon$ 附近，所以可用 $\epsilon \approx n/r$ 估计隐私预算

</div>

</div>

<!--
具体怎么生成扰动？


第一步，输入真实查询嵌入x_0、维度n、隐私预算ε；
第二步，采样距离r（Gamma分布）和方向v（单位球面均匀）；
第三步，用x = x_0 + r·v合成扰动后的查询向量。

如果要一句话解释“扰动是怎么操作的”，就是：在向量空间里，以x_0为起点，随机挑一个方向，再沿这个方向走r这么远。

输入和输出也可以这么记：输入是“真实向量+维度+预算”，输出是“扰动后的查询向量x”。

这里的隐私预算ε可以理解成一个旋钮：ε越小，扰动越大，隐私更强；ε越大，扰动越小，可用性更好。

右边的图展示了一个有意思的性质：维度越高，Gamma分布越陡峭，r越集中在期望附近。这意味着可以用ε≈n/r来近似反推隐私预算。

这个特性对实际应用很重要——用户不需要深入理解数学，只要看扰动大小r，就能估计隐私保护程度。

补充一下径向分量和方向向量的直观理解：
- 径向分量r：就是“离真实查询有多远”，相当于地图上从起点到终点的直线距离
- 方向向量v：就是“往哪个方向偏”，相当于地图上的方向
- 合起来就是：先按Gamma分布决定“走多远”，再在单位球面上随便挑一个方向，这样就得到了扰动后的向量x。
-->

---
layout: two-cols-header
---

## 搜索范围k'的计算：如何保证不丢目标文档？

::left::

我们用扰动后的嵌入$e_{k'}$去检索top-$k'$个文档，怎么确保这$k'$个文档里包含了原始查询$e_k$的top-$k$个目标文档？
- 这里$e_k$是原始查询嵌入，$e_{k'}$是扰动后上传到云端的嵌入

<hr>

在单位球面上：
- $\alpha_k$：原始查询top-$k$文档对应的极角
- $\Delta\alpha_k$：$e_k$和$e_{k'}$之间的扰动角（≈r）
- 需要 $\alpha_{k'} = \alpha_k + \Delta\alpha_k$

::right::

<div class="flex flex-col justify-center items-center h-full">

<img src="/image/RemoteRAG/dc5b386358244399c87829cd96fd7ec99207108fe6cdc07ccf4f711711580e5a.jpg" alt="斜投影示意" class="w-7/12 mb-4">

<img src="/image/RemoteRAG/ec27a8d63be19970558bdff01ca16b3ce7e9bd7256eb301a20080fdaf478f33c.jpg" alt="正投影示意" class="w-7/12">

<div class="text-center text-xs text-gray-500 mt-2">图3：3维投影示意</div>

</div>

<!--
接下来讲搜索范围k'的计算。这里有个核心约束：我们用扰动后的嵌入去检索，但必须保证原始查询的top-k目标文档不会被漏掉。

先看几何示意图，逻辑很清楚：
第一，原始查询e_k的top-k文档对应一个极角范围α_k；
第二，扰动查询e_k'和真实查询之间有个夹角Δα_k（≈r）；
第三，为了覆盖最坏情况，需要把检索范围扩大到α_{k'} = α_k + Δα_k。

这样无论扰动往哪个方向偏，目标文档都一定在这个更大的范围内。这个设计很直接——用几何边界做最坏情况保障，没有复杂的数学，就是把两个角度加起来。
-->

---
layout: two-cols-header
---

## k'怎么选：把“角度”换成“数量”

::left::

<div class="pr-5 mr-2 border-r border-gray-300">


- 假设：文档嵌入在单位球面上近似均匀分布（用来算面积比例）
- 定义：$\alpha_k$ 是“刚好覆盖 top-$k$”的球面半角（蓝圈的大小）
- 引理1：给定$k,N$可以算出$\alpha_k$（面积比例 ↔ 文档数量）
- 定理1：把半角放大到$\alpha_{k'}=\alpha_k+\Delta\alpha_k$，再算出对应的$k'$
> 圈变大一点，覆盖的文档数就必须跟着变大，否则会漏掉原来的top-$k$

</div>

::right::


- 引理1（$k$与$\alpha_k$）：
  $$ k = N \cdot \frac{\Omega_{n-1}(\pi)}{\Omega_n(\pi)} \cdot \int_0^{\alpha_k} \sin^{n-2} \theta \, d\theta $$

- 定理1（$k'$的选择）：
  $$ k' - k = N \cdot \frac{\Omega_{n-1}(\pi)}{\Omega_n(\pi)} \cdot \int_{\alpha_k}^{\alpha_{k'}} \sin^{n-2} \theta \, d\theta,\ \ \alpha_{k'} = \alpha_k + \Delta\alpha_k $$

<!--
这一页我们分两层来讲：先看宏观流程，再看公式细节。

我们从宏观上看要解决的核心问题是：查询偏了，搜索范围要扩大多少才不会漏掉目标？
流程就是三步走：
1. **数量转角度**：先算原始 $k$ 个文档占了多大的角 $\alpha_k$。
2. **角度扩展**：因为有扰动 $\Delta\alpha$，所以要把搜索半径扩大到 $\alpha_{k'} = \alpha_k + \Delta\alpha$。
3. **角度转数量**：范围变大了，里面圈住的文档数自然就变成了 $k'$。

那这个数量和角度怎么转换呢？就是右边这个看似复杂的积分公式：
$$ k = N \cdot \frac{\Omega_{n-1}}{\Omega_n} \cdot \int \sin^{n-2} \theta \, d\theta $$

这个公式可以拆成三部分看，物理含义非常清晰：

1.  **$N$（总数）**：这是基数，文档总共有多少个。

2.  **$\int \sin^{n-2} \theta \, d\theta$（形状积分）**：这是在算“球冠”的面积。
    - 用的是“切片法”：从极点（0度）一直积到边界（$\alpha_k$）。
    - 为什么是 $\sin^{n-2}$？因为在高维空间，切片（$(n-1)$维球）的表面积正比于 $\sin^{n-2}\theta$。这一项就是在累加所有切片的面积。

3.  **$\frac{\Omega_{n-1}}{\Omega_n}$（归一化系数）**：
    - $\Omega_n$ 是整个球的总面积，$\Omega_{n-1}$ 是切片的面积常数。
    - 这一项的作用是把计算出的面积**归一化**，变成一个 0 到 1 之间的比例。

**一句话总结**：
$$ \text{局部数量 } k = \text{总数量 } N \times \left( \frac{\text{球冠面积}}{\text{球总面积}} \right) $$
-->

---
layout: default
---

## 隐私预算ε的选择：在隐私和成本间权衡


### 两个阈值

用户通常有两个明确的阈值：

1. **隐私阈值（上界）**：
   - 随着扰动r增大，攻击效果逐渐降低（下图）
   - 当攻击效果低于用户可接受的阈值时，得到最小的r
   - 因为 $\epsilon \approx n/r$，所以这确定了**ε的最大值**

2. **成本阈值（下界）**：
   - 计算和通信成本随k'增大而增加
   - 最大可接受的k'确定了最大的$\Delta\alpha_k$（即r）
   - 这确定了**ε的最小值**


<!--
这一页只回答一个问题：$\epsilon$ 到底怎么选。

方法很直接，分两步。

第一步，先定隐私要求，得到$\epsilon$的上界。
比如我们要求攻击效果必须低于30分，那么扰动$r$就不能太小。因为$\epsilon \approx n/r$，$r$越大，$\epsilon$越小，所以这一步会给出一个“最大可用$\epsilon$”。

第二步，再看系统预算，得到$\epsilon$的下界。
计算和通信成本主要由$k'$决定，$k'$不能无限放大。把可接受的最大$k'$代回去，就能得到一个“最小可用$\epsilon$”。

最后结论很清楚：$\epsilon$必须落在这个区间里——上界来自隐私，下界来自成本。我们不是拍脑袋调参，而是在约束内选一个可落地的值。
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

归一化嵌入的L2距离和余弦距离：$d_{l2}(e_a, e_b) = \|e_a - e_b\|$ 和 $d_{\cos}(e_a, e_b) = 1 - \langle e_a, e_b \rangle$

**定理2**：对于归一化向量，L2距离和余弦距离排序一致：$d_{l2}(e_a, e_b) = \sqrt{2 d_{\cos}(e_a, e_b)}$

所以只用考虑余弦距离。

::right::

### 具体流程

**1. 用户端**：
- 用PHE加密查询嵌入 $e_k$，得到 $[[e_k]]$
- 发送 $[[e_k]]$ 到云端

**2. 云端**：
- 对k'个文档中的每个嵌入e，计算加密的余弦距离：
- $[[d_{\cos}(e_k, e)]] = 1 - \langle [[e_k]], e \rangle$
- （因为PHE支持线性运算，可以直接算）
- 返回所有 $[[d_{\cos}]]$ 给用户

**3. 用户端**：
- 解密所有距离
- 排序得到top-k文档的索引

<!--
好，现在我们有了k'个候选文档。接下来要在这k'个里面找出真正和原始查询最相关的k个。但问题是，我们不能把原始查询直接发给云端，对吧？所以这里用同态加密。

为什么选部分同态加密呢？主要是权衡。安全多方计算通常需要引入第三方，有点麻烦；全同态加密虽然强大但太慢了。好在余弦距离只涉及内积这种线性运算，部分同态加密就完全够用。

这里有个有意思的地方——看定理2，对于归一化后的向量，L2距离和余弦距离的排序结果是完全一致的。所以我们只需要算余弦距离就行，能省不少事。

具体流程很清楚：用户把查询加密后发给云端，云端在加密域上计算它和k'个文档的余弦距离，返回加密的距离值，用户解密后自己排序。这样云端全程看不到真实查询。
-->

---
layout: two-cols-header
---

## 文档获取：直接检索 vs 不经意传输

::left::

<div class="pr-5 mr-2 border-r border-gray-300">

### 先回答一个问题

用户拿到top-k文档索引后，能不能直接发给云端要文档？

风险在这里：云端知道这k个索引后，可以求平均嵌入$\bar{e}$。如果$\bar{e}$离真实查询$e_k$太近，就会泄露查询方向。

### 判据：泄露到底有多大？

定理3给出可计算的角度关系：
$$ \tan \omega = \frac{\tan \alpha_k}{\sqrt{k}} $$

- $\omega$：$e_k$和$\bar{e}$的夹角
- $\omega$越小，说明$\bar{e}$越接近$e_k$，泄露越强

</div>

::right::


比较$\omega$和扰动角$\Delta\alpha_k$（约等于$r$）：

1. **直接检索**（$\omega \geq \Delta\alpha_k$）
   - 泄露不超过当前隐私预算
   - 直接发索引取文档
   - 通信最省

2. **OT检索**（$\omega < \Delta\alpha_k$）
   - 平均嵌入泄露超过预算
   - 用k-out-of-k' OT取文档
   - 云端不知道用户具体取了哪k个

<!--
这一页只讲一件事：文档阶段到底能不能直接发索引。

关键风险是“平均嵌入泄露”。云端拿到top-k索引后，可以算出平均向量$\bar{e}$。如果$\bar{e}$和真实查询$e_k$夹角太小，查询语义就暴露了。

定理3把这个风险量化成$\omega$，所以决策可以落到一个可计算规则：只比较$\omega$和$\Delta\alpha_k$。

如果$\omega \ge \Delta\alpha_k$，泄露还在预算内，直接检索即可。
如果$\omega < \Delta\alpha_k$，泄露超预算，就切换到OT。

所以这里不是“二选一的经验判断”，而是“单一阈值驱动的策略切换”。
-->

---
layout: two-cols
---

## 整体流程回顾

<br>

**模块1：隐私保护+范围限制**

1. 用户计算查询嵌入 $e_k$
2. 生成扰动嵌入 $e_{k'}$（满足 $(n,\epsilon)$-DistanceDP）
3. 发送 $e_{k'}$ 和 k' 到云端
4. 云端返回 k' 个相关文档

**模块2：加密检索**

1. 用户加密 $[[e_k]]$ 发送到云端
2. 云端计算加密余弦距离返回
3. 用户解密排序得到 top-k 索引

::right::

<br>
<br>
<br>

**模块3：文档获取**

- 若 $\omega \geq \Delta\alpha_k$：直接获取
- 若 $\omega < \Delta\alpha_k$：使用 OT 协议

<br>

**流程总结**

用户通过三个模块获得相关文档，云端无法知道查询内容，实现隐私保护。

<!--
好，我们把所有模块串起来看一下完整的流程。

模块1是隐私保护+范围限制。用户在本地算出查询嵌入，加上扰动后发给云端。云端返回和扰动嵌入最相关的k'个文档。这一步既保护了隐私，又大大缩小了后续的计算范围。

模块2是加密检索。用户把真实查询加密后发给云端，云端在那k'个候选文档上计算加密的余弦距离，返回给用户。用户解密后自己排序，得到真正的top-k索引。

模块3是文档获取。根据平均嵌入的泄露情况，智能地选择是直接发索引，还是用OT协议来获取文档。

整个流程下来，用户拿到了想要的文档，而云端从头到尾都不知道真正的查询内容是什么。这就是RemoteRAG的完整设计。
-->

---
layout: two-cols-header
---

## 安全性与通信分析

::left::

### 安全性分析

**模块1**：扰动嵌入满足 $(n,\epsilon)$-DistanceDP

**模块2(a)**：加密查询，PHE计算不泄露信息

**模块2(b)**：若 $\omega \geq \Delta\alpha_k$，泄露在预算内

**模块2(c)**：OT协议保证索引不可见

用户在隐私预算约束下获得top-k文档，不泄露查询信息。

::right::

### 通信开销对比

| 方案 | 轮数 | 通信量 |
|---|---|---|
| 隐私忽略 | 1 | nβ + kη |
| 完全隐私 | 2 | (n+2N+1)β + Nη |
| RemoteRAG (直接) | 2 | (2n+k+k'+1)β + kη |
| RemoteRAG (OT) | 2 | 2(n+k'+1)β + k'η |

- 隐私忽略：用户上传查询嵌入，云端直接返回top-k（相当于$\epsilon \to \infty$）
- 完全隐私：全程密码学保护，等价$k'=N$对全部文档计算并用OT取回（相当于$\epsilon \to 0$）

> 另外，论文还提到一个工程优化：把可合并的消息打包发送，这样可以进一步减少交互轮数。

<!--
接下来看看安全性和通信开销的分析。

安全性方面，每个模块都有相应的保护机制：模块1用(n,ε)-DistanceDP保护扰动嵌入，模块2用同态加密保护真实查询，模块3根据具体情况选择直接检索或OT。这三层保护叠加起来，能确保在隐私预算内不泄露查询信息。

通信开销的对比很有意思。看右边的表格，隐私忽略方案确实最快，但完全没有隐私保护。完全隐私方案虽然安全，但通信量是N个文档级别的，实际根本用不起来。RemoteRAG的关键就在于把搜索范围缩到了k'个，通信量一下子就降下来了。

这里补一句论文里的定义（Section 4.3）：
- 隐私忽略方案：用户直接上传查询嵌入，云端直接回top-k，等价于$\epsilon \to \infty$。
- 完全隐私方案：追求完全保护查询隐私，等价于$k'=N$，要在全量文档上做加密计算并通过OT取文档，代价很高。

而且还有优化空间，比如可以把扰动嵌入和加密查询合并成一条消息发送，进一步减少通信轮数。
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
- **实验结果**：
  - 扰动r增大，攻击效果从50降到10
  - r=0.2时，攻击完全失效
  - ε增大，攻击效果变好（扰动变小）

::right::

<img src="/image/RemoteRAG/a2d2a267d5cbed6508d4b5cf1d2ad153e67003072872420e0c2bdde1beb9d907.jpg" alt="SacreBLEU-r" class="w-7/12 mx-auto mb-4">
<img src="/image/RemoteRAG/19e2dcf1d872041679fd356c88cee2f3f16f5714dc028d9a229623af44b607ef.jpg" alt="SacreBLEU-ε" class="w-7/12 mx-auto">
<div class="text-center text-xs text-gray-500 mt-1">图4：扰动r和隐私预算ε对应的SacreBLEU指标</div>

<!--
现在看实验结果，先看隐私保护效果。

论文用了现有的嵌入反转攻击方法GEIA和Vec2Text来测试，用SacreBLEU这个指标衡量攻击能不能恢复出原始查询。

看右边的图，效果很明显。随着扰动r增大，攻击效果从50一路降到10。特别是当r达到0.2的时候，攻击就基本完全失效了。

另一张图展示的是攻击效果随ε的变化。ε越大，扰动越小，攻击效果越好，这完全符合我们的理论预期。

所以用户可以根据自己对隐私的重视程度，选择一个合适的ε值。这个权衡的决定权在用户手里。
-->

---
layout: two-cols
---

## 实验评估：检索准确率

**实验配置**

- 数据集：MS MARCO、NQ、TQA
- 文档规模：10^4, 10^5, 10^6
- 嵌入模型：MiniLM, MPNet, T5, OpenAI-1, OpenAI-2
- 参数：k=5/10/15/20，r=0.03/0.05/0.07/0.1

**评价指标：Recall**

检查原始查询 $e_k$ 的top-k文档是否都包含在扰动查询 $e_{k'}$ 检索的k'个文档中。

计算方式：$\text{Recall} = \frac{|\text{top-k} \cap \text{top-k'}|}{k}$

::right::

<br>

**实验结果**

<div class="text-center text-2xl font-bold mt-6 mb-4">
Recall = 100% ✓
</div>

所有设置下，原始查询的top-k文档全部被检索到，验证了定理1的正确性。

<!--
然后是检索准确率的实验。

实验配置很全面：测试了不同的文档规模（从1万到100万）、不同的k值、不同的扰动大小r，还用了5种不同的嵌入模型。评价指标是Recall，就是看原始查询的top-k文档有没有全部被包含在k'个候选文档里。

结果很漂亮——所有设置下Recall都是100%！

这说明什么？说明我们前面讲的那些理论不是纸上谈兵，定理1的公式真的能保证不漏掉目标文档。只要按照公式选k'，就能100%召回。这个理论保证在实践中是靠得住的。
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
<img src="/image/RemoteRAG/532a08a235f189fcabfb4039dfb8d47885a603e3bfa92e8c3e39039cb092956d.jpg" alt="开销分解" class="w-full">
</div>

<!--
这一页先看效率主结论。

同样是保护查询隐私，三种方案的代价差异非常大：
- 隐私忽略方案最快，3.15ms和8KB，但没有隐私保护。
- 完全隐私方案最安全，但要2.72小时和1.43GB，基本不可部署。
- RemoteRAG两种模式都在1秒内，通信量也控制在百KB以内。

关键原因在最后一行：主要计算开销集中在模块2(a)同态加密，占95%以上。
RemoteRAG可用，不是因为同态加密变便宜了，而是因为先把计算范围从N缩到k'，只在候选集上做加密精排。
-->

---
layout: default
---

## 实验评估：效率（续）

<br>

<div class="grid grid-cols-2 gap-8 px-10">

<div class="text-center">
<img src="/image/RemoteRAG/8c3f5de2ca88a072c79260c66ddd91d33f6bc385e4efaf576c1f5c93cfead114.jpg" alt="计算成本" class="w-full mx-auto">
<div class="text-sm text-gray-600 mt-3 font-bold">计算成本对比</div>
</div>

<div class="text-center">
<img src="/image/RemoteRAG/f987c387ab48168f1d2c45fa24d53a5462a3b38df722057c01e07969561e8e24.jpg" alt="通信成本" class="w-full mx-auto">
<div class="text-sm text-gray-600 mt-3 font-bold">通信成本对比</div>
</div>

</div>

<!--
这一页是上一页的展开图。

左图看计算成本：完全隐私方案随文档规模上升会急剧变慢，RemoteRAG增长明显更平缓。
右图看通信成本：完全隐私方案接近全量传输，RemoteRAG保持在小规模通信区间。

所以结论很明确：
第一，瓶颈仍然是密码学计算本身。
第二，决定可用性的关键是“计算规模控制”，也就是先筛k'再精排。
第三，RemoteRAG是在隐私约束下，把系统拉回到可部署区间。
-->

---
layout: end
---

# 谢谢！

## 欢迎提问与讨论

<br>

### 要点回顾

<div class="grid grid-cols-3 gap-6 mt-8 text-sm">
  <div class="text-center">
    <p class="font-semibold">(n,ε)-DistanceDP</p>
    <p class="text-xs text-gray-600 mt-1">n维嵌入空间的隐私定义</p>
  </div>
  <div class="text-center">
    <p class="font-semibold">搜索范围限制</p>
    <p class="text-xs text-gray-600 mt-1">从N缩小到k'</p>
  </div>
  <div class="text-center">
    <p class="font-semibold">理论+实验验证</p>
    <p class="text-xs text-gray-600 mt-1">100%准确率</p>
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
