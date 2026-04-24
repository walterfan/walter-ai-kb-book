---
title: "Part 0 — 引言：用 AI 给软件项目造一个知识库（60 分钟）"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: partial
keywords:
  - presentation
  - deepwiki
  - overview
  - onboarding
---

# Part 0 — 部门分享：用 AI 给软件项目造一个知识库（60 分钟）

```{admonition} 使用说明
:class: tip

这一部分不是一章独立的技术内容，而是**整本书的 60 分钟分享版**。
面向的是 *部门内部同事* —— 前后端工程师，大多数人用过 Cursor / Codex / Claude Code，
但没专门做过 RAG / KG。节奏是 **30 分钟讲 + 20 分钟 demo + 10 分钟 Q&A**。

- `index.md`（本文）—— 可直接通读的讲稿，讲者可以当"口水稿"用。
- `outline.md` —— 分钟级 speaker outline，精确到每分钟讲什么。
- `slides.md` —— slides 大纲，每页一个标题 + bullet + 讲稿备注，
  方便复制到 slidev / reveal / Keynote。

书中所有用到的概念、数字、引用，都指向后续章节里的某一章。
这一讲只走**主线**——不陷入任何一个细节——细节请回到相应 Part。

**术语约定**：讲稿里直接用英文的概念 —— `Prose / Code / Dual Stack /
frontmatter / footer / tuple / retrieval / embedding / graph / RRF /
MCP / agent / commit-not-pages / L-git / L-entity / L-link`。这些词的精确性
高于任何常见中文翻译，硬翻反而会丢掉它们的工程意涵。
```

## 开场 —— 一个周二下午的场景（3 分钟）

周二下午两点。新同事入职六周，她在 PR 频道里问了一句：

> *"`runSync` 是在哪儿被调用的？"*

资深工程师截了一张 `grep` 的图回过去：**37 个命中** —— 有注释，有测试，
有一行日志模板里的字符串字面量，还有两个完全无关的类型上同名的方法。

她还是不知道这个仓库到底干了什么。

翻到 wiki，搜 "sync"，找到三段讲"同步工作流"的文稿，**一个字都没提到函数名**。
换到 ChatGPT，把 prompt 写得很努力——模型自信满满地编造了两个并不存在的调用者。

几周过去了，她还在猜。

这就是第 8 章开头那个场景 {cite}`fanyamin2026deepwiki`。今天这一个小时，
我想跟大家讲的是：**为什么我们每天都在重复这个周二下午，以及一个"代码仓库的知识库"
应该长什么样才能救这个下午。**

---

## Why —— 我们为什么需要一个 *软件项目* 的知识库（5 分钟）

工程团队每天都在产生知识碎片——代码、工单、聊天记录、设计稿、runbook——
产出速度比人类能整理的速度快得多。

过去我们用三种办法对付这件事：

1.  **写文档。** 写得动的时候文档跟得上；一旦团队/代码库变大，文档永远落后一个版本。
2.  **`grep` + "去问某某人"。** 这是绝大多数团队的现实。部落知识（tribal knowledge）
    集中在少数几个人头上，他们一离职，一段代码就变"遗迹"。
3.  **把整个 repo 丢给 LLM。** 听起来诱人，但：上下文窗口撑不住（~20 kLOC 以上就崩），
    没有引用来源（不可验证），**还会自信地编造**（Chapter 8 里那两个不存在的函数）。

这三种办法都没有解决问题的结构：**软件知识是两种不同的东西**——

- **Prose（文稿）**：*为什么* 这么设计、这个模块 *干什么*、on-call 时
  *该怎么操作*。这部分人类写得好，LLM 写不好，漂移得快。
- **Code（代码）**：*谁调用* `runSync`、*哪个结构体* 实现了 `Repository`、
  这个函数 *在第几行*。这部分机器查得准，人类记不住。

前者答的是 *"为什么"*，后者答的是 *"哪里 / 谁 / 怎样"*。两种知识的问法、
写法、维护方式**完全不同** —— 把它们塞进同一个 wiki 或同一个 LLM 上下文，
结果就是开场那个周二下午。

