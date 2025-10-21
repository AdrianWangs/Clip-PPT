---
theme: seriph
background: /image/slides/image.png
title: 'Ranked Keyword Search Over Encrypted Cloud Data Through Machine Learning Method'
info: |
  ## 基于机器学习的加密数据排序检索
  ML-RKS/ML-RKS+：效率与前向安全的权衡
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
## 基于机器学习的加密排序检索

<div class="pt-12">
  <span class="px-2 py-1 font-semibold">汇报人: 未知</span>
  </div>

<div class="pt-8 text-sm">
  Yinbin Miao, Wei Zheng, Xiaohua Jia, Xineng Liu, Kim-Kwang Raymond Choo, Robert H. Deng (2022)
  <br>
  IEEE Transactions on Services Computing (TSC)
</div>

<!--
本研究解决“加密数据排序检索”的效率与前向安全难题：静态场景提效，动态更新引入置换矩阵确保旧令牌不能检索新增数据。总体兼顾精度与复杂度。
-->

---
layout: default
---
## 分享目的与受众
- 面向云安全/可搜索加密从业者
- 解析 ML-RKS/ML-RKS+ 机制
- 强调搜索复杂度与精度
- 阐明前向安全与更新
- 提供工程化实现要点

<!--
本页明确目标受众与汇报主线：为何需要 ML-RKS/ML-RKS+，以及我们如何在工程上落实“快而安全”的加密检索方案。
-->

---
layout: section
---
# 研究背景与动机

<!--
背景集中在两点：加密条件的快速排序检索，以及动态更新下的前向安全需求；行业现实要求更低的搜索复杂度与更可控的更新成本。
-->

---
layout: two-cols-header
---
## 问题定义与挑战
::left::
- 返回 Top-k 排序结果
- 多关键词权重表达
- 倒排/树索引复杂度高
- 动态更新开销显著
- 前向安全防文件注入
::right::
![System model](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/1fcf8300fb08de6368af2d42a638858855eef936384a1c336cc5790ec3882d31.jpg){width="80%"}

<div class="text-xs text-gray-500">Figure: 系统模型（数据拥有者/用户/云服务器）</div>

<!--
图中流程：本地构建TF-IDF向量并聚类建索引，云端仅处理加密索引与查询令牌；挑战在于同时兼顾检索效率、动态更新与前向安全。
-->

---
layout: default
---
## 相关工作概览
- 倒排索引排序时间线性
- 树索引次线性但代价高
- 语义扩展常牺牲精度
- 现有动态方案更新重
- 多方案缺前向安全性

<!--
先行工作多在索引结构与加密原语间权衡：倒排简单但排序慢，树索引快但维护难；动态更新与前向安全往往无法兼得。
-->

---
layout: default
---
## 方法总览：ML-RKS 与 ML-RKS+
- ML-RKS：k-means 聚类
- 每簇建平衡二叉树
- 排序用 Secure kNN
- ML-RKS+：置换矩阵
- 支持动态与前向安全

<!--
核心思路：先聚类降规模，再用树索引实现次线性检索；在动态场景引入置换矩阵打破令牌与新增文件的可匹配性，满足前向安全。
-->

---
layout: default
---
## 模型/系统框架图
- 本地生成密钥与向量
- 聚类建树形安全索引
- 云端存储加密索引
- 用户生成加密查询
- 云端返回加密结果

![Balanced tree example](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/f82c7f1d63131f0742d8ef6f2319562d43404ab1ed9b00f9d4a4e6908b490e76.jpg){class="w-9/12 mx-auto"}

<div class="text-xs text-gray-500">Figure: 平衡二叉树索引的检索示意</div>

<!--
流程强调“本地敏感、云端计算”分离：构建与密钥留在本地，云端仅用加密索引与令牌完成排序检索。
-->

