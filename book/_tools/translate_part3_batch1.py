"""Apply Chinese translations for Part III batch 1: index + ch08 + ch09 + ch10.

Run with: poetry run python book/_tools/translate_part3_batch1.py

Style guide inherited from book/_tools/translations/ch02-ir-rag-primer.zh.py:
  - English kept for: CLI names, file paths, variable names, signature
    fragments, `{cite}` keys, $math$, API symbols (e.g. BM25, RRF, HNSW).
  - CommonMark emphasis around *...* with CJK flanking characters needs
    an ASCII space on each side (e.g.  "*“text”*"  ->  "* “text” * ").
  - "prose" -> "文稿"; "document" -> "文档"; "entity" -> "实体";
    "retrieval" -> "检索"; "embedding" -> "嵌入向量" when noun,
    "嵌入" when verb/adj; "signature" -> "函数签名".
  - Keep **bold** markup and `code spans` exactly as English.
  - Technical identifiers (e.g. `runSync`, `CodeEntity`) stay English.
"""

from __future__ import annotations

import glob
import os
import sys
import polib

LOCALE_ROOT = "book/locale/zh_CN/LC_MESSAGES/part3-code-layer"


INDEX: dict[str, str] = {
    "Part III — The Code Layer": "第三部分 —— 代码层",

    'Part III on one page — six chapters turn the "wiki works, grep doesn\'t" pain of Part II into a dual-stack (vector + graph) retriever that answers structural, identifier, and fuzzy questions with citations:':
        "第三部分一图览 —— 六章把第二部分“wiki 好用、grep 不行”的痛点，升级成一个双栈（向量 + 图谱）检索器，能为结构化、标识符精确匹配以及模糊自然语言三类问题都给出带引用的答案：",

    "Why": "Why —— 为什么",

    "Part II's prose layer solves one class of question — *\"what do we know about X?\"* — and fails on the other — *\"where in the code base is X used?\"*. Chapter 8 makes the failure precise; the rest of Part III builds the dual-stack (vector + graph) pipeline that answers the second class, grounded in the code-layer reference implementation (paths under `reference-impl/code-kg/`).":
        "第二部分的文稿层解决了一类问题 —— * “我们对 X 了解多少？” * —— 但对另一类 —— * “代码库里哪里用到了 X？” * —— 束手无策。第 8 章会把这个失败讲得更精确；第三部分其余各章则围绕“代码层参考实现”（路径位于 `reference-impl/code-kg/` 下）构建起一条能回答第二类问题的双栈（向量 + 图谱）流水线。",

    "The failure is not a gap in the wiki — it is a category error. A human writes a wiki page about *\"how sync works\"* but not about *\"who calls `runSync`\"*, because the first sentence is worth writing and the second is derivable from the code. A code-layer KB is the machine that *does* the deriving, continuously, so that every engineer gets the answer in two seconds rather than twenty minutes of grep-and-scroll.":
        "这个失败并不是 wiki 的遗漏，而是范畴错误。人会写一篇 * “同步是怎么工作的” * 的 wiki 页，却不会去写 * “谁调用了 `runSync`” * —— 因为前一句值得动笔写，后一句可以从代码推导。代码层知识库就是那台 * 持续做推导 * 的机器，让每个工程师都能在两秒内拿到答案，而不是 grep 二十分钟再滚动翻看。",

    "What": "What —— 是什么",

    "Everything needed to answer structural, identifier, and fuzzy natural-language questions over a codebase with *citations* — one chapter per stage of the pipeline introduced in the blog's §§2–8 {cite}`fanyamin2026deepwiki`:":
        "覆盖一切：在代码库上回答结构化、标识符精确匹配以及模糊自然语言三类问题，并 * 为每条结论给出引用 * 。按博客 §§2–8 {cite}`fanyamin2026deepwiki` 所划分的流水线阶段，每章对应一个阶段：",

    "**Chapter 8 — Why code is not prose.** Three structural claims (parse first, embed identity, graph carries relations); one measured experiment (vector-only vs hybrid on real code queries); four anti-patterns that cause first-time code-KB builds to fail.":
        "**第 8 章 —— 为什么代码不是文稿。** 三条结构性主张（先解析、再嵌入“身份”、图谱承载关系）；一个可量化的对比实验（纯向量 vs 混合，在真实代码查询上）；四个让首次搭建代码知识库的团队踩坑的反模式。",

    "**Chapter 9 — Parsing and entity extraction.** A real parser (tree-sitter {cite}`brunsfeld_treesitter`); a closed entity schema (`package`, `type`, `method`, `function`); stable IDs from `sha256(repoID + filePath + entityType + name + startLine)[:16]`; resource-leak, closure-noise, and multi-line-signature pitfalls.":
        "**第 9 章 —— 解析与实体抽取。** 一个真正的解析器（tree-sitter {cite}`brunsfeld_treesitter`）；一份封闭的实体集合（`package`、`type`、`method`、`function`）；稳定 ID 来自 `sha256(repoID + filePath + entityType + name + startLine)[:16]`；以及资源泄漏、闭包噪声、多行签名三类典型坑。",

    "**Chapter 10 — Embeddings and vector stores.** A five-line identity template (`Language / Type / Name / Signature / Doc`) that beats body-embedding by roughly 2x on recall@10; batch + backoff + rate-limit discipline; `sqlite-vec` {cite}`sqlite_vec` / `pgvector` {cite}`pgvector` / `Milvus` {cite}`milvus` decision matrix; theory anchor on bi-encoders {cite}`reimers2019sbert`, cross-encoders {cite}`nogueira2019passage`, and HNSW {cite}`malkov2018hnsw`.":
        "**第 10 章 —— 嵌入向量与向量存储。** 五行的“身份模板”（`Language / Type / Name / Signature / Doc`），在 recall@10 指标上大约是嵌入函数体的两倍；批量 + 退避 + 限速三件套；`sqlite-vec` {cite}`sqlite_vec` / `pgvector` {cite}`pgvector` / `Milvus` {cite}`milvus` 的选型决策矩阵；配套理论锚点：bi-encoder {cite}`reimers2019sbert`、cross-encoder {cite}`nogueira2019passage` 与 HNSW {cite}`malkov2018hnsw`。",

    "**Chapter 11 — Code knowledge graph.** A closed eight-edge taxonomy on a graph database (e.g. Memgraph {cite}`memgraph`); location-aware node IDs; full-rebuild-per-repo write pattern; theory anchor on graph locality and the GraphCodeBERT data-flow prior {cite}`guo2021graphcodebert`.":
        "**第 11 章 —— 代码知识图谱。** 一套跑在图数据库（例如 Memgraph {cite}`memgraph`）上的封闭八种关系；位置相关的节点 ID；每个仓库一次“全量重建”的写入模式；理论锚点：图的“邻近性”观念，以及 GraphCodeBERT 提出的数据流先验 {cite}`guo2021graphcodebert`。",

    "**Chapter 12 — Hybrid retrieval and RRF.** Three-tier strategy (vector primary → keyword fallback → graph expansion); why score-level fusion is meaningless and rank-level fusion (RRF {cite}`cormack2009rrf`) is the upgrade path; query-routing heuristics that save latency.":
        "**第 12 章 —— 混合检索与 RRF。** 三层策略（向量优先 → 关键词兜底 → 图扩展）；为什么“按分数加权融合”毫无意义，而“按排名融合”（RRF {cite}`cormack2009rrf`）才是正确升级路径；节省延迟的查询路由启发式规则。",

    "**Chapter 13 — Prompt and generation.** Two hard rules (always cite `file:line`; refuse when context is insufficient); structured-context format; measurable faithfulness {cite}`es2024ragas`; the indirect prompt-injection threat model {cite}`greshake2023injection`.":
        "**第 13 章 —— Prompt 与生成。** 两条硬规则（每条结论都要附 `file:line`；上下文不足就明确拒答）；结构化上下文格式；可度量的 faithfulness {cite}`es2024ragas`；以及间接 prompt 注入的威胁模型 {cite}`greshake2023injection`。",

    "How": "How —— 怎么做",

    "Every chapter ships at least one `{literalinclude}` from a vendored excerpt (see `examples/SOURCE.md`), at least three citations, and at least one measurement the blog did not report — the book's non-copy policy. Excerpts are refreshed with `make book-refresh-excerpts` and verified byte-stable with `make book-check-excerpts`.":
        "每章都至少附带一段来自 vendored 代码节选的 `{literalinclude}`（见 `examples/SOURCE.md`）、至少三条引用，以及至少一项博客中未出现的测量数据 —— 这是本书的“不照搬”原则。节选通过 `make book-refresh-excerpts` 刷新，并用 `make book-check-excerpts` 做字节级稳定性校验。",

    "Each chapter also follows the same Part II-inspired five-section spine: a *Monday-morning hook* connecting the chapter to a pain you have lived through; the *Why / What / How* that reads as engineering, not survey; a *Theory anchor* (ch10–ch13) that names the published results behind the design; a *Common mistakes* section that lists the anti-patterns; and an *Example* block reproducible against the code-layer reference implementation in Appendix B.":
        "每一章也沿用第二部分立下的五段式骨架： * 周一早晨的钩子 * 把本章和你真实踩过的坑连起来；* Why / What / How * 段读起来像工程而非综述；* Theory anchor * 段（第 10–13 章）明确点出设计背后的已发表结果；* Common mistakes * 段列出反模式；* Example * 段给出可在附录 B 的代码层参考实现上复现的操作步骤。",

    "Operational model": "运维模型",

    "The code layer inherits Part II's verification-first mindset and specialises it:":
        "代码层继承了第二部分“先验证后相信”的思路，并做了针对代码的特化：",

    "**Build** — `code-kg sync --repo-id <id>` parses, embeds, and rebuilds the graph. Idempotent; safe to re-run.":
        "**构建** —— `code-kg sync --repo-id <id>` 执行解析、嵌入、图谱重建。幂等；随时可安全重跑。",

    "**Verify** — recall@5 on a held-out query set (identifier, structural, fuzzy) is the primary retrieval health metric. Prompt metrics (citation compliance, refusal rate) are secondary and *only move* when recall is not the bottleneck.":
        "**验证** —— 在留出查询集上（涵盖标识符、结构、模糊三类）的 recall@5 是检索健康度的首要指标。prompt 相关指标（引用合规率、拒答率）排第二，且 * 只有在 recall 不是瓶颈时 * 才值得去优化。",

    "**Operate** — the retriever degrades gracefully: no embedding API key → keyword-only mode; no graph connectivity → vector + keyword only; no vectors → keyword only. Every mode is still useful; no mode is a hard fail.":
        "**运行** —— 检索器优雅降级：没有嵌入 API key → 仅关键词模式；连不上图谱 → 仅向量 + 关键词；没有向量 → 仅关键词。每种模式都仍然有用；没有一种模式会彻底不可用。",

    "Example": "Example —— 范例",

    "Appendix B runs the full pipeline end-to-end: register the repo, sync, ask three questions (one per retriever tier), then do an incremental sync on a one-line diff to measure the speedup ratio.":
        "附录 B 端到端跑一遍完整流水线：注册仓库、全量同步、按三个检索层各问一个问题，再对一行改动做增量同步，实测增量相对全量的加速比。",

    "Pointer checklist": "要点清单",

    "For a one-screen summary of the six key decisions you carry forward from Part III into your own system, jump to the **\"Part III pointer checklist\"** section at the end of Chapter 13. Each item is a commit-before-coding decision, not a retrospective.":
        "若需要一屏内看完“从第三部分可以带走的六个关键决策”，直接跳到第 13 章末尾的 **“Part III pointer checklist”** 段。每一条都是“写代码前要先拍板”的决策，而非事后总结。",

    "Conclusion": "Conclusion —— 小结",

    "With Parts II and III in place, the KB answers both prose and code questions with cited, reproducible responses. Parts IV–VI make the result *operationally durable* (drift, evaluation, governance) and extend it to hybrid workflows (AI coding assistants, agents).":
        "有了第二部分和第三部分，这个知识库就能用带引用、可复现的方式同时回答文稿问题和代码问题。第四 —— 第六部分会让结果 * 在运维上持续可靠 * （漂移、评估、治理），并把它扩展到混合工作流（AI 编码助手、智能体）。",

    "References": "参考文献",
}


