---
theme: seriph
background: /image/slides/image.png
title: "Prϵϵmpt: Sanitizing Sensitive Prompts for LLMs"
info: |
  ## 面向 LLM 的敏感提示词净化方案
  把 prompt 中可独立识别的敏感 token 先在本地净化，再交给云端 LLM。
class: pre
drawings:
  persist: false
transition: slide-left
mdc: true
highlighter: shiki
lineNumbers: false
katex: true
hideInToc: true
---

<div class="pre-cover">
  <div class="pre-kicker">论文分享 · 隐私保护 LLM</div>

  <div class="pre-title">Prϵϵmpt</div>
  <div class="pre-subtitle">Sanitizing Sensitive Prompts for LLMs</div>

  <div class="pre-lead mt-7">
    一篇关于 <b>LLM 推理阶段 prompt 隐私保护</b> 的论文：在 prompt 进入云端模型之前，先处理其中可识别的敏感 token。
  </div>

  <div class="pre-meta mt-7">
    <span>NDSS 2026 · CCF A</span>
    <span>University of Michigan · University of Toronto · UW-Madison · UC San Diego</span>
  </div>

  <div class="absolute bottom-8 right-8 text-sm" style="color:var(--pre-muted);">主讲人：王宇哲</div>
</div>

<!--
今天我分享的论文是 Prϵϵmpt，题目是 Sanitizing Sensitive Prompts for LLMs。这篇论文发表在 NDSS 2026。NDSS 是网络与系统安全方向的顶会，在 CCF 推荐目录里属于 A 类会议。

这篇论文解决的是一个比较实际的问题：用户把 prompt 发给云端 LLM 之前，能不能先把里面的敏感 token 处理掉，同时尽量不影响模型回答。这里的敏感 token 可以是姓名、身份号、年龄、工资，也可以是病历里的诊断信息。

我选这篇论文，是因为它刚好接在我之前做的 RAG 隐私方案后面。RAG 就是检索增强生成，先从资料库里找相关内容，再把这些内容交给 LLM 生成回答。我原来的方案主要保护检索阶段，也就是让云服务器在检索时看不到用户查询和相关数据。

但 RAG 还有后半段。检索结束以后，客户端会把结果解密，再把明文 context 和用户问题一起交给 LLM。这里的 context 指检索出来、准备给模型参考的上下文材料。这样一来，检索阶段虽然保护住了，生成阶段的 LLM 还是会接触到隐私信息。

所以我关注的是这个缺口：能不能在 context 和 prompt 送进 LLM 之前，先做一次本地预处理。Prϵϵmpt 的思路正好在这里：先处理 prompt 里的敏感 token，再把处理后的 prompt 发给云端模型。

机制先不展开。后面会依次说明它怎么识别 token、怎么处理不同类型的字段、实验效果能到什么程度。

Q&A 预案：
Q：为什么选这篇？
A：因为它正好补的是 RAG 生成前这一段。我之前更关注检索侧，但检索结果最终还是要进 LLM。Prϵϵmpt 提供了一个可以放在生成前的预处理思路，所以和我的方向是连得上的。
-->

---
layout: default
class: pre
---

## 本次分享主线

<div class="pre-lead mt-4">
这篇论文可以先看成一个问题：<b>能不能在不改云端 LLM API 的前提下，先在本地降低 prompt 里敏感 token 的暴露风险。</b>
</div>

<div class="pre-grid3 mt-8">
  <div class="pre-card pre-card--risk">
    <div class="pre-card-title">为什么需要</div>
    <p>推理阶段的 prompt 会直接交给云端 LLM。训练数据隐私保护管不到这一步。</p>
  </div>
  <div class="pre-card pre-card--brand">
    <div class="pre-card-title">大致思路</div>
    <p>先在用户本地找出敏感 token，再根据它在任务里的作用决定怎么处理。</p>
  </div>
  <div class="pre-card pre-card--proof">
    <div class="pre-card-title">怎么判断</div>
    <p>看三件事：保护范围有没有说清楚，回答会不会明显变差，能不能直接接到现有 LLM API 前面。</p>
  </div>
</div>

<div class="pre-callout mt-8">
整场汇报按这条路线走：先讲问题，再讲设计，最后看实验和限制。具体机制和数据后面展开。
</div>

<!--
汇报路线先定下来。

第一部分先讲问题。这里不是训练数据泄露，而是用户每次调用 LLM 时，prompt 本身就要交给服务端。这个输入里经常有真实数据。

第二部分讲方法。Prϵϵmpt 没有把整段 prompt 加密，也不是简单删掉敏感字段。它先在本地找出敏感 token，再判断这个 token 对当前任务有没有用，然后选择不同的处理方式。

第三部分看实验和限制。我主要关心三个问题：第一，它到底保护哪些内容；第二，处理以后回答质量会不会掉；第三，它能不能作为一层预处理，接到现有 LLM API 前面。


Q&A 预案：
Q：这是不是只是 PII 脱敏？
A：不完全是。PII 指可以识别到个人的信息，比如姓名、证件号、手机号。普通打码通常只关心把敏感值藏起来；Prϵϵmpt 还要求处理后的 prompt 仍然能让 LLM 正常完成任务。具体差别后面讲分类和净化机制时再展开。
-->

---
layout: default
class: pre
---

## Prompt 隐私问题

<div class="pre-flow mt-7">
  <div class="pre-node">用户 prompt<span>医疗、财务、身份信息</span></div>
  <div class="pre-arrow"></div>
  <div class="pre-node pre-node--risk">云端 LLM<span>提供商可见输入</span></div>
  <div class="pre-arrow pre-arrow--risk"></div>
  <div class="pre-node pre-node--risk">隐私泄露<span>推理阶段发生</span></div>
</div>

<div class="pre-grid2 mt-8">
  <div>
    <div class="pre-section-title">普通调用</div>
    <div class="pre-example mt-3">请总结这份体检报告：姓名、身份号、诊断结果、保险信息...</div>
    <ul class="pre-list">
      <li>服务商处理请求时就能看到输入。</li>
      <li>“不用于训练”不能解决输入可见问题。</li>
    </ul>
  </div>
  <div>
    <div class="pre-section-title">few-shot 调用</div>
    <div class="pre-example mt-3">示例1：病历文本 → 抽取结果<br/>示例2：真实病历 → 抽取结果</div>
    <ul class="pre-list">
      <li>prompt 不只包含问题，还包含样本。</li>
      <li>样本越真实，暴露面越大。</li>
    </ul>
  </div>
</div>

<div class="pre-cite">Prϵϵmpt · 关注 inference-time prompt privacy，而不是训练数据隐私。</div>

<!--
先看背景：为什么 prompt 隐私要单独拿出来讲？

很多 LLM 隐私问题讨论的是训练阶段，比如模型会不会记住训练样本，能不能被别人抽出来。但真实使用云端 LLM 时，还有一个更直接的问题：prompt 要发给服务端。

举个例子，医生把体检报告发给 GPT 帮忙总结，prompt 里可能有病人姓名、身份号、诊断结果和保险信息。服务商就算承诺“不用这批数据训练”，处理请求时仍然能看到输入。

few-shot 会让这个问题更明显。few-shot 简单说，就是在 prompt 里放几条示例，让模型照着格式回答。麻烦在于，这些示例经常来自真实数据。做病历信息抽取时，用户可能直接贴几条真实病历给模型看。这样 prompt 里就不只是一个问题，而是几条完整样本。

