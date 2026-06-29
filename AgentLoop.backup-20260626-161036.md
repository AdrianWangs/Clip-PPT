---
theme: seriph
background: /image/slides/image.png
title: "Agent Loop 的安全检测与可验证推理"
info: |
  ## 两篇 USENIX Security 2025 论文的组合报告
  从污点型漏洞检测到 LLM 推理正确性证明
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

<div class="text-[4.05rem] leading-[1.08] font-bold">
Agent Loop 的安全检测<br />
与可验证推理
</div>

<div class="mt-5 text-[2rem] font-bold">
AgentFuzz 与 zkGPT 论文汇报
</div>

<div class="mt-6 text-sm">

**论文一：** Make Agent Defeat Agent: Automatic Detection of Taint-Style Vulnerabilities in LLM-based Agents

**论文二：** zkGPT: An Efficient Non-interactive Zero-knowledge Proof Framework for LLM Inference

**会议：** USENIX Security 2025 · CCF-A

</div>

<div class="absolute bottom-8 right-8">
  <p class="text-sm">主讲人：王宇哲</p>
</div>

<!--
我先解释一下为什么选这个题。

我原来的方向是 RAG 加密码学，主要关心检索增强系统里的隐私、可信和可验证。但最近真去找论文会发现，这个交叉点的高质量新论文不多，能拿来做组会汇报的更少。

另一个现实情况是，现在大家的研究重心都在往 AI 系统走，尤其是 Agent。模型不只是回答问题，它开始调用工具、写代码、查数据库，安全问题也跟着变复杂。

所以我没有硬找一篇很窄的 RAG 加密码学论文，而是选了 AgentFuzz 和 zkGPT 放在一起讲。

AgentFuzz 讲 Agent 的攻击面，zkGPT 讲模型推理证明。一个偏 AI Agent，一个偏密码学。合起来看，还是在讲我关心的那条线：AI 系统怎么变得更可信、更可验证。

我讲这两篇还有一个目的：不是把题目带成单纯的 AI 安全，而是给大家一个方向，看看前沿 AI 和我们做的密码学能不能接起来。

AI 系统现在跑得很快，但里面很多问题并不只是模型问题。比如隐私怎么保护，关键推理怎么证明，工具调用怎么审计，外部数据怎么可信接入。这些地方其实都能放进密码学方法。

所以这里的“AI 加密码学”要落到具体问题上：在 AI 场景里用密码学处理证明、隐私、审计、访问控制。以后如果继续做 RAG、Agent 或多模态系统，选题可以从这些切入点往下挖。

也借这次组会，让大家看看现在 AI 前沿里，除了模型效果，还有系统安全、证明和可审计这些问题。

今天不是单讲一篇论文，而是把两篇论文放在一起看。

AgentFuzz 讲的是怎么测 Agent 里的漏洞：恶意 prompt 有没有机会一路跑到 eval、SQL、shell 这些危险位置。

zkGPT 讲的是另一个问题：模型服务商能不能证明，这个输出真的是某个模型算出来的，而且不用公开模型参数。

我把它们放在一起，是想讲一件事：Agent 现在不只是回答问题，它会驱动工具。安全问题也就不只在回答里，而是在整条执行链路里。
-->

---
layout: default
---

## 背景：AI 系统从文本生成走向闭环执行

<div class="text-sm mt-2">
主线：模型先解决“怎么生成文本”，再解决“怎么决定动作”，最后进入“怎么执行、怎么留证据”的系统问题。
</div>

<div class="evolution-board mt-4">

<div class="evolution-step">
  <div class="evolution-index">01</div>
  <div class="evolution-title">语言模型</div>
  <div class="evolution-sub">Prompt → Text</div>
  <ul>
    <li>根据上下文预测 token</li>
    <li>输出回答、代码或计划</li>
    <li>计划需要人或系统接着做</li>
  </ul>
  <div class="evolution-turn">边界在文本：回答是否可信</div>
</div>

<div class="evolution-step">
  <div class="evolution-index">02</div>
  <div class="evolution-title">Agent</div>
  <div class="evolution-sub">Goal → Action</div>
  <ul>
    <li>把任务拆成多步</li>
    <li>选择工具或下一步动作</li>
    <li>接收 observation 后继续推理</li>
  </ul>
  <div class="evolution-turn">边界外移：输出开始决定动作</div>
</div>

<div class="evolution-step">
  <div class="evolution-index">03</div>
  <div class="evolution-title">Harness</div>
  <div class="evolution-sub">Model + Tools + Runtime</div>
  <ul>
    <li>接入 tools、memory、guardrails</li>
    <li>解析模型输出并路由工具</li>
    <li>记录 tracing/logs</li>
  </ul>
  <div class="evolution-turn">风险进入 parser、router、tool 参数</div>
</div>

<div class="evolution-step">
  <div class="evolution-index">04</div>
  <div class="evolution-title">Loop Engineering</div>
  <div class="evolution-sub">Observe → Reason → Act → Verify</div>
  <ul>
    <li>控制上下文进入模型</li>
    <li>约束工具调用和停止条件</li>
    <li>沉淀 proof、log 和审计证据</li>
  </ul>
  <div class="evolution-turn">问题变成可控、可证明、可审计</div>
</div>

</div>

<div class="evolution-axis mt-5">
  <span>文本生成</span>
  <span>行动决策</span>
  <span>系统接入</span>
  <span>证据审计</span>
</div>

