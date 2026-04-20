"""Chinese translations for source/part2-prose-layer/index.md.

See source/_tools/translations/ch02-ir-rag-primer.zh.py for the full
style guide. Part II conventions follow Part I's:

- CLI, ADR, Git, YAML, Markdown, toctree, gettext, Diátaxis,
  Sphinx, MyST, BM25 kept in English.
- "prose-layer reference implementation" -> "文稿层参考实现"
  (the redacted stand-in the book uses for the author's private
  file-based wiki project).
- "wiki" is kept in English because it is a product category term
  (like "CMS" or "ORM") rather than a translatable concept.
- CommonMark CJK emphasis rule still applies — see the Part I
  style guide.
"""

PO_PATH = "part2-prose-layer/index.po"

TRANSLATIONS: dict[str, str] = {
    "Part II — The Prose Layer": "第二部分 —— 文稿层",
    (
        "The five chapters of Part II, on one page — a storage "
        "choice (Ch 4) whose trust properties (Ch 5) the pipeline "
        "(Ch 6) must preserve, served through search and a static "
        "site (Ch 7), with an operational model (Ch 7a) that keeps "
        "the whole thing honest as the code underneath changes:"
    ): (
        "第二部分的五章，浓缩在一页："
        "一个**存储选型**（第 4 章），"
        "它的**信任属性**（第 5 章）必须被**流水线**（第 6 章）一路保住，"
        "经由搜索和静态站点（第 7 章）对外服务，"
        "再加上一套**运维模型**（第 7a 章）—— "
        "在底下的代码持续变化时，让整套东西仍然是诚实的："
    ),
    "Why": "为什么",
    (
        "Human-authored prose — tutorials, how-tos, runbooks, ADRs — "
        "is the oldest layer of a software KB and the one machines "
        "cannot produce on their own. Part II shows how the "
        "prose-layer reference implementation keeps that layer "
        "trustworthy, searchable, and automatable without locking "
        "the content into a proprietary system — and how to keep it "
        "correct over time."
    ): (
        "人写的文稿 —— 教程、how-to、runbook、ADR —— "
        "是软件知识库最古老的那一层，"
        "也是唯一机器没办法凭空生成的那一层。"
        "第二部分展示的是：文稿层参考实现如何让这一层"
        "**可信、可搜、可自动化**，"
        "同时不把内容锁死在某个专有系统里 —— "
        "以及如何让它**随时间推移仍然正确**。"
    ),
    "What": "是什么",
    (
        "A file-based wiki (Chapter 4), YAML frontmatter + footer "
        "as the two-block provenance-and-review record (Chapter 5), "
        "the classification pipeline (Chapter 6), publishing and "
        "in-memory search (Chapter 7), and an operational model for "
        "keeping the prose correct as the code underneath it "
        "changes (Chapter 7a)."
    ): (
        "一个基于文件的 wiki（第 4 章），"
        "由 YAML frontmatter 加 footer 组成的双块"
        "「来源 + 评审」记录（第 5 章），"
        "分类流水线（第 6 章），"
        "发布与内存搜索（第 7 章），"
        "以及一套在底下的代码持续变化时、"
        "仍让文稿保持正确的**运维模型**（第 7a 章）。"
    ),
    "How": "怎么做",
    (
        "Five chapters. Chapters 4–7 handle *getting prose in*. "
        "Chapter 7a closes Part II with the four-corner operational "
        "model (opinionated page set, metadata footer, three-level "
        "updates, verification gates) that Part IV and "
        "ch18/ch21/ch22 later operationalise, and that mirrors Part "
        "III's four-corner close (parsing / embeddings / graph / "
        "prompt)."
    ): (
        "五章。第 4–7 章负责 *把文稿收进来* 。"
        "第 7a 章用一个「四角」运维模型收尾："
        "一份**固定的页面集**、一个**元数据 footer**、"
        "**三级更新策略**、以及**校验闸**。"
        "这四个角后面在第四部分以及第 18、21、22 章里被具体落地，"
        "和第三部分结尾的另一个「四角」"
        "（解析 / embedding / 图谱 / prompt）互为镜像。"
    ),
    "Example": "示例",
    (
        "End-to-end run of the CLI against a messy raw folder, "
        "producing a clean wiki. The full walkthrough is in Appendix A."
    ): (
        "用 CLI 对一个乱糟糟的 raw 文件夹跑一次端到端流程，"
        "产出一个干净的 wiki。"
        "完整的分步演示放在附录 A。"
    ),
    "Conclusion": "结论",
    (
        "File-based + Git-backed + pipeline-validated + "
        "*operationally modelled* = a prose layer that behaves like "
        "code: reviewable, diffable, automatable, and auditable for "
        "staleness."
    ): (
        "**基于文件** + **由 Git 托管** + **流水线校验** + "
        "*有运维模型支撑* = "
        "一个「行为像代码」的文稿层："
        "可评审、可 diff、可自动化，"
        "而且**过时与否是可审计的**。"
    ),
    "References": "参考文献",

    # ---- Section: Where Part II sits in the book ----
    "Where Part II sits in the book": "**第二部分在书里的位置**",
    (
        "Part II is the first of the book's two parallel "
        "\"layer\" parts. Part III takes the same shape — five "
        "chapters that pick a substrate, harden its contract, "
        "run a pipeline over it, expose it for search, and "
        "close with an operational model — but applied to "
        "*code* rather than *prose*. Part V then shows the two "
        "layers cooperating (a document-layering tuple that "
        "reads both; a retrieval surface that fuses prose "
        "passages with code embeddings). Reading Part II alone "
        "gives you a defensible prose-layer KB; reading Parts "
        "II and III together gives you the substrate Part V "
        "turns into a code-aware knowledge base; Part VI is "
        "governance for everything Parts II–V produced."
    ): (
        "**第二部分是这本书里**"
        "**两个平行的“层”部分**中的**第一个**。"
        "**第三部分**走的是**同一个形状** —— "
        "**五章**：**选定一个承载层、把它的契约锤结实、"
        "在它之上跑一条流水线、把它暴露出去以便查询、**"
        "**最后以一个运维模型收尾** —— "
        "**只不过应用对象是** *代码* **而不是** *文稿* 。"
        "**第五部分**随后**展示这两层怎么协作**"
        "（**一个同时读这两层的文档分层元组**；"
        "**一个把文稿段落和代码 embedding 融合在一起的检索面**）。"
        "**单读第二部分**，你会得到"
        "**一个站得住脚的文稿层知识库**；"
        "**第二、第三部分一起读**，**你会得到**"
        "**第五部分用来变成一个懂代码的知识库的那块承载层**；"
        "**第六部分**是**对第二到第五部分所产出之一切的治理**。"
    ),
    (
        "The prose-layer structure is deliberately mirrored in "
        "Part III's close: *four corners* on each side, so "
        "that the book's Parts V and VI can talk about both "
        "layers in the same vocabulary. Noticing the mirror is "
        "the cheap way to internalise the shape; §\"How\" "
        "below names the mirror explicitly."
    ): (
        "**文稿层的结构**，**被刻意地镜像到**"
        "**第三部分的收尾**里： *两边各四个角* ，"
        "**这样**这本书的**第五、第六部分**"
        "**就可以用同一套词汇讨论两层**。"
        " *注意到这次镜像* ，"
        "**是内化这个形状的最便宜的方法**；"
        "**下面的** §“How” **会把这次镜像显式命名出来**。"
    ),

    # ---- Section: dependency chain ----
    "The five chapters as a dependency chain":
        "**把这五章看作一条依赖链**",
    (
        "The chapters are not independent essays; each is the "
        "substrate the next one stands on. The table below "
        "makes the substrate relation explicit — if you are "
        "deciding where to cut the part for a short reading "
        "session, cutting *across* the dependency arrows is "
        "cheaper than cutting *along* them."
    ): (
        "**这些章节不是彼此独立的散论**；"
        "**每一章都是下一章所站立的承载层**。"
        "**下面这张表**把这种**承载关系**显式化 —— "
        "**如果你要决定**"
        "**把这个部分在一次短时间阅读里切在哪里**，"
        " *沿与依赖箭头正交的方向切* ，"
        "**比** *沿着它们切* **更便宜**。"
    ),
    "Chapter": "**章**",
    "Picks up from": "**接自**",
    "Produces": "**产出**",
    "Consumed by": "**被谁消费**",

    # -- Ch 4 row --
    "**Ch 4** File-based wiki": "**第 4 章** 基于文件的 wiki",
    "Part I's \"KB as code\" thesis":
        "**第一部分**“**知识库即代码**”的主张",
    "`WikiRepository` + `FileRepository` + the \"Git is your audit log\" contract":
        "`WikiRepository` + `FileRepository` + "
        "“**Git 就是你的审计日志**”这份契约",
    "Everything else in Part II; ch14 (drift detection)":
        "**第二部分其余所有章节**；**第 14 章（漂移检测）**",

    # -- Ch 5 row --
    "**Ch 5** Provenance": "**第 5 章** 来源",
    "Ch 4's filesystem contract": "**第 4 章**的**文件系统契约**",
    "Frontmatter (lineage) + `PKB-metadata` footer (review) + the AI-sets-pending rule":
        "Frontmatter（**谱系**）+ `PKB-metadata` footer（**评审**）+ "
        "**AI 写入即 pending 规则**",
    "Ch 6's ingest (writes footers); ch15 gates; ch18 document layering":
        "**第 6 章的 ingest**（**写 footer**）；"
        "**第 15 章的闸**；"
        "**第 18 章的文档分层**",

    # -- Ch 6 row --
    "**Ch 6** Pipeline": "**第 6 章** 流水线",
    "Ch 4 (files) + Ch 5 (schema)":
        "**第 4 章（文件）+ 第 5 章（schema）**",
    "Six CLI verbs; ingest that writes well-formed files with `unreviewed` trust; an append-only governance log":
        "**六个 CLI 动词**；"
        "**能写出规格良好、信任为 `unreviewed` 的文件的 ingest**；"
        "**一份只追加的治理日志**",
    "Ch 7 (indexes files it produced); ch14 (re-triggers ingest on drift)":
        "**第 7 章**（**给它产出的文件建索引**）；"
        "**第 14 章**（**漂移时重新触发 ingest**）",

    # -- Ch 7 row --
    "**Ch 7** Publish + search": "**第 7 章** 发布 + 搜索",
    "Ch 6's committed tree": "**第 6 章**已经**提交进仓库的那棵文件树**",
    "In-memory postings list for the live server; Sphinx static build":
        "**在线服务用的内存里 postings list**；**Sphinx 静态构建**",
    "Ch 7a's \"what can gates check?\" (search is *not* a gate); ch21's agent retrieval":
        "**第 7a 章**的“**闸能检查什么？**”（**搜索** *不是* **闸**）；"
        "**第 21 章的 agent 检索**",

    # -- Ch 7a row --
    "**Ch 7a** Operational model": "**第 7a 章** 运维模型",
    "Everything above": "**以上的全部**",
    "Four-corner model C1–C4; the Part II checklist":
        "**四角模型 C1–C4**；**第二部分的清单**",
    "Ch 14 (change detection, C2-driven); ch15 (gates, C4); ch16 (three-level updates, C3); ch18/ch21 (both layers)":
        "**第 14 章（变更检测，由 C2 驱动）**；"
        "**第 15 章（闸，C4）**；"
        "**第 16 章（三级更新，C3）**；"
        "**第 18/21 章（两层都会被处理）**",

    # -- Closing paragraph of dependency section --
    (
        "Two arrows are worth singling out. Chapter 5's "
        "frontmatter contract is the *only* artefact the live "
        "server (Ch 7) and the classification pipeline (Ch 6) "
        "*both* read — if you break the schema in Ch 5, you "
        "break both consumers at once. And Chapter 7a's "
        "footer (C2) is the one field every later chapter in "
        "Parts IV–VI touches, because it is the hinge between "
        "per-page state and the operational cycle that acts "
        "on it."
    ): (
        "**有两条箭头值得单独拎出来讲**。"
        "**第 5 章**的 frontmatter 契约"
        "**是在线服务**（**第 7 章**）"
        "和**分类流水线**（**第 6 章**）"
        " *同时* 读的**唯一一份**制品 —— "
        "**如果你把第 5 章的 schema 改坏了**，"
        "**这两个消费者会一起坏**。"
        "而**第 7a 章的 footer （C2）**，"
        "**是后续第四、五、六部分里**"
        "**每一章都会触碰的那一个字段** —— "
        "**因为它是按页状态和对这种状态做事的那个运维循环之间的铰链**。"
    ),

    # ---- Section: mirror ----
    "The Part II ⇄ Part III mirror":
        "**第二部分 ⇄ 第三部分的镜像**",
    (
        "The two layers are not symmetric in their *content* "
        "— prose drifts, code does not; prose has paragraphs, "
        "code has functions; prose is updated by humans, code "
        "by commits. They are symmetric in their *operational "
        "shape*, and the mirror is worth stating once so that "
        "Parts V and VI can rely on it:"
    ): (
        "这两层**在 *内容* 上并不对称** —— "
        "**文稿会漂移，代码不会**；"
        "**文稿以段落为单位，代码以函数为单位**；"
        "**文稿由人类更新，代码由 commit 更新**。"
        "它们**对称的是** *运维形状* ；"
        "**这次镜像值得明讲一次**，"
        "这样**第五和第六部分就可以依赖它**："
    ),
    "Part III (code)": "**第三部分（代码）**",
    "Shared shape": "**共享的形状**",
    "Ch 4 File-based wiki": "**第 4 章** 基于文件的 wiki",
    "Ch 8 Why code is not prose":
        "**第 8 章** 为什么代码不是文稿",
    "*Pick a substrate and name its contract*":
        " *选定一个承载层，并命名它的契约* ",
    "Ch 5 Frontmatter + footer":
        "**第 5 章** frontmatter + footer",
    "Ch 9 Parsing and entity extraction":
        "**第 9 章** 解析与实体抽取",
    "*Make the contract machine-readable*":
        " *把契约变得机器可读* ",
    "Ch 6 Classification pipeline":
        "**第 6 章** 分类流水线",
    "Ch 10 + Ch 11 Embeddings + graph":
        "**第 10 + 11 章** embedding + 图谱",
    "*Run a pipeline over the substrate*":
        " *在承载层之上跑一条流水线* ",
    "Ch 7 Publish + search (prefix index)":
        "**第 7 章** 发布 + 搜索（**前缀索引**）",
    "Ch 12 Hybrid retrieval + RRF":
        "**第 12 章** 混合检索 + RRF",
    "*Expose the substrate for query*":
        " *把承载层暴露出去以便查询* ",
    "Ch 7a Four-corner operational model":
        "**第 7a 章** 四角运维模型",
    "Ch 13 Prompt + generation":
        "**第 13 章** Prompt + 生成",
    "*Close with a stable shape the rest of the book refers to*":
        " *以一个本书余下部分都会回头引用的稳定形状收尾* ",
    (
        "The mirror is why the book's glossary (Appendix D) "
        "uses the same vocabulary for both layers and why "
        "Chapter 18's document-layering tuple can treat prose "
        "and code uniformly. It is also why teams that adopt "
        "Part II first and Part III second usually *compress* "
        "Part III's timeline — the operational shape is "
        "already in place."
    ): (
        "**这次镜像**，**就是**"
        "**本书词汇表（附录 D）对两层使用同一套词汇的原因**，"
        "也是**第 18 章的文档分层元组**"
        "**能够统一处理文稿和代码**的**原因**。"
        "**也是**"
        "**那些先落地第二部分、再落地第三部分的团队**"
        "**通常 *把第三部分的时间线压短* 的原因** —— "
        "**那个运维形状**已经**到位了**。"
    ),

    # ---- Section: reading paths ----
    "Reading paths — pick one by the problem you have":
        "**阅读路径 —— 按你手头的问题挑一条**",
    (
        "Part II is 1 600 lines of book. You do not need to "
        "read it linearly. Three typical paths cover most "
        "readers' purposes:"
    ): (
        "**第二部分**有**一千六百行**。"
        "**你不需要按次序读它**。"
        "**三条典型路径**，**已经覆盖了多数读者的目的**："
    ),
    (
        "**\"I have 20 minutes before a meeting and I want the "
        "thesis.\"** Read the hook opening and `## Why` of "
        "**Ch 4**, then the `## Why` of **Ch 7a**, then Ch "
        "7a's `## Part II in one page — a pointer checklist`. "
        "That is the whole argument in three pages. Return for "
        "the mechanics later."
    ): (
        "**“离开会还有 20 分钟，我只要论点。”** "
        "**读**：**第 4 章**的 hook 开场和 `## Why` ，"
        "接着**第 7a 章**的 `## Why` ，"
        "然后**第 7a 章**的"
        " `## Part II in one page — a pointer checklist` 。"
        "**这就是整套论证的三页版**。"
        "**机械细节**可以**晚点再回来看**。"
    ),
    (
        "**\"I am building the tool-chain.\"** Read **Ch 4 → "
        "Ch 5 → Ch 6** in order, skipping the `## Competing "
        "approaches` tables on the first pass. Then read the "
        "code references in `ch04/repository.go`, "
        "`ch05/frontmatter.go`, and `ch06/pipeline.go`. Skim "
        "Ch 7; revisit Ch 7a after you have run the pipeline "
        "once against a real corpus and want to know which "
        "rules to enforce."
    ): (
        "**“我在搭工具链。”** "
        "**按序读**：**第 4 → 5 → 6 章**，"
        "**第一遍先跳过** `## Competing approaches` 的表。"
        "**然后读代码引用**："
        " `ch04/repository.go` 、"
        " `ch05/frontmatter.go` 、"
        " `ch06/pipeline.go` 。"
        "**速读第 7 章**；"
        "**等你已经对着一份真实语料跑过一遍流水线、**"
        "**想知道要强制哪些规则时**，"
        "**再回头读第 7a 章**。"
    ),
    (
        "**\"I have an existing KB and I am doing a "
        "postmortem.\"** Skip the chapter `## Why` sections "
        "and go straight to: **Ch 6 §\"How LLM classification "
        "fails in production\"**, **Ch 7 §\"Where the tiny "
        "search engine fails\"**, and **Ch 7a §\"What this "
        "model does *not* solve\"**. Cross-reference each "
        "symptom you have seen in the wild against the Part "
        "II checklist in Ch 7a; that will tell you which "
        "chapter to read in full."
    ): (
        "**“我有一个现成的知识库，我在做事后复盘。”** "
        "**跳过各章的 `## Why` 小节**，"
        "**直接去读**："
        "**第 6 章 §“How LLM classification fails in production”**、"
        "**第 7 章 §“Where the tiny search engine fails”**、"
        "以及**第 7a 章 §“What this model does *not* solve”**。"
        "**把你在现场看到的每一个症状**，"
        "**去对照第 7a 章的第二部分清单**；"
        "**那会告诉你要完整读哪一章**。"
    ),
    (
        "These paths are the reason the part is shaped the "
        "way it is: each chapter has a self-contained opening, "
        "a self-contained failure catalogue, and a "
        "self-contained \"competing approaches\" table, so "
        "that a reader arriving mid-part has a complete unit "
        "of thought to take away without reading the part in "
        "order."
    ): (
        "**这几条路径**，**就是这个部分被这样组织的原因**："
        "**每一章**都**自带**"
        "**一段自洽的开场、一份自洽的失败目录、**"
        "**以及一张自洽的“竞品方案”表** —— "
        "**这样**"
        "**从这个部分中途走进来的读者**"
        "**不用按序读，**"
        "**也能带走一套完整的思考单元**。"
    ),

    # ---- Override fuzzy: "Part II (prose)" — used as table header ----
    "Part II (prose)": "**第二部分（文稿）**",
}