所以这篇论文看的是 inference-time prompt privacy，也就是推理阶段的输入隐私。它先不讨论模型以后会不会记住，而是问这一次调用里，服务端能不能少看到一些敏感内容。

Q&A 预案：
Q：few-shot 是什么？
A：few-shot 就是在 prompt 里放少量示例，让模型根据这些示例理解任务格式。比如先给它两三条“病历文本 -> 提取结果”的例子，再让它处理新的病历。

Q：为什么 few-shot 会放大隐私问题？
A：因为示例往往不是凭空编的，而是从真实数据里拿的。原本一次 prompt 可能只包含一个用户的问题；加了 few-shot 后，prompt 里还会多出几条完整样本，里面可能带姓名、诊断、账号或其他隐私字段，暴露面就变大了。

Q：服务商不训练用户数据，风险还大吗？
A：风险还是在。这里担心的是请求内容在服务端可见，可能进入日志、审计、调试链路或内部访问范围。不训练只能解决训练污染，不能解决输入可见。
-->

---
layout: default
class: pre
---

## 现有方案不足

<div class="pre-grid3 mt-6">
  <div class="pre-card">
    <div class="pre-card-title">密码学推理</div>
    <p>HE / MPC 这类加密推理可以给强隐私，但代价太高。论文引用的方案在 BERT 上单次推理超过 16 分钟。</p>
  </div>
  <div class="pre-card">
    <div class="pre-card-title">LLM 改写</div>
    <p>本地 LLM 可以生成代理 prompt，但很难证明它一定不泄露敏感信息。</p>
  </div>
  <div class="pre-card">
    <div class="pre-card-title">直接 DP 加噪</div>
    <p>对整段文本或文本向量加差分隐私噪声，容易破坏语义、格式和长 prompt 的可用性。</p>
  </div>
</div>

<div class="pre-split mt-8">
  <div class="pre-panel pre-panel--risk">
    <div class="pre-section-title">共同问题</div>
    <p>它们大多把所有敏感信息当成同一类问题处理：要么全加密，要么全改写，要么全加噪。</p>
  </div>
  <div class="pre-panel pre-panel--proof">
    <div class="pre-section-title">Prϵϵmpt 的做法</div>
    <p>先问一个更小的问题：这个 token 在当前任务里到底起什么作用？然后再决定怎么处理。</p>
  </div>
</div>

<!--
接下来要回答一个问题：为什么不直接用已有方案？

第一种是密码学推理，比如 HE 或 MPC。HE 是同态加密，MPC 是多方安全计算，简单说就是让服务端在看不到明文的情况下参与计算。这个方向隐私强，但成本太高。论文引用的对比里，BERT 级别的一次隐私推理已经超过 16 分钟。这里还是 BERT，不是 GPT 这类更大的生成式模型。

第二种是本地 LLM 改写 prompt。它看起来轻，但很难给安全性结论。模型可能漏掉敏感字段，也可能把用户原意改坏。另外，它很难说清楚到底泄露了多少。

第三种是直接加噪。DP 是差分隐私，核心是用随机噪声降低单个输入被识别出来的风险。但如果对整段文本或文本向量加噪，问题会变复杂。文本向量可以理解成模型内部使用的一组数字表示；向量被扰乱以后，语义、格式和长上下文都可能被破坏。

所以这篇论文想避开两个极端：不想做成本很高的全加密推理，也不想只做没有证明的改写。它把问题收窄到 token 级字段，然后看不同 token 应该怎么处理。

下一页先看这个分类的出发点：LLM 做任务时，并不总是需要看到敏感字段的真实值。

Q&A 预案：
Q：16 分钟这个数字是不是有点过时？
A：具体数字会随着系统进步变化，但这里的结论不依赖这个精确值。全密码学推理和“在现有 LLM API 前做输入净化”不是一个成本档。
-->

---
layout: default
class: pre
---

## 关键观察

<div class="pre-grid2 mt-5">
  <div class="pre-card pre-card--brand">
    <div class="pre-card-title">格式型敏感 token</div>
    <div class="pre-example mt-3">My SSN is <b>055-46-6168</b>.</div>
    <p class="mt-4">翻译或格式化时，LLM 只需要知道“这是一个 SSN 格式的字符串”。真实数字通常不重要。</p>
    <div class="pre-tag">后面用可恢复机制处理</div>
  </div>
  <div class="pre-card pre-card--proof">
    <div class="pre-card-title">数值型敏感 token</div>
    <div class="pre-example mt-3">I am <b>50</b> and earn <b>500,000</b>.</div>
    <p class="mt-4">退休建议、金融分析、医疗建议会用到数值本身。这里不能任意替换。</p>
    <div class="pre-tag pre-tag--proof">后面用近似机制处理</div>
  </div>
</div>

<div class="pre-callout mt-8">
论文正式分类是 Category I / II；这里用“格式型”和“数值型”来对应它们对 LLM 的作用。
</div>

<!--
这是论文的出发点。

LLM 看到敏感字段时，不一定总是需要真实值。比如翻译 “My SSN is 055-46-6168”，模型主要需要知道这里是一个 SSN。真实号码是多少，对翻译结果基本没帮助。

但年龄、薪资、账户余额不一样。50 岁和 20 岁的退休建议不会一样，年薪 50 万和 5 万的财务建议也不会一样。这些字段如果随便替换，模型回答的其实就不是原来的问题。

所以这篇论文就把敏感 token 分成了两类：

1. 格式型敏感 token：
   后面会用“可恢复机制”去做处理。
2. 数值型敏感 token：
   后面会用“近似机制”去做处理


Q&A 预案：
Q：同一个字段在不同任务里作用会不会变？
A：会。年龄在翻译里可能只是普通数字，在金融或医疗建议里就会影响推理。论文按实体类型做相对保守的分类，好处是实现简单，代价是有些任务会多处理一点。
-->

---
layout: default
class: pre
---

## 方案局限性

<div class="pre-lead mt-4">
Prϵϵmpt 不是完整的 prompt 隐私方案。它只处理 <b>NER 找到的敏感字段</b>，不理解整段内容是否敏感。
</div>

<div class="pre-grid3 mt-7">
  <div class="pre-card pre-card--proof">
    <div class="pre-card-title">能保护什么</div>
    <p>姓名、SSN、信用卡号、年龄、薪资这类字段级信息。</p>
  </div>
  <div class="pre-card pre-card--risk">
    <div class="pre-card-title">依赖什么</div>
    <p>NER 必须先识别出来。漏检的字段不会进入净化流程，会原样发给云端。</p>
  </div>
  <div class="pre-card pre-card--risk">
    <div class="pre-card-title">不保护什么</div>
    <p>整句话透露出的敏感事实，例如健康状况、家庭处境、业务秘密。</p>
    <div class="pre-example mt-3">My neighbor is in an abusive marriage.</div>
  </div>
</div>

<div class="pre-callout mt-8">
后面所有机制、证明和实验结果，都要放在这个范围内理解：字段被识别出来以后，系统怎么净化它。
</div>

<!--
Prϵϵmpt 有价值，但不能把它说成完整的 prompt privacy 方案。它的承诺范围需要先讲清楚。

第一，它能保护的是字段级信息。比如姓名、SSN、信用卡号、年龄、薪资。这些字段单独拿出来就可能泄露隐私，所以论文先把目标收窄到这些 token。