<div class="caption">递进关系：文本能力增强 → 外部工具接入 → 安全边界外移 → 需要检测、证明和审计</div>

<!--
这一页我想先把 AI 系统本身的发展背景讲明白。

前面我解释了为什么要讲 AI 加密码学。这里如果直接跳到 AgentFuzz 和 zkGPT，会显得这两篇论文像是硬凑到一起的，好像没什么关系。实际上，它们都对应 AI 系统从“文本生成”走向“闭环执行”以后出现的新问题。

最早我们把大模型当成文本生成器。输入 prompt，输出回答、代码或者计划。这个阶段的边界比较清楚：模型说了什么，用户再决定要不要信。

后来变成 Agent。模型不只是写计划，而是开始决定下一步动作。比如要不要调用搜索，要不要执行代码，要不要查数据库。到这里，模型输出就不只是文本了，它会影响外部环境。

再往后是 Harness。模型本身不会直接连数据库，也不会自己开 shell。Harness 把工具、memory、权限、日志接进来，也负责解析模型输出。很多安全问题就是在这里出现的：一句自然语言，最后变成了一个工具参数。

最后才是 Loop Engineering。系统要管整轮循环：上下文怎么进模型，工具怎么约束，什么时候停，出了问题之后有没有证据。

所以这页的递进关系是：从文本生成，到行动决策，到工具执行，再到证据审计。

AgentFuzz 和 zkGPT 就落在这条线上。AgentFuzz 关注执行链路里哪里可能被恶意 prompt 控制；zkGPT 关注关键推理输出能不能被证明。这样后面讲两篇论文就不是散的，而是顺着 AI 系统演进讲下去。
-->

---
layout: two-cols-header
---

## 背景一：语言模型

::left::

<div class="viewpoint">
观点：语言模型的输出仍是文本，安全边界主要停留在“回答是否可信”。
</div>

语言模型的基本形态是：

- 输入一段上下文
- 预测下一个 token
- 生成文本回答
- 通过指令和示例完成任务

<div class="small mt-5">

在这个阶段，模型主要是一个文本函数：输入 prompt，输出 answer。它可以生成计划，但计划本身不会自动执行。

</div>

::right::

<div class="img-figure bg-figure">
  <img src="/image/AgentLoop/agentloop-bg-language-model-flat.png" />
</div>

<div class="caption">科研绘图：语言模型仍是文本输入到文本输出</div>

语言模型可以解释问题、组织答案、生成代码或计划。

但它本身不直接执行外部动作：

- 不访问真实数据库
- 不调用真实工具
- 不维护长期状态
- 不负责执行结果验证

<!--
先看最早的形态：语言模型。

它很强，可以写代码、写计划、解释问题。但它本质上还是文本进、文本出。

它说“我查了数据库”，不代表它真的查了。没有外部系统配合，它只是生成了这句话。

所以这一阶段的安全问题，更多是回答可不可信，不是执行链路有没有被打穿。
-->

---
layout: two-cols-header
---

## 背景二：Agent

::left::

<div class="viewpoint">
观点：Agent 的关键变化不是“更会聊天”，而是模型输出进入 ReAct 式行动循环。
</div>

Agent 的变化在于：模型输出开始进入行动循环。

典型循环是：

1. 读取任务和上下文
2. 生成下一步计划
3. 选择工具或动作
4. 接收 observation
5. 继续下一轮推理

::right::

<div class="img-figure bg-figure">
  <img src="/image/AgentLoop/agentloop-bg-react-agent-flat.png" />
</div>

<div class="caption">科研绘图：ReAct 把推理、行动和观察连成循环</div>

ReAct 把 reasoning 和 acting 交错起来。这一步让模型从“回答问题”变成“推进任务”。

<div class="small mt-5">

AgentFuzz 论文里的 Agent Loop 更接近这种 ReAct 式循环：模型先推理，再选择动作，工具返回 observation 后继续推理。

</div>

<!--
到 Agent 之后，事情就变了。

模型不只是给人看答案，而是参与一个循环：想一步、做一步、看反馈，再想下一步。

ReAct 就是这种思路的代表。

这里要注意，AgentFuzz 论文里的 Agent Loop 也更像这个东西：模型输出动作，工具返回 observation，然后继续。
-->

---
layout: two-cols-header
---

## 背景三：Agent Harness

::left::

<div class="viewpoint">
观点：Harness 是模型和真实系统之间的连接层，也是很多 source-to-sink 风险出现的位置。
</div>

Harness 是模型外面的运行框架。

它通常包含：

- instructions：任务规则
- tools：可调用能力
- memory/context：历史和外部信息
- guardrails：输入输出约束
- tracing/logs：执行记录
- handoff：不同 Agent 或人工接力

::right::

<div class="img-figure bg-figure">
  <img src="/image/AgentLoop/agentloop-bg-harness-flat.png" />
</div>

<div class="caption">科研绘图：Harness 把模型输出连接到真实工具</div>

真实风险通常出现在 harness 连接处：

- LLM 输出进入 parser / router
- tool 参数进入代码、SQL、shell
- observation 回到上下文

<div class="small mt-3">

AgentFuzz 关注的就是这些连接点上的 source-to-sink 路径。

</div>

<!--
Harness 可以理解成 Agent 的外壳。

模型自己不会直接碰数据库，也不会自己执行 shell。真正把这些能力接进来的，是 harness。

它会解析模型输出，决定调哪个工具，把参数传下去，再把结果塞回上下文。

很多漏洞就出在这里：模型一句话，经过 parser 和 router，最后变成了真实操作。
-->

