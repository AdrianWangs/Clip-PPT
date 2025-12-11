# Project Context

## Purpose

本项目是一个**学术论文演示幻灯片**集合，使用 Slidev 框架创建高质量的学术报告 PPT。主要用于在学术会议、组会等场合进行论文内容的汇报与讲解。研究领域集中在：

- 隐私保护检索（Privacy-Preserving Retrieval）
- 可搜索加密（Searchable Encryption）
- 跨模态检索（Cross-Modal Retrieval）
- CLIP 嵌入与语义搜索

## Tech Stack

- **Slidev** `v51.x` - 核心 PPT 框架，基于 Markdown 的现代幻灯片工具
- **Vue 3** - 用于自定义组件和交互
- **KaTeX** - 数学公式渲染
- **Shiki** - 代码高亮
- **主题**: `@slidev/theme-seriph`（主要）、`slidev-theme-academic` 等

## Project Conventions

### PPT 编写规范

#### 文件结构
每个 PPT 是一个独立的 Markdown 文件（如 `VCSE-HST.md`），包含完整的 frontmatter 配置和所有幻灯片内容。

#### Frontmatter 模板
```yaml
---
theme: seriph
background: /image/slides/image.png
title: 'English Title'
info: |
  ## 中文副标题
  简短描述
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
```

#### 标题页规范
```markdown
# English Paper Title

## 中文翻译标题

<div class="pt-12">
  <span class="px-2 py-1 font-semibold">汇报人: 王宇哲</span>
</div>

<div class="pt-6 text-sm">
  Author Name (Institution, Year)
  <br>
  Journal/Conference Name
</div>
```

### 内容风格规范

#### 禁止事项（严格遵守）

1. **禁止使用小标题堆砌**
   - ❌ 错误：`### 1.1 概述 → ### 1.2 定义 → ### 1.3 算法`
   - ✅ 正确：使用叙事性段落自然过渡

2. **禁止在标题中说明技术实现**
   - ❌ 错误：`基于双线性对的分数验证方案`
   - ✅ 正确：`分数正确性验证`

3. **禁止生造技术词汇**
   - ❌ 错误：发明一些看起来很高深但实际意义不明的术语
   - ✅ 正确：使用领域内已有的、被广泛认可的术语

4. **禁止随意定义概念**
   - ❌ 错误：`定义 1.2：语义球面聚类是指...`
   - ✅ 正确：自然引入概念，用通俗语言解释其含义和作用

5. **禁止内容超出屏幕范围**
   - 每页内容控制在合理长度
   - 复杂内容分多页展示
   - 善用 `two-cols-header` 布局分配空间

#### 推荐做法

1. **叙事性表达**
   - 像讲故事一样展开技术内容
   - 先说"为什么需要"，再说"是什么"，最后说"怎么做到的"

2. **演讲备注（必须）**
   - 每页结尾添加 `<!-- ... -->` 备注
   - 备注内容应详细、口语化，方便汇报时使用
   - 备注应包含：此页要点、过渡语、补充解释

3. **公式与代码**
   - 使用 KaTeX 语法：`$...$` 行内，`$$...$$` 块级
   - 复杂公式配文字解释，不要让公式孤立存在

4. **图表使用**
   - 图片放在 `figures/` 或 `image/` 目录
   - 必须添加图注：`<div class="text-center text-xs text-gray-500 mt-1">图X：描述</div>`

### 布局使用指南

```markdown
# 常用布局

---
layout: two-cols-header    # 双列带标题，最常用
---

---
layout: default            # 单列标准布局
---

---
layout: center             # 居中布局，用于重点强调
---

---
layout: end                # 结束页
---
```

### 文件命名

- PPT 文件：`论文简称.md`（如 `VCSE-HST.md`、`Miao-RKS-2022.md`）
- 图片文件：`描述性名称.png`（如 `system_model.png`、`merkle_beam_verification.png`）
- 归档文件存放于 `PPT列表/归档/`

## Domain Context

### 核心领域知识

1. **可搜索加密 (Searchable Encryption, SE)**
   - 允许用户在加密数据上执行搜索操作
   - 保护数据隐私同时保持可用性

2. **CLIP (Contrastive Language-Image Pre-training)**
   - OpenAI 的跨模态预训练模型
   - 将图像和文本映射到统一的 512 维语义空间
   - 使用余弦相似度衡量语义相关性

3. **ASPE (Asymmetric Scalar-Product-Preserving Encryption)**
   - 一种内积保持加密方案
   - 加密后向量的内积等于原始向量的内积
   - 常用于隐私保护相似度计算

4. **系统模型**
   - **数据所有者 (DO)**：生成密钥、构建加密索引、上传数据
   - **数据用户 (DU)**：生成查询、验证结果
   - **云服务器 (CS)**：存储密文、执行搜索（通常假设半诚实）

### 常见技术术语中英对照

| 中文 | 英文 |
|------|------|
| 陷阱门 | Trapdoor |
| 倒排索引 | Inverted Index |
| 球面聚类 | Spherical Clustering |
| 束搜索 | Beam Search |
| 前向安全 | Forward Security |
| 分数验证 | Score Verification |
| 完整性验证 | Integrity Verification |

## Important Constraints

1. **语言要求**：PPT 正文使用中文，保留英文原标题
2. **排版约束**：所有内容必须在屏幕内完整显示，禁止滚动
3. **学术规范**：引用论文时需注明作者、年份和出处
4. **风格一致性**：新 PPT 必须与现有 PPT 保持统一风格

## External Dependencies

1. **Slidev CLI** - `pnpm dev` 启动本地预览，`pnpm build` 构建静态页面
2. **图片资源**
   - 本地图片存放于 `figures/` 或 `image/` 目录
   - 支持外部图片 URL（需确保可访问性）
3. **部署平台** - Netlify / Vercel（参见 `netlify.toml` 和 `vercel.json`）