第二，它依赖 NER。NER 是 named entity recognition，中文叫命名实体识别。放在这篇论文里，可以简单理解成：先从 prompt 里找出姓名、证件号、年龄、金额这些敏感片段。只有被 NER 找出来的 token，后面才会进入加密或加噪流程。漏检的字段不会被保护。

第三，它不处理整句话透露出的隐私。比如 “My neighbor is in an abusive marriage”，这句话没有身份号，也没有姓名，但这句话本身已经透露了一个敏感事实。NER 很可能找不到一个明确要替换的字段，Prϵϵmpt 也不会判断这句话该不该发给 LLM。

结论很简单：它是一层字段净化器。它可以降低 token 级敏感值暴露，但不能替代内容审核、访问控制，也不能保证整段 prompt 都安全。后面讲系统流程、安全性证明和实验时，都要记住这个前提。

Q&A 预案：
Q：保护范围这么窄，还有价值吗？
A：有，但不能把它说大。它处理的是最直接的一类泄露：身份字段和数值字段。实际使用时，可以把它放在现有 LLM API 前面，先处理这些字段；至于整段内容是否允许发送，还需要系统另外判断。
-->

---
layout: default
class: pre
---

## 系统流程

<div class="pre-figure pre-figure--system mt-4">
  <img src="/image/Preempt/2f2a7f3969ce3f5d87bbee14b235a35b25c32acb2a9cb0d956f697afbc45d231.jpg" alt="Prϵϵmpt system overview" />
  <div class="pre-figcaption">Figure 1: 用户本地注册、净化 prompt、发送给不可信 LLM，再对响应反净化。</div>
</div>

<div class="pre-grid3 mt-5">
  <div class="pre-stat"><div class="num">1</div><div class="lbl">Configuration Manager<br/>生成密钥和参数</div></div>
  <div class="pre-stat"><div class="num">2</div><div class="lbl">Sanitizer<br/>NER 找敏感片段，再分类净化</div></div>
  <div class="pre-stat"><div class="num">3</div><div class="lbl">Desanitizer<br/>恢复格式型 token</div></div>
</div>

<div class="pre-cite">系统图对应论文 Figure 1：客户端本地处理，LLM API 不需要修改。</div>

<!--
系统流程对应原文 Figure 1。

这个系统分成两个阶段看会更清楚：一次性的注册阶段，和每次调用 LLM 时的净化阶段。

第一步是注册。Configuration Manager，也就是配置管理模块，会为用户生成格式保留加密用的密钥，也会初始化每类敏感 token 的格式空间。比如 SSN、信用卡号、电话号码，各自有自己的格式。用户还会指定数值加噪的隐私参数 epsilon，也就是控制噪声大小的参数。后面每一次净化，都会用这些本地配置。

第二步是输入 prompt 以后，Sanitizer，也就是净化器，先做 type annotation，中文可以叫类型标注。论文里的 type annotator，也就是类型标注器，是用 NER 实现的。它先找出 prompt 里的敏感 token，再标注它属于哪一类：Category I 是格式型字段，Category II 是数值型字段。

第三步是 pre-processor，也就是预处理器。它会做两件事：一是统计数值型 token 的数量，用来分配 epsilon；二是生成 helper string Ψ，可以理解成辅助字符串，用来记录 token 之间的函数依赖。函数依赖就是一个字段可以由另一个字段算出来，比如出生年份可以由当前年份和年龄推出来。年龄和出生年份不能分别乱加噪，否则净化后会前后矛盾。

第四步才是逐个 token 净化。非敏感 token 不动。格式型token用格式保留加密，所以输出还是同格式字段；数值型 token 用带距离的本地差分隐私加噪，所以输出是接近原值的数值。之后 post-processor，也就是后处理器，会根据 helper string Ψ 修正依赖字段，得到最终 sanitized prompt，也就是净化后的 prompt。

第五步，客户端把 sanitized prompt 发给不可信 LLM。云端只看到净化后的输入，不需要改 LLM API。LLM 返回回答以后，客户端再跑 Desanitizer，也就是反净化器。格式型字段可以用加密密钥解回来；数值型字段默认不反解，因为它本来就是用近似值换隐私。

所以这张图的重点是：敏感信息的识别、参数、加密、加噪和反净化都在客户端侧完成；云端 LLM 只参与普通推理。

Q&A 预案：
Q：如果不维护映射表，怎么恢复？
A：格式型字段靠 FPE 密钥恢复，不需要表。数值型字段本来就不是为了恢复精确值，而是让 LLM 在近似值上完成任务，所以通常不会反解。
-->

---
layout: default
class: pre
---

## 具体方案：Sanitizer 怎么跑

<div class="pre-split mt-3" style="grid-template-columns: 0.92fr 1.08fr; gap: 0.9rem;">
  <div class="pre-figure pre-figure--compact">
    <img src="/image/Preempt/preempt_algorithm1.png" alt="Prϵϵmpt sanitization algorithm" style="max-height: 330px; object-fit: contain;" />
    <div class="pre-figcaption">Algorithm 1: 净化流程。</div>
  </div>
  <div>
    <div class="pre-section-title">页面符号</div>
    <div class="pre-grid2 mt-2" style="gap: 0.45rem;">
      <div class="pre-mini" style="padding: 0.38rem 0.5rem;"><b style="font-size:1.08rem;">ρ</b><br/><span>原始 prompt</span></div>
      <div class="pre-mini" style="padding: 0.38rem 0.5rem;"><b style="font-size:1.08rem;">ρ̂</b><br/><span>净化后的 prompt</span></div>
      <div class="pre-mini" style="padding: 0.38rem 0.5rem;"><b style="font-size:1.08rem;">ε</b><br/><span>总隐私预算</span></div>
      <div class="pre-mini" style="padding: 0.38rem 0.5rem;"><b style="font-size:1.08rem;">t</b><br/><span>数值型 token 数量</span></div>
    </div>
    <div class="pre-section-title mt-3">预算分配的含义</div>
    <ul class="pre-list" style="font-size: 0.78rem; line-height: 1.42;">
      <li>ε 不是输入数据，而是用户设定的隐私预算。</li>
      <li>ε 越大，噪声越小，回答更准，但隐私更弱。</li>
      <li>有 t 个数值型 token 时，每个 token 使用 ε/t。</li>
      <li>helper string Ψ 记录字段依赖，供后处理修正。</li>
    </ul>
  </div>
</div>

Sanitizer 接口：$\mathsf{Sanitize}(\rho,K_U,\epsilon)\rightarrow \hat{\rho}$

预算分配：$\epsilon_i=\epsilon/t$，只对数值型 token 分配预算。

<!--
Prϵϵmpt 的 Sanitizer 可以先理解成一个本地函数。它接收三个输入：原始 prompt rho、用户密钥 KU、总隐私预算 epsilon。它输出净化后的 prompt rho hat，也就是准备发给云端 LLM 的版本。用公式写就是：$\mathsf{Sanitize}(\rho,K_U,\epsilon)\rightarrow \hat{\rho}$。

这里先把 epsilon 说清楚。epsilon 不是 prompt 里的信息，也不是要从公式里推导出什么隐藏内容。它是用户提前设定的隐私预算。可以把它理解成“这次数值净化允许暴露多少信息”的控制旋钮。epsilon 越大，mLDP 加的噪声越小，模型回答更准，但隐私更弱；epsilon 越小，噪声越大，隐私更强，但回答更容易偏。

真正的执行过程是按 token 逐个处理的。

