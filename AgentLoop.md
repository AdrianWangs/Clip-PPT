---
theme: seriph
title: "Agent Loop 的安全检测与可验证推理"
info: |
  ## 两篇 USENIX Security 2025 论文的组合报告
  从污点型漏洞检测到 LLM 推理正确性证明
drawings:
  persist: false
transition: slide-left
mdc: true
highlighter: shiki
lineNumbers: false
katex: true
hideInToc: true
class: al
---

<div class="al-cover">
<div class="al-cover-glow"></div>

<div class="al-kicker">USENIX Security 2025 · CCF-A</div>

<div class="text-[3.9rem] leading-[1.06] font-bold" style="color:var(--al-ink); letter-spacing:-0.01em;">
Agent Loop 的安全检测<br />
与<span style="color:var(--al-brand);">可验证</span>推理
</div>

<div class="mt-3 text-[1.5rem] font-semibold" style="color:var(--al-ink-soft);">
当 AI 不再只是回答，而是开始驱动工具
</div>

<div class="grid grid-cols-2 gap-4 mt-8 w-[92%]">
  <div class="al-card al-card--risk">
    <div class="hd"><span class="dot"></span>论文一 · AgentFuzz</div>
    <div class="text-xs" style="color:var(--al-ink-soft); line-height:1.5;">
      Make Agent Defeat Agent: Automatic Detection of Taint-Style Vulnerabilities in LLM-based Agents
    </div>
    <div class="mt-2"><span class="al-badge al-badge--risk">找漏洞：prompt 能不能打到危险操作</span></div>
  </div>
  <div class="al-card al-card--proof">
    <div class="hd"><span class="dot"></span>论文二 · zkGPT</div>
    <div class="text-xs" style="color:var(--al-ink-soft); line-height:1.5;">
      zkGPT: An Efficient Non-interactive Zero-knowledge Proof Framework for LLM Inference
    </div>
    <div class="mt-2"><span class="al-badge al-badge--proof">给证明：输出真是这个模型算的</span></div>
  </div>
</div>

</div>

<div class="absolute bottom-8 right-10 text-sm" style="color:var(--al-ink-soft);">
  主讲人：王宇哲
</div>

<!--
先一句话定调：今天讲两篇 USENIX Security 2025 的论文，AgentFuzz 和 zkGPT。

一篇是站在攻击者视角找漏洞：恶意 prompt 有没有机会一路跑到 eval、SQL、shell 这些危险操作。
另一篇是站在验证者视角给证明：模型服务商能不能证明这个输出真的是某个模型算出来的，而且不公开模型参数。

为什么把这两篇放一起？因为它们都在回答同一个大背景下的问题：Agent 现在不只是回答问题，它开始驱动工具。安全的边界，也就从"回答里"挪到了"整条执行链路里"。

下一页我先说清楚，我为什么会选这个题。
-->

---
layout: default
class: al
---

## 为什么讲这个题：从 IEG 走到 AI × 密码学

<div class="al-kicker">选题动机</div>

<div class="grid grid-cols-2 gap-5 mt-3">

<div class="al-card al-card--brand" v-click>
  <div class="hd"><span class="dot"></span>现实：IEG 方向能讲的论文太少</div>
  <div class="text-sm mt-1" style="color:var(--al-ink-soft); line-height:1.6;">
    我原来的方向是 IEG，包括 IEG + 安全、IEG + 可搜索加密。
  </div>
  <ul class="text-sm mt-2" style="color:var(--al-ink-soft); line-height:1.6;">
    <li>这个交叉点高质量新论文不多</li>
    <li>多数工作是套用传统密码学方案（如 <b>ABE</b>）再做衍生</li>
    <li>能直接拿来组会汇报的更少</li>
  </ul>
</div>

<div class="al-card al-card--proof" v-click>
  <div class="hd"><span class="dot"></span>思考：AI 时代怎么接密码学</div>
  <ul class="text-sm mt-1" style="color:var(--al-ink-soft); line-height:1.6;">
    <li>大模型本身和密码学结合<b>很难</b>：模型太大、太黑盒</li>
    <li>但 Agent 这类<b>工程化</b>的东西，本质是在<b>限定 AI 的操作</b></li>
    <li>一旦操作被框住，就有了清晰的边界和接口</li>
  </ul>
</div>

</div>

<div class="al-callout mt-5" v-click>
关键转换：把 <b>AI 当作密码学方案里的一个敌手（adversary）</b>。系统的其它部分按密码学假设设计，AI 的行为被约束、被检测、被证明 —— 这样整个系统接入 AI 之后仍然能稳定、可信地运行。AgentFuzz 和 zkGPT 就是这个思路下的两个具体样本。
</div>

<!--
这页讲我为什么选这个题，其实有两个层面。

第一个是现实。我原来的方向是 IEG，加安全、加可搜索加密。但真去找论文会发现，这个交叉点能讲的新东西不多。很多所谓新方案，其实是把以前的传统密码学搬过来，比如 ABE，再衍生一点东西。能直接拿来组会讲的高质量论文就更少了。

第二个是我自己的一点思考，虽然这不完全是我的研究方向。我觉得大模型直接和密码学结合是比较难的，模型太大、太黑盒，你很难给它做一个干净的密码学假设。

但是 Agent 不一样。Agent、还有后面各种 engineering 的工程，本质上都是在限定 AI 能做什么、不能做什么。它把 AI 的操作框进了一个有边界、有接口的系统里。

一旦有了边界，思路就打开了。我们可以把 AI 当成密码学方案里的一个敌手。系统其它部分照着密码学的假设来设计，AI 的行为就交给检测、约束和证明来管。这样系统接进 AI 之后，还是能稳定、可信地跑。

今天这两篇论文，AgentFuzz 和 zkGPT，就是这个思路下的两个具体例子。一个负责检测 AI 可能被利用的路径，一个负责证明 AI 的关键计算。后面所有内容，都顺着这条线展开。
-->

---
layout: default
class: al
---

## 背景：能力每升一级，安全边界就外移一层

<div class="al-kicker">主线 · 一句话</div>

<div class="text-sm mt-1" style="color:var(--al-ink-soft);">
模型先学会"生成文本"，再学会"决定动作"，接着"接入真实系统"，最后要"留下证据"。每多一种能力，攻击面就往外挪一步。
</div>

<div class="evolution-board mt-4">

<div class="evolution-step" v-click>
  <div class="evolution-index">01</div>
  <div class="evolution-title">语言模型</div>
  <div class="evolution-sub">Prompt → Text</div>
  <ul>
    <li>预测 token，生成回答</li>
    <li>能写代码、写计划</li>
    <li>但计划不会自己执行</li>
  </ul>
  <div class="evolution-turn">⚠ 风险还在文本里：回答可不可信</div>
</div>

<div class="evolution-step" v-click>
  <div class="evolution-index">02</div>
  <div class="evolution-title">Agent</div>
  <div class="evolution-sub">Goal → Action</div>
  <ul>
    <li>把任务拆成多步</li>
    <li>自己选工具、定下一步</li>
    <li>看 observation 再推理</li>
  </ul>
  <div class="evolution-turn">⚠ 边界外移：输出开始决定动作</div>
</div>

<div class="evolution-step" v-click>
  <div class="evolution-index">03</div>
  <div class="evolution-title">Harness</div>
  <div class="evolution-sub">Model + Tools + Runtime</div>
  <ul>
    <li>接入 tools、memory、权限</li>
    <li>解析输出并路由到工具</li>
    <li>记录 tracing / logs</li>
  </ul>
  <div class="evolution-turn">⚠ 风险进入 parser、router、tool 参数</div>
</div>

<div class="evolution-step" v-click>
  <div class="evolution-index">04</div>
  <div class="evolution-title">Loop Engineering</div>
  <div class="evolution-sub">Observe → Reason → Act → Verify</div>
  <ul>
    <li>管整轮循环与停止条件</li>
    <li>约束工具调用</li>
    <li>沉淀 proof、log、审计证据</li>
  </ul>
  <div class="evolution-turn">⚠ 问题升级为：可控、可证明、可审计</div>
</div>

</div>

<div class="evolution-axis mt-4" v-click>
  <span>文本生成</span>
  <span>行动决策</span>
  <span>系统接入</span>
  <span>证据审计</span>
</div>

<div class="al-callout mt-3" v-click>
顺着这条线看，AgentFuzz 和 zkGPT 就不是硬凑：一个管 <b style="color:var(--al-risk)">第 3 步的风险路径</b>，一个管 <b style="color:var(--al-proof)">关键推理的证明</b>。
</div>
<!--
这页是整个背景的纲，我想先把一条主线立起来。

这条线很简单：模型的能力每往上升一级，安全的边界就往外挪一层。我分四步讲。

第一步，语言模型。它就是预测下一个 token，生成回答，能写代码、写计划。但注意，计划写出来不会自己跑。所以这个阶段，风险还关在文本里——你只需要问，这个回答可不可信。

第二步，Agent。模型不只写计划了，它开始自己拆任务、自己选工具、自己定下一步，看到反馈再接着想。边界就在这里第一次外移：模型的输出，开始决定真实动作。

第三步，Harness，可以理解成 Agent 的外壳。模型自己不碰数据库、不开 shell，是 Harness 把工具、记忆、权限接进来，还负责解析模型输出、路由到工具。很多漏洞就出在这：一句自然语言，经过 parser 和 router，最后变成一个真实的工具参数。

第四步，Loop Engineering。到这里，关注点不再是单条 prompt，而是整轮循环——上下文怎么进、工具怎么约束、什么时候停、出了事有没有证据。问题升级成三个词：可控、可证明、可审计。

把这四步连起来，下面这条轴就出来了：文本生成、行动决策、系统接入、证据审计。

