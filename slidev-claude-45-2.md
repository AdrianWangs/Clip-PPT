---
theme: seriph
background: /image/slides/image.png
title: 'An Efficient and Privacy-Preserving Cross-Modal Retrieval Scheme for Encrypted Cloud Data'
info: |
	## 高效隐私保护的云端加密跨模态检索方案
	基于CLIP与可搜索加密的双层索引设计
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

# An Efficient and Privacy-Preserving Cross-Modal Retrieval Scheme for Encrypted Cloud Data

## 基于CLIP与可搜索加密的跨模态检索

<div class="pt-12">
	<span class="px-2 py-1 font-semibold">汇报人：王宇哲</span>
</div>

<div class="pt-6 text-sm">
	Wei Jiang et al. · Chinese Academy of Sciences · 2024
	<br>
	2025 CSCWD · Computer Supported Cooperative Work in Design
</div>

<!--
大家好，今天分享的论文是《高效隐私保护的云端加密数据跨模态检索方案》，来自中科院信工所在CSCWD 2025的最新工作。
-->

---
layout: two-cols-header
---

# 研究背景与动机

::left::

### 关键趋势与挑战

- **数据上云常态化**：企业与个人敏感信息日益集中在云端
- **可搜索加密 (SE)**：在密文上实现检索，兼顾可用性与隐私
- **大模型时代**：LLM/RAG需要丰富知识库支撑
- **隐私风险凸显**：RAG默认明文存储，极易暴露敏感数据

*如何在利用大模型增强能力的同时，守住数据隐私底线？*

::right::

### 研究动机

- **RAG + SE 的需求**：构建既安全又可用的私有知识库检索
- **跨模态空白**：现有SE主要聚焦文本，缺乏图文混合场景支持
- **性能要求高**：云端大规模检索必须兼顾速度与精准
- **本文目标**：设计一个<br>**高效、安全、可扩展的跨模态检索框架**

<!--
我们需要同时兼顾安全、效率与大模型协同，这是本文想解决的核心痛点。
-->

---
layout: default
---

## 相关工作

<br>

- **SCMR**：基于Paillier同态加密；高安全性但随机噪声影响匹配稳定性
- **PPCMR**：采用转置密码；密钥与文件数绑定，管理成本高
- **PITR**：客户端使用HNSW构建图索引；本地计算负担沉重

<br>

<!--
现有方案或安全但慢，或高效却难以扩展至跨模态，本文需另辟蹊径。
-->

---
layout: default
---

## 系统整体架构

<div class="mt-6">
	<img src="./image/slides/4b54b44966dbcab05f40169586f9e8c021d1bd9c36eab15cfea84a35a2224e82.jpg" alt="系统模型" class="w-5/12 mx-auto">
	<div class="text-center text-sm text-gray-500 mt-2">图1：三方协同的跨模态检索系统</div>
</div>

<div class="grid grid-cols-3 gap-6 mt-4">
	<div class="bg-gray-50 p-4 rounded-lg">
		<h3 class="text-lg font-bold text-gray-800 mb-3">数据所有者 (DO)</h3>
		<ul class="text-sm space-y-2">
			<li>生成CLIP与安全索引所需密钥</li>
			<li>提取图文特征，构建两层索引</li>
			<li>对原始数据与索引执行加密</li>
			<li>上传密文至云端存储</li>
		</ul>
	</div>

	<div class="bg-gray-50 p-4 rounded-lg">
		<h3 class="text-lg font-bold text-gray-800 mb-3">数据用户 (DU)</h3>
		<ul class="text-sm space-y-2">
			<li>继承DO分发的密钥素材</li>
			<li>本地提取查询特征</li>
			<li>生成SSE陷阱门与Secure kNN查询</li>
			<li>解密云端返回的结果</li>
		</ul>
	</div>

	<div class="bg-gray-50 p-4 rounded-lg">
		<h3 class="text-lg font-bold text-gray-800 mb-3">云服务器 (CS)</h3>
		<ul class="text-sm space-y-2">
			<li>存储加密索引与密文文件</li>
			<li>接收DU提交的陷阱门</li>
			<li>执行“粗筛 + 精排”检索流程</li>
			<li>返回Top-k的加密结果</li>
		</ul>
	</div>
