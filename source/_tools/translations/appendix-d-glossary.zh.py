"""Chinese translations for source/appendix-d-glossary.md.

Design rules for this file:

1. **Term heads stay in English.** MyST glossary cross-references
   (`{term}`ADR`` across the book) resolve on the definition-list
   term, not on its translation. Translating "ADR" to "架构决策记录"
   would silently break ~20 cross-references across Parts II-VI.
   For terms that are already Chinese-friendly as English acronyms
   (ADR, BM25, HNSW, KB, MCP, MyST, PKB, RAG, RRF, tree-sitter) we
   therefore *keep the head verbatim* and only translate the body.
2. **Prose/Document heads keep the ``(zh: ...)`` suffix.** This is a
   deliberate bilingual signpost; the English edition benefits from
   it too.
3. **Citations and inline code survive round-trips.** ``{cite}`key```
   and backticked identifiers are copied verbatim — no localisation.
4. **CJK emphasis.** When ``*`` / ``**`` sit next to a Chinese
   character, an ASCII space separates them (CommonMark requirement;
   see ch02-ir-rag-primer.zh.py for the full style guide).
"""

PO_PATH = "appendix-d-glossary.po"

TRANSLATIONS: dict[str, str] = {
    "Appendix D — Glossary": "附录 D —— 术语表",

    # --- Translator's note -------------------------------------------------

    (
        "**Translator's note on *prose* vs. *document*.** English has two "
        "perfectly good words that English-speaking engineers do not usually "
        "conflate: *prose* (the human-authored narrative content) and "
        "*document* (the file object that carries content, which may be "
        "prose or code or both). Chinese-language software engineering tends "
        "to flatten both words to 「文档」 , which collapses a distinction "
        "this book relies on throughout Parts II and III. The Chinese "
        "edition therefore adopts the convention:"
    ): (
        "**译者按：关于 *prose* 与 *document* 。** "
        "英文里有两个**意思完全不一样**的词 —— "
        "一个是 *prose* （**人写的叙述性内容本身**），"
        "一个是 *document* （**承载内容的文件对象** —— "
        "里面可以是 prose、可以是代码、也可以二者皆有）—— "
        "**英文工程界并不把这两个词混为一谈**。"
        "而中文软件工程界的习惯是**把两者一并压扁成**「文档」 —— "
        "这会**直接踩塌**本书第二、三部分都依赖的一个区分。"
        "因此，中文版采用以下约定："
    ),

    "**prose → 文稿** (the narrative content itself; 文稿层 = the prose layer)": (
        "**prose → 文稿** （叙述性内容本身；**文稿层** = prose layer）"
    ),

    (
        "**document → 文档** (the file object, Diátaxis category, or "
        "classified artefact — as in document-layering)"
    ): (
        "**document → 文档** （文件对象、Diátaxis 分类、"
        "或被分级的制品 —— 例如 document-layering 中的 document）"
    ),

    "**documentation → 文档工作 / 文档体系** (the engineering activity)": (
        "**documentation → 文档工作 / 文档体系** （作为一项**工程活动**）"
    ),

    (
        "Every glossary entry and cross-reference below honours this "
        "distinction; watch for it in particular in *Prose*, *Document*, "
        "and *L0–L4*."
    ): (
        "下面每一条术语和交叉引用都**遵循这套区分**；"
        "特别留意 *Prose* 、 *Document* 、以及 *L0–L4* 这三条。"
    ),

    # --- Glossary term heads (kept English; see file docstring) -----------

    "ADR": "ADR",
    "BM25": "BM25",
    "Diátaxis": "Diátaxis",
    "Entity": "Entity",
    "HNSW": "HNSW",
    "KB": "KB",
    "L0–L4": "L0–L4",
    "Layer tuple": "Layer tuple",
    "L1 / L2 / L3 (update strategy)": "L1 / L2 / L3 （更新策略）",
    "MCP": "MCP",
    "MyST": "MyST",
    "PKB": "PKB",
    "PKB-metadata footer": "PKB 元数据页脚",
    "Prose (zh: 文稿)": "Prose / 文稿",
    "Document (zh: 文档)": "Document / 文档",
    "RAG": "RAG",
    "RRF": "RRF",
    "tree-sitter": "tree-sitter",

    # --- Glossary definitions ---------------------------------------------

    (
        "Architecture Decision Record. A short, append-only document "
        "that records the context, decision, and consequences of a "
        "single architectural choice. See MADR for a specific "
        "template. {cite}`nygard_adr` {cite}`madr`"
    ): (
        "**架构决策记录**（Architecture Decision Record）。一份"
        "**简短、只追加**的文档，记录**单一架构决策**的背景、"
        "决策本身、以及其后果。MADR 是一个具体的模板。 "
        "{cite}`nygard_adr` {cite}`madr`"
    ),

    (
        "A tf-idf-descended ranking function widely used in full-text "
        "search. {cite}`robertson2009probabilistic`"
    ): (
        "一族**从 tf-idf 发展而来**的排序函数，在全文检索里"
        "广泛使用。 {cite}`robertson2009probabilistic`"
    ),

    (
        "A four-type documentation taxonomy (Tutorial, How-to, "
        "Reference, Explanation) used throughout Part II. "
        "{cite}`procida_diataxis`"
    ): (
        "一种把文档分为**四类**的分类法 —— 教程（Tutorial）、"
        "操作指南（How-to）、参考（Reference）、解释（Explanation）—— "
        "第二部分通篇使用。 {cite}`procida_diataxis`"
    ),

    (
        "In the Code Knowledge Graph, a hashable unit — file, function, "
        "class, package — with a stable content-addressed ID."
    ): (
        "在**代码知识图谱**（Code Knowledge Graph）中，一个"
        "**可哈希的单元** —— 文件、函数、类、包 —— "
        "拥有稳定的、**内容寻址**的 ID。"
    ),

    (
        "Hierarchical Navigable Small World. The ANN index backing "
        "most modern vector stores, including pgvector. "
        "{cite}`malkov2020hnsw`"
    ): (
        "**Hierarchical Navigable Small World**（分层可导航小世界）。"
        "一种**近似最近邻**（ANN）索引，是当下多数向量存储"
        "（包括 pgvector）**底层采用的算法**。 "
        "{cite}`malkov2020hnsw`"
    ),

    (
        "Knowledge Base. In this book, the union of prose, code, "
        "embeddings, and graph that a team queries to do its job."
    ): (
        "**知识库**（Knowledge Base）。在本书中，指一个团队为了完成"
        "日常工作而查询的**文稿、代码、向量、以及图**的并集。"
    ),

    (
        "The five-tier document-layer model introduced in Chapter 18 "
        "(L0 code and comments; L1 committed human prose such as ADRs; "
        "L2 collaborative human prose such as wiki pages; L3 reviewed "
        "AI-drafted prose; L4 unreviewed AI drafts). Chapter 18 "
        "upgrades the single-axis model to the four-tuple "
        "⟨L, U, R, S⟩."
    ): (
        "第 18 章引入的**五层文档模型** —— L0 代码与注释；"
        "L1 已提交的人写文稿（如 ADR）；L2 协作式人写文稿（如 wiki 页面）；"
        "L3 经人复核的 AI 草稿；L4 未经复核的 AI 草稿。第 18 章把这个"
        "**单轴模型**升级为四元组 ⟨L, U, R, S⟩ 。"
    ),

    (
        "The four-valued classification ⟨L, U, R, S⟩ — document "
        "layer, updated-by, review-status, review-score — introduced "
        "in Chapter 18 as the operational replacement for single-axis "
        "document tiering."
    ): (
        "**四元分级** ⟨L, U, R, S⟩ —— 文档层（Layer）、由谁更新"
        "（Updated-by）、复核状态（Review-status）、复核评分"
        "（Review-score）—— 第 18 章引入，**在工程上替代**单轴文档分级。"
    ),

    (
        "The three update levels from Chapter 16. **L1 mechanical**: "
        "rules only, zero LLM tokens. **L2 bounded-LLM**: one page's "
        "body plus one diff fed to an LLM, bounded to a few "
        "kilobytes. **L3 human-led**: human writes, LLM copy-edits. "
        "Not to be confused with the document-layer L0–L4 above; the "
        "number line is different."
    ): (
        "第 16 章提出的**三级更新策略**。 **L1 机械式** ："
        "**只走规则**，零 LLM token。 **L2 受控 LLM** ："
        "**只喂一页正文加一份 diff** 给 LLM，总量控制在几 KB 以内。 "
        "**L3 人主导** ：**人来写**，LLM 做文字润色。**切勿**与上面的"
        "文档层 L0–L4 混淆 —— 两条数轴**不是一回事**。"
    ),

    (
        "Model Context Protocol — the standard the book uses to let "
        "IDE agents query the KB. {cite}`mcp_spec`"
    ): (
        "**Model Context Protocol** —— 本书选用的标准协议，用来让"
        "**IDE 里的 agent** 查询知识库。 {cite}`mcp_spec`"
    ),

    (
        "Markedly Structured Text — the Markdown flavour Sphinx "
        "understands natively via `myst-parser`."
    ): (
        "**Markedly Structured Text** —— 一种 Markdown 方言，Sphinx "
        "通过 `myst-parser` **原生支持**。"
    ),

    (
        "Project Knowledge Base — a KB scoped to a single software "
        "project, in contrast to a team- or organisation-wide KB. "
        "This book's opinionated ten-page set (`00-overview` through "
        "`09-runbook`) is a typical PKB shape."
    ): (
        "**Project Knowledge Base** —— 范围**只覆盖单个软件项目**的"
        "知识库，与**团队级**或**组织级**知识库相对。本书推荐的"
        "**十页骨架**（从 `00-overview` 到 `09-runbook`）就是一个"
        "典型的 PKB 形态。"
    ),

    (
        "The HTML-comment block at the foot of every content page, "
        "carrying six fields (`last_updated`, `commit`, `updated_by`, "
        "`review_status`, `review_score`, `reviewed_by`). Introduced "
        "in Chapter 5 as the operational counterpart to the YAML "
        "frontmatter: frontmatter carries provenance (who created the "
        "page, at what commit); the footer carries review state (who "
        "signed off, with what score, when)."
    ): (
        "**每一页内容页底部**的一段 HTML 注释块，携带六个字段 —— "
        "`last_updated` 、`commit` 、`updated_by` 、`review_status` 、"
        "`review_score` 、`reviewed_by` 。第 5 章把它作为"
        "**与 YAML frontmatter 配对**的运维侧记录引入：frontmatter "
        "记录**来源**（谁在哪个 commit 创建了这页），页脚记录"
        "**复核状态**（谁、几分、何时签字）。"
    ),

    (
        "Human-authored narrative text — tutorials, how-tos, "
        "reference pages, explanations, ADRs, runbooks. In this "
        "book, *prose* is the material the **prose layer** (Part II) "
        "handles and is deliberately contrasted with *code* (which "
        "the **code layer** in Part III handles via parsing and "
        "embeddings). The distinction matters because prose has "
        "paragraphs as its natural chunking unit, drifts against the "
        "code it describes, and updates when a human decides it is "
        "wrong; code has functions as its natural unit, does not "
        "drift (it is the source of truth), and updates every "
        "commit. Chapter 8 opens with exactly this split. Contrast "
        "with *Document*."
    ): (
        "**人写的叙述性文本** —— 教程、how-to、参考页、解释、ADR、"
        "运维手册。在本书里， *prose* （**文稿**）是第二部分"
        "**文稿层**所处理的对象，**刻意与** *code* （**代码**）"
        "对照 —— 后者由第三部分的**代码层**通过解析和向量化处理。"
        "这个区分**之所以重要**，是因为文稿的**自然切块单位**是段落，"
        "它**相对于所描述的代码会漂移**，由人在**判断它不对**时更新；"
        "代码的自然单位是函数，**不会漂移**（它就是真理本身），"
        "**每一次 commit 都在更新**。第 8 章以**这一对比**开篇。"
        "与 *Document* 对照。"
    ),

    (
        "The *container* for content, independent of whether the "
        "content is prose or code. A markdown file with YAML "
        "frontmatter is a document; its body may be prose, a code "
        "block, or both. *Document-layering* (Chapter 18, L0–L4) "
        "classifies documents by provenance and authority, not by "
        "their internal content type. Rule of thumb: *prose* (文稿) "
        "when we mean the readable content, *document* (文档) when "
        "we mean the file object that carries it."
    ): (
        "**承载内容的容器** —— 与容器里装的是 prose 还是 code 无关。"
        "一个带 YAML frontmatter 的 markdown 文件就是一个 document；"
        "它的正文**可以是文稿**、**可以是一段代码**、也**可以两者都有**。 "
        "*Document-layering* （第 18 章， L0–L4 ）"
        "**按来源和权威度给 document 分级**，而**不是**按其内部的内容类型。"
        "**记忆口诀** ：当我们指**可读的内容本身**时，用 *prose* （文稿）；"
        "当我们指**承载它的那个文件对象**时，用 *document* （文档）。"
    ),

    (
        "Retrieval-Augmented Generation. The pattern of grounding an "
        "LLM's output in retrieved context. {cite}`lewis2020rag` "
        "{cite}`gao2023retrieval`"
    ): (
        "**检索增强生成**（Retrieval-Augmented Generation）。把 LLM "
        "的输出**锚定在被检索出来的上下文之上**的一种模式。 "
        "{cite}`lewis2020rag` {cite}`gao2023retrieval`"
    ),

    (
        "Reciprocal Rank Fusion. A rank-combination method used in "
        "hybrid retrieval. {cite}`cormack2009rrf`"
    ): (
        "**倒数排名融合**（Reciprocal Rank Fusion）。一种"
        "**把多路排序合并**的方法，在混合检索中常用。 "
        "{cite}`cormack2009rrf`"
    ),

    (
        "Incremental, multi-language parser powering the code-KB "
        "parse stage. {cite}`brunsfeld2018treesitter`"
    ): (
        "一个**增量式、多语言**的解析器，**支撑**代码知识库的"
        "解析阶段。 {cite}`brunsfeld2018treesitter`"
    ),

    "References": "参考文献",
}