顺着这条线，今天这两篇论文的位置也就清楚了。AgentFuzz 管第三步的风险路径，找恶意 prompt 能不能打穿；zkGPT 管关键推理的证明。它们不是硬凑在一起，而是同一条演进线上的两个点。
-->

---
layout: two-cols-header
class: al
---

## 演进 ① 语言模型：文本进，文本出

<div class="al-kicker">背景 · 阶段 1 / 4</div>

::left::

<div class="viewpoint">
这一阶段模型是个<b>文本函数</b>：输入 prompt，输出 answer。它能写计划，但计划不会自己跑。
</div>

<div class="al-card al-card--muted mt-2">
  <div class="hd"><span class="dot"></span>它能做什么</div>
  <ul>
    <li>预测下一个 token，生成回答</li>
    <li>解释问题、组织答案、写代码或计划</li>
  </ul>
</div>

<div class="al-card al-card--muted mt-3">
  <div class="hd"><span class="dot" style="background:var(--al-ink-soft)"></span>它<b>不</b>能做什么</div>
  <ul>
    <li>不访问真实数据库、不调真实工具</li>
    <li>不维护长期状态、不验证执行结果</li>
  </ul>
</div>

::right::

<div class="al-figure-box">
  <div class="al-flow" style="justify-content:center;">
    <div class="al-node al-node--brand">Prompt<span class="sub">上下文</span></div>
    <div class="al-arrow" style="max-width:3rem"></div>
    <div class="al-node al-node--strong">Language Model<span class="sub">next-token</span></div>
    <div class="al-arrow" style="max-width:3rem"></div>
    <div class="al-node al-node--brand">Text<span class="sub">回答</span></div>
  </div>
  <div class="al-figure-cut">
    <span class="al-badge" style="background:#f0f0f4;color:var(--al-ink-soft)">✕ 不执行任何工具</span>
  </div>
</div>

<div class="al-callout mt-4">
模型说"我查了数据库"，不代表它真查了 —— 没有外部系统配合，这只是一句生成的文本。所以这阶段的安全问题是<b>回答可不可信</b>，还谈不上执行链路被打穿。
</div>

<!--
先看最早的形态：语言模型。

右边这张图很简单：prompt 进去，模型预测 token，吐出文本。注意下面那行——它不执行任何工具。

它很强，能写代码、写计划、解释问题。但本质还是文本进、文本出。

它说"我查了数据库"，不代表它真的查了。没有外部系统配合，它只是把这句话生成出来而已。

所以这一阶段的安全问题，集中在回答可不可信，还没到执行链路会不会被打穿。
-->

---
layout: two-cols-header
class: al
---

## 演进 ② Agent：模型输出开始驱动动作

<div class="al-kicker">背景 · 阶段 2 / 4</div>

::left::

<div class="viewpoint">
关键变化不是"更会聊天"，而是模型输出进入 <b>ReAct 式行动循环</b>：想一步、做一步、看反馈，再想下一步。
</div>

<div class="al-steps mt-3">
  <div class="al-step"><div class="idx">1</div><div><div class="t">Reason 推理</div><div class="d">读任务和上下文，想下一步该干嘛</div></div></div>
  <div class="al-step"><div class="idx">2</div><div><div class="t">Act 行动</div><div class="d">选择工具或动作，给出调用参数</div></div></div>
  <div class="al-step"><div class="idx">3</div><div><div class="t">Observe 观察</div><div class="d">拿到工具返回，回填进上下文继续推理</div></div></div>
</div>

::right::

<div class="al-figure-box">
  <div class="al-loop">
    <div class="al-node al-node--strong" style="grid-area:r;">Reason<span class="sub">推理下一步</span></div>
    <div class="al-node al-node--brand" style="grid-area:a;">Act<span class="sub">调用工具</span></div>
    <div class="al-node al-node--brand" style="grid-area:o;">Observe<span class="sub">读取结果</span></div>
    <div class="al-loop-ring"></div>
  </div>
</div>

<div class="al-callout mt-4">
这一步让模型从"回答问题"变成"推进任务"。AgentFuzz 论文里的 Agent Loop 正是这种简化的 ReAct 循环 —— 后面讲它的攻击模型，就建立在这张图上。
</div>

<!--
到 Agent 之后，事情就变了。

模型不再只是给人看答案，它进了一个循环：想一步、做一步、看反馈，再想下一步。右边这个环就是 ReAct——Reason、Act、Observe 三个节点转起来。

左边把这三步拆开了：先推理该干嘛，再选工具给参数，再把工具返回读回来接着想。

这一步的意义是，模型从"回答问题"变成"推进任务"。

记住这张环图，因为 AgentFuzz 论文里的 Agent Loop 就是这种简化的 ReAct。后面讲它怎么找漏洞，都是在这张图上做文章。
-->

---
layout: two-cols-header
class: al
---

## 演进 ③ Harness：风险真正出现的连接层

<div class="al-kicker">背景 · 阶段 3 / 4</div>

::left::

<div class="viewpoint">
Harness 是模型和真实系统之间的<b>连接层</b>，也是大量 source-to-sink 风险出现的位置。
</div>

<div class="text-sm mt-2" style="color:var(--al-ink-soft);">模型自己不碰数据库、不开 shell。把这些能力接进来的是 Harness：</div>

<div class="grid grid-cols-2 gap-2 mt-2 text-xs">
  <div class="al-chip">instructions 任务规则</div>
  <div class="al-chip">tools 可调用能力</div>
  <div class="al-chip">memory 历史与外部信息</div>
  <div class="al-chip">guardrails 输入输出约束</div>
  <div class="al-chip">tracing / logs 执行记录</div>
  <div class="al-chip">handoff Agent 或人接力</div>
</div>

::right::

<div class="al-figure-box">
  <div class="al-flow">
    <div class="al-node al-node--strong">LLM 输出</div>
    <div class="al-arrow al-arrow--risk"></div>
    <div class="al-node al-node--risk">Parser /<br>Router</div>
    <div class="al-arrow al-arrow--risk"></div>
    <div class="al-node al-node--sink">Tool<br>代码 / SQL / shell</div>
  </div>
  <div class="al-figure-note">一句自然语言，经 parser、router，最后变成真实工具参数</div>
</div>

<div class="takeaway">
真实风险通常就出现在这些连接点：LLM 输出 → parser/router → tool 参数 → 代码/SQL/shell。<b>AgentFuzz 关注的正是这条 source-to-sink 路径。</b>
</div>

<!--
Harness 可以理解成 Agent 的外壳。

模型自己不会碰数据库，也不会自己开 shell。真正把这些能力接进来的，是 Harness。左边列的就是它管的事：指令、工具、记忆、护栏、日志、接力。

但重点在右边这条链。模型吐出一句话，先进 parser 和 router 被解析、被路由，最后变成一个真实的工具参数，落到代码、SQL 或者 shell 上。

很多漏洞就出在这里：一句自然语言，走完这条链，就成了一次真实操作。

这条 source-to-sink 路径，就是后面 AgentFuzz 要测的东西。
-->

---
layout: two-cols-header
class: al
---

## 演进 ④ Loop Engineering：问题升级为链路治理

<div class="al-kicker">背景 · 阶段 4 / 4</div>

::left::

<div class="viewpoint">
对象不再是单条 prompt，而是<b>整轮循环</b>：输入怎么进、输出怎么解析、工具怎么约束、何时停、怎么留证据。
</div>

<div class="al-vs mt-3">
  <div class="al-card al-card--muted" style="padding:0.6rem 0.7rem">
    <div class="text-xs font-bold" style="color:var(--al-ink-soft)">Prompt Engineering</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.4">只关心<b>单次输入</b>写得好不好</div>
  </div>
  <div class="mid">→</div>
  <div class="al-card al-card--brand" style="padding:0.6rem 0.7rem">
    <div class="text-xs font-bold" style="color:var(--al-brand)">Loop Engineering</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.4">关心<b>整个闭环</b>怎么可控、可证、可审计</div>
  </div>
</div>

::right::

<div class="al-figure-box">
  <div class="al-loop">
    <div class="al-node al-node--brand" style="grid-area:r;">Reason</div>
    <div class="al-node al-node--brand" style="grid-area:a;">Act</div>
    <div class="al-node al-node--brand" style="grid-area:o;">Observe</div>
    <div class="al-node al-node--strong" style="grid-area:v;">Verify<span class="sub">证据/审计</span></div>
    <div class="al-loop-ring"></div>
  </div>
</div>

<div class="grid grid-cols-2 gap-2 mt-3 text-xs">
  <div class="al-chip-risk">① 输入会不会污染工具参数</div>
  <div class="al-chip-proof">② 关键推理是否可验证</div>
  <div class="al-chip-risk">③ 工具执行有没有可靠记录</div>
  <div class="al-chip-proof">④ 事后能不能复现链路</div>
</div>

<!--
到 Loop Engineering 这一步，关注点彻底变了。

左边这个对比是核心：Prompt Engineering 只管单次输入写得好不好；Loop Engineering 管的是整个闭环——上下文怎么进、输出怎么解析、工具怎么约束、什么时候停、出了事怎么留证据。环图也多了一个节点：Verify。

下面这四个问题，就是闭环里真正要回答的：输入会不会污染工具参数、关键推理能不能验证、工具执行有没有记录、事后能不能复现。

注意我用了两种颜色：红的偏"找风险"，绿的偏"给证明"。这正好对应 AgentFuzz 和 zkGPT。这也是为什么这两篇能放一起讲——它们落在同一个闭环的不同问题上。
-->

---
layout: default
class: al
---

## 研究问题：两条线，对应两篇论文

<div class="al-kicker">从背景 · 收敛到问题</div>