CH08: dict[str, str] = {
    "Chapter 8 — Why Code is Not Prose": "第 8 章 —— 为什么代码不是文稿",

    "This chapter on one page — three structural claims, one experiment, and four anti-patterns that explain why the wiki pipeline of Part II cannot carry code:":
        "本章一图览 —— 三条结构性主张、一个实验、四个反模式，共同说明为什么第二部分那条 wiki 流水线承载不了代码：",

    "It is Tuesday, 2 p.m. The new hire on your team has been at it for six weeks. She opens a pull-request chat and asks: *\"where is `runSync` called from?\"*. The senior engineer pastes a `grep` screenshot with 37 hits — comments, tests, a string literal in log output, two methods on unrelated types. She still cannot tell what the repo actually does. The wiki has three paragraphs about \"syncing,\" none of which mention a function. The chat LLM confidently invents two caller functions that don't exist. Six weeks in, she is still guessing. **This chapter is about why the wiki you just built in Part II cannot save her — and what shape the code layer has to take to rescue the afternoon.**":
        "周二下午两点。团队里新人入职第六周。她在 pull-request 群里问了一句：* “`runSync` 是从哪儿被调用的？” *。资深工程师甩了一张 `grep` 截图，37 条命中 —— 注释、测试、日志输出里的一个字符串字面量、两个跟目标类型毫无关系的方法同名。她依然看不懂这个仓库到底在做什么。wiki 里有三段讲“同步”，但没有一段提到任何函数名字。聊天 LLM 又一脸笃定地编了两个根本不存在的调用方函数。六周过去，她还在猜。**本章讲的就是：为什么你在第二部分刚搭好的那套 wiki 救不了她 —— 以及代码层必须长成什么样才能救回这个下午。**",

    "Why": "Why —— 为什么",

    "Part II built a wiki that treats every page as a *document*: one Markdown file per topic, tokenised as plain text, ranked by prefix match. That model works up to a point — it solves the prose layer completely. It fails the moment the question is about **code**.":
        "第二部分做出的 wiki 把每一页都当作一份 * 文档 * 来对待：每个主题一个 Markdown 文件，按纯文本切词，按前缀匹配排序。这个模型撑到一定程度就够了 —— 它把文稿层问题解决得很彻底。但一旦问题落到 **代码** 上，这个模型立刻失灵。",

    "Consider a new-hire scenario that the companion blog post opens with {cite}`fanyamin2026deepwiki`: somebody asks *\"where is `runSync` called from?\"*. In a seven-year-old Go repository that sentence has three bad answers and one correct one. The bad answers are:":
        "考虑配套博客 {cite}`fanyamin2026deepwiki` 开篇就用的新人场景：有人问 * “`runSync` 是从哪儿被调用的？” *。在一个七年老的 Go 仓库里，这句话有三个糟糕的回答和一个正确的回答。糟糕的回答是：",

    "`grep -r runSync` — returns every comment, every log-line, every test, every string literal, and every method on an unrelated type that happens to share the name.":
        "`grep -r runSync` —— 每一条注释、每一行日志、每一个测试、每一个字符串字面量，以及任何恰好同名但类型毫无关系的方法，通通返回。",

    "*\"Just read the code.\"* — the senior engineer's answer, and a confession that the codebase has outgrown individual human capacity.":
        "* “你自己看代码吧。” * —— 资深工程师的经典回答，同时也是承认：这份代码库已经超出了一个人脑子能装下的尺度。",

    "Pasting the whole repository into a chat LLM — blows the context window, returns a confidently wrong answer, and provides no traceable citation.":
        "把整个仓库丢进聊天 LLM —— 撑爆上下文、回答得自信却错误，而且没有任何可追溯的引用。",

    "The correct answer is *\"there are five callers, all in `reference-impl/code-kg/service.go`, lines 154, 161, 278, 364, and 376\"* — and to produce that answer at scale a KB must model **code as code**, not as prose. That means parse it into a tree, extract entities, store them with stable identifiers, and remember who calls whom.":
        "正确的回答是 * “总共有 5 个调用方，都在 `reference-impl/code-kg/service.go` 的 154、161、278、364、376 行” * —— 要在规模上可复现地给出这个回答，知识库就必须 **把代码当代码建模**、而不是当成文稿。也就是：解析成语法树、抽取实体、以稳定标识符存储，并记录谁调用了谁。",

    "This chapter explains why that is not optional, surveys the academic literature that has been telling us so for a decade {cite}`allamanis2018survey`, and sets up the five chapters that follow: parsing (ch09), embedding (ch10), graphing (ch11), retrieval (ch12), and generation (ch13).":
        "本章会解释为什么这件事不是可选项，顺手梳理一下学界过去十年一直在提醒我们的那套文献 {cite}`allamanis2018survey`，并为后续五章搭好舞台：解析（第 9 章）、嵌入（第 10 章）、图谱（第 11 章）、检索（第 12 章）与生成（第 13 章）。",

    "What": "What —— 是什么",

    "Three claims from the *naturalness of code* literature {cite}`allamanis2018survey` shape everything in Part III.":
        "* “代码的自然性” * 这一脉文献 {cite}`allamanis2018survey` 中的三条主张，塑造了第三部分的所有设计。",

    "**Claim 1 — Code has structure that prose retrievers discard.** A function is not a bag of words. It has a name, a signature, a docstring, a body, a start-line, an end-line, imports, and — once you have imports — a *call graph*. A `RecursiveCharacterTextSplitter` configured for Markdown will cheerfully cut a Java method into three chunks, severing the signature from its implementation and the implementation from its trailing brace. The resulting embeddings place those chunks in three different regions of vector space. A query for the *method* retrieves some of the fragments, in wrong order, with no way to stitch them back.":
        "**主张 1 —— 代码带有文稿检索器会丢弃的结构。** 一个函数不是词袋。它有名字、签名、docstring、函数体、起始行、结束行、import，而且 —— 一旦有了 import —— 还会有一张 * 调用图 * 。你给 Markdown 配的 `RecursiveCharacterTextSplitter` 会兴高采烈地把一个 Java 方法切成三段，让签名与实现分离，让实现与它的结束花括号分离。切出来的嵌入会把这三段摆在向量空间里三个不同的区域。查询这个 * 方法 * 时，你只能捞到若干碎片、顺序错乱，还没法拼回去。",

    "**Claim 2 — Code search needs exact-match escape hatches that dense retrieval cannot provide on its own.** When the user types `entityID` they expect the function named `entityID` — not the \"semantic neighbours of *entity* and *ID*\". The CodeSearchNet evaluation {cite}`husain2019codesearchnet` made this concrete: early dense-only code searchers lost hard to BM25 {cite}`robertson2009bm25` on queries dominated by identifiers. The fix is hybrid retrieval (ch12), but the prerequisite is still Claim 1 — you must have named entities to rank.":
        "**主张 2 —— 代码搜索需要精确匹配的逃生舱，稠密检索独自做不到。** 当用户输入 `entityID`，他期待的是名为 `entityID` 的那个函数 —— 不是 * “* entity * 和 * ID * 的语义邻居” * 。CodeSearchNet 的评测 {cite}`husain2019codesearchnet` 把这件事钉死了：在以标识符为主的查询上，早期纯稠密代码搜索完败于 BM25 {cite}`robertson2009bm25`。补救办法是混合检索（第 12 章），但前提依然是主张 1 —— 你首先得有命名实体可排。",

    "**Claim 3 — Code has relations that no amount of embedding captures.** Vector space encodes similarity; it does not encode *calls*, *implements*, *imports*, *returns*. Two functions with identical signatures and comments cluster tightly in vector space even when one lives in the HTTP handler layer and the other in the background worker. GraphCodeBERT {cite}`guo2021graphcodebert` showed that injecting data-flow edges into training improves code understanding tasks; our weaker, engineering-grade version of that insight is: if you want to answer *who calls what*, you must build the graph yourself (ch11) — a lesson the DeepWiki methodology {cite}`fanyamin2026deepwiki` pushes hard in §§2 and 6.":
        "**主张 3 —— 代码中存在再多嵌入也捕捉不到的关系。** 向量空间编码相似性，不编码 * 调用 * 、* 实现 * 、* 导入 * 、* 返回 * 。两个签名和注释都一样的函数，即使一个位于 HTTP handler 层、一个位于后台 worker，它们在向量空间里也会紧紧聚在一起。GraphCodeBERT {cite}`guo2021graphcodebert` 证明：把数据流边注入到训练里能显著提升代码理解任务；我们的工程版简化表述是：如果你要回答 * 谁调用了谁 * ，就只能自己建图（第 11 章） —— DeepWiki 方法论 {cite}`fanyamin2026deepwiki` 在 §§2 和 §§6 反复敲这个黑板。",

    "How": "How —— 怎么做",

    "The architectural consequence is a **dual stack**: a vector store for similarity, and a graph store for structure. Both are fed by the same parser, and the parser is the first place the design decisions show.":
        "对应的架构结论就是 **双栈** ：一个向量存储负责相似性，一个图存储负责结构。两者由同一个解析器喂数据，而解析器正是第一个会暴露设计决策的地方。",

    "Part III is organised around the pipeline that the code-layer reference implementation actually runs inside its `Service.runSync` and `runIncrementalSync` methods:":
        "第三部分的组织方式，就照着代码层参考实现在 `Service.runSync` 和 `runIncrementalSync` 里真实跑的那条流水线展开：",

    "Three properties of this stack earn their own chapters later:":
        "这套栈的三项性质稍后各自有专章来展开：",

    "**Stable identity.** The entity ID is a content-free but location-aware hash — `sha256(repoID + filePath + entityType + name + startLine)[:16]`. That choice is what lets Chapter 11's graph survive a re-index and Chapter 14's incremental sync delete-then-insert on `M` without leaving dangling edges.":
        "**稳定身份。** 实体 ID 不依赖内容、但与位置绑定 —— `sha256(repoID + filePath + entityType + name + startLine)[:16]`。正是这个选择，让第 11 章的图谱能挺过重建索引，也让第 14 章的增量同步在处理 `M`（修改）时可以先删后插而不留下悬空边。",

    "**Structured embedding input.** We do not embed the function body. We embed a short, templated header — *Language / Type / Name / Signature / Doc* — because that is what carries the *intent* the user actually queries for. Chapter 10 measures the recall difference.":
        "**结构化嵌入输入。** 我们不嵌入函数体。我们嵌入的是一段短小的模板化表头 —— * Language / Type / Name / Signature / Doc * —— 因为这才是承载了“用户在检索时真正要表达的意图”的那部分。第 10 章会量化两种输入在 recall 上的差距。",

    "**Bounded relation taxonomy.** We ship eight edge types (`CONTAINS`, `IMPORTS`, `CALLS`, `IMPLEMENTS`, `EMBEDS`, `DEPENDS_ON`, `RETURNS`, `ACCEPTS`) and nothing else. Adding a ninth is a design-review-level change — a guardrail that keeps the graph operationally reasonable.":
        "**有界关系集合。** 我们一共交付八种边（`CONTAINS`、`IMPORTS`、`CALLS`、`IMPLEMENTS`、`EMBEDS`、`DEPENDS_ON`、`RETURNS`、`ACCEPTS`），再无其他。加第九种是一次要走设计评审级别的改动 —— 这条护栏让图谱在运维上一直可控。",

    "Every chapter after this one works against a vendored excerpt from the code-layer reference implementation (paths under `reference-impl/code-kg/`), with provenance headers written by `make book-refresh-excerpts` (see `examples/SOURCE.md`).":
        "本章之后的每一章都会基于代码层参考实现的 vendored 代码节选（路径位于 `reference-impl/code-kg/` 下）来展开，节选开头的来源元数据由 `make book-refresh-excerpts` 生成（见 `examples/SOURCE.md`）。",

    "Example": "Example —— 范例",

    "A one-minute demonstration makes the three claims concrete. The inputs are two files, one per layer.":
        "一分钟的演示就能把三条主张落到实处。输入是两份文件，每层一份。",

    "**Prose layer** (Markdown) — `runbook/onboarding.md`:":
        "**文稿层**（Markdown） —— `runbook/onboarding.md`：",

    "**Code layer** (Go) — a minimal `service_sync.go`:":
        "**代码层**（Go） —— 一个最小的 `service_sync.go`：",

    "Ask the prose-layer index (Part II) *\"how do I sync a repo?\"* — you get the runbook back. That's correct; it's what the prose layer is for.":
        "向第二部分的文稿层索引问 * “怎么同步一个仓库？” * —— 你会拿到那份 runbook。这是对的，因为文稿层就是干这个用的。",

    "Now ask the prose-layer index *\"where is `runSync` called from?\"*. You get nothing useful, because:":
        "现在换个问题再问文稿层索引：* “`runSync` 是从哪儿被调用的？” *。你会什么有用的都拿不到，原因是：",

    "No page contains the literal string `runSync` — the runbook uses the CLI name `code-kg sync`, not the Go method name.":
        "没有一篇页面包含字面字符串 `runSync` —— runbook 用的是 CLI 名 `code-kg sync`，而不是 Go 里的方法名。",

    "Even if it did, you'd get prose describing sync, not a list of call sites.":
        "就算某篇包含了，它给你的也是一段讲“同步是什么”的文稿，而不是一张调用点列表。",

    "Finally, ask the code layer the same question. The answer is a list of lines — five lines — each citing `reference-impl/code-kg/service.go` with a `file:line` anchor. That is the artefact Part III teaches you to build.":
        "最后，把同一个问题丢给代码层。回答是一张行级列表 —— 5 条 —— 每条都以 `file:line` 锚点引用了 `reference-impl/code-kg/service.go`。这就是第三部分要教你造的成品。",

    "A reproducible version of this experiment, run against the code-layer reference implementation, appears in Appendix B.":
        "这个实验的可复现版本（跑在代码层参考实现上）见附录 B。",

    "Common mistakes": "常见错误",

    "These are the four design failures we see most often in first-time code-KB builds. Each is the *opposite* of one of the three claims above; the fourth is a scope failure.":
        "下面是我们在“首次搭建代码知识库”的团队里最常见到的四种设计失败。前三个分别是上文三条主张的 * 反面 * ；第四个是 scope 失败。",

    "**1 — Treating code as long prose.** The symptom is a single embedding per file or per \"chunk\" of fixed character length. `RecursiveCharacterTextSplitter(chunk_size=1500)` cuts a Java method into three pieces and places them in three different regions of vector space. The fix is Claim 1 from the *What* section: parse first, then embed one *entity* at a time with a stable identity. The parser (Chapter 9) is what makes this possible; embedding-from-chunk cannot.":
        "**1 —— 把代码当长文稿对待。** 症状是每个文件或者每个固定字符长度的“chunk”只生成一个嵌入。`RecursiveCharacterTextSplitter(chunk_size=1500)` 会把一个 Java 方法切成三段，扔到向量空间的三个不同区域。解决办法就是 * What * 那一节的主张 1：先解析、再按一个 * 实体 * 一个嵌入的方式生成，并给每个实体稳定身份。解析器（第 9 章）是让这件事成为可能的关键；按 chunk 切出来再嵌入做不到。",

    "**2 — Dense-only retrieval.** The symptom is that typing an exact identifier (`entityID`, `runSync`) ranks the real definition below three unrelated neighbours. Embeddings optimise for semantic neighbourhood, and exact identifiers rarely live at the *closest* point in that neighbourhood. The fix is the hybrid retriever of Chapter 12 — BM25-style scoring as either a fallback tier or a fused rank alongside dense retrieval.":
        "**2 —— 仅使用稠密检索。** 症状是：输入一个精确标识符（`entityID`、`runSync`）时，真正的定义会排在三个毫无关系的“邻居”之下。嵌入优化的是语义邻域，而精确标识符很少正好落在那个邻域的 * 最近点 * 。解决办法是第 12 章的混合检索 —— 把 BM25 风格的打分作为兜底层，或者和稠密检索做融合排名。",

    "**3 — Graph-free design.** The symptom is that queries of the form *\"who calls X\"*, *\"what implements Y\"* simply *can't* be asked. Vector space does not encode edges. The industry's attempt to paper over this with larger context windows (*\"just paste the whole repo\"*) scales linearly with codebase size and collapses above roughly 20 kLOC. The fix is Chapter 11: a bounded graph that carries identity + relations, sitting alongside the vector store.":
        "**3 —— 没有图谱的设计。** 症状是 * “谁调用了 X” * 、* “什么实现了 Y” * 这类问题根本 * 问不出来 * 。向量空间不编码边。业界用更大上下文窗口去遮盖这个问题（* “把整个仓库贴进去不就行了” * ）的做法，在代码规模上只能线性扩展，过了大约 20 kLOC 就会塌掉。解决办法是第 11 章：一个承载身份 + 关系的有界图谱，和向量存储并列存在。",

    "**4 — Boiling the ocean.** The symptom is an architecture document that proposes a unified store with a custom embedding, a custom index, and a custom fine-tune — before the team has shipped a single citeable answer. Part III's construction is deliberately boring: tree-sitter + sqlite-vec + Memgraph + one-prompt generator. Start there. Upgrade specific stages (Chapter 15's upgrade matrix) once you have measured what actually moves the retrieval numbers.":
        "**4 —— 想一口气烧开整片海洋。** 症状是：团队还没交付过哪怕一条可引用的答案，架构文档就提出要造一个带自定义嵌入、自定义索引、自定义微调的“统一存储”。第三部分的构造刻意保持乏味：tree-sitter + sqlite-vec + Memgraph + 一个单 prompt 的生成器。就从这里开始。等你量化了哪些指标真正能把检索数据往上抬之后，再按第 15 章的升级矩阵有针对性地升级某个阶段。",

    "Conclusion": "Conclusion —— 小结",

    "Prose retrievers and code retrievers look similar at the API level — both take a query string and return ranked documents — but they fail on different queries and for different reasons. The rest of Part III is a construction proof that a file-based wiki (Part II) plus a four-stage code pipeline (parse / embed / graph / retrieve) covers *both* question classes without needing a single unified store.":
        "文稿检索器和代码检索器在 API 层面长得很像 —— 都是接收一个查询串、返回一串排序后的文档 —— 但它们会在不同的查询上失败，而且失败的原因也不同。第三部分后面的内容，是一次构造性证明：一个基于文件的 wiki（第二部分）加上一条四阶段的代码流水线（解析 / 嵌入 / 图 / 检索），可以 * 同时 * 覆盖两类问题，而无需把它们硬塞进一个统一存储。",

    "Chapter 9 starts at the first stage: parsing.":
        "第 9 章从第一个阶段开始讲：解析。",

    "References": "参考文献",
}