</div>

---
layout: default
---

## 核心思想：两阶段加密检索

<br>

### 阶段一：粗筛 (Fast Filtering)

- 基于 **LSH** 的局部敏感哈希，将候选空间快速压缩
- 独立的加密倒排索引支持64路并行检索
- 目标：在保持高召回的前提下显著降低候选数量

### 阶段二：精排 (Precise Ranking)

- 使用 **Secure kNN** 在密文上保持内积
- 在候选集上进行精准排序，保留Top-k结果
- 目标：兼顾安全性与检索准确度

<div class="mt-6 p-4 bg-yellow-50 rounded-lg text-center">
	<p><strong>漏斗式“粗筛 + 精排”设计</strong>：兼顾百万级数据检索的效率与精度</p>
</div>

---
layout: two-cols-header
---

## 第一阶段：LSH 与加密倒排索引

::left::

### E2LSH 算法回顾

$$H(f) = \left\lfloor\frac{A f + b}{r}\right\rfloor$$

- $A$：随机投影矩阵
- $b$：随机偏移向量
- $r$：分桶宽度

**输出**：512维CLIP特征 → 128位哈希码

> 将哈希码切分为 **64 段 × 2 位**，既提升召回率，也便于并行查表。

::right::

### 加密倒排索引构建

<div class="mt-4">
	<img src="./image/slides/475b42ab9a31f455b022231eafdedf63a75db122d4d14964ea1ac3f0d997b7fe.jpg" alt="倒排索引示例" class="w-10/12 mx-auto">
	<div class="text-xs text-gray-500 text-center mt-2">图2：多段索引并行过滤示意</div>
</div>

- 每段哈希值作为关键字Key（经SSE加密）
- 共享哈希值的图像ID集合构成Value
- 查询时并行命中多段索引，快速定位候选集

<!--
第一层牺牲精排精度换取高召回，后续仍可用第二层修正。
-->

---
layout: two-cols-header
---

## 第二阶段：Secure kNN 内积保持

::left::

### 设计问题

- 候选集规模虽小，仍需在密文上完成准确排序
- 要求云端可计算但无法窥探原始语义

### Secure kNN 方案

- 密钥：$k_{kNN} = \{M_1, M_2, s\}$
- 利用**向量分裂 + 随机矩阵变换**实现可计算密文

::right::

### 内积保持性

$$\tilde{f}_i \cdot \tilde{q} = f_i \cdot q$$

- 密文运算结果与明文完全一致
- 支持余弦/内积相似度排序
- 云端仅能观察分数大小，无法推断特征值

<div class="mt-6 p-4 bg-green-50 rounded-lg text-center">
	<p>在不泄露明文特征的前提下，保持检索精度。</p>
</div>

---
layout: two-cols-header
---

## Secure kNN 向量分裂机制

::left::

### 加密特征向量 $f_i$

- 若 $s[j] = 0$：复制，$f_{i,1}[j] = f_{i,2}[j] = f_i[j]$
- 若 $s[j] = 1$：拆分求和，$f_{i,1}[j] + f_{i,2}[j] = f_i[j]$
- 最终密文：$\tilde{f}_i = \{M_1^T f_{i,1}, M_2^T f_{i,2}\}$

::right::

### 加密查询向量 $q$

- 若 $s[j] = 1$：复制，$q_1[j] = q_2[j] = q[j]$
- 若 $s[j] = 0$：拆分求和，$q_1[j] + q_2[j] = q[j]$
- 最终密文：$\tilde{q} = \{M_1^{-1} q_1, M_2^{-1} q_2\}$