第一，系统先运行类型标注器 M_tau。M_tau 的输入是原始 prompt，输出是一串带类型的 token。比如一句话里有姓名、SSN、年龄、金额，M_tau 会用NER把这些片段标出来。NER 本身不提供隐私保护，它只是入口。没有被识别出来的字段，后面不会被 FPE 或 mLDP 处理。

第二，预处理器 M_Pre 统计数值型 token 的数量 t，并生成 helper string Ψ。这里的 t 只统计数值型 token，不是所有 token。t 的作用是分配隐私预算。公式是 $\epsilon_i=\epsilon/t$，意思是第 i 个数值 token 使用总预算的 t 分之一。

这个公式要表达的是“预算拆分”，不是“信息推导”。假设总预算是 epsilon，prompt 里有 t 个数值字段。如果每个字段都用完整 epsilon，那么多个字段合在一起，整体隐私损失会超过用户设定的总预算。所以论文把总预算平均分给这些数值 token。每个数值 token 用自己的 $\epsilon_i$ 去做 mLDP 扰动，最后整体仍然受总预算 epsilon 控制。

helper string Ψ 用来记录字段之间的依赖关系，比如年龄和出生年份。

第三，系统逐个处理 token。非敏感 token 原样保留；格式型 token 走 FPE，输出仍然像同类型字段；数值型 token 走 mLDP，输出接近原值的近似值。Prϵϵmpt 不是把整段 prompt 交给另一个模型重写，而是在本地做局部净化。

第四，后处理器 M_Post 根据 helper string Ψ 修正依赖字段。举个例子，如果原文是“我 25 岁，出生于 2001 年”，系统不应该把年龄变成 27，同时把出生年独立变成 1991。更合理的做法是先扰动年龄，再按依赖关系推导出生年。这样净化后的文本仍然前后一致。

Q&A 预案：
Q：为什么要把 epsilon 除以 t？
A：因为同一个 prompt 里可能有多个数值型 token。把预算分给每个 token，可以用组合性质控制总隐私损失，不让多字段叠加后超过用户设定的总预算。

Q：这个公式是在算什么？
A：它不是在算原始信息，也不是让我们推导出敏感值。它只是在分配隐私预算：总预算是 epsilon，数值型 token 有 t 个，所以每个数值 token 分到 epsilon/t。
-->

---
layout: default
class: pre
---

## FPE：保留格式

<div class="pre-split mt-5">
  <div>
    <div class="pre-section-title">它做什么</div>
    <p>FPE（Format-Preserving Encryption）是一种加密方式：密文和明文属于同一个格式空间。</p>
    <div class="pre-equation mt-4">SSN: 055-46-6168 → 569-83-4469</div>
    <p class="mt-4">没有密钥的人看到的是另一个合法 SSN；有密钥的用户可以无损解密。</p>
  </div>
  <div>
    <div class="pre-section-title">它适合什么</div>
    <table class="pre-table mt-2">
      <thead>
        <tr><th>类型</th><th>原因</th></tr>
      </thead>
      <tbody>
        <tr><td>SSN / 信用卡号</td><td>格式比具体值重要</td></tr>
        <tr><td>电话号码 / IP</td><td>结构稳定，便于保留</td></tr>
        <tr><td>姓名</td><td>可替换成另一个姓名形态</td></tr>
      </tbody>
    </table>
  </div>
</div>

<div class="pre-callout mt-7">
FPE 主要保留格式：密文仍然像一个合法实体，LLM 不会因为输入形态被破坏而跑偏。
</div>

<!--
先看格式型字段，对应的是 FPE。

FPE 是 format-preserving encryption，中文可以说格式保留加密。普通加密会把 SSN 变成一串模型看不懂的字符；FPE 会把它变成另一个合法 SSN。长度、分隔符、字符集合都还在，只是具体值换了。

为什么要保留格式？因为 LLM 会看输入形态。模型看到的仍然是一个像 SSN 的字段，翻译、摘要、格式化时就不容易跑偏。回答回来以后，用户本地可以用密钥解回来。

这里的FPE也有边界。
第一，他依赖于足够大的格式空间。如果字段只有 M/F 两个值，或者只是一个很小的枚举集合，加密后的可猜范围就很小。

第二，比如姓名这种实体，形式可以保留，但姓名背后的文化、性别、地区信息可能会丢。

Q&A 预案：
Q：姓名加密后可能不像真实姓名，会不会影响 LLM？
A：可能会。如果任务只需要把姓名当实体占位符，影响不大；如果任务要判断姓名来源、性别或文化背景，FPE 后这些语义就不可靠了。
-->

---
layout: default
class: pre
---

## mLDP：公式不是方法，是验收标准

<div class="pre-split mt-4">
  <div>
    <div class="pre-section-title">公式在说什么</div>
    <p style="font-size: 0.82rem; line-height: 1.5;">限速 120 不教你怎么开车。mLDP 公式也不教你怎么加噪，它只规定加噪结果必须满足什么条件。</p>
    <div class="pre-figure pre-figure--compact mt-3">
      <img src="/image/Preempt/preempt_mldp_formula.png" alt="mLDP definition formula" style="max-height: 105px; object-fit: contain;" />
    </div>
    <div class="pre-callout mt-3" style="font-size: 0.76rem; line-height: 1.42; padding: 0.55rem 0.7rem;">
      例子：x = 50，x' = 52，O = 输出在 51 到 53 之间。mLDP 要求 50 岁和 52 岁产生 O 的概率不能差太多。
    </div>
  </div>
  <div>
    <div class="pre-section-title">论文实际怎么做</div>
    <p style="font-size: 0.82rem;">从 Gamma 分布采样偏移量，加到真实值上：</p>
    <ul class="pre-list" style="font-size: 0.78rem; line-height: 1.42; margin-top: 0.3rem;">
      <li>真实值 x = 50 岁</li>
      <li>采样偏移量 r = +2</li>
      <li>输出 52，发给云端</li>
      <li>但 52 岁本身也可能输出 52</li>
    </ul>
    <p style="font-size: 0.76rem; margin-top: 0.45rem; color: var(--pre-muted);">所以云端看到 52，不能直接判断原值是 50 还是 52。</p>
  </div>
</div>

<!--
再看数值型字段。这里用 mLDP，但要先搞清楚一件事：这个公式不是方法，是验收标准。mLDP 公式不教你怎么加噪声，只规定加噪结果必须满足一个不等式。满足了算合格，不满足就不安全。

公式 $\Pr[M(x)\in O]\le e^{\epsilon d(x,x')}\Pr[M(x')\in O]$ 可以直接按页面上的例子读。

这里固定 x = 50，x' = 52，O 表示"输出在 51 到 53 之间"。左边 $\Pr[M(50)\in O]$，就是原值 50 岁时，净化结果落在 51 到 53 的概率。右边 $\Pr[M(52)\in O]$，就是原值 52 岁时，净化结果落在同一个范围的概率。

mLDP 要求这两个概率不能差太多。原因很直接：如果 50 岁和 52 岁都有可能产生 52 这一类输出，云端只看到 52，就不能直接反推出原值是 50 还是 52。

实际怎么加噪？论文从 Gamma 分布里采样一个随机偏移量，加到真实值上。比如原值 50，采到偏移量 +2，输出就是 52。ε 控制这个偏移量的大小：ε 越小，噪声越大，隐私越强；ε 越大，噪声越小，回答更准。


