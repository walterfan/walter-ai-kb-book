"""Chinese translations for book/part1-foundations/ch03-diataxis-and-software-docs.md.

See book/_tools/translations/ch02-ir-rag-primer.zh.py for the full
style guide. Chapter-specific notes:

- **Diátaxis** is kept as "Diátaxis" (with the acute accent), because
  the taxonomy name is a proper noun coined by Daniele Procida. Body
  text uses "Diátaxis" rather than "典型分类法" or similar.
- The four doc types — tutorial, how-to, reference, explanation —
  are translated on first mention, but the labels in the `doc_type`
  YAML enum stay in English because they are values the schema
  enforces, not prose.
- DITA, DITA-OT, OASIS, Write-the-Docs, DokuWiki, Kubernetes, Docker,
  Compose, Go, Python, goroutines, channels, asyncio, decorators:
  kept in English.
- "ADR" and "runbook" stay in English (used as running abbreviations
  across the book).
- CommonMark emphasis rule: `*italic*` between two CJK characters
  needs an ASCII space outside each `*`.
- Table cells must be translated as complete stand-alone msgids; do
  NOT merge them.
- YAML and YAML-like code blocks are kept verbatim in the translation
  (the content is a schema snippet, not prose).
"""

PO_PATH = "part1-foundations/ch03-diataxis-and-software-docs.po"