---
layout: two-cols-header
---

## 背景四：Loop Engineering

::left::

<div class="viewpoint">
观点：Loop Engineering 的对象不是单次 prompt，而是每轮输入、输出、工具执行和证据记录。
</div>

Prompt engineering 关注单次输入。

Loop Engineering 关注闭环系统：

- 上下文如何进入模型
- 模型输出如何被解析
- 工具调用如何约束
- observation 如何回填
- 什么时候停止
- 如何记录和评估

::right::

<div class="img-figure bg-figure">
  <img src="/image/AgentLoop/agentloop-bg-loop-engineering-flat.png" />
</div>

<div class="caption">科研绘图：Loop Engineering 关注每一轮输入、执行和审计</div>

当系统进入 loop，安全问题也变成链路问题：

1. 输入是否会污染工具参数
2. 关键推理是否可验证
3. 工具执行是否有可靠记录
4. 事后审计是否能复现链路

<div class="small mt-3">

这正是 AgentFuzz 和 zkGPT 可以连接起来的原因。

</div>

<!--
到 Loop Engineering 这一步，问题就不是“prompt 怎么写得更好”了。

要看整轮循环：模型看到什么、能调用什么、工具怎么约束、什么时候停、日志怎么记。

后面为什么能把 AgentFuzz 和 zkGPT 放在一起，也是因为这里。

一个负责找危险路径，一个负责证明关键推理。工具到底有没有执行，还得看日志。
-->

---
layout: default
---

## 研究问题：Agent Loop 的安全检测与推理证明

<div class="problem-viewpoint">
观点：真正需要保护的不是所有输出，而是会进入工具选择、参数生成、代码片段或策略分支的关键 LLM 输出。
</div>

<div class="img-figure problem-image mt-5">
  <img src="/image/AgentLoop/agentloop-research-problem-flat.png" />
</div>

<div class="mt-3 text-xs">

读图：AgentFuzz 找 taint path；zkGPT 证明关键 LLM step；tool logs 记录工具执行事实。

</div>

<!--
这页是整场报告的总图。

上面红线是攻击链：恶意 prompt 能不能从 LLM output 一路走到 sink。

下面蓝线是证明链：关键 LLM step 能不能留下 proof，之后进入 audit record。

别把 zkGPT 理解成“证明整个 Agent 安全”。它只证明模型计算。工具执行这件事，还是要看 tool logs。
-->

---
layout: two-cols-header
---

## 背景五：污点型漏洞检测

::left::

Agent Loop 中，恶意输入可能从 prompt 或 observation 出发，经过 LLM、parser 和 tool router，最终进入敏感操作。

典型 sink 包括：

- 代码执行
- SQL 执行
- shell 命令
- 网络请求
- 文件操作

::right::

### 对应论文：AgentFuzz

AgentFuzz 解决的问题是：

<div class="mt-5 text-center text-lg">

把 prompt 当 source，把代码、SQL、shell 当 sink，自动测试中间链路能不能打通

</div>

它的定位是安全测试，不是运行时防御。

<div class="takeaway">
先找出“哪里可能被恶意输入控制”，后面才知道哪些节点值得修复、隔离或加证明。
</div>

<!--
先讲第一条线，污点型漏洞检测。

source 就是攻击者能控制的输入，比如 prompt 或 observation。sink 是危险操作，比如 eval、SQL、shell。

Agent 让这个问题变麻烦，因为中间多了 LLM。输入不是直接进 sink，而是先被模型解释成工具和参数。

AgentFuzz 要做的就是把这条链路测出来。
-->

---
layout: two-cols-header
---

## 背景六：LLM 推理证明

::left::

在关键节点上，系统可能需要确认：

- 服务商是否用了声明的模型
- 输出是否由该模型推理得到
- 中间计算是否被篡改
- 模型参数是否仍然保密

::right::

### 对应论文：zkGPT

zkGPT 解决的问题是：

<div class="mt-5 text-center text-lg">

在不公开模型参数的前提下，证明输出确实由指定模型算出

</div>

它证明的是计算正确性，不证明回答语义正确。

<div class="takeaway">
它验证“这个输出从哪里来”，不验证“这个输出是否安全”，也不验证“工具是否执行成功”。
</div>

<!--
第二条线是推理证明。

有些场景里，服务商不想公开模型参数，但用户又想知道：你到底是不是按承诺的模型跑的？

zkGPT 解决的就是这个问题。

它能证明这次输出确实来自某个模型推理，但不证明这句话是对的，也不证明工具真的执行成功。
-->

---
layout: two-cols-header
---

## Agent Loop 的基本结构

::left::

<div class="viewpoint">
观点：AgentFuzz 论文中的 Agent Loop 更接近 ReAct 式循环，核心是“推理输出”如何变成“工具动作”。
</div>

Agent 不只是“问模型一句话”。

它通常会做四步：

1. 接收用户 prompt
2. 拼接系统 prompt 和上下文
3. 让 LLM 生成动作计划或工具调用参数
4. 解析输出并执行工具

<div class="small mt-5">

风险点在第 4 步：LLM 输出从文本变成真实操作。这里的 loop 可以理解为 simplified ReAct workflow。

</div>

<div class="takeaway">
这里的关键 LLM 输出，通常不是 final answer，而是 tool name、argument、code、SQL 或策略分支。
</div>

::right::

<img src="/image/AgentLoop/agentfuzz_workflow.png" class="w-full mt-4" />

