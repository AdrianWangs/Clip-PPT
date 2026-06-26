---
theme: seriph
title: "MemLineage: Lineage-Guided Enforcement for LLM Agent Memory"
info: |
  ## Lineage-Guided Enforcement for LLM Agent Memory
  用来源链路保护 LLM Agent 的长期记忆
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

# MemLineage
## Lineage-Guided Enforcement for LLM Agent Memory

<div class="mt-6 text-sm">

**作者：** Ciyan Ouyang, Rui Hou

**单位：** Institute of Information Engineering, CAS

**版本：** arXiv:2605.14421v1, 2026

</div>

<div class="absolute bottom-8 right-8 text-sm">
主讲人：王宇哲
</div>

<!--
今天讲 MemLineage。它解决的是 LLM Agent 长期记忆里的来源问题。

一句话概括：长期 memory 让 Agent 能跨会话工作，但也让外部内容有机会先写入、再沉淀、最后在未来会话里影响敏感工具调用。MemLineage 的做法不是判断某句话恶不恶意，而是把每条 memory 的来源链路保存下来，并在敏感动作前检查：这个动作到底能不能由这些来源授权。
-->

---
layout: default
---

## 汇报路线

<div class="grid grid-cols-3 gap-7 mt-10">

<div>

<div class="section-tag">Part 1</div>

### 引言与背景

- Agent Memory 是什么
- 为什么需要 memory
- memory poisoning 为什么难防
- 贯穿例子：转账 Agent

</div>

<div>

<div class="section-tag">Part 2</div>

### 方法

- Provenance：证明 entry 没被伪造
- Lineage：保留派生来源
- Gate：阻止不可信来源授权敏感动作

</div>

<div>

<div class="section-tag">Part 3</div>

### 实验

- 三类攻击的 ASR
- $\tau$ 与链长 $K$
- 开销与 utility
- 边界和限制

</div>

</div>

<!--
这次按线性逻辑讲。

第一部分先把背景讲清楚。大家不一定熟悉 Agent Memory，所以先说明它是什么、为什么需要它、为什么它会变成攻击面。

第二部分讲方法。我会把 MemLineage 拆成三件事：先证明 entry 没被伪造，再保留派生来源，最后在工具调用前做 gate。

第三部分讲实验，只看能支持论文主张的结果：ASR、阈值消融、开销和 utility。
-->

---
layout: two-cols-header
---

## Agent Memory 是什么

::left::

Agent Memory 是 Agent 的长期状态。

它通常保存四类内容：

- 用户偏好和长期目标
- 历史任务和中间结论
- 工具返回结果
- Agent 自己总结出的观察

<div class="mt-5 small">

普通 RAG 主要是“查外部知识”。Agent Memory 更像“保存自己的工作状态”，会被后续会话继续使用。

</div>

::right::

<img src="/image/MemLineage/agent-memory-concept.png" class="w-full mt-2" />

<div class="caption">生成图：Agent 在当前任务与长期 memory 之间读写</div>

<!--
先解释 Agent Memory。

它不是简单的聊天记录，也不只是 RAG 的知识库。更准确地说，它是 Agent 的长期状态。Agent 在执行任务时，会把用户偏好、工具结果、任务中间状态、自己的总结写进去。下一次用户再来，它会从 memory 里把相关内容取出来。

这个能力很重要。没有 memory，Agent 每次都像第一次见到用户；有 memory，任务才能跨会话继续。
-->

---
layout: two-cols-header
---

## 为什么需要 memory

::left::

### 没有 memory

- 用户每次都要重复上下文
- 工具结果只在本轮有效
- 多轮任务断开后很难恢复
- Agent 只能做短任务

::right::

### 有 memory

- 记住上次处理到哪里
- 复用工具返回和文档摘要
- 保存用户授权过的偏好
- 支撑财务、邮件、代码修改这类跨会话工作

<div class="mt-6 text-sm">

memory 的作用很实际：减少重复输入，让任务能接着做。

</div>

<!--
为什么需要 memory？因为很多 Agent 任务不是一轮完成的。