<div class="viewpoint">
真正要保护的不是所有输出，而是会进入<b>工具选择、参数生成、代码片段或策略分支</b>的关键 LLM 输出。围绕它，有两个独立又互补的问题。
</div>

<div class="al-branch mt-4">
  <div class="al-branch-root">关键 LLM 输出</div>
  <div class="al-branch-cols">
    <div class="al-card al-card--risk" v-click="1">
      <div class="hd"><span class="dot"></span>问题一 · 风险检测</div>
      <div class="al-flow al-flow--sm my-2">
        <div class="al-node al-node--risk">prompt</div>
        <div class="al-arrow al-arrow--risk"></div>
        <div class="al-node al-node--risk">LLM</div>
        <div class="al-arrow al-arrow--risk"></div>
        <div class="al-node al-node--sink">sink</div>
      </div>
      <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.5;">恶意输入能不能一路流到 <code>eval</code>/SQL/shell？</div>
      <div class="mt-2"><span class="al-badge al-badge--risk">AgentFuzz：自动找污点路径</span></div>
    </div>
    <div class="al-card al-card--proof" v-click="2">
      <div class="hd"><span class="dot"></span>问题二 · 推理证明</div>
      <div class="al-flow al-flow--sm my-2">
        <div class="al-node al-node--proof">x, w</div>
        <div class="al-arrow al-arrow--proof"></div>
        <div class="al-node al-node--strong">f</div>
        <div class="al-arrow al-arrow--proof"></div>
        <div class="al-node al-node--proof">y + proof</div>
      </div>
      <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.5;">这步输出，真是承诺的模型算出来的吗？</div>
      <div class="mt-2"><span class="al-badge al-badge--proof">zkGPT：给关键推理出证明</span></div>
    </div>
  </div>
</div>

<div class="al-callout mt-4" v-click="3">
两条线不重叠：一条问"哪里会被打穿"，一条问"输出可不可信"。它们都落在同一批关键推理节点上，所以可以接起来看。
</div>

<!--
背景讲完，把四个问题收敛成两条研究主线。

第一条是风险检测：恶意输入能不能从 prompt 一路流到 sink。这对应 AgentFuzz。

第二条是推理证明：关键这步输出，是不是承诺的模型真算出来的。这对应 zkGPT。

注意这两条线不重叠。一条管"哪里会被打穿"，一条管"输出可不可信"。但它们都落在同一批关键推理节点上——会决定工具、参数、代码的那些节点。所以后面能把它们接起来。

接下来分别展开这两篇。先讲 AgentFuzz。
-->

---
layout: two-cols-header
class: al
---

## AgentFuzz：把漏洞看成一条污点路径

<div class="al-kicker al-kicker--risk">论文一 · 威胁模型</div>

::left::

<div class="viewpoint">
taint-style 漏洞的结构很简单：攻击者输入能不能<b>流到</b>危险操作。问题不在"prompt 看起来恶不恶意"。
</div>

<div class="al-steps mt-3">
  <div class="al-step al-step--risk"><div class="idx">S</div><div><div class="t">source 源</div><div class="d">攻击者可控输入，例如 user prompt、网页、observation</div></div></div>
  <div class="al-step al-step--risk"><div class="idx">P</div><div><div class="t">propagation 传播</div><div class="d">经 LLM、parser、tool router 一层层翻译成动作</div></div></div>
  <div class="al-step al-step--risk"><div class="idx">K</div><div><div class="t">sink 汇</div><div class="d">安全敏感操作，例如 <code>eval</code>、SQL、命令执行</div></div></div>
</div>

::right::

<img src="/image/AgentLoop/agentfuzz_vuln_example.png" class="w-[82%] mx-auto" />

<div class="caption">原文图：真实 Agent 漏洞示例，恶意 prompt 最终进入 <code>eval</code></div>

<div class="al-callout al-callout--risk mt-3">
难点是这条路不直：中间有 LLM 在"翻译"用户意图。所以不能只看输入字面，要测整条链路通不通。
</div>

<!--
先讲第一篇 AgentFuzz，它的威胁模型就是 taint-style 漏洞。

这个词不用想复杂。三个东西：source 是攻击者能控制的输入，比如 prompt、网页、工具返回的 observation；propagation 是中间传播，输入经过 LLM、parser、router 一层层翻译；sink 是危险操作，比如 eval、SQL、shell。

问题不是"这个 prompt 看起来恶不恶意"，而是"它能不能一路流到 sink"。

Agent 把这件事变难了，因为中间多了个 LLM 在翻译用户意图。输入不是直接进 sink，而是先被模型解释成工具和参数。所以你光看输入字面没用，得测整条链路通不通。右边就是论文里一个真实例子，恶意 prompt 最后进了 eval。
-->

---
layout: two-cols-header
class: al
---

## AgentFuzz：为什么不能照搬传统 fuzzing

<div class="al-kicker al-kicker--risk">论文一 · 设计动机</div>

::left::

<div class="viewpoint">
目标不是判断 prompt 恶不恶意，而是验证模型输出<b>能不能被诱导到 sink</b>。
</div>

<div class="al-vs mt-4">
  <div class="al-card al-card--muted">
    <div class="hd" style="font-size:0.86rem;">传统 fuzzing</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.6;">输入是结构化字节<br/>随机翻转就能改路径<br/>覆盖率直接可测</div>
  </div>
  <div class="mid">≠</div>
  <div class="al-card al-card--risk">
    <div class="hd" style="font-size:0.86rem;">Agent 场景</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.6;">输入是自然语言 prompt<br/>乱改模型就不调目标工具<br/>要同时对齐语义和参数</div>
  </div>
</div>

::right::

<div class="text-sm mt-1" style="color:var(--al-ink-soft);">论文把难点拆成三个子问题，正好对应后面三个阶段：</div>

<div class="al-steps mt-3">
  <div class="al-step al-step--risk"><div class="idx">1</div><div><div class="t">生成</div><div class="d">怎么写出能调到目标功能的 seed prompt</div></div></div>
  <div class="al-step al-step--risk"><div class="idx">2</div><div><div class="t">调度</div><div class="d">怎么优先选更可能到达 sink 的 seed</div></div></div>
  <div class="al-step al-step--risk"><div class="idx">3</div><div><div class="t">变异</div><div class="d">怎么改 prompt，既语义正确又满足路径约束</div></div></div>
</div>

<div class="al-callout al-callout--risk mt-4">
一句话：先走到目标功能，再逼近敏感 sink，最后把 payload 放进会流向 sink 的参数里。
</div>

<!--
为什么不能直接拿传统 fuzzing 来用？

传统 fuzzing 处理的是结构化字节，随机翻转几位就能改执行路径，覆盖率也好测。

但 Agent 的输入是一段自然语言。你乱改，模型可能根本不调那个目标工具，那后面 payload 再强也没用。这里要同时对齐两件事：语义——让模型选对功能；参数——让它满足 sink 前面的条件。

所以论文把难点拆成三个子问题：怎么生成 seed、怎么调度 seed、怎么变异 seed。这三个正好对应接下来三个阶段。

压成一句话就是：先走到目标功能，再逼近 sink，最后把 payload 塞进会流过去的参数。
-->

---
layout: default
class: al
---

## AgentFuzz 方法总览：带方向的三阶段

<div class="al-kicker al-kicker--risk">论文一 · 整体流程</div>

<div class="al-flow mt-6" style="justify-content:center;">
  <div class="al-card al-card--risk" style="width:15rem;" v-click="1">
    <div class="hd"><span class="dot"></span>① 生成 Seed</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.55;">静态分析从 sink 反向找 call chain，借类名/方法名语义，让 LLM 写出能调到目标功能的 prompt</div>
  </div>
  <div class="al-arrow al-arrow--risk" style="min-width:3rem;"></div>
  <div class="al-card al-card--risk" style="width:15rem;" v-click="2">
    <div class="hd"><span class="dot"></span>② 反馈调度</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.55;">跑起来看执行 trace，按"语义 + 距离 − 重复"打分，把资源集中到更可能触发 sink 的 seed</div>
  </div>
  <div class="al-arrow al-arrow--risk" style="min-width:3rem;"></div>
  <div class="al-card al-card--risk" style="width:15rem;" v-click="3">
    <div class="hd"><span class="dot"></span>③ 定向变异</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.55;">功能变异器对齐意图，参数变异器满足路径约束，触达 sink 后插入 PoC payload</div>
  </div>
</div>

<div class="al-callout al-callout--risk mt-8" v-click="4">
和随机 fuzzing 最大的区别：每一步都朝 sink 收敛。生成把方向定下来，调度决定先试谁，变异负责最后一公里。
</div>

<!--
这是 AgentFuzz 的整体流程，三个阶段。

第一阶段，生成 seed。它先做静态分析，从 sink 反向找调用链，再借代码里的类名方法名推断功能，让 LLM 写出能调到目标功能的 prompt。

第二阶段，反馈调度。把 seed 跑起来看 trace，按一个打分公式排序——语义贴不贴近、离 sink 远不远、有没有重复探索，然后把测试资源集中到更有希望的 seed 上。

第三阶段，定向变异。两类变异器：一类改任务意图让模型选对功能，一类改参数满足路径约束。一旦摸到 sink，就把 PoC payload 插进那个会流过去的参数。

和随机 fuzzing 最大的区别就是带方向：生成定方向，调度定顺序，变异管最后一公里。下面把三个阶段分别展开。
-->

---
layout: two-cols-header
class: al
---

## 阶段一 · 生成：先让 Agent 走到目标功能

<div class="al-kicker al-kicker--risk">论文一 · Seed Generation</div>

::left::

<div class="viewpoint">
传统 fuzzer 不知道怎么写自然语言 prompt。AgentFuzz 的策略是<b>从代码里抠语义线索</b>，让 LLM 生成像真实用户请求的 seed。
</div>