Q&A 预案：
Q：税务或医疗剂量这种精确计算，mLDP 还能用吗？
A：如果小误差会改变决策就不行。mLDP 适合建议、比较、粗粒度问答这类对近似值容忍度高的任务。
-->

---
layout: default
class: pre
---

## 字段依赖

<div class="pre-grid2 mt-5">
  <div class="pre-card pre-card--risk">
    <div class="pre-card-title">独立加噪的问题</div>
    <div class="pre-example mt-3">My age is 25, I was born in 2001.</div>
    <p class="mt-4">如果 age 和 year 分别独立加噪，净化后的文本可能前后矛盾。</p>
  </div>
  <div class="pre-card pre-card--proof">
    <div class="pre-card-title">helper string Ψ 记录关系</div>
    <div class="pre-example mt-3">year = 2026 - age</div>
    <p class="mt-4">系统只对 age 加一次噪声，year 由后处理重新计算。</p>
  </div>
</div>

<div class="pre-flow mt-7">
  <div class="pre-node">原始值<span>age = 25, year = 2001</span></div>
  <div class="pre-arrow"></div>
  <div class="pre-node pre-node--proof">只扰动 age<span>age' = 27</span></div>
  <div class="pre-arrow"></div>
  <div class="pre-node">推导 year'<span>2026 - 27 = 1999</span></div>
</div>

<div class="pre-callout mt-6" style="font-size: 0.88rem; line-height: 1.5;">
净化结果仍然一致：age' = 27，year' = 1999。这里的关键不是多加一次噪声，而是用已经扰动后的 age' 推导相关字段。
</div>

<!--
还有一个细节很容易出问题：同一个 prompt 里的敏感值经常有关联。

比如一句话里同时有年龄和出生年份。如果年龄加一次噪声，出生年份再独立加一次噪声，净化后的文本可能前后对不上。模型看到这种矛盾，回答质量就会受影响。

Prϵϵmpt 用 helper string Ψ 表达这种依赖关系。helper string Ψ 可以理解成一份本地辅助说明，告诉后处理器哪些字段之间有关联。做法是只扰动源头值，再用后处理推导相关值。

年龄和出生年份的关系可以写成 $\mathrm{year}=2026-\mathrm{age}$。系统只需要对 age 加一次噪声。比如 $\mathrm{age}=25$ 被扰动成 $\mathrm{age}'=27$，那么 $\mathrm{year}'$ 就由 $2026-27$ 得到 1999。这样净化后的文本仍然前后一致。

这里用到了差分隐私的后处理性质：只基于已经净化的值继续计算，不会额外增加隐私损失。简单说，后处理只看已经加噪后的结果，不再接触原始敏感值。它解决的不是隐私更强的问题，而是净化后的 prompt 不要自相矛盾。

Q&A 预案：
Q：helper string Ψ 是怎么来的？
A：论文给了两种来源：用户提供，或者用本地模型推断。helper string Ψ 可以先理解成“字段依赖说明”。工程上比较麻烦的是第二种，依赖关系一旦推断错，后面的计算虽然还会继续跑，但回答就可能变差。
-->

---
layout: default
class: pre
---

## 安全性证明

<div class="pre-proof-grid mt-3">
  <div>
    <div class="pre-section-title">Privacy game</div>
    <ol class="pre-list" style="font-size: 0.82rem; line-height: 1.46;">
      <li>攻击者给出两个结构相同的 prompt：ρ₀ 和 ρ₁。</li>
      <li>系统随机选择其中一个，返回净化后的 prompt。</li>
      <li>攻击者只能看净化结果，猜原始 prompt 是哪个。</li>
    </ol>
    <div class="pre-example mt-3" style="font-size: 0.82rem; line-height: 1.42;">目标：净化结果不应该让攻击者明显猜中真实输入。</div>
  </div>
  <div>
    <div class="pre-section-title">安全性结论</div>
    <div class="pre-figure pre-figure--compact mt-3">
      <img src="/image/Preempt/preempt_privacy_bound.png" alt="Prϵϵmpt privacy bound" style="max-height: 125px; object-fit: contain;" />
    </div>
    <ul class="pre-list mt-3" style="font-size: 0.82rem; line-height: 1.46;">
      <li><b>Adv</b>：攻击者优势，越接近 0 越好。</li>
      <li><b>e^(lε)</b>：数值字段的可区分度。</li>
      <li><b>negl(κ)</b>：破解 FPE 的概率，可忽略。</li>
    </ul>
  </div>
</div>

安全性上界：$\mathrm{Adv}\le e^{l\epsilon}+\mathrm{negl}(\kappa)$

<div class="pre-proof-steps mt-4">
  <div class="pre-mini">
    <div class="pre-mini-title">格式型字段</div>
    <p>靠 FPE。没有密钥时，密文看起来像同格式的另一个值。</p>
  </div>
  <div class="pre-mini">
    <div class="pre-mini-title">数值型字段</div>
    <p>靠 mLDP。数值越接近，净化结果越难区分。</p>
  </div>
  <div class="pre-mini">
    <div class="pre-mini-title">hybrid argument</div>
    <p>构造中间 prompt，每次只替换一个 token，把多字段问题拆成单字段问题。</p>
  </div>
</div>

<div class="pre-callout mt-4" style="font-size: 0.82rem; line-height: 1.42; padding: 0.56rem 0.75rem;">
  证明边界：只覆盖已识别并净化的 token；NER 漏检和整句话语义泄露不在这个结论里。
</div>

<!--
安全性证明可以按一个猜谜游戏讲。

攻击者先给两个 prompt，记作 ρ0 和 ρ1。这两个 prompt 结构相同，允许泄露的信息也相同，比如非敏感文本、token 类型和格式。系统随机选其中一个做净化，然后把净化结果交给攻击者。攻击者的任务是猜系统到底选的是 ρ0 还是 ρ1。

Adv 就是在衡量攻击者比随机猜强多少。如果攻击者只能随机猜，成功率大约是二分之一，Adv 接近 0。Adv 越大，说明净化结果越能帮助攻击者判断真实输入。

公式右边有两项。第一项 $e^{l\epsilon}$ 来自数值型字段，因为数值字段用 mLDP。l 表示两个候选数值之间的距离范围，epsilon 是隐私预算。l 越大，或者 epsilon 越大，两个输入越容易区分。第二项 $\mathrm{negl}(\kappa)$ 来自格式型字段，因为格式字段靠 FPE。没有密钥时，攻击者破解 FPE 的概率可以忽略。

格式型字段靠 FPE，数值型字段靠 mLDP；多个字段时，用逐个替换的 hybrid argument，把多个 token 的差异拆成一个 token 一个 token 来看。

hybrid argument 可以理解成一种“中间状态”证明方法。假设 ρ0 和 ρ1 有 5 个敏感 token 不一样，直接比较整段 prompt 会很难。证明会构造一串中间 prompt：第一个中间状态只把第 1 个 token 从 ρ0 换成 ρ1，第二个中间状态再换第 2 个 token，依次换到第 5 个。这样每一步只差一个 token。

如果攻击者能区分最开始的 ρ0 和最后的 ρ1，那他一定在某两个相邻中间状态之间看出了差别。但相邻状态只差一个 token，所以这个问题就退化成“单个 token 的净化是否安全”。格式型 token 用 FPE 保证，数值型 token 用 mLDP 保证。这样就能把多字段 prompt 的隐私问题拆成单字段安全性问题。