例如财务 Agent 处理账单，邮件 Agent 维护联系人，代码 Agent 记住项目规范。如果没有 memory，用户每次都要重新解释背景，工具结果也没法沉淀。

所以 memory 不是让 Agent 看起来更像人，而是让它具备连续工作能力。
-->

---
layout: default
---

## 一个贯穿例子：转账 Agent

<img src="/image/MemLineage/banking-lineage-example.png" class="w-[86%] mx-auto mt-1" />

<!--
下面用一个例子贯穿后面的所有内容。

用户有一张可信账单：收款人 Alice，金额 120 美元。这个来源可以授权转账参数。

同一轮任务里，Agent 还读到一个外部备忘录。备忘录里混入了攻击者的目标：把收款人改成 Mallory。

Agent 把上下文总结成一条新 memory。几天后，用户说“帮我处理上次那张账单”。这条 memory 被召回，模型可能准备调用 send_money。

问题不是这句话看起来恶不恶意，而是 recipient 这个参数到底来自可信账单，还是外部备忘录。
-->

---
layout: default
---

## 为什么这不是普通 prompt injection

普通 prompt injection 的危险在当前上下文里。

memory poisoning 的危险在未来会话里。

<div class="plain-table mt-8">

| 类型 | 攻击出现在哪里 | 防御难点 |
| --- | --- | --- |
| 单轮 prompt injection | 当前 prompt 里有恶意指令 | 本轮检测、隔离、策略控制 |
| memory poisoning | 恶意内容被写入长期 memory | 跨会话保留，之后再被召回 |
| sleeper-via-derivation | 恶意影响被总结成新 memory | 新 entry 有合法签名，但来源不可信 |

</div>

<div class="mt-6 text-sm">

MemLineage 重点处理第三种：污染内容经过 LLM 派生以后，仍然要能追到外部来源。

</div>

<!--
这页区分一下问题。

普通 prompt injection 是当前上下文里有恶意指令，防御可以集中在本轮输入。

memory poisoning 更麻烦，因为恶意内容可以先写入长期 memory。它不一定马上触发，而是在之后的会话里被检索出来。

最难的是 sleeper-via-derivation。攻击者不直接写入最终指令，而是给一段外部材料。LLM 把它总结、改写成新的 memory。新 memory 是 Agent 自己写的，有合法签名，但关键影响来自外部来源。
-->

---
layout: two-cols-header
---

## 现有防御为什么不够

::left::

### 三个常见思路

- 签名：证明 entry 是谁写的
- 过滤：拦截明显恶意文本
- sandbox：粗粒度禁用外部 memory 或高风险能力

::right::

### 在转账例子里的问题

- `e1` 的确是 Agent 写的，签名会通过
- 外部备忘录被总结后，文本不一定显得恶意
- 全禁外部 recall 会让正常账单任务也难做

<div class="mt-6 text-sm">

缺的是一条链：`e1` 虽然由 Agent 写入，但它受哪些父内容影响？

</div>

<!--
签名、过滤、sandbox 都有价值，但都不是完整答案。

签名能说明 entry 没被伪造。问题是 `e1` 本来就是 Agent 写的，所以签名不会拦它。

过滤能处理明显恶意文本。但如果 Mallory 这个参数经过总结变成普通提醒，过滤器很难稳定判断。

粗粒度 sandbox 能安全，但会牺牲可用性。用户问“上次那张账单”，系统如果完全不召回历史内容，任务就做不下去。

因此需要保留派生来源，而不是只看当前文本。
-->

---
layout: default
---

## 论文目标

MemLineage 要让长期 memory 满足三件事：

1. 伪造 entry 进不来。
2. 不可信来源经过总结、改写以后，标签还在。
3. 敏感工具调用不能由不可信来源授权。

<div class="mt-10 text-xl">

它不试图判断“这段文本是不是恶意”。它判断“这段文本的来源能不能授权当前动作”。

</div>

<!--
这里给出论文目标。

第一，伪造 entry 要进不来，所以需要签名和日志。

第二，外部来源经过总结、改写以后，来源标签不能丢。