<div class="caption">原文图：LLM-based Agent 的简化工作流</div>

<!--
这里回到 AgentFuzz 的论文图。

普通聊天是模型吐一段文本。Agent 多了一步：把文本解析成动作。

比如模型输出一个 JSON，说 tool 是 calc，参数是 1+1。Harness 看到以后，就真的调用工具。

风险就在这里。文本一旦变成动作，安全边界就往外扩了。
-->

---
layout: two-cols-header
---

## AgentFuzz：污点型漏洞模型

::left::

taint-style 漏洞的结构很简单：

- **source**：攻击者可控输入，例如 user prompt
- **propagation**：输入经过 LLM、parser、tool router 等中间层传播
- **sink**：安全敏感操作，例如 `eval`、SQL 执行、命令执行

问题不是“prompt 看起来恶不恶意”，而是：

<div class="mt-4 text-center text-lg">

攻击者输入是否能流到 sink

</div>

::right::

<img src="/image/AgentLoop/agentfuzz_vuln_example.png" class="w-[82%] mx-auto" />

<div class="caption">原文图：真实 Agent 漏洞示例，恶意 prompt 最终进入 `eval`</div>

<!--
taint-style 这个词不用想复杂。

source 是攻击者能控制的东西，sink 是不能乱喂用户输入的地方。

中间经过 LLM、parser、router。只要攻击者输入能一路流到 sink，就有问题。

Agent 的难点是这条路不直，中间有模型在“翻译”用户意图。
-->

---
layout: two-cols-header
---

## AgentFuzz：设计动机

::left::

<div class="viewpoint">
观点：AgentFuzz 的目标不是判断 prompt 是否恶意，而是验证模型输出能不能被诱导到 sink。
</div>

传统 fuzzing 处理的是结构化输入。

Agent 场景不同：

- 输入是自然语言 prompt
- 触发 sink 需要语义对齐
- 代码路径里有很多动态调用
- 变异时不能只改字节，还要改意图和参数

::right::

论文把难点拆成三个问题：

1. 怎么生成能调用目标功能的 seed prompt
2. 怎么优先选择更可能到达 sink 的 seed
3. 怎么变异 prompt，让它既语义正确，又满足路径约束

<div class="small mt-5">

这里的 seed 是 fuzzing 的初始测试输入。AgentFuzz 的 seed 不是字节串，而是一段自然语言。

</div>

<div class="takeaway">
可以把方法压成三句话：先走到目标功能，再逼近敏感 sink，最后把 payload 放到会流向 sink 的参数里。
</div>

<!--
传统 fuzzing 可以改字节、改字段。

但 Agent 的输入是自然语言。你随便乱改，模型可能根本不会调目标工具。

所以 AgentFuzz 不是简单多生成几个 prompt。它要让 prompt 朝着某个 sink 走。

说白了，先让 Agent 走到目标功能附近，再想办法把 payload 送进去。
-->

---
layout: default
---

## AgentFuzz 方法总览

<img src="/image/AgentLoop/agentfuzz_architecture.png" class="w-[96%] mx-auto mt-3" />

<div class="caption">原文图：AgentFuzz 的三个阶段</div>

<div class="mt-5 text-sm">

读图方式：第一阶段生成能调用目标功能的 seed；第二阶段根据执行反馈选择更有希望的 seed；第三阶段按 sink 约束变异 prompt。整体目标是把测试资源集中到更可能触发 sink 的路径上。

</div>

<!--
这张图不用每个框都细讲。

就看三步：第一步生成 seed，先把 Agent 引到相关功能；第二步跑起来看 trace，挑更有希望的 seed；第三步按 sink 约束去变异 prompt。

这和普通随机 fuzzing 的区别很明显。它是带方向的。
-->

---
layout: two-cols-header
---

## AgentFuzz 阶段一：功能相关 seed 生成

::left::

AgentFuzz 先做静态分析：

- 识别预定义 sink，例如 SQL injection、code injection
- 从 sink 反向找 call chain
- 利用类名、方法名里的自然语言语义
- 让 LLM 生成 functionality-specific seed prompt

<div class="small mt-5">

例子：方法名里出现 `PermissionCheck`、`similarity_search`，这些词本身就暗示了 Agent 需要被诱导到什么功能。

</div>

::right::

### 设计目标

传统 fuzzer 不知道怎么写自然语言 prompt。

AgentFuzz 的策略是利用代码里的语义线索，让 LLM 生成“像用户请求”的测试输入。

<div class="mt-6 text-sm">

关键不是生成攻击 payload，而是先让 Agent 走到目标功能附近。

</div>

<!--
第一阶段是 seed generation。

它不是一上来写攻击 prompt，而是先根据代码里的名字和 call chain 推断功能。

比如方法名里有 PermissionCheck，seed 就应该像一个需要权限检查的用户请求。

如果连目标工具都调不到，后面 payload 再厉害也没用。
-->

---
layout: two-cols-header
---

## AgentFuzz 阶段二：反馈驱动 seed 调度

::left::

AgentFuzz 的 seed 分数来自三类反馈：

- 语义分数：prompt 语义是否贴近目标组件
- 距离分数：执行 trace 离 sink 还有多远
- 惩罚分数：避免反复选同一个 seed 或同一条 call chain

最终形式是：

<div class="text-center mt-4">

$F_s = \alpha S_s + \beta D_s - P_s$

</div>

<div class="small mt-3">

$S_s$ 表示语义是否贴近目标组件；$D_s$ 表示 trace 离 sink 的远近；$P_s$ 用来减少重复探索。