<div class="al-flow mt-4">
  <div class="al-node al-node--sink">sink</div>
  <div class="al-arrow al-arrow--risk"></div>
  <div class="al-node al-node--risk">反向 call chain</div>
  <div class="al-arrow al-arrow--risk"></div>
  <div class="al-node al-node--risk">类名/方法名语义</div>
  <div class="al-arrow al-arrow--risk"></div>
  <div class="al-node">seed prompt</div>
</div>

<div class="text-xs mt-3" style="color:var(--al-ink-soft);line-height:1.6;">
先识别预定义 sink（SQL/code injection），从 sink 反向找调用链，再借方法名语义让 LLM 写 prompt。
</div>

::right::

<div class="al-card al-card--muted">
  <div class="hd" style="font-size:0.86rem;"><span class="dot" style="background:var(--al-risk);"></span>例子：方法名就是线索</div>
  <div class="mt-2"><code>PermissionCheck()</code> · <code>similarity_search()</code></div>
  <div class="text-xs mt-3" style="color:var(--al-ink-soft);line-height:1.6;">这些名字本身就暗示了 Agent 该被诱导到什么功能。seed 于是长成"一个需要权限检查的用户请求"。</div>
</div>

<div class="al-callout al-callout--risk mt-4">
关键不是生成攻击 payload，而是先把 Agent 引到目标功能附近 —— 连工具都调不到，后面再强的 payload 也没用。
</div>

<!--
第一阶段，生成 seed。

它不是一上来就写攻击 prompt。它先做静态分析：从 sink 反向找调用链，再借代码里的类名、方法名语义，让 LLM 生成 prompt。

右边这个例子很直观。方法名里有 PermissionCheck、similarity_search，这些词本身就暗示了 Agent 需要被诱导到什么功能。seed 就应该长成一个"需要做权限检查的用户请求"。

这一阶段的关键，不是写攻击 payload，而是先把 Agent 引到目标功能附近。道理很简单——连目标工具都调不到，后面 payload 再厉害也没用。
-->

---
layout: two-cols-header
class: al
---

## 阶段二 · 调度：用一个打分公式排优先级

<div class="al-kicker al-kicker--risk">论文一 · Seed Scheduling</div>

::left::

<div class="viewpoint">
两个 seed 离 sink 的控制流距离可能一样，但语义完全不同。在 Agent 里，<b>语义决定模型选不选对工具</b>。
</div>

<div class="al-formula al-formula--risk mt-4">

$$F_s = \alpha S_s + \beta D_s - P_s$$

</div>

<div class="al-legend">
  <span><b class="k" style="color:var(--al-risk);">S_s</b> 语义分：prompt 贴不贴近目标组件</span>
  <span><b class="k" style="color:var(--al-risk);">D_s</b> 距离分：trace 离 sink 还有多远</span>
  <span><b class="k" style="color:var(--al-risk);">P_s</b> 惩罚分：压制重复探索</span>
</div>

::right::

<div class="text-sm" style="color:var(--al-ink-soft);">公式怎么读：分数越高越先试。</div>

<div class="al-steps mt-3">
  <div class="al-step al-step--risk"><div class="idx">+</div><div><div class="t">α·S<sub>s</sub> 语义越贴近，越值得试</div><div class="d">光近还不够，模型得真的愿意走这条功能</div></div></div>
  <div class="al-step al-step--risk"><div class="idx">+</div><div><div class="t">β·D<sub>s</sub> 离 sink 越近，越值得试</div><div class="d">由执行 trace 实测，而不是只看静态代码</div></div></div>
  <div class="al-step al-step--risk"><div class="idx">−</div><div><div class="t">P<sub>s</sub> 反复选同一条链就扣分</div><div class="d">逼 fuzzer 去探新路径，别原地打转</div></div></div>
</div>

<div class="al-callout al-callout--risk mt-4">
α、β 是权重，平衡"语义贴合"和"距离接近"两个信号。本质：把有限的测试预算押在最可能打穿的 seed 上。
</div>

<!--
第二阶段，调度。核心就是中间这个打分公式，我详细讲一下。

F_s 是一个 seed 的综合分，分数越高越优先试。它由三项组成。

第一项，α 乘 S_s，语义分。它衡量这个 prompt 的语义贴不贴近目标组件。为什么要这一项？因为光"距离近"不够，模型还得真的愿意往这个功能走。

第二项，β 乘 D_s，距离分。它衡量执行 trace 离 sink 还有多远。注意是实际跑出来的 trace，不是静态估计。

第三项，减 P_s，惩罚分。如果一个 seed 或者一条调用链被反复选，就扣分，逼着 fuzzer 去探索新路径，别在一个地方打转。

α 和 β 是权重，用来平衡语义和距离这两个信号。

为什么不能只看控制流距离？因为两个 prompt 可能离 sink 一样近，但语义完全不一样，而在 Agent 里语义会直接影响模型选哪个工具。所以这个公式本质上是在做一件事：把有限的测试预算，押在最可能打穿的 seed 上。
-->

---
layout: two-cols-header
class: al
---

## 阶段三 · 变异：两类变异器，定向逼近 sink

<div class="al-kicker al-kicker--risk">论文一 · Sink-guided Mutation</div>

::left::

<div class="al-card al-card--risk">
  <div class="hd"><span class="dot"></span>功能变异器</div>
  <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.6;">调整 prompt 的任务意图，让模型更可能选到目标组件</div>
</div>

<div class="al-card al-card--risk mt-3">
  <div class="hd"><span class="dot"></span>参数变异器</div>
  <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.6;">按运行时参数和路径约束，改动 prompt 中会流向 sink 的片段；触达 sink 后插入 PoC payload</div>
</div>

::right::

<div class="text-sm" style="color:var(--al-ink-soft);">普通 prompt mutation 容易把语义改坏。AgentFuzz 的变异分三拍走：</div>

<div class="al-steps mt-3">
  <div class="al-step al-step--risk"><div class="idx">1</div><div><div class="t">选对功能</div><div class="d">功能变异器先让模型走到目标组件</div></div></div>
  <div class="al-step al-step--risk"><div class="idx">2</div><div><div class="t">满足约束</div><div class="d">参数变异器让参数过 sink 前面的判断</div></div></div>
  <div class="al-step al-step--risk"><div class="idx">3</div><div><div class="t">oracle 判定</div><div class="d">用判定器确认漏洞是否真的被触发</div></div></div>
</div>

<div class="al-callout al-callout--risk mt-4">
oracle 是判定器，用来判断某个输入是否真的触发了漏洞。比随机改 prompt 稳很多。
</div>

<!--
第三阶段，变异。这里有两类变异器。

功能变异器，改的是任务意图，让模型更可能选到目标功能。

参数变异器，改的是 prompt 里那些会流向 sink 的参数片段，让它满足路径约束。一旦摸到 sink 附近，就把 PoC payload 插到那个会流过去的参数里。

右边是它的节奏：先用功能变异器选对功能，再用参数变异器满足约束，最后用 oracle 判定漏洞到底有没有被触发。oracle 就是个判定器。

普通的 prompt mutation 容易把语义改坏，模型一懵就不走目标功能了。AgentFuzz 这种分层定向的变异，稳很多。
-->

---
layout: two-cols-header
class: al
---

## AgentFuzz 实验设置：评测对象是真实 Agent

<div class="al-kicker al-kicker--risk">论文一 · 实验设置</div>

::left::

<div class="viewpoint">
评测对象不是玩具项目，而是 GitHub 上真实流行的 Agent。盯的目标是<b>会触发危险操作的 sink 调用点</b>。
</div>

<div class="al-statgrid mt-4">
  <div class="al-stat"><div class="num risk">20</div><div class="lbl">开源 Agent 应用</div></div>
  <div class="al-stat"><div class="num risk">13</div><div class="lbl">超过 10k stars</div></div>
  <div class="al-stat"><div class="num risk">828</div><div class="lbl">sink callsites</div></div>
  <div class="al-stat"><div class="num">GPT-4o</div><div class="lbl">基础模型</div></div>
</div>

<div class="text-xs mt-3" style="color:var(--al-ink-soft);line-height:1.6;">
每个 sink callsite 设 5 分钟 timeout，AgentFuzz 和被测 Agent 用同一个基础模型。
</div>

::right::

<div class="al-figure-box">
  <img src="/image/AgentLoop/agentfuzz_dataset_table.png" class="w-full" />
  <div class="al-figure-note">原文表：20 个 Agent 数据集与漏洞统计</div>
</div>

<!--
实验设置看几个数。

第一，数据集不是玩具，是 20 个真实开源 Agent，其中 13 个 star 数过万。

第二，论文盯的是 828 个 sink callsite，也就是 828 个可能触发危险操作的代码点。

第三，AgentFuzz 和被测 Agent 用的是同一个基础模型 GPT-4o，每个 sink 给 5 分钟超时。

它最后报告 34 个潜在漏洞，再人工确认。目标不是证明系统安全，而是尽量把高风险路径找出来。
-->

---
layout: two-cols-header
class: al
---

## AgentFuzz 实验结果：高召回，几乎零误报

<div class="al-kicker al-kicker--risk">论文一 · 主要结果与消融</div>

::left::

<div class="al-statgrid mt-2">
  <div class="al-stat"><div class="num risk">34</div><div class="lbl">true positives</div></div>
  <div class="al-stat"><div class="num risk">0</div><div class="lbl">false positives</div></div>
  <div class="al-stat"><div class="num">100%</div><div class="lbl">precision</div></div>
  <div class="al-stat"><div class="num">97.14%</div><div class="lbl">recall</div></div>
</div>