第三，敏感工具调用前要看来源。外部备忘录可以帮助回答非敏感问题，但不能授权转账收款人。

这就是 MemLineage 和很多输入过滤方案的区别。
-->

---
layout: center
---

# 方法

---
layout: default
---

## 方法总览：三件事连起来做

<img src="/image/MemLineage/method-three-parts.png" class="w-[92%] mx-auto" />

<!--
方法部分拆成三件事。

第一，provenance。每条 memory 都有 metadata、签名和 Merkle log，保证 entry 身份和历史可审计。

第二，lineage。每条新 memory 都记录它从哪些父 memory 派生出来，边上有权重，表示影响强度。

第三，gate。检索时把标签带回上下文，敏感工具调用前检查参数来源。

这三件事必须连起来。只有签名没有 lineage，解决不了 `e1` 这种 Agent 自己写出的污染摘要。只有 lineage 没有 gate，也只是记录风险，不会阻止工具调用。
-->

---
layout: two-cols-header
---

## 方法一：Provenance 先保证 entry 身份

::left::

每条 memory entry 包含：

- `eid`：entry id
- `content`：内容
- `writer`：写入主体
- `h_src`：原始数据 hash
- `h_ctx`：写入时上下文 hash
- `parents`：父 entry 列表
- `trust`：信任标签
- `signature`：Ed25519 签名

::right::

### 这一步解决什么

- 没有注册密钥，不能伪造合法 entry
- Merkle log 让历史可审计
- 删除只留下 tombstone，不能静默改写

<div class="mt-6 text-sm">

但它只回答“谁写的”。`e1` 是 Agent 写的，不代表 `e1` 的参数来源可信。

</div>

<!--
第一步是 provenance。

每条 memory 都有 writer、source hash、context hash、parents、trust 等字段，并用 writer 的 Ed25519 key 签名。entry hash 再进入 Merkle log。

这保证伪造 entry 很难通过验证，也保证历史不能被悄悄重写。

但是这一步只回答“谁写的”。在账单例子里，`e1` 的 writer 是 Agent，这是真的。问题是 `e1` 的 recipient 受外部备忘录影响。所以还需要 lineage。
-->

---
layout: two-cols-header
---

## 方法二：Lineage 记录派生来源

::left::

Memory store 被表示成一个有向无环图：

$$
G=(V,E)
$$

- 节点：memory entry
- 边：父 entry 影响子 entry
- 边权：$w(p,c)\in[0,1]$
- 阈值：$\tau$

账单例子里，可信账单和外部备忘录都是 `e1` 的父节点。

::right::

传播规则：

$$
\mathrm{trust}(c)=
\max_{p:\,w(p,c)>\tau}\mathrm{trust}(p)
$$

trust 数值越大越不安全：

- Trusted
- Derived-Trusted
- Derived-Untrusted
- External

<div class="mt-4 small">

如果外部备忘录到 `e1` 的边足够强，External 标签会传播到 `e1`。

</div>

<!--
第二步是 lineage。

每条 memory 是一个节点。如果某个父 entry 出现在写入子 entry 的上下文里，就形成一条边。边权表示父节点对新 entry 的影响程度。

传播规则很简单：只看强边，也就是 $w>\tau$ 的边；在这些父节点里取最不安全的标签。

所以如果外部备忘录对 `e1` 的影响足够强，`e1` 就不能被当成普通 Trusted memory。
-->

---
layout: two-cols-header
---

## attribution：边权从哪里来

::left::

论文讨论三种做法：

**Coarse**

只要父 entry 出现在上下文，就设 $w=1$。

**LM-self-eval**

用二级 LLM judge 判断父 entry 对子 entry 的影响。

**Attention**

用白盒模型的 attention 读数估计影响。

::right::

### 需要注意的点

- Coarse 保守，不容易漏掉风险边
- LM-self-eval 更细，但 judge 也要防 prompt injection
- Attention 需要开放权重，生产 API 不一定可用
- $\tau$ 不是越大越安全：太大反而会断链

<div class="mt-5 text-sm">

