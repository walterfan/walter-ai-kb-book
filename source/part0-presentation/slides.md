---
title: "Part 0 — Slides 大纲"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: partial
keywords:
  - presentation
  - slides
---

# Slides 大纲

```{admonition} 使用方式
:class: tip

本文件是 *每页一张 slide 的大纲* —— 每一个 `##` 对应一张 slide。

- **bullet** 是片上文字（精简，不超过 5 行；每行不超过 10 个字为原则）。
- **引用块** `>` 是 speaker notes（讲稿备注），不上屏。
- 可以直接用 [slidev](https://sli.dev/) 渲染；或复制到 Keynote / Google Slides
  的 Outline 视图一次性导入。

一共 **25 张 slide** 左右（大约 1 张 / 2 分钟 + demo 时段的 3 张）。
排练时如果某张停留超 3 分钟，说明那张内容太多，需要拆或砍。

**术语约定**：书里"没有贴切中文翻译"的概念一律用英文原词 ——
`Prose / Code / Dual Stack / frontmatter / footer / tuple / retrieval / embedding /
graph / RRF / MCP / agent / commit-not-pages / L-git / L-entity / L-link`。
不是懒，是这些词的精确性比中文代替词更有价值。
```

---

## Slide 1 —— 标题页

- 用 AI 给软件项目造一个知识库
- 60 分钟部门分享
- Walter (Yamin) Fan

> 开场不要急着讲话。让标题停 10 秒。报家门 1 句。
> 承诺："我今天只走主线，不陷细节；留 10 分钟给大家 Q&A。"

---

## Slide 2 —— 周二下午 2 点

- 新同事入职 6 周
- PR 里问： *"`runSync` 是在哪儿被调用的？"*
- `grep` 返回 **37 个命中**

> 这是整本书第 8 章的开场。停顿 3 秒。
> 不要马上给答案——让听众心里先有一个"这场景我熟"的共鸣。
> 强调一下：新同事问的不是"怎么用"，是"这段代码被谁用"。这类问题恰恰是
> wiki 永远写不完、grep 永远吵、LLM 永远编的那一类。

---

## Slide 3 —— 三种错误的"解法"

- `grep -r runSync` → 37 个噪音命中
- "去问某某人" → tribal knowledge
- 把整个 repo 丢给 ChatGPT → 编造 + 无引用

> 问全场："在座有多少人做过第 3 种？" 等 3 秒。气氛出来了再继续。
> 把第 3 种点穿：不是"上下文不够大"的问题，是**没有可验证来源**的问题。
> 就算 context window 再大十倍，没有 citation 仍然只是 plausible bullshit。

---

## Slide 4 —— Thesis（本讲的论点）

- 软件知识 = **Prose** + **Code**
- Prose：人写好 / LLM 写不好 / 会漂移
- Code：机器查得准 / 人记不住
- KB 必须**同时**处理两者，并让它们**互相指**

> 全场的主论点。一字一字念，不要快。
> "互相指" 这三个字是重点 —— 它是 L0-L4 层、file:line citation、
> publish gate 的共同源头：prose 必须能指一段 code，code 必须能被 prose 解释。
> 一个只处理 prose 的系统叫"文档"，一个只处理 code 的系统叫"搜索"，
> 两头都处理而且互相指的系统才是 **KB**。

---

## Slide 5 —— 地图：六个 Part

- Part I **Foundations** — 词汇
- Part II **Prose Layer** — 文件型 wiki
- Part III **Code Layer** — parse → embed → graph → retrieve
- Part IV **Ops & Lifecycle** — 不让它腐烂
- Part V **Hybrid Layer** — L0-L4 / agent / MCP
- Part VI **Governance & Outlook** — 成本 / 隐私 / 安全

> **停 30 秒不讲话**，让地图进脑子。
> 然后说："接下来 50 分钟只走主线，不讲任何细节。"
> 顺带点一句："Part I–II 是背景，III–IV 是系统，V–VI 是治理。
> 很多团队的 KB 在 Part IV 那里死掉 —— 能建不能维护。"

---

## Slide 6 —— 今天的主线（6 条）

1.  frontmatter + footer（Ch 5）
2.  Code ≠ Prose（Ch 8）
3.  L0-L4 tuple（Ch 18）
4.  Hybrid retrieval + RRF（Ch 12）
5.  三级更新策略（Ch 16）
6.  commit-not-pages 预算（Ch 22）

> 这 6 条是整本书里**最值钱**的东西。
> 每一条只讲 3-4 分钟。Demo 之前，一共 22 分钟。
> 如果现场想补一页"研究脉络"，就用三句话带过：
> *Zhu et al.* = LLM 更适合 reasoning than extraction；
> *RepoAgent* = repo 文档是 "结构分析 → 生成 → 更新" 的流水线；
> *CGM* = 图应该进入 repo-level 理解，而不只是待在索引旁边。

---

## Slide 7 —— 概念 1：Footer 的那条铁律

```yaml
layer:         L2
updated_by:    ai              # ← 这行
review_status: pending         # ← 和这行决定一切
review_score:  0
commit:        a1b2c3d
```

- **AI 写的页面，`review_status` 永远 `pending`**
- 人看过、打分，才 `approved`

> 一条铁律。重复两遍。
> "写得便宜" 和 "可信任" 必须**解耦**。
> 别小看 `pending` 这四个字母 —— 它是检索排序、publish gate、agent
> 引用决策共用的**最小可验证单位**。没有它，KB 和"一个拼写更好的
> markdown 文件夹"没区别。

---

## Slide 8 —— 概念 2：Code 不是 Prose

- Claim 1：有**结构**（名字 / 签名 / 调用图）
- Claim 2：需要**精确匹配**的逃生口
- Claim 3：有 embedding 抓不住的**关系**

> Chunking 把 Java method 切三份 → 三个向量空间区域。
> 用户问 "entityID" 时要的是名叫 entityID 的函数，不是 "entity" 和 "ID" 的语义邻居。
> 两个签名相同但分别住在 HTTP handler 层和后台 worker 层的函数，
> 在向量里挨得很近 —— 但它们的语义天差地别。
> 这三条都不是性能问题，是**语义类型错误**：把关系当相似度看。

---

## Slide 9 —— Dual Stack（对偶栈）

```{mermaid}
flowchart LR
    A[Git] --> B[Parser]
    B --> C[Entity + stable ID]
    C --> D[Embeddings]
    C --> E[Graph]
    D --> F[Hybrid retriever]
    E --> F
    F --> G[Prompt + gen]
```

- Entity ID = `sha256(...)[:16]`
- Embed **identity**（5 行）而不是 body
- 8 条 edge，加第 9 条需要 design review

> 最想强调的是 stable ID —— 它让增量同步敢做 delete-then-insert。
> 另一个反直觉点：**为什么只 embed 那 5 行 identity 而不是 body？**
> 因为用户输入的是"意图"，不是"实现"；identity 是离意图最近的那一面，
> body 是离意图最远的那一面。Ch 10 实测 recall@10 差不多翻一倍。

---

## Slide 10 —— 概念 3：单轴不够

| Tier | 谁写 |
|:--:|:--|
| L0 | 代码 |
| L1 | 人，已提交 |
| L2 | 人，协作 |
| L3 | AI，已审 |
| L4 | AI，未审 |

> 博客原版这样分。用了一段时间发现它**把两件事混在一起**了：
> "谁写的" 和 "审过没"。这两件事的漂移速度完全不同，不能共用一个 tier。

---

## Slide 11 —— tuple ⟨L, U, R, S⟩

- $L$ layer
- $U$ updated_by（human / ai / ai+human）
- $R$ review_status（pending / approved）
- $S$ review_score（0-5）

> retrieval 要的是 **四个** 数字，不是一个。
> "L1 + human + approved + 4" 和 "L1 + ai + pending + 0" 的差别是"救命"级的。
> 别把这 4 个字段当"元数据"—— 它们是**做决策用的参数**：
> 检索加权、agent 过滤、publish gate，都读这四个数字。

---

## Slide 12 —— tuple 的 retrieval 权重

| 页面 | tuple | 权重 |
|:--|:--|:--:|
| 人写 ADR，已审 | ⟨L1, human, approved, 4⟩ | **1.0** |
| LLM 重写 ADR，待审 | ⟨L1, ai, pending, 0⟩ | **0.3** |
| LLM 草稿，人审 | ⟨L3, ai+human, approved, 4⟩ | **0.8** |
| LLM 草稿，没审 | ⟨L3, ai, pending, 0⟩ | **0.2** |

> 同是 L1，权重差 3 倍 —— 这就是 tuple 的价值。
> 最反直觉的一行：**LLM 草稿人审过（0.8）> LLM 重写 ADR 没审（0.3）**。
> 权威来自"谁签了字"，不是"谁写的第一稿"。

---

## Slide 13 —— 概念 4：Hybrid Retrieval

1.  **Vector** → 主路（语义接近）
2.  **Keyword / BM25** → fallback（identifier）
3.  **Graph expansion** → 补充（calls / implements）

> 三种检索**回答三种不同的问题**，不是三种速度。
> 用户问 "entityID" 时要的是名叫 entityID 的函数，不是 "entity" 和 "ID"
> 的语义邻居。一个只有 vector 的 retriever 在 identifier-heavy query 上
> 会被 15 年前的 BM25 吊打，这不是吓唬 —— CodeSearchNet 当年就测过。

---

## Slide 14 —— RRF：一行公式值连城

$$
\text{rrf}(d) = \sum_i \frac{1}{k + \text{rank}_i(d)}
$$

- 只看 **rank**，不看 score
- 加权平均分 = **迷信**

> 为什么分数融合是迷信？因为 cosine、BM25、graph-hop 的分数
> **不在同一个量纲上**。同一个文档在 retriever A 拿 0.82、在 B 拿 14.7，
> 加权平均是把两个不同单位的数字强行相加，没有物理意义。
> RRF 把问题降到"排名"这个**跨 retriever 不变量**上 —— 这才是可加的。

---

## Slide 15 —— 概念 5：三级更新

| 级 | 谁做 | LLM 成本 |
|:--:|:--|:--:|
| **L1** | 脚本 | **0 token** |
| **L2** | LLM + 5k context | 有界 |
| **L3** | 人 + LLM 辅助 | 变量 |

- **Rule first, LLM second**
- AI 所有改动 → `pending`

> L1 覆盖 footer commit 字段更新、死链修复、re-stamp。
> L2 是段落级改写、引用对齐。
> L3 是架构变更、废弃工作流、冲突合并。
> 一句话记住：**"能脚本就别叫 LLM，能 LLM 就别叫人"**。
> 顺序反了，成本直接翻一个数量级，而且审阅者会先弃权。

---

## Slide 16 —— 概念 6：commit-not-pages

> KB 的 LLM 成本应该是 **提交次数** 的可预测函数，
> **不**是 **页面数** 的函数。

- Naive：$N_\text{cand} \times 15k$ token
- 三级：$N_\text{L1}\cdot 0 + N_\text{L2}\cdot 5k + N_\text{L3}\cdot 0$

> 这是今天**最想大家记住的一句工程纪律**。慢一点、重一点。
> 它的反面是一条漂亮的死路："KB 越有用越大 → 每次 commit 越贵 →
> 预算爆掉 → 停止维护"。commit-not-pages 就是把这条曲线**从 O(KB size)
> 拽回 O(change rate)**。

---

## Slide 17 —— 数字落地

- 一周 19 candidates：12 → L1，5 → L2，2 → L3
- L2 调用 ≈ 3k token × 5 = 15k token
- **每 repo 每周几美分**
- Naive baseline：**贵十倍以上**

> "贵十倍以上" 这个数字不是在讲节省美金 ——
> 真正贵的是**评审者的注意力**，不是 token。
> 400 文件 PR 没人看；20 页有人看：省的是人，不是钱。

---

## Slide 18 —— Demo 1：增量同步

```bash
code-kg sync --incremental
# L-git:    1 file
# L-entity: 1 entity moved
# L-link:   no broken links
# vector:   2.1 s
# keyword:  0.4 s
# graph:    20 s
```

| 场景 | Full | Incremental | 加速 |
|:--|--:|--:|--:|
| keyword | ~3 min | ~5 s | **36×** |
| vector | ~3 min | <1 s | **180×** |
| graph | ~3 min | ~20 s | **9×** |

> 这不是"向量很快"，是 **stable ID + 三层过滤 (L-git / L-entity / L-link)**
> 把 99 % 的工作挡在了增量处理之外。
> 记住这张表的**形状**：180× 来自向量不需要重算；9× 来自图必须重写最小子图；
> 36× 是两者之间的地板。

---

## Slide 19 —— Demo 2：Agent + MCP 三工具

| 工具 | 作用 |
|:--|:--|
| `kb.search(q, k, filter)` | 按 tuple 过滤的语义搜 |
| `kb.read(page_id)` | 返回 body + **footer** |
| `kb.cite(q, k)` | 返回 `file:line` 锚点 |

> 开 IDE 实演。指着 MCP 调用日志。
> 强调 `kb.read` 带 footer —— agent 自己看 `review_status` 决定要不要引用。
> 真正革命性的一件事不是 "agent 会调 API"，是 **agent 开始读 footer** ——
> 它第一次拿到了"要不要相信这一页"的机器可读信号。

---

## Slide 20 —— Agent round-trip

```text
/ask "ingest pipeline 是怎么处理 CSV 的?"
  → kb.search(filter="review_status==approved")
  → kb.read("ch06")
  → 回答 + 引用 ch06 §3

追问 "具体是哪个文件？"
  → kb.cite(q="CSV parsing")
  → 返回 internal/pipeline/csv_loader.go:42
```

> 两次问题之间，agent **不再**靠记忆 —— 每次都回 KB 拿 `file:line`。
> 这一条就足以把 "AI 助手" 从 "巧舌如簧的文案机" 变成 "可追责的工程伙伴"。

---

## Slide 21 —— Demo 3：Publish Gates

```bash
make book-check
✗ H2  broken file:line anchor (ch14.md → service.go:154)
✗ H4  undefined cite key (ch11.md)
⚠ S1  18 pages pending review (threshold 10)
⚠ S5  L1 ratio 14%  (threshold 20%)
→ publish blocked: 2 hard, 2 soft
```

- **Hard**：挡 publish
- **Soft**：只告警

> "一个 KB 成熟" 的定义：**不是没错，而是错会被抓住**。
> 对比一下 "wiki 烂掉" 的典型路径 —— 没人知道它烂了。
> publish gate 的价值是把"腐烂"变成一个**机器可见的事件**。

---

## Slide 22 —— 三句话带走

1.  Code 不是 Prose。**别** dump 整个 repo。
2.  AI 写的页面 **永远 `pending`**。
3.  按 **commit** 预算，不按页面。

> 慢。每句念完停 3 秒。
> 三句话背后是三种工程纪律：**对结构的尊重、对审阅的敬畏、对成本的诚实**。
> 其中任何一条都足以改变一个团队的 KB 命运。

---

## Slide 23 —— 如果你只有 20 分钟阅读

- **做 Prose** → Ch 4 + 5 + Ch 7a 的 Part II checklist
- **做 Code** → Ch 8 + Ch 12 RRF + Ch 13 两条硬规则
- **做 Ops** → Ch 14 三层过滤 + Ch 22 commit-not-pages

> 整本书 24 章；如果今天只记住这张 slide，已经够用。
> 留一句给听众："先挑一条今天能开工的。明天就动。"

---

## Slide 24 —— Q&A

- "Copilot 不够吗？"
- "tree-sitter + sqlite-vec + Memgraph 在我们栈上能跑吗？"
- "L1 比例低于 20% 怎么办？"
- "内部代码能丢给外部 LLM 吗？"

> 每个问题都在 `outline.md` 的"可预期问题"里准备了答案。
> 现场回答不出来的，记下来，**不硬答**。一个诚实的 "不知道，会后补" 比
> 十个漂亮的 hallucination 有价值得多 —— 今天讲的整本书，本质就是这个。

---

## Slide 25 —— 谢谢 / 入口

- 书的入口：`source/_build/html/` 或 `http://localhost:8800`
- 反馈：PR 到 `source/part0-presentation/`
- **用 AI 给软件项目造一个知识库**

> "希望今天讲的六条，明天有一条你会去试。"