CH09: dict[str, str] = {
    "Chapter 9 — Parsing and Entity Extraction": "第 9 章 —— 解析与实体抽取",

    "This chapter on one page — one entity model, one adapter per language, three pitfalls the parser itself must handle:":
        "本章一图览 —— 一个实体模型、每种语言一个适配器、解析器本身必须处理的三类坑：",

    "You wrote the first version yesterday evening. Sixty lines of regex. `func `, `def `, `class ` — how hard could it be? This morning the indexer emitted 15 000 \"functions\" in a 4 kLOC repo. Half the hits are closure literals inside `map(...)` calls. Three of them are the word `function` inside a string literal. The call graph you built off of those entities is a beautiful fiction: 80 % of the edges point at anonymous `func1`, `func2`, `func3`. Every chapter after this one — embeddings, graph, retrieval, generation — is downstream of what this module emits. **This chapter is about why the parser is the single most leverage-positive component in a code KB, and what a boringly correct one actually looks like.**":
        "昨晚你写了第一版。60 行正则。`func `、`def `、`class ` —— 这能有多难？今天早上索引器在一个 4 kLOC 的仓库里吐出了 15 000 个“函数”。其中一半的命中是 `map(...)` 里的闭包字面量。有 3 个是字符串字面量里那个单词 `function`。你基于这些实体建起来的调用图是一出漂亮的虚构：80% 的边都指向匿名的 `func1`、`func2`、`func3`。本章之后的每一章 —— 嵌入、图谱、检索、生成 —— 都在这个模块的输出下游。**本章讲的是：为什么解析器是代码知识库里“杠杆最大”的一个模块，以及一版“乏味地正确”的解析器具体长什么样。**",

    "Why": "Why —— 为什么",

    "Everything downstream — embeddings (ch10), graph (ch11), retrieval (ch12), answers (ch13) — is a function of what the parser emits. If the parser drops a method, no retriever can find it. If the parser confuses a signature with a body, every embedding is off. The parser is the single most leverage-positive component in a code-KB; it is also the one most likely to be written in a hurry and never touched again.":
        "下游的一切 —— 嵌入（第 10 章）、图谱（第 11 章）、检索（第 12 章）、回答（第 13 章）—— 都是解析器输出的函数。解析器漏了一个方法，任何检索器都找不到它。解析器把签名和函数体搞混了，每一份嵌入都会偏。解析器是代码知识库中杠杆最大的一个模块；它也最容易在赶工时被仓促写完、之后再也没人碰。",

    "A naive parser — \"split on `func ` for Go, `def ` for Python, regex for Java\" — collapses at the first nested generic, first multi-line signature, first anonymous function literal, first heredoc, or first one of several dozen other language-specific eccentricities. The DeepWiki methodology {cite}`fanyamin2026deepwiki` argues (§4) that shipping *one thin extractor per language* on top of a **real** parser is both cheaper and more robust than the grep-shaped alternative.":
        "朴素解析器 —— “Go 按 `func ` 切、Python 按 `def ` 切、Java 靠正则” —— 只要碰上第一个嵌套泛型、第一个多行签名、第一个匿名函数字面量、第一个 heredoc，或者几十种语言特有怪癖中的任何一个，就会当场崩溃。DeepWiki 方法论 {cite}`fanyamin2026deepwiki` 在 §4 明确说：在 * 一个真实的 * 解析器之上，为每种语言写 * 一个薄薄的抽取器 * ，比 grep 风格的替代方案既更便宜也更稳健。",

    "What": "What —— 是什么",

    "Three design decisions define the extraction contract in the code-layer reference implementation's `reference-impl/code-kg/parser` package.":
        "代码层参考实现中 `reference-impl/code-kg/parser` 这个包对抽取契约的定义，由三个设计决策确定。",

    "**1 — One parser, many languages.** Tree-sitter {cite}`brunsfeld_treesitter` gives a uniform parse-tree API over Go, Java, and Python, along with an incremental parsing model and the error-tolerance property that matters in a KB: files that are mid-edit should still produce usable trees. The alternative stack (per-language toolchains: `go/ast`, `javaparser`, `libcst`) triples both dependencies and the surface area of \"one-off bugs\".":
        "**1 —— 一个解析器、多种语言。** Tree-sitter {cite}`brunsfeld_treesitter` 为 Go、Java、Python 提供了统一的语法树 API，附带增量解析模型，以及知识库场景很看重的容错性：一个正在被编辑中的文件，仍然能产出可用的语法树。另一条路（每种语言各自一套工具链：`go/ast`、`javaparser`、`libcst`）会把依赖和“一次性 bug”的表面积都翻三倍。",

    "**2 — A language-neutral intermediate representation.** Whatever tree-sitter emits is collapsed to a `CodeMetadata` struct: a list of files, each with functions and classes, each entity carrying `name`, `start_line`, `end_line`, `signature`, `docstring`, `body`. That IR is small enough to reason about, large enough to feed every downstream stage, and — critically — *language-free*. Chapter 10 embeds it, Chapter 11 graphs it, Chapter 14 diffs it.":
        "**2 —— 一份与语言无关的中间表示。** Tree-sitter 吐出的东西，一律坍缩到一个 `CodeMetadata` 结构：一张文件列表，每个文件下含其函数和类；每个实体带 `name`、`start_line`、`end_line`、`signature`、`docstring`、`body`。这份 IR 小到可被完整地讨论，大到能喂饱每一个下游阶段，而且 —— 关键是 —— * 与语言无关 * 。第 10 章拿它去嵌入，第 11 章拿它建图，第 14 章拿它做差分。",

    "**3 — Supported extensions and skip directories are configured, not inferred.** The parser refuses to walk `vendor/`, `node_modules/`, `.git/`, `__pycache__/`, `dist/`, `build/`, `target/`, `.next/`. Every one of those defaults is a scar from somebody's first run choking on a monorepo. `allamanis2018survey` {cite}`allamanis2018survey` catalogues the same pathology at research scale: most \"big code\" corpora need aggressive vendoring filters before any model survives training.":
        "**3 —— 支持的扩展名和要跳过的目录是“配置”，不是“推断”。** 解析器拒绝深入 `vendor/`、`node_modules/`、`.git/`、`__pycache__/`、`dist/`、`build/`、`target/`、`.next/`。这份默认名单里每一条都来自某次“在 monorepo 上首次运行被噎死”的疤痕。`allamanis2018survey` {cite}`allamanis2018survey` 在学术规模上整理了同一类病症：绝大多数 “big code” 语料在模型训练前都需要一轮激进的 vendor 过滤。",

    "How": "How —— 怎么做",

    "The parser service is 66 lines. Vendored from `reference-impl/code-kg/parser/parser.go` at the commit recorded in the header:":
        "解析器服务一共 66 行。以下代码来自 `reference-impl/code-kg/parser/parser.go`，所属 commit 记录在开头的元数据里：",

    "parser.Service — supported extensions, skip dirs, single Walk.":
        "parser.Service —— 支持的扩展名、要跳过的目录，以及一次 Walk。",

    "Three things are worth naming on that listing:":
        "这段代码上有三点值得点名：",

    "Line-range `26-30` (`supportedExtensions`) is the closed set of file types the KB indexes. Adding a fourth language is a one-line change — and a downstream review obligation, because the tree-sitter grammar must be linked in too.":
        "第 26–30 行（`supportedExtensions`）是知识库会索引的那组**封闭**文件类型。加第四种语言是一行改动 —— 同时也是一项下游评审责任，因为必须把对应的 tree-sitter 语法也链接进来。",

    "Line-range `32-50` (`CollectSupportedFiles`) shows the `filepath.Walk` with the `SkipDir` shortcut. In a 120 k-file monorepo the `node_modules/` branch alone holds 95 % of the inode count; skipping it lazily (before descending) is what makes first sync tolerable.":
        "第 32–50 行（`CollectSupportedFiles`）展示了带 `SkipDir` 短路的 `filepath.Walk`。在一个 12 万文件量级的 monorepo 里，光是 `node_modules/` 这一支就能吃掉 95% 的 inode；在真正下钻之前就“懒惰地”跳过它，是首次同步得以忍受的关键。",

    "`CollectGoFiles` (line 52 in the source) is a legacy alias that has widened over time: it now returns *all* supported files, not just Go. Renames are risky in a library used by many call-sites, so the project leaves the name and adds a new method — a common pattern with clear provenance in the Git blame.":
        "源码第 52 行的 `CollectGoFiles` 是一个随着时间“扩大了职责”的遗留别名：今天它返回的是 * 所有 * 支持的文件，而不只是 Go。在一个已有众多调用点的库里改名风险很高，所以项目保留了这个名字、再加一个新方法 —— 这是一种在 Git blame 里有迹可循的常见模式。",

    "The entity model": "实体模型",

    "The IR that downstream stages consume is the `CodeEntity` struct:":
        "下游各阶段消费的 IR 就是 `CodeEntity` 这个结构体：",

    "CodeEntityType enum plus the canonical CodeEntity record.":
        "CodeEntityType 枚举，加上规范化的 CodeEntity 记录。",

    "Three aspects of that definition have structural consequences:":
        "这份定义中有三个方面会带来结构性的连锁后果：",

    "`EntityType` is a small closed enum (`package`, `file`, `function`, `class`, `struct`, `interface`, `variable`, `constant`). New entity types require a migration; that is a feature, not a bug. See §*Bounded relation taxonomy* in Chapter 11 for the symmetric argument on edges.":
        "`EntityType` 是一个小而封闭的枚举（`package`、`file`、`function`、`class`、`struct`、`interface`、`variable`、`constant`）。新增实体类型需要一次迁移；这是特性，不是 bug。关于边上的对称论证，见第 11 章的 §* Bounded relation taxonomy * 段。",

    "`StartLine` and `EndLine` are first-class fields on every entity. They make the entity ID (Chapter 11) stable across re-indexes, and they let Chapter 13's generator cite results as `file.ext:L12-L47`. Every downstream affordance in the KB ultimately rests on the parser having preserved the original source coordinates.":
        "`StartLine` 和 `EndLine` 是每个实体上的一等字段。它们让实体 ID（第 11 章）在每次重建索引之间保持稳定，也让第 13 章的生成器可以把结果写成 `file.ext:L12-L47` 的形式引用。知识库里每一项下游能力，归根结底都依赖于解析器完整保留了原始源码坐标。",

    "`Body`, `Signature`, and `DocString` are kept separate. The body is truncated to 4 000 characters (in `parseFileForSync`) before being stored, while the signature and docstring are never truncated. That split is the foundation of Chapter 10's *embed-the-header-not-the-body* rule: the signature and docstring survive in full to the embedder; the body survives to the retriever only, truncated.":
        "`Body`、`Signature`、`DocString` 三者分开存放。`Body` 在存入前由 `parseFileForSync` 截断到 4000 字符，而 `Signature` 和 `DocString` 从不截断。这种拆分是第 10 章 * embed-the-header-not-the-body * 规则的基础：签名和 docstring 完整送给嵌入器；函数体只以截断形式送给检索器。",

    "Per-language adapters": "每语言适配器",

    "Tree-sitter emits a syntax tree, not a named-entity list. The conversion lives in a different package (the per-language adapter in `reference-impl/code-kg/rag`, not vendored in this book because it is boilerplate-heavy), but the pattern is short and worth making explicit. For each supported language, one visitor:":
        "Tree-sitter 吐出的是语法树，不是命名实体列表。从语法树到实体列表的转换位于另一个包里（`reference-impl/code-kg/rag` 下的每语言适配器，本书没有把它 vendor 进来，因为模板代码太多），但其模式很短，值得显式写一遍。对每种支持的语言，写一个 visitor：",

    "Walks the tree in pre-order.":
        "前序遍历整棵语法树。",

    "When it sees a node whose kind is in a per-language whitelist — Go `function_declaration`, `method_declaration`, `type_spec` with a `struct_type` or `interface_type`; Python `function_definition`, `class_definition`; Java `method_declaration`, `class_declaration` — it records the entity.":
        "当看到一个节点的 kind 命中当前语言的白名单 —— Go 的 `function_declaration`、`method_declaration`、带 `struct_type` 或 `interface_type` 的 `type_spec`；Python 的 `function_definition`、`class_definition`；Java 的 `method_declaration`、`class_declaration` —— 就记录下这个实体。",

    "Uses the node's source range to fill `StartLine`, `EndLine`, and `Body`.":
        "用节点的源码范围去填 `StartLine`、`EndLine` 以及 `Body`。",

    "Uses preceding doc-comment nodes (if present) as the `DocString`.":
        "如果该节点前面有文档注释节点，就把它们取作 `DocString`。",

    "The discipline is: *one visitor per language, as dumb as possible*. No cross-file resolution (that happens in Chapter 11's graph builder), no symbol tables, no type inference. The tree-sitter grammar carries the language-specific complexity; our code stays small.":
        "纪律是： * 每种语言一个 visitor，尽可能笨 * 。不做跨文件解析（那是第 11 章的图谱 builder 的事）、不维护符号表、不做类型推断。语言特有的复杂度由 tree-sitter 语法来承担；我们自己的代码保持小。",

    "Pitfalls from the field": "来自生产的坑",

    "Three failure modes are worth the reader's attention because they all cost time to diagnose:":
        "下面三种失败模式值得读者特别留意，因为一旦踩上，排查都要花时间：",

    "**Resource leaks.** Tree-sitter trees hold a pointer into a Rust-owned arena and must be freed with `tree.Close()` (or the bindings' equivalent). Forgetting is not an immediate crash; it surfaces later as a slow memory creep under a long-running indexer. `defer tree.Close()` is mandatory.":
        "**资源泄漏。** Tree-sitter 的语法树持有一个指向 Rust 端 arena 的指针，必须用 `tree.Close()`（或对应绑定的等价调用）释放。忘记释放并不会立刻崩 —— 它会在长跑的 indexer 里以缓慢内存上涨的形式浮出水面。`defer tree.Close()` 是强制动作。",

    "**Closures and anonymous functions.** Every language has them, and they *all* show up as \"function-like\" nodes in the parse tree. Emitting them as entities pollutes the graph with hundreds of anonymous nodes called `func1`, `func2`, etc. The fix is a per-language filter: only emit top-level and method-level functions; treat anonymous functions as part of their enclosing entity's body.":
        "**闭包与匿名函数。** 每种语言都有，而它们在语法树里 * 全部 * 表现为“像函数的节点”。把它们作为实体发射出去，会让图谱里挤进几百个叫 `func1`、`func2` 之类的匿名节点。修法是每语言一个过滤器：只发射顶层和方法级函数；把匿名函数当作其外层实体函数体的一部分。",

    "**Generic types and multi-line signatures.** The *signature* we store is the first non-empty line of the body — via the `extractSignature` helper we see again in Chapter 10. For a Go generic like `func Map[K comparable, V any](m map[K]V) []K` that works. For a Java method whose parameters wrap across five lines, it produces a truncated signature. Our fix is to feed the full signature from the tree-sitter node range, not from a naive line-split — see `extractSignature` uses. This is called out as a known bug with a tracked fix.":
        "**泛型与多行签名。** 我们存下来的 * 签名 * 是函数体的第一行非空行 —— 用的是第 10 章也会再次见到的 `extractSignature` 工具函数。对 `func Map[K comparable, V any](m map[K]V) []K` 这样的 Go 泛型，这样做没问题；但对参数折成五行的 Java 方法，它只能给出被截断的签名。我们的修法是改成把 tree-sitter 节点的完整范围喂给签名提取，而不是简单按行切 —— 参见 `extractSignature` 的各处调用。这个问题被登记为一个有追踪的已知 bug。",

    "Common mistakes": "常见错误",

    "Three additional anti-patterns come up whenever a team tries to short-cut the parser stage. Each is *tempting* because it seems cheaper up front, and each pays back the cost 10x downstream.":
        "每当团队试图在解析器阶段抄近道，下面这三种反模式就会冒出来。每一个在前期看起来都 * 挺诱人 * 的，因为好像省事；每一个在下游都会以 10 倍代价偿还。",

    "**1 — \"Regex is enough for MVP.\"** The symptom is a one-line identifier regex — `/func\\s+(\\w+)/` — emitting 15 000 entities in a 4 kLOC repo. Comments match. String literals containing the word `function` match. The test harness's `describe(\"function X\", ...)` matches. The regex is not *approximately* a parser — it is a completely different function. Every chapter downstream (embeddings, graph, retrieval) inherits the noise and amplifies it. Use a real parser (tree-sitter, language-server, compiler frontend) from the first commit. It is not the slow path.":
        "**1 —— “MVP 用正则就够了”。** 症状是一行识别符正则 —— `/func\\s+(\\w+)/` —— 在一个 4 kLOC 的仓库里吐出 15 000 个实体。注释也命中。包含单词 `function` 的字符串字面量也命中。测试框架里的 `describe(\"function X\", ...)` 也命中。正则不是 * 近似 * 的解析器 —— 它是一个完全不同的函数。每一个下游章节（嵌入、图谱、检索）都会继承并放大这些噪声。从第一次提交起就用真正的解析器（tree-sitter、语言服务、编译器前端）。它不是那条慢路径。",

    "**2 — Unstable entity IDs.** The symptom is that re-running the indexer on an unchanged repo produces a diff in your vector store. Why? The `id` was constructed from `filepath + name`, or from a hash that included the full body (so whitespace edits cascade), or it contained an auto-increment counter. The graph's edges then point at IDs that no longer exist. The fix is the scheme of Chapter 10: `sha256(repoID + filePath + entityType + name + startLine)[:16]`. Stable across re-index, but sensitive enough that moving a function to a new line produces a new ID (which is correct behaviour).":
        "**2 —— 不稳定的实体 ID。** 症状是：在一个没改过的仓库上重跑 indexer，你的向量存储居然出现了 diff。为什么？因为 `id` 是 `filepath + name` 拼的，或者是一个把完整函数体一起哈希进去的 hash（于是一次空白改动就会级联），或者它里面干脆带了一个自增计数器。这样一来，图谱的边就会指向已经不存在的 ID。解决办法是第 10 章的方案：`sha256(repoID + filePath + entityType + name + startLine)[:16]`。在重建索引之间稳定；但又敏感到：把一个函数挪到新的一行就会产生新 ID（这正是正确行为）。",

    "**3 — Emitting \"too clever\" entity types.** The symptom is a parser that emits 23 entity kinds — `struct-field`, `enum-variant`, `type-alias`, `const-declaration`, … — and a retrieval layer that now has to reason about which kinds to mix. Cardinality explodes, ranking signals dilute, and the graph's node types outgrow any reasonable visualisation. Start with the four of Chapter 9 — `package`, `type`, `method`, `function` — even for Java where \"interface\" feels different from \"class.\" You can always refine later; you cannot un-emit an entity type that is already baked into 200 downstream rules.":
        "**3 —— 吐出“过于聪明”的实体类型。** 症状是：一个解析器吐出了 23 种实体 —— `struct-field`、`enum-variant`、`type-alias`、`const-declaration` —— 然后检索层开始要琢磨“到底哪些类型可以混在一起排”。基数爆炸，排序信号被稀释，图谱的节点类型多到画不下任何像样的可视化。就从第 9 章的四种开始 —— `package`、`type`、`method`、`function` —— 哪怕是 Java（虽然“interface”感觉和“class”不一样）。你随时可以以后再细化；但你没法把一个已经被嵌进下游 200 条规则的实体类型“撤回”。",

    "Example": "Example —— 范例",

    "A reproducible four-line demonstration, run against the code-layer reference implementation itself:":
        "四行命令就能在代码层参考实现自身上复现一次演示：",

    "On the commit used for this chapter's excerpts, the output is:":
        "在本章节选对应的 commit 上，输出如下：",

    "The ratio matters more than the absolute numbers: a healthy Go codebase is function-heavy. If you see 5 000 \"functions\" on a 50 kLOC Java repo, your parser is treating every closure as an entity — go fix the visitor.":
        "比例比绝对数字更重要：一个健康的 Go 代码库是“函数密集”的。如果你在一个 50 kLOC 的 Java 仓库上看到 5000 个“函数”，那就是你的解析器把每个闭包都当成了实体 —— 去修那个 visitor。",

    "Conclusion": "Conclusion —— 小结",

    "The parser is small, but everything in Part III depends on three contracts it establishes: a uniform IR across languages (Claim 1), faithful source coordinates on every entity (Claim 2), and an aggressive default skip-list for vendored directories (Claim 3). Break any of the three and every downstream chapter breaks with it.":
        "解析器很小，但第三部分的每一层都靠它立下的三条契约活着：跨语言统一的 IR（主张 1）、每个实体都忠实保留源码坐标（主张 2）、以及对 vendor 目录的激进默认跳过名单（主张 3）。这三条哪一条破了，下游每一章也跟着破。",

    "Chapter 10 takes the IR as input and turns the *identity* half of each entity (language, type, name, signature, docstring) into a vector — the part, famously, where most code-RAG tutorials go wrong.":
        "第 10 章把这份 IR 作为输入，把每个实体的 * 身份 * 那一半（语言、类型、名字、签名、docstring）变成一个向量 —— 这也正是众所周知、大多数 code-RAG 教程会走偏的那一段。",

    "References": "参考文献",
}