<div class="al-vs mt-4">
  <div class="al-card al-card--risk">
    <div class="hd" style="font-size:0.82rem;">AgentFuzz</div>
    <div class="text-xs" style="color:var(--al-ink-soft);">precision <b style="color:var(--al-risk);">100%</b></div>
  </div>
  <div class="mid">vs</div>
  <div class="al-card al-card--muted">
    <div class="hd" style="font-size:0.82rem;">LLMSmith</div>
    <div class="text-xs" style="color:var(--al-ink-soft);">precision <b>2.92%</b></div>
  </div>
</div>

::right::

<div class="al-figure-box">
  <img src="/image/AgentLoop/agentfuzz_table_3.png" class="w-full" />
  <div class="al-figure-note">原文表 3：去掉任一模块，recall 都明显下降</div>
</div>

<div class="al-callout al-callout--risk mt-3">
三个模块不是装饰：seed 生成、反馈调度、sink-guided 变异共同决定能不能触发 sink。
</div>

<!--
看结果。

AgentFuzz 找到 34 个 true positives，0 个 false positives，precision 100%，recall 97.14%。对比 baseline LLMSmith，它的 precision 只有 2.92%，也就是绝大多数报出来的是误报。差距非常大。

右边是消融实验。把 seed 生成、调度、语义打分、变异任意去掉一个，recall 都会明显往下掉。

这说明三个模块不是摆设，是共同起作用的：自然语言 seed 负责走到功能，语义反馈负责排序，sink-guided 变异负责最后触发。少一个都不行。
-->

---
layout: default
class: al
---

## AgentFuzz 的输出：不是"安全了"，是"风险在哪"

<div class="al-kicker al-kicker--risk">论文一 · 作用边界</div>

<div class="al-vs mt-5" style="align-items:stretch;">
  <div class="al-card al-card--muted" style="flex:1;">
    <div class="hd" style="font-size:0.9rem;color:var(--al-ink-soft);">它不回答</div>
    <div class="text-sm mt-2" style="color:var(--al-ink-soft);line-height:1.7;">这个系统已经安全了吗？</div>
  </div>
  <div class="mid">→</div>
  <div class="al-card al-card--risk" style="flex:1.6;">
    <div class="hd" style="font-size:0.9rem;"><span class="dot"></span>它回答：风险落在哪些路径上</div>
    <div class="text-sm mt-2" style="color:var(--al-ink-soft);line-height:1.75;">
      · 哪些 source→sink 路径能被 prompt 触发<br/>
      · 哪些功能会调用安全敏感操作<br/>
      · 哪些 LLM 输出会变成工具名、参数、代码片段<br/>
      · 哪些路径需要修复、隔离或加审计
    </div>
  </div>
</div>

<div class="al-callout al-callout--risk mt-6">
放进可验证 Agent Loop，AgentFuzz 的角色是<b>风险定位</b>：它指出哪些 LLM 推理节点值得重点保护——这正是下一篇要加证明的地方。
</div>

<!--
强调一下 AgentFuzz 的输出边界，这关系到它怎么和第二篇接起来。

它不回答"这个系统安全了吗"。它回答的是风险落在哪些路径上：哪些 prompt 能影响哪些 sink，哪些功能会碰危险操作，哪些 LLM 输出会变成工具名、参数、代码。

这个结果正好接到后面的 zkGPT。因为不是每个 LLM 调用都值得加证明，成本太高。真正值得保护的，是那些会决定工具、参数、代码片段的关键推理节点。AgentFuzz 干的就是把这些节点指出来。
-->

---
layout: default
class: al
---

## 从风险发现到推理证明：换一个视角

<div class="al-kicker al-kicker--proof">论文一 → 论文二 · 视角切换</div>

<div class="al-flow mt-8" style="align-items:stretch;justify-content:center;">
  <div class="al-card al-card--risk" style="width:21rem;">
    <div class="hd"><span class="dot"></span>AgentFuzz · 攻击者视角</div>
    <div class="text-sm mt-2" style="color:var(--al-ink-soft);line-height:1.7;">这个 Agent Loop 里，<b style="color:var(--al-risk);">哪里</b>可能被恶意 prompt 控制？</div>
    <div class="mt-3"><span class="al-badge al-badge--risk">找污点路径</span></div>
  </div>
  <div class="al-arrow al-arrow--proof" style="min-width:4rem;"></div>
  <div class="al-card al-card--proof" style="width:21rem;">
    <div class="hd"><span class="dot"></span>zkGPT · 验证者视角</div>
    <div class="text-sm mt-2" style="color:var(--al-ink-soft);line-height:1.7;">这一步输出，是否<b style="color:var(--al-proof);">确实</b>由承诺的模型推理得到？</div>
    <div class="mt-3"><span class="al-badge al-badge--proof">给推理出证明</span></div>
  </div>
</div>

<div class="al-callout al-callout--proof mt-8">
两者落在同一批 <b>LLM 推理节点</b>上：AgentFuzz 指出"哪些 LLM 输出会影响 sink"，zkGPT 给这些输出加上"算得对"的证明。一个管攻击面，一个管可信度。
</div>

<!--
这里换到第二篇，也是换一个视角。

AgentFuzz 是攻击者视角：我能不能用 prompt 控制 Agent 的敏感动作？

zkGPT 是验证者视角：你给我的这个输出，真的是承诺模型算出来的吗？

两者不是一个问题，但都落在 LLM 推理节点上，尤其是会产生工具名、参数、SQL、代码的那些节点。一个管"哪里会被打穿"，一个管"输出可不可信"，所以后面能接起来。
-->

---
layout: two-cols-header
class: al
---

## zkGPT 问题背景：模型保密，但结果要可信

<div class="al-kicker al-kicker--proof">论文二 · 问题设定</div>

::left::

<div class="viewpoint">
矛盾点很现实：模型参数是服务商的资产，<b>不能公开</b>；但用户和监管方又想确认，输出真的来自声明的那个模型。
</div>

<div class="al-steps mt-3">
  <div class="al-step al-step--proof"><div class="idx">?</div><div><div class="t">是不是声明的模型</div><div class="d">有没有偷偷换成更小、更便宜的模型</div></div></div>
  <div class="al-step al-step--proof"><div class="idx">?</div><div><div class="t">输出是不是真算出来的</div><div class="d">有没有在中间步骤偷换结果</div></div></div>
  <div class="al-step al-step--proof"><div class="idx">?</div><div><div class="t">能不能不看参数就验证</div><div class="d">验证方不应拿到模型权重</div></div></div>
</div>

::right::

<div class="al-formula al-formula--proof mt-2">

$$y = f(x, w)$$

</div>

<div class="al-legend">
  <span><b class="k" style="color:var(--al-proof);">x</b> 输入（公开）</span>
  <span><b class="k" style="color:var(--al-proof);">w</b> 模型参数（保密）</span>
  <span><b class="k" style="color:var(--al-proof);">y</b> 输出（公开）</span>
</div>

<div class="text-sm mt-4" style="color:var(--al-ink-soft);">零知识证明（ZKP）让 prover 证明这个等式成立：</div>

<div class="al-steps mt-2">
  <div class="al-step al-step--proof"><div class="idx">✓</div><div><div class="t">y 确实 = f(x, w)</div><div class="d">这次计算按规则完成，中间没被偷换</div></div></div>
  <div class="al-step al-step--proof"><div class="idx">✓</div><div><div class="t">proof 不泄露 w</div><div class="d">验证者拿不到模型参数，却能确认结果</div></div></div>
</div>

<div class="al-callout al-callout--proof mt-3">
non-interactive：证明一旦生成，验证者可离线验证，不需要和 prover 多轮交互。
</div>

<!--
zkGPT 的背景很现实，是一个矛盾。

左边：模型参数 w 是服务商的核心资产，不能直接给别人看。但用户又有三个疑问——你用的是不是声明的模型？有没有偷偷换成小模型省成本？输出是不是真算出来的，中间有没有被改？而且验证的时候，用户还不能拿到你的模型权重。

右边就是 zkGPT 借助的工具，零知识证明。把一次推理写成 y = f(x, w)：x 是输入，公开；w 是模型参数，保密；y 是输出，公开。

ZKP 能做到两件看似矛盾的事：一是证明 y 确实等于 f(x, w)，也就是这次计算是按规则老老实实算出来的，中间没被偷换；二是这个证明不泄露 w，验证者拿不到模型参数，却依然能确认结果对。

再补一个词，non-interactive，非交互。证明一旦生成，验证者自己离线就能验，不需要反复和服务商来回交互。

注意一个边界：它证明的是计算过程，不证明语义。模型胡说八道，也可以配一个完全正确的 proof。
-->

---
layout: default
class: al
---

## zkGPT 方法论：把推理翻译成可检查的关系

<div class="al-kicker al-kicker--proof">论文二 · 四步主线</div>

<div class="viewpoint">
核心思路：先把 Transformer 推理翻译成证明系统能检查的<b>数学关系</b>，再用系统优化把 prover 时间压下来。
</div>

<div class="al-grid4 mt-6">
  <div class="al-card al-card--proof" v-click="1">
    <div class="hd"><span class="dot"></span>① 量化</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.55;">浮点数转成有限域上的整数关系，让证明系统能处理</div>
  </div>
  <div class="al-card al-card--proof" v-click="2">
    <div class="hd"><span class="dot"></span>② 约束化</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.55;">把每层拆成矩阵乘法、softmax、GeLU、normalization 等约束</div>
  </div>
  <div class="al-card al-card--proof" v-click="3">
    <div class="hd"><span class="dot"></span>③ 分后端证明</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.55;">算术关系走 GKR，非线性关系用 lookup / Lasso</div>
  </div>
  <div class="al-card al-card--proof" v-click="4">
    <div class="hd"><span class="dot"></span>④ 系统优化</div>
    <div class="text-xs" style="color:var(--al-ink-soft);line-height:1.55;">constraint fusion + circuit squeeze 降 prover 开销</div>
  </div>