---
layout: two-cols-header
---
## 关键算法与伪代码
::left::
- 构建：向量化与聚类
- 每簇建平衡二叉树
- 查询：加密令牌匹配
- 剪枝：节点上界筛除
- 返回：跨簇合并Top-k
::right::
```python
# Pseudo-code (≤25行)
def build_index(files, vocab, k):
    vecs = tfidf_vectorize(files, vocab)
    clusters = kmeans(vecs, k)
    trees = {c: build_bbt(vecs[c]) for c in clusters}
    return trees

def search(trees, query, topk, sk):
    token = encrypt_query(query, sk)
    C = []
    for t in trees.values():
        C.extend(prune_rank(t, token, topk))
    return topk_merge(C, topk)

def prune_rank(tree, token, topk):
    H, R = [], []
    while not tree.empty():
        node = tree.pop()
        if upper_bound(node, token) < kth(R, topk):
            continue
        if node.is_leaf():
            R.append(score(node.vec, token))
        else:
            H.extend(node.children)
    return R
```

<!--
剪枝关键在“节点向量上界”判断：若上界低于当前第k名得分，则整棵子树无需展开，显著减少比较次数。
-->

---
layout: two-cols-header
---
## 目标函数与直觉
::left::
$$\mathcal{S}(\mathbf d_i,\mathbf q)=\mathbf d_i\cdot \mathbf q=\sum_{w_j\in q} v_{i,j}\,\omega_j$$
- 基于 TF-IDF 的相关性
- 加密域中保持内积
- Top-k 排序等价保留

$$J=\sum_{y=1}^{p}\sum_{\mathbf d_i\in \mathcal C_y}\lVert\mathbf d_i-\boldsymbol\mu_y\rVert^2$$
- k-means 聚类最小化簇内方差
- 降规模利于次线性检索
::right::
- 倒排排序约为 \(O(mn)\)
- 树索引约为 \(O(zm\log n)\)
- 聚类+剪枝降低常数项
- Secure kNN 兼顾效率/安全

<!--
等式(1)给出加权内积评分；聚类目标减少跨簇干扰并压缩搜索空间；综合实现更低复杂度与稳定Top-k。
-->

---
layout: two-cols-header
---
## 动态更新与前向安全（ML-RKS+）
::left::
- 引入置换矩阵扰动
- 令牌与新增文件脱钩
- 防止旧令牌匹配新增
- 降低跨簇更新代价
- 不牺牲检索准确性
::right::
- 支持文件增删改操作
- 更新仅影响局部簇
- 索引重建范围受控
- 与已发令牌不兼容
- 满足前向安全定义

<!--
ML-RKS+通过置换矩阵实现“令牌新旧隔离”，动态增量不被历史查询利用；聚类组织让更新局部化，避免全局重构。
-->

---
layout: two-cols-header
---
## 实验设置（数据/指标/对照）
::left::
- 真实数据集评估
- 指标：P@k / Top-k 命中
- 度量：检索时延/更新开销
- 对照：倒排/树索引方案
- 变量：簇数 p、k 值
::right::
![Experiment figure](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/a36c1fb24cd44737174aa7a79c2efd5fc45555bcfe70cbe97a400bb2d4abee53.jpg){class="w-10/12 mx-auto"}

<div class="text-xs text-gray-500">Figure: 评估设置与变量示意</div>

<!--
实验围绕检索效率、排序准确性与更新代价展开；关注 p 和 k 对时延与命中率的影响，并与代表性基线对比。
-->

---
layout: two-cols-header
---
## 主要结果
::left::
- 次线性检索显著提速
- 排序精度与静态持平
- 跨簇合并保持Top-k
- 动态更新成本更可控
- 满足前向安全需求
::right::
![Main results](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/1a333de6a44e896d4c8dc53697bf8c1226b626d8df565eed1425015661e46891.jpg){class="w-10/12 mx-auto"}

<div class="text-xs text-gray-500">Figure: 主结果曲线（检索性能与排序准确性）</div>

<!--
请关注曲线间距与斜率：在相同数据规模与k取值下，ML-RKS/ML-RKS+同时保持较低时延与稳定命中率。
-->