这个证明的边界也很明确：它只覆盖已经被 NER 找到并净化的 token。漏检字段、整句话本身透露出的语义，不在这个证明范围里。

Q&A 预案：
Q：这个安全性证明是不是等价于上下文隐私？
A：不是。它只证明净化后的敏感 token 难以区分，不证明整段上下文安全。

Q：e^{lε} 如果很大，这个 bound 还有意义吗？
A：有，但它保护的是距离相近的数值；两个值差得越远，本来就越容易区分。
-->

---
layout: default
class: pre
---

## 实用性分析

<div class="pre-grid2 mt-5">
  <div class="pre-card pre-card--proof">
    <div class="pre-card-title">不依赖真实值</div>
    <p>翻译、格式化、引用等任务，LLM 对格式型 token 的具体值不敏感。</p>
    <div class="pre-example mt-3">My SSN is 055-46-6168.</div>
    <div class="pre-equation mt-4">净化 → LLM → 反净化 ≈ 原始回答</div>
  </div>
  <div class="pre-card pre-card--brand">
    <div class="pre-card-title">依赖近似值</div>
    <p>退休建议、金融问答、数值比较等任务，需要数值接近原值，但不总是需要完全精确。</p>
    <div class="pre-example mt-3">I am 50 and earn 500,000.</div>
    <div class="pre-equation mt-4">误差 ≈ 数值噪声带来的输出变化</div>
  </div>
</div>

<div class="pre-callout mt-8">
论文没有证明“输入小改动，回答就一定小改动”；它主要通过实验观察这种近似处理是否还能保住答案质量。
</div>

<!--
安全性讲完以后，还要看可用性。这里可以分两类任务。

第一类是不依赖真实值的任务。翻译最典型。SSN 换成另一个合法 SSN，句子怎么翻基本不受影响；最后再反净化，用户看到的还是原来的值。

第二类依赖数值，但允许近似。比如退休建议、金融问答、数值比较。模型要知道大概年龄、大概金额，但很多情况下不需要完全精确到原值。

论文这里的意思是：如果输入里的数值只是轻微变化，很多任务的回答也不应该完全变掉。比如 50 岁变成 48 岁，退休建议大概率还是同一类建议。

Q&A 预案：
Q：这能算对真实 LLM 的严格证明吗？
A：不能。它只是说明这类近似处理为什么可能可用，真正是否影响答案，还要看翻译、RAG、长上下文 Q/A 和金融 Q/A 的实验。
-->

---
layout: default
class: pre
---

## 实验结果

<div class="pre-split mt-4">
  <div>
    <table class="pre-table pre-table-lg">
      <thead>
        <tr>
          <th>任务</th>
          <th>结果</th>
          <th>指标说明</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>翻译</td>
          <td>BLEU 下降通常小于 0.02</td>
          <td>BLEU：译文和参考译文的连续词片段相似度</td>
        </tr>
        <tr>
          <td>RAG</td>
          <td>准确率 100%</td>
          <td>RAG：先检索 context，再基于 context 回答</td>
        </tr>
        <tr>
          <td>长上下文 Q/A</td>
          <td>Prϵϵmpt STS 0.934；Papillon 0.854</td>
          <td>Papillon：代理改写基线；STS 越高，回答语义越接近</td>
        </tr>
        <tr>
          <td>金融多轮 Q/A</td>
          <td>ε=2.0 时中位相对误差 2.44%</td>
          <td>相对误差：偏离原答案的比例；中位数：一批样本中间那个</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="pre-figure pre-figure--compact">
    <img src="/image/Preempt/cf6083a196e2412af7adac2e45e6b9caed62d6634cdf7194d2f4004a863ab016.jpg" alt="Financial QA median relative error" />
    <div class="pre-figcaption">Figure 2: 金融多轮 Q/A 中，ε 增大时中位相对误差下降。</div>
  </div>
</div>

<!--
实验我按四组结果讲，不逐个表格展开。

第一组是翻译。指标是 BLEU，可以简单理解成译文和参考译文有多少连续词片段重合。格式型字段替换以后，BLEU 基本不变，很多配置下降小于 0.02。这和前面的判断一致：翻译通常不需要知道真实 SSN 或真实姓名。

第二组是 RAG，论文报告准确率 100%。RAG 就是先检索 context，再基于 context 回答。这里的 question 是用户问题，context 是检索出来的参考材料。两者要一起净化，而且同一个敏感属性要保持一致；否则匹配关系会断。

第三组是长上下文 Q/A。论文用 STS，也就是语义相似度，看两段回答意思有多接近。这里 Papillon 是对比基线，它的思路是先用代理模型改写 prompt，再把改写后的 prompt 交给云端模型。Prϵϵmpt 的 STS 是 0.934，Papillon 是 0.854。在这组任务上，Prϵϵmpt 的回答更接近原始回答。

第四组是金融多轮 Q/A，用的是 ConvFinQA。ConvFinQA 是一个围绕财报表格做多步数值推理的数据集，对数字更敏感。epsilon 等于 2.0 时，中位相对误差是 2.44%。相对误差就是回答和原答案差了多少，再除以原答案；中位数就是把所有样本误差排个序，取中间那个，避免被极端错误带偏。噪声不太大时，回答还能接近原答案。但 ε=2.0 更偏可用性，不应该被讲成强隐私。

Q&A 预案：
Q：RAG 100% 样本量大吗？
A：不能按生产结论理解。这个实验更像机制验证，说明联合净化不会天然破坏匹配关系。真实生产 RAG 还会有召回、权限、上下文选择和长尾实体问题。
-->

---
layout: default
class: pre
---

## NER 覆盖率

<div class="pre-split mt-5">
<div>
<div class="pre-section-title">为什么 NER 关键</div>
<ul class="pre-list">
<li>NER 是 Named Entity Recognition，负责从 prompt 里找出姓名、年龄、金额等实体。</li>
<li>只有被识别出来的敏感 token，后面的 FPE / mLDP 才会生效。</li>
<li>漏检 token 不会被净化，会原样进入云端 LLM。</li>
</ul>
<div class="pre-panel pre-panel--risk mt-5">
<div class="pre-section-title">论文结果</div>
<p>UniNER 在翻译样本中识别约 96% 的唯一 PII 值；长上下文 Q/A 中识别约 92% 的唯一角色身份。</p>
</div>
</div>
<div class="pre-figure">
<img src="/image/Preempt/d5431b012fff1b3ba33f32935ab275f90639cbe35da0d492e0713cdbd5cf40fe.jpg" alt="English German BLEU with age privacy budget" />
<div class="pre-figcaption">Figure 3a: 年龄作为敏感 PII 时，BLEU 随隐私预算 ε 变化。</div>
</div>
</div>

<!--
实验里有两个点需要单独拿出来讲。第一个是 NER。

NER 是 named entity recognition，中文是命名实体识别。它负责从 prompt 里找出姓名、年龄、金额、证件号这些敏感片段。Prϵϵmpt 后面的 FPE 和 mLDP 都依赖这个入口。

论文里 UniNER 的结果还可以。UniNER 是论文使用的实体识别模型。翻译样本中，它识别并净化了大约 96% 的唯一 PII 值；长上下文 Q/A 里，大约 92% 的唯一角色身份被净化。PII 就是 personally identifiable information，也就是可以识别到个人的信息。

但这里不能只看 92% 和 96% 这两个数字。漏掉的那部分不会被后面的机制补救，会直接进入云端 LLM。换到医疗、金融、代码或企业内部文档，NER 的表现也可能变化。