</div>

<div class="al-flow mt-3" style="justify-content:center;gap:0.4rem;">
  <span class="al-chip al-chip-proof">①②③ 翻译成可检查的数学关系</span>
  <div class="al-arrow al-arrow--proof" style="min-width:2.5rem;"></div>
  <span class="al-chip al-chip-proof">④ 把 prover 时间压下来</span>
</div>

<div class="al-callout al-callout--proof mt-8" v-click="5">
四步的目标不是证明"回答语义正确"，而是证明<b>这次输出确实来自指定模型的一次推理计算</b>。
</div>

<!--
这页先别急着看协议名，看主线。

zkGPT 要做的事情很朴素：把一次 Transformer 推理，变成证明系统能检查的数学关系。一共四步。

第一步，量化。把 LLM 推理里的浮点数转成有限域上的整数，因为证明系统只能在有限域上做。

第二步，约束化。把 Transformer 每一层拆成具体约束：矩阵乘法、softmax、GeLU、normalization。

第三步，分后端证明。不同类型的关系用不同后端：算术关系，比如大批量加法乘法，走 GKR；非线性关系，用 lookup 或 Lasso 这类查表方法。

第四步，系统优化。用 constraint fusion 和 circuit squeeze 把 prover 开销降下来，不然太慢。

这四步的目标很明确：不是证明回答语义正确，而是证明这次输出确实来自指定模型的一次推理计算。
-->

---
layout: two-cols-header
class: al
---

## zkGPT 方法总览：证明的是计算图

<div class="al-kicker al-kicker--proof">论文二 · prover workflow</div>

::left::

<div class="al-figure-box">
  <img src="/image/AgentLoop/zkgpt_workflow.png" class="w-[92%] mx-auto" />
  <div class="al-figure-note">原文图：LLM prover workflow</div>
</div>

::right::

<div class="viewpoint">
Transformer 先拆成 layer，再变成 constraint，再落到 circuit 和后端协议。<b>不同类型的关系，用不同后端证明。</b>
</div>

<div class="al-steps mt-3">
  <div class="al-step al-step--proof"><div class="idx">A</div><div><div class="t">算术关系 → GKR</div><div class="d">大批量加法、乘法，比如矩阵乘法</div></div></div>
  <div class="al-step al-step--proof"><div class="idx">N</div><div><div class="t">非线性关系 → lookup / Lasso</div><div class="d">用查表检查 softmax、GeLU、normalization</div></div></div>
</div>

<div class="al-callout al-callout--proof mt-4">
抓住一句话就够：zkGPT 证明的是<b>这张计算图被正确执行了</b>，不是结果语义对不对。
</div>

<!--
这张图是 zkGPT 的整体 workflow。

流程是这样：Transformer 先被拆成一层层 layer，每层再变成 constraint 约束，约束再落到 circuit 电路和后端协议上。

关键在右边：不同类型的关系，用不同后端证明。算术关系，比如矩阵乘法里的大批量加法乘法，走 GKR。非线性关系，比如 softmax、GeLU、normalization，用 lookup 或 Lasso 这种查表思路，会便宜很多。

这里不用把协议公式推一遍。抓住一句话就够：zkGPT 证明的是这张计算图被正确执行了，不是结果语义对不对。
-->

---
layout: two-cols-header
class: al
---

## zkGPT 瓶颈：两类计算在证明系统里很贵

<div class="al-kicker al-kicker--proof">论文二 · 技术瓶颈</div>

::left::

<div class="al-card al-card--proof">
  <div class="hd"><span class="dot"></span>线性层 · 大矩阵乘法</div>
  <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.6;">
    权重矩阵大 → bookkeeping table 开销高<br/>
    grouping 利用稀疏性和量化范围压缩工作量
  </div>
</div>

<div class="al-figure-box mt-3">
  <img src="/image/AgentLoop/zkgpt_grouping.png" class="w-[78%] mx-auto" />
  <div class="al-figure-note">原文图：grouping algorithm 的直觉</div>
</div>

::right::

<div class="al-card al-card--proof">
  <div class="hd"><span class="dot"></span>非线性层 · ZKP 不友好操作</div>
  <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.6;">division · square root · exponentiation · softmax / GeLU / normalization</div>
</div>

<div class="text-sm mt-3" style="color:var(--al-ink-soft);">这些在算术电路里硬模拟代价极高。zkGPT 的策略：</div>

<div class="al-steps mt-2">
  <div class="al-step al-step--proof"><div class="idx">→</div><div><div class="t">不硬算，用 advice + lookup</div><div class="d">把复杂函数换成查表，降低证明关系数量</div></div></div>
</div>

<div class="al-callout al-callout--proof mt-4">
抓住两个瓶颈：<b>矩阵乘法规模大</b>，<b>非线性函数在证明系统里很贵</b>。下一页就是针对这两点的优化。
</div>

<!--
瓶颈分两类。

左边是线性层，主要是大矩阵乘法。矩阵大，记录中间结果的 bookkeeping table 也大。zkGPT 用 grouping，利用矩阵里大量的 padding zero 和量化后取值范围小这两个性质，把要做的工作压下来。

右边是非线性层，更麻烦。division、square root、exponentiation，还有 softmax、GeLU、normalization，这些在零知识证明里都很贵，因为证明系统本质上只擅长加法乘法。

zkGPT 的办法不是在算术电路里硬模拟这些函数，而是用 advice 加 lookup，把复杂函数换成查表，降低需要证明的关系数量。

这页只要抓住两个瓶颈：矩阵乘法规模大，非线性函数在证明系统里很贵。下一页就是针对这两点的优化。
-->

---
layout: two-cols-header
class: al
---

## zkGPT 效率优化：贴着 Transformer 结构做

<div class="al-kicker al-kicker--proof">论文二 · 效率优化</div>

::left::

<div class="al-card al-card--proof">
  <div class="hd"><span class="dot"></span>矩阵乘法优化</div>
  <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">
    · 利用 padding zero 的稀疏性<br/>
    · 利用量化后取值范围小<br/>
    · 用 grouping 降低 field multiplication 数量
  </div>
</div>

<div class="al-card al-card--proof mt-3">
  <div class="hd"><span class="dot"></span>非线性层优化</div>
  <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">
    · 除法、平方根、指数转成更便宜的 lookup / range 关系<br/>
    · 避免在算术电路里完整模拟复杂函数
  </div>
</div>

::right::

<div class="text-sm" style="color:var(--al-ink-soft);">在上面两类优化之上，再加两个系统级手段：</div>

<div class="al-steps mt-3">
  <div class="al-step al-step--proof"><div class="idx">F</div><div><div class="t">constraint fusion</div><div class="d">把可合并的约束放一起，减少非线性层证明开销</div></div></div>
  <div class="al-step al-step--proof"><div class="idx">S</div><div><div class="t">circuit squeeze</div><div class="d">把逐层证明里可并行的部分展开，提高并行度</div></div></div>
</div>

<div class="al-callout al-callout--proof mt-4">
目标很工程化：不只给理论复杂度，而是把 GPT-2 推理证明压到 <b>CPU 服务器上几十秒</b>的可接受范围。
</div>

<!--
效率优化分两块，左边是针对前面两个瓶颈的。

矩阵乘法这块，利用 padding zero 的稀疏性、量化后取值范围小，再用 grouping 降低有限域乘法的数量。

非线性层这块，把除法、平方根、指数换成更便宜的 lookup 和 range 关系，不在算术电路里完整模拟。

右边是两个系统级优化。constraint fusion，把能合并的约束放一起，减少非线性层的证明开销。circuit squeeze，把逐层证明里可以并行的部分展开，提高并行度。

这几个加在一起，目标很工程化：不是只给一个理论复杂度，而是把 GPT-2 的推理证明，压到 CPU 服务器上几十秒就能跑完。下一页看具体数字。
-->

---
layout: two-cols-header
class: al
---

## zkGPT 实验结果：GPT-2 推理证明压到 21.8 秒

<div class="al-kicker al-kicker--proof">论文二 · 主要结果</div>

::left::

<div class="viewpoint">
关键配置：fully optimized，32 线程。这组数字说明，<b>给 LLM 推理出零知识证明已经能在 CPU 上落地</b>。
</div>

<div class="al-statgrid mt-4">
  <div class="al-stat"><div class="num proof">21.8s</div><div class="lbl">prover time</div></div>
  <div class="al-stat"><div class="num proof">0.35s</div><div class="lbl">verifier time</div></div>
  <div class="al-stat"><div class="num">101K</div><div class="lbl">proof size</div></div>
  <div class="al-stat"><div class="num">≈ FP32</div><div class="lbl">量化后 PPL</div></div>
</div>

<div class="al-callout al-callout--proof mt-4">
verifier 只要 0.35 秒：生成证明慢，但验证极快——正好匹配"一次证明、多方反复验证"的场景。
</div>

::right::

<div class="al-figure-box">
  <img src="/image/AgentLoop/zkgpt_tables_3_4.png" class="w-full" />
  <div class="al-figure-note">原文表 3/4：proof time、proof size 与量化后文本质量</div>
</div>

<!--
这是 zkGPT 最重要的结果。

最终配置是全部优化打开、32 线程。三个数：prover time 21.8 秒，verifier time 0.35 秒，proof size 101K。

注意 verifier 只要 0.35 秒。这个非对称很关键——生成证明慢，但验证极快，正好匹配真实场景：服务商生成一次证明，很多用户或监管方反复验证。