---
layout: two-cols-header
---
## 主要结果（续）
::left::
- 更新操作影响局部簇
- 置换矩阵抑制泄露
- 复杂度优势更稳定
- 大规模下优势更明显
- 工程成本可接受
::right::
![More results](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/3ce07714993968abe20c0b96fdece370bfc208e31fd84b24fc448b3cb2e243a0.jpg){class="w-10/12 mx-auto"}

<div class="text-xs text-gray-500">Figure: 动态更新与安全性相关的对比结果</div>

<!--
该页突出动态场景的稳定性：更新代价远低于全局重建，同时保持前向安全；图形对比显示趋势稳定。
-->

---
layout: two-cols-header
---
## 消融与可扩展性
::left::
- 簇数 p 增大→剪枝增强
- 树高 h 增大→时延上升
- 权重分布偏斜→鲁棒
- k 增大→合并成本升高
- 负载上升→优势更明显
::right::
![Scalability](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/cdda39bef4b2e40aaf69da152244621976adf5814e976f7c1f72ab515c0cd8f0.jpg){class="w-10/12 mx-auto"}

<div class="text-xs text-gray-500">Figure: 规模/参数变化下的性能趋势</div>

<!--
消融关注 p、h、k 的影响：p 提升削弱搜索空间，k 提升增加合并开销；总体趋势显示扩展性良好。
-->

---
layout: default
---
## 工程实现要点
- 统一TF-IDF词典
- 聚类前向量归一
- 节点存上界向量
- 剪枝阈值随 k 调整
- 更新触发局部重建

<!--
实现层面需要关注词典一致性与向量标准化；节点上界与k相关，阈值宜自适应；动态更新尽量限制在受影响簇内。
-->

---
layout: default
---
## 局限性与讨论
- 语义表达受TF-IDF限
- 未覆盖访问模式隐私
- 需信任本地端安全
- 前向不含后向安全
- 超大词典存储压力

<!--
坦诚不足：TF-IDF难捕获深层语义，访问/搜索模式需额外方案(如ORAM)；动态安全聚焦前向，后向需另行增强。
-->

---
layout: default
---
## 应用前景与建议
- 企业加密文档检索
- 医疗合规数据共享
- 政务云受控查询
- 科研数据托管查询
- 混合云隐私搜索

<!--
落地重点在合规与可控性：敏感行业可在不解密前提下支持高效检索，降低数据出域与审计风险。
-->

---
layout: section
---
# 结论

<!--
总结方法、优势与安全性质；给出工程落地要点与未来可演进方向，为进一步产品化提供参考。
-->

---
layout: default
---
## 结论要点
- ML-RKS 降低检索复杂度
- ML-RKS+ 满足前向安全
- 排序精度与静态持平
- 动态更新代价更低
- 具备良好可扩展性

<!--
方案在效率与安全间取得平衡：保持Top-k排序质量，同时显著缩短检索与更新耗时，适用于大规模云端数据。
-->

---
layout: default
---
## 参考文献（择要）
- C. Ge et al. Secure keyword search and data sharing mechanism for cloud computing. IEEE TDSC, 2020.
- D. X. Song et al. Practical techniques for searches on encrypted data. IEEE S&P, 2000.
- D. Boneh et al. Public key encryption with keyword search. EUROCRYPT, 2004.
- C. Wang et al. Enabling secure and efficient ranked keyword search over outsourced cloud data. IEEE TPDS, 2011.
- N. Cao et al. Privacy-preserving multi-keyword ranked search over encrypted cloud data. IEEE TPDS, 2013.
- Z. Fu et al. Multi-keyword fuzzy search over encrypted data. IEEE TIFS, 2016.

<!--
仅列最相关条目；完整清单见论文原文。格式统一到“作者. 标题.  venue, 年.”，便于检索。
-->

---
layout: end
---
# 谢谢！

## 欢迎提问

<!--
如需工程实现细节与参数建议（p、k、阈值、自适应剪枝），或与现有索引系统对接方案，可在Q&A中交流。
-->