TRANSLATIONS: dict[str, str] = {
    # ---- title, Why ----
    "Chapter 3 — Diátaxis and Software Docs": (
        "第 3 章 —— Diátaxis 与软件文档"
    ),
    "Why": "为什么",
    (
        "A knowledge base without a document-type taxonomy is a "
        "search problem. A knowledge base with the *wrong* taxonomy "
        "is a filing problem. Filing problems are more expensive "
        "than search problems because filing problems are authored, "
        "and authored mistakes compound."
    ): (
        "一个没有文档类型分类的知识库，是一个搜索问题。"
        "一个采用了 *错的* 分类的知识库，是一个归档问题。"
        "归档问题比搜索问题更贵 —— "
        "因为归档问题是人主动“写”进去的，"
        "而被写进去的错误会不断累积利息。"
    ),
    (
        "The working engineers Lethbridge and colleagues surveyed "
        "{cite}`lethbridge2003software` were asked, effectively, "
        "*\"why do you not read the docs?\"* The answers boiled down "
        "to: *because I do not know which document answers my "
        "question, and when I find one, it turns out not to be the "
        "document I wanted.* Aghajani et al. "
        "{cite}`aghajani2019software` two decades later report the "
        "same symptom in a different register: large fractions of "
        "bug reports about documentation are \"wrong type of content "
        "for the section it lives in.\""
    ): (
        "Lethbridge 等人 {cite}`lethbridge2003software` "
        "调研过的那些一线工程师，"
        "被问到的本质上就是那一个问题："
        "*“你为什么不看文档？”* "
        "答案归结起来是这样的："
        "*因为我不知道哪一份文档能回答我的问题，"
        "而当我终于找到一份看起来像的时候，"
        "它又不是我真正想要的那一份。* "
        "二十年后，Aghajani 等人 {cite}`aghajani2019software` "
        "在另一个场景里报告了同样的症状："
        "关于文档的 bug 报告里，"
        "很大一部分都是“内容放在了错误的章节里”。"
    ),
    (
        "A good taxonomy makes this symptom disappear. Daniele "
        "Procida's **Diátaxis** {cite}`procida_diataxis` is, at time "
        "of writing, the taxonomy most likely to survive contact "
        "with a real software project. It has four types; it is "
        "orthogonal along two axes; it is small enough to fit on a "
        "postcard; and — most importantly for this book — it is "
        "small enough that a classification pipeline, human or "
        "LLM-driven, can actually be trained against it without "
        "hand-wringing over twenty-way ties."
    ): (
        "一套好的分类学能让这种症状消失。"
        "Daniele Procida 提出的 **Diátaxis** {cite}`procida_diataxis` —— "
        "截至本书写作时 —— "
        "是最能在真实软件项目里活下来的那套分类。"
        "它只有四种类型；"
        "它沿两根正交的轴展开；"
        "它小到能印在一张明信片上；"
        "而且 —— 对本书最重要的一点是 —— "
        "它小到一条分类流水线（无论是人工的还是 LLM 驱动的）"
        "真的可以被训练起来，"
        "而不至于陷在二十种类型的平票里无从决断。"
    ),
    # ---- What ----
    "What": "是什么",
    (
        "Diátaxis divides technical documentation along two axes, "
        "producing four quadrants {cite}`procida_diataxis`:"
    ): (
        "Diátaxis 沿两根轴把技术文档划分开，"
        "产生四个象限 {cite}`procida_diataxis`："
    ),
    # Table column/row labels
    "Practical": "实用（Practical）",
    "Theoretical": "理论（Theoretical）",
    "**Studying**": "**学习中（Studying）**",
    "**Tutorial** — learning-oriented": (
        "**Tutorial（教程）** —— 面向学习"
    ),
    "**Explanation** — understanding-oriented": (
        "**Explanation（解释）** —— 面向理解"
    ),
    "**Working**": "**工作中（Working）**",
    "**How-to** — task-oriented": (
        "**How-to（操作指南）** —— 面向任务"
    ),
    "**Reference** — information-oriented": (
        "**Reference（参考）** —— 面向信息"
    ),
    (
        "The two axes (*practical ↔ theoretical* and *studying ↔ "
        "working*) are not about the writer's mood; they are about "
        "the reader's state. A reader is either studying (trying to "
        "build a mental model) or working (trying to get something "
        "done right now). Orthogonally, they are either seeking "
        "concrete action or seeking concepts. Any piece of writing "
        "that honestly answers *both* axes at once is almost "
        "certainly two pieces of writing that got glued together."
    ): (
        "这两根轴（*实用 ↔ 理论* 与 *学习中 ↔ 工作中*）"
        "讲的不是写作者的心情，"
        "讲的是阅读者的状态。"
        "一个读者要么在“学习”（正尝试构建一个心智模型），"
        "要么在“工作”（正想立刻把一件事做完）；"
        "与此正交地，"
        "他要么在找具体行动，要么在找概念。"
        "任何一篇号称同时如实回答 *两根* 轴的文字，"
        "大概率其实是两篇被粘在一起的文字。"
    ),
    (
        "An important property of the taxonomy for our purposes is "
        "that a document's type determines *the shape of its ideal "
        "first sentence*:"
    ): (
        "对本书的目的来说，这套分类有一条很重要的性质："
        "一份文档的类型会决定 *它理想开头第一句话的形状*："
    ),
    "A **tutorial** starts with what the reader will build.": (
        "一份 **tutorial（教程）** 从“读者将会造出什么”开始写。"
    ),
    (
        "A **how-to** starts with the goal state the reader wants to "
        "reach."
    ): (
        "一份 **how-to（操作指南）** 从“读者想到达的目标状态”开始写。"
    ),
    (
        "A **reference** starts with the name of the thing being "
        "described."
    ): (
        "一份 **reference（参考）** 从“被描述之物的名字”开始写。"
    ),
    (
        "An **explanation** starts with the question being answered."
    ): (
        "一份 **explanation（解释）** 从“正在被回答的问题”开始写。"
    ),
    (
        "This will matter in Chapter 6, where we ask an LLM to "
        "classify raw imports into the four types."
    ): (
        "这一点到第 6 章会变得重要 —— "
        "届时我们会让一个 LLM 把原始导入的文档分类到这四种类型中去。"
    ),
    # ---- Chapter-level mindmap intro (sits above `## Why`) ----
    (
        "This chapter on one page — the two classification axes the "
        "chapter argues a software KB needs, the four Diátaxis doc "
        "types, the opinionated ten-page instantiation this book "
        "adopts, and what is deliberately *not* on that list:"
    ): (
        "本章全貌，一页看完 —— "
        "本章主张一个软件知识库需要的两根分类轴、"
        "Diátaxis 的四种文档类型、"
        "本书采用的那份有态度的十页实例，"
        "以及 *刻意不放进* 这份清单里的东西："
    ),
    # ---- How ----
    "How": "怎么做",
    (
        "The prose-layer reference implementation lifts Diátaxis "
        "directly into its frontmatter schema. From "
        "`wiki-template/metadata/SCHEMA.md`:"
    ): (
        "文本层参考实现把 Diátaxis 直接搬到了它的 frontmatter schema 里。"
        "摘自 `wiki-template/metadata/SCHEMA.md`："
    ),
    # YAML code block — msgid has literal newlines; rendered verbatim.
    (
        "---\n"
        "title: \"Page Title\"\n"
        "doc_type: reference            "
        "# tutorial | how-to | reference | explanation\n"
        "verification_status: supported "
        "# supported | unreviewed | uncertain | contradicted | "
        "superseded\n"
        "created_by: alice\n"
        "updated_by: alice\n"
        "source:\n"
        "  type: original               "
        "# original | git_repo | doc | url\n"
        "  uri: \"\"\n"
        "---\n"
    ): (
        "---\n"
        "title: \"Page Title\"\n"
        "doc_type: reference            "
        "# tutorial | how-to | reference | explanation\n"
        "verification_status: supported "
        "# supported | unreviewed | uncertain | contradicted | "
        "superseded\n"
        "created_by: alice\n"
        "updated_by: alice\n"
        "source:\n"
        "  type: original               "
        "# original | git_repo | doc | url\n"
        "  uri: \"\"\n"
        "---\n"
    ),
    "Two observations are worth pausing on.": (
        "有两条观察值得停一下。"
    ),
    (
        "**First**, `doc_type` is a first-class *field*, not a "
        "free-form tag. It has four legal values, not a hundred. "
        "That constraint is load-bearing. Every downstream component "
        "— the search index (Chapter 7), the LLM-assisted classifier "
        "(Chapter 6), the ADR-vs-runbook separation (Chapter 18) — "
        "assumes that `doc_type` is one of exactly four labels. The "
        "moment the project admits a fifth, the classifier has to be "
        "retrained, the index has to be re-weighted, and every rule "
        "in the layer model has to be audited. Staying at four is "
        "cheap; growing to five is never cheap."
    ): (
        "**第一**：`doc_type` 是一个一等公民的 *字段*，"
        "不是一个自由格式的 tag。"
        "它的合法取值只有四个，不是一百个。"
        "这个约束是承重的。"
        "下游的每一个组件 —— 搜索索引（第 7 章）、"
        "LLM 辅助分类器（第 6 章）、"
        "ADR 与 runbook 的分离（第 18 章） —— "
        "都假设 `doc_type` 恰好落在这四个标签其中之一。"
        "一旦项目接受了第五个标签，"
        "分类器就得重训、"
        "索引就得重加权、"
        "分层模型里的每一条规则都得被重新审一遍。"
        "守在四个是便宜的，长到五个从来都不便宜。"
    ),
    (
        "**Second**, the schema bundles `doc_type` with a *trust* "
        "field (`verification_status`) and a *provenance* field "
        "(`source`). This is not incidental. The blog post the book "
        "builds on {cite}`fanyamin2026deepwiki` argues in its §11 "
        "that *document layering* (L0 – L4, which Chapter 18 "
        "unpacks in full) is the mechanism that keeps AI-generated "
        "pages, human-authored runbooks, and architectural decisions "
        "from getting confused for one another. Diátaxis classifies "
        "a document along the *reader-intent* axis; "
        "`verification_status` and `source` classify it along the "
        "*author-and-trust* axis. Both axes have to be present for a "
        "software KB to stay honest."
    ): (
        "**第二**：这份 schema 把 `doc_type` 和一个 *信任* 字段 "
        "（`verification_status`）、"
        "一个 *来源* 字段（`source`）捆在一起。"
        "这不是偶然。"
        "本书底稿的那篇博客 {cite}`fanyamin2026deepwiki` 在 §11 里论证道："
        "*文档分层*（L0 – L4，第 18 章会完整展开）"
        "正是那个用来防止"
        "AI 生成页、人工 runbook、"
        "架构决策这三者被混为一谈的机制。"
        "Diátaxis 沿 *读者意图* 这根轴给文档分类；"
        "`verification_status` 和 `source` 沿 *作者与信任* 那根轴给它分类。"
        "对一个诚实的软件知识库来说，这两根轴都必须在场。"
    ),
    (
        "A specific competing view deserves direct engagement. "
        "**DITA** {cite}`oasis_dita`, the OASIS-maintained \"Darwin "
        "Information Typing Architecture\", is the formal taxonomy "
        "that the large technical-writing industry uses. DITA is "
        "richer than Diátaxis, has XML schemas, and supports "
        "arbitrary content types (`task`, `concept`, `reference`, "
        "`troubleshooting`, plus specialisations). For a "
        "technical-writing team producing printed manuals across "
        "multiple products, DITA is the right tool. For a software "
        "team producing wiki pages alongside code, DITA imposes a "
        "tooling cost — XML editors, DITA-OT build pipelines, "
        "specialised authors — that outweighs its flexibility. "
        "Diátaxis's willingness to be *small* is, in our context, a "
        "feature, not a limitation. The Write-the-Docs community "
        "style-guide corpus {cite}`wtd_write_the_docs` comes to a "
        "similar practical conclusion."
    ): (
        "有一种具体的对立观点值得正面回应。"
        "**DITA** {cite}`oasis_dita` —— "
        "OASIS 维护的 “Darwin Information Typing Architecture” —— "
        "是大型技术写作行业实际使用的那套正式分类。"
        "DITA 比 Diátaxis 更丰富，"
        "带 XML schema，"
        "支持任意多的内容类型（`task`、`concept`、`reference`、`troubleshooting`，"
        "以及它们各自的特化）。"
        "对那种要跨多条产品线生产印刷手册的技术写作团队来说，"
        "DITA 是对的工具。"
        "但对一个要在代码旁边同步生产 wiki 页的软件团队来说，"
        "DITA 强加的一整套工具链成本 —— "
        "XML 编辑器、DITA-OT 构建流水线、专业化的撰稿人 —— "
        "已经压过了它的灵活性。"
        "在我们这个场景下，"
        "Diátaxis “愿意让自己 *很小* ” 这一点本身是优点，不是缺陷。"
        "Write-the-Docs 社区的风格指南语料 {cite}`wtd_write_the_docs` "
        "得到的也是类似的实务结论。"
    ),
    # ---- Example ----
    "Example": "示例",
    (
        "A dump of the pages under `wiki-template/content/` — the "
        "template this repo uses to seed a new wiki — falls cleanly "
        "into the four Diátaxis types:"
    ): (
        "把 `wiki-template/content/` 下的页面导出一份来看 —— "
        "这也是本仓库用来初始化一个新 wiki 的模板 —— "
        "它们能干净利落地落进 Diátaxis 的四个类型里："
    ),
    "File": "文件",
    "Diátaxis type": "Diátaxis 类型",
    "Reader's state": "读者的状态",
    # File names kept verbatim (they are paths in the template).
    "`content/devops/kubernetes.md`": "`content/devops/kubernetes.md`",
    "**reference**": "**reference（参考）**",
    "working": "工作中",
    "surveys Kubernetes primitives with signatures and examples": (
        "概述 Kubernetes 的基本概念，附带签名和示例"
    ),
    "`content/devops/docker.md`": "`content/devops/docker.md`",
    "same pattern, focused on Docker CLI + Compose": (
        "同样的模式，聚焦在 Docker CLI + Compose"
    ),
    "`content/programming/go/concurrency.md`": (
        "`content/programming/go/concurrency.md`"
    ),
    "**explanation**": "**explanation（解释）**",
    "studying": "学习中",
    (
        "\"understanding-oriented\" — why goroutines, channels, and "
        "`sync` are shaped the way they are"
    ): (
        "“面向理解” —— 解释 goroutine、channel 和 `sync` "
        "为什么长成现在这个样子"
    ),
    "`content/programming/go/interfaces.md`": (
        "`content/programming/go/interfaces.md`"
    ),
    (
        "discusses the *idea* of structural typing in Go rather than "
        "a step-by-step recipe"
    ): (
        "讨论的是 Go 里结构化类型的 *理念*，"
        "而不是一份步骤化的菜谱"
    ),
    "`content/programming/python/asyncio.md`": (
        "`content/programming/python/asyncio.md`"
    ),
    "same shape as the Go concurrency page": (
        "和上面那份 Go 并发页的形状一样"
    ),
    "`content/programming/python/decorators.md`": (
        "`content/programming/python/decorators.md`"
    ),
    (
        "discusses what decorators *are* and when to reach for them"
    ): (
        "讨论的是 decorator *是什么*、以及什么时候该动用它"
    ),
    (
        "The template folder, as it ships, contains mostly "
        "explanations and one reference section — there are no "
        "tutorials or how-tos yet. That is a *feature-state* "
        "observation about this template (it is a starter set, not a "
        "finished KB), not a bug. The classification exercise makes "
        "the gap visible immediately: a mature project using this "
        "wiki should acquire tutorials (onboarding paths) and "
        "how-tos (runbooks) over time. Chapter 6's classification "
        "pipeline flags exactly that kind of imbalance when it "
        "reports doc-type histograms."
    ): (
        "这个模板目录“出厂状态”主要是 explanation，"
        "加一个 reference 分区 —— "
        "tutorial 和 how-to 还都没有。"
        "这算是对当前模板的一条 *现状* 观察 —— "
        "它是一个起点模板，而不是一个完成态的知识库 —— "
        "不是缺陷。"
        "而“做一次分类”这个动作，"
        "让这个缺口立刻变得可见："
        "一个基于本 wiki 长起来的成熟项目，"
        "随着时间推移应当长出 tutorial（上手路径）和 how-to（runbook）。"
        "第 6 章的分类流水线在报告 doc_type 直方图时，"
        "检测的就是这种失衡。"
    ),
    (
        "The same exercise on the `wiki-template/metadata/SCHEMA.md` "
        "file itself is interesting: it is a **reference** (it "
        "documents the schema) that also contains a small "
        "**explanation** (\"Trust Model\" section, lines 48–53). "
        "This is a useful reminder that Diátaxis is a classifier "
        "over *files*, not over *paragraphs*. A document-layer "
        "review (Chapter 18) should flag files whose body spans two "
        "quadrants and consider whether to split them."
    ): (
        "对 `wiki-template/metadata/SCHEMA.md` 这份文件本身做同样的练习，"
        "结果挺有意思："
        "它是一份 **reference**（它在描述 schema），"
        "但其中又包含一小段 **explanation**（“Trust Model”一节，48–53 行）。"
        "这是一个有用的提醒："
        "Diátaxis 是 *以文件为粒度* 的分类器，"
        "而不是以段落为粒度。"
        "一次文档分层复审（第 18 章）"
        "应当把正文跨了两个象限的文件标出来，"
        "并考虑要不要把它拆开。"
    ),
    # ---- opinionated instantiation ----
    "One opinionated instantiation": "一份有态度的具体实例",
    (
        "Diátaxis tells you the *kinds* of page. It does not tell "
        "you *which specific pages* a software project should ship. "
        "Two teams can both be \"Diátaxis-compliant\" and still end "
        "up with wildly different tables of contents: one writes "
        "five tutorials and no runbook; the other writes a runbook, "
        "a reference, and nothing else. Both are defensible. Neither "
        "helps a new engineer who has to figure out *where the "
        "runbook lives* in a project they have never seen before."
    ): (
        "Diátaxis 告诉你页面的 *类型*，"
        "但它并不告诉你一个软件项目 *具体要交付哪几页*。"
        "两个团队完全可以都“符合 Diátaxis”，"
        "最终却得到截然不同的目录："
        "一个写了五篇 tutorial、没有 runbook；"
        "另一个写了一份 runbook、一份 reference，此外什么都没有。"
        "两种都能各自自圆其说。"
        "但两种都帮不到一个新来的工程师 —— "
        "他要在一个从没见过的项目里找到 *runbook 放在哪儿*。"
    ),
    (
        "The author's private project-knowledge-base toolkit "
        "{cite}`fanyamin_pkb_skill` resolves this by committing to a "
        "small, stable set of pages — one concrete answer to "
        "\"which specific pages should a software KB have?\" — with "
        "numbers that fix the reading order. This book adopts a "
        "ten-page cut of that set as its canonical instantiation. "
        "Teams are free to diverge; the claim is not that these ten "
        "are the *only* valid pages, but that picking *some* stable "
        "set, early, is more valuable than arguing about which set:"
    ): (
        "作者私人维护的那套 project-knowledge-base 工具链 "
        "{cite}`fanyamin_pkb_skill` "
        "对这个问题的回答是：承诺一组小而稳定的页面 —— "
        "对“一个软件知识库具体该有哪几页？”给出一个具体答案 —— "
        "并且用编号把阅读顺序也钉死。"
        "本书取其中的一个十页版本，"
        "作为自己的标准实例。"
        "各团队完全可以另有选择；"
        "这里的主张不是“只有这十页是对的”，"
        "而是“早早挑定 *某一组* 稳定页面”"
        "比“反复争论该挑哪一组”更值钱："
    ),
    "#": "#",
    "Page": "页面",
    "What it answers": "它回答的是什么",
    "00": "00",
    "`overview`": "`overview`",
    "explanation": "explanation（解释）",
    "*\"What is this project, in five minutes?\"*": (
        "*“这个项目是什么？五分钟讲清楚。”*"
    ),
    "01": "01",
    "`quick-start`": "`quick-start`",
    "tutorial": "tutorial（教程）",
    "*\"How do I get to 'hello world' in ten minutes?\"*": (
        "*“我怎么在十分钟内跑通 hello world？”*"
    ),
    "02": "02",
    "`architecture`": "`architecture`",
    "*\"What are the containers, components, and why?\"* (C4; see Chapter 4)": (
        "*“有哪些容器、哪些组件，以及为什么？”*（C4 模型；见第 4 章）"
    ),
    "03": "03",
    "`repo-map`": "`repo-map`",
    "reference": "reference（参考）",
    "*\"Where is what, at the current commit?\"*": (
        "*“在当前 commit 下，什么放在哪儿？”*"
    ),
    "04": "04",
    "`data-and-api`": "`data-and-api`",
    "*\"What is the public contract?\"*": (
        "*“对外公开的契约是什么？”*"
    ),
    "05": "05",
    "`workflows`": "`workflows`",
    "*\"What does the code actually do, step by step?\"*": (
        "*“代码实际上一步一步做了什么？”*"
    ),
    "06": "06",
    "`conventions`": "`conventions`",
    "*\"Naming, layout, style rules.\"*": (
        "*“命名、布局、风格规则。”*"
    ),
    "07": "07",
    "`testing`": "`testing`",
    "how-to + reference": "how-to + reference",
    "*\"How do I run tests, and what do they cover?\"*": (
        "*“我怎么跑测试，它们覆盖了什么？”*"
    ),
    "08": "08",
    "`runbook`": "`runbook`",
    "how-to": "how-to（操作指南）",
    "*\"When it breaks, what do I do?\"*": (
        "*“它挂了的时候，我该怎么办？”*"
    ),
    "09": "09",
    "`observability`": "`observability`",
    "*\"What do I watch, and where do I look?\"*": (
        "*“我该看哪些指标，该去哪儿看？”*"
    ),
    (
        "Two notes on what is *not* on this list. There is no "
        "`adr/` page, because ADRs are a *collection*, not one "
        "page; they live under their own directory and are layered "
        "separately in Chapter 18. There is no `changelog`, because "
        "a well-kept Git history plus release notes subsumes it for "
        "most teams."
    ): (
        "对于 *没* 出现在清单里的东西，有两点要说明。"
        "没有 `adr/` 页，"
        "因为 ADR 是一个 *集合*，不是一页；"
        "它们住在自己专用的目录里，"
        "并在第 18 章里单独分层处理。"
        "没有 `changelog` 页，"
        "因为对大多数团队来说，"
        "一份保养得当的 Git 历史加上 release note 已经把它覆盖掉了。"
    ),
    (
        "The numbering matters more than it looks. A reader landing "
        "cold on a project's docs should be able to read `00` "
        "through `04` in order and be ready to touch the code; `05` "
        "through `09` are what they return to when they are working. "
        "A tool scanning the KB — the classification pipeline in "
        "Chapter 6, the document-layering tuple in Chapter 18 — gets "
        "a stable directory shape to target. And a maintainer "
        "deciding whether to accept a new page has a simple test: "
        "*does this fit into one of the ten slots, or does it want "
        "to be an eleventh?* The moment the answer is \"an "
        "eleventh\", the discussion is \"is this page worth "
        "restructuring the taxonomy for?\" — a productive question — "
        "rather than \"where shall I put this?\" — a filing problem."
    ): (
        "这套编号的作用，远比看上去大。"
        "一个完全冷启动落到项目文档上的读者，"
        "应该可以按顺序读 `00` 到 `04`，然后就能动手改代码；"
        "`05` 到 `09` 则是他在“工作中”回头查的那几页。"
        "一个扫描知识库的工具 —— "
        "第 6 章里的分类流水线、"
        "第 18 章里的文档分层四元组 —— "
        "也就因此拿到了一份稳定的目录形状可以对齐。"
        "而一个在审核是否接受新页面的维护者，"
        "手上也多了一个简单的判据："
        "*这一页能塞进那十个槽里的某一个吗？"
        "还是它想成为第十一个？* "
        "一旦答案是“第十一个”，"
        "对话就从“这东西我该放哪儿？”（一个归档问题）"
        "变成了“这一页是否值得我们重新调整整套分类？”"
        "—— 后者是一个有建设性的问题。"
    ),
    (
        "This is one concrete answer. Chapter 7a (\"The prose-layer "
        "operational model\") makes it Corner C1 of the book's "
        "four-corner operational model."
    ): (
        "这就是一个具体答案。"
        "第 7a 章（“文本层运营模型”）"
        "会把它定为本书四角运营模型中的 C1 角。"
    ),
    # ---- Conclusion ----
    "Conclusion": "小结",
    (
        "Once `doc_type` is a first-class, four-valued field, "
        "downstream problems shrink. Search weighting can prefer "
        "how-tos for \"how do I\" queries. The LLM classifier has a "
        "closed vocabulary. The document-layer model has something "
        "to hang its rules on. ADRs, vision documents, and runbooks "
        "— none of which are pure Diátaxis types — get their own "
        "first-class layer in Chapter 18, rather than being "
        "shoehorned into a \"Miscellaneous\" category no one "
        "searches. Keeping the taxonomy small is not parsimony for "
        "parsimony's sake; it is what makes every downstream chapter "
        "in this book implementable."
    ): (
        "一旦 `doc_type` 是一个一等公民、只有四个值的字段，"
        "下游的问题全都会收缩。"
        "搜索加权在碰到“我该怎么……”的查询时可以偏向 how-to。"
        "LLM 分类器拿到的是一份封闭词表。"
        "文档分层模型也终于有东西可以挂规则了。"
        "而 ADR、愿景文档、runbook —— "
        "这几类都不是纯粹的 Diátaxis 类型 —— "
        "会在第 18 章里拿到属于自己的一等公民层，"
        "而不是被硬塞进一个谁都不会去搜的 “Miscellaneous” 类别。"
        "把分类保持得小，"
        "不是为了“极简”本身 —— "
        "而是为了让本书下游每一章都仍然有可能被真正实现出来。"
    ),
    "References": "参考文献",
}