表 4 是量化后的文本质量，PPL 相比 FP32 只小幅变化。所以它不是靠把模型质量大幅牺牲掉来换速度。

一句话：给 LLM 推理出零知识证明，已经能在普通 CPU 服务器上落地了。
-->

---
layout: two-cols-header
class: al
---

## zkGPT 消融：两层优化共同把时间打下来

<div class="al-kicker al-kicker--proof">论文二 · 消融分析</div>

::left::

<div class="al-figure-box">
  <img src="/image/AgentLoop/zkgpt_table_5.png" class="w-full" />
  <div class="al-figure-note">原文表 5：constraint fusion 与 circuit squeeze 的加速贡献</div>
</div>

::right::

<div class="text-sm" style="color:var(--al-ink-soft);">同一份 GPT-2 证明，去掉某层优化后的 prover time：</div>

<div class="al-steps mt-3">
  <div class="al-step al-step--proof"><div class="idx">−</div><div><div class="t">去掉 constraint 优化 → 33.2s</div><div class="d">约束层不合并，非线性证明变重</div></div></div>
  <div class="al-step al-step--proof"><div class="idx">−</div><div><div class="t">去掉 circuit 优化 → 36.5s</div><div class="d">电路层不展开，并行度下降</div></div></div>
  <div class="al-step al-step--proof"><div class="idx">✓</div><div><div class="t">两者都用 → 21.8s</div><div class="d">约束层 + 电路层共同作用</div></div></div>
</div>

<div class="al-callout al-callout--proof mt-4">
速度不是靠堆硬件，而是<b>证明系统贴着 Transformer 结构做了优化</b>。少任一层，时间都明显回升。
</div>

<!--
表 5 看这两个优化到底有没有用。

同一份 GPT-2 证明，去掉 constraint 优化，总时间从 21.8 秒涨到 33.2 秒；去掉 circuit 优化，涨到 36.5 秒；两个都用，才降到 21.8 秒。

这说明 zkGPT 的速度不是单靠 32 线程硬件堆出来的，它确实是贴着 Transformer 的结构，在约束层和电路层都做了优化。少任何一层，时间都会明显回升。

对组会理解来说，记住一句话就够：证明系统需要贴着模型结构优化，不需要展开每个协议公式。
-->

---
layout: default
class: al
---

## zkGPT 的边界：证明计算来源，不证明语义

<div class="al-kicker al-kicker--proof">论文二 · 证明边界</div>

<div class="al-vs mt-5" style="align-items:stretch;">
  <div class="al-card al-card--proof" style="flex:1;">
    <div class="hd"><span class="dot"></span>它能证明</div>
    <div class="text-sm mt-2" style="color:var(--al-ink-soft);line-height:1.8;">
      · 输出确实由承诺模型和给定输入算出<br/>
      · prover 没在中间偷换某些结果<br/>
      · proof 不公开模型参数<br/>
      · 验证者用较小开销就能检查
    </div>
  </div>
  <div class="mid">vs</div>
  <div class="al-card al-card--muted" style="flex:1;">
    <div class="hd" style="color:var(--al-ink-soft);">它不证明</div>
    <div class="text-sm mt-2" style="color:var(--al-ink-soft);line-height:1.8;">
      · 工具调用真的执行成功<br/>
      · Agent 的规划决策是安全的<br/>
      · prompt 没有被注入<br/>
      · 模型输出语义是真的<br/>
      · 被证明的节点 = Agent 全部行为
    </div>
  </div>
</div>

<div class="al-callout al-callout--proof mt-6">
有 proof，只说明"模型按承诺算出了这段输出"。它是<b>可信计算的一块拼图</b>，不是完整的 Agent 安全证明——这正好留给下一步的组合。
</div>

<!--
这页很重要，因为 zkGPT 很容易被误解。

左边是它能证明的：这个输出确实是承诺模型在给定输入上算出来的，中间没被偷换；而且证明不公开模型参数，验证者花很小开销就能检查。

右边是它不证明的，这部分更要记住。它不能证明工具调用真的执行成功，不能证明 Agent 的规划是安全的，不能证明 prompt 没被注入，更不能证明模型输出的语义是真的。它也不代表被证明的这个节点就等于整个 Agent 的全部行为。

所以有 proof，只能说明模型按承诺算出了这段输出。它是可信计算的一块拼图，不是完整的 Agent 安全证明。这个边界正好留给下一步——把它和 AgentFuzz 组合起来。
-->

---
layout: default
class: al
---

## 组合框架：先找风险路径，再给关键节点加证明

<div class="al-kicker">论文一 + 论文二 · 串联</div>

<div class="al-grid3 mt-6">
  <div class="al-card al-card--risk" v-click="1">
    <div class="hd"><span class="dot"></span>① 找路径</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">AgentFuzz 定位 prompt → LLM → parser / tool router → sink 的风险路径</div>
  </div>
  <div class="al-card al-card--brand" v-click="2">
    <div class="hd"><span class="dot"></span>② 挑节点</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">从路径里选出决定 tool、argument、code、SQL 或策略分支的关键推理</div>
  </div>
  <div class="al-card al-card--proof" v-click="3">
    <div class="hd"><span class="dot"></span>③ 加证明</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">zkGPT 为这些节点生成零知识正确性证明，可离线复查</div>
  </div>
</div>

<div class="al-flow al-flow--sm mt-5" style="justify-content:center;" v-click="4">
  <span class="al-chip al-chip-risk">找风险路径</span>
  <span class="al-arrow"></span>
  <span class="al-chip">挑关键节点</span>
  <span class="al-arrow al-arrow--proof"></span>
  <span class="al-chip al-chip-proof">加推理证明</span>
</div>

<div class="al-callout mt-6" v-click="5">
组合后的目标不是"证明整个 Agent 安全"，而是<b>选择性验证关键输出</b>：让高风险路径上的关键推理有证据可查。
</div>

<!--
现在把两篇论文接起来，这是整个报告的落点。

第一步，AgentFuzz 找风险路径，也就是 prompt 到 sink 这条线。

第二步，从路径里挑出关键 LLM 推理节点。哪些算关键？就是那些会决定工具、参数、代码、SQL 或策略分支的节点。

第三步，对这些挑出来的节点，用 zkGPT 加零知识证明，而且这个证明可以离线复查。

注意配色：红色是 AgentFuzz 管的攻击面，绿色是 zkGPT 管的可信度，中间蓝色是框架本身在做的事——选节点。

组合后的目标不是证明整个 Agent 安全，而是选择性验证关键输出：让高风险路径上的关键推理有证据可查。这是一个务实的定位。
-->

---
layout: two-cols-header
class: al
---

## 可验证 Agent Loop 的审计记录

<div class="al-kicker">落地设想 · 证据结构</div>

::left::

<div class="text-sm" style="color:var(--al-ink-soft);">对每个高风险路径，记录一条可复查证据：</div>

<div class="al-card al-card--muted mt-3" style="font-family:var(--al-mono);font-size:0.78rem;line-height:1.95;">
<span style="color:var(--al-brand);">path_id</span>　　AgentFuzz 发现的 source→sink 路径<br/>
<span style="color:var(--al-brand);">input_hash</span>　进入节点的 prompt/context hash<br/>
<span style="color:var(--al-brand);">model_commit</span> 模型参数 commitment<br/>
<span style="color:var(--al-brand);">output_hash</span>　LLM 输出 hash<br/>
<span style="color:var(--al-proof);">zk_proof</span>　　zkGPT 推理证明<br/>
<span style="color:var(--al-risk);">tool_call_log</span> 工具名、参数、返回状态
</div>

::right::

<div class="viewpoint">
核心设计：<b>证明只覆盖关键节点</b>，不覆盖所有调用。proof 和 log 分工，必须放一起看。
</div>

<div class="al-vs mt-4">
  <div class="al-card al-card--proof">
    <div class="hd" style="font-size:0.84rem;">zk_proof</div>
    <div class="text-xs" style="color:var(--al-ink-soft);">证明"模型怎么想"<br/>关键推理按承诺模型执行</div>
  </div>
  <div class="mid">+</div>
  <div class="al-card al-card--risk">
    <div class="hd" style="font-size:0.84rem;">tool_log</div>
    <div class="text-xs" style="color:var(--al-ink-soft);">记录"系统怎么做"<br/>工具动作是否真的发生</div>
  </div>
</div>

<div class="al-callout mt-4">
没有 tool log，zkGPT 只能证明模型输出，<b>不能证明工具动作真的发生过</b>。两类证据缺一不可。
</div>

<!--
如果真要落地，我会把证据记成左边这一类结构。

path_id 说明这条路径为什么危险，来自 AgentFuzz。input_hash 和 output_hash 绑定一次具体推理。model_commit 绑定模型。zk_proof 证明模型计算。tool_call_log 记录工具到底被怎么调了。

右边是最重要的一点：分工。zk_proof 证明模型怎么想，也就是关键推理确实按承诺模型算的；tool_log 记录系统怎么做，也就是工具动作有没有真的发生。

这两类证据缺一不可。如果只有 proof 没有 log，你只能证明模型输出了一个工具调用指令，但没法证明这个工具真的被执行了。所以必须放一起看。
-->

---
layout: default
class: al
---

## 安全收益与代价

<div class="al-kicker">组合方案 · 务实评估</div>

