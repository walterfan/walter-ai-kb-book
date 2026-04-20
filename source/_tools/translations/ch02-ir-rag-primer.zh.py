"""Chinese translations for source/part1-foundations/ch02-ir-rag-primer.md.

Style guide for this chapter (and reused by later chapters):

- Keep English for widely-used technical terms and product names: BM25,
  RAG, GraphRAG, HippoRAG, HNSW, IVFFlat, pgvector, Elasticsearch,
  OpenSearch, Pinecone, Milvus, Qdrant, Weaviate, Solr, Lucene,
  Tantivy, Bleve, Kibana, Leiden, MCP, LLM, BEIR, RRF, DPR, ANN,
  TF-IDF, BGE, MTEB, voyage-code, tsvector, `drainOnShutdown`, etc.
- Translate the surrounding prose into idiomatic Chinese that matches
  the author's blog voice (punchy, concrete, mildly sardonic).
- Preserve {cite}`key` directives, backticks, *emphasis*, **strong**,
  and the table-cell structure exactly — they are format tokens, not
  prose.
- Use Chinese typographic quotes (“ ”) and full-width punctuation in
  flowing prose, but keep half-width punctuation inside code spans.
- IMPORTANT — CommonMark's emphasis rules require ASCII whitespace or
  punctuation on at least one side of a `*` delimiter, and CJK
  characters do NOT count. When a span of italic prose sits between
  two CJK characters, insert a single ASCII space outside each `*`
  (e.g. write `中文 *italic bit* 中文` rather than
  `中文*italic bit*中文`); MyST will render the emphasis correctly
  and the extra space disappears after CJK justification.
"""

PO_PATH = "part1-foundations/ch02-ir-rag-primer.po"