安全性依赖 attribution 没漏掉关键边。这个点在实验的 $\tau \times K$ 消融里会体现。

</div>

<!--
边权可以用不同算法给。

Coarse 最保守，只要父 entry 在上下文里，就认为它可能影响了新 memory。它会多标一些无关父节点，但不容易漏掉攻击链。

LM-self-eval 让另一个模型判断影响程度，精度更高，但 judge 自己也可能被 prompt injection，所以论文讨论了 JSON envelope 等硬化手段。

Attention 需要白盒模型，闭源 API 通常拿不到。

这里要特别注意，$\tau$ 不是越大越安全。因为只有 $w>\tau$ 才传播，阈值太大反而会让风险边断掉。
-->

---
layout: two-cols-header
---

## 方法三：Gate 检查敏感动作

::left::

<img src="/image/MemLineage/lineage-gate-concept.png" class="w-full mt-1" />

<div class="caption">生成图：来源链路进入 gate，只有授权路径能触发工具</div>

::right::

M6 gate 不是文本分类器。

它检查：

- 当前工具是否敏感
- 参数引用了哪些 memory
- 这些 memory 的来源标签是什么
- 该来源能否授权该参数

例子：`send_money.recipient` 必须来自可信账单或当前用户请求，不能来自外部备忘录。

<!--
第三步是 gate。

M6 gate 不需要判断一句话是不是恶意。它只看敏感工具调用的参数来源。

比如 `send_money.recipient` 这个参数，应该来自可信账单或用户当前请求。如果 Mallory 只来自外部备忘录，gate 就拒绝。若系统同时有可信账单里的 Alice，可以走 repair-and-retry，只替换这个参数，而不是让整个任务失败。
-->

---
layout: default
---

## 三部分合起来挡住什么

<div class="plain-table mt-6">

| 攻击路径 | 只签名 | MemLineage |
| --- | --- | --- |
| 攻击者伪造 entry | 能挡住 | 能挡住 |
| 污染内容通过合法路径写入 | 挡不住来源污染 | lineage 记录父来源 |
| LLM 总结出新 memory | 只看到 Agent 签名 | External 标签沿强边传播 |
| 后续触发 `send_money` | 可能执行 | gate 拒绝或修复未授权参数 |

</div>

<div class="mt-8 text-lg">

核心链路：entry 可验证，来源可追踪，动作要授权。

</div>

<!--
这页把方法合起来看。

如果攻击者伪造 entry，签名层已经能挡住。

真正困难的是后面三种：污染内容通过合法路径进入；LLM 总结出新 memory；未来会话里触发敏感工具。只签名会看到“Agent 写的合法 entry”，但 MemLineage 会继续看它的父来源。

最后 gate 判断参数是否授权。外部来源可以被召回用于非敏感问答，但不能授权转账参数。
-->

---
layout: center
---

# 实验

---
layout: two-cols-header
---

## 实验设置：三类攻击，三类防御

::left::

### 攻击

- Poison raw：伪造/外部写入触发词后门
- Graft forged：污染经验走合法写入路径
- Sleeper derived：外部内容被 LLM 派生为新 memory

### 防御

- no defense
- signature-only baseline
- MemLineage

::right::

### 评价指标

ASR：Attack Success Rate，越低越好。

论文还评估：

- $\tau \times K$ 消融
- 每操作 latency
- benign workflow 的 utility
- AgentDojo 上的 recovery

<!--
实验先看 headline。

攻击有三类，对应我们前面讲的威胁路径：原始投毒、合法路径污染、派生后 sleeper。

防御有三类：不防御、只签名、MemLineage。

主要指标是 ASR，越低越好。后面再看阈值、性能和 utility。
-->

---
layout: two-cols-header
---

## RQ1：ASR 结果

::left::

<img src="/image/MemLineage/x3.png" class="w-[92%] mx-auto" />

<div class="caption">论文原图：deterministic harness 上的 ASR matrix</div>

::right::

### 读法

- no defense：三类攻击都成功
- sig-only：能挡 raw poison，但挡不住 graft 和 sleeper
- MemLineage：三列 ASR 都是 0