</div>

::right::

### 设计依据

两个 seed 可能离 sink 的控制流距离一样，但语义完全不同。

Agent 场景里，语义决定模型会不会选择正确工具。

所以 AgentFuzz 同时看：

- 代码距离
- 运行 trace
- prompt 与目标组件的语义一致性

<!--
第二阶段是 seed scheduling。

只看控制流距离不够。两个 prompt 可能离 sink 一样近，但语义完全不一样。

在 Agent 里，语义会影响模型选哪个工具。

所以它同时看三件事：语义像不像、trace 离 sink 远不远、有没有重复探索。
-->

---
layout: two-cols-header
---

## AgentFuzz 阶段三：sink-guided seed mutation

::left::

AgentFuzz 有两类变异器：

- **功能变异器**：调整 prompt 的任务意图，让它更贴近目标组件
- **参数变异器**：根据运行时参数和路径约束，改动 prompt 中会流向 sink 的片段

如果 sink 已经被触达，就把 PoC payload 插入到对应参数位置。

::right::

### 设计目标

普通 prompt mutation 容易把语义改坏。

AgentFuzz 的变异更有目标：

1. 先让模型选择正确功能
2. 再让参数满足路径约束
3. 最后用 oracle 判断漏洞是否被触发

<div class="small mt-5">

oracle 是判定器，用来判断某个输入是否真的触发了漏洞。

</div>

<!--
第三阶段是 mutation。

这里分两层：先改任务意图，让模型更可能选到目标功能；再改参数，让它满足 sink 前面的条件。

如果已经摸到 sink 附近，就把 PoC payload 插到那个会流过去的参数里。

这比随机改 prompt 稳很多。
-->

---
layout: two-cols-header
---

## AgentFuzz 实验设置

::left::

论文评估了 20 个开源 Agent：

- 都是 GitHub 上较流行的 Agent 应用
- 13 个超过 10,000 stars
- 覆盖 828 个 sink callsites
- 使用 GPT-4o 作为 AgentFuzz 和被测 Agent 的基础模型
- 每个 sink callsite 设置 5 分钟 timeout

::right::

<img src="/image/AgentLoop/agentfuzz_dataset_table.png" class="w-[88%] mx-auto" />

<div class="caption">原文表：20 个 Agent 数据集和漏洞统计</div>

<!--
实验设置简单看两个数。

第一，数据集不是玩具项目，是 20 个真实开源 Agent，很多 star 数不低。

第二，论文盯的是 828 个 sink callsites。

它最后报告 34 个潜在漏洞，再人工确认。目标不是证明系统安全，而是尽量把高风险路径找出来。
-->

---
layout: two-cols-header
---

## AgentFuzz 实验结果

::left::

<img src="/image/AgentLoop/agentfuzz_table_2.png" class="w-full mt-4" />

<div class="caption">原文表 2：AgentFuzz 与 LLMSmith 对比</div>

### 主要结果

- AgentFuzz：34 TP，0 FP，1 FN
- precision：100%
- recall：97.14%
- LLMSmith precision：2.92%

::right::

<img src="/image/AgentLoop/agentfuzz_table_3.png" class="w-full mt-4" />

<div class="caption">原文表 3：消融实验</div>

### 消融结果

去掉 seed generation、scheduling、semantic score 或 mutation，recall 都明显下降。

这说明 AgentFuzz 的三个模块不是装饰，而是共同决定能不能触发 sink。

<!--
这里看表 2 和表 3。

表 2 里 AgentFuzz 找到 34 个 true positives，0 个 false positives。对比 LLMSmith，误报少很多。

表 3 是消融。去掉 seed generation、scheduling、semantic score 或 mutation，recall 都会掉。

所以三个模块不是摆设。自然语言 seed、语义反馈、sink-guided mutation 都有用。
-->

---
layout: default
---

## AgentFuzz 的输出与作用边界

AgentFuzz 的输出不是“系统已经安全”，而是：

- 哪些 source-to-sink 路径可以被 prompt 触发
- 哪些 Agent 功能会调用安全敏感操作
- 哪些 LLM 输出会成为工具名、参数或代码片段
- 哪些路径需要开发者修复、隔离或加审计

<div class="mt-7 text-sm">

放到可验证 Agent Loop 里，AgentFuzz 的角色是风险定位：它告诉我们哪些 LLM 推理节点值得重点保护。

</div>

<!--
AgentFuzz 的输出不是“这个系统安全了”。

它输出的是路径：哪些 prompt 可以影响哪些 sink，哪些功能会碰危险操作。

这个结果很适合接到后面的 zkGPT。

因为不是每个 LLM 调用都值得证明。真正值得加证明的，是那些会决定工具、参数、代码片段的推理节点。
-->

---
layout: default
---

## 从风险发现到推理证明

AgentFuzz 回答的是攻击面问题：

<div class="mt-4 text-center text-lg">

这个 Agent Loop 里，哪里可能被恶意 prompt 控制？

</div>

zkGPT 回答的是计算正确性问题：

<div class="mt-4 text-center text-lg">

这一步 LLM 输出，是否确实由承诺的模型推理得到？

</div>

<div class="mt-8 text-sm">

两者的连接点是 LLM 推理节点：AgentFuzz 找出“哪些 LLM 输出会影响 sink”，zkGPT 给这些输出加证明。

</div>

<!--
这里换到第二篇。