绝大多数"文档工具"只处理第一种。而一个 *软件项目* 的知识库必须把两者**同时**
处理好，还要让它们**互相指**（一段 Prose 必须能 `file:line` 精准指向一段 Code，
一段 Code 也必须能回溯到解释它的 Prose）。

> **这是这本书的 Thesis**：一个软件项目的知识库 = 一个 *Prose layer* +
> 一个 *Code layer* + 一个让两者协作的 *Hybrid layer* + 一套让它们
> *不腐烂* 的运维纪律。
>
> 把这个定义倒过来说可能更锋利一点：**一个只处理 Prose 的系统叫"文档"，
> 一个只处理 Code 的系统叫"搜索"；两头都处理、并且互相指的系统，
> 才配叫 KB。**

接下来 50 分钟，我按这个骨架讲，不陷入任何细节。

---

## What —— 这本书的六个 Part，一张图说清楚（5 分钟）

```{mermaid}
flowchart LR
    P1[Part I<br/>Foundations<br/>词汇与方法] --> P2
    P1 --> P3
    P2[Part II<br/>Prose Layer<br/>文件型 wiki] --> P5
    P3[Part III<br/>Code Layer<br/>parse→embed→graph→retrieve] --> P5
    P2 --> P4[Part IV<br/>Ops &amp; Lifecycle<br/>增量同步 / 评测 / 漂移]
    P3 --> P4
    P4 --> P5[Part V<br/>Hybrid Layer<br/>L0–L4 / Agent / MCP]
    P5 --> P6[Part VI<br/>Governance &amp; Outlook<br/>成本 / 隐私 / 安全]
```

用一句话串起来：

- **Part I**：建立词汇 —— 什么叫"软件知识库"，IR / RAG 的最小必要背景，
  Diátaxis 的四象限（tutorial / how-to / reference / explanation）。
- **Part II**：*Prose Layer* —— 用文件（Markdown + Git）做 wiki，
  用 frontmatter + footer 保留出处与审阅状态。
- **Part III**：*Code Layer* —— parse → embed → graph → hybrid retrieve → prompt，
  让 KB 能回答 "`runSync` 在哪儿被调用"。
- **Part IV**：*Ops & Lifecycle* —— 让它**不腐烂**。增量同步、评测、drift、
  link rot。
- **Part V**：*Hybrid Layer* —— Prose + Code + graph + agent。L0–L4 文档
  分层、agent 通过 MCP 工具使用 KB。
- **Part VI**：*Governance & Outlook* —— 成本、隐私、安全，以及剩下的
  开放问题。

大多数团队的 KB 都是在 **Part IV** 那里死掉的：能建，不能维护。今天的六个
灵魂概念里，有一半直接对着 Part IV 写的。

今天这一小时，我只讲**主线上的六个灵魂概念**：

1.  *Prose 的两块契约*：frontmatter（出处）+ footer（审阅状态）
2.  *Code 不是 Prose*：三条结构性主张 + Dual Stack（vector + graph）
3.  *L0–L4 tuple*：⟨layer, updated_by, review_status, review_score⟩
4.  *Hybrid Retrieval*：vector → keyword → graph expansion + RRF
5.  *三级更新策略*：L1 机械 / L2 有界 LLM / L3 人审
6.  *Commit-not-pages 预算*：KB 的 LLM 成本应该与 **提交次数** 成正比，
    而不是页面数

每个概念我只讲 3-4 分钟，然后用一个 demo 段落把它们串起来。细节请回到相应
的 Part。

---

## 一个研究脉络 —— 为什么这件事在 2024–2025 变得"成形"（3 分钟，可压缩）

如果你担心今天讲的只是一个工程师的私有偏好，其实这两年论文里的脉络已经很清楚了：

- **Zhu et al. 的综述** 说明：LLM 在 KG 场景里，往往**更擅长拿着结构化上下文做推理**，
  而不是从原始文本里稳定地 few-shot 抽取结构
  {cite}`zhu2024llmsknowledgegraphconstruction`。这正对应本书的分工：
  **parser / schema / verifier 负责造结构，LLM 负责解释和综合。**
- **RepoAgent** 把"项目级代码文档"明确定义成三段流水线：**全局结构分析 →
  文档生成 → 文档更新** {cite}`luo2024repoagentllmpoweredopensourceframework`。
  这说明"给 repo 写文档"不是一次 prompt，而是一个长期维护系统。
