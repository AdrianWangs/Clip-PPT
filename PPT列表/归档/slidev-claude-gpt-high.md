---
theme: seriph
background: /image/slides/image.png
title: 'Ranked Keyword Search Over Encrypted Cloud Data Through Machine Learning Method'
info: |
  ## 基于机器学习的云端加密数据排序检索
  兼顾效率与前向安全的ML-RKS方案
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
highlighter: shiki
lineNumbers: false
mdc: true
katex: true
hideInToc: true
---
# Ranked Keyword Search Over Encrypted Cloud Data Through Machine Learning Method
## 基于机器学习的云端加密数据排序检索

<div class="pt-12">
  <span class="px-2 py-1 font-semibold">汇报人: 未知</span>
</div>

<div class="pt-8 text-sm">
  Yinbin Miao et al. (Xidian University & CityU HK, 2022)
  <br>
  IEEE Transactions on Services Computing
</div>

<!-- 本页概述论文聚焦的云端密文检索痛点，点出ML-RKS系列兼顾检索效率与前向安全的核心目标，为后续细节预热，并提醒听众关注作者团队与发表刊物背景。 -->

---
layout: default
---
## 分享目的与受众
- 面向**密文检索**与云服务研发团队
- 梳理ML-RKS系列实现的关键创新
- 评估方案在效率与安全上的收益
- 讨论落地部署时的参数取舍

<!-- 本页明确听众定位与汇报主线，提示后续内容将从创新点、性能表现到部署要点逐层展开，邀请听众对照自身业务需求思考适配性。 -->

---
layout: section
---
# 研究背景与动机
- 云上数据外包规模持续攀升
- 传统密文检索效率瓶颈凸显
- 动态更新触发前向安全威胁

<!-- 本页回顾云端数据外包与安全检索需求的同步提升，强调效率瓶颈与前向安全风险共同促成机器学习辅助索引的提出。 -->

---
layout: two-cols-header
---
## 相关工作与痛点
::left::
- 倒排索引在多关键词下仍为O(nm)
- 树型索引当z接近n时延迟飙升
- 动态更新与前向安全缺乏统筹

::right::
- **对比综述**：表1量化RKS与ML-RKS差距
- **应用驱动**：实时共享需兼顾隐私低延迟

<!-- 本页结合表一总结既有方案在复杂度与安全性上的短板，突出缺乏聚类缩减与前向安全兼顾能力是本文亟待解决的核心问题。 -->

---
layout: default
---
## 核心方案总览
- k-means聚类缩短候选索引路径
- 平衡二叉树维持子集内排序准确
- 扩展kNN加密保持明密一致
- 随机填充与拆分保障令牌匿名
- ML-RKS+置换矩阵实现前向安全

<!-- 本页凝练ML-RKS与ML-RKS+的核心组件，包括聚类索引结构、加密得分保持以及增强的前向安全机制，让听众先建立整体框架。 -->

---
layout: two-cols-header
---
## 系统流程与架构
::left::
- 数据拥有者提取TF-IDF并聚类
- 构建加密索引后上传云端
- 数据用户生成权重化查询令牌
- 云服务器按得分返回Top-k密文

::right::
![System model diagram](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/1fcf8300fb08de6368af2d42a638858855eef936384a1c336cc5790ec3882d31.jpg)
<div class="text-xs text-gray-500">Figure: 系统模型流程</div>

<!-- 本页通过系统流程图串联三类角色与四个阶段，提醒听众关注权重化查询与加密索引交互以及云端仅执行内积的受限能力。 -->

---
layout: two-cols-header
---
## 索引构建策略
::left::
- 聚类根节点替代原始中心向量
- 父节点分量取子节点最大值
- 逐层剪枝降低冗余得分计算
- 候选校验维持跨簇排序精度

::right::
![Balanced tree search example](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/f82c7f1d63131f0742d8ef6f2319562d43404ab1ed9b00f9d4a4e6908b490e76.jpg)
<div class="text-xs text-gray-500">Figure: 平衡二叉树检索示例</div>

<!-- 本页借助树结构示例说明聚类后的索引如何通过最大值父节点实现剪枝，并强调仍需校验未选簇以保持Top-k准确性。 -->

---
layout: two-cols-header
---
## 关键算法与伪代码
::left::
- 输入簇内文档向量初始化节点
- 底层补足节点保持树形平衡
- 元素级最大值生成父节点向量
- 安全kNN加密输出索引密文