> **互补分裂**：特征与查询在同一位上的分裂策略相反，确保内积恢复。

---
layout: two-cols-header
---

## 内积保持性证明

$$
\begin{aligned}
	ilde{f}_i \cdot \tilde{q} &= (M_1^T f_{i,1}) \cdot (M_1^{-1} q_1) + (M_2^T f_{i,2}) \cdot (M_2^{-1} q_2) \\
&= f_{i,1}^T q_1 + f_{i,2}^T q_2 = \sum_{j=1}^d (f_{i,1}[j]q_1[j] + f_{i,2}[j]q_2[j])
\end{aligned}
$$

::left::

### 当 $s[j] = 0$

- $f_{i,1}[j] = f_{i,2}[j] = f_i[j]$
- $q_1[j] + q_2[j] = q[j]$
- 贡献：$f_i[j] (q_1[j] + q_2[j]) = f_i[j] q[j]$

::right::

### 当 $s[j] = 1$

- $f_{i,1}[j] + f_{i,2}[j] = f_i[j]$
- $q_1[j] = q_2[j] = q[j]$
- 贡献：$(f_{i,1}[j] + f_{i,2}[j]) q[j] = f_i[j] q[j]$

<div class="mt-6 p-4 bg-gray-50 rounded-lg text-center">
	<p>逐维求和即得 $\sum_j f_i[j]q[j] = f_i \cdot q$，内积保持性成立。</p>
</div>

---
layout: two-cols-header
---

## 端到端流程回顾

::left::

### 数据所有者 (离线阶段)

1. CLIP提取图文特征
2. E2LSH 生成64段哈希
3. 构建加密倒排索引 + Secure kNN 密文特征
4. 加密原始文件并外包至云

### 数据用户 (在线查询)

1. 本地提取查询特征
2. 生成SSE陷阱门与Secure kNN查询
3. 云端执行粗筛/精排，返回密文结果
4. 本地解密Top-k并展示

::right::

<div class="mt-4">
	<img src="./image/slides/ddd96773dc9c28616e142faccbdf633a96f462b7c008308877cc5e282ee845cd.jpg" alt="流程示意" class="w-full">
	<div class="text-xs text-gray-500 text-center mt-2">图3：端到端检索流水线</div>
</div>

---
layout: two-cols-header
---

## 示例：检索“海滩上的狗”

::left::

### 粗筛阶段

- 查询哈希并行匹配64个加密索引
- LSH特性让“狗”“海滩”键更易命中
- 高效过滤掉“猫”等无关候选
- 输出候选集：`{ID_狗, ID_海滩}`

::right::

### 精排阶段

- Secure kNN 计算密文内积
- 比较 $Sim(\tilde{f}_{狗}, \tilde{q})$ 与 $Sim(\tilde{f}_{海滩}, \tilde{q})$
- 得到排序列表 `[ID_狗, ID_海滩]`
- 用户解密还原为对应图像

<div class="mt-6 p-3 bg-blue-50 rounded text-sm text-center">
	<strong>云端全程不见明文。</strong> 只暴露访问模式与相似度次序。
</div>

---
layout: section
---

# 威胁模型与安全分析

---
layout: default
---

## 安全设定与目标

<div class="grid grid-cols-2 gap-6 mt-6">
	<div class="bg-gray-50 p-4 rounded-lg">
		<h3 class="text-lg font-bold text-gray-800 mb-3">威胁模型假设</h3>
		<ul class="text-sm space-y-2">
			<li>云服务器：诚实但好奇</li>
			<li>DO / DU：可信且不泄露密钥</li>
			<li>通信信道：安全加密</li>
			<li>攻击模型：密文攻击 (COA)</li>
		</ul>
	</div>

	<div class="bg-gray-50 p-4 rounded-lg">
		<h3 class="text-lg font-bold text-gray-800 mb-3">安全目标</h3>
		<ul class="text-sm space-y-2">
			<li><strong>文件隐私</strong>：密文文件不可逆</li>
			<li><strong>陷阱门隐私</strong>：查询语义不可推断</li>
			<li><strong>索引隐私</strong>：哈希键与特征值不泄露</li>
		</ul>
	</div>