AgentFuzz 是攻击者视角：我能不能用 prompt 控制 Agent 的敏感动作？

zkGPT 是验证者视角：你给我的这个输出，真的是承诺模型算出来的吗？

两者不是一个问题，但都落在 LLM 推理节点上。尤其是会产生工具名、参数、SQL、代码的节点。
-->

---
layout: two-cols-header
---

## zkGPT：问题背景

::left::

<div class="viewpoint">
观点：zkGPT 证明的是关键输出的计算来源，不证明输出语义安全。
</div>

LLM 服务商可能不愿公开模型参数。

但用户或监管方又想确认：

- 服务商是否真的用了声明的模型
- 输出是否由该模型推理得到
- 服务商有没有为了省成本换成小模型

::right::

### 证明关系

零知识证明（ZKP）让 prover 证明：

<div class="text-center mt-4">

$y = f(x, w)$

</div>

其中：

- $x$ 是输入
- $w$ 是模型参数
- $y$ 是输出
- proof 不泄露 $w$

<div class="small mt-4">

non-interactive 指证明生成后，验证者可以离线验证，不需要多轮交互。

</div>

<!--
zkGPT 的背景很现实。

模型参数是服务商的资产，不能直接给别人看。但用户又想确认：你没有偷偷换模型，也没有改中间结果。

ZKP 做的事情就是：证明 y=f(x,w)，但不把 w 交出去。

注意，它证明的是计算过程，不证明语义。模型胡说八道也可能有一个正确的 proof。
-->

---
layout: default
---

## zkGPT 方法论：四步拆解

zkGPT 的主线可以按四步看：

<div class="takeaway">
先把 Transformer 推理翻译成证明系统能检查的数学关系，再用系统优化把 prover 时间降下来。
</div>

1. **量化**：把 LLM 推理里的浮点数转成有限域上可处理的整数关系
2. **约束化**：把 Transformer layer 拆成矩阵乘法、softmax、GeLU、normalization 等约束
3. **分后端证明**：算术关系用 GKR，非线性关系用 lookup/Lasso
4. **系统优化**：用 constraint fusion 和 circuit squeeze 降低 prover 开销

<div class="mt-7 text-sm">

这四步的目标很明确：不是证明“回答语义正确”，而是证明“这次输出确实来自指定模型的一次推理计算”。

</div>

<!--
这页先别急着看协议名。

zkGPT 要做的事情很朴素：把一次 Transformer 推理，变成证明系统能检查的数学关系。

量化是为了把浮点数变成有限域里的数。

约束化是把每一层计算拆出来。

后面再用不同证明后端处理不同计算，最后做工程优化，不然 prover 太慢。
-->

---
layout: default
---

## zkGPT 方法总览

<img src="/image/AgentLoop/zkgpt_workflow.png" class="w-[52%] mx-auto mt-0" />

<div class="caption">原文图：LLM prover workflow</div>

<div class="mt-4 text-sm">

zkGPT 把 Transformer 推理拆成约束，再用不同后端协议证明不同类型的关系：算术关系走 GKR，非线性相关关系用 lookup/Lasso。简单理解：GKR 处理大批量加法、乘法；lookup/Lasso 用查表方式检查 softmax、GeLU、normalization 这类非线性关系。

</div>

<!--
这张图是 zkGPT 的整体 workflow。

Transformer 先被拆成 layer，再变成 constraint，再落到 circuit 和 backend protocol。

算术关系，比如加法乘法，走 GKR。

softmax、GeLU、normalization 这种非线性操作，用 lookup/Lasso 这类查表思路会便宜一些。

这里不用把协议推一遍。抓住“证明的是计算图”就够了。
-->

---
layout: two-cols-header
---

## zkGPT：主要技术瓶颈

::left::

### 线性层

瓶颈来自大矩阵乘法。

- 权重矩阵大
- bookkeeping table 开销高
- grouping 利用稀疏性和量化范围

<img src="/image/AgentLoop/zkgpt_grouping.png" class="w-[66%] mx-auto mt-2" />

<div class="caption">原文图：grouping algorithm 的直觉</div>

::right::

### 非线性层

LLM 里还有很多 ZKP 不友好的操作：

- division
- square root
- exponentiation
- softmax / GeLU / normalization

zkGPT 的策略不是硬在算术电路里模拟，而是用 advice 和 lookup 降低证明关系数量。

<div class="takeaway">
这页只需要抓住两个瓶颈：矩阵乘法规模大，非线性函数在证明系统里很贵。
</div>

<!--
瓶颈分两类。

线性层主要是大矩阵乘法。矩阵大，bookkeeping table 也大。

非线性层更麻烦，softmax 里的 exp、normalization 里的 sqrt，在 ZKP 里都很贵。

zkGPT 的办法不是硬算到底，而是用 advice 和 lookup 把验证关系变便宜。
-->

---
layout: two-cols-header
---

## zkGPT：效率优化

::left::

### 矩阵乘法优化

- 利用 padding zero 的稀疏性
- 利用量化后取值范围小
- 用 grouping 降低 field multiplication 数量

### 非线性层优化

- 把除法、平方根、指数转为更便宜的 lookup/range 关系
- 避免在算术电路里完整模拟复杂函数

::right::

### 两个系统级优化

**constraint fusion**

把可合并的约束放到一起，减少非线性层证明开销。

**circuit squeeze**

把逐层证明里可并行的部分展开，提高并行度。

<div class="small mt-5">

论文的目标很工程化：不是只给理论复杂度，而是把 GPT-2 推理证明压到 CPU 服务器上可接受的时间。