CH10: dict[str, str] = {
    "Chapter 10 — Embeddings and Vector Stores": "第 10 章 —— 嵌入向量与向量存储",

    "This chapter on one page — three contracts, one decision matrix, one theory anchor, four mistakes:":
        "本章一图览 —— 三份契约、一份决策矩阵、一处理论锚点、四类典型错误：",

    "You follow the first tutorial you find. You embed every function body with `text-embedding-3-small`. 412 vectors land in pgvector. The demo works on the query you rehearsed. Then the user types *\"where do we retry embedding calls\"* and the top hit is a completely unrelated helper whose body happens to contain the words `retry` and `embedding` inside a comment. The right answer — `GenerateEmbeddings`, the actual retry loop — ranks eleventh. You double the model size. Recall@10 moves from 0.60 to 0.63. **This chapter is about why you cannot fix a code-embedding problem by spending more on the model, and what the cheap, boring fix looks like instead.**":
        "你按你搜到的第一份教程做。你用 `text-embedding-3-small` 把每一个函数体都嵌入一遍。412 条向量落进 pgvector。在你预演过的那条查询上 demo 表现良好。然后用户输入 * “where do we retry embedding calls” * ，排第一的命中是一个毫不相关的小工具函数，它的函数体里恰好在注释里写了 `retry` 和 `embedding` 两个词。真正正确的答案 —— `GenerateEmbeddings`，真正的重试循环 —— 排在第 11 位。你把模型规模翻倍。Recall@10 从 0.60 动到 0.63。**本章讲的是：为什么你没法用“在模型上多砸钱”来修一个代码嵌入问题；以及那个又便宜又乏味的修法长什么样。**",

    "Why": "Why —— 为什么",

    "An embedding is a cheap, lossy summary of an entity that lives in a vector space where similarity ≈ cosine distance. Two decisions dominate whether those summaries are useful for a code KB: *what you embed* and *where you store the vector*. Both are routinely gotten wrong.":
        "嵌入向量是实体的一份廉价有损摘要，存在于一个“相似度 ≈ 余弦距离”的向量空间里。对代码知识库来说，这份摘要好不好用由两个决定主导： * 你嵌入的是什么 * ，以及 * 向量存在哪里 * 。这两件事业界大多数人都做错了。",

    "The typical mistake, inherited from prose-RAG tutorials, is to embed *the function body*. Bodies are noisy: they carry irrelevant local variable names, implementation details that rotate weekly, and, in statically typed languages, whole blocks of boilerplate (error wrapping, logging, trivial pass-throughs) that have almost no signal about what the function *does*. The DeepWiki methodology {cite}`fanyamin2026deepwiki` (§5) and the CodeSearchNet evaluation {cite}`husain2019codesearchnet` both land on the same prescription: embed the **structured identity** of the entity — its language, type, name, signature, and doc-comment — and keep the body as a secondary retrieval artefact.":
        "最典型的错误，继承自讲 prose-RAG 的教程，就是去嵌入 * 函数体 * 。函数体是很吵的信号：里面有大量无关的局部变量名、每周都在轮换的实现细节；在静态类型语言里，还塞着大段大段几乎不能说明“这个函数到底在做什么”的样板代码（错误包装、日志、一行的 pass-through）。DeepWiki 方法论 {cite}`fanyamin2026deepwiki`（§5）和 CodeSearchNet 的评测 {cite}`husain2019codesearchnet` 最终落在同一条处方上：去嵌入实体的 **结构化身份** —— 它的语言、类型、名字、签名和文档注释 —— 把函数体作为 * 次级的 * 检索物料留着。",

    "The storage decision is equally loaded. The field has converged on approximate-nearest-neighbour search via HNSW {cite}`malkov2020hnsw` as the default algorithm, but the question of *which* store to deploy depends on whether you are a single user indexing a laptop's worth of repos, a team sharing an index, or a scale-out SaaS. We run three shortlisted options through a decision matrix and land on sqlite-vec {cite}`sqlite_vec` for the code-layer reference implementation's default config, with pgvector {cite}`pgvector` and Milvus {cite}`milvus` as documented upgrade paths.":
        "存储选型同样不轻松。领域已经收敛到“用 HNSW {cite}`malkov2020hnsw` 做近似最近邻”作为默认算法，但具体 * 选哪一种存储 * ，要看你是“一个人在笔记本上索引几个仓库”、“一个团队共用一个索引”，还是“要横向扩展的 SaaS”。我们用一份决策矩阵过了三个候选，最终在代码层参考实现的默认配置里选了 sqlite-vec {cite}`sqlite_vec`，把 pgvector {cite}`pgvector` 和 Milvus {cite}`milvus` 写进文档作为升级路径。",

    "What": "What —— 是什么",

    "Three contracts define Chapter 10.": "第 10 章由三份契约定义。",

    "**1 — Structured input template.** The embedder receives a fixed five-line string per entity:":
        "**1 —— 结构化输入模板。** 嵌入器收到的是每个实体固定五行的字符串：",

    "The rules that matter:": "关键规则：",

    "Same order, same labels, every time — the embedder sees identical prefixes on every record, which makes intra-corpus comparisons stable.":
        "每次都用相同顺序、相同标签 —— 嵌入器在每条记录上看到完全一致的前缀，这样语料内部的比较才稳定。",

    "The signature is **trimmed to its first source line**; multi-line signatures are collapsed. `extractSignature` in Chapter 9 is the implementation.":
        "签名会被 **裁到源码里的第一行** ；多行签名会被折叠。实现见第 9 章的 `extractSignature`。",

    "The doc is the docstring as parsed by tree-sitter, *not* the full comment block preceding the entity. Inline comments inside the body never make it into the embedding input.":
        "`doc` 取的是 tree-sitter 解析出来的 docstring，* 不是 * 实体之前那段完整的注释块。函数体内部的行内注释永远进不了嵌入输入。",

    "The body is **omitted on purpose**. It is persisted, truncated to 4 000 characters, on the entity row and used only by the retriever and the generator.":
        "函数体 **是故意省略的** 。它会以截断到 4000 字符的形式存在实体行上，只给检索器和生成器用。",

    "**2 — Batch + backoff + rate-limit.** Embedding APIs are slow, metered, and flaky. The enricher wraps three primitives around every call: batch size (default 50 — set in `CODE_KG_EMBEDDING_BATCH_SIZE`), exponential backoff (base 500 ms, `maxRetries` attempts), and an optional per-minute rate limit that sleeps to keep the caller under a configured RPS.":
        "**2 —— 批量 + 退避 + 限速。** 嵌入 API 又慢、又按量计费、又容易抖动。enricher 在每次调用外面包了三件基本装备：批大小（默认 50，由 `CODE_KG_EMBEDDING_BATCH_SIZE` 控制）、指数退避（初始 500 ms，最多 `maxRetries` 次），以及一个可选的按分钟限速器，用 sleep 把调用方压在配置好的 RPS 之下。",

    "**3 — Store choice is a decision matrix.** Three dimensions: *how many users share one index*, *how many vectors do you expect at steady state*, and *what's the operational cost you're willing to pay*.":
        "**3 —— 存储选择是一份决策矩阵。** 三个维度： * 共享一个索引的用户数 * 、* 稳态下预期的向量数量 * 、* 你愿意承担的运维成本 * 。",

    "Store": "存储",
    "When to choose": "何时选择",
    "Pain point": "痛点",
    "`sqlite-vec` {cite}`sqlite_vec`": "`sqlite-vec` {cite}`sqlite_vec`",
    "Single-user / IDE-embedded / ≤ 1 M vectors": "单用户 / 嵌入 IDE / ≤ 1 M 向量",
    "No multi-writer; no HA": "不支持多写；没有 HA",
    "`pgvector` {cite}`pgvector`": "`pgvector` {cite}`pgvector`",
    "Team deployment on existing Postgres; ≤ 50 M vectors": "团队部署、复用已有 Postgres；≤ 50 M 向量",
    "HNSW index rebuild blocks writes briefly": "HNSW 索引重建会短暂阻塞写入",
    "`Milvus` {cite}`milvus`": "`Milvus` {cite}`milvus`",
    "Dedicated vector service; ≥ 10 M vectors + multi-tenant": "专用向量服务；≥ 10 M 向量 + 多租户",
    "Operational complexity; separate cluster": "运维复杂度高；需要独立集群",

    "The code-layer reference implementation ships `sqlite-vec` because its target user is a developer running the KB locally alongside their editor. The production-scale choices above are explicitly supported via the `pgvector.Store` interface — see the §*Why an interface* note in the *How* section.":
        "代码层参考实现默认发的是 `sqlite-vec`，因为它面向的是“把知识库和编辑器一起在本地跑着”的开发者。上面那两个更大规模的选项通过 `pgvector.Store` 这个接口被显式支持 —— 见 * How * 段里的 §* Why an interface * 小节。",

    "Theory anchor: bi-encoders, cross-encoders, HNSW":
        "理论锚点：bi-encoder、cross-encoder 与 HNSW",

    "Before the *How*, the two ideas that underpin everything this chapter does, so that the practical choices don't read as arbitrary.":
        "在进入 * How * 之前，先点两个概念 —— 本章所有实践选择的底层支撑都来自这两个概念，这样那些选择读起来才不会像是拍脑袋。",

    "**Bi-encoder vs cross-encoder.** The embedding model we call is a *bi-encoder*: query and document are encoded *independently* into a vector each, and retrieval is cosine similarity between them {cite}`reimers2019sbert`. The independence is the whole point — a document's embedding can be computed *once* at index time and reused for every future query. A *cross-encoder* encodes the (query, document) pair *together*, which gives consistently higher ranking quality {cite}`nogueira2019passage` — and which costs one model invocation *per candidate* at query time, so it is unusable as primary retrieval. The book's Chapter 15 discusses the upgrade path: bi-encoder for primary retrieval, cross-encoder for top-k re-ranking. Knowing this shape is what makes the cost of re-ranking predictable.":
        "**Bi-encoder vs cross-encoder。** 我们调用的嵌入模型是一种 * bi-encoder * ：query 和 document 被 * 独立地 * 各自编成一个向量，检索时算两者之间的余弦相似度 {cite}`reimers2019sbert`。这种独立性本身就是它最大的价值 —— 一份文档的嵌入可以在索引阶段 * 算一次 * ，然后被之后任何一次查询反复复用。* cross-encoder * 则把 (query, document) 这个对 * 一起 * 送进模型编码，可以稳定地给出更好的排序质量 {cite}`nogueira2019passage` —— 代价是：每个候选都需要一次模型调用，所以它不能作为首轮检索使用。本书第 15 章会讨论升级路径：bi-encoder 作为首轮检索，cross-encoder 只对 top-k 做重排。先把这个形状搞清楚，重排的成本就可预测了。",

    "**HNSW and why vector search is logarithmic.** The three stores named above do *not* compare the query against every stored vector. They build a Hierarchical Navigable Small-World graph {cite}`malkov2018hnsw`: a layered graph where long-range links at upper layers enable rapid \"zoom-in,\" and dense short-range links at the base layer give precise local navigation. An approximate nearest-neighbour query runs in time roughly logarithmic in the number of vectors, not linear. Two operational consequences fall out of this directly: (a) inserts are more expensive than reads (a new vector must be woven into the graph at every layer), which is why the reference implementation's enricher is *async* and *idempotent*; and (b) recall is a tunable parameter, not a binary property, which is why every vector DB exposes an `efSearch`-type knob. Chapter 10 does not *tune* that knob, but knowing the knob exists is how you later trade 10 % recall for 3x latency when a user reports the search is slow.":
        "**HNSW 以及“为什么向量搜索是对数复杂度”。** 上文三种存储 * 都不会 * 把查询和每一条存储向量挨个比较。它们构建的是一个 Hierarchical Navigable Small-World 图 {cite}`malkov2018hnsw`：一个分层图，上层的长程链接用来快速“拉远视野找到大致方向”，底层的密短程链接负责精确的局部导航。一次近似最近邻查询的运行时间，大约与向量数成对数关系，而不是线性关系。由此直接带来两个运维影响：（a）写入比读取更贵（一个新向量必须被织进每一层的图），所以参考实现的 enricher 必须是 * 异步 * 并且 * 幂等 * 的；（b）recall 是一个可调参数，不是二元属性，所以每一种向量数据库都会暴露一个类似 `efSearch` 的旋钮。第 10 章不会去 * 调 * 这个旋钮，但事先知道“这个旋钮存在”，是你将来在“用户说搜索变慢了”的时候，能拿 10% recall 换 3x 延迟的前提。",

    "How": "How —— 怎么做",

    "The enricher (the layer that owns the embedding model) is 128 lines. Vendored from `reference-impl/code-kg/enricher/service.go`:":
        "enricher（拥有嵌入模型的那一层）一共 128 行。以下代码来自 `reference-impl/code-kg/enricher/service.go`：",

    "enricher.Service — embedder/summarizer interfaces and configuration.":
        "enricher.Service —— embedder/summarizer 接口与配置。",

    "Two `interface`s (lines 12–19) are what make the storage decision above negotiable. `Embedder` abstracts the vendor; `Summarizer` is an optional side-channel that lets you swap in an LLM-generated doc-comment when the source doesn't have one. Both are satisfied by `rag.EmbeddingService` in the default wiring.":
        "第 12–19 行的两个 `interface` 就是让上面那份存储决策“可谈判”的关键。`Embedder` 抽象掉了供应商；`Summarizer` 是一个可选的旁路，允许你在源码本身没有文档注释时，用一个 LLM 生成的 doc-comment 顶上。默认接线里两者都由 `rag.EmbeddingService` 实现。",

    "The retry + rate-limit discipline, in the loop that does the actual API call:":
        "在真正发起 API 调用的那个循环里，“重试 + 限速”纪律如下：",

    "Batch embedding with exponential backoff — every hosted API needs this.":
        "带指数退避的批量嵌入 —— 每一种托管 API 都需要这一套。",

    "Line 81 is the backoff formula: `retryBaseMs * 2^i`. With defaults (`retryBase = 500 ms`, `maxRetries = 3`) that's `500, 1000, 2000` ms between attempts — enough to survive the brief provider hiccups that CodeSearchNet-scale indexing runs hit approximately every few thousand batches, and short enough that a genuinely-broken provider fails the whole sync fast.":
        "第 81 行是退避公式：`retryBaseMs * 2^i`。默认值（`retryBase = 500 ms`、`maxRetries = 3`）下，重试之间的间隔是 `500、1000、2000` ms —— 足够撑过 CodeSearchNet 规模索引跑每几千批会遇到的短暂供应商抖动，又短到一旦供应商真正坏了能快速让整次同步失败。",

    "The embedding-input builder is a one-liner worth calling out:":
        "嵌入输入的 builder 是一行小函数，但值得点出来：",

    "The five-line structured template that replaces raw function bodies.":
        "替代“裸函数体”的那份五行结构化模板。",

    "`BuildEntityInput` is called once per entity inside `Service.generateAndStoreEmbeddings`, which in turn batches 50 entities at a time and persists the resulting vectors with the **same ID** that the graph node (Chapter 11) and the entity row (Chapter 9) share:":
        "`BuildEntityInput` 会在 `Service.generateAndStoreEmbeddings` 里对每个实体调一次；这个方法本身再按 50 个一批地组织调用，并用 **和图谱节点（第 11 章）以及实体行（第 9 章）完全相同的 ID** 把得到的向量持久化下来：",

    "The `Upsert(ID, vector)` call is what makes the same sqlite row addressable from the entity store, the vector store, and the graph store in exact equivalence — Chapter 11 depends on this.":
        "`Upsert(ID, vector)` 这次调用，正是让“同一条 sqlite 行”能在实体存储、向量存储、图谱存储三者里以完全等价的 ID 被寻址的关键 —— 第 11 章依赖这一点。",

    "Why an interface?": "为什么要搞一层接口？",

    "`pgvector.Store` is the interface type. The default implementation is backed by sqlite-vec via the `sqlite_vec` Go bindings (bound in `Service.NewService`):":
        "`pgvector.Store` 是接口类型。默认实现借 `sqlite_vec` 的 Go 绑定落在 sqlite-vec 上（在 `Service.NewService` 里完成接线）：",

    "The package name is historical: the author prototyped with Postgres + pgvector first, then switched to sqlite-vec for distribution simplicity. The interface survived. To swap in real pgvector you write one additional implementation (120-ish lines) and change one line in `NewService`. That is the intended upgrade path.":
        "包名来自历史：作者最早用 Postgres + pgvector 做原型，后来为了分发简单切到了 sqlite-vec。接口存活了下来。要换回真正的 pgvector，你需要再写一份实现（大概 120 行），并在 `NewService` 里改一行。这就是预期中的升级路径。",

    "Measured: embedding body vs embedding the template":
        "实测：嵌入函数体 vs 嵌入模板",

    "We ran a small side-experiment on the code-layer reference implementation's own corpus: same 1 624 Go/Python entities, two embedding passes, one over the raw body truncated at 4 000 chars, one over `BuildEntityInput`'s template. Then 40 hand-labelled natural-language queries from the companion repo's issue tracker (\"how do I register a new repo\", \"where is sync retried\", …). Recall@10 with OpenAI `text-embedding-3-small` {cite}`openai_embeddings_v3`:":
        "我们在代码层参考实现自己的语料上跑了一个小对照实验：同一份 1624 个 Go/Python 实体，做两轮嵌入 —— 一轮针对截断到 4000 字符的裸函数体，一轮针对 `BuildEntityInput` 的模板。然后用 40 条从配套仓库 issue tracker 人工标注出来的自然语言查询（“怎么注册一个新仓库”、“同步是在哪里重试的”……）。在 OpenAI `text-embedding-3-small` {cite}`openai_embeddings_v3` 上的 Recall@10：",

    "Input": "输入",
    "Recall@10": "Recall@10",
    "Body (truncated)": "函数体（截断）",
    "0.62": "0.62",
    "Structured": "结构化",
    "0.81": "0.81",

    "The 19-point gap is the price of embedding the boilerplate along with the signal. The same gap was independently reported by CodeSearchNet's dense baselines {cite}`husain2019codesearchnet` and is the empirical reason this book insists on the five-line template. The parallel free-weight alternative we spot-checked — BGE `bge-base-en-v1.5` {cite}`xiao2024bge` — retained a smaller but still real gap (0.58 → 0.74), so the lesson is not provider-specific.":
        "这 19 个百分点的差距，就是“把样板代码和信号一起嵌入”所付的代价。CodeSearchNet 的稠密基线 {cite}`husain2019codesearchnet` 独立报出过相同的差距；这也是本书坚持那份五行模板的经验依据。我们抽查的开源权重替代品 —— BGE `bge-base-en-v1.5` {cite}`xiao2024bge` —— 上的差距变小但仍然真实（0.58 → 0.74），所以这个结论不是某一家厂商专属的。",

    "Common mistakes": "常见错误",

    "These are the four embedding anti-patterns that most reliably turn a promising code-KB into a mediocre one.":
        "下面四个嵌入反模式，最能把一个有潜力的代码知识库拖成一个平庸的项目。",

    "**1 — Embedding raw function bodies.** The symptom is that two unrelated helpers with similar control flow (for-loop + try/except + return) rank each other as nearest neighbours. Bodies are dominated by syntactic boilerplate. The measured hit — ~33 % recall@10 (bodies) vs ~67 % recall@10 (identity) on the reference corpus — is not a tuning delta, it's a design delta. Embed the template *\"Language: Go. Type: method. Name: RunSync. Signature: ... . Doc: ...\"*.":
        "**1 —— 嵌入裸函数体。** 症状是：两个毫无关系的小工具函数（都写成 for-loop + try/except + return）互相把对方排成最近邻。函数体被语法样板主导。在参考语料上实测到的差距 —— 函数体约 33% recall@10 对身份约 67% —— 不是调参能填的差，是设计层面的差。改成嵌入那份模板： * “Language: Go. Type: method. Name: RunSync. Signature: ... . Doc: ...” * 。",

    "**2 — No batching or backoff.** The symptom is that the first indexer run works, the second run hits 429s and dies halfway through 5 000 entities, and re-running wastes 3 000 already-computed embeddings because there was no checkpoint. The fix is the boring triangle: batch (50–100 inputs), bounded concurrency, exponential backoff, persisted-per-entity so re-run is idempotent. Every embedding API in production tightens rate limits over time; write this defensively on day one.":
        "**2 —— 不做批量也不做退避。** 症状是：第一次跑 indexer 成功，第二次撞上 429，在 5000 个实体处死掉一半；再跑一次又白白浪费掉 3000 条已经算好的嵌入，因为没有 checkpoint。修法就是那个乏味的三角形：批量（50–100 条）、有限并发、指数退避，并按每个实体持久化，使得重跑天然幂等。生产上任何嵌入 API 的限速都会随时间变严；这一层从第一个提交就要防御性地写好。",

    "**3 — Choosing a vector DB before you know your corpus size.** The symptom is a Kubernetes operator, a Milvus cluster, and six hours of YAML — for 3 800 entities. Below 50 k entities, `sqlite-vec` (or `pgvector` if you already run Postgres) is both faster *and* simpler than a dedicated vector database. Scale *horizontally when measured*, not when anticipated. The Chapter 15 upgrade-matrix gives the exact thresholds.":
        "**3 —— 在还不了解语料规模之前就选向量数据库。** 症状是：一个 Kubernetes operator、一个 Milvus 集群、六个小时的 YAML —— 只为了 3800 个实体。50 k 实体以下，`sqlite-vec`（若你已经在用 Postgres 就换 `pgvector`）比专用向量数据库 * 既更快也更简单 * 。* 在被量化证明需要的时候 * 再横向扩容，而不是“我估计会需要”。第 15 章的升级矩阵会给出具体阈值。",

    "**4 — Mixing embedding models mid-flight.** The symptom is a search that returns a mix of `v1` and `v3` vectors because someone upgraded the embedding model and forgot to re-index. Cosine similarity across different model families is meaningless. Either pin the model and re-index on deliberate upgrades, or store the model name *on each vector* and filter retrieval by model. The fix is cheap if you plan for it; the failure mode is silent and nearly impossible to debug after the fact.":
        "**4 —— 半路混用嵌入模型。** 症状是：搜索返回了 `v1` 和 `v3` 向量的混合，因为有人把嵌入模型升级了却忘记重建索引。不同模型家族之间的余弦相似度毫无意义。要么把模型钉死，在有意升级时重建索引；要么 * 在每条向量上都存一个模型名 * ，并在检索时按模型过滤。提前计划好就很便宜；一旦发生了再想排查就非常难。",

    "Example": "Example —— 范例",

    "A three-command reproduction against the running reference implementation:":
        "在运行中的参考实现上跑这三条命令即可复现：",

    "If step 1 is omitted, the sync still completes — the enricher becomes `unavailable` and Chapter 12's retriever falls back to keyword-only. That is the intended degrade path.":
        "如果第 1 步省略，同步依然会完成 —— enricher 会进入 `unavailable` 状态，第 12 章的检索器降级为仅关键词。这正是预期的降级路径。",

    "Conclusion": "Conclusion —— 小结",

    "Embeddings are the single line item in a code-KB that most easily turns operational money into retrieval quality. Two rules buy the most improvement: embed the *identity* of the entity, not its body; and keep the storage choice flexible behind a narrow interface. Chapter 11 takes the *other* half of each entity — its relationships — and builds a graph out of them.":
        "在代码知识库的所有预算科目里，嵌入是那一项最容易把“运营预算”转化为“检索质量”的。两条规则能带来最多的改进：嵌入实体的 * 身份 * 而不是它的函数体；把存储选型藏在一个窄接口后面、保持可替换。第 11 章会处理每个实体的 * 另一半 * —— 它的关系 —— 并用它们建起一张图。",

    "References": "参考文献",
}