TRANSLATIONS: dict[str, str] = {
    # ---------------------------------------------------------------
    # Title + Why
    # ---------------------------------------------------------------
    "Chapter 2 — An IR and RAG Primer": "第 2 章 —— IR 与 RAG 入门",
    "Why": "为什么",
    (
        "\"Retrieval-Augmented Generation\" is often described in two "
        "sentences: *chunk your documents, embed the chunks, take the "
        "top-k nearest neighbours of the user's query, paste them into "
        "the prompt.* This description is not wrong, exactly. It is "
        "instead the shortest possible description, and it lands in the "
        "same unlucky cognitive spot as \"a car is four wheels and an "
        "engine\" — technically accurate, useless for debugging."
    ): (
        "“检索增强生成”（Retrieval-Augmented Generation）通常被浓缩成两句话："
        "*把文档切块、给每块算 embedding、取用户查询的 top-k 最近邻、"
        "拼进 prompt。* 这种说法不能说错，只能说它是能给出的最短说法，"
        "而且恰好掉进了“汽车就是四个轮子加一台发动机”那种认知陷阱 —— "
        "技术上挑不出毛病，但在排查问题时一点用都没有。"
    ),
    (
        "The deeper lesson behind that description is one that a "
        "practitioner learns the hard way: *the hardest part of a "
        "knowledge base is not writing it, it is making it findable, "
        "usable, and up-to-date* {cite}`fanyamin2026kb_pipeline`. Every "
        "section of this chapter is, under the surface, a piece of that "
        "one sentence. Findable is retrieval. Usable is fusion and "
        "evaluation. Up-to-date is every failure mode that is "
        "downstream of a stale index."
    ): (
        "这句定义背后藏着一条工程师只能用教训换来的道理："
        "*知识库最难的不是“写出来”，而是“找得到、用得上、跟得上”* "
        "{cite}`fanyamin2026kb_pipeline`。"
        "本章的每一节，归根结底都是在拆解这一句。"
        "“找得到”对应检索；“用得上”对应融合与评估；"
        "“跟得上”对应索引过期之后各种下游的故障模式。"
    ),
    (
        "Information retrieval as a field is roughly sixty years old "
        "{cite}`manning2008introduction`. It has accumulated a "
        "vocabulary, a set of evaluation disciplines, and a long "
        "catalogue of failure modes that every practical knowledge base "
        "rediscovers the hard way if the designers have not read them "
        "first. This chapter gives the minimum IR / RAG vocabulary the "
        "rest of the book assumes, then does three things most short "
        "RAG primers skip: it lists vanilla RAG's failure modes "
        "honestly, introduces GraphRAG as a serious alternative for one "
        "specific class of those failures, and closes with a judgment "
        "matrix for picking a retrieval substrate — full-text, "
        "pgvector, Elasticsearch, or a specialised vector store "
        "{cite}`fanyamin2026elasticsearch_rag` "
        "{cite}`fanyamin2026pgvector_rag`. Readers already fluent in "
        "BM25, dense retrieval, hybrid retrieval, the GraphRAG "
        "literature, and substrate trade-offs can skim this chapter for "
        "notation and move on."
    ): (
        "信息检索（IR）作为一个学科，大约已经有六十年的历史 "
        "{cite}`manning2008introduction`，"
        "积累下一整套术语、一整套评估方法，"
        "以及一份很长的失败模式清单 —— "
        "设计者要是没先读过这份清单，每一个落地的知识库都会把这些坑重新踩一遍。"
        "本章先给出全书后文会默认你掌握的最小 IR / RAG 词汇表，"
        "再做三件大多数 RAG 短文会跳过的事："
        "诚实地列出 vanilla RAG 的失败模式、"
        "把 GraphRAG 作为其中一类失败的严肃替代方案介绍给你、"
        "最后用一张判断矩阵告诉你怎么选检索底座 —— 全文搜索、pgvector、"
        "Elasticsearch，还是专用向量数据库 "
        "{cite}`fanyamin2026elasticsearch_rag` "
        "{cite}`fanyamin2026pgvector_rag`。"
        "对 BM25、稠密检索、混合检索、GraphRAG 文献以及底座取舍已经熟悉的读者，"
        "可以直接翻过去，只留意记号即可。"
    ),
    # ---------------------------------------------------------------
    # What — intro
    # ---------------------------------------------------------------
    # ---- Chapter-level mindmap intro (sits above `## Why`) ----
    (
        "This chapter on one page — the retrieval primitives, the "
        "RAG pipeline, the failure modes that motivate everything "
        "beyond vanilla RAG, GraphRAG as a structural alternative, "
        "and the substrate-choice matrix that translates these ideas "
        "into deployment decisions:"
    ): (
        "本章全貌，一页看完 —— "
        "检索原语、RAG 流水线、"
        "一份解释“为什么朴素 RAG 之外的一切都是有原因的”的失败模式清单、"
        "作为结构性替代的 GraphRAG，"
        "以及把这些概念翻译成部署决策的底座选择矩阵："
    ),
    "What": "是什么",
    (
        "Six terms carry almost all the weight in the rest of the "
        "book; defining them once precisely makes later chapters much "
        "shorter. Two more terms — the failure mode catalogue for RAG, "
        "and GraphRAG — carry most of the weight of the debates you "
        "will find in the literature."
    ): (
        "六个术语撑起了全书后文几乎所有的重量；"
        "在这里精确地定义一次，后面的章节就能少写很多铺垫。"
        "再加两个术语 —— RAG 的失败模式清单以及 GraphRAG —— "
        "就撑起了你在文献里会看到的大部分争论。"
    ),
    # ---------------------------------------------------------------
    # BM25
    # ---------------------------------------------------------------
    "Lexical retrieval: TF-IDF and BM25": "词法检索：TF-IDF 与 BM25",
    (
        "Lexical retrieval scores a document against a query as a "
        "function of *which query terms appear*, *how often they "
        "appear* (term frequency), and *how unusual they are across the "
        "corpus* (inverse document frequency). TF-IDF is the original "
        "formulation {cite}`manning2008introduction`; BM25 is the "
        "workhorse refinement that every modern full-text search engine "
        "— Lucene, Elasticsearch, Tantivy, PostgreSQL's `tsvector`, "
        "Bleve — ultimately descends from "
        "{cite}`robertson2009probabilistic`. For code KBs, BM25 over "
        "identifiers remains surprisingly strong: identifiers carry a "
        "lot of signal, and a well-tokenised BM25 index routinely beats "
        "a poorly-tuned embedding model on exact-symbol lookups such as "
        "*\"find all call sites of `runSync`\"*."
    ): (
        "词法检索为文档对查询打分，依据三件事："
        "*哪些查询词出现*、*出现了几次*（term frequency，词频）、"
        "以及*它们在整个语料里有多罕见*（inverse document frequency，逆文档频率）。"
        "TF-IDF 是最早的公式 {cite}`manning2008introduction`；"
        "BM25 则是那个被一线打磨出来的改进版 —— 现代所有主流全文搜索引擎 "
        "（Lucene、Elasticsearch、Tantivy、PostgreSQL 的 `tsvector`、Bleve）"
        "归根结底都是 BM25 的衍生 {cite}`robertson2009probabilistic`。"
        "在代码知识库这个场景里，基于标识符的 BM25 强得意外："
        "标识符本身就带着很强的信号，"
        "一个分词分得好的 BM25 索引，"
        "在 *“找出 `runSync` 的所有调用点”* 这类精确符号查询上，"
        "常常能轻松打赢一个调得不好的 embedding 模型。"
    ),
    # ---- Formula + three design decisions + pathologies ----
    (
        "It is worth spending a page on *why* BM25 works, because most "
        "engineers use it through a library call and never see the "
        "shape of its answer. For a query $q$ made of terms $t_1, "
        "t_2, \\dots$, and a document $D$ with length $|D|$ in an "
        "index whose average document length is $\\text{avgdl}$, BM25 "
        "scores the pair as a sum over query terms:"
    ): (
        "花一页讲讲 *为什么* BM25 管用是值得的，"
        "因为大多数工程师是通过一次库函数调用见到 BM25 的，"
        "根本看不到它的答案形状。"
        "对于一个由词项 $t_1, t_2, \\dots$ 组成的查询 $q$，"
        "以及一篇长度为 $|D|$、所在索引的平均文档长度为 $\\text{avgdl}$ 的文档 $D$，"
        "BM25 给二者打的分是对查询词项的一个求和："
    ),
    # The display-math msgid is raw LaTeX; translate to itself so the
    # catalog reports 100% and the formula renders identically in both
    # builds. Sphinx never "translates" math, but an empty msgstr would
    # cause sphinx-intl to skip the block entirely; giving it back the
    # same string is the cleanest signal of "reviewed, no change".
    (
        "\n"
        "\\text{BM25}(q, D) \\;=\\; \\sum_{t \\in q}\n"
        "  \\underbrace{\\text{IDF}(t)}_{\\text{how rare is }t?}\n"
        "  \\;\\cdot\\;\n"
        "  \\underbrace{\\frac{f(t, D)\\,(k_1 + 1)}\n"
        "                   {f(t, D) + k_1\\!\\left(1 - b + b\\,\\frac{|D|}{\\text{avgdl}}\\right)}}_{\\text{saturating, length-normalised TF}}.\n"
    ): (
        "\n"
        "\\text{BM25}(q, D) \\;=\\; \\sum_{t \\in q}\n"
        "  \\underbrace{\\text{IDF}(t)}_{\\text{how rare is }t?}\n"
        "  \\;\\cdot\\;\n"
        "  \\underbrace{\\frac{f(t, D)\\,(k_1 + 1)}\n"
        "                   {f(t, D) + k_1\\!\\left(1 - b + b\\,\\frac{|D|}{\\text{avgdl}}\\right)}}_{\\text{saturating, length-normalised TF}}.\n"
    ),
    (
        "Read from left to right, three design decisions fall out of "
        "the formula:"
    ): "从左到右读一遍，三个设计决策就从公式里浮现出来：",
    (
        "**Rare terms dominate.** The IDF factor makes a document "
        "that contains a term occurring in 1% of the corpus count far "
        "more than one containing a term that appears in half of it. "
        "This is why a well-built BM25 index nails identifier-literal "
        "queries: an error code like `ERR_QUEUE_DRAIN` appears in a "
        "handful of documents, so its IDF is enormous and the "
        "document that mentions it wins by a wide margin. It is also "
        "why BM25 tends to out-rank vector retrieval on \"search for "
        "this exact symbol\" workloads: *vectors do not know what "
        "\"rare\" means*."
    ): (
        "**稀有词主导分数。** IDF 因子让包含一个“只在语料 1% 里出现”的词的文档，"
        "远远压过包含一个“出现在一半语料里”的词的文档。"
        "这正是一个造得好的 BM25 索引在字面标识符查询上极准的原因："
        "像 `ERR_QUEUE_DRAIN` 这样的错误码只出现在屈指可数的几份文档里，"
        "IDF 被顶得极高，提到它的那份文档会以巨大优势胜出。"
        "这也是在“搜这个精确符号”这类负载上，"
        "BM25 往往能把向量检索压在身下的原因 —— "
        "*向量并不知道“稀有”是什么意思* 。"
    ),
    (
        "**Term frequency saturates.** Unlike raw TF-IDF — where "
        "repeating a term ten times multiplies its contribution by "
        "ten — BM25's TF numerator is bounded above by $(k_1 + 1)$. "
        "In the Elasticsearch default of $k_1 = 1.2$, the tenth "
        "occurrence of a term contributes almost nothing more than "
        "the third. This single property is why BM25 does not get "
        "tricked by `keyword keyword keyword keyword` filler and "
        "TF-IDF does. The lesson for a code KB is that *TF saturation "
        "is exactly what you want when an identifier legitimately "
        "appears two hundred times in a generated file*."
    ): (
        "**词频会饱和。** 不像原始的 TF-IDF —— "
        "在 TF-IDF 里把一个词重复十次，贡献就放大十倍 —— "
        "BM25 的 TF 分子被 $(k_1 + 1)$ 这个上界卡住。"
        "在 Elasticsearch 默认的 $k_1 = 1.2$ 下，"
        "一个词的第十次出现几乎比第三次出现多不了多少。"
        "正是这一条性质，让 BM25 不会被 `keyword keyword keyword keyword` "
        "这种塞词操作骗到，而 TF-IDF 会。"
        "对代码知识库而言，这里的启示是："
        "*当某个标识符在一个自动生成的文件里合法地出现了两百次时，"
        "TF 饱和恰恰就是你想要的行为* 。"
    ),
    (
        "**Length is normalised, but only partway.** The $b$ "
        "parameter (default $0.75$) controls how aggressively BM25 "
        "penalises long documents. At $b=0$ length does not matter; "
        "at $b=1$ a document twice the average length is halved in "
        "effective term frequency. The middle ground is deliberate: "
        "long documents really do have more chances to mention a "
        "term by accident, but they also legitimately cover more "
        "ground. For a software KB whose documents range from "
        "50-word ADR stubs to 5000-word runbooks, this matters more "
        "than the choice of $k_1$."
    ): (
        "**长度会被归一化，但只归一半。** $b$ 参数（默认 $0.75$）"
        "控制 BM25 对长文档的惩罚有多狠。"
        "$b=0$ 时长度不起作用；"
        "$b=1$ 时一篇两倍平均长度的文档，其有效词频会被砍半。"
        "中间这个折中是有意的："
        "长文档确实更容易“顺手”提到某个词，"
        "但它们也确实名正言顺地覆盖了更多内容。"
        "对于一个文档从 50 字的 ADR 存根到 5000 字的 runbook 不等的软件知识库，"
        "$b$ 的取值比 $k_1$ 的取值更要紧。"
    ),
    (
        "In practice, $k_1 \\in [1.2, 2.0]$ and $b \\in [0.5, 0.9]$ "
        "covers almost every production setting. The popular mistake "
        "is to tune these before the tokeniser. Four well-known BM25 "
        "pathologies to keep in mind, because each one will "
        "eventually show up in a real KB:"
    ): (
        "实践里，$k_1 \\in [1.2, 2.0]$ 和 $b \\in [0.5, 0.9]$ "
        "几乎能覆盖所有生产场景。"
        "常见的错误是先调这两个，再调分词器 —— 顺序是反的。"
        "下面四个众所周知的 BM25 病症值得记在本子上，"
        "因为它们每一个迟早都会在真实知识库里冒出来："
    ),
    (
        "**Short-query sensitivity.** On one-word queries, BM25 "
        "degenerates to \"which document has the highest IDF-weighted "
        "TF for that word\", which is fine until the word is a "
        "common English verb. Remedy: query expansion, or a dense "
        "retriever running in parallel, fused at the end."
    ): (
        "**单词查询很敏感。** 遇到一词查询，BM25 就退化成"
        "“哪篇文档对这个词有最大的 IDF 加权 TF”，"
        "这在词是某个常见英语动词前都还好用。"
        "解法：查询扩展，或者并行跑一条稠密检索，最后做融合。"
    ),
    (
        "**Vocabulary mismatch.** *\"wait for the pool to finish\"* "
        "and *\"drainOnShutdown\"* share zero query terms, so BM25 "
        "scores them zero. This is not a bug in BM25; it is the "
        "reason dense retrieval exists as a complement."
    ): (
        "**词汇对不上。** *“wait for the pool to finish”* 和 "
        "*“drainOnShutdown”* 这两个查询在词项上交集是零，"
        "BM25 给出的分也就是零。"
        "这不是 BM25 的 bug，而正是稠密检索作为互补存在的理由。"
    ),
    (
        "**Compound-word breakage.** `drainOnShutdown` indexed as "
        "one token is invisible to the human query *\"drain on "
        "shutdown\"*. Three lines of tokeniser configuration — "
        "camel-case splitting, snake-case splitting, optional "
        "language-model subword fallback — often matter more than "
        "three weeks of embedding-model fine-tuning. Chapter 10 "
        "returns to this in anger."
    ): (
        "**复合词断裂。** 一个把 `drainOnShutdown` 索引成单个 token 的 BM25 系统，"
        "对人类查询 *“drain on shutdown”* 而言是不可见的。"
        "三行分词器配置 —— 驼峰拆分、下划线拆分、"
        "可选的语言模型子词兜底 —— "
        "往往比三周的 embedding 模型微调更顶用。"
        "第 10 章会专门回来收拾这件事。"
    ),
    (
        "**Stopword asymmetry.** Naïve stopword removal strips "
        "*not*, *or*, *no*, *nil* from queries, which in a software "
        "KB is the difference between *\"does it return nil\"* and "
        "*\"does it return\"*. The code-layer retriever in Part III "
        "keeps these words."
    ): (
        "**停用词不对称。** 朴素地去停用词，会把查询里的 "
        "*not*、*or*、*no*、*nil* 都扔掉 —— "
        "可在软件知识库里，这恰恰就是 "
        "*“它会不会返回 nil”* 与 *“它会不会返回”* 的区别。"
        "第三部分的代码层检索器保留这些词。"
    ),
    (
        "There is a second class of query where BM25 is not a fallback "
        "but the primary winner: *identifier-literal* queries. A user "
        "searching for order number `20260115` or HTTP status `502` or "
        "ticket `PROJECT-1234` does not want *\"paragraphs that feel "
        "like they might discuss 502 errors\"*; they want *\"the "
        "paragraph that mentions `20260115`\"*. A vector retriever, "
        "confronted with `20260115`, will happily return a general "
        "discussion of order creation because it looks semantically "
        "adjacent; a BM25 retriever will return the paragraph that "
        "actually contains the literal "
        "{cite}`fanyamin2026elasticsearch_rag`. Any KB whose users ask "
        "identifier-literal questions — and for software KBs that is "
        "almost all of them — must keep a BM25 path, full stop."
    ): (
        "还有另一类查询，BM25 不是兜底，而是主力："
        "*字面标识符*（identifier-literal）查询。"
        "用户搜订单号 `20260115`、HTTP 状态码 `502` 或工单 `PROJECT-1234` 时，"
        "要的不是 *“一些感觉上跟 502 有关的段落”*，"
        "要的是 *“那段明确提到了 `20260115` 的话”*。"
        "向量检索遇到 `20260115`，会一本正经地给你返回一段关于“如何创建订单”的介绍 —— "
        "因为它在语义空间里看起来就是挨着的；"
        "而 BM25 会直接返回真正包含这个字面量的那一段 "
        "{cite}`fanyamin2026elasticsearch_rag`。"
        "任何一个用户会问字面标识符问题的知识库 —— "
        "对软件类知识库来说几乎就是全部 —— "
        "就必须保留一条 BM25 通路，没有商量。"
    ),
    # ---------------------------------------------------------------
    # Dense retrieval
    # ---------------------------------------------------------------
    "Dense retrieval: embeddings and ANN": "稠密检索：embedding 与 ANN",
    (
        "Dense retrieval replaces the sparse bag-of-words "
        "representation with a dense vector produced by a neural "
        "encoder, and finds neighbours in that vector space. The modern "
        "ancestor is Dense Passage Retrieval {cite}`karpukhin2020dpr`; "
        "the modern scaling trick is Hierarchical Navigable Small World "
        "graphs for approximate-nearest-neighbour search "
        "{cite}`malkov2020hnsw`, which is what pgvector and most other "
        "production vector stores use under the hood. Dense retrieval "
        "shines on paraphrases — *\"which function waits for the worker "
        "pool to drain?\"* will find `drainOnShutdown` even if the "
        "query uses none of the same words."
    ): (
        "稠密检索把稀疏的词袋表示换成神经编码器生成的稠密向量，"
        "然后在这个向量空间里找邻居。"
        "它的现代祖师爷是 Dense Passage Retrieval（DPR）"
        "{cite}`karpukhin2020dpr`；"
        "让它能工业化的规模化技巧，是为近似最近邻搜索（ANN）设计的 HNSW "
        "（Hierarchical Navigable Small World）图 "
        "{cite}`malkov2020hnsw` —— pgvector 以及大多数生产级向量库底下用的都是它。"
        "稠密检索的强项在于“意译”：*“哪个函数在等 worker pool 排空？”* "
        "这种查询一个词都不用和目标重合，它依然能把 `drainOnShutdown` 找出来。"
    ),
    (
        "The counterweight to remember is that dense retrieval is only "
        "as good as the training distribution of its encoder. A "
        "general-purpose encoder that has seen little Go code will "
        "treat `ctx.Done()` and `context.Background()` as closer than "
        "they should be; a code-trained encoder like Voyage's "
        "`voyage-code` or the BGE family {cite}`voyage_code2` "
        "{cite}`xiao2024bge` will keep them distinct. Pick your encoder "
        "for your domain, not for its leaderboard rank on "
        "MTEB-in-general."
    ): (
        "需要时刻提醒自己的反面是："
        "稠密检索的效果，顶多只能到它编码器训练分布的水平。"
        "一个几乎没见过 Go 代码的通用编码器，"
        "会把 `ctx.Done()` 和 `context.Background()` 放得比应有的更近；"
        "一个真正在代码上训练过的编码器 —— 比如 Voyage 的 `voyage-code` 或 BGE 家族"
        " {cite}`voyage_code2` {cite}`xiao2024bge` —— 才会把它们分开。"
        "选编码器要按你的领域选，别盯着 MTEB 通用榜。"
    ),
    # ---------------------------------------------------------------
    # Hybrid retrieval
    # ---------------------------------------------------------------
    "Hybrid retrieval and Reciprocal Rank Fusion": (
        "混合检索与 Reciprocal Rank Fusion"
    ),
    (
        "Lexical and dense retrieval have complementary failure modes, "
        "which is exactly the setup in which fusion helps. Reciprocal "
        "Rank Fusion {cite}`cormack2009rrf` is the rank-combination "
        "method that most production hybrid systems use, partly because "
        "it is score-free (so neither ranker has to be calibrated) and "
        "partly because it has remarkably few knobs. For a code KB in "
        "particular, Part III (Chapters 10 – 12) argues that *hybrid is "
        "not optional* — lexical alone misses paraphrases, dense alone "
        "misses exact-symbol lookups, and fusion is cheaper than "
        "picking a side."
    ): (
        "词法检索和稠密检索的失败模式是互补的 —— "
        "这正是融合（fusion）能帮上忙的典型场景。"
        "生产环境里大多数混合系统用的都是 Reciprocal Rank Fusion（RRF）"
        "{cite}`cormack2009rrf`，"
        "一方面因为它是“无分数（score-free）”的，"
        "两边的排序器都不必做分数校准，"
        "另一方面因为它几乎没什么可调的旋钮。"
        "对代码知识库而言，第三部分（第 10 – 12 章）会反复论证："
        "*混合不是可选项* —— "
        "纯词法漏意译，纯稠密漏精确符号，"
        "而融合比你二选一要便宜得多。"
    ),
    (
        "Two levers that properly belong to the hybrid layer — and that "
        "a pure-vector-store pipeline usually loses — are worth naming "
        "explicitly, because they change the character of retrieval "
        "more than any embedding upgrade:"
    ): (
        "有两根本应属于混合层的操纵杆 —— 也是纯向量库流水线通常会丢掉的 —— "
        "值得在这里点名，因为它们对检索性格的改变，比你换任何 embedding 模型都大："
    ),
    (
        "**Field weighting.** Tokens appearing in a document's *title* "
        "are a stronger signal of what the document is *about* than the "
        "same tokens buried in the body. A production Elasticsearch / "
        "Solr / pgvector + `tsvector` setup routinely weights the title "
        "field around two times the content field; the effect on "
        "nDCG@10 is larger than most of the choices upstream of it "
        "{cite}`fanyamin2026elasticsearch_rag`."
    ): (
        "**字段加权（Field weighting）。** "
        "出现在文档*标题*里的词，"
        "对“这篇文档在讲什么”的信号强度，比埋在正文里的同样的词要大得多。"
        "生产环境里 Elasticsearch / Solr / pgvector + `tsvector` 的常规做法，"
        "就是给标题字段大约两倍于正文字段的权重；"
        "这一下对 nDCG@10 的提升，"
        "往往比它上游的多数选择都更明显 "
        "{cite}`fanyamin2026elasticsearch_rag`。"
    ),
    (
        "**Function scoring (freshness, authority, popularity).** A "
        "document that scores highly on lexical + dense similarity but "
        "was last updated three years ago is, for most KB questions, a "
        "worse answer than a 90%-as-similar document updated last week. "
        "Multiplying the fused score by a freshness decay function "
        "turns this intuition into a scored ranking term, not an "
        "afterthought "
        "{cite}`fanyamin2026elasticsearch_rag`."
    ): (
        "**函数评分（Function scoring，覆盖新鲜度、权威性、热度）。** "
        "一篇在词法 + 稠密相似度上都打高分、但三年没更新过的文档，"
        "对绝大多数知识库问题来说，"
        "都不如一篇相似度只有它 90%、但上周刚更新的新文档。"
        "用一个新鲜度衰减函数去乘融合后的分数，"
        "就把这个直觉变成了排序里的一项正式得分，"
        "而不是事后再补的补丁 "
        "{cite}`fanyamin2026elasticsearch_rag`。"
    ),
    (
        "Structured filtering — *\"only pages in the `worker` package\""
        ", \"only docs tagged `runbook`\", \"only the current major "
        "version\"* — is the third lever and is discussed on its own in "
        "Chapter 10. The practical point for now: as soon as structured "
        "filters enter the picture, the choice of retrieval substrate "
        "(pgvector? Elasticsearch? a specialised vector database?) "
        "stops being a matter of taste. The \"How\" section of this "
        "chapter gives a judgment matrix "
        "{cite}`fanyamin2026pgvector_rag`."
    ): (
        "结构化过滤 —— *“只要 `worker` 包下的页面”、"
        "“只要打了 `runbook` 标签的文档”、“只要当前大版本”* —— "
        "是第三根操纵杆，放到第 10 章单独讨论。"
        "在这里只强调一个现实问题："
        "一旦结构化过滤进入视野，"
        "检索底座的选择（pgvector？Elasticsearch？专用向量数据库？）"
        "就不再是口味问题。"
        "本章“怎么做”一节会给出一张判断矩阵 "
        "{cite}`fanyamin2026pgvector_rag`。"
    ),
    # ---------------------------------------------------------------
    # Re-ranking
    # ---------------------------------------------------------------
    "Re-ranking: the second-stage retriever": "重排：第二阶段的检索器",
    (
        "Fusion gives you a better *list*. Re-ranking gives you a "
        "better *top-k*. The distinction is worth making carefully, "
        "because \"add a reranker\" is advice so frequently given "
        "and so rarely explained that many teams implement it as "
        "\"call Cohere Rerank\" and never find out what the model is "
        "actually doing for them."
    ): (
        "融合给你一条更好的 *列表* ；"
        "重排（Re-ranking）给你一个更好的 *top-k* 。"
        "这个区别值得仔细厘清："
        "“加一个 reranker”这条建议被说得太多、被解释得太少，"
        "以至于很多团队把它实现成“调一下 Cohere Rerank”，"
        "然后就再也没搞清楚那个模型到底替他们干了什么。"
    ),
    (
        "The setup is a two-stage pipeline. Stage one is your fused "
        "BM25 + dense retriever, which is fast, operates over the "
        "whole index, and is asked to return a *generous* top-k — "
        "typically 50 or 100 candidates. Stage two is the reranker, "
        "which is slow, operates only over those candidates, and is "
        "asked to reorder them into the final top-k (typically 5 to "
        "10) that the LLM will actually see. The first stage "
        "optimises *recall* (\"did the right document make the "
        "top-100?\"); the second optimises *precision at small k* "
        "(\"is the right document at position 1?\"). Neither stage "
        "can do the other's job well, which is why the two-stage "
        "shape is the dominant production pattern "
        "{cite}`nogueira2019passage`."
    ): (
        "架子是两段式的。第一阶段是融合过的 BM25 + 稠密检索，"
        "速度快、覆盖整个索引，被要求返回一个 *慷慨的* top-k —— "
        "典型值是 50 或 100 个候选。"
        "第二阶段就是那个 reranker，速度慢、只对这些候选动手，"
        "被要求把它们重新排成最终送进 LLM 的 top-k（通常是 5 到 10）。"
        "第一阶段优化的是 *召回率* （“对的文档上没上 top-100？”），"
        "第二阶段优化的是 *小 k 下的精度* （“对的文档是不是就在第 1 位？”）。"
        "哪一阶段都做不好另一阶段的事，"
        "这也正是两段式成为主流生产范式的原因 "
        "{cite}`nogueira2019passage`。"
    ),
    (
        "The technical reason stage two needs to be separate comes "
        "down to a single architectural choice: **bi-encoder** vs "
        "**cross-encoder** {cite}`reimers2019sbert`."
    ): (
        "第二阶段之所以必须单独存在，技术原因可以归结到一个架构抉择："
        "**双编码器**（bi-encoder）与 **交叉编码器**（cross-encoder）之争 "
        "{cite}`reimers2019sbert`。"
    ),
    (
        "A **bi-encoder** — which is what every dense retriever in "
        "this chapter has been so far — encodes the query and the "
        "document *independently* into two vectors, then scores them "
        "by a cheap similarity function (cosine, dot product). The "
        "encoding cost of the document is paid once at index time; "
        "at query time you only encode the query, then do an ANN "
        "search against millions of precomputed vectors. Billions of "
        "documents are feasible. The cost is representational: the "
        "model can only compare the two fixed vectors, never the "
        "*interaction* of specific tokens across the query and the "
        "document."
    ): (
        "**双编码器** —— 本章前面提到的所有稠密检索器都是这种 —— "
        "把查询和文档 *各自独立* 编码成两个向量，"
        "再用一个便宜的相似度函数（余弦、点积）打分。"
        "文档的编码代价在索引时一次性付掉；"
        "查询时你只编码一次查询，"
        "然后在百万量级的预计算向量上做一次 ANN 搜索。"
        "上到十亿文档都没问题。"
        "代价在表达力：模型只能比较这两个定长向量本身，"
        "永远看不到查询词项与文档词项之间的 *交互* 。"
    ),
    (
        "A **cross-encoder** concatenates the query and the document "
        "into one input — something like `[CLS] query [SEP] document "
        "[SEP]` — and runs the whole concatenation through a "
        "transformer that outputs a single relevance score. Because "
        "attention runs across both sides, the model can directly "
        "weigh *which query token aligns with which document token*, "
        "which is exactly the signal needed to separate \"talks about "
        "rate limiting in general\" from \"talks about rate limiting "
        "on the ingest endpoint\". The cost is computational: every "
        "(query, document) pair is a separate transformer forward "
        "pass, so you cannot afford to run a cross-encoder over the "
        "whole index. You *can* afford to run it over 100 candidates."
    ): (
        "**交叉编码器** 把查询与文档拼成一个输入 —— "
        "形如 `[CLS] query [SEP] document [SEP]` —— "
        "再把整条输入送进一个 transformer，输出一个相关性分数。"
        "因为注意力机制横跨查询和文档两侧，"
        "模型可以直接权衡 *哪个查询 token 与哪个文档 token 对齐* ，"
        "这恰好就是区分"
        "“笼统地讲限流”与“讲 ingest 接口上的限流”所需要的那点信号。"
        "代价在算力：每一对 (查询, 文档) 都是一次独立的 transformer 前向，"
        "所以在整个索引上跑交叉编码器是负担不起的。"
        "但在 100 个候选上跑，*是* 负担得起的。"
    ),
    (
        "This is the whole reason re-ranking is a separate stage. "
        "The bi-encoder gives you recall on the corpus scale; the "
        "cross-encoder gives you precision on the shortlist. Trying "
        "to do either job with the other model costs either quality "
        "or money."
    ): (
        "这就是重排必须单独成一阶段的全部理由。"
        "双编码器在语料规模上给你召回，"
        "交叉编码器在候选名单上给你精度。"
        "想让其中一个去干另一个的活，不是赔质量，就是赔钱。"
    ),
    (
        "For a rough order-of-magnitude feel: a modern cross-encoder "
        "reranker on CPU might score 50 – 200 (query, document) "
        "pairs per second, and on a single commodity GPU 500 – 2000 "
        "pairs per second. With a stage-1 top-100 and a per-query "
        "budget under 100ms, that comfortably fits. With a stage-1 "
        "top-1000 and the same budget, it does not. The practical "
        "consequence is that *the stage-1 top-k is a cost dial*, "
        "not an accuracy dial — past some point, more recall costs "
        "more latency without helping the end-to-end answer."
    ): (
        "给点数量级的感觉："
        "一个现代的交叉编码器 reranker 在 CPU 上"
        "大约能每秒打分 50 – 200 对 (查询, 文档)，"
        "单张消费级 GPU 能到每秒 500 – 2000 对。"
        "第一阶段给 top-100、每个查询预算 100ms 以内，这个数量级是舒舒服服能吃下的；"
        "第一阶段给 top-1000、预算还是那个，就吃不下了。"
        "实用结论是： *第一阶段的 top-k 是一个成本旋钮* ，"
        "不是一个精度旋钮 —— "
        "越过某个点之后，再加召回只是在买延迟，而对最终答案没有帮助。"
    ),
    (
        "Three open-weight reranker families are worth knowing "
        "about, because they cover most of the design space without "
        "lock-in:"
    ): (
        "三类开权重 reranker 值得认识一下，"
        "因为它们几乎覆盖了整个设计空间，且都不会把你锁死在某家厂商上："
    ),
    (
        "**MS MARCO cross-encoders** — the sentence-transformers "
        "family, trained on Microsoft's 8.8M-passage MS MARCO "
        "dataset {cite}`nogueira2019passage`. Robust, "
        "well-understood, widely benchmarked. A good default for "
        "English KBs."
    ): (
        "**MS MARCO 交叉编码器** —— sentence-transformers 这一家，"
        "在 Microsoft 的 880 万段落的 MS MARCO 数据集上训练 "
        "{cite}`nogueira2019passage`。"
        "稳、理解得透、被 benchmark 得够多。"
        "英文知识库的一个合格默认项。"
    ),
    (
        "**BGE rerankers** — part of the BGE family already cited "
        "for embeddings {cite}`xiao2024bge`; multilingual, and the "
        "small variants (≈300M parameters) fit on a single GPU. A "
        "good choice when the KB is mixed-language or when you want "
        "one vendor across embeddings and reranking."
    ): (
        "**BGE rerankers** —— 就是前面在 embedding 一节引用过的 BGE 家族"
        "的一部分 {cite}`xiao2024bge`；多语言，"
        "小号变体（≈3 亿参数）单张 GPU 就能装下。"
        "知识库里是混合语言、或者你希望 embedding 和 rerank 都走同一家时，"
        "是一个很合适的选择。"
    ),
    (
        "**Hosted APIs** (Cohere Rerank, Voyage Rerank, Jina "
        "Rerank). The quality-per-dollar is usually fine, the "
        "integration cost is trivial, and the operational concern is "
        "straightforward: *every query now talks to an external "
        "service*. For a KB that deliberately avoids sending "
        "proprietary code off-prem, this is disqualifying; for a "
        "public-docs KB it is often the right first-cut choice."
    ): (
        "**托管 API** （Cohere Rerank、Voyage Rerank、Jina Rerank）。"
        "单位美元的质量通常不差，集成代价几乎为零，"
        "运维上的顾虑也简单直接： *每一次查询现在都要去调一个外部服务* 。"
        "对于一个明确要求“专有代码不出机房”的知识库，这是一票否决；"
        "但对于一个公开文档的知识库，这常常是最合适的第一版选择。"
    ),
    "Four honest caveats before adopting one:": "采用之前，四条诚实的提醒：",
    (
        "**A reranker makes a mediocre retriever look good, not a "
        "broken one look good.** If stage one has poor recall — the "
        "right document is not in its top-100 — the cross-encoder "
        "cannot retrieve something that was never shown to it. "
        "Teams that report \"we added reranking and quality "
        "*dropped*\" have almost always tuned stage one to return "
        "fewer, more confident candidates after the rerank, "
        "starving stage two."
    ): (
        "**reranker 能把一个平庸的检索器变好看，但救不了一个坏掉的。** "
        "如果第一阶段召回差 —— 正确文档根本没进它的 top-100 —— "
        "交叉编码器也没法召回一个从没被递到它面前的东西。"
        "那些报告“我们加了 rerank，质量 *反而掉了*”的团队，"
        "几乎永远是把第一阶段调成了“返回更少、更自信的候选”，"
        "把第二阶段饿死了。"
    ),
    (
        "**Latency is additive, not hidden.** A 50ms cross-encoder "
        "pass on top of a 30ms hybrid retrieval is 80ms to first "
        "LLM token, not 30ms. For agent loops with many retrievals "
        "per turn this accumulates fast. Chapter 21 on agents "
        "returns to this budget."
    ): (
        "**延迟是叠加的，不是隐藏的。** "
        "一次 50ms 的交叉编码器调用叠在一次 30ms 的混合检索之上，"
        "到 LLM 吐出第一个 token 的时间是 80ms，不是 30ms。"
        "对那些一个回合里要多次检索的 agent 循环，这个账会涨得很快。"
        "第 21 章讨论 agent 时会回到这个预算问题。"
    ),
    (
        "**Evaluation matters more, not less, with a reranker in "
        "the loop.** A reranker can reorder a list in ways that "
        "look right on three sample queries and are wrong on the "
        "long tail. The BEIR-style evaluation in Chapter 15 stays "
        "in place; it moves downstream of the reranker, not around "
        "it."
    ): (
        "**加了 reranker 之后，评估只会更重要，而不是更次要。** "
        "一个 reranker 重排列表的方式，可能在三条样例查询上看起来合理，"
        "在长尾上却是错的。"
        "第 15 章里那套 BEIR 风格的评估不会因此撤掉；"
        "它只是整个前移，挪到了 reranker 的下游，而不是绕开它。"
    ),
    (
        "**Rerankers do not replace the other levers.** Field "
        "weighting and freshness decay, applied at the fusion "
        "stage, still matter; the cross-encoder has no idea that "
        "the document it scored highly was last updated three years "
        "ago. The healthy mental model is: *fusion assembles a "
        "candidate list with the right structural biases; the "
        "reranker reorders within those biases*."
    ): (
        "**reranker 不能替代前面那几根操纵杆。** "
        "在融合阶段做的字段加权与新鲜度衰减还是要做；"
        "交叉编码器并不知道它打了高分的那份文档上次更新是三年前。"
        "健康的心智模型是： *融合负责组出一个带有合适结构性偏置的候选名单，"
        "reranker 只在这些偏置之内重新排序* 。"
    ),
    (
        "For the workloads this book targets, the honest "
        "recommendation is: do not add a reranker until hybrid "
        "retrieval with field weighting and freshness decay is "
        "measured and clearly leaving precision on the table. When "
        "you do add one, measure on the same BEIR-style harness the "
        "first stage uses, cap the stage-1 top-k at something you "
        "can actually afford, and keep the reranker interchangeable "
        "behind an interface so you can swap MS MARCO for BGE for a "
        "hosted API without rewriting the retrieval layer. The "
        "code-layer reference implementation in Chapter 12 wires in "
        "a cross-encoder exactly this way."
    ): (
        "对本书面向的那些负载，诚实的建议是："
        "在混合检索 + 字段加权 + 新鲜度衰减已经量化过，"
        "并且明显还把精度留在桌上之前，不要急着加 reranker。"
        "真要加的时候，用第一阶段同一套 BEIR 风格的评估脚手架去量，"
        "把第一阶段的 top-k 封在你真的负担得起的范围内，"
        "并把 reranker 藏在一个接口后面保持可替换 —— "
        "以便你把 MS MARCO 换成 BGE、再换成某个托管 API 时，"
        "不需要重写整个检索层。"
        "第 12 章里代码层的参考实现正是这样接入交叉编码器的。"
    ),
    # ---------------------------------------------------------------
    # RAG
    # ---------------------------------------------------------------
    "Retrieval-Augmented Generation": "检索增强生成（RAG）",
    (
        "Retrieval-Augmented Generation, as formalised by Lewis et al. "
        "{cite}`lewis2020rag`, is the pattern of composing a retriever "
        "and a generator in series so that the retrieved context "
        "conditions the generator's output. The modern RAG survey by "
        "Gao and colleagues {cite}`gao2023retrieval` catalogues the "
        "variants — Naive RAG, Advanced RAG with query rewriting and "
        "re-ranking, Modular RAG — and is a good map of the design "
        "space. This book is, under a thin coat of paint, an "
        "applied-RAG book; the prose layer (Part II) and the code layer "
        "(Part III) are two specialisations of the same pattern."
    ): (
        "Retrieval-Augmented Generation（RAG）由 Lewis 等人正式定型 "
        "{cite}`lewis2020rag`，"
        "核心就是把检索器与生成器串成一条流水线，"
        "让检索到的上下文去约束生成器的输出。"
        "Gao 等人较新的一篇 RAG 综述 {cite}`gao2023retrieval` "
        "把这个家族的变体都梳理了一遍 —— "
        "Naive RAG、带查询改写和重排的 Advanced RAG、Modular RAG —— "
        "是一张很好的设计空间地图。"
        "撕掉表面那层漆，本书其实是一本“应用型 RAG”书："
        "文本层（第二部分）和代码层（第三部分）是同一个模式的两种特化。"
    ),
    # ---------------------------------------------------------------
    # Evaluation
    # ---------------------------------------------------------------
    "Evaluation: BEIR and friends": "评估：BEIR 和它的朋友们",
    (
        "Retrieval without evaluation is superstition. BEIR "
        "{cite}`thakur2021beir` is the benchmark suite that made "
        "zero-shot retrieval evaluation concretely testable across "
        "domains, and the methodology it uses — labelled queries, "
        "nDCG@10, Recall@k — transfers directly to a home-grown code "
        "KB. Chapter 15 builds a mini-BEIR for a code-layer instance; "
        "readers who want to compare a BM25 baseline against a "
        "pgvector-backed system without that scaffolding risk mistaking "
        "\"the answer looks nice\" for \"the answer is right\"."
    ): (
        "没有评估的检索就是迷信。"
        "BEIR {cite}`thakur2021beir` 是那套"
        "让零样本检索评估能在多领域具体做起来的基准集，"
        "它用的那套方法 —— 标注查询、nDCG@10、Recall@k —— "
        "可以一对一搬到一个自建的代码知识库上。"
        "第 15 章会给一个代码层实例搭一个 mini-BEIR；"
        "要是不搭这套脚手架，"
        "就去比较 BM25 基线和 pgvector 后端的系统，"
        "最容易犯的错就是把“回答看起来不错”当成“回答是对的”。"
    ),
    # ---------------------------------------------------------------
    # Limits of vanilla RAG
    # ---------------------------------------------------------------
    "The limits of vanilla RAG": "Vanilla RAG 的边界",
    (
        "\"Vanilla RAG\" — in this book's usage — means: split "
        "documents into roughly-paragraph-sized chunks, embed each "
        "chunk, retrieve top-k by vector similarity, concatenate into a "
        "prompt, call the LLM. This baseline works well enough for the "
        "demo that it has absorbed the entire popular imagination of "
        "what RAG *is*. It also has a well-known catalogue of failure "
        "modes that show up as soon as real users ask real questions. "
        "Five are worth naming here:"
    ): (
        "本书口径下的“Vanilla RAG”，意思是："
        "把文档切成大约段落大小的 chunk、"
        "给每个 chunk 算 embedding、"
        "按向量相似度取 top-k、"
        "拼成 prompt、调 LLM。"
        "这个基线在 demo 阶段的效果好到足以独占大众对“RAG 是什么”的全部想象，"
        "也有一份已经很出名的失败模式清单 —— "
        "只要真实用户开始问真实问题，它们立刻就会浮出水面。"
        "下面五条值得点名："
    ),
    (
        "**The chunk-boundary problem.** A 200-word chunk cuts a "
        "paragraph in half; the sentence that explains *why* an API "
        "returns `nil` lives in chunk `k`, the sentence that shows "
        "*what* it returns lives in chunk `k+1`, and a retriever "
        "scoring by individual-chunk similarity returns one without the "
        "other. Symptom: the answer is plausible but missing the "
        "qualifier. Mitigations include overlapping chunks, "
        "parent-document retrieval, and late-chunking schemes; none of "
        "them fully solve it, and any code-aware KB has to chunk on "
        "*syntactic* rather than character boundaries (Chapter 10)."
    ): (
        "**chunk 边界问题。** "
        "一个 200 词的 chunk 会把一段话从中间劈开："
        "解释一个 API *为什么* 返回 `nil` 的那句话落在 `k` 号 chunk 里，"
        "说明它*返回什么*的那句话落在 `k+1` 号 chunk 里，"
        "而一个按单 chunk 相似度打分的检索器，"
        "只会把它们中的一句送回来。"
        "症状：答案听着合理，但正好缺了那个关键限定。"
        "缓解手段包括带重叠的 chunk、parent-document 检索、late-chunking 等，"
        "没有一个能彻底解决；"
        "任何“懂代码”的知识库都必须按*语法边界*切块，"
        "而不是按字符数切块（第 10 章）。"
    ),
    (
        "**Semantic match ≠ semantic relevance.** Vector similarity "
        "finds *things that look like* the query, which is not the same "
        "as *things that answer* the query. A query \"how do I "
        "rate-limit the ingest endpoint?\" retrieves, via vector "
        "similarity, the five paragraphs in the repo that talk most "
        "about rate limiting — none of which is the paragraph about "
        "*the ingest endpoint specifically*. The fix is almost always "
        "hybrid retrieval plus a cross-encoder re-ranker (see the "
        "*Re-ranking* subsection above); re-ranking is the honest "
        "step many \"just add vectors\" stacks skip."
    ): (
        "**语义相似 ≠ 语义相关。** "
        "向量相似度找的是 *“看起来像查询”* 的东西，"
        "不是 *“能回答查询”* 的东西。"
        "查询“怎么给 ingest 接口做限流？”在向量意义上，"
        "会把仓库里最“关于限流”的五段话召回来 —— "
        "但其中没有一段是 *专门讲 ingest 接口* 的那段。"
        "解法几乎永远是混合检索再加一个交叉编码器式的重排器"
        "（cross-encoder re-ranker，参见上面的 *重排* 一节）；"
        "而重排恰恰是很多“上向量就完事了”的技术栈会跳过的那一步。"
    ),
    (
        "**The multi-hop / global-question problem.** Vanilla RAG "
        "retrieves a flat set of top-k chunks. Questions of the form "
        "*\"what are the three main themes of this codebase?\"* or "
        "*\"summarise how the ingest pipeline has evolved across the "
        "last ten commits\"* require reasoning over structure the top-k "
        "chunks do not carry. The honest answer for this class of "
        "question is: *vanilla RAG cannot answer it*. This is the gap "
        "GraphRAG (next section) is designed for "
        "{cite}`edge2024graphrag`."
    ): (
        "**多跳 / 全局问题。** "
        "Vanilla RAG 召回的是一组扁平的 top-k chunk。"
        "像 *“这个代码库的三条主线是什么？”* 或 "
        "*“总结一下 ingest 流水线在最近十次 commit 里是怎么演化的”* "
        "这种问题，需要对 top-k chunk 本身没有承载的结构做推理。"
        "对这一类问题最诚实的回答是：*vanilla RAG 回答不了*。"
        "这正是下一节的 GraphRAG 所针对的缺口 "
        "{cite}`edge2024graphrag`。"
    ),
    (
        "**The stale-index problem.** An embedding index built at "
        "commit `a1b2c3d` is, by definition, a snapshot. Between that "
        "snapshot and the user's query the repo has moved; functions "
        "were renamed, pages were rewritten. Unless the pipeline "
        "re-embeds on every change (expensive) or detects and re-embeds "
        "only affected files (operationally complex), the retrieved "
        "chunk is a pre-image of a file that no longer exists. Chapter "
        "14 is entirely about bounding this gap."
    ): (
        "**索引过期问题。** "
        "一个在 commit `a1b2c3d` 上构建的 embedding 索引，"
        "按定义就是一份快照。"
        "从那份快照到用户发出查询之间，仓库已经动过了："
        "函数被改名了、页面被重写了。"
        "除非流水线每次变更都重算 embedding（昂贵）、"
        "或者能精准检测并只重算受影响的文件（运维复杂），"
        "否则你召回的 chunk 就是一份文件早已不存在的原像。"
        "第 14 章整章都在讨论怎么把这个时间差压到最小。"
    ),
    (
        "**The faithfulness problem.** Even with perfect retrieval, the "
        "generator can still fabricate. Code-LLMs in particular are "
        "documented to generate plausible-looking `file:line` "
        "references that do not correspond to any actual file or line "
        "{cite}`chen2023faithfulness`. The only durable mitigation is "
        "*mechanical citation verification*: every `file:line` the LLM "
        "emits has to resolve at the build's HEAD commit, or the answer "
        "is rejected by the gate (Chapter 15)."
    ): (
        "**忠实性（faithfulness）问题。** "
        "即使检索是完美的，生成器仍然会编。"
        "尤其是代码 LLM，"
        "生成形如 `file:line` 的引用、看着很像真的、但实际上并不存在 —— "
        "这一点已经被文献记录在案 {cite}`chen2023faithfulness`。"
        "唯一长期有效的缓解手段是*机械化的引用校验*："
        "LLM 给出的每一个 `file:line`，"
        "都要能在构建对应的 HEAD commit 上解析得到，"
        "否则答案就被闸门直接拒掉（第 15 章）。"
    ),
    (
        "None of these is a reason to give up on RAG — they are reasons "
        "to stop calling \"vanilla RAG\" *the RAG*. The literature "
        "calls the mitigation layer \"Advanced RAG\" "
        "{cite}`gao2023retrieval`; this book calls it *the work*."
    ): (
        "这五条都不是放弃 RAG 的理由 —— "
        "而是让你别再把“vanilla RAG”当成 *“那个 RAG”* 的理由。"
        "文献把这个缓解层叫“Advanced RAG” {cite}`gao2023retrieval`；"
        "本书直接叫它 *“真正要干的那些活”*。"
    ),
    # ---------------------------------------------------------------
    # GraphRAG
    # ---------------------------------------------------------------
    "GraphRAG and its neighbours": "GraphRAG 以及它的邻居们",
    (
        "GraphRAG, introduced by Edge et al. at Microsoft Research "
        "{cite}`edge2024graphrag`, is a specific answer to the third "
        "limit above: the global-question, multi-hop problem. The "
        "intuition is straightforward even if the engineering is not. "
        "Instead of retrieving flat chunks and hoping the LLM stitches "
        "them back together, GraphRAG *pre-computes* the stitching at "
        "index time by building a graph over entities and relations "
        "extracted from the corpus, and then answers global questions "
        "by summarising the graph, not the chunks."
    ): (
        "GraphRAG 由 Microsoft Research 的 Edge 等人提出 "
        "{cite}`edge2024graphrag`，"
        "它针对的正是上面第三条 —— 全局问题 / 多跳问题。"
        "直觉不复杂，工程实现则不简单。"
        "它不再是召回一组扁平的 chunk 再指望 LLM 自己把它们重新“缝”起来，"
        "而是在建索引时就*预先算好*这种“缝合”："
        "从语料里抽取实体和关系、建成一张图，"
        "然后在回答全局问题时，总结的是这张图，不是那些 chunk。"
    ),
    "Concretely, GraphRAG as described in the paper runs in four stages:": (
        "具体来说，论文里的 GraphRAG 分四个阶段："
    ),
    "Stage": "阶段",
    "Input": "输入",
    "Output": "输出",
    "Who pays": "谁在出钱",
    "**1. Entity extraction**": "**1. 实体抽取**",
    "Raw chunks": "原始 chunk",
    "Typed entities + relations (via LLM extraction prompt)": (
        "带类型的实体 + 关系（由 LLM 抽取 prompt 完成）"
    ),
    "Index-time LLM calls, O(chunks)": "建索引期的 LLM 调用，O(chunks)",
    "**2. Graph construction**": "**2. 图构建**",
    "Entities and relations": "实体与关系",
    "A knowledge graph (nodes = entities, edges = relations with provenance)": (
        "一张知识图谱（节点 = 实体，边 = 带来源信息的关系）"
    ),
    "Cheap": "便宜",
    "**3. Community detection**": "**3. 社区检测**",
    "The graph": "整张图",
    "Hierarchical clusters (\"communities\") via algorithms such as Leiden": (
        "通过 Leiden 等算法产生的层次化聚类（“社区”）"
    ),
    "**4. Community summarisation**": "**4. 社区摘要**",
    "Each community": "每一个社区",
    "An LLM-generated summary at each level of the hierarchy": (
        "层次结构每一层上，由 LLM 生成的摘要"
    ),
    "Index-time LLM calls, O(communities)": "建索引期的 LLM 调用，O(communities)",
    (
        "At query time, GraphRAG has two modes: **local** search (start "
        "from the entities the query mentions, walk the graph, retrieve "
        "their summaries) and **global** search (run the query against "
        "*every* top-level community summary, map-reduce the answers). "
        "The global mode is the thing vanilla RAG literally cannot do: "
        "every community summary was produced with full visibility of "
        "its community's chunks, so the map step has a fighting chance "
        "of returning a globally correct answer to a globally framed "
        "question."
    ): (
        "查询阶段 GraphRAG 有两种模式："
        "**local（局部）** 搜索 —— 从查询里提到的实体出发，"
        "在图上行走，把它们的摘要召回来；"
        "**global（全局）** 搜索 —— 把查询同时打到*每一份*顶层社区摘要上，"
        "用 map-reduce 的方式合并答案。"
        "全局模式恰好是 vanilla RAG 字面意义上做不到的事："
        "每一份社区摘要，都是在能完整看到该社区所有 chunk 的前提下生成的，"
        "因此 map 这一步才有机会，"
        "对一个全局提问给出一个全局正确的回答。"
    ),
    "Two practical consequences follow:": "由此直接推出两条实操结论：",
    (
        "**GraphRAG is not cheaper than vanilla RAG. It is a different "
        "cost curve.** Indexing costs rise sharply — typically one to "
        "two orders of magnitude more LLM calls at index time — in "
        "exchange for query-time answers to questions vanilla RAG "
        "cannot answer at all. If your queries are all \"what does "
        "`drainOnShutdown` do?\", GraphRAG is wasted effort. If a "
        "non-trivial fraction of queries are \"what are the three main "
        "subsystems of this codebase, and how do they talk to each "
        "other?\", GraphRAG earns its indexing cost back on the first "
        "dozen queries."
    ): (
        "**GraphRAG 并不比 vanilla RAG 便宜，它只是换了一条成本曲线。** "
        "建索引成本会陡增 —— 典型情况下，"
        "建索引期的 LLM 调用会多出一到两个数量级 —— "
        "换来的是能回答一类 vanilla RAG 根本答不了的查询。"
        "如果你全部的查询都是“`drainOnShutdown` 是干嘛的？”，"
        "GraphRAG 就是在浪费钱；"
        "如果其中有相当一部分是"
        "“这个代码库的三大子系统是什么、它们之间怎么交互？”，"
        "GraphRAG 会在前十几条查询里就把建索引的钱挣回来。"
    ),
    (
        "**The extracted graph is the product, not a byproduct.** The "
        "graph is human-inspectable, correctable, and re-usable for "
        "non-RAG purposes (visualisation, impact analysis, onboarding). "
        "Teams that adopt GraphRAG often end up valuing the graph more "
        "than the summarisation."
    ): (
        "**抽出来的那张图是产品本身，不是副产品。** "
        "这张图人是可以看、可以改、可以用到 RAG 以外的地方的 —— "
        "可视化、影响分析、新人上手都行。"
        "采用 GraphRAG 的团队，"
        "最后往往更看重那张图，而不是它上面的摘要。"
    ),
    (
        "A neighbour worth knowing about is **HippoRAG** "
        "{cite}`gutierrez2024hipporag`, which keeps the "
        "knowledge-graph structure of GraphRAG but replaces Leiden + "
        "LLM-summarisation with a personalised-PageRank-based retrieval "
        "step inspired by the hippocampus's memory-indexing model. "
        "HippoRAG reports competitive multi-hop answer quality at "
        "substantially lower index-time cost. Whether it generalises to "
        "code KBs specifically is, as of 2025, an open question — but "
        "the direction (graph structure + cheap graph-algorithmic "
        "retrieval, instead of expensive LLM pre-summarisation) is "
        "worth tracking."
    ): (
        "一个值得关注的邻居是 **HippoRAG** {cite}`gutierrez2024hipporag`，"
        "它保留了 GraphRAG 的知识图谱结构，"
        "但把 Leiden + LLM 摘要这一步，"
        "换成了受海马体“记忆索引”模型启发的、基于个性化 PageRank 的检索。"
        "HippoRAG 报告称，在多跳问答上质量可对标 GraphRAG，"
        "而建索引成本显著更低。"
        "它在代码知识库这个特定场景上能否泛化，"
        "截至 2025 年仍是一个开放问题 —— "
        "但这个方向（图结构 + 便宜的图算法检索，"
        "而不是昂贵的 LLM 预摘要）值得一直盯着。"
    ),
    (
        "This book does not ask you to pick a side in the "
        "GraphRAG-vs-vanilla debate. Part V (Chapter 19) uses a small "
        "knowledge graph for a narrow purpose — guided context "
        "assembly for code — which is closer in spirit to "
        "GraphRAG-local than GraphRAG-global. The design choice is "
        "always: *what class of question is hard for me, and what is "
        "the cheapest structure that makes that class answerable?*"
    ): (
        "本书不要求你在 GraphRAG 和 vanilla RAG 之间站队。"
        "第五部分（第 19 章）会用一张小型知识图谱做一件窄的事 —— "
        "为代码做“引导式上下文装配”（guided context assembly） —— "
        "在精神上更接近 GraphRAG-local，而不是 GraphRAG-global。"
        "设计问题永远只有一个："
        "*哪一类问题对我而言最难，"
        "以及能让这一类问题变得可回答的、最便宜的结构是什么？*"
    ),
    # ---------------------------------------------------------------
    # How
    # ---------------------------------------------------------------
    "How": "怎么做",
    (
        "Seven definitions do not yet tell you *which retriever to build "
        "first*. A reasonable order of operations, and the order this "
        "book takes, is:"
    ): (
        "七个定义还告诉不了你 *先搭哪个检索器* 。"
        "一个合理的上手顺序，也是本书采用的顺序，是这样的："
    ),
    (
        "**Start with plain full-text search** — `rg` over the repo, or "
        "SQLite FTS5 over a collection of markdown notes — before you "
        "even write a chunker {cite}`fanyamin2026kb_pipeline`. If this "
        "does not already work, nothing downstream will rescue you: "
        "embeddings do not make bad file organisation findable. The "
        "vast majority of personal KBs, and an uncomfortable share of "
        "project KBs, are still operating below this line."
    ): (
        "**先从朴素的全文搜索开始** —— 对着仓库跑 `rg`，"
        "或者给一堆 markdown 笔记套一个 SQLite FTS5 —— "
        "甚至还没动手写 chunker 之前 "
        "{cite}`fanyamin2026kb_pipeline`。"
        "如果这一步都跑不起来，后面任何东西都救不了你："
        "embedding 并不能把一份组织混乱的文件体系变得“找得到”。"
        "绝大多数个人知识库，以及一部分不那么好看的项目知识库，"
        "至今仍在这条线以下运行。"
    ),
    (
        "**Upgrade to BM25** as soon as the full-text stage stops "
        "keeping up — when you want ranking by term rarity, field "
        "weighting, or phrase matching. BM25 is almost free, and it is "
        "a real baseline: *if the BM25 baseline beats you, you do not "
        "yet have a retrieval system, you have a vector store with "
        "decorations.*"
    ): (
        "**升级到 BM25**，"
        "一旦全文搜索阶段开始跟不上 —— "
        "你开始想要按词的稀有度排序、按字段加权、或者做短语匹配 —— 就该换了。"
        "BM25 几乎是免费的，而且它是一条真正的基线："
        "*如果 BM25 基线把你打赢了，"
        "你手里还不是一个检索系统，而是一个挂了一些装饰的向量库。*"
    ),
    (
        "**Add dense retrieval** when you can afford embeddings and you "
        "have at least one query class that BM25 clearly fails on. For "
        "code KBs, that class is \"paraphrased intent\" (Chapter 10)."
    ): (
        "**加上稠密检索**，"
        "当你能负担得起 embedding、"
        "且至少有一类查询 BM25 明显答不好时。"
        "对代码知识库而言，这类查询就是“意译式提问”（第 10 章）。"
    ),
    (
        "**Fuse lexical and dense with RRF** {cite}`cormack2009rrf` "
        "once both retrievers independently work. Fusion makes both "
        "systems better and *almost never* makes either worse — but "
        "only if both rankers are individually sane."
    ): (
        "**用 RRF 把词法和稠密融合起来** {cite}`cormack2009rrf`，"
        "在两个检索器各自都能独立跑起来之后。"
        "融合会让两边都变强，而且 *几乎永远* 不会让任何一边变差 —— "
        "前提是两边各自都是合格的排序器。"
    ),
    (
        "**Add a cross-encoder reranker** only when fusion with field "
        "weighting and freshness decay is measured and *still leaving "
        "precision on the table* {cite}`nogueira2019passage` "
        "{cite}`reimers2019sbert`. The reranker replaces the top-k "
        "slice of the fused list, not the fused list itself; a "
        "stage-1 top-100 reranked down to a stage-2 top-10 is the "
        "canonical shape. Skip this step on a KB whose precision at "
        "top-3 is already good enough — adding a cross-encoder only "
        "buys latency in that regime."
    ): (
        "**加一个交叉编码器的 reranker**，"
        "只有在融合 + 字段加权 + 新鲜度衰减已经被量化过、"
        "且 *明显还把精度留在桌上* 的时候才加 "
        "{cite}`nogueira2019passage` {cite}`reimers2019sbert`。"
        "reranker 替换的是融合列表里 top-k 的那一段，"
        "而不是整张融合列表本身；"
        "“第一阶段 top-100，重排到第二阶段 top-10”是最常见的形态。"
        "如果一个知识库在 top-3 的精度上已经够用，就跳过这一步 —— "
        "再加交叉编码器，在这种场景下只是在买延迟。"
    ),
    (
        "**Add a generator** only after retrieval and re-ranking are "
        "measured. A well-retrieved-but-badly-generated answer is a "
        "citation problem; a badly-retrieved-but-fluently-spoken "
        "answer is a hallucination problem. The book treats the "
        "second as the more expensive failure mode and delays "
        "generator tuning until Chapter 13."
    ): (
        "**最后才加生成器**，"
        "而且要在检索和重排都已经被量化过之后。"
        "“检索对但生成坏”是一个引用问题，"
        "“检索烂但生成顺”是一个幻觉问题。"
        "本书把后者当成更昂贵的故障模式，"
        "把生成器的调优推迟到第 13 章再谈。"
    ),
    (
        "**Evaluate before tuning anything** {cite}`thakur2021beir`. "
        "This is the step everyone skips. The book does not."
    ): (
        "**调任何东西之前先评估** {cite}`thakur2021beir`。"
        "这是所有人都会跳过的那一步。本书不跳。"
    ),
    (
        "**Consider GraphRAG only when the query workload demands it** "
        "{cite}`edge2024graphrag`. If more than, say, 20% of real "
        "queries are globally framed — *\"what are the main "
        "components\", \"how has X evolved\", \"which modules depend on "
        "which\"* — the cost curve favours a graph. If they are mostly "
        "local — *\"where is X called\", \"what does Y return\"* — it "
        "does not."
    ): (
        "**只有在查询负载真的需要的时候才考虑 GraphRAG** "
        "{cite}`edge2024graphrag`。"
        "如果真实查询中，"
        "比如说超过 20% 都是全局框架下的问题 —— "
        "*“主要组件有哪些”、“X 是怎么演化的”、“哪些模块依赖哪些模块”* —— "
        "成本曲线就会倒向图；"
        "如果大部分是局部的 —— "
        "*“X 在哪被调用”、“Y 返回什么”* —— 就不会。"
    ),
    (
        "The blog post underlying this book {cite}`fanyamin2026deepwiki` "
        "uses the same core ordering, and uses it as an argument "
        "against what it calls the \"Demo-grade approach\": "
        "ingest-then-LLM, with neither a ranking baseline nor an "
        "evaluation harness. This chapter adds steps 0, 4, 6, and 7, "
        "which the blog treats implicitly."
    ): (
        "作为本书底稿的那篇博客 {cite}`fanyamin2026deepwiki`，"
        "用的是同一个核心顺序，"
        "并以此反驳那种它称为“Demo 级做法”的路线："
        "直接“塞数据然后喂给 LLM”，"
        "既没有排序基线，也没有评估脚手架。"
        "本章把博客里隐含处理的第 0 步、第 4 步、第 6 步和第 7 步，"
        "显式补了出来。"
    ),
    # ---------------------------------------------------------------
    # Substrate choice
    # ---------------------------------------------------------------
    "Choosing the retrieval substrate": "怎么选检索底座",
    (
        "At some point between step 2 and step 3, you will stop being "
        "able to hide behind *\"we'll pick a vector store later\"*. The "
        "choice of substrate — the thing that actually stores and "
        "searches your index — materially constrains every lever in "
        "this chapter. Field weighting, freshness decay, structured "
        "filtering, hybrid fusion: each is either a one-line feature "
        "or a ground-up engineering project, depending on the "
        "substrate. The four realistic options as of 2026, and the "
        "workloads each earns "
        "{cite}`fanyamin2026pgvector_rag` "
        "{cite}`fanyamin2026elasticsearch_rag`:"
    ): (
        "在第 2 步和第 3 步之间的某个时刻，"
        "你就再也藏不进 *“向量库晚点再选”* 这句话后面了。"
        "底座 —— 真正帮你存索引、搜索引索的那个东西 —— "
        "会实打实地约束住本章里提到的每一根操纵杆。"
        "字段加权、新鲜度衰减、结构化过滤、混合融合："
        "每一项在不同底座上，"
        "要么就是一行配置的内建能力，要么就是一个从零做起的工程。"
        "截至 2026 年，现实的选择基本只有下面四种，"
        "以及它们各自配得上的负载 "
        "{cite}`fanyamin2026pgvector_rag` "
        "{cite}`fanyamin2026elasticsearch_rag`："
    ),
    "Substrate": "底座",
    "Best when": "适合的场景",
    "Pays for itself when": "何时值回票价",
    "Skip if": "什么情况下直接跳过",
    (
        "**Plain full-text** (`rg`, SQLite FTS5, PostgreSQL `tsvector`)"
    ): (
        "**朴素全文搜索**（`rg`、SQLite FTS5、PostgreSQL 的 `tsvector`）"
    ),
    (
        "You are one person; the corpus fits on one machine; the hard "
        "question is *find the file*, not *rank the paragraph*."
    ): (
        "你是一个人在战斗；整个语料能装下一台机器；"
        "真正难的问题是 *“找到那份文件”*，而不是 *“给段落排序”*。"
    ),
    (
        "Cost is zero; latency is sub-second; no model dependency."
    ): (
        "成本为零；延迟在亚秒级；完全不依赖任何模型。"
    ),
    (
        "You need paraphrase matching or ranked top-k across dozens of "
        "documents."
    ): (
        "当你需要“意译匹配”、"
        "或是在几十份文档间做有排序的 top-k 时，就该换了。"
    ),
    "**pgvector on PostgreSQL**": "**PostgreSQL 上的 pgvector**",
    (
        "You already run PostgreSQL; corpus is under a few million "
        "vectors; you want vectors and business rows to `JOIN`."
    ): (
        "你本来就在用 PostgreSQL；向量数量在几百万以下；"
        "你希望向量能和业务表直接 `JOIN`。"
    ),
    (
        "Zero new operational surface; ACID; one `CREATE EXTENSION "
        "vector`. HNSW + cosine distance handles most paraphrase "
        "queries at millisecond latency."
    ): (
        "没有新增任何运维面；ACID 天然具备；"
        "一条 `CREATE EXTENSION vector` 就开张。"
        "HNSW + 余弦距离在毫秒级别就能搞定绝大多数意译查询。"
    ),
    (
        "You need first-class BM25, field weighting, or "
        "function-scoring built in (you can layer them on with "
        "`tsvector`, but you are now writing the features "
        "Elasticsearch ships)."
    ): (
        "当你需要原生的 BM25、字段加权、函数评分 —— "
        "虽然也可以用 `tsvector` 往上叠，"
        "但那时你写的其实就是 Elasticsearch 自带的那些功能。"
    ),
    "**Elasticsearch / OpenSearch**": "**Elasticsearch / OpenSearch**",
    (
        "You need BM25 *and* vectors *and* structured filtering *and* "
        "field weighting *and* freshness scoring in one query; your "
        "users search with identifier literals as often as with "
        "paraphrases."
    ): (
        "你在一次查询里同时需要 BM25、向量、"
        "结构化过滤、字段加权和新鲜度评分；"
        "你的用户用字面标识符搜索的频率，"
        "和用意译搜索的频率不相上下。"
    ),
    (
        "Native hybrid retrieval with RRF, Function Score for decay, "
        "bool queries for filtering, Kibana for quality inspection."
    ): (
        "带 RRF 的原生混合检索、"
        "用 Function Score 做衰减、"
        "用 bool 查询做过滤、用 Kibana 检查数据质量。"
    ),
    (
        "You do not have JVM capacity; a single node is not enough for "
        "your traffic; the team has no operational experience with it."
    ): (
        "你没有 JVM 运维能力；单节点撑不住你的流量；"
        "团队里没人有用它的经验。"
    ),
    (
        "**Specialised vector DB** (Pinecone, Milvus, Qdrant, Weaviate, "
        "…)"
    ): (
        "**专用向量数据库**（Pinecone、Milvus、Qdrant、Weaviate 等等）"
    ),
    (
        "Corpus is tens of millions of vectors or more; you need "
        "multi-tenant isolation, auto-sharding, or managed SLAs."
    ): (
        "语料量达到千万级及以上；"
        "你需要多租户隔离、自动分片，或者托管化的 SLA。"
    ),
    (
        "Scale and managed-service SLAs beyond what a single pgvector "
        "or ES cluster will give you."
    ): (
        "规模与托管服务 SLA 已经超出一套 pgvector 或 ES 集群的能力范围。"
    ),
    (
        "Corpus is under a few million; cost transparency matters; you "
        "do not need the scale knobs."
    ): (
        "当语料只有几百万规模、"
        "你很看重成本可见性、"
        "而且也根本用不到那些“规模旋钮”时，就别碰了。"
    ),
    (
        "The book's running prose-layer example fits comfortably in "
        "pgvector; the running code-layer example is larger but still "
        "lives inside a pgvector + BM25 hybrid. Neither needs "
        "Elasticsearch, let alone a specialised vector database. That "
        "is not an accident — it is the *typical* scale of a software "
        "project's knowledge base. The \"defaults-first\" heuristic is: "
        "**start with pgvector, add Elasticsearch when mixed "
        "identifier-literal and paraphrase queries force your hand, and "
        "keep specialised vector stores in reserve for the scale cliff "
        "you will probably never hit** {cite}`fanyamin2026pgvector_rag`."
    ): (
        "本书的文本层示例放在 pgvector 里完全够用；"
        "代码层示例更大，但也仍然住在 pgvector + BM25 的混合方案里。"
        "两边都不需要 Elasticsearch，更不需要专用向量数据库。"
        "这不是巧合 —— 这恰恰就是一个软件项目知识库的*典型*规模。"
        "“默认先用最简单的”原则就是："
        "**先上 pgvector；"
        "只有当字面标识符查询和意译查询混在一起、逼得你不得不升级时，"
        "才加 Elasticsearch；"
        "专用向量库则留给那道你大概率永远也不会撞上的规模悬崖** "
        "{cite}`fanyamin2026pgvector_rag`。"
    ),
    # ---------------------------------------------------------------
    # Example
    # ---------------------------------------------------------------
    "Example": "示例",
    (
        "A toy corpus will do. Imagine four snippets in a Go repository:"
    ): (
        "一个玩具语料就够了。设想一个 Go 仓库里的四段代码："
    ),
    # Code block — msgid has literal newlines between lines. Translation
    # is identical to the source (code is rendered verbatim) but the key
    # must match exactly, newlines and all.
    (
        "D1  func runSync(ctx context.Context) error { ... }   "
        "// internal/worker/pool.go:40\n"
        "D2  defer func() { if r := recover(); r != nil { ... } }  "
        "// internal/worker/pool.go:55\n"
        "D3  func drainOnShutdown() { ... }                     "
        "// internal/worker/pool.go:287\n"
        "D4  // how to safely shut the worker pool down        "
        "// doc/runbook/shutdown.md:12\n"
    ): (
        "D1  func runSync(ctx context.Context) error { ... }   "
        "// internal/worker/pool.go:40\n"
        "D2  defer func() { if r := recover(); r != nil { ... } }  "
        "// internal/worker/pool.go:55\n"
        "D3  func drainOnShutdown() { ... }                     "
        "// internal/worker/pool.go:287\n"
        "D4  // how to safely shut the worker pool down        "
        "// doc/runbook/shutdown.md:12\n"
    ),
    "Now three queries, and how each retriever would score them:": (
        "下面三条查询，以及每种检索器会怎么给它们打分："
    ),
    "Query": "查询",
    "BM25 winner": "BM25 的赢家",
    "Dense winner": "稠密的赢家",
    "RRF winner": "RRF 的赢家",
    "GraphRAG winner": "GraphRAG 的赢家",
    "*\"who calls `runSync`\"*": "*“谁调用了 `runSync`”*",
    "D1, then D3 (identifier match)": "D1，其次 D3（标识符匹配）",
    "D1, then D3": "D1，其次 D3",
    "D1 — agreement is cheap": "D1 —— 两边一致时代价最低",
    "D1 via the call-graph edge `caller → runSync`": (
        "通过调用图上 `caller → runSync` 这条边找到 D1"
    ),
    "*\"how do we wait for workers to finish\"*": (
        "*“我们怎么等 worker 执行完”*"
    ),
    "D4 (keyword \"wait\"/\"workers\") but misses D3": (
        "D4（关键字 “wait” / “workers” 命中），但漏掉了 D3"
    ),
    "D3 (paraphrase of \"drain on shutdown\")": (
        "D3（“drain on shutdown” 的意译）"
    ),
    "D3 and D4 both rank highly": "D3 和 D4 都排在前面",
    "D3 via graph walk from `worker-pool` community": (
        "从 `worker-pool` 社区出发沿图行走找到 D3"
    ),
    "*\"what are the main shutdown concerns in this package\"*": (
        "*“这个 package 里关于 shutdown 的主要关注点有哪些”*"
    ),
    "none of the four is obviously best": "四个里没有哪一个是明显更好的",
    "same — dense over-weights any single chunk": (
        "同上 —— 稠密会在任何单一 chunk 上过度加权"
    ),
    "same — RRF cannot invent a global view": (
        "同上 —— RRF 无法凭空造出一个全局视角"
    ),
    "a pre-computed summary of the `shutdown` community": (
        "一份预先算好的 `shutdown` 社区摘要"
    ),
    (
        "The first two rows are the case for hybrid retrieval: neither "
        "retriever alone answers both queries well. The third row is "
        "the case for GraphRAG: neither BM25 nor dense nor their fusion "
        "can answer a global question from four disconnected chunks. "
        "You can force an LLM to guess an answer; you cannot force any "
        "of those retrievers to *find* it. Chapter 12 walks through an "
        "actual RRF implementation from the code-layer reference "
        "implementation and measures the effect on real queries; "
        "Chapter 19 does the equivalent walkthrough for a "
        "GraphRAG-local-style graph over code."
    ): (
        "前两行支持“混合检索”的论点："
        "任何一个检索器单独上，都没办法同时答好这两条查询。"
        "第三行则是“GraphRAG”的论点："
        "不论 BM25、稠密，还是它们的融合，"
        "都没办法从四段互不相连的 chunk 里给出全局答案。"
        "你可以逼 LLM 猜一个答案，"
        "但你逼不出任何一个上述检索器去*真正找到*它。"
        "第 12 章会走一遍代码层参考实现里真实的 RRF 代码，"
        "并度量它在真实查询上的效果；"
        "第 19 章会对一张“GraphRAG-local 风格”的代码图做同样的事。"
    ),
    (
        "A competing view a reader should weigh is **dense-only "
        "retrieval with long context packing** — the shape that many "
        "*\"just throw the repo at Gemini 2.5 or Claude Opus 4\"* "
        "approaches take. For small, low-traffic repositories this can "
        "be perfectly adequate, and it has the clear advantage of "
        "needing no infrastructure. Its disadvantages are latency, "
        "cost, and — critically — that it loses structural filtering: "
        "*\"only functions in package `worker`\"* is a one-line "
        "predicate over a BM25 index and a prompt-engineering "
        "nightmare in a context-only pipeline "
        "{cite}`fanyamin2026deepwiki`. It also cannot, in principle, "
        "answer the third row of the table above any better than "
        "vanilla RAG: a million-token context without structure is "
        "still a bag of chunks."
    ): (
        "有一种需要读者对比权衡的对立观点："
        "**纯稠密检索 + 长上下文塞进去**，"
        "也就是很多 *“直接把整个仓库甩给 Gemini 2.5 或 Claude Opus 4”* 路线的形态。"
        "对规模小、流量也小的仓库，这样做完全可以胜任，"
        "而且有一个明显的优点：基础设施归零。"
        "它的缺点则是延迟、成本，"
        "以及 —— 这一点最关键 —— 它丢掉了结构化过滤："
        "*“只要 `worker` 包里的函数”* 在 BM25 索引上是一行谓词，"
        "在一个纯上下文流水线里则是一场 prompt 工程噩梦 "
        "{cite}`fanyamin2026deepwiki`。"
        "而且原则上，"
        "它对上面第三行那种全局问题，也不会比 vanilla RAG 答得更好："
        "一百万 token 的上下文，没有结构，依然只是一袋 chunk。"
    ),
    # ---------------------------------------------------------------
    # Conclusion
    # ---------------------------------------------------------------
    "Conclusion": "小结",
    "Four claims summarise the chapter and set up the rest of the book.": (
        "四句话总结本章，也为全书后文立起框架。"
    ),
    (
        "*Ranking is the hard part of retrieval; generation is the easy "
        "part.* Teams that optimise the generator before the ranker end "
        "up with fast nonsense. The book assumes this lesson has been "
        "learnt — every retriever before every generator, every "
        "benchmark before every retriever, every citation before every "
        "answer."
    ): (
        "*检索真正难的部分是排序；生成反倒是容易的那一半。* "
        "先去调生成器、再去调排序器的团队，"
        "最后得到的是一台高速运转的胡说八道机器。"
        "本书默认这条教训已经被你吃过了 —— "
        "每一个检索器都要先于它的生成器、"
        "每一次基准评估都要先于它要评估的那个检索器、"
        "每一个引用都要先于它所支撑的那个答案。"
    ),
    (
        "*Vanilla RAG is a baseline, not a destination.* Its five "
        "limits — chunk boundaries, similarity-vs-relevance, multi-hop "
        "gaps, staleness, and faithfulness — are engineering problems "
        "with engineering answers. The rest of this book is the long "
        "form of those answers."
    ): (
        "*Vanilla RAG 是基线，不是终点。* "
        "它的五条边界 —— chunk 边界、相似 vs. 相关、多跳鸿沟、"
        "索引过期、忠实性 —— 都是工程问题，也都有工程解。"
        "本书接下来的每一章，都是这些工程解的展开版。"
    ),
    (
        "*GraphRAG is not an upgrade to vanilla RAG; it is a different "
        "cost curve for a different class of question.* Adopt it when "
        "your queries are globally framed, skip it when they are not, "
        "and in either case remember that the graph is itself an asset "
        "— it outlives any one retrieval strategy."
    ): (
        "*GraphRAG 不是 vanilla RAG 的升级版；"
        "它是为另一类问题准备的另一条成本曲线。* "
        "查询是全局框架下的，就用它；不是，就不用；"
        "不管用不用，都要记住那张图本身就是资产 —— "
        "它活得比任何一个具体的检索策略都久。"
    ),
    (
        "*Substrate is a workload choice, not a fashion choice.* The "
        "decision between `rg`, pgvector, Elasticsearch, and a "
        "specialised vector database is driven by the shape of your "
        "queries and the size of your corpus, not by which project "
        "trended on Hacker News last month. The most common mistake is "
        "to skip the first option and pay for the last."
    ): (
        "*底座是负载决定的，不是时尚决定的。* "
        "在 `rg`、pgvector、Elasticsearch 和专用向量数据库之间做选择，"
        "应该由你查询的形状和语料的规模决定，"
        "不应该由上个月谁上了 Hacker News 的热门决定。"
        "最常见的错误是 —— 跳过第一个选项，"
        "然后去为最后一个选项付钱。"
    ),
    # ---------------------------------------------------------------
    # References
    # ---------------------------------------------------------------
    "References": "参考文献",
}