</div>

<!--
效率优化可以分成两块。

一块是矩阵乘法，利用 padding zero、量化范围这些性质减少工作量。

另一块是非线性层，把除法、平方根、指数换成更便宜的 lookup/range 关系。

再加上 constraint fusion 和 circuit squeeze，才把 GPT-2 的证明时间压到几十秒。
-->

---
layout: default
---

## zkGPT 实验结果

<img src="/image/AgentLoop/zkgpt_tables_3_4.png" class="w-[56%] mx-auto mt-0" />

<div class="caption">原文表 3/4：GPT-2 proof time、proof size 与量化后文本质量</div>

<div class="mt-5 text-sm">

关键读数：fully optimized 32-thread 配置下 prover time 为 21.8s，verifier time 为 0.35s，proof size 为 101K。量化后 PPL 相比 FP32 只小幅变化。

</div>

<!--
这张表是 zkGPT 最重要的结果。

最终 32 线程、所有优化打开的配置下，prover time 是 21.8 秒，verifier time 是 0.35 秒，proof size 是 101K。

表 4 看量化后的文本质量，PPL 只小幅变化。

所以它不是靠把模型质量大幅牺牲掉来换速度。
-->

---
layout: two-cols-header
---

## zkGPT：消融分析

::left::

<img src="/image/AgentLoop/zkgpt_table_5.png" class="w-full mt-5" />

<div class="caption">原文表 5：constraint fusion 与 circuit squeeze 的加速贡献</div>

::right::

表 5 的主要结果：

- 没有 constraint optimization：33.2s
- 没有 circuit optimization：36.5s
- 两者都用：21.8s

这说明性能提升不是单个 trick，而是约束层和电路层共同作用。

<div class="small mt-5">

对组会理解来说，知道“证明系统需要贴着 Transformer 结构优化”就够了，不需要展开每个协议公式。

</div>

<!--
表 5 看优化到底有没有用。

没有 constraint optimization，总时间 33.2 秒。

没有 circuit optimization，总时间 36.5 秒。

两个都用，降到 21.8 秒。

这说明 zkGPT 的速度不是单靠硬件堆出来的，它确实贴着 Transformer 结构做了优化。
-->

---
layout: default
---

## zkGPT 的证明边界

<div class="problem-viewpoint">
观点：zkGPT 让关键输出可验证，但它不是 Agent 安全证明。
</div>

### 证明范围

- 输出确实由承诺模型和给定输入计算得到
- prover 没有在推理计算里偷换某些中间结果
- proof 不公开模型参数
- 验证者可以用较小开销检查 proof

### 非证明范围

- 工具调用真的执行成功
- Agent 的规划决策是安全的
- prompt 没有被注入
- 模型输出语义是真的
- 被证明的推理节点就是整个 Agent Loop 的全部行为

<!--
这页很重要，因为 zkGPT 很容易被误解。

它能证明：这个输出是承诺模型在给定输入上算出来的，中间没有被偷换。

但它不能证明工具执行成功。

也不能证明规划是安全的。

更不能证明输出语义是真的。

有 proof，只能说明模型按承诺算出了这段输出。别把它当成完整的 Agent 安全证明。
-->

---
layout: default
---

## 组合框架：风险路径与推理证明

<div class="problem-viewpoint">
观点：组合后的主线是选择性验证关键输出，而不是证明整个 Agent Loop 完全安全。
</div>

<div class="mt-8 text-center text-xl">

AgentFuzz  
发现 prompt → LLM → parser/tool router → sink 的风险路径

↓

选出关键 LLM 推理节点  
这些节点会决定 tool、argument、code、SQL 或策略分支

↓

zkGPT  
为这些推理节点生成零知识正确性证明

</div>

<div class="takeaway">
组合后的目标不是“证明整个 Agent 安全”，而是让高风险路径上的关键推理有证据可查。
</div>

<!--
现在把两篇论文接起来。

第一步，AgentFuzz 找风险路径。

第二步，从路径里挑出关键 LLM 推理节点。这里的关键节点通常会决定 tool、argument、code、SQL 或策略分支。

第三步，对这些节点加 zkGPT proof。

这样审计时，至少能知道当时关键输出是不是来自承诺模型。
-->

---
layout: two-cols-header
---

## 可验证 Agent Loop 的审计记录

::left::

对每个高风险路径，可以记录：

- `path_id`：AgentFuzz 发现的 source-to-sink 路径
- `input_hash`：进入关键 LLM 节点的 prompt/context hash
- `model_commitment`：被承诺的模型参数 commitment
- `output_hash`：LLM 输出 hash
- `zk_proof`：zkGPT proof
- `tool_call_log`：工具名、参数、返回状态

::right::

### 设计原则

证明只覆盖关键节点，不覆盖所有调用。

日志负责记录工具执行事实，ZK proof 负责证明模型计算事实。

两者要放在一起看：

<div class="mt-4 text-center text-lg">

proof 证明“模型怎么想”  
log 记录“系统怎么做”

</div>

<div class="takeaway">
如果没有 tool log，zkGPT 只能证明模型输出，不能证明工具动作真的发生过。
</div>

<!--
如果真要落地，我会把证据记成这一类结构。

path_id 说明这条路径为什么危险。

input_hash、output_hash 绑定一次具体推理。

model_commitment 绑定模型。

zk_proof 证明模型计算。

tool_call_log 记录工具到底被怎么调了。