- **CGM** 更进一步：它不满足于把图谱放在检索器旁边，而是把**代码图直接并入模型**
  来做项目级任务 {cite}`tao2025codegraphmodelcgm`。这说明图不是临时补丁，
  而是 repo-level 理解里的**一等信号**。

所以这本书不是在发明一个孤立技巧，而是在把一条越来越清晰的 research line
工程化：**结构化抽取、项目级持续更新、图增强理解**。

---

## How —— 六个灵魂概念各 3 分钟（约 22 分钟）

### 1. Prose 的两块契约：frontmatter + footer（第 5 章）

一个 wiki 页面，凭什么值得被相信？凭 **它能回答两个问题**——

- *这页是怎么来的？* —— `frontmatter` 记录 lineage（来源、作者、上次验证的 commit）。
- *这页现在还可信吗？* —— `PKB-metadata` footer 记录 review 状态。

footer 的四个字段是这本书后面一切的地基：

```yaml
<!-- PKB-metadata -->
layer:         L2            # L0–L4, 与第 18 章文档分层对齐
updated_by:    ai            # human / ai / ai+human
review_status: pending       # pending / approved
review_score:  0             # 0–5, 人类审阅时给
reviewed_by:   null
commit:        a1b2c3d       # 这个页面最后一次被验证时对应的 commit
```

这里有一条**铁律**，整本书反复用到：

> **AI 写的页面，`review_status` 永远是 `pending`。** 人类看过、打分，才能 `approved`。

这条规则把 *"写得便宜"* 和 *"可信任"* 解耦了。LLM 可以一分钱重写 100 页，
但这些页面在人类签字之前都是 `pending` —— 检索排序、publish gate、agent
的引用决策都可以用这个字段 **无争议地** 做决策。

别小看 `pending` 这四个字母：它是**检索排序、publish gate、agent 决策**
共用的"最小可验证单位"。没有它，KB 和"一个拼写更好的 markdown 文件夹"
没什么区别。

### 2. Code 不是 Prose：三条主张 + Dual Stack（第 8 章）

开场那个 "`runSync` 在哪儿被调用" 的场景，病根是 wiki 把 Code 当成了
**长文稿**。第 8 章总结了三条主张 {cite}`allamanis2018survey`：

1.  **Code 有 prose retrieval 会丢掉的结构。** 一个函数不是词袋：它有
    名字、签名、docstring、body、起止行、imports，以及——一旦有了
    imports——**调用图**。用 `RecursiveCharacterTextSplitter(chunk_size=1500)`
    切 Java 方法，会把签名、实现、尾括号切到向量空间三个不同区域。
2.  **Code 检索需要精确匹配的逃生口。** 用户输入 `entityID` 时要的是名字叫
    `entityID` 的函数，不是 "*entity* 和 *ID* 的语义邻居"。CodeSearchNet
    {cite}`husain2019codesearchnet` 最早的那批 dense-only 检索器就在
    identifier-heavy 的 query 上输给了十五年前的 BM25
    {cite}`robertson2009bm25`。
3.  **Code 有 embedding 抓不住的关系。** 向量空间 encode "相似"，不 encode
    **calls / implements / imports / returns**。两个签名相同但分别住在
    HTTP handler 层和后台 worker 层的函数，在向量空间里挨得很近 ——
    但它们的语义天差地别。

这三条都不是"性能问题"，是**语义类型错误** —— 把"关系"当"相似度"看。
一旦同意这一点，下面这个 Dual Stack 就不再是"为了更准"，而是
"为了讲对" ——

```{mermaid}
flowchart LR
    A[Git working tree] --> B[Parser<br/>tree-sitter]
    B --> C[Entity<br/>stable ID]
    C --> D[Embeddings<br/>sqlite-vec / pgvector]
    C --> E[Graph<br/>Memgraph]
    D --> F[Hybrid retriever]
    E --> F
    F --> G[Prompt &amp; generator]
```

三个不能省的设计决定：

- **Stable identity.** `sha256(repoID + filePath + entityType + name + startLine)[:16]`。
  这是 entity 的**身份证**，让 graph 在 re-index 后活下来，让增量同步敢做
  `delete-then-insert`，不留悬挂边。