::right::
```python
def build_index(vectors):
    nodes = [Node(v) for v in vectors]
    pad = next_power_of_two(len(nodes))
    while len(nodes) < pad:
        nodes.append(Node(nodes[-1].value))
    level = nodes[:]
    tree = []
    while len(level) > 1:
        parent = []
        for i in range(0, len(level), 2):
            merged = np.maximum(level[i].value, level[i+1].value)
            parent.append(Node(merged))
        tree.append(level)
        level = parent
    root = level[0]
    return encrypt_tree(tree + [[root]])
```

<!-- 本页用伪代码展示索引构建的关键循环，并提醒听众注意填充节点与元素级最大化如何支撑后续的密态得分。 -->

---
layout: default
---
## 目标函数与加密映射
$$
S(\mathbf{d}_i,\mathbf{q}) = \sum_{w_j \in q} TF_{i,j} \cdot IDF_j \cdot \omega_j
$$
$$
S(\widehat{\mathbf{d}}_i,\widehat{\mathbf{q}}) = \widehat{\mathbf{d}}_i \cdot \widehat{\mathbf{q}} = S(\mathbf{d}_i,\mathbf{q})
$$
$$
S(\widehat{\mathbf{c}}_y,\widehat{\mathbf{q}}) = \widehat{\mathbf{c}}_y \cdot \widehat{\mathbf{q}}
$$
- 得分函数保留TF-IDF加权语义
- 扩展kNN保持明密结果一致
- 阈值检测避免跨簇漏检

<!-- 本页强调目标函数在明密文一致性上的保证，并提示σ等随机扰动如何在保持精度的同时为安全性提供余地。 -->

---
layout: two-cols-header
---
## 前向安全机制
::left::
- ML-RKS+引入版本相关置换矩阵
- 查询令牌同步版本随机因子
- 更新操作同乘新矩阵阻断旧令牌
- 理论复杂度约O(log L_y)可控

::right::
![Versioned update example](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/a36c1fb24cd44737174aa7a79c2efd5fc45555bcfe70cbe97a400bb2d4abee53.jpg)
<div class="text-xs text-gray-500">Figure: 版本化更新示例</div>

<!-- 本页借由更新示意强调置换矩阵与版本号联动如何抵御旧令牌检索新文件，并提示复杂度保持在对数级别。 -->

---
layout: default
---
## 安全性分析要点
- 随机拆分向量与逆矩阵防止线性恢复
- 令牌同源碰撞概率随ε指数衰减
- 引入U个虚假关键词抵御背景推断
- σ参数调节排名隐私与精度权衡

<!-- 本页归纳四个关键安全结论，提醒听众σ与虚假维度数量是可调的安全旋钮，同时强调拆分矩阵提供的基础保密性。 -->

---
layout: two-cols-header
---
## 实验设置
::left::
- 数据集：20Newsgroups含20类文档
- 实现：Java于i7-8565U与8GB内存
- 比较基线：RKS与RKS+静态方案
- 默认参数：n<=10000,m<=1000,k<=50

::right::
<div class="bg-slate-100 rounded p-4 text-sm space-y-2">
  <div><span class="font-semibold">聚类数:</span> p = 5</div>
  <div><span class="font-semibold">伪关键词:</span> U = V = 1</div>
  <div><span class="font-semibold">查询关键词:</span> t <= 50</div>
</div>

<!-- 本页交代实验环境与关键超参数，提醒听众聚类规模与伪关键词数量决定了预处理成本与安全级别。 -->

---
layout: two-cols-header
---
## 聚类开销评估
::left::
- 聚类时间随n增先升后降
- 增大m会线性拉升迭代轮次
- 簇数提升显著增加预处理
- 预处理换取后续检索加速

::right::
<div class="grid grid-cols-2 gap-2">
  ![Clustering time vs n](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/49c70ebb6781ae7b8b689e5efa3e402027067f1643cbdbe50394ccd896b5c80d.jpg){class="w-full"}
  ![Clustering time vs clusters](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/b415e41fe0cb16e59fd02480f4d93e7b7f6c4438b4ab50c91d61dde4c689a53b.jpg){class="w-full"}
</div>
<div class="text-xs text-gray-500">Figure: 聚类耗时对n与p的影响</div>

<!-- 本页通过两幅曲线展示聚类阶段的时间变化，引导听众理解预处理成本与后续效率之间的权衡关系。 -->

---
layout: two-cols-header
---
## 索引与令牌生成
::left::
- 索引构建复杂度保持O(nm)
- ML-RKS较RKS生成时间更低
- RKS+因矩阵运算略慢于ML-RKS+
- 令牌生成对m或t呈线性关系

::right::
<div class="grid grid-cols-2 gap-2">
  ![Index build time](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/6b43812655f558776e0af5d5008a255392a56e6c1e08978dd37c1139723be30e.jpg){class="w-full"}
  ![Token generation time](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/6ebc17e9509e944558f390624afd6130b6a191451dc2e7d8ffeebc2d95b4a131.jpg){class="w-full"}