右边这张图是原文 Figure 3 的一部分。它看的是年龄净化时 BLEU 随 epsilon 变化。对翻译来说，年龄噪声本身不是主要问题；真正决定隐私覆盖面的，还是敏感字段有没有被识别出来。

Q&A 预案：
Q：NER 漏检会不会破坏形式化证明？
A：对已经识别并净化的 token，机制的证明还在；但漏检 token 不受保护。论文用扩展泄露函数 L_NER 去刻画这个问题，也就是把“NER 会漏什么”写进模型里；这只是建模方式，不会让漏掉的字段变安全。
-->

---
layout: default
class: pre
---

## 格式保留

<div class="pre-split mt-5">
  <div>
    <div class="pre-section-title">RAG 事实检索对比</div>
    <table class="pre-table pre-table-lg mt-2">
      <thead>
        <tr><th>净化方式</th><th>准确率</th><th>含义</th></tr>
      </thead>
      <tbody>
        <tr><td>FPE</td><td>100%</td><td>保留原字段格式</td></tr>
        <tr><td>AES</td><td>70.97%</td><td>普通加密，格式被破坏</td></tr>
        <tr><td>错误格式随机替换</td><td>77.42%</td><td>看起来像替换，但不像原类型</td></tr>
      </tbody>
    </table>

<div class="pre-callout mt-5">
这里的结论不是“FPE 一定最好”，而是：LLM 会利用输入格式。把 SSN、日期、邮编这类字段变成不像原类型的字符串，会影响回答。
</div>
  </div>
  <div class="pre-figure">
    <img src="/image/Preempt/fc329362e1065749623dadf905c089e0f3a166b4c7c1e53623a6d75cb8dfdf11.jpg" alt="English French BLEU with age privacy budget" />
    <div class="pre-figcaption">Figure 3b: ε 越大，数值噪声越小，翻译质量略有回升。</div>
  </div>
</div>

<!--
第二个注意点是格式。

论文做了一个很直接的对比。同样是 RAG 事实检索，用 FPE 处理敏感字段，准确率是 100%；换成普通 AES，准确率掉到 70.97%；随机替换成错误格式，准确率是 77.42%。

AES 是常见的对称加密，安全性没有问题，但密文不像原来的字段。原来是邮编、日期、信用卡号，AES 之后可能变成一串模型不认识的字符。错误格式替换也一样，字段看起来不再是原来的类型。

这个实验给出的信息很直接：LLM 不只看语义，也看输入形态。SSN 像 SSN，日期像日期，邮编像邮编，模型才更容易按原任务处理。FPE 的价值就在这里：不是只把值藏起来，还保留模型能用的格式线索。

右边这张图也是原文 Figure 3 的一部分。epsilon 越大，数值噪声越小，翻译质量略有回升。不过在翻译任务里这个趋势不强，因为翻译本来就不太依赖年龄的精确值。

Q&A 预案：
Q：为什么不用普通 AES？
A：如果只看加密强度，AES 没问题；但给 LLM 用时，格式被破坏会影响任务。Prϵϵmpt 用 FPE，是为了让密文仍然像同类型字段，减少对回答质量的影响。
-->

---
layout: default
class: pre
---

## 方案对比

<table class="pre-table pre-table-lg mt-5">
  <thead>
    <tr>
      <th>方案</th>
      <th>证明</th>
      <th>可用性</th>
      <th>无状态</th>
      <th>主要问题</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Prϵϵmpt</td>
      <td>有</td>
      <td>高</td>
      <td>是</td>
      <td>只保护 token 级隐私</td>
    </tr>
    <tr>
      <td>HE / MPC</td>
      <td>强</td>
      <td>理论上高</td>
      <td>是</td>
      <td>推理成本过高</td>
    </tr>
    <tr>
      <td>替换表</td>
      <td>弱</td>
      <td>较高</td>
      <td>否</td>
      <td>映射表本身是风险</td>
    </tr>
    <tr>
      <td>Redaction</td>
      <td>直观</td>
      <td>低</td>
      <td>是</td>
      <td>LLM 缺关键值无法回答</td>
    </tr>
    <tr>
      <td>LLM 改写</td>
      <td>弱</td>
      <td>不稳定</td>
      <td>依实现</td>
      <td>可能漏泄露，难证明</td>
    </tr>
  </tbody>
</table>

<div class="pre-callout mt-6">
论文里的对比要放在限定范围里看：token 级敏感信息，加上现有 LLM API。只看这个范围，Prϵϵmpt 的成本不高，回答也没有明显变差。
</div>

<!--
前面讲完机制和实验，现在把它和几类替代方案放在一起看。

Prϵϵmpt 不是全面更强。它适合的场景很具体：token 级敏感信息，以及现有 LLM API 前面的输入净化。

HE 和 MPC 隐私强，但成本高。这里 HE 指同态加密，MPC 指多方安全计算，目标都是让服务端在不知道明文的情况下参与计算。直接遮盖就是删除或打码敏感值，普通替换则是把敏感值换成另一个占位值；这两种方法容易做，但模型可能缺少必要信息，或者系统要维护映射表。LLM 改写看起来轻，但容易漏，也很难说明到底泄露了多少。

所以它的位置是在中间：比直接遮盖多保留一些可用信息，比 HE/MPC 更容易接入现有 API。代价也很明确：它只处理已经识别出来的 token 级信息。

Q&A 预案：
Q：如果只看隐私强度，Prϵϵmpt 比 HE/MPC 弱很多吧？
A：是的。HE/MPC 保护得更强，但成本也高很多。Prϵϵmpt 不是要替代它们，而是解决一个更轻的场景：现有 LLM API 前面能不能先做一遍输入处理。
-->

---
layout: default
class: pre
---

## 主要局限

<div class="pre-grid3 mt-6">
  <div class="pre-card pre-card--risk">
    <div class="pre-card-title">上下文语义不保护</div>
    <p>如果故事情节、病情描述或业务背景本身足以泄露隐私，Prϵϵmpt 防不住。</p>
    <div class="pre-example mt-3">“我的邻居正在遭受家庭暴力。”</div>
  </div>
  <div class="pre-card pre-card--risk">
    <div class="pre-card-title">NER 决定覆盖率</div>
    <p>漏检 token 会原样进入 LLM。换领域后 NER 性能可能下降。</p>
    <div class="pre-example mt-3">手机号、邮箱、内部项目代号</div>
  </div>
  <div class="pre-card pre-card--risk">
    <div class="pre-card-title">数值保护不是强 DP</div>
    <p>mLDP 是距离敏感保护。数值距离大、重复查询多时，隐私保证会变弱。</p>
    <div class="pre-example mt-3">48 和 50 更难区分；20 和 90 更容易区分。</div>
  </div>
</div>

<div class="pre-panel mt-8">
  <div class="pre-section-title">放在什么位置</div>
  <p>Prϵϵmpt 适合接在 LLM API 前面，先处理 token 级敏感字段。放到 RAG 里，它只能补生成前这一段，检索隐私、访问控制和上下文语义保护还要另外做。</p>
</div>

<!--
机制、实验和对比讲完以后，限制也要讲清楚。

这篇论文做的是 prompt privacy 里的一个子问题：已经识别出来的敏感 token 怎么处理。这个点有价值，但不能把它说成完整的 prompt privacy 方案。