- **结构化的 embedding 输入。** 我们 **不** embed 函数体，而是 embed 一个
  5 行的 identity header：`Language / Type / Name / Signature / Doc`。
  第 10 章实测，recall@10 差不多 **翻一倍** —— 因为用户输入的是 *意图*，
  identity 是离意图最近的那一面，body 是离意图最远的那一面。
- **8 条 edge 的受限关系分类学。** `CONTAINS / IMPORTS / CALLS / IMPLEMENTS /
  EMBEDS / DEPENDS_ON / RETURNS / ACCEPTS`，加第九条需要**设计评审级别**
  的讨论。这是一个**让 graph 在运营上长期讲得通的护栏** —— 没有这条
  护栏，graph 的 schema 两个 sprint 就会变成没人敢碰的"博物馆"。

### 3. L0–L4 tuple：为什么单轴不够（第 18 章）

博客原版的 L0–L4 是一个**单轴权威度**模型 {cite}`fanyamin2026deepwiki`：

| Tier | 权威度 | 谁写 | 例子 |
|:--:|:--|:--|:--|
| **L0** | 最强 | 代码与注释 | 函数体、docstring、OpenAPI |
| **L1** | 强 | 人类，已提交 | ADR、架构文档、手写 runbook |
| **L2** | 中 | 人类，协作型 | wiki 页面、设计文档、复盘 |
| **L3** | 弱 | AI，已审阅 | LLM 生成，人类看过 |
| **L4** | 条件性 | AI，未审阅 | LLM 生成的 draft |

用了一段时间之后，第 18 章指出这个单轴**不够** —— 它把两件必须分开的事
混在一起：*谁写了当前这一版* 和 *有没有人审阅过*。这两件事的漂移速度
完全不同：作者可能十年不变，审阅状态可能一个 commit 就翻转。

于是升级成一个 **tuple**（把 footer 4 字段直接搬进来）：

$$
\text{layer} = \langle L,\ U,\ R,\ S \rangle
$$

| 页面 | 单轴 | tuple | 检索权重 |
|:--|:--:|:--|:--:|
| L1 ADR，人写，已审，评 4 | L1 | ⟨L1, human, approved, 4⟩ | **1.0** |
| L1 ADR，LLM 重写，待审 | L1 | ⟨L1, ai, pending, 0⟩ | **0.3** |
| L3 摘要，LLM 草稿，人审过 | L3 | ⟨L3, ai+human, approved, 4⟩ | **0.8** |
| L3 摘要，LLM 草稿，没审 | L3 | ⟨L3, ai, pending, 0⟩ | **0.2** |

单轴能给检索一个数，tuple 能给四个。对一个凌晨 3 点的线上事故问题来说，
能分清楚 `⟨L1, human, approved⟩` 和 `⟨L1, ai, pending⟩` 之间的差别，
**救不救命是两码事**。

最反直觉的一行 —— "LLM 草稿 + 人审过" 的权重（0.8）**高于** "L1 ADR +
LLM 重写没审" 的权重（0.3）。**权威来自"谁签了字"，不是"谁写的第一稿"**。
这句话比它看起来更重要：一旦一个团队接受了"签字才是权威"，LLM 就可以
被放心地用来**批量生产 draft**，因为它们在签字之前对 KB 的决策面
没有任何影响力。

### 4. Hybrid Retrieval + RRF：为什么分数融合没意义（第 12 章）

Code 检索不能只用 vector，也不能只用 keyword，也不能只用 graph。这不是
性能问题，是 **语义问题** —— 三种 retriever 回答的是三种不同的问题。
第 12 章用一个 **三层漏斗** 把它们绑在一起：

1.  **Vector** 作为主路（回答 "语义接近" 的 query）
2.  **Keyword / BM25** 作为 fallback（回答 "我就要这个 identifier" 的 query）
3.  **Graph expansion** 作为补充（回答 "谁调用它、它实现谁" 的 query）

融合时 **不要做分数融合**。不同 retriever 的分数不在同一个量纲上 ——
同一个文档可能在 A 拿 0.82 (cosine)、在 B 拿 14.7 (BM25)、在 C 拿 2 (hops)。
把它们加权相加，等于把三种不同单位的数字强行叠加，是纯迷信。正确做法
是 **RRF**（Reciprocal Rank Fusion {cite}`cormack2009rrf`）：