<div class="mt-6 text-sm">

最重要的是 sleeper-derived：它证明只看 writer 不够，必须看派生来源。

</div>

<!--
这张图是最重要的结果。

no defense 三列都是 1，说明三类攻击都成功。

signature-only baseline 能挡住 raw poison，因为伪造 entry 没有合法签名。但它挡不住 Graft 和 Sleeper，因为这两类攻击可以让污染内容走合法写入路径，甚至由 Agent 自己写出新 memory。

MemLineage 三列都是 0。它挡住后两列靠的不是更强的文本过滤，而是 lineage propagation 加 sensitive-action gate。
-->

---
layout: two-cols-header
---

## RQ2：阈值 $\tau$ 与链长 $K$

::left::

<img src="/image/MemLineage/x6.png" class="w-full mt-3" />

<div class="caption">论文原图：τ × K 消融。绿色表示 External 标签传播到链尾</div>

::right::

### 结论

- Coarse：只要 $\tau<1$，链路都能传播
- LM-self-eval：边权会随派生深度衰减
- 链越长，安全的 $\tau$ 上限越低
- $\tau$ 过高会断链，不是更安全

例子：$w_0=0.9,d=0.7$ 时，$K=5$ 的最深边约为 $0.216$，所以 $\tau=0.30$ 会丢链。

<!--
这页回答一个重要问题：阈值怎么设。

传播规则是 $w>\tau$ 才传播，所以 $\tau$ 太大反而会让真实风险边断掉。

Coarse 的边权固定为 1，所以只要 $\tau<1$ 都传播。LM-self-eval 更真实，边权会随着派生链变长而衰减。

因此不能只看一步派生来设阈值。如果部署允许更长的派生链，阈值要更保守。
-->

---
layout: two-cols-header
---

## RQ3/RQ4：开销和 utility

::left::

### 性能开销

论文报告单核 median latency：

- `ed25519_sign`：27.5 μs
- `ed25519_verify`：80.8 μs
- `propagate_trust`：1.0 μs
- `policy_gate_call`：0.7 μs
- 8 entries 的 filter + tag：717.8 μs

<div class="mt-4 text-sm">

这些开销低于一次 LLM 调用的噪声量级。

</div>

::right::

### Utility

benign workflows 都保持 1.00：

- benign direct
- benign derived
- external QA
- external derived QA

<img src="/image/MemLineage/x7.png" class="w-full mt-4" />

<div class="caption">论文原图：参数级 authority 比粗粒度 taint 保留更多 utility</div>

<!--
性能上，MemLineage 的成本主要来自签名验证。lineage 传播和 gate 本身都是微秒级。

论文把这个开销和 LLM 调用比较。一次 LLM API 调用通常是百毫秒到秒级，所以这些 provenance 操作不在关键瓶颈上。

Utility 上，论文的 benign workflows 都保持 1.00。右图说明参数级 authority 的意义：不是看到外部内容就全拒绝，而是检查敏感参数是否由可信来源授权。
-->

---
layout: two-cols-header
---

## RQ5：更接近真实 Agent 的验证

::left::

### Two-session RAG-to-memory

- Session 1：外部文档被总结进 memory
- Session 2：只召回 summary
- sig-only 把 summary 当成 Trusted
- MemLineage 保留 External 父边并阻止工具调用

### AgentDojo

在 banking DirectAttack 上，authority repair 兼顾攻击阻断和任务恢复。

::right::

<img src="/image/MemLineage/x5.png" class="w-full mt-2" />

<div class="caption">论文原图：AgentDojo gate sweep</div>

<!--
除了 deterministic harness，论文还做了更接近真实 Agent 的验证。

Two-session RAG-to-memory 很贴近我们前面的例子：第一轮外部文档被总结进 memory，第二轮只召回 summary。sig-only 会把 summary 当成可信，因为 writer 是合法的；MemLineage 能保留外部父边。

AgentDojo 部分主要看 recovery。deny 能保安全，但可能损失任务成功率。authority repair 在有可信参数来源时，可以修复攻击者控制的参数。
-->