第一，上下文语义不保护。如果 prompt 本身的描述已经暴露敏感事实，它不会拦。第二，NER 决定覆盖率。没识别出来的字段会直接发出去。第三，mLDP 是距离敏感保护，也就是数值越接近越难区分，不是让所有数值都不可区分。重复查询时，攻击者还可能通过多次观测缩小范围。

所以我会把它放在生成前看：prompt 交给 LLM 之前，先处理最直接的一批敏感字段。它能补 RAG 生成侧的一段缺口，但检索隐私、访问控制和上下文语义治理还要单独做。

Q&A 预案：
Q：这篇论文最大的 weakness 是什么？
A：最大的问题是保护范围。token 级字段处理得比较细，但上下文语义隐私基本没碰。其次是 NER，实际系统里只要识别漏了，后面的机制就没有机会生效。
-->

---
layout: default
class: pre
---

## 和 RAG 的关系

<div class="pre-flow pre-flow-wide mt-6">
  <div class="pre-node">用户查询<span>query</span></div>
  <div class="pre-arrow"></div>
  <div class="pre-node pre-node--proof">检索隐私<span>SSE / HE / DP</span></div>
  <div class="pre-arrow"></div>
  <div class="pre-node">检索上下文<span>context</span></div>
  <div class="pre-arrow"></div>
  <div class="pre-node pre-node--proof">生成前净化<span>Prϵϵmpt</span></div>
  <div class="pre-arrow pre-arrow--risk"></div>
  <div class="pre-node pre-node--risk">云端 LLM<span>answer</span></div>
</div>

<div class="pre-grid2 mt-8">
  <div class="pre-card pre-card--proof">
    <div class="pre-card-title">可借鉴</div>
    <p>先判断字段作用，再选择处理方式。不同字段、不同查询类型不一定适合同一套隐私工具。</p>
  </div>
  <div class="pre-card pre-card--brand">
    <div class="pre-card-title">不能替代</div>
    <p>它不能保护检索阶段的查询向量，也不能控制上下文是否被允许进入 LLM。</p>
  </div>
</div>

<!--
最后回到开头的 RAG 隐私问题。

RAG 可以拆成两段：前面是检索，后面是生成。SSE、HE、DP 检索这些工作，主要解决的是用户怎么在云端知识库里搜，同时不暴露查询。SSE 是可搜索加密，HE 是同态加密，DP 是差分隐私。Prϵϵmpt 不解决这部分。

它处理的是下一步：检索结果和用户问题进入 LLM 之前，能不能先净化一遍。所以它不是可搜索加密的替代品。检索侧仍然要管 query、文本向量、访问权限和上下文选择。上下文选择指系统最终选择哪些检索内容交给模型。生成侧可以用它处理 SSN、姓名、账号、年龄、薪资这些字段。

对我自己的 RAG 方案来说，可以直接借的是这个位置：检索阶段保护完以后，不应该默认把明文 context 直接交给 LLM。生成前还可以加一层本地净化，至少先处理 token 级敏感字段。

Q&A 预案：
Q：这篇论文和我们组可搜索加密的关系是什么？
A：它不做密文检索，所以不是可搜索加密的替代。它补的是生成侧：检索时尽量不暴露查询，生成前再尽量不把敏感字段直接交给 LLM。
-->

---
layout: default
class: pre
---

## RAG 生成前净化架构

<div class="pre-figure pre-figure--architecture mt-4">
  <img src="/image/Preempt/ieg-preempt-architecture.svg" alt="RAG Preempt privacy architecture" />
  <div class="pre-figcaption">客户端负责检索和 Preempt 净化；云服务器厂商只接触净化后的 prompt/context。</div>
</div>

<!--
最后把前面的讨论落到 RAG 系统里。

这里有四个实体：用户、客户端、RAG 知识库、云服务器厂商。用户不直接访问云端 LLM，而是把问题交给客户端。客户端是可信侧，负责两件事：第一，向 RAG 知识库发起检索，并拿回相关 context；第二，把用户问题和 context 组合起来，在本地做 Preempt 净化。图里的绿色箭头只表示 RAG 检索和 context 返回，不是一个新的技术模块。

RAG 知识库也在可信侧。它提供业务数据和检索索引，但不应该把明文 context 直接发给云服务器厂商。这里的 context 指检索出来、准备交给 LLM 参考的上下文材料。图里红色虚线就是这个禁止路径：知识库明文不能绕过客户端直接进云端。

真正跨过隐私边界的，只有净化后的 prompt 和 context。云服务器厂商负责 LLM 推理，返回的也是基于净化输入生成的回答。客户端拿到回答以后，再做 desanitize，也就是把可恢复的字段还原。格式型字段可以恢复，数值型字段一般保持近似结果。

Preempt 不是用来解决所有隐私问题。它解决的是生成前这一段：在 RAG 检索已经完成以后，不要把用户问题和检索 context 的明文直接交给云厂商。检索权限、数据库访问控制、上下文是否允许进入 LLM，这些还是 RAG 系统自己要管。

Q&A 预案：
Q：云服务器厂商还能看到什么？
A：它能看到净化后的 prompt/context、请求时间、模型调用元数据和模型输出。Preempt 只减少 token 级敏感值暴露，不隐藏调用行为本身。

Q：RAG 知识库是不是完全不出可信侧？
A：是的，这张图按这个目标设计。知识库明文不直接给云厂商；客户端只把检索后的 context 经过 Preempt 处理后再发给 LLM。
-->

---
layout: default
class: pre
---

<div style="height: 100%; display: grid; grid-template-columns: 0.85fr 1.15fr; align-items: center; gap: 3rem;">
  <div>
    <div style="font-size: 4.8rem; line-height: 1; font-weight: 800; color: #111827; letter-spacing: -0.06em;">
      谢谢
    </div>
    <div style="margin-top: 1rem; width: 72px; height: 4px; background: #111827;"></div>
    <div style="margin-top: 1.2rem; font-size: 1.05rem; color: #374151;">
      Questions are welcome.
    </div>
  </div>

  <div style="font-size: 1.08rem; line-height: 1.75; color: #111827;">
    <p>
      Prϵϵmpt 的定位很明确：先处理 prompt 中能被识别出来的敏感 token，再把净化后的内容交给现有 LLM API。
    </p>
    <p style="margin-top: 1.1rem;">
      格式型字段用 FPE 保持结构，数值型字段用 mLDP 保留近似值。它能降低字段级泄露风险，但不覆盖整段语义本身的敏感性。
    </p>
    <div style="margin-top: 2rem; font-size: 0.78rem; line-height: 1.5; color: #4b5563;">
      Amrita Roy Chowdhury et al. · Prϵϵmpt: Sanitizing Sensitive Prompts for LLMs · NDSS 2026 · CCF A
    </div>
  </div>
</div>

<!--
最后收一下。prompt 隐私涉及的范围很宽，Prϵϵmpt 没有试图一次做完。它先只处理 prompt 里能被识别出来的敏感 token，这样问题会小很多，也更容易接到现有系统里。

Prϵϵmpt 把范围收窄到 token 级敏感信息，然后按作用分开处理。格式型字段用 FPE，保留结构，也能恢复；数值型字段用 mLDP，放弃精确值，保留近似值。

但限制也要一起记住：上下文语义泄露、NER 漏检、重复查询下的数值推断，这些还没有被解决。

所以这篇论文适合拿来补 RAG 生成前的隐私处理，但不能直接当成完整的 prompt privacy 方案。谢谢大家，欢迎提问。
-->