$$
\text{rrf}(d) = \sum_{i} \frac{1}{k + \text{rank}_i(d)}
$$

只关心 rank，不关心 score。一行公式把问题降到 "排名" 这个
**跨 retriever 不变量** 上 —— 这才是可加的。这一行是整本书里最短、
最值钱的东西之一。

### 5. 三级更新策略：让 "保持新鲜" **便宜**（第 16 章）

一旦 KB 有几百页了，每次 commit 都重新跑全量 LLM 重写 —— **成本很低，但会
产出一个没人会评审的 400 文件 PR**。第 16 章把更新分成三级：

| 级别 | 谁做 | LLM 成本 | 处理 |
|:--:|:--|:--:|:--|
| **L1** | 脚本（机械） | **0 token** | footer 的 `commit` 字段更新；死链修复；re-stamp |
| **L2** | LLM + 受限 context（~5 k token） | 有界 | 段落级改写、拼写修正、跟一个函数变动同步引用 |
| **L3** | 人 + LLM 辅助 | 变量 | 架构变更、废弃工作流、有冲突的信息合并 |

**规则：Rule first, LLM second.** 能用 L1 解决的绝不调 LLM；能 L2 解决的
绝不叫人。AI 做的所有改动，`review_status` 永远落到 `pending` ——
前面那条铁律。

顺序反过来的代价比 token 本身贵得多：把能脚本的事交给 LLM，成本翻十倍；
把能 LLM 的事叫人，**评审者会先弃权** —— 然后整个 KB 就慢慢烂掉。
这条规则真正保护的不是预算，是**评审者的注意力**。

### 6. Commit-not-pages 预算：KB 应该有多贵？（第 22 章）

最后一条，也是今天最想大家带走的一条工程纪律：

> **一个 KB 的 LLM 成本，应该是 *提交次数* 的可预测函数，而不是
> *页面数* 的函数。**

Naive baseline —— "主题有变就重写全页" —— 成本是：

$$
\text{cost}_\text{naive} \approx N_\text{candidates} \times C_\text{full-page}
$$

其中 $C_\text{full-page}$ 大概 8–20 k token 的一次调用。随着 KB 变大，
候选数也涨，你会得到一条漂亮的死路：**KB 越有用 → 越大 → 每次 commit
越贵 → 预算爆掉 → 停止维护**。

三级更新策略下：

$$
\text{cost}_\text{3L} \approx N_\text{L1}\cdot 0 + N_\text{L2}\cdot C_\text{bounded} + N_\text{L3}\cdot 0
$$

L1 和 L3 都 **不花 LLM token**。L2 上限约 5 k token。

commit-not-pages 真正做的事，是把成本曲线 **从 $O(\text{KB size})$ 拽回
$O(\text{change rate})$**。KB 再大都可以，因为每次 commit 的开销只跟
*这次改动* 的规模有关。

具体到第 16 章那个例子（一周 19 个候选：12→L1、5→L2、2→L3），按 2024 年
`text-embedding-3-small` / `gpt-4o-mini` 的定价 {cite}`openai_embeddings_v3`
算下来是 **每仓库每周几美分**。Naive baseline 在同样 19 个候选上花费
**高出十倍以上**，*而且* 会烧掉评审者的时间 —— 那才是更贵的资源。

三条可以今天就开始做的规则：

1.  **按 commit 定预算**（例如小团队每次 commit $\$0.10$ 上限）。
2.  **L1 比例是一项 KPI。** 50 % 健康，90 % 优秀，低于 20 % 说明规则
    没覆盖常见场景。
3.  **L3 的瓶颈是人的注意力，不是钱。** 不要试图拿 L3 换 L2 省钱 ——
    一旦评审积压，整个 pipeline 会从上往下锁死。

---

## Example —— 一次完整的同步 + 一次 agent 问答（20 分钟 demo）

这一段**最好现场跑**。讲稿里保留命令与预期输出，以便演示不成功时可以切到截图 fallback。