这里最重要的是分工：proof 证明模型怎么算，log 记录系统怎么做。
-->

---
layout: two-cols-header
---

## 安全收益与代价

::left::

### 收益

- 高风险路径更可审计
- 关键 LLM 输出不能被服务商随意替换
- proof 可以离线验证，适合事后审计
- AgentFuzz 的结果可以指导“哪里值得加证明”

::right::

### 代价

- 证明仍有成本，不适合给每次普通调用都加
- zkGPT 当前实验聚焦 GPT-2 级别模型
- proof 不覆盖外部工具、数据库、文件系统的真实执行
- AgentFuzz 发现的是已覆盖 sink 和 threat model 下的漏洞

<div class="small mt-5">

所以合理策略是 selective verification：只证明会影响敏感 sink 的推理节点。

</div>

<!--
组合以后，好处是关键路径更容易审计，服务商也不容易随便替换关键输出。

但代价也明显。证明不是免费的，zkGPT 现在实验还是 GPT-2 级别。

AgentFuzz 也受 sink 列表、威胁模型和时间预算限制。

所以更合理的做法不是全量证明，而是只证明高风险节点。
-->

---
layout: default
---

## 组合方案的边界

这条链路能提高“可验证性”，但不能直接等价于“安全”。

<div class="plain-table mt-8">

| 问题 | AgentFuzz | zkGPT |
| --- | --- | --- |
| 恶意 prompt 能不能到达 sink | 能测试 | 不处理 |
| LLM 推理是不是按承诺模型执行 | 不处理 | 能证明 |
| 工具是否真实执行成功 | 不处理 | 不处理 |
| Agent 规划是否安全 | 间接暴露风险 | 不证明 |
| 事后审计是否有证据 | 提供风险路径和 PoC | 提供推理 proof |

</div>

<!--
这张表就是边界。

AgentFuzz 能测恶意 prompt 能不能到 sink，但不证明推理计算。

zkGPT 能证明推理计算，但不处理 prompt injection，也不证明工具执行。

所以组合后更像“可审计 Agent Loop”，不是“完全安全 Agent Loop”。

这个说法要保守一点。
-->

---
layout: default
---

## 未来演进方向

Agent Loop 的安全会继续从“单点防御”走向“链路治理”。

可以沿四个方向推进：

1. **路径发现**：先找出 prompt、observation、memory 会流向哪些敏感操作
2. **选择性证明**：只给会影响 tool、argument、code、SQL 的关键推理加 proof
3. **工具执行验证**：用日志、sandbox、attestation 记录工具是否真的执行
4. **端到端审计**：把路径、proof、tool log 绑定成可复查证据

<div class="mt-6 text-sm">

未来更可能出现的是“可审计 Agent Loop”，而不是一次性证明整个 Agent 完全安全。

</div>

<!--
往后看，我觉得方向不是做一个大而全的证明。

Agent 太复杂了，外部工具、环境状态、日志、权限都在变。

更现实的路是拆开做：先找路径，再证明关键推理，再记录工具执行，最后把这些证据串起来审计。

这也是这两篇论文放在一起最有意思的地方。
-->

---
layout: default
---

## 后续研究建议

如果想继续做 Agent 安全或隐私方向，不要从“大系统”开始。

具体可以按四步做：

1. 先画数据流：source、parser、tool router、sink 分别在哪里
2. 再定威胁模型：攻击者控制 prompt、网页、memory，还是工具返回
3. 再选证明对象：证明模型计算、工具执行，还是策略约束
4. 最后做实验：同时报告安全效果、误报漏报、成本和可用性

<div class="mt-6 text-sm">

一句话：先把链路讲清楚，再谈机制。否则很容易做成“看起来安全，但不知道保护了什么”。

</div>

<!--
如果后面有同学想做 Agent 安全，我建议先别急着起大名字。

先画数据流。source 在哪，parser 在哪，router 在哪，sink 在哪。

再定威胁模型：攻击者能控制 prompt、网页内容、memory，还是工具返回？

最后再选机制。ZK、sandbox、fuzzing、日志都只是工具，先弄清楚自己保护什么。
-->

---
layout: default
---

## 总结

### 系统背景

Agent 正在从“模型输出文本”走向“闭环执行系统”。一旦模型输出会控制工具，安全问题就变成了数据流、证明和审计问题。

### AgentFuzz

用 directed greybox fuzzing 找 Agent 里的 taint-style 漏洞。实验中在 20 个开源 Agent 上发现 34 个 0-day 漏洞，precision 100%，已有 23 个 CVE ID。

### zkGPT

用非交互零知识证明验证 LLM 推理计算。论文在 GPT-2 上报告 25 秒以内的证明时间，最终表中 32-thread all-opt 配置为 21.8s。

### 结论

AgentFuzz 负责发现“哪里危险”，zkGPT 负责证明“关键推理是否按承诺执行”。两者结合能提高 Agent Loop 的可审计性，但不能替代工具执行验证和规划安全分析。

<!--
最后收一下。

第一，Agent 正在从文本回答变成闭环执行系统。只要模型输出能控制工具，安全边界就不只在模型内部。

第二，AgentFuzz 是风险发现工具。它找的是 prompt 到 sink 的路径。

第三，zkGPT 是推理证明工具。它证明关键输出是不是按承诺模型算出来。

两者放在一起，能让 Agent Loop 更可审计。但它还不是完整安全方案。工具执行、规划安全、外部状态，都还要单独处理。
-->

---
layout: default
class: refs-slide
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