<div class="al-vs mt-5" style="align-items:stretch;">
  <div class="al-card al-card--proof" style="flex:1;" v-click="1">
    <div class="hd"><span class="dot"></span>收益</div>
    <div class="text-sm mt-2" style="color:var(--al-ink-soft);line-height:1.85;">
      · 高风险路径更可审计<br/>
      · 关键 LLM 输出不能被服务商随意替换<br/>
      · proof 可离线验证，适合事后审计<br/>
      · AgentFuzz 的结果指导"哪里值得加证明"
    </div>
  </div>
  <div class="mid">vs</div>
  <div class="al-card al-card--muted" style="flex:1;" v-click="2">
    <div class="hd" style="color:var(--al-ink-soft);">代价</div>
    <div class="text-sm mt-2" style="color:var(--al-ink-soft);line-height:1.85;">
      · 证明仍有成本，不适合给每次调用都加<br/>
      · zkGPT 当前实验聚焦 GPT-2 级别模型<br/>
      · proof 不覆盖工具、数据库、文件的真实执行<br/>
      · AgentFuzz 只覆盖已建模的 sink 与威胁模型
    </div>
  </div>
</div>

<div class="al-callout al-callout--proof mt-6" v-click="3">
所以合理策略是 <b>selective verification</b>：只证明会影响敏感 sink 的关键推理节点，而不是全量证明。
</div>

<!--
组合以后，好处是关键路径更容易审计，服务商也不容易随便替换关键输出。

但代价也明显。证明不是免费的，zkGPT 现在实验还是 GPT-2 级别。

AgentFuzz 也受 sink 列表、威胁模型和时间预算限制。

所以更合理的做法不是全量证明，而是只证明高风险节点。
-->

---
layout: default
class: al
---

## 组合方案的边界：可验证不等于安全

<div class="al-kicker">组合方案 · 能力边界</div>

<div class="viewpoint mt-4">
这条链路提高的是<b>可验证性</b>，不能直接等价于"安全"。下表把两篇论文各自管到哪、管不到哪摆清楚。
</div>

<div class="plain-table mt-4">

| 关心的问题 | AgentFuzz | zkGPT |
| --- | --- | --- |
| 恶意 prompt 能不能到达 sink | <b style="color:var(--al-risk)">能测试</b> | 不处理 |
| LLM 推理是否按承诺模型执行 | 不处理 | <b style="color:var(--al-proof)">能证明</b> |
| 工具是否真实执行成功 | 不处理 | 不处理 |
| Agent 规划是否安全 | 间接暴露风险 | 不证明 |
| 事后审计是否有证据 | 提供风险路径 + PoC | 提供推理 proof |

</div>

<div class="al-callout mt-4">
两者都答不上"工具是否真实执行"这一行——组合后是<b>可审计 Agent Loop</b>，不是完全安全 Agent Loop。
</div>

<!--
这张表就是边界。

AgentFuzz 能测恶意 prompt 能不能到 sink，但不证明推理计算。

zkGPT 能证明推理计算，但不处理 prompt injection，也不证明工具执行。

特别注意"工具是否真实执行成功"这一行，两篇论文都打了"不处理"。所以组合后更像可审计 Agent Loop，不是完全安全 Agent Loop。

这个说法要保守一点。
-->

---
layout: default
class: al
---

## 未来演进方向：从单点防御到链路治理

<div class="al-kicker">展望 · 四个方向</div>

<div class="al-grid4 mt-6">
  <div class="al-card al-card--risk" v-click="1">
    <div class="hd"><span class="dot"></span>① 路径发现</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">找出 prompt、observation、memory 会流向哪些敏感操作</div>
  </div>
  <div class="al-card al-card--brand" v-click="2">
    <div class="hd"><span class="dot"></span>② 选择性证明</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">只给影响 tool、argument、code、SQL 的关键推理加 proof</div>
  </div>
  <div class="al-card al-card--proof" v-click="3">
    <div class="hd"><span class="dot"></span>③ 执行验证</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">用日志、sandbox、attestation 记录工具是否真的执行</div>
  </div>
  <div class="al-card al-card--brand" v-click="4">
    <div class="hd"><span class="dot"></span>④ 端到端审计</div>
    <div class="text-xs mt-1" style="color:var(--al-ink-soft);line-height:1.65;">把路径、proof、tool log 绑定成可复查证据链</div>
  </div>
</div>

<div class="al-callout mt-8" v-click="5">
更可能落地的是<b>可审计 Agent Loop</b>，而不是一次性证明整个 Agent 完全安全。
</div>

<!--
往后看，我觉得方向不是做一个大而全的证明。

Agent 太复杂了，外部工具、环境状态、日志、权限都在变。

更现实的路是拆开做：先找路径，再证明关键推理，再记录工具执行，最后把这些证据串起来审计。

这也是这两篇论文放在一起最有意思的地方。
-->

---
layout: default
class: al
---

## 后续研究建议：先讲清链路，再谈机制

<div class="al-kicker">展望 · 四步法</div>

<div class="al-steps mt-5">
  <div class="al-step"><div class="idx">1</div><div><div class="t">先画数据流</div><div class="d">source、parser、tool router、sink 分别在哪里</div></div></div>
  <div class="al-step"><div class="idx">2</div><div><div class="t">再定威胁模型</div><div class="d">攻击者控制 prompt、网页、memory，还是工具返回</div></div></div>
  <div class="al-step"><div class="idx">3</div><div><div class="t">再选证明对象</div><div class="d">证明模型计算、工具执行，还是策略约束</div></div></div>
  <div class="al-step"><div class="idx">4</div><div><div class="t">最后做实验</div><div class="d">同时报告安全效果、误报漏报、成本与可用性</div></div></div>
</div>

<div class="al-callout mt-6">
一句话：<b>先把链路讲清楚，再谈机制</b>。否则很容易做成"看起来安全，但不知道保护了什么"。
</div>

<!--
如果后面有同学想做 Agent 安全，我建议先别急着起大名字。

先画数据流。source 在哪，parser 在哪，router 在哪，sink 在哪。

再定威胁模型：攻击者能控制 prompt、网页内容、memory，还是工具返回？

最后再选机制。ZK、sandbox、fuzzing、日志都只是工具，先弄清楚自己保护什么。
-->

---
layout: default
class: al
---

## 总结

<div class="al-kicker">全篇收束</div>

<div class="grid grid-cols-2 gap-4 mt-5">
  <div class="al-card al-card--risk" v-click="1">
    <div class="hd"><span class="dot"></span>AgentFuzz：找"哪里危险"</div>
    <div class="text-xs mt-2" style="color:var(--al-ink-soft);line-height:1.8;">
      用 directed greybox fuzzing 找 taint-style 漏洞。20 个开源 Agent 上发现 <b style="color:var(--al-risk)">34 个 0-day</b>，precision 100%，已有 23 个 CVE ID。
    </div>
  </div>
  <div class="al-card al-card--proof" v-click="2">
    <div class="hd"><span class="dot"></span>zkGPT：证"是否按承诺执行"</div>
    <div class="text-xs mt-2" style="color:var(--al-ink-soft);line-height:1.8;">
      用非交互零知识证明验证 LLM 推理。GPT-2 上 32-thread all-opt 配置 prover <b style="color:var(--al-proof)">21.8s</b>，verifier 0.35s，proof 101K。
    </div>
  </div>
</div>

<div class="viewpoint mt-5" v-click="3">
<b>系统背景</b>：Agent 正从"模型输出文本"走向"闭环执行系统"。一旦模型输出会控制工具，安全就变成数据流、证明和审计问题。
</div>

<div class="al-callout mt-3" v-click="4">
两者结合提高 Agent Loop 的<b>可审计性</b>，但不替代工具执行验证和规划安全分析。
</div>

<!--
最后收一下。

第一，Agent 正在从文本回答变成闭环执行系统。只要模型输出能控制工具，安全边界就不只在模型内部。

第二，AgentFuzz 是风险发现工具。它找的是 prompt 到 sink 的路径。

第三，zkGPT 是推理证明工具。它证明关键输出是不是按承诺模型算出来。

两者放在一起，能让 Agent Loop 更可审计。但它还不是完整安全方案。工具执行、规划安全、外部状态，都还要单独处理。
-->

---
layout: default
class: al refs-slide
---

## 参考资料

- ReAct 论文：<https://arxiv.org/abs/2210.03629>
- OpenAI Agents SDK 文档：<https://openai.github.io/openai-agents-python/>
- OpenAI Practical Guide to Building Agents：<https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf>
- Anthropic Building Effective Agents：<https://www.anthropic.com/engineering/building-effective-agents>
- Model Context Protocol 官方介绍：<https://modelcontextprotocol.io/introduction>
- AgentFuzz USENIX 官方页面：<https://www.usenix.org/conference/usenixsecurity25/presentation/liu-fengyu>
- AgentFuzz 论文 PDF：<https://www.usenix.org/system/files/usenixsecurity25-liu-fengyu.pdf>
- zkGPT USENIX 官方页面：<https://www.usenix.org/conference/usenixsecurity25/presentation/qu-zkgpt>
- zkGPT 正式版 PDF：<https://www.usenix.org/system/files/usenixsecurity25-qu-zkgpt.pdf>
- zkGPT 预发表版 PDF：<https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-516-qu-zkgpt.pdf>

<div class="mt-8 text-sm">

本报告中的论文截图均来自上述 PDF，概念串联部分为基于两篇论文边界的组合分析。

</div>

<!--
参考资料放在这里。

论文截图都来自原文 PDF。前面把 AgentFuzz 和 zkGPT 接起来的那条线，是我基于两篇论文能力边界做的组合分析，不是某篇论文已经提出了一个完整系统。
-->

---
layout: end
---

# 谢谢

## 欢迎提问与讨论

<div class="mt-8 text-sm">

一个问题可以作为讨论入口：如果只能给 Agent Loop 的一类节点加证明，应该优先证明 tool selection、argument generation，还是 final answer generation？

</div>

<!--
最后留一个讨论问题。

如果证明资源有限，优先证明哪类节点？

我个人会先选 tool selection 和 argument generation。因为它们直接决定真实操作。

final answer generation 更像展示层，风险通常低一些。
-->