```{admonition} 可运行的 demo 脚本
:class: tip

三个 demo 都有对应的自包含 Python 脚本，位于
`source/examples/part0-presentation/`，零外部依赖，一键可跑：

- **Demo 1**：`poetry run python source/examples/part0-presentation/demo1_incremental_sync.py`
- **Demo 2**：`poetry run python source/examples/part0-presentation/demo2_agent_kb_query.py`
- **Demo 3**：`poetry run python source/examples/part0-presentation/demo3_publish_gates.py`

详见 `source/examples/part0-presentation/README.md`。
```

### Demo 1 —— 一次增量同步：36× / 180× / 9×（8 分钟）

背景：一个 100 kLOC 的 Go 仓库，第一次全量 sync 用时约 3 分钟。现在在 `service.go`
改一行代码，commit 之后问 KB："做了哪些事？花了多久？"

```bash
# Step 1 —— 全量 sync（一次性，走 tree-sitter + embedding API + graph rebuild）
code-kg sync --repo-id demo-repo
# → parsed 8,421 entities, 34,182 relations
# → embedded 8,421 identity headers   (batched, with backoff)
# → graph rebuilt                     (≈ 3 minutes wall clock)

# Step 2 —— 改一行代码，commit
echo '// touch' >> service.go && git commit -am "no-op edit"

# Step 3 —— 增量 sync
code-kg sync --repo-id demo-repo --incremental
# → L-git:    diff HEAD^..HEAD finds 1 file
# → L-entity: 1 entity moved (service.go:runSync, same ID re-pinned)
# → L-link:   no broken links
# → vector:   2.1 s
# → keyword:  0.4 s
# → graph:    20 s  (small subgraph rebuild)
```

把数字摆上来（Appendix B 里可复现）{cite}`fanyamin2026deepwiki`：

| 场景 | 全量 | 增量 | 加速比 |
|:--|--:|--:|--:|
| 关键词 | ~3 分钟 | ~5 秒 | **36×** |
| 向量检索 | ~3 分钟 | <1 秒 | **180×** |
| 图重建 | ~3 分钟 | ~20 秒 | **9×** |

> **要讲的观点**：这个 180× 不是 "vector 很快"，而是 *stable entity ID +
> L-git / L-entity / L-link 三层过滤* 让绝大多数 commit 只需要碰 1-2 个
> entity。第 14 章那句话是：
> *"Detection is cheap and deterministic; update is expensive and sometimes
> uses an LLM. 把两者合二为一就会同时得到两者最糟糕的部分。"*
> 记住这张表的**形状**：180× 来自 vector 不需要重算；9× 来自 graph 必须
> 重写最小子图；36× 是两者之间的地板。

### Demo 2 —— 一个 agent 拿 KB 回答问题（8 分钟）

这一段最好开一个 IDE（Cursor / Claude Code），让 agent 通过 MCP 调用 KB。
三个工具就够了（第 21 章）：

| 工具 | 输入 | 输出 |
|:--|:--|:--|
| `kb.search(query, k, filter)` | 自然语言 + top-k + tuple predicate | `{page_id, score, tuple, snippet}` 列表 |
| `kb.read(page_id)` | page id | body + frontmatter + **footer** |
| `kb.cite(query, k)` | 自然语言 + top-k | `{page_id, file:line}` 锚点 |

一次完整 round-trip：

```text
08:15  开发者在 IDE 里输入  /ask "ingest pipeline 是怎么处理 CSV 的?"
       agent 调用          kb.search(q=..., k=5, filter="review_status==approved")
       KB 返回             [
                             {page_id: "ch06", score: 0.83,
                              tuple: ⟨L2, human, approved, 4⟩, ...},
                             {page_id: "ingest-runbook", ...},
                             ...
                           ]
       agent 调用          kb.read("ch06")
       KB 返回             { body: ..., frontmatter: ...,
                             footer: {review_status: approved, ...} }
       agent 回答          引用 ch06 第 3 段 + ingest-runbook 第 4 节。

08:17  开发者追问          "具体是哪个文件 parse 的 CSV？"
       agent 调用          kb.cite(q="CSV parsing", k=3)
       KB 返回             [
                             {page_id: "ch06",
                              file_line: "internal/pipeline/csv_loader.go:42"},
                             ...
                           ]
       agent 回答          "`internal/pipeline/csv_loader.go:42`—— 是 CSV loader
                           的入口函数 `parseCSV`。" （带可点击的 file:line 链接）
```