</div>
<div class="text-xs text-gray-500">Figure: 索引与令牌生成耗时</div>

<!-- 本页突出聚类带来的索引构建加速与令牌生成的线性特性，提醒听众量化预处理收益。 -->

---
layout: two-cols-header
---
## 搜索时延与更新
::left::
- 查询延迟随n线性增长仍<100ms
- 增大m或k提升得分计算成本
- ML-RKS+搜索显著快于RKS+
- 新增文件更新耗时高于修改删除

::right::
<div class="grid grid-cols-2 gap-2">
  ![Search latency](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/ff5d83e8c92f14357e7fddfafbf5c885188a274a832f6c362099dc07466d8c84.jpg){class="w-full"}
  ![Update cost](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/df058342fbd3825cb304c67b32b035c7010c9a3c47bf29946dca4dfe53c0bafe.jpg){class="w-full"}
</div>
<div class="text-xs text-gray-500">Figure: 搜索延迟与更新成本</div>

<!-- 本页提醒听众关注小于一百毫秒的搜索延迟上限以及不同更新操作的耗时差异，突出ML-RKS+在动态环境下的优势。 -->

---
layout: two-cols-header
---
## 准确率与排名隐私
::left::
- σ减小提升P_k但暴露排序
- 跨簇取Top-k保持RKS同等精度
- σ增大提高扰动与隐私保护
- 参数调优需贴合业务验收

::right::
<div class="grid grid-cols-2 gap-2">
  ![Search accuracy](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/37a1b300aa569043756e754f8e480d41bbca50c1a4614598f3ee312f6358add1.jpg){class="w-full"}
  ![Rank privacy](https://cdn-mineru.openxlab.org.cn/result/2025-10-21/99ec5320-3a91-4791-a67b-f4c5f4535912/527688e7177b24b6a0e8bf25cda442a923493cd82b7796294e5756381690a238.jpg){class="w-full"}
</div>
<div class="text-xs text-gray-500">Figure: 准确率与排名隐私权衡</div>

<!-- 本页引导听众理解σ参数对准确率与排名隐私的对冲作用，便于实际部署时设定双赢区间。 -->

---
layout: default
---
## 消融与参数洞察
- 单簇Top-k策略带来轻微精度损失
- 增大聚类数量有助平衡检索负载
- 虚假维度数量直接映射安全级别
- σ作为隐私旋钮支撑多行业场景

<!-- 本页总结参数敏感性观察，提示可通过调节聚类数与虚假维度数量在性能与安全间取得定制化平衡。 -->

---
layout: default
---
## 局限性与讨论
- 依赖TF-IDF难覆盖语义嵌入需求
- 密钥分发链路需额外可信保障
- 聚类模型对数据漂移较为敏感
- 未覆盖访问与删除隐私防护

<!-- 本页坦诚方案在语义表达、密钥管理与隐私类型上的局限，提醒听众部署时需配套补强措施。 -->

---
layout: default
---
## 应用前景与建议
- 企业云文档检索可率先试点
- 与RAG结合需拓展密钥协同接口
- 建议定期重聚类校准数据分布
- 配合密钥审计与访问日志监控

<!-- 本页提出潜在落地路线与操作建议，鼓励听众结合现有检索系统制定渐进式引入计划。 -->

---
layout: section
---
# 结论
- ML-RKS实现高效密文多关键词检索
- ML-RKS+兼顾动态更新与前向安全
- 理论与实测共同验证性能收益
- 可调参数支撑多样隐私策略

<!-- 本页回顾方案亮点，强调效率、安全与可调性三大支柱，同时引出最后的参考与交流。 -->

---
layout: default
---
## 参考文献
- Miao Y. et al. Ranked Keyword Search Over Encrypted Cloud Data. IEEE TSC 2022.
- Cao N. et al. Privacy-Preserving Multi-Keyword Ranked Search. IEEE TPDS 2013.
- Zhang Y. et al. File-Injection Attacks on Searchable Encryption. USENIX Security 2016.
- Najafi M. et al. Forward Secure Ranked Searchable Encryption. ACM CCS 2020.
- Bost R. et al. Forward Secure Searchable Encryption. ACM CCS 2016.

<!-- 本页列出核心参考，提醒听众可进一步查阅基础工作与前向安全研究线索。 -->

---
layout: end
---
# 谢谢！
## 欢迎提问

<!-- 本页邀请听众交流，提示可以围绕参数选型、部署路径与安全增强方案展开讨论。 -->
