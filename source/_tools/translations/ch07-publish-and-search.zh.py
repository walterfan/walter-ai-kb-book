"""Chinese translations for source/part2-prose-layer/ch07-publish-and-search.md.

See source/_tools/translations/ch02-ir-rag-primer.zh.py for the full
style guide. Chapter-specific notes:

- Sphinx, MyST, MyST-Parser, Elasticsearch, OpenSearch, Meilisearch,
  Algolia, Bleve, Lucene, Porter, Damerau-Levenshtein, kagome,
  go-jieba, BM25, TF-IDF, RAG, JVM, Docker, CJK, CLI, HTTP, PDF,
  JSON, Furo, GitHub Pages, S3, Read the Docs kept in English.
- Six-verb CLI: `kb-cli`, `serve` kept in English.
- `IndexEngine`, `SearchService`, `Search`, `SearchResult`,
  `AddPage`, `UpdatePage`, `DeletePage`, `LoadAndIndex`, `tokenize`,
  `buildSearchIndex`, `CreatePage`, `rebuildAllLocked`,
  `searchTerms`, `pages`, `verify` kept in English as identifiers.
- `$b$` math kept verbatim.
- CommonMark emphasis rule applies.
"""

PO_PATH = "part2-prose-layer/ch07-publish-and-search.po"