三个可以强调的细节：

1.  **`kb.read` 把 footer 一起返回**。agent 在引用之前先看 `review_status`、
    `review_score` —— "这页 AI 写的没审阅" 对 agent 是个强信号。
    真正革命性的一件事不是 "agent 会调 API"，是 **agent 开始读 footer** ——
    它第一次拿到了 "要不要相信这一页" 的机器可读信号。
2.  **`kb.cite` 返回的是 `file:line`，不是文稿**。这把第 12 章的硬规则
    做成了工具。agent 如果虚构行号，第 15 章的 CI gate 会把这种页面挡在
    publish 之外 —— 写 KB 的和读 KB 的 agent 对 hallucination 有了
    **同一套治理闭环**。
3.  **`filter` 参数**让 agent 按 tuple 过滤 —— 要不要只用 approved 的？
    要不要排除 L4？完全由 agent 策略决定。换句话说：**tuple 不是元数据，
    是 agent 的 API**。

### Demo 3 —— 发布门禁（4 分钟）

最后留 4 分钟演示第 15 章的 **publish gates**——KB 要上线前，必须过的机械检查。

**Hard gates（挡住 publish）**：

- 每一页都必须有 `PKB-metadata` footer。
- 每一个 `file:line` 锚点都必须在 **当前 commit** 下能解析。
- 页面内不得有 `[TODO]` / `[FIXME]` 占位符。
- 每一个 `{cite}` key 都必须在 `references.bib` 里存在。

**Soft warnings（只告警）**：

- `review_status: pending` 的页面超过 N 个。
- `last_verified_commit` 超过 30 天没更新。
- L1 比例低于 20%（第 22 章的 KPI）。

```bash
make book-check
# ✗ H2  broken file:line anchor: ch14.md:  service.go:154 (deleted in a1b2c3)
# ✗ H4  undefined cite key: ch11.md:       {cite}`huang2024graphpagerank`
# ⚠ S1  18 pages have review_status=pending (threshold: 10)
# ⚠ S5  L1 ratio: 14%  (threshold: 20%)
# → publish blocked: 2 hard, 2 soft
```

这就是 "一个 KB 成熟" 的样子：**不是没错，而是错会被抓住**。
把这一条对比一下 wiki 烂掉的典型路径 —— 没人知道它烂了。publish gate
的价值是**把腐烂变成一个机器可见的事件**。

---

## Conclusion —— 我想让你带走的三句话（2 分钟）

1.  **Code 不是 Prose**。别把一个 repo 全塞进 LLM 的 context；给它造一个
    Dual Stack（vector + graph）和一个 *retrieve → cite → refuse* 的纪律。
2.  **AI 写的页面永远 `pending`**。写便宜 ≠ 可信；让 `review_status` 当
    那个无争议的 ground truth。
3.  **按 commit 做预算，不按页面**。三级更新策略让 KB 的成本随 *项目
    变化率* 走，不随 *KB 规模* 走 —— 这是让 KB 长期活着的工程纪律，
    不是一条微优化。

这三句话背后是三种工程纪律：
**对结构的尊重、对审阅的敬畏、对成本的诚实**。
其中任何一条，都足以改变一个团队 KB 的命运。

这本书有六个 Part、二十四章。如果你 **只有 20 分钟** 的阅读预算 ——

- 做 Prose Layer，读 **Ch 4 + Ch 5 + Ch 7a 的 Part II 一页 checklist**。
- 做 Code Layer，读 **Ch 8 + Ch 12 的 RRF 那一节 + Ch 13 的两条硬规则**。
- 做 Ops，读 **Ch 14 的三层过滤 + Ch 22 的 commit-not-pages**。

剩下的时间 —— **Q&A**。先挑一条今天能开工的 —— 明天就动。

---

## References

```{bibliography}
:filter: keywords % "deepwiki" or keywords % "presentation" or keywords % "code-layer" or keywords % "operations" or keywords % "hybrid" or keywords % "governance"
```

```{toctree}
:hidden:

outline
slides
```