def apply(batch_name: str, translations: dict[str, str]) -> tuple[int, int, list[str]]:
    """Apply translations to the matching .po file. Returns (applied, missing,
    unmatched_msgids_list)."""
    po_path = os.path.join(LOCALE_ROOT, f"{batch_name}.po")
    if not os.path.exists(po_path):
        raise FileNotFoundError(po_path)
    po = polib.pofile(po_path)
    applied = 0
    unmatched: list[str] = []
    for e in po:
        if e.msgid in translations:
            e.msgstr = translations[e.msgid]
            if "fuzzy" in e.flags:
                e.flags.remove("fuzzy")
            applied += 1
    # Missing = translations supplied but not found in po
    po_msgids = {e.msgid for e in po}
    for key in translations:
        if key not in po_msgids:
            unmatched.append(key)
    po.save(po_path)
    untrans_after = len(po.untranslated_entries()) + len(po.fuzzy_entries())
    return applied, untrans_after, unmatched


def main() -> int:
    batches = [
        ("index", INDEX),
        ("ch08-why-code-is-not-prose", CH08),
        ("ch09-parsing-and-entity-extraction", CH09),
        ("ch10-embeddings-and-vector-stores", CH10),
    ]
    for name, d in batches:
        applied, remaining, unmatched = apply(name, d)
        print(f"{name:45s} applied={applied:3d}  remaining_untranslated={remaining:3d}  unmatched_keys={len(unmatched)}")
        for key in unmatched:
            print(f"   UNMATCHED: {key[:80]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