---
layout: default
---

## 该怎么看实验结论

论文的实验证明三点：

1. 签名层有用，但只能解决伪造 entry。
2. sleeper-derived 这类攻击需要 lineage 才能挡住。
3. gate 做到参数级 authority，比粗粒度禁用 memory 更可用。

<div class="mt-8 text-lg">

实验不是在证明“模型不会被诱导”。它证明的是：当污染链路能被记录下来时，防御层可以阻止它授权敏感动作。

</div>

<!--
实验要这样读。

第一，签名不是没用，它能挡 raw poison。但它不能处理 Agent 自己写出的污染派生。

第二，sleeper-derived 是论文的关键分界线。只有 lineage 能把外部来源一路带到链尾。

第三，gate 的粒度很重要。如果只是粗粒度 taint，系统会安全但难用。参数级 authority 能在安全和 utility 之间更精细地处理。
-->

---
layout: default
---

## 限制

**推理模型本身被假设可信。** 如果模型权重或推理服务被后门污染，memory 层不能单独解决。

**安全性依赖 attribution recall。** 关键边如果没被打成强边，标签传播会断。

**no-strong-parent 默认偏 permissive。** 没有强父边时论文默认 Trusted，严格模式可以改成 fail-closed，但会带来误拒。

**adaptive attack 还没完整统计评估。** 论文只给了机制级边界和 strict-mode 缓解。

<!--
限制需要明确说。

第一，论文假设模型推理路径可信。模型本身被污染不是 MemLineage 能单独解决的问题。

第二，安全性依赖 attribution。只要关键边被识别为强边，定理就成立；但如果漏边，链路就断。

第三，没有强父边时默认 Trusted，这是为了减少误拒，但也会有 fail-open 风险。

第四，adaptive attack 还不是完整统计实验。论文做了机制边界，但大规模自适应 payload sweep 仍是未来工作。
-->

---
layout: default
---

## 结论

MemLineage 的位置很清楚：

它不是新的恶意文本检测器。

它是 memory 层的来源链路机制。

<div class="mt-8">

一条 memory 要经过三次检查：

1. **身份**：谁写的，是否可验证。
2. **来源**：从哪些父内容派生。
3. **授权**：这些来源能不能支持当前敏感动作。

</div>

<div class="mt-8 text-lg">

Agent 越依赖长期 memory，越需要这种跨会话、跨派生的来源追踪。

</div>

<!--
最后总结。

MemLineage 不是检测恶意文本，而是给 memory 建来源链路。

它把问题拆成三层：身份、来源、授权。身份靠签名和日志，来源靠 lineage DAG，授权靠 sensitive-action gate。

我的判断是：Agent 越依赖长期 memory，这类机制越重要。因为未来的风险不一定出现在当前 prompt 里，而可能来自几天前写入、几轮派生后的 memory。
-->

---
layout: end
---

# 谢谢

## 欢迎提问与讨论

<div class="mt-8 text-left mx-auto w-[72%] text-sm">

**要点**

- Agent Memory 是长期状态，不只是聊天记录
- 只签名不够，因为污染摘要可以由 Agent 自己写入
- MemLineage 用 provenance + lineage + gate 控制敏感动作
- 关键风险在 attribution 漏边和 adaptive attack

</div>

<!--
收束一下。

第一，Agent Memory 是长期状态，会影响未来工具调用。

第二，只签名不够，因为 Agent 自己写出的 memory 也可能受到外部内容影响。

第三，MemLineage 的做法是把来源链路保留下来，在敏感动作前检查是否有授权来源。

第四，后续真正要继续研究的是 attribution 的可靠性和自适应攻击。

QA 预案：
- Q: 会不会禁用所有外部内容？
  A: 不会。外部内容可以用于非敏感问答，但不能授权敏感参数。
- Q: 为什么不直接做文本过滤？
  A: 因为攻击影响可能经过总结和改写，文本不一定保留明显恶意形式。
- Q: 最大风险是什么？
  A: attribution 漏边。如果关键父边没有超过阈值，来源标签会断。
-->