</div>

<div class="mt-6 p-4 bg-gray-50 rounded-lg text-sm">
	<p><strong>文件隐私：</strong> 采用AES等对称加密，密钥仅掌握在DO/DU端。</p>
	<p><strong>陷阱门隐私：</strong> 基于SSE与Secure kNN的安全性，COA下无法反推查询。</p>
	<p><strong>索引隐私：</strong> SSE仅泄露访问模式；没有 $k_{kNN}$ 即无法恢复特征。</p>
	<p class="mt-2 text-red-600"><strong>提示：</strong> Secure kNN (ASPE) 对选择明文攻击相对脆弱，可通过增加随机噪声维度换取更高安全性。</p>
</div>

---
layout: section
---

# 实验评估

---
layout: two-cols-header
---

## 效率表现

::left::

### 索引构建

<img src="./image/slides/ef5c8c32cb97341042e77a6fb1e0e4e009ee7f9eea83b2e0b9655c3a1fef5667.jpg" alt="索引构建时间" class="w-11/12">

- 构建时间随数据量线性增长
- 对比PITR快约 **10%**
- 64段索引可并行生成密文

::right::

### 检索效率

<img src="./image/slides/6e793d3320d400f18704d9c2e859527bc0f7008492219fc8a22b4cec5dc43491.jpg" alt="检索时间" class="w-11/12">

- 检索速度优于PITR ~ **10%**
- 相比MU-TEIR提速 **2 个数量级**
- LSH粗筛显著减少密文内积次数

<div class="mt-4 p-3 bg-gray-50 rounded text-sm">
	性能提升主要来自第一层索引的并行化与有效过滤。
</div>

---
layout: two-cols-header
---

## 检索精度

::left::

### Top-k 精确率

<img src="./image/slides/f20a1479e62ff19ef828bd670c3a140bc66eb5d43b614a5c4467f4bb488fe25a.jpg" alt="Top-k 精确率" class="w-full">

- 各Top-k区间均优于MU-TEIR
- Top-20仍保持较高精确率
- 支持文本→图像跨模态（MU-TEIR不具备）

::right::

### 数据集指标

<div class="bg-gray-50 p-4 rounded-lg mb-4">
	<h4 class="font-bold text-gray-800 mb-2">平均精确率 (mAP)</h4>
	<ul class="text-sm space-y-1">
		<li><strong>Caltech256</strong>：0.853</li>
		<li><strong>CIFAR-100</strong>：0.649</li>
	</ul>
</div>

<div class="bg-gray-50 p-4 rounded-lg text-sm">
	<p><strong>精度折损原因：</strong> 第一层LSH可能误滤相关项，k增大时影响凸显。</p>
	<p class="mt-2"><strong>折中策略：</strong> 增设更多SSE实例能提升召回，但会增加计算负担。</p>
</div>

---
layout: two-cols-header
---

## 局限性与展望

::left::

### 当前局限

- **模态覆盖有限**：高度依赖CLIP，难以直接扩展至视频/音频
- **精度折中**：LSH粗筛可能误删相关样本
- **密钥管理困难**：对称密钥更适合“一对一”共享
- **索引泄露风险**：SSE键值结构仍可被推断，需要更强保护

::right::

### 未来方向

- **多模态模型融合**：引入音频、视频预训练模型拓展场景
- **精细过滤策略**：研究可学习的第一层索引替代LSH
- **非对称加密SE**：探索PEKS等公钥方案应对“One-to-Many”共享
- **形式化安全强化**：对索引加密进行严格的安全性证明

---
layout: end
---

# 谢谢！

## 欢迎交流与提问

<!--
汇报完毕，期待大家的讨论。
-->
