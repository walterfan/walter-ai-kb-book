"""Chinese translations for source/part1-foundations/ch01-why-kb-for-software.md.

See source/_tools/translations/ch02-ir-rag-primer.zh.py for the full
style guide. Chapter-specific notes:

- "Knowledge base" is rendered as "知识库"; abbreviation "KB" is kept
  in English because the book uses it as a running abbreviation.
- "ADR" (Architecture Decision Record) is kept in English — it is a
  widely-recognised acronym in the Chinese engineering community.
- "runbook" and "tree-sitter" kept in English (product/tool names).
- DeepWiki, Sourcegraph Cody, Notion AI, DokuWiki, Memgraph, pgvector,
  GitHub, Docker Compose, CVS, Subversion: all kept in English.
- CommonMark emphasis rule: `*italic*` between two CJK characters
  needs an ASCII space outside each `*`, or CommonMark will render
  the delimiters as literals.
"""

PO_PATH = "part1-foundations/ch01-why-kb-for-software.po"

TRANSLATIONS: dict[str, str] = {
    # ---- title, Why ----
    "Chapter 1 — Why a Knowledge Base for Software?": (
        "第 1 章 —— 为什么要给软件建一个知识库？"
    ),
    "Why": "为什么",
    (
        "Imagine a first-day engineer opening a mid-sized service "
        "repository. They ask their senior teammate a question that "
        "sounds innocent: *\"where is `runSync` called from, and why "
        "does its `defer` block include a `recover`?\"*. The answer "
        "they usually get is some version of \"just read the code.\" "
        "The blog post that this book is built on "
        "{cite}`fanyamin2026deepwiki` opens with exactly this scene, "
        "and it lingers on the scene for a reason: the scene is not "
        "about that one function. It is about the shape of every "
        "modern codebase."
    ): (
        "想象一个刚入职第一天的工程师，打开了一个中等规模的服务仓库。"
        "他向资深同事抛出一个听着很无辜的问题："
        "*“`runSync` 是从哪些地方被调用的？它的 `defer` 块里为什么还要 `recover`？”*。"
        "他通常会得到一个“你自己看代码去”的回答。"
        "本书底稿的那篇博客 {cite}`fanyamin2026deepwiki` 开头就是这一幕，"
        "而且特意停了一下 —— 因为这一幕讲的根本不是那一个函数，"
        "讲的是每一个现代代码库的样子。"
    ),
    (
        "A production repository today is routinely hundreds of "
        "thousands of lines long, spread across dozens of packages "
        "and layered on top of internal frameworks that the new-hire "
        "has never seen. The README describes the repository as it "
        "was two years ago. The architecture diagram is in a slide "
        "deck no one can find. The comments were written for the "
        "compiler, not for a human. The institutional memory — *why "
        "we picked this data store, why this function has a retry, "
        "who to page when it breaks* — lives mostly in the heads of "
        "three senior engineers who are, at that moment, in a "
        "meeting."
    ): (
        "今天一个生产仓库动辄几十万行，"
        "散落在几十个 package 里，"
        "底下还压着一层新人从没见过的内部框架。"
        "README 描述的是两年前的样子；"
        "架构图躺在一份没人找得到的幻灯片里；"
        "注释是写给编译器看的，不是写给人看的。"
        "真正的“组织记忆” —— "
        "*我们为什么选这个数据库、"
        "这个函数为什么要加重试、"
        "它挂了要呼谁* —— "
        "多半只存在三位资深工程师的脑子里，"
        "而这三位此刻正在开会。"
    ),
    (
        "This is not a new complaint. David Parnas argued in 1986 "
        "that no real software project follows a rational design "
        "process, but that we should nevertheless *fake one in the "
        "documentation* so that the artifact we leave behind is "
        "understandable to future maintainers "
        "{cite}`parnas1986rational`. Seventeen years later, "
        "Lethbridge, Singer and Forward surveyed working engineers "
        "and found the expected gap: engineers acknowledge that "
        "documentation is important and simultaneously admit they "
        "rarely read it, rarely trust it, and routinely treat source "
        "code and personal conversations as their primary sources of "
        "truth {cite}`lethbridge2003software`. Another sixteen years "
        "on, Aghajani and colleagues systematically catalogued the "
        "documentation issues that show up in issue trackers and "
        "found — unsurprisingly — that staleness, completeness gaps, "
        "and wrong-audience material dominate the list "
        "{cite}`aghajani2019software`."
    ): (
        "这不是一个新鲜的抱怨。"
        "David Parnas 早在 1986 年就指出，"
        "没有哪个真实的软件项目真的按“理性设计过程”推进，"
        "但我们至少应该*在文档里把它装成是按这样推进的*，"
        "好让留给未来维护者的那份产物有人看得懂 "
        "{cite}`parnas1986rational`。"
        "十七年后，Lethbridge、Singer 和 Forward 调研一线工程师，"
        "得到了预料之中的鸿沟："
        "工程师一方面承认文档很重要，"
        "另一方面承认自己几乎不看、几乎不信，"
        "并且常规性地把源码和私下交流当成真理的首选来源 "
        "{cite}`lethbridge2003software`。"
        "又过了十六年，"
        "Aghajani 等人系统梳理了 issue 跟踪系统里的文档问题，"
        "毫不意外地发现："
        "过期、不完整、面向错误读者 —— "
        "这三类占了清单的大头 "
        "{cite}`aghajani2019software`。"
    ),
    (
        "Forty years, three papers, one uncomfortable pattern: we "
        "have known about this problem longer than many current "
        "engineers have been alive, and we still do not solve it. "
        "What has changed, recently, is the economics of *not asking "
        "humans to write the KB in the first place.* Three forces "
        "compound. Embedding-model prices dropped roughly 5× in a "
        "single release cycle in early 2024 — OpenAI's "
        "`text-embedding-3-small` at US \\$0.00002 per 1K tokens is "
        "the public marker, and open-weights models such as BGE "
        "{cite}`xiao2024bge` remove the per-token cost entirely on a "
        "modest GPU. Tree-sitter {cite}`brunsfeld2018treesitter` "
        "parses a mid-sized repository on a laptop in single-digit "
        "seconds, across a dozen languages, without a build system. "
        "Large language models have made the *generation* side of "
        "retrieval-augmented workflows accessible to any team that "
        "can write a prompt. The three together turn the question on "
        "its head: it stops being \"can we afford to write a KB\" "
        "and becomes \"can we afford *not* to derive one\" "
        "{cite}`openai_embeddings_v3`."
    ): (
        "四十年、三篇论文，指向同一个尴尬的模式："
        "这个问题存在的时间，"
        "比很多在职工程师的年龄都长，"
        "而我们至今没解决它。"
        "真正最近发生变化的，"
        "是 *“一开始就不要求人类去写知识库”* 的那本经济账。"
        "三股力量叠加："
        "2024 年初，embedding 模型的价格在一个发布周期里直接砍到五分之一 —— "
        "OpenAI 的 `text-embedding-3-small` 每 1K token 只要 US \\$0.00002，"
        "是公开的价格标尺；"
        "像 BGE 这样的开放权重模型 {cite}`xiao2024bge` "
        "更是直接把每 token 成本压到零 —— 一块普通 GPU 就够了。"
        "Tree-sitter {cite}`brunsfeld2018treesitter` "
        "在一台笔记本上就能用个位数秒数解析一个中等仓库，"
        "跨十几种语言、完全不依赖项目的构建系统。"
        "大语言模型则把检索增强工作流的 *生成* 那一端，"
        "交到了任何一个会写 prompt 的团队手里。"
        "三者合一，把问题整个翻了过来："
        "原先问的是“我们能不能负担得起去写一个知识库”，"
        "现在问的是“我们能不能负担得起 *不去* 推导出一个知识库” "
        "{cite}`openai_embeddings_v3`。"
    ),
    # ---- Chapter-level mindmap intro (sits above `## Why`) ----
    (
        "This chapter on one page — four kinds of material, four "
        "properties, two reference implementations, and three forces "
        "that changed the economics:"
    ): (
        "本章全貌，一页看完 —— "
        "四类材料、四条性质、两个参考实现，"
        "外加三股改变了这件事经济账的力量："
    ),
    # ---- What ----
    "What": "是什么",
    (
        "A **software knowledge base** in this book is the union of "
        "the answers a team needs in order to do its work, stored "
        "somewhere those answers can be retrieved with high precision "
        "and verifiable provenance. Concretely, that union contains "
        "at least four kinds of material:"
    ): (
        "本书口径下的**软件知识库**，"
        "是一个团队为完成本职工作所需要的各种答案的并集，"
        "存在某个能以高精度、可验证来源的方式被检索到的地方。"
        "具体来说，这个并集至少包含四类材料："
    ),
    (
        "**Code and its structure** — the files, functions, classes, "
        "call graphs, and type signatures that answer questions like "
        "*\"where is `runSync` called from\"* without a human "
        "interpreting. The repository is the authoritative source; "
        "the KB's job is to make it queryable."
    ): (
        "**代码及其结构** —— "
        "文件、函数、类、调用图、类型签名，"
        "能在不需要人来解释的情况下回答诸如 "
        "*“`runSync` 是从哪里被调用的”* 这类问题。"
        "代码仓库是权威来源，"
        "知识库的任务是让它“可查询”。"
    ),
    (
        "**Prose** — the tutorials, how-to articles, reference "
        "pages, and explanations that answer *\"how do I do X\"* and "
        "*\"what does this module actually mean\"*, classified by "
        "Diátaxis type {cite}`procida_diataxis` (see Chapter 3)."
    ): (
        "**文本** —— "
        "教程、how-to 文章、参考页、解释性文章，"
        "回答的是 *“我该怎么做 X”* 以及 *“这个模块到底在讲什么”*，"
        "按 Diátaxis 类型 {cite}`procida_diataxis` 分类（见第 3 章）。"
    ),
    (
        "**Decisions** — Architecture Decision Records "
        "{cite}`nygard_adr,madr` that answer *\"why is it this way "
        "and not some other way.\"* Crucially, an ADR records the "
        "alternatives that were rejected and who was in the room "
        "when the call was made. ADRs are the part of the KB that "
        "survives re-orgs."
    ): (
        "**决策** —— "
        "Architecture Decision Records（ADR）"
        "{cite}`nygard_adr,madr` —— "
        "回答的是 *“为什么是这样，而不是别的样子。”* "
        "关键在于："
        "一份 ADR 会记录下被否决掉的那些备选方案，"
        "以及当时谁在场做出的决定。"
        "ADR 是知识库里在组织架构调整后仍然能活下来的那一部分。"
    ),
    (
        "**Runbooks and ops lore** — how to deploy, how to debug, "
        "what an alert at 3 a.m. actually means, and who to page "
        "when it does."
    ): (
        "**Runbook 与运维经验** —— "
        "怎么发布、怎么排障、"
        "凌晨三点那条告警到底意味着什么、以及此时该呼谁。"
    ),
    (
        "We will call the whole thing a *KB* for short. It is not a "
        "wiki, not an issue tracker, not a chat search. It is the "
        "union of those, organized so that both humans and agents "
        "can ask it questions and get grounded answers."
    ): (
        "下文我们把这一整套东西简称为 *KB*（知识库）。"
        "它不是 wiki，不是工单系统，不是聊天搜索，"
        "它是这三者的并集 —— "
        "只是被重新组织成一种结构："
        "人和 agent 都可以向它提问、并得到有来源支撑的答案。"
    ),
    (
        "A KB in the sense of this book has four properties, each "
        "earning its own chapter later: it is **queryable** "
        "(retrieval works), has **provenance** (every fact points to "
        "a file, a commit, or an ADR), is **layered** "
        "(machine-generated content sits next to hand-written "
        "content and the two are distinguishable), and is **honest** "
        "(when the KB does not know, the KB says so). Provenance is "
        "Chapter 5, layering is Chapter 18, honesty is Chapter 13, "
        "and queryability is most of Part III."
    ): (
        "本书口径下的知识库有四条性质，"
        "后面每一条都会有一整章来展开："
        "它**可查询（queryable）**，"
        "即检索是真的能用的；"
        "它有**溯源（provenance）**，"
        "每一条事实都指向某个文件、某个 commit、或某份 ADR；"
        "它是**分层的（layered）**，"
        "机器生成内容和人工撰写内容可以挨在一起，但两者可区分；"
        "它是**诚实的（honest）**，"
        "知识库不知道某件事的时候，它会说自己不知道。"
        "溯源是第 5 章、"
        "分层是第 18 章、"
        "诚实是第 13 章，"
        "可查询性贯穿整个第三部分的大部分章节。"
    ),
    # ---- How ----
    "How": "怎么做",
    (
        "The next twenty-three chapters are an implementation of "
        "those four properties on top of two real reference systems "
        "the author uses daily:"
    ): (
        "后面二十三章，"
        "就是在作者日常使用的两个真实参考系统之上，"
        "实现这四条性质："
    ),
    (
        "**The prose-layer reference implementation** — a file-based "
        "wiki that handles prose, decisions, and runbooks. It is the "
        "repository you are reading this book inside."
    ): (
        "**文本层参考实现** —— "
        "一个基于文件的 wiki，"
        "负责承载文本、决策和 runbook。"
        "它就是你现在读到的这本书所在的那个仓库。"
    ),
    (
        "**The code-layer reference implementation** — a companion "
        "service that handles code structure via tree-sitter parsing "
        "{cite}`brunsfeld2018treesitter`, a property graph stored in "
        "Memgraph, and dense embeddings stored in pgvector."
    ): (
        "**代码层参考实现** —— "
        "一个配套的伴随服务，"
        "用 tree-sitter {cite}`brunsfeld2018treesitter` 做代码解析、"
        "把属性图存进 Memgraph、"
        "把稠密 embedding 存进 pgvector。"
    ),
    (
        "Neither system is new or experimental. What the book adds "
        "is **the missing tissue between them**: the IR theory "
        "(Chapter 2), the doc-type taxonomy (Chapter 3), the "
        "provenance discipline (Chapter 5), the document-layer model "
        "(Chapter 18), and the evaluation and operations practice "
        "(Part IV)."
    ): (
        "这两套系统都不算新，也不算实验性。"
        "本书真正要补上的是**它们之间那块缺失的结缔组织**："
        "IR 理论（第 2 章）、"
        "文档类型分类学（第 3 章）、"
        "溯源纪律（第 5 章）、"
        "文档分层模型（第 18 章），"
        "以及评估与运维实践（第四部分）。"
    ),
    (
        "The system this book describes is **strictly more flexible "
        "and strictly more work** than a hosted service. That is the "
        "honest trade-off; different teams will pick different sides "
        "of it. The most visible hosted alternative today is "
        "**DeepWiki** {cite}`cognition_deepwiki`, a closed-source "
        "SaaS that auto-generates wiki-style pages for any public "
        "GitHub repository. DeepWiki's output is frequently "
        "impressive as a reading experience, and the source blog "
        "post is titled \"give your repo its own DeepWiki\" "
        "{cite}`fanyamin2026deepwiki` for that reason. What DeepWiki "
        "does not give you is ownership of the pipeline, control "
        "over the document-type taxonomy, a place to put ADRs, or "
        "the ability to hook the KB up to your team's IDE agents on "
        "your own terms. Other systems in this space — Sourcegraph "
        "Cody {cite}`sourcegraph_cody` for code-level Q&A, Notion AI "
        "{cite}`notion_ai` for prose-level Q&A — each solve a "
        "*piece* of the problem well. The book's angle is that the "
        "pieces belong together, and that building the integrated "
        "version is now affordable."
    ): (
        "本书描述的这套系统，"
        "和一个托管服务相比，"
        "是**严格更灵活、也严格更费力**的。"
        "这就是摆在台面上的取舍，"
        "不同的团队会倒向不同的一边。"
        "今天最显眼的托管替代品是 **DeepWiki** {cite}`cognition_deepwiki` —— "
        "一个闭源 SaaS，"
        "能自动为任何一个公开 GitHub 仓库生成 wiki 风格的页面。"
        "作为阅读体验，DeepWiki 的输出经常令人印象深刻，"
        "本书的底稿博客之所以叫"
        "“给代码仓库造一个 DeepWiki” {cite}`fanyamin2026deepwiki`，"
        "原因也正是如此。"
        "DeepWiki 给不了你的是：流水线的所有权、"
        "文档类型分类的控制权、"
        "放置 ADR 的地方，"
        "以及按你自己的条款把知识库接入团队 IDE agent 的能力。"
        "这个空间里还有另一些系统："
        "代码级问答的 Sourcegraph Cody {cite}`sourcegraph_cody`，"
        "文本级问答的 Notion AI {cite}`notion_ai` —— "
        "它们各自把问题中的 *一块* 解决得很好。"
        "本书的观点是："
        "这些块本就该连在一起，"
        "而把它们组合成一个一体化版本，今天是负担得起的。"
    ),
    "Who this book is for": "这本书是写给谁的",
    (
        "This book assumes a team that owns a real codebase (on the "
        "order of 50k lines and up, three or more engineers, at "
        "least a year of history), is willing to run a small Docker "
        "Compose stack and pay for embedding-model calls in the low "
        "single-digit dollars per full sync, and wants to keep the "
        "pipeline on-premises or on its own cloud account rather "
        "than hand it to a vendor. If you can describe your "
        "documentation problem in one sentence and a page of "
        "DokuWiki would close it, this book is overkill. If your "
        "codebase has grown past the point where any one person "
        "holds it all in their head, this book is the cheap option."
    ): (
        "本书假设的读者是这样一个团队："
        "手里有一个真实的代码库（大约 5 万行以上、三个或以上工程师、至少一年的历史），"
        "愿意跑一套不大的 Docker Compose 栈、"
        "愿意为 embedding 模型调用掏每次全量同步几美元以内的钱，"
        "并且希望把整条流水线留在本地或自己的云账号里，而不是交给某个厂商。"
        "如果你可以用一句话描述你的文档问题、"
        "再写一页 DokuWiki 就能收尾，"
        "那这本书对你而言是杀鸡用牛刀。"
        "如果你的代码库已经大到没有任何一个人能全部装进脑子，"
        "那这本书就是最便宜的那个选项。"
    ),
    # ---- Example ----
    "Example": "示例",
    (
        "Here is the shape of what we want \"using the KB\" to feel "
        "like by the end of Part V. The new-hire's question — "
        "*\"where is `runSync` called from, and why does its `defer` "
        "include a `recover`?\"* — should produce an answer with the "
        "structure shown below. The repository names, line numbers, "
        "commit, and ADR in the block are **an illustrative "
        "mock-up**; Appendix B reproduces an answer of exactly this "
        "shape against a real codebase using a real HTTP call, and "
        "Chapter 13 explains how the confidence line is computed."
    ): (
        "下面是我们希望在第五部分末尾，"
        "“使用知识库”应该有的体感。"
        "新人的那个问题 —— "
        "*“`runSync` 是从哪里被调用的、"
        "它的 `defer` 为什么要 `recover`？”* —— "
        "应当产生下面这样结构的回答。"
        "下方代码块里的仓库名、行号、commit 和 ADR，"
        "**只是一个用来说明的占位样例**；"
        "附录 B 会用真实代码库、一次真实的 HTTP 调用，"
        "复现一份严格是这种形状的回答，"
        "第 13 章则会解释最后那一行置信度是怎么算出来的。"
    ),
    # Code block — msgid has literal newlines; translation must match
    # exactly (code is rendered verbatim).
    (
        "runSync is called from 4 sites:\n"
        "  - internal/worker/pool.go:142  (Pool.dispatch)\n"
        "  - internal/worker/pool.go:287  (Pool.drainOnShutdown)\n"
        "  - cmd/sync/main.go:58          (runCLISync)\n"
        "  - internal/test/integration.go:31 (harness)\n"
        "\n"
        "The defer/recover pattern was added in commit 4a1c92b\n"
        "(\"handle panic in sync goroutine without killing the pool\", "
        "2024-03-02)\n"
        "and is discussed in ADR-0014 (\"Panic-safety in worker "
        "pools\"):\n"
        "> We chose to recover and log because a panic in a single "
        "sync target\n"
        "> must not take down sibling targets; see incident "
        "I-2024-02-17.\n"
        "\n"
        "Confidence: high (4 citations; ADR present; call graph up "
        "to date\n"
        "as of commit 4a1c92b).\n"
    ): (
        "runSync is called from 4 sites:\n"
        "  - internal/worker/pool.go:142  (Pool.dispatch)\n"
        "  - internal/worker/pool.go:287  (Pool.drainOnShutdown)\n"
        "  - cmd/sync/main.go:58          (runCLISync)\n"
        "  - internal/test/integration.go:31 (harness)\n"
        "\n"
        "The defer/recover pattern was added in commit 4a1c92b\n"
        "(\"handle panic in sync goroutine without killing the pool\", "
        "2024-03-02)\n"
        "and is discussed in ADR-0014 (\"Panic-safety in worker "
        "pools\"):\n"
        "> We chose to recover and log because a panic in a single "
        "sync target\n"
        "> must not take down sibling targets; see incident "
        "I-2024-02-17.\n"
        "\n"
        "Confidence: high (4 citations; ADR present; call graph up "
        "to date\n"
        "as of commit 4a1c92b).\n"
    ),
    (
        "The shape is what matters. In the real system each of those "
        "citations is a `file:line` anchor resolved from the call "
        "graph at the current commit, not a paraphrase from a "
        "training corpus. The confidence line is mechanical: it "
        "counts citations, checks whether an ADR is attached, and "
        "compares the KB's `last_synced_commit` to `git HEAD`. If "
        "the answer cannot meet its own bar, the KB is allowed — and "
        "required — to say so (Chapter 13)."
    ): (
        "真正重要的是这种形状。"
        "在真实系统里，"
        "上面那些引用每一条都是一条 `file:line` 锚 —— "
        "由当前 commit 上的调用图解析得到，"
        "不是从训练语料里“复述”出来的。"
        "最后那一行置信度是机械计算出来的："
        "数一下引用数量、"
        "检查有没有挂 ADR、"
        "比较一下知识库的 `last_synced_commit` 和 `git HEAD`。"
        "如果答案过不了它自己这一关，"
        "知识库被允许 —— 而且被要求 —— 直接说出来（第 13 章）。"
    ),
    (
        "The machinery that produces this kind of answer is the "
        "subject of Parts III through V. The ingredient list, "
        "however, is only four items long: tree-sitter, an embedding "
        "model, a graph store, and a disciplined prompt. Those are "
        "the four corners the blog post {cite}`fanyamin2026deepwiki` "
        "names as 四件套 (\"the four-piece set\"), and the book "
        "spends the middle chapters picking each corner apart."
    ): (
        "产生这种回答的机器，"
        "是第三到第五部分的主题。"
        "而它的配料表只有四项："
        "tree-sitter、一个 embedding 模型、一个图存储、"
        "以及一套有纪律的 prompt。"
        "这四样就是底稿博客 {cite}`fanyamin2026deepwiki` "
        "里叫作“四件套”的东西，"
        "本书中段的若干章节就是在把这四个角一个一个拆开来看。"
    ),
    # ---- Conclusion ----
    "Conclusion": "小结",
    (
        "The gap between \"the codebase\" and \"what the team needs "
        "to know about the codebase\" is older than most of the "
        "current software stack. It has outlasted CVS, Subversion, "
        "and three generations of wiki software. What has finally "
        "shifted is the cost of *deriving* a KB from artefacts we "
        "already have, rather than asking humans to hand-write one "
        "in parallel with their actual work. The rest of this book "
        "is a concrete recipe for that derivation, written with "
        "enough citations and code that a reader can, if they want, "
        "rebuild the whole thing and then replace every piece they "
        "disagree with."
    ): (
        "“代码库”和“团队需要知道的关于代码库的那些事” —— "
        "这两者之间的鸿沟，"
        "比今天大部分软件技术栈都老。"
        "它熬死了 CVS、熬死了 Subversion、"
        "熬过了三代 wiki 软件。"
        "真正终于在动的，"
        "是*从已有工件推导出一个知识库*的成本 —— "
        "而不是要求人类在做真正的工作的同时，"
        "再并行手写一份出来。"
        "本书后面的章节，"
        "就是这条推导的具体做法："
        "配上足够多的引文和代码，"
        "让一个读者 —— 如果他愿意 —— "
        "可以把整套东西重搭一遍，"
        "然后把他不同意的每一块替换掉。"
    ),
    "References": "参考文献",
}