TRANSLATIONS: dict[str, str] = {
    # ---- Title + headings + mindmap ----
    "Chapter 7 — Publish and Search": "第 7 章 —— 发布与搜索",
    (
        "This chapter at a glance — the decisive trade-off "
        "between a bespoke in-memory index and an operational "
        "search cluster, the ten-line tokeniser whose defaults "
        "carry surprising weight, the failure modes prefix-match "
        "search has on identifier-literal and CJK queries, and "
        "the staircase of scaling moves that keep `Search(...)` "
        "a single stable interface across five orders of "
        "magnitude of corpus size:"
    ): (
        "本章一页速览 —— "
        "“**定制的内存索引** vs. **一套要运维的搜索集群**”之间"
        "那一次**决定性的取舍**；"
        "那个**十行**的分词器 —— "
        "它的默认值却意外地承重；"
        "**前缀匹配搜索**在**标识符字面量查询**和 "
        "**CJK 查询**上的失败形态；"
        "以及一整条**台阶式**的扩容路径 —— "
        "让 `Search(...)` 在**五个数量级**的语料规模上"
        "仍然是**同一个稳定的接口**："
    ),
    "Why": "为什么",
    "What": "是什么",
    "How": "怎么做",
    "Example": "示例",
    "Conclusion": "结论",
    "References": "参考文献",
    "Competing approaches": "其他做法",
    "The in-memory index": "内存索引",
    "Tokenisation": "分词",
    "Building the postings list": "构建 postings list",
    "Querying": "查询",
    "Live updates": "实时更新",
    "Static publishing with Sphinx": "用 Sphinx 做静态发布",
    "Where the tiny search engine fails — and why that is still fine": (
        "这台小小的搜索引擎在哪里会失败 —— 以及为什么那仍然没关系"
    ),
    "Common mistakes in wiring up search": "在把搜索接起来时的常见错误",

    # ---- Why ----
    (
        "By the end of Chapter 6 we have a committed tree of "
        "well-formed Markdown pages with honest frontmatter. Two "
        "questions remain before Part II can close:"
    ): (
        "第 6 章走到尾声时，"
        "我们已经有了**一棵提交进 Git 的、格式规范的 Markdown 页面树**，"
        "带着诚实的 frontmatter 。"
        "在第二部分能够收尾之前，还剩两个问题："
    ),
    (
        "**How do readers find a page?** Navigation is one "
        "answer (the Diátaxis-shaped toctree does that). "
        "*Search* is the other, and it is the first place a KB "
        "fails when it grows past a few hundred pages."
    ): (
        "**读者怎么找到某一页？** "
        "导航是一条答案（由 Diátaxis 形状的 toctree 给出）。 "
        "*搜索* 是另一条。"
        "当一个知识库长过几百页时，"
        "**搜索是它最先崩坏的地方**。"
    ),
    (
        "**How do readers consume pages?** The backend serves "
        "dynamic rendering, but the same files must also build "
        "as a static site — so the KB survives the server, can "
        "be mirrored, and can be vendored into other repos."
    ): (
        "**读者怎么消费页面？** "
        "后端提供动态渲染，"
        "**但同一批文件也必须能构建成一个静态站点** —— "
        "好让这个知识库"
        "**能在服务器之外活下来**、**可以被镜像**、"
        "**可以被 vendor 进其他仓库**。"
    ),
    (
        "This chapter covers both, and it tries to resist two "
        "temptations the ecosystem pushes hard. The first: "
        "\"just plug in Elasticsearch\". An operational search "
        "cluster is its own on-call rotation; a file-based wiki "
        "with tens of thousands of pages does not earn it. The "
        "second: \"do not ship your own search\". A ten-line "
        "tokeniser and a prefix-match loop is enough to make 95 "
        "% of a software KB usable, and it is fully under your "
        "control, debuggable, and deployable in a single binary."
    ): (
        "这一章两个都讲，"
        "同时**顶住生态里两种被反复推销的诱惑**。"
        "第一种：“直接上 Elasticsearch”。"
        "一套要运维的搜索集群本身就是**一套独立的 on-call 排班**；"
        "一个几万页级别的文件型 wiki **还配不上这个代价**。"
        "第二种：“别自己发自家搜索”。"
        "**十行**分词器 + **一个前缀匹配循环**"
        "已经足够让 95% 的软件知识库**够用**，"
        "并且它**完全在你手里**、**可调试**、"
        "**能塞进单个 binary 里发布**。"
    ),

    # ---- What ----
    "Two systems cooperate:": "两个系统合作完成这件事：",
    (
        "**In-memory index** (this chapter, "
        "`backend/internal/wiki/index.go`): a Go struct mapping "
        "slugs to parsed pages, plus a side map `searchTerms: "
        "map[term]→[]slug`. It runs inside the `kb-cli serve` "
        "process, holds everything for live lookup, and is "
        "rebuilt from disk on every pipeline stage that writes."
    ): (
        "**内存索引**（本章，`backend/internal/wiki/index.go` ）："
        "一个 Go struct —— "
        "把 slug 映射到已解析的 page ，"
        "外加一张旁挂表 `searchTerms: map[term]→[]slug` 。"
        "它跑在 `kb-cli serve` 进程里，"
        "把**全部东西**留在内存里给实时查询用，"
        "**每一个会写入的流水线阶段都会从磁盘把它重建一次**。"
    ),
    (
        "**Static publisher** "
        "(`wiki-template/metadata/_sphinx/`): a Sphinx "
        "{cite}`sphinx` + MyST-Parser {cite}`myst_parser` build "
        "target whose input is the same `content/` tree. Running "
        "`make sphinx-build` emits a fully static HTML site into "
        "`metadata/_build/html/` that can be hosted anywhere "
        "(GitHub Pages, S3, a laptop)."
    ): (
        "**静态发布器** "
        "（`wiki-template/metadata/_sphinx/` ）："
        "一个 Sphinx {cite}`sphinx` + MyST-Parser "
        "{cite}`myst_parser` 的构建目标，"
        "输入就是同一棵 `content/` 树。"
        "跑一次 `make sphinx-build` ，"
        "就会往 `metadata/_build/html/` 里产出一份**完全静态的 HTML 站**，"
        "**随便什么地方都能托管** —— "
        "GitHub Pages、S3、你的笔记本电脑。"
    ),
    (
        "Neither system owns the content; both are *views* of "
        "the filesystem. Delete the server, and the static build "
        "still renders. Delete the static build, and the server "
        "still searches. The file is the authoritative artefact, "
        "as Chapter 4 promised."
    ): (
        "**两套系统都不拥有内容；**"
        "**两者都是对文件系统的 *视图* 。**"
        "把服务器删掉，静态构建照常渲染。"
        "把静态构建删掉，服务器照常搜索。"
        "**文件才是权威制品**，"
        "第 4 章已经这么承诺过。"
    ),

    # ---- How: in-memory index ----
    "The core data structure fits on one screen:": (
        "核心数据结构**一屏就能装下**："
    ),
    "`IndexEngine` — slug map, plus a few specialised views.": (
        "`IndexEngine` —— slug 映射表，加上几张专门用途的视图。"
    ),
    (
        "\tHeading  string `json:\"heading\"`\n\tExcerpt  string `json:\"excerpt\"`\n}\n\ntype SearchResult struct {\n\tPages    []PageSummary `json:\"pages,omitempty\"`\n\tSections []SectionRef  `json:\"sections,omitempty\"`\n\tTotal    int           `json:\"total\"`\n}\n\ntype IndexEngine struct {\n\tmu sync.RWMutex\n\n\tpages         map[string]*Page\n"
    ): (
        "\tHeading  string `json:\"heading\"`\n\tExcerpt  string `json:\"excerpt\"`\n}\n\ntype SearchResult struct {\n\tPages    []PageSummary `json:\"pages,omitempty\"`\n\tSections []SectionRef  `json:\"sections,omitempty\"`\n\tTotal    int           `json:\"total\"`\n}\n\ntype IndexEngine struct {\n\tmu sync.RWMutex\n\n\tpages         map[string]*Page\n"
    ),
    (
        "Eight auxiliary maps — by title letter, category, word, "
        "author, `doc_type`, source type, `verification_status` "
        "— are all derived from `pages` and rebuilt in one pass. "
        "The only field that matters for full-text search is "
        "`searchTerms`."
    ): (
        "有八张辅助视图 —— "
        "按标题首字母、按 category、按词、按作者、"
        "按 `doc_type` 、按 source type、"
        "按 `verification_status` —— "
        "**全部**从 `pages` 派生，"
        "**一轮遍历全部重建**。"
        "就**全文检索**而言，"
        "**真正重要的字段只有 `searchTerms`** 。"
    ),

    # ---- Tokenisation ----
    "The tokeniser is ten lines of Go:": "分词器是**十行**的 Go：",
    "`tokenize` — lowercase, letter-or-digit split, length ≥ 2, dedupe.": (
        "`tokenize` —— 转小写、按“非字母非数字”切、长度 ≥ 2、去重。"
    ),
    (
        "func (idx *IndexEngine) buildSearchIndex() {\n\tidx.searchTerms = make(map[string][]string)\n\tfor slug, p := range idx.pages {\n\t\tterms := tokenize(p.Frontmatter.Title + \" \" + p.Body + \" \" + strings.Join(p.Frontmatter.Tags, \" \"))\n\t\tfor _, term := range terms {\n\t\t\tidx.searchTerms[term] = append(idx.searchTerms[term], slug)\n\t\t}\n\t}\n}\n\nfunc tokenize(text string) []string {\n\ttext = strings.ToLower(text)\n\twords := strings.FieldsFunc(text, func(r rune) bool {\n\t\treturn !unicode.IsLetter(r) && !unicode.IsDigit(r)\n\t})\n"
    ): (
        "func (idx *IndexEngine) buildSearchIndex() {\n\tidx.searchTerms = make(map[string][]string)\n\tfor slug, p := range idx.pages {\n\t\tterms := tokenize(p.Frontmatter.Title + \" \" + p.Body + \" \" + strings.Join(p.Frontmatter.Tags, \" \"))\n\t\tfor _, term := range terms {\n\t\t\tidx.searchTerms[term] = append(idx.searchTerms[term], slug)\n\t\t}\n\t}\n}\n\nfunc tokenize(text string) []string {\n\ttext = strings.ToLower(text)\n\twords := strings.FieldsFunc(text, func(r rune) bool {\n\t\treturn !unicode.IsLetter(r) && !unicode.IsDigit(r)\n\t})\n"
    ),
    "Three choices encoded here are worth defending:": (
        "这里编码进去的**三个选择**值得单独辩护一下："
    ),
    (
        "**Unicode letter/digit, not ASCII whitespace.** "
        "`unicode.IsLetter` covers CJK characters, Cyrillic, "
        "Arabic — anything with a Unicode letter category — so a "
        "wiki in any language tokenises correctly."
    ): (
        "**用 Unicode 字母 / 数字，不是 ASCII 空白。** "
        "`unicode.IsLetter` 把 CJK 字符、西里尔字母、阿拉伯字母 —— "
        "**所有带 Unicode letter 类别的东西** —— 全都涵盖了，"
        "所以**任何语言**的 wiki 都能被**正确**分词。"
    ),
    (
        "**No stemming.** Porter's 1980 algorithm "
        "{cite}`porter1980stemming` would give better recall on "
        "English (\"install\" / \"installing\" / \"installed\" "
        "all collapse to \"instal\"), but it is "
        "language-specific and it makes search results "
        "surprising to engineers who expect literal matching. "
        "The trade-off goes the other way in a software KB."
    ): (
        "**不做词干提取。** "
        "Porter 1980 年的那个算法 {cite}`porter1980stemming` "
        "确实能在英文上把召回率提起来"
        "（“install” / “installing” / “installed”都塌成“instal”），"
        "**但它是语言相关的**，"
        "而且会让**期望字面匹配的工程师**对搜索结果感到意外。"
        "**在软件知识库里**，这笔取舍是**反过来**的。"
    ),
    (
        "**Length ≥ 2, deduped.** Kills single-letter noise; "
        "keeps memory linear in document length, not quadratic."
    ): (
        "**长度 ≥ 2，去重。** "
        "**干掉单字母噪声**；"
        "让内存在文档长度上**线性**增长，"
        "而不是**平方**增长。"
    ),

    # ---- Building postings list ----
    "Index construction is a nested loop, not a B-tree:": (
        "**构建索引就是一层嵌套循环，不是一棵 B-tree：**"
    ),
    "`buildSearchIndex` — tokenise every page, invert into a map.": (
        "`buildSearchIndex` —— 给每一页分词，倒排进一个 map。"
    ),
    (
        "\nfunc (idx *IndexEngine) buildTrustIndex(summaries []PageSummary) {\n\tidx.trustIndex = make(map[VerificationStatus][]PageSummary)\n\tfor _, s := range summaries {\n\t\tif s.VerificationStatus != \"\" {\n\t\t\tidx.trustIndex[s.VerificationStatus] = append(idx.trustIndex[s.VerificationStatus], s)\n\t\t}\n\t}\n}\n"
    ): (
        "\nfunc (idx *IndexEngine) buildTrustIndex(summaries []PageSummary) {\n\tidx.trustIndex = make(map[VerificationStatus][]PageSummary)\n\tfor _, s := range summaries {\n\t\tif s.VerificationStatus != \"\" {\n\t\t\tidx.trustIndex[s.VerificationStatus] = append(idx.trustIndex[s.VerificationStatus], s)\n\t\t}\n\t}\n}\n"
    ),
    (
        "For each page, tokenise `title + body + tags`, and for "
        "every token, append the slug. The result is a "
        "*postings list* in the classical IR sense "
        "{cite}`manning2008introduction` — a map from term to "
        "list of documents containing it. There is no tf/idf "
        "weight stored per token and no positional information, "
        "which is why the query side is also short."
    ): (
        "对每一页，"
        "把 `title + body + tags` 一起分词，"
        "**每一个 token 都把这一页的 slug 追加进去**。"
        "结果就是经典 IR 意义下的**一张 postings list** "
        "{cite}`manning2008introduction` —— "
        "一张从 term 到“包含该 term 的文档列表”的 map 。"
        "**没有**per-token 的 tf-idf 权重，**没有**位置信息，"
        "**所以**查询那一侧也很短。"
    ),

    # ---- Querying ----
    (
        "A query is tokenised the same way, each term is "
        "prefix-matched against the index's keys, and slugs are "
        "scored by \"how many query terms hit this document\":"
    ): (
        "查询也用**同一套分词**，"
        "每一个 term 都对索引的 key 做**前缀匹配**，"
        "然后 slug 按“**有多少个查询 term 命中了这页**”打分："
    ),
    "`Search` — prefix match, term-count score, sort, return summaries.": (
        "`Search` —— 前缀匹配、按命中 term 数打分、排序、返回摘要。"
    ),
    (
        "\tdefer idx.mu.RUnlock()\n\treturn idx.sourceIndex\n}\n\nfunc (idx *IndexEngine) GetTrustIndex() map[VerificationStatus][]PageSummary {\n\tidx.mu.RLock()\n\tdefer idx.mu.RUnlock()\n\treturn idx.trustIndex\n}\n\nfunc (idx *IndexEngine) Search(query, searchType string) (*SearchResult, error) {\n\tidx.mu.RLock()\n\tdefer idx.mu.RUnlock()\n\n\tterms := tokenize(query)\n\tif len(terms) == 0 {\n\t\treturn &SearchResult{}, nil\n\t}\n\n\tslugScores := make(map[string]int)\n\tfor _, term := range terms {\n\t\tfor indexTerm, slugs := range idx.searchTerms {\n\t\t\tif strings.HasPrefix(indexTerm, term) {\n\t\t\t\tfor _, slug := range slugs {\n\t\t\t\t\tslugScores[slug]++\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n\n\ttype scored struct {\n\t\tslug  string\n\t\tscore int\n\t}\n\tvar scoredSlugs []scored\n\tfor slug, score := range slugScores {\n\t\tscoredSlugs = append(scoredSlugs, scored{slug, score})\n\t}\n\tsort.Slice(scoredSlugs, func(i, j int) bool {\n\t\treturn scoredSlugs[i].score > scoredSlugs[j].score\n\t})\n"
    ): (
        "\tdefer idx.mu.RUnlock()\n\treturn idx.sourceIndex\n}\n\nfunc (idx *IndexEngine) GetTrustIndex() map[VerificationStatus][]PageSummary {\n\tidx.mu.RLock()\n\tdefer idx.mu.RUnlock()\n\treturn idx.trustIndex\n}\n\nfunc (idx *IndexEngine) Search(query, searchType string) (*SearchResult, error) {\n\tidx.mu.RLock()\n\tdefer idx.mu.RUnlock()\n\n\tterms := tokenize(query)\n\tif len(terms) == 0 {\n\t\treturn &SearchResult{}, nil\n\t}\n\n\tslugScores := make(map[string]int)\n\tfor _, term := range terms {\n\t\tfor indexTerm, slugs := range idx.searchTerms {\n\t\t\tif strings.HasPrefix(indexTerm, term) {\n\t\t\t\tfor _, slug := range slugs {\n\t\t\t\t\tslugScores[slug]++\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n\n\ttype scored struct {\n\t\tslug  string\n\t\tscore int\n\t}\n\tvar scoredSlugs []scored\n\tfor slug, score := range slugScores {\n\t\tscoredSlugs = append(scoredSlugs, scored{slug, score})\n\t}\n\tsort.Slice(scoredSlugs, func(i, j int) bool {\n\t\treturn scoredSlugs[i].score > scoredSlugs[j].score\n\t})\n"
    ),
    "Four properties of this implementation:": (
        "这份实现有**四条属性**："
    ),
    (
        "**Prefix match**, not exact. A query for `insta` "
        "matches `install`, `installation`, and `installer`. "
        "This is the pragmatic compromise that covers most of "
        "what stemming would give."
    ): (
        "**前缀匹配**，不是精确匹配。"
        "查询 `insta` 会匹到 `install` 、 `installation` 、 `installer` 。"
        "**这是一次务实的妥协**，"
        "它覆盖掉了词干提取能给你的**大部分收益**。"
    ),
    (
        "**No BM25, no tf-idf** "
        "{cite}`manning2008introduction,robertson2009probabilistic`. "
        "The score is the cardinality of matching query terms. "
        "This is weaker than a real IR ranker, but at these "
        "document counts the user rarely notices."
    ): (
        "**没有 BM25、没有 tf-idf** "
        "{cite}`manning2008introduction,robertson2009probabilistic` 。"
        "得分就是“**命中了几个查询 term**”这件事的基数。"
        "这比一个**真正的 IR ranker** 弱，"
        "但**在本章所瞄准的文档数量级**上，"
        "用户**基本察觉不到**。"
    ),
    (
        "**No boolean operators**, no phrase queries, no fielded "
        "queries. A software KB's typical query is 1–3 keywords; "
        "giving up Lucene-style syntax buys simplicity."
    ): (
        "**不支持布尔运算符**，不支持短语查询、不支持字段限定查询。"
        "一个软件知识库里**典型的查询**是 1 到 3 个关键词；"
        "**放弃 Lucene 风格的查询语法**买回来的是**简洁**。"
    ),
    (
        "**Linear in `|searchTerms|` per query.** For the "
        "10k-page range this book targets, \"linear in the "
        "index\" is fast enough on a single thread. Past that, "
        "the correct move is to reach for Bleve or Meilisearch, "
        "not to reinvent those inside the CLI binary."
    ): (
        "**每次查询的复杂度在 `|searchTerms|` 上线性。** "
        "对本书瞄准的 1 万页量级来说，"
        "“**在索引上线性**”在**单线程**上就够快。"
        "**再往上**的正确做法是去摸 Bleve 或 Meilisearch，"
        "**而不是**在 CLI binary 里把它们**重新发明一遍**。"
    ),
    (
        "The whole search subsystem, end to end, is under 100 "
        "lines of Go. It is *correct* for the scale it targets, "
        "it is debuggable by any Go programmer, and it ships "
        "with the binary. When the scale changes, the interface "
        "does not — `SearchService` already takes a query string "
        "and returns `SearchResult`, and a future Bleve-backed "
        "implementation can drop in behind it without touching "
        "the HTTP or CLI layers."
    ): (
        "整套搜索子系统，端到端，"
        "**不到 100 行 Go** 。"
        "它在它瞄准的规模上 *是正确的* ，"
        "**任何一个 Go 程序员都能调它**，"
        "而且它就**跟着那个 binary 一起发布**。"
        "规模变了，**接口也不用变** —— "
        "`SearchService` **已经**接受一个查询字符串、返回一个 `SearchResult` ；"
        "哪天换成一个 Bleve 后端，"
        "可以直接**塞在接口后面**，"
        "**HTTP 和 CLI 这两层都不用动**。"
    ),

    # ---- Live updates ----
    (
        "Every write path (Chapter 5's `CreatePage`, the ingest "
        "loop of Chapter 6, the update path, the delete path) "
        "ends by calling `index.AddPage`, `index.UpdatePage`, or "
        "`index.DeletePage`, all of which take the lock and "
        "rebuild the derived maps:"
    ): (
        "每一条写入路径（第 5 章的 `CreatePage` 、"
        "第 6 章的 ingest 循环、更新路径、删除路径）"
        "最后都会调一下 "
        "`index.AddPage` 、 `index.UpdatePage` 、 "
        "或 `index.DeletePage` ，"
        "**每一个**都会拿锁、重建派生视图："
    ),
    "`AddPage` — single-writer, whole-map rebuild, simple enough to trust.": (
        "`AddPage` —— **单写**，**整张表重建**，**简单到值得信任**。"
    ),
    (
        "\n\tidx.pages = make(map[string]*Page)\n\tfor _, p := range pages {\n\t\tidx.pages[p.Frontmatter.Slug] = p\n\t}\n\n\tidx.rebuildAllLocked()\n"
    ): (
        "\n\tidx.pages = make(map[string]*Page)\n\tfor _, p := range pages {\n\t\tidx.pages[p.Frontmatter.Slug] = p\n\t}\n\n\tidx.rebuildAllLocked()\n"
    ),
    (
        "\"Rebuild everything\" sounds wasteful, but it is "
        "linear in the number of pages and runs exactly once per "
        "write, inside a mutex. It eliminates the traditional "
        "failure mode of incremental indexers: stale entries "
        "that nobody realises are there until a user complains. "
        "The cost is measured in milliseconds; the benefit is "
        "that the index is provably consistent with `pages` "
        "after every operation."
    ): (
        "“**全部重建**”听起来很浪费，"
        "但它在页面数上是**线性**的，"
        "并且每一次写入**只跑一次**，**全程锁内**。"
        "**它干掉了增量索引器那种典型失败形态：**"
        "**那些没人发现的过期条目**"
        "——直到用户抱怨才冒出来。"
        "**代价以毫秒计；**"
        "**收益是每一次操作之后，**"
        "索引与 `pages` 之间是**可证一致的**。"
    ),

    # ---- Static publishing ----
    (
        "For publishing, the prose-layer reference "
        "implementation does not invent a builder; it leverages "
        "Sphinx + MyST-Parser, the same stack this book is built "
        "with. A minimal `metadata/_sphinx/conf.py` looks like:"
    ): (
        "在发布这一块，"
        "文稿层参考实现**不去发明构建器** —— "
        "**直接借力** Sphinx + MyST-Parser，"
        "和**这本书自己**用的是同一套栈。"
        "一个**最小版**的 `metadata/_sphinx/conf.py` 长这样："
    ),
    (
        "extensions = [\"myst_parser\", \"sphinxcontrib.mermaid\"]\nsource_suffix = {\".md\": \"markdown\"}\nhtml_theme    = \"sphinx_rtd_theme\"\nmaster_doc    = \"index\"\n"
    ): (
        "extensions = [\"myst_parser\", \"sphinxcontrib.mermaid\"]\nsource_suffix = {\".md\": \"markdown\"}\nhtml_theme    = \"sphinx_rtd_theme\"\nmaster_doc    = \"index\"\n"
    ),
    (
        "The root `index.md` uses the same `INDEX.md` that "
        "`pipeline.Build()` regenerates after every ingest. That "
        "file is the bridge between the live server and the "
        "static site: both views consume it. A site build is one "
        "shell command:"
    ): (
        "根目录的 `index.md` 用的就是**那份 `INDEX.md`** —— "
        "`pipeline.Build()` 在**每一次 ingest 之后都会重新生成**它。"
        "**那份文件**就是**实时服务器**和**静态站**之间的桥："
        "**两种视图**都消费它。"
        "站点构建**一条 shell 命令**就够了："
    ),
    (
        "$ make sphinx-build WIKI_DIR=./demo\n$ ls ./demo/metadata/_build/html/\nindex.html  search.html  _static/  _sources/  ...\n"
    ): (
        "$ make sphinx-build WIKI_DIR=./demo\n$ ls ./demo/metadata/_build/html/\nindex.html  search.html  _static/  _sources/  ...\n"
    ),
    "Three things you get for free from Sphinx:": (
        "**从 Sphinx 里白捡的三件东西：**"
    ),
    (
        "**In-page search.** Sphinx emits a client-side "
        "JavaScript index that works offline, using the Porter "
        "stemmer at build time. Readers of the static site have "
        "a search that rivals the server's."
    ): (
        "**页内搜索。** "
        "Sphinx 会产出一份**客户端 JavaScript 索引**，"
        "**离线**也能用，"
        "构建时用 Porter stemmer 做词干。"
        "**静态站的读者拿到的搜索体验和服务器端不相上下。**"
    ),
    (
        "**Cross-references.** `{doc}`, `{ref}`, and citation "
        "roles resolve across the whole tree, and the build "
        "fails if they do not. This is far stricter than the "
        "live server's prefix match, and it catches broken "
        "references that `verify` did not."
    ): (
        "**交叉引用。** "
        "`{doc}` 、 `{ref}` 和各种引用 role "
        "会在**整棵树**上做解析，"
        "**解不出来**就**直接 build 失败**。"
        "这比实时服务器上的前缀匹配**严格得多**，"
        "**还会抓出** `verify` 没抓到的那些坏引用。"
    ),
    (
        "**A themeable output.** Read the Docs theme, Furo, book "
        "theme, PDF via xelatex — one Markdown source tree "
        "renders to all of them."
    ): (
        "**可换皮肤的输出。** "
        "Read the Docs 主题、Furo 、book theme、"
        "通过 xelatex 生成 PDF —— "
        "**同一棵 Markdown 源码树**可以渲染成**以上全部**。"
    ),
    (
        "What you give up is *interactivity*: the static site "
        "cannot create pages, rerank search by click-through, or "
        "show \"recent changes in the last hour\". For a "
        "software KB that is deliberately versioned in Git, that "
        "is the right trade-off. Mutation lives in the repo and "
        "in the server; publishing is a derived, immutable "
        "artefact."
    ): (
        "**你放弃的是 *交互性* ：**"
        "静态站**不能**创建页面、"
        "**不能**根据点击率把搜索结果重新排序、"
        "**也不能**显示“最近一小时的变更”。"
        "对一个**故意用 Git 做版本控制**的软件知识库来说，"
        "**这正是对的取舍**。"
        "**变更在仓库里、在服务器里；**"
        "**发布是一份派生的、不可变的制品。**"
    ),

    # ---- Example ----
    "Three queries against the same pages, walked through by hand.": (
        "**对同一批页面走三次查询**，**手工**演算一遍。"
    ),
    "Given these three pages under `content/`:": (
        "假设 `content/` 下有以下三页："
    ),
    (
        "`how-to/enable-tls.md` — `title: How to enable TLS`, "
        "tags `[tls, security]`"
    ): (
        "`how-to/enable-tls.md` —— "
        "`title: How to enable TLS` ，"
        "tags `[tls, security]` 。"
    ),
    (
        "`reference/api.md` — `title: API Reference`, body "
        "mentions \"install\" and \"tokenization\""
    ): (
        "`reference/api.md` —— "
        "`title: API Reference` ，"
        "正文里提到 “install” 和 “tokenization”。"
    ),
    (
        "`explanation/auth-model.md` — `title: Authentication "
        "Model`, body discusses \"TLS\" and \"tokens\""
    ): (
        "`explanation/auth-model.md` —— "
        "`title: Authentication Model` ，"
        "正文里讨论“TLS”和“tokens”。"
    ),
    "Query `tls`:": "**查询 `tls`：**",
    "tokens: `[\"tls\"]`": "tokens：`[\"tls\"]`",
    "prefix match on `tls` → hits `tls` in pages 1 and 3.": (
        "对 `tls` 做前缀匹配 → 命中第 1 页和第 3 页中的 `tls` 。"
    ),
    "scores: `{how-to/enable-tls: 1, explanation/auth-model: 1}`": (
        "得分：`{how-to/enable-tls: 1, explanation/auth-model: 1}`"
    ),
    "sort by score desc, return both.": "按得分倒序，两页都返回。",
    "Query `token`:": "**查询 `token`：**",
    "tokens: `[\"token\"]`": "tokens：`[\"token\"]`",
    "prefix match on `token` → hits `tokenization` (page 2) and `tokens` (page 3).": (
        "对 `token` 做前缀匹配 → "
        "命中第 2 页里的 `tokenization` "
        "和第 3 页里的 `tokens` 。"
    ),
    "scores: `{reference/api: 1, explanation/auth-model: 1}`": (
        "得分：`{reference/api: 1, explanation/auth-model: 1}`"
    ),
    "both returned.": "两页都返回。",
    "Query `tls token`:": "**查询 `tls token`：**",
    "tokens: `[\"tls\", \"token\"]`": "tokens：`[\"tls\", \"token\"]`",
    "page 3 hits both prefixes → score 2": (
        "第 3 页同时命中两个前缀 → 得分 2"
    ),
    "pages 1 and 2 hit one prefix each → score 1": (
        "第 1、2 页各命中一个前缀 → 得分 1"
    ),
    "order: `explanation/auth-model`, then the other two.": (
        "排序：`explanation/auth-model` 排第一，然后是另外两页。"
    ),
    (
        "No query is more clever than the user expects, which is "
        "a feature."
    ): (
        "**没有一个查询比用户预期的更聪明 —— 这正是一个 feature 。**"
    ),

    # ---- Where tiny search fails ----
    (
        "Chapter 2 built the vocabulary — TF-IDF, BM25, hybrid "
        "retrieval, re-ranking — for a reason: *that* is the "
        "retrieval surface a serious RAG pipeline hands to an "
        "LLM. The search engine in this chapter is its much "
        "humbler cousin, a few kilobytes of Go that a human at a "
        "search box uses directly. It is worth being explicit "
        "about what this engine cannot do, because the "
        "temptation to \"just add a reranker\" to it is exactly "
        "the temptation a team should resist until the problem "
        "actually appears."
    ): (
        "第 2 章把词汇表搭起来是有理由的 —— "
        "TF-IDF、BM25、混合检索、重排序 —— "
        "*那一层* 才是一条**严肃的 RAG 流水线**递给 LLM 的**检索面**。"
        "本章这台搜索引擎是**它非常谦卑的表亲**："
        "几千字节的 Go 代码，"
        "直接给坐在搜索框前的**人**用的。"
        "**值得明确说一句**："
        "这台引擎**做不了什么** —— "
        "因为**“那就给它加个 reranker”**这种诱惑，"
        "**恰恰是一个团队应该顶住的诱惑**，"
        "**直到问题真的冒出来之前都不要动**。"
    ),
    (
        "Four query classes defeat the prefix-match index in "
        "predictable ways. Each has a cheap workaround and an "
        "expensive one; almost every team reaches for the "
        "expensive one first."
    ): (
        "有**四类查询**会以**可预见的方式**把前缀匹配索引干翻。"
        "每一类都**配一个便宜解和一个昂贵解**；"
        "**几乎所有团队一上来都先去抓昂贵解**。"
    ),
    (
        "**Identifier-literal queries that paraphrase.** A user "
        "searches for `\"rate limit ingest\"` when the symbol in "
        "the code is `ingestRateLimit`. The tokeniser split the "
        "identifier at case boundaries in the postings list, so "
        "`rate`, `limit`, and `ingest` all land as separate "
        "terms — but the user's query tokens also land as the "
        "same three terms, so this case actually works. The case "
        "that *does* fail is the inverse: the user searches for "
        "the paraphrase `\"throttle incoming traffic\"`, which "
        "shares zero tokens with either the identifier or the "
        "prose that describes it. This is the classic "
        "vocabulary-mismatch failure Chapter 2 names; the cheap "
        "fix is an aggressive tag set on the page itself (the "
        "frontmatter `tags:` field is already in the postings "
        "list), the expensive fix is dense retrieval (Chapter "
        "8). A small team should almost always try the cheap fix "
        "first."
    ): (
        "**“换了说法”的标识符字面量查询。** "
        "代码里的符号是 `ingestRateLimit` ，"
        "用户搜的却是 `\"rate limit ingest\"` 。"
        "分词器在 postings list 里按大小写边界把标识符切开，"
        "所以 `rate` 、 `limit` 、 `ingest` 作为**三个独立 term** 存进去 —— "
        "**但用户的查询 token 恰好也是这三个**，"
        "**所以这一例其实能工作**。"
        "**真正 *会* 失败的是反过来的那一例：**"
        "用户换了一种说法：`\"throttle incoming traffic\"` ，"
        "它**和标识符、和描述它的那段文稿都零 token 重合**。"
        "**这正是第 2 章给出的经典“词汇不匹配”失败。** "
        "**便宜解**是**在页面本身**上打一套**进攻性的 tag** "
        "（ frontmatter 里的 `tags:` 字段本来就已经在 postings list 里了）；"
        "**昂贵解**是稠密检索（第 8 章）。"
        "**一个小团队几乎永远应该先试便宜解。**"
    ),
    (
        "**CJK queries on a tree with no segmentation.** The "
        "tokeniser uses `unicode.IsLetter` to split on anything "
        "that is not a letter or digit — which in Chinese or "
        "Japanese means *every character is a letter, so nothing "
        "splits*. A page containing `配置文件路径` and a query "
        "`配置文件` match only if the page's *full sequence* "
        "begins with the query, which it usually does not. The "
        "honest fix is a segmenter: `go-jieba` for Chinese, "
        "`kagome` for Japanese, both a `go get` away. The "
        "dishonest fix is to declare CJK support out of scope; "
        "teams that do this regret it when the first non-English "
        "user arrives. The hook is already there — the "
        "`tokenize` function is the only place that turns body "
        "text into terms, so swapping it for a language-aware "
        "tokeniser is a localised change."
    ): (
        "**在一棵“没做分词”的树上做 CJK 查询。** "
        "分词器用 `unicode.IsLetter` "
        "**只**在“不是字母也不是数字”的字符上切 —— "
        "**在中文或日文里，每一个字符都 *是* 字母**，"
        "**所以一个都不切**。"
        "一页里含 `配置文件路径` ，"
        "查询是 `配置文件` —— "
        "**只有当这一页的 *完整序列* 以这个查询开头时，才匹得上**，"
        "而**通常不会**。"
        "**诚实的修法**是一个分词器："
        "中文用 `go-jieba` ，"
        "日文用 `kagome` —— **一个 `go get` 就能拿到**。"
        "**不诚实的修法**是宣布“CJK 支持不在我们范围里”；"
        "**这样做的团队**"
        "在**第一个非英文用户到来时会后悔**。"
        "**钩子已经在那里了** —— "
        "**`tokenize` 函数是整个系统里唯一把正文转成 term 的地方**，"
        "**把它换成一个懂语言的分词器，就是一次局部改动。**"
    ),
    (
        "**Typo tolerance.** A search for `recieve` returns "
        "nothing, because the postings list only contains "
        "`receive`. Stemming would not fix this (both words stem "
        "differently); edit distance would. The library answer "
        "is `fuzzy` matching at query time, typically with a "
        "Damerau-Levenshtein distance of 1 or 2 on terms above "
        "some minimum length. The in-memory implementation can "
        "add this in a dozen lines of Go for the 10k-page scale, "
        "but it does so at a quadratic cost (every query term is "
        "compared to every postings-list term) that matters "
        "above ~100k terms. Meilisearch's typo tolerance is "
        "excellent and its operational cost is a single binary; "
        "at that scale it is the right move."
    ): (
        "**容错拼写。** "
        "用户搜 `recieve` —— "
        "**一条结果都没有**，"
        "因为 postings list 里只有 `receive` 。"
        "**词干提取修不好这个问题**（两者的词干本来就不同）；"
        "**编辑距离可以**。"
        "**标准答案**是：在查询时做 `fuzzy` 匹配，"
        "一般用 Damerau-Levenshtein 距离 1 或 2，"
        "并设一个最小 term 长度门槛。"
        "**内存实现**用十几行 Go 就能加上 —— "
        "**在 1 万页这个量级上**没问题，"
        "**但代价是平方**（每个查询 term 都要和每个 postings-list term 比一次），"
        "**到 10 万 term 以上就吃不消了**。"
        "**Meilisearch 的容错拼写非常好**，"
        "**运维代价就一个 binary**；"
        "**到那个规模，它就是对的选择**。"
    ),
    (
        "**Ranking by relevance, not cardinality.** The `Search` "
        "function scores by \"how many query terms hit this "
        "document\". A sufficiently long page that *mentions* "
        "every term beats a focused page that *is about* the "
        "term. This is exactly the pathology BM25 was designed "
        "to fix via its length-normalisation term $b$ (Chapter "
        "2): long documents should not dominate just because "
        "they are long. The cheap fix in the in-memory "
        "implementation is field weighting — boost title matches "
        "over body matches, as Chapter 2 also names — which the "
        "`searchTerms` map could implement by keeping a per-term "
        "origin (\"was this token in the title or the body?\") "
        "and adding a small coefficient at query time. The "
        "in-repo implementation does not do this today; the "
        "interface supports it without a migration. Chapter 2's "
        "*Advanced RAG* section shows why field weighting "
        "matters more than most tuning knobs below it."
    ): (
        "**按相关性排序，而不是按基数。** "
        "`Search` 函数按“**这个文档里命中了几个查询 term**”打分。"
        "一页**足够长**、 *顺嘴提了每一个 term* 的文档，"
        "会**压过一页紧扣主题、真正在讲那个 term 的文档**。"
        "**这正是** BM25 **通过它的长度归一化项 $b$ 被设计来修掉的那种病态**"
        "（第 2 章）：**一个文档不应该只因为长就一路压过其他文档**。"
        "**内存实现里的便宜修法**是**字段加权** —— "
        "**标题里的命中**比**正文里的命中**权重更高，"
        "第 2 章也点过名 —— "
        "在 `searchTerms` 映射里实现它的办法是："
        "**为每个 term 记一下出处**"
        "（“这个 token 当时在 title 里，还是在 body 里？”），"
        "**在查询时乘一个小系数**。"
        "**当前的仓库实现还没做这一步；**"
        "**接口层面本身已经支持，不需要迁移**。"
        "第 2 章的 *Advanced RAG* 那一节"
        "讲过：**为什么字段加权比它底下的绝大多数调参旋钮都更重要**。"
    ),
    (
        "The common thread is that the right moment to reach for "
        "Chapter 2's heavier machinery is *when a specific query "
        "class stops working*, not before. A software KB whose "
        "live search is a prefix-match index and whose "
        "agent-facing retrieval is a BM25+dense+rerank pipeline "
        "is not a contradiction — it is the healthy design. "
        "Different consumers have different budgets and "
        "different expectations; serving both from the same "
        "storage layer (files on disk) is the architectural win "
        "that makes the disagreement cheap."
    ): (
        "**这几类的共同线索是：**"
        "**抬手去抓第 2 章那套更重的机器的时机，**"
        "*是当一类具体的查询开始失败时* ，**不是在此之前**。"
        "**一个**实时搜索是前缀匹配索引、"
        "**而**面向 agent 的检索是 BM25+稠密+重排序流水线的软件知识库，"
        "**不是自相矛盾** —— "
        "**那是健康的设计**。"
        "**不同消费者有不同预算、有不同期望；**"
        "**用同一层存储（磁盘上的文件）把两边都伺候了，**"
        "**这本身就是那个让“意见分歧”变便宜的架构层面胜利。**"
    ),

    # ---- Common mistakes ----
    (
        "Beyond the query-class failures, four scaling and "
        "wiring mistakes are frequent enough to warrant their "
        "own list:"
    ): (
        "**除了“按查询类别”的失败形态，**"
        "**还有四个**在扩容和接线环节里**频繁出现的错误**，"
        "值得单独列一下："
    ),
    (
        "**Trying to keep an incremental index correct.** The "
        "prose layer uses whole-map rebuild on write for a "
        "reason: incremental update is the source of almost "
        "every \"search is stale\" bug in database-backed wikis. "
        "At the scale this chapter targets, the whole rebuild is "
        "milliseconds; giving that up to chase constant-factor "
        "performance is the classic over-engineering failure."
    ): (
        "**非要把增量索引维护对。** "
        "文稿层**写入时整表重建**是有理由的：**增量更新**"
        "是**基于数据库的 wiki 里几乎所有“搜索结果陈旧”类 bug 的源头**。"
        "**在本章瞄准的规模上**，"
        "**整表重建也就是毫秒级**；"
        "**为了追求常数因子的性能把它放弃掉**，"
        "**是经典的过度工程失败**。"
    ),
    (
        "**Bolting on a second search system \"for the "
        "production site\".** A team adds Elasticsearch "
        "\"because the in-memory one is not serious enough\" and "
        "ends up with two search layers that sometimes disagree "
        "— readers on the live server see one result set, "
        "readers on the published static site see another. The "
        "staircase in Competing approaches is a *sequence*, not "
        "a choice: pick the lowest step that currently fails, "
        "migrate the whole KB to it, and keep a single "
        "`Search(...)` interface."
    ): (
        "**为了“生产站”再挂一套搜索系统上去。** "
        "一个团队加上了 Elasticsearch，"
        "**理由**是“内存那套不够严肃”，"
        "**结果**是**两套搜索层有时候意见不一致** —— "
        "实时服务器上的读者看到一套结果，"
        "**静态站上的读者看到另一套**。"
        "**“其他做法”那一节里的台阶是一个 *序列* ，不是一次选择：**"
        "**挑当前开始失败的最低一档，**"
        "**把整个知识库都迁到那一档上，**"
        "**继续只保留一个 `Search(...)` 接口**。"
    ),
    (
        "**Indexing content the trust layer disavows.** A naïve "
        "`LoadAndIndex` indexes every file under `content/`, "
        "including pages whose `verification_status` is "
        "`contradicted` or `superseded`. Those pages then "
        "surface in search results with no visible signal that "
        "they are stale. The right move is to index them but "
        "filter them out of the default query (and surface them "
        "via an explicit \"include superseded\" toggle for "
        "archaeologists). Chapter 5's trust fields are retrieval "
        "metadata, not just display metadata."
    ): (
        "**把信任层已经否认掉的内容也索引进来。** "
        "一个天真的 `LoadAndIndex` 会把 `content/` 下的每一个文件都索引进来，"
        "**包括那些 `verification_status` 是 `contradicted` 或 `superseded` 的页面**。"
        "这些页面随后**就这么出现在搜索结果里**，"
        "**没有任何可见的“它已经过时”的信号**。"
        "**正确的做法**是**照索引**，"
        "**但把它们从默认查询里过滤掉**"
        "（再提供一个显式的“包含 superseded”开关给考古爱好者）。"
        "**第 5 章里那些信任字段是检索元数据**，"
        "**不仅仅是显示元数据**。"
    ),
    (
        "**Treating the Sphinx in-page search as the "
        "\"production\" search.** Sphinx's client-side search is "
        "excellent for a static mirror; it is a disaster if an "
        "organisation relies on it exclusively. It does not see "
        "frontmatter, it cannot filter by `verification_status`, "
        "and its ranking is driven by Porter stemming "
        "{cite}`porter1980stemming` — which is a good signal on "
        "English prose and a *noisy* signal on identifier-literal "
        "queries. Keep the live server's search authoritative "
        "for authenticated readers; let the static build's search "
        "exist for the public or offline case, and for those "
        "readers only."
    ): (
        "**把 Sphinx 的页内搜索当成“生产级”搜索。** "
        "**Sphinx 的客户端搜索**作为**一份静态镜像**的搜索**非常好用**；"
        "**如果一个组织把它当成唯一的搜索，那就是灾难。**"
        "**它看不到 frontmatter ，**"
        "**它不能按 `verification_status` 过滤**，"
        "**它的排序由 Porter 词干提取驱动** "
        "{cite}`porter1980stemming` —— "
        "**这个信号在英文文本上还不错，**"
        "**在“标识符字面量”类查询上就是 *噪声* 信号**。"
        "**对已登录的读者来说，让实时服务器的搜索保持权威；**"
        "**让静态构建的搜索**"
        "**存在是为了“对公”或者“离线”场景，"
        "而且只为那一批读者存在**。"
    ),

    # ---- Competing approaches table ----
    "System": "系统",
    "Index size for 10k pages": "1 万页的索引体积",
    "Setup cost": "搭建成本",
    "Fit for a file-based KB": "与文件型知识库的契合度",
    "In-memory prefix index (this chapter)": "内存前缀索引（本章）",
    "~20 MB": "~20 MB",
    "0 (built-in)": "0（内置）",
    "Great below 10k pages.": "1 万页以下很好用。",
    "Bleve {cite}`bleve`": "Bleve {cite}`bleve`",
    "~100 MB on disk": "磁盘上 ~100 MB",
    "`go get` + a few lines": "`go get` + 几行代码",
    "Natural scale-up; still embedded, no server.": (
        "**自然的扩容路径**；仍然**内嵌**，**无需服务端进程**。"
    ),
    "Meilisearch {cite}`meilisearch`": "Meilisearch {cite}`meilisearch`",
    "Separate process": "独立进程",
    "Docker + an API key": "Docker + 一个 API key",
    "Excellent ranking, typo tolerance; operational cost.": (
        "排序好，容错拼写好；**有运维成本**。"
    ),
    "Algolia DocSearch {cite}`algolia_docsearch`": (
        "Algolia DocSearch {cite}`algolia_docsearch`"
    ),
    "Crawled, hosted": "**爬、托管**",
    "Signup + crawl config": "注册 + 爬虫配置",
    "Free for open source; locks you in for private KBs.": (
        "开源项目免费；**私有知识库会被锁定**。"
    ),
    "Elasticsearch / OpenSearch": "Elasticsearch / OpenSearch",
    "JVM cluster": "JVM 集群",
    "High": "**高**",
    "Overkill for a KB at this scale.": (
        "**对本章规模的知识库是 over-engineer 的**。"
    ),
    "Sphinx in-page search only": "**只用** Sphinx 页内搜索",
    "Build-time": "构建时",
    "0": "0",
    "Good for static docs; no live updates.": (
        "对**静态文档**来说够用；**没有实时更新**。"
    ),
    "The book's recommendation is the staircase:": (
        "**本书的建议是这条台阶：**"
    ),
    "Start with the in-memory index. It is good enough for any team KB.": (
        "**从内存索引开始。** "
        "**对任何一个团队知识库来说都够用。**"
    ),
    "Add Sphinx's static search in parallel for the published site.": (
        "**并行**给已发布的站点加上 Sphinx 的静态搜索。"
    ),
    (
        "Swap Bleve in behind the `Search` interface if the "
        "in-memory version becomes CPU-bound."
    ): (
        "**当内存版本变成 CPU-bound 时**，"
        "在 `Search` 接口背后**换上 Bleve**。"
    ),
    (
        "Only promote to Meilisearch or Elasticsearch when you "
        "have an explicit product reason (typo tolerance, "
        "fielded boosts, multi-tenant ranking)."
    ): (
        "**只在你有显式的产品理由时**"
        "（容错拼写、字段加权、多租户排序）"
        "**才升级到 Meilisearch 或 Elasticsearch**。"
    ),
    (
        "Each step up preserves the `Search(query, type) → "
        "SearchResult` contract, so client code does not change."
    ): (
        "**每一次上台阶都保留 "
        "`Search(query, type) → SearchResult` 这份契约 —— "
        "客户端代码不用改。**"
    ),

    # ---- Conclusion ----
    (
        "A file-based wiki earns its \"as simple as possible, "
        "but no simpler\" badge when the search layer is also "
        "simple enough to audit. An in-memory postings map + a "
        "ten-line tokeniser is a complete, honest search engine "
        "for a small-to-medium software KB. Sphinx handles the "
        "static view, with its own stemmer-based search for the "
        "published site. Every page is indexed consistently "
        "because every write path ends in the same `AddPage` "
        "call, inside the same mutex."
    ): (
        "**一个基于文件的 wiki 要拿到“尽可能简单、"
        "但别更简单”那枚徽章**，"
        "**前提是搜索层也简单到能被审计**。"
        "**一张内存 postings 映射表 + 一个十行的分词器，**"
        "**对一个中小规模的软件知识库来说，**"
        "**就是一台完整、诚实的搜索引擎**。"
        "**Sphinx 负责静态视图那一边**，"
        "**带着它自己那套基于词干提取的搜索**。"
        "**每一页之所以都被一致地索引，**"
        "**是因为每一条写入路径都在同一个 mutex 里"
        "调同一个 `AddPage` 结束**。"
    ),
    (
        "Part II ends here. The prose layer has all its moving "
        "parts: files (Chapter 4), frontmatter as provenance "
        "(Chapter 5), the pipeline (Chapter 6), and publish + "
        "search (this chapter). Part III turns from prose to "
        "code — embeddings, code graphs, and the hybrid "
        "retrieval that makes a software KB different from a "
        "document warehouse."
    ): (
        "**第二部分到此收尾**。"
        "文稿层**所有会动的零件**都齐了："
        "**文件**（第 4 章）、"
        "**作为来源的 frontmatter**（第 5 章）、"
        "**流水线**（第 6 章）、"
        "以及**发布 + 搜索**（本章）。"
        "**第三部分**要**从文稿转向代码** —— "
        "**embedding、代码图谱、**"
        "**以及让一个软件知识库**"
        "**不同于一座文档仓库的那种混合检索**。"
    ),

    # ---- Hook opening ----
    (
        "A new engineer joined last week. On Thursday she "
        "types `recieve` into the wiki's search box and gets "
        "zero results. On Friday she types `配置文件` and gets "
        "zero results. On Monday she types `rate limit` and "
        "the first page returned is a three-year-old blog "
        "post, while the actual runbook — whose title is "
        "literally *\"Rate limit configuration\"* — is on page "
        "four. On Tuesday she opens the JIRA ticket \"the "
        "wiki's search is broken\" and assigns it to you."
    ): (
        "上周**新来了一位工程师**。"
        "周四，她往 wiki 的搜索框里输了 `recieve` —— "
        "**零条结果**。"
        "周五，她输的是 `配置文件` —— **零条结果**。"
        "周一，她输的是 `rate limit` —— "
        "**排第一的**是**一篇三年前的博客帖**，"
        "而真正的那份 runbook —— "
        "**标题就叫** *“Rate limit configuration”* —— "
        "**在第四页**。"
        "到了周二，她**开了一个 JIRA 工单**，"
        "标题是“**wiki 的搜索坏了**”，**指派给你**。"
    ),
    (
        "The wiki's search is not broken. It is a ten-line "
        "tokeniser and a prefix-match loop, and against that "
        "specification it is working perfectly. What is broken "
        "is that a ten-line tokeniser is what this team ships "
        "for the *entire* lifetime of the KB, instead of "
        "treating it as the first step on a staircase whose "
        "later steps are easy. This chapter is about both "
        "pieces: the tiny engine that earns its place at the "
        "bottom of the staircase, and the honest map of which "
        "step to climb to when which query class starts "
        "failing."
    ): (
        "wiki 的搜索**其实并没有坏**。"
        "它是**一个十行的 tokenizer**"
        "**加一段前缀匹配循环** —— "
        "**对着它那份规格**，**它工作得好极了**。"
        "**坏的是这件事**："
        "**这个团队把“十行 tokenizer”**"
        "**当成了知识库 *全生命周期* 里交付的东西**，"
        "**而没有把它当成一段阶梯的第一级** —— "
        "**一段后面几级都很容易上的阶梯**。"
        "这一章**两件事都讲**："
        "**那个小小的、凭实力占住阶梯最底层的引擎**，"
        "以及**一张诚实的地图** —— "
        "**当什么类型的查询开始失败时，**"
        "**应该往上爬到阶梯的哪一级**。"
    ),
}
