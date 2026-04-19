"""Chinese translations for book/part2-prose-layer/ch05-frontmatter-provenance-trust.md.

See book/_tools/translations/ch02-ir-rag-primer.zh.py for the full
style guide. Chapter-specific notes:

- "frontmatter" / "footer" kept in English (paired concepts).
- "provenance" -> "来源" (when referring to lineage) /
  "来源记录"; "the provenance problem" -> "来源问题".
- YAML field names (created_by, verification_status, etc.)
  kept verbatim.
- Enum values (`supported`, `unreviewed`, `approved`, `pending`,
  `human`, `ai`, `ai+human`, `tutorial`, `how-to`, `reference`,
  `explanation`) kept in English because schemas match them.
- Pandoc, MyST, Notion, Confluence, W3C PROV, PROV-O, RDF, OWL,
  OpenAPI, API, SHA, LLM, CI, PR, Git, URL, Wayback Machine,
  ORM, Markdown, YAML, JSON, Vim kept in English.
- "PKB-metadata" literal token kept verbatim.
- Alice kept as proper noun.
- CommonMark emphasis rule — ASCII whitespace around `*...*` when
  flanked by CJK characters.
"""

PO_PATH = "part2-prose-layer/ch05-frontmatter-provenance-trust.po"

TRANSLATIONS: dict[str, str] = {
    # ---- Title + headings + mindmap intro ----
    "Chapter 5 — Frontmatter as a Provenance Record": (
        "第 5 章 —— 把 frontmatter 当作一份来源记录"
    ),
    (
        "This chapter at a glance — the four questions a trust "
        "layer must answer, the two-block split between lineage "
        "(frontmatter) and review state (footer), the cultural "
        "commitment that `AI → unreviewed`, and the failure "
        "patterns that collapse even well-schemed provenance into "
        "decoration:"
    ): (
        "本章一页速览 —— "
        "一个**信任层**必须回答的四个问题，"
        "把“来源”（frontmatter）和“评审状态”（footer）拆成两块的那次选择，"
        "“**AI → unreviewed**”这条文化承诺，"
        "以及那些即使 schema 设计得再好、"
        "也会让来源记录一路退化成装饰的失败形态："
    ),
    "Why": "为什么",
    "What": "是什么",
    "How": "怎么做",
    "Example": "示例",
    "Conclusion": "结论",
    "References": "参考文献",
    "Competing approaches": "其他做法",
    "Parsing and serialising": "解析与序列化",
    "Inferring frontmatter for foreign files": "为外来文件推断 frontmatter",
    "The trust default for AI content": "AI 内容的信任默认值",
    "Enforcing immutability on update": "在更新路径上强制不可变",
    "Frontmatter versus footer: two blocks, not one": (
        "frontmatter 与 footer：两块，不是一块"
    ),

    # ---- Why ----
    (
        "A KB is only as useful as it is trusted. And \"trust\" "
        "in a software knowledge base is not a feeling — it is a "
        "set of concrete questions the KB must answer, every "
        "time, without a human:"
    ): (
        "一个知识库有多好用，取决于它有多被信任。"
        "而一个软件知识库里的“信任”并不是感觉 —— "
        "它是一串**具体的问题**，"
        "知识库每一次都得在**不需要有人在场**的情况下把它们答出来："
    ),
    "**Who wrote this?** A human teammate, or an LLM?": (
        "**是谁写的？** 一个人类同事，还是一个 LLM？"
    ),
    "**When was it written, and against which version of the software?**": (
        "**什么时候写的？对着哪个版本的软件写的？**"
    ),
    "**Has anybody verified it is still true?**": (
        "**有人验证过这东西现在还是真的吗？**"
    ),
    "**If it came from somewhere else, where?**": (
        "**如果它是从别的地方搬过来的，从哪儿搬的？**"
    ),
    (
        "A page with no answers to these questions is noise. A "
        "page with clear answers can be reviewed, ranked, "
        "retired, or escalated automatically. Buneman et al. "
        "call this the *provenance problem* — \"the description "
        "of the origins of a piece of data and the process by "
        "which it arrived in a database\" "
        "{cite}`buneman2001provenance` — and the W3C PROV data "
        "model generalises it to any information artefact "
        "{cite}`w3c_prov`. This chapter shows how the "
        "prose-layer reference implementation turns those "
        "abstract questions into a handful of required YAML "
        "fields (plus, as §\"Frontmatter versus footer\" will "
        "argue, one HTML-comment footer), and how the code "
        "enforces invariants on them so the trust signal cannot "
        "silently rot."
    ): (
        "一张没有答案的页，是噪声。"
        "一张有清晰答案的页，可以被评审、被排序、被下线、被自动升级。"
        "Buneman 等人把这件事叫作 *来源问题* —— "
        "“对一份数据的**出身**、以及它**到达数据库的过程**的描述”"
        "{cite}`buneman2001provenance` —— "
        "W3C 的 PROV 数据模型又把它推广到"
        "任何信息制品上 {cite}`w3c_prov` 。"
        "这一章要展示的是：文稿层参考实现"
        "怎么把这些抽象问题变成一小组必填的 YAML 字段"
        "（再加上 §“frontmatter 与 footer”会论证的那一段"
        "HTML-comment footer），"
        "以及代码怎么在它们上面强制不变式，"
        "好让信任信号**不会静默腐烂**。"
    ),

    # ---- What ----
    (
        "Every Markdown page in `content/` begins with a YAML "
        "frontmatter block delimited by `---` fences. The "
        "contract for that block is declared explicitly in the "
        "repo, at `wiki-template/metadata/SCHEMA.md`, and it is "
        "the only piece of configuration in the system that is "
        "*not* Go code:"
    ): (
        "`content/` 底下的每一份 Markdown 页面"
        "都以一段 YAML frontmatter 打头，"
        "由 `---` 围栏包起来。"
        "这一段的**契约**在仓库里被显式声明出来："
        "`wiki-template/metadata/SCHEMA.md` ，"
        "而这是整个系统里**唯一** *不是* Go 代码的配置："
    ),
    "The frontmatter contract, verbatim from `SCHEMA.md`.": (
        "frontmatter 契约，原样抄自 `SCHEMA.md` 。"
    ),
    (
        "\n```yaml\n---\ntitle: \"Page Title\"           # "
        "Required\nslug: page-title               # "
        "Auto-generated from title\ntags: [tag1, tag2]             "
        "# Optional\nsummary: \"Brief description\"   # "
        "Recommended\ncreated: 2026-01-01T00:00:00Z # "
        "Auto-set\ncreated_by: alice              # Immutable "
        "after creation\nupdated: 2026-01-01T00:00:00Z # "
        "Auto-set\nupdated_by: alice              # Updated on "
        "each edit\nstatus: published              # draft | "
        "published | archived\ndoc_type: reference            # "
        "tutorial | how-to | reference | "
        "explanation\nverification_status: supported # supported "
        "| unreviewed | uncertain | contradicted | "
        "superseded\nsource:                        # Optional, "
        "immutable\n  type: original               # original | "
        "git_repo | doc | url\n  uri: \"\"\n  path: \"\"\n  ref: "
        "\"\"\n---\n```\n\n"
    ): (
        "\n```yaml\n---\ntitle: \"Page Title\"           # "
        "必填\nslug: page-title               # "
        "从 title 自动生成\ntags: [tag1, tag2]             "
        "# 可选\nsummary: \"Brief description\"   # "
        "建议填\ncreated: 2026-01-01T00:00:00Z # "
        "自动设置\ncreated_by: alice              # 创建后不可变\n"
        "updated: 2026-01-01T00:00:00Z # 自动设置\n"
        "updated_by: alice              # 每次编辑都更新\n"
        "status: published              # draft | published | archived\n"
        "doc_type: reference            # tutorial | how-to | reference | explanation\n"
        "verification_status: supported # supported | unreviewed | uncertain | contradicted | superseded\n"
        "source:                        # 可选，不可变\n"
        "  type: original               # original | git_repo | doc | url\n"
        "  uri: \"\"\n  path: \"\"\n  ref: "
        "\"\"\n---\n```\n\n"
    ),
    "Three fields in particular carry the trust signal:": (
        "其中有三个字段**扛着**整份信任信号："
    ),
    (
        "`created_by` — *who* produced the page (a username, or "
        "the literal string `\"ai\"`). **Immutable** after "
        "creation."
    ): (
        "`created_by` —— *谁* 产出的这一页"
        "（一个用户名，或者字面字符串 `\"ai\"` ）。"
        "**创建后不可变。**"
    ),
    (
        "`verification_status` — *how trustworthy* the content "
        "currently is (`supported` / `unreviewed` / `uncertain` "
        "/ `contradicted` / `superseded`)."
    ): (
        "`verification_status` —— 当前这份内容 *有多可信* "
        "（ `supported` / `unreviewed` / `uncertain` / "
        "`contradicted` / `superseded` ）。"
    ),
    (
        "`source` — *where it came from*, if not written "
        "directly in the wiki (`type`, `uri`, `path`, `ref`). "
        "Also **immutable**."
    ): (
        "`source` —— 如果不是直接在 wiki 里写的， *它从哪儿来* "
        "（ `type` 、 `uri` 、 `path` 、 `ref` ）。"
        "**同样不可变。**"
    ),
    (
        "The remainder — `created`, `updated`, `commit`, `tags`, "
        "`summary`, `doc_type`, `status` — support those three "
        "by answering \"when\", \"at which version\", and "
        "\"about what\". The full YAML-1.2 specification "
        "{cite}`yaml_spec` governs the serialisation, and the "
        "frontmatter-block convention itself was popularised by "
        "Pandoc {cite}`pandoc`."
    ): (
        "其他字段 —— `created` 、 `updated` 、 `commit` 、 "
        "`tags` 、 `summary` 、 `doc_type` 、 `status` —— "
        "用来支撑上面那三个，"
        "回答“**什么时候**”、“**对着哪个版本**”、"
        "“**关于什么**”这类问题。"
        "序列化这块由完整的 YAML-1.2 规范 {cite}`yaml_spec` 负责；"
        "而 frontmatter 块这个约定本身，"
        "是被 Pandoc {cite}`pandoc` 推广开的。"
    ),
    (
        "Why YAML and not, say, a sidecar JSON file or a "
        "database row? Three reasons:"
    ): (
        "为什么是 YAML，"
        "不是旁挂一份 JSON、也不是一行数据库记录？"
        "三条理由："
    ),
    (
        "**Co-location.** The metadata travels with the content "
        "in a single file. A reader who `cat`s the page sees the "
        "provenance without opening a separate tool."
    ): (
        "****共处一地。**** "
        "元数据和内容**在同一份文件里**同行。"
        "一个读者 `cat` 一下页面，"
        "就能看到来源，"
        "不用另外打开任何工具。"
    ),
    (
        "**Diffability.** A metadata change is a line diff in "
        "Git, reviewable alongside a body change. Sidecar files "
        "split the review across two filenames; database rows "
        "across two systems."
    ): (
        "**可 diff。** "
        "元数据改动就是 Git 里的一行 diff ，"
        "可以和正文改动**并排**一起评审。"
        "旁挂文件会把评审劈到两个文件名；"
        "数据库行会把评审劈到两套系统。"
    ),
    (
        "**Human-writable.** The first author types the YAML by "
        "hand when they create a page. Machines read and patch "
        "it later, but the schema is still human-obvious, which "
        "keeps the trust contract from disappearing behind an "
        "ORM."
    ): (
        "**人可手写。** "
        "第一个作者在新建页面时，是**手敲** YAML 的。"
        "后面机器当然要去读、去补丁，"
        "但 schema 本身对人仍然是一眼可见的 —— "
        "这就让信任契约不会**被埋在某个 ORM 后面消失**。"
    ),

    # ---- How: parsing / serialising ----
    (
        "The code lives entirely in `frontmatter.go`, and it is "
        "short enough to read in one sitting. Parsing splits the "
        "file on the `---` delimiter and unmarshals the YAML "
        "block:"
    ): (
        "代码全都在 `frontmatter.go` 里，"
        "短到可以**一坐读完**。"
        "解析逻辑就是在 `---` 分隔符上把文件切开，"
        "再把 YAML 块反序列化："
    ),
    "`ParseFrontmatter` — `---` is the fence, YAML does the rest.": (
        "`ParseFrontmatter` —— `---` 是围栏，其余交给 YAML。"
    ),
    (
        "\t\"os\"\n\t\"path/filepath\"\n\t\"strings\"\n\t\"time\"\n\n\t\"gopkg.in/yaml.v3\"\n)\n\nconst frontmatterDelimiter = \"---\"\n\n// ParseFrontmatter extracts YAML frontmatter and body from Markdown content.\n// Returns the Frontmatter struct and the body (everything after the closing ---).\nfunc ParseFrontmatter(content string) (*Frontmatter, string, error) {\n\ttrimmed := strings.TrimSpace(content)\n\tif !strings.HasPrefix(trimmed, frontmatterDelimiter) {\n\t\treturn nil, content, nil\n\t}\n\n\trest := trimmed[len(frontmatterDelimiter):]\n\tidx := strings.Index(rest, \"\\n\"+frontmatterDelimiter)\n\tif idx < 0 {\n\t\treturn nil, content, nil\n\t}\n\n\tyamlBlock := rest[:idx]\n\tbody := rest[idx+len(\"\\n\"+frontmatterDelimiter):]\n\tif strings.HasPrefix(body, \"\\n\") {\n"
    ): (
        "\t\"os\"\n\t\"path/filepath\"\n\t\"strings\"\n\t\"time\"\n\n\t\"gopkg.in/yaml.v3\"\n)\n\nconst frontmatterDelimiter = \"---\"\n\n// ParseFrontmatter extracts YAML frontmatter and body from Markdown content.\n// Returns the Frontmatter struct and the body (everything after the closing ---).\nfunc ParseFrontmatter(content string) (*Frontmatter, string, error) {\n\ttrimmed := strings.TrimSpace(content)\n\tif !strings.HasPrefix(trimmed, frontmatterDelimiter) {\n\t\treturn nil, content, nil\n\t}\n\n\trest := trimmed[len(frontmatterDelimiter):]\n\tidx := strings.Index(rest, \"\\n\"+frontmatterDelimiter)\n\tif idx < 0 {\n\t\treturn nil, content, nil\n\t}\n\n\tyamlBlock := rest[:idx]\n\tbody := rest[idx+len(\"\\n\"+frontmatterDelimiter):]\n\tif strings.HasPrefix(body, \"\\n\") {\n"
    ),
    (
        "Serialisation is the inverse, building the YAML block "
        "back around the body:"
    ): (
        "序列化就是反向操作：把 YAML 块围着正文重新拼回来："
    ),
    "`SerializeFrontmatter` — round-trip with the standard YAML marshaller.": (
        "`SerializeFrontmatter` —— 用标准 YAML marshaller 做 round-trip。"
    ),
    (
        "\t}\n\n\tvar fm Frontmatter\n\tif err := yaml.Unmarshal([]byte(yamlBlock), &fm); err != nil {\n\t\treturn nil, \"\", fmt.Errorf(\"invalid frontmatter YAML: %w\", err)\n\t}\n\n\treturn &fm, body, nil\n}\n\n// SerializeFrontmatter produces the YAML frontmatter block + body Markdown.\nfunc SerializeFrontmatter(fm *Frontmatter, body string) (string, error) {\n\tyamlBytes, err := yaml.Marshal(fm)\n\tif err != nil {\n"
    ): (
        "\t}\n\n\tvar fm Frontmatter\n\tif err := yaml.Unmarshal([]byte(yamlBlock), &fm); err != nil {\n\t\treturn nil, \"\", fmt.Errorf(\"invalid frontmatter YAML: %w\", err)\n\t}\n\n\treturn &fm, body, nil\n}\n\n// SerializeFrontmatter produces the YAML frontmatter block + body Markdown.\nfunc SerializeFrontmatter(fm *Frontmatter, body string) (string, error) {\n\tyamlBytes, err := yaml.Marshal(fm)\n\tif err != nil {\n"
    ),
    (
        "The symmetry matters. The same bytes that a human wrote "
        "can be read by the server, patched, and written back, "
        "without any lossy projection through a secondary "
        "schema. This is what makes \"edit with `vim` and commit "
        "with `git`\" a supported workflow rather than an escape "
        "hatch."
    ): (
        "**对称性**很重要。"
        "一个人写出来的那段字节，"
        "能被服务器读进来、打补丁、再写回去，"
        "中间**不会**经过任何次级 schema 的有损投影。"
        "这就是为什么“用 `vim` 编辑、用 `git` 提交”"
        "是一个**被正式支持的工作流**，"
        "而不是一个紧急逃生门。"
    ),

    # ---- How: inferring ----
    (
        "Not every Markdown file that lands in `content/` was "
        "created by the wiki. Imports from `raw/`, files dropped "
        "in by `cp`, files synced from another repo — all must "
        "become first-class pages. `InferFrontmatter` "
        "synthesises a minimal, plausible frontmatter from the "
        "filename and the file's mtime:"
    ): (
        "并不是所有掉进 `content/` 里的 Markdown 文件都是 wiki 自己创建的。"
        "从 `raw/` 导入的、"
        "用 `cp` 扔进来的、"
        "从另一个仓库同步进来的 —— "
        "这些**全都要**变成一等公民页面。"
        "`InferFrontmatter` 从文件名和 mtime 里"
        "合成一份最小但看起来合理的 frontmatter："
    ),
    "`InferFrontmatter` — a sane default for files that arrived without a header.": (
        "`InferFrontmatter` —— 给那些“光着身子”到的文件一份靠谱默认值。"
    ),
    (
        "\t}\n\n\tvar buf bytes.Buffer\n\tbuf.WriteString(frontmatterDelimiter + \"\\n\")\n\tbuf.Write(yamlBytes)\n\tbuf.WriteString(frontmatterDelimiter + \"\\n\")\n\tbuf.WriteString(body)\n\treturn buf.String(), nil\n}\n\n// InferFrontmatter creates a Frontmatter with sensible defaults for a file\n// that has no frontmatter. Title is derived from filename, timestamps from mtime.\nfunc InferFrontmatter(filePath string) *Frontmatter {\n\tbase := filepath.Base(filePath)\n\tname := strings.TrimSuffix(base, filepath.Ext(base))\n\n\ttitle := strings.ReplaceAll(name, \"-\", \" \")\n\ttitle = strings.ReplaceAll(title, \"_\", \" \")\n\ttitle = strings.Title(title) //nolint:staticcheck\n\n\tslug := GenerateSlug(base)\n\n\tnow := time.Now().UTC()\n\tif info, err := os.Stat(filePath); err == nil {\n\t\tnow = info.ModTime().UTC()\n\t}\n\n\treturn &Frontmatter{\n"
    ): (
        "\t}\n\n\tvar buf bytes.Buffer\n\tbuf.WriteString(frontmatterDelimiter + \"\\n\")\n\tbuf.Write(yamlBytes)\n\tbuf.WriteString(frontmatterDelimiter + \"\\n\")\n\tbuf.WriteString(body)\n\treturn buf.String(), nil\n}\n\n// InferFrontmatter creates a Frontmatter with sensible defaults for a file\n// that has no frontmatter. Title is derived from filename, timestamps from mtime.\nfunc InferFrontmatter(filePath string) *Frontmatter {\n\tbase := filepath.Base(filePath)\n\tname := strings.TrimSuffix(base, filepath.Ext(base))\n\n\ttitle := strings.ReplaceAll(name, \"-\", \" \")\n\ttitle = strings.ReplaceAll(title, \"_\", \" \")\n\ttitle = strings.Title(title) //nolint:staticcheck\n\n\tslug := GenerateSlug(base)\n\n\tnow := time.Now().UTC()\n\tif info, err := os.Stat(filePath); err == nil {\n\t\tnow = info.ModTime().UTC()\n\t}\n\n\treturn &Frontmatter{\n"
    ),
    "Two defaults encode policy:": "有两条默认值里藏着**政策**：",
    (
        "`CreatedBy: \"human\"`. An imported file is *not* "
        "assumed to be AI unless the importer says so. Chapter 6 "
        "will show the pipeline overriding this when it knows "
        "better."
    ): (
        "`CreatedBy: \"human\"` 。"
        "一份导入进来的文件， *默认不是* AI 写的，"
        "除非导入方明确说它是。"
        "第 6 章会讲到流水线在更清楚时是怎么把这个默认值覆盖掉的。"
    ),
    (
        "`VerificationStatus: VerificationSupported`. A file "
        "that already existed in the repo has earned at least "
        "provisional trust; it is not automatically demoted to "
        "`unreviewed`."
    ): (
        "`VerificationStatus: VerificationSupported` 。"
        "一个已经存在于仓库里的文件**至少已经赢得了暂时的信任**；"
        "它不会被自动降级成 `unreviewed` 。"
    ),

    # ---- How: trust default for AI ----
    (
        "The single most consequential line in the whole "
        "frontmatter subsystem is three lines long:"
    ): (
        "整个 frontmatter 子系统里**后果最大**的一块代码，"
        "长度只有三行："
    ),
    "`DefaultVerificationStatus` — one branch, one cultural commitment.": (
        "`DefaultVerificationStatus` —— 一个分支，一条文化承诺。"
    ),
    (
        "\t\tSlug:               slug,\n\t\tCreated:            "
        "now,\n\t\tCreatedBy:          "
        "\"human\",\n\t\tUpdated:            now,\n\t\tStatus:             "
        "PageStatusPublished,\n\t\tDocType:            "
        "DocTypeReference,\n\t\tVerificationStatus: "
        "VerificationSupported,\n\t}\n"
    ): (
        "\t\tSlug:               slug,\n\t\tCreated:            "
        "now,\n\t\tCreatedBy:          "
        "\"human\",\n\t\tUpdated:            now,\n\t\tStatus:             "
        "PageStatusPublished,\n\t\tDocType:            "
        "DocTypeReference,\n\t\tVerificationStatus: "
        "VerificationSupported,\n\t}\n"
    ),
    (
        "If the author is AI, the default verification status is "
        "`unreviewed`. If the author is human, it is "
        "`supported`. This is the policy `SCHEMA.md` declares at "
        "the prose level (\"AI-authored pages default to "
        "`verification_status: unreviewed`\"), made executable. "
        "No human reviewer has to remember to demote an AI page; "
        "the default does it for them."
    ): (
        "如果作者是 AI，默认的验证状态就是 `unreviewed` 。"
        "如果作者是人，就是 `supported` 。"
        "这就是 `SCHEMA.md` 在文稿层宣布的那条政策 "
        "（“AI 写的页面默认 `verification_status: unreviewed`”）"
        "的**可执行形态**。"
        "没有哪个人类评审需要专门记住“要把 AI 页面降级”；"
        "默认值已经替他们做了。"
    ),
    (
        "The write path honours the same rule. `CreatePage` in "
        "`service_write.go` branches on the `wikiAuthor` "
        "parameter and then calls the helper:"
    ): (
        "写入路径也**遵守同一条规则**。"
        "`service_write.go` 里的 `CreatePage` 在 `wikiAuthor` 参数上分支，"
        "然后调用辅助函数："
    ),
    "`CreatePage` — author identity is a first-class argument, not a late inference.": (
        "`CreatePage` —— 作者身份是一等参数，而不是事后推断出来的。"
    ),
    (
        "type UpdatePageRequest struct {\n\tTitle              string             `json:\"title\"`\n\tBody               string             `json:\"body\"`\n\tTags               []string           `json:\"tags\"`\n\tSummary            string             `json:\"summary\"`\n\tDocType            DocType            `json:\"doc_type\"`\n\tCategory           string             `json:\"category\"`\n\tVerificationStatus VerificationStatus `json:\"verification_status,omitempty\"`\n}\n\nfunc (s *WikiService) CreatePage(req CreatePageRequest, user *auth.User, wikiAuthor string) (*PageResponse, error) {\n\tslug := GenerateSlug(req.Title + \".md\")\n\n\tif existing := s.findFileBySlug(slug); existing != \"\" {\n\t\treturn nil, fmt.Errorf(\"page already exists: %s\", slug)\n\t}\n\n\tnow := time.Now().UTC()\n\tcreatedBy := \"human\"\n\tif user != nil {\n\t\tcreatedBy = user.Username\n\t}\n\tif wikiAuthor == \"ai\" {\n\t\tcreatedBy = \"ai\"\n\t}\n\n\tdocType := req.DocType\n\tif docType == \"\" {\n\t\tdocType = DocTypeReference\n\t}\n\n\tvs := req.VerificationStatus\n\tif vs == \"\" {\n\t\tvs = DefaultVerificationStatus(createdBy)\n\t}\n\tif wikiAuthor == \"ai\" && vs == \"\" {\n\t\tvs = VerificationUnreviewed\n\t}\n\n\tfm := Frontmatter{\n\t\tTitle:              req.Title,\n\t\tSlug:               slug,\n\t\tTags:               req.Tags,\n\t\tSummary:            req.Summary,\n\t\tCreated:            now,\n\t\tCreatedBy:          createdBy,\n\t\tUpdated:            now,\n\t\tUpdatedBy:          createdBy,\n"
    ): (
        "type UpdatePageRequest struct {\n\tTitle              string             `json:\"title\"`\n\tBody               string             `json:\"body\"`\n\tTags               []string           `json:\"tags\"`\n\tSummary            string             `json:\"summary\"`\n\tDocType            DocType            `json:\"doc_type\"`\n\tCategory           string             `json:\"category\"`\n\tVerificationStatus VerificationStatus `json:\"verification_status,omitempty\"`\n}\n\nfunc (s *WikiService) CreatePage(req CreatePageRequest, user *auth.User, wikiAuthor string) (*PageResponse, error) {\n\tslug := GenerateSlug(req.Title + \".md\")\n\n\tif existing := s.findFileBySlug(slug); existing != \"\" {\n\t\treturn nil, fmt.Errorf(\"page already exists: %s\", slug)\n\t}\n\n\tnow := time.Now().UTC()\n\tcreatedBy := \"human\"\n\tif user != nil {\n\t\tcreatedBy = user.Username\n\t}\n\tif wikiAuthor == \"ai\" {\n\t\tcreatedBy = \"ai\"\n\t}\n\n\tdocType := req.DocType\n\tif docType == \"\" {\n\t\tdocType = DocTypeReference\n\t}\n\n\tvs := req.VerificationStatus\n\tif vs == \"\" {\n\t\tvs = DefaultVerificationStatus(createdBy)\n\t}\n\tif wikiAuthor == \"ai\" && vs == \"\" {\n\t\tvs = VerificationUnreviewed\n\t}\n\n\tfm := Frontmatter{\n\t\tTitle:              req.Title,\n\t\tSlug:               slug,\n\t\tTags:               req.Tags,\n\t\tSummary:            req.Summary,\n\t\tCreated:            now,\n\t\tCreatedBy:          createdBy,\n\t\tUpdated:            now,\n\t\tUpdatedBy:          createdBy,\n"
    ),
    "Two things deserve attention:": "有两件事值得留意：",
    (
        "`createdBy` is chosen at creation time from the "
        "authenticated user *or* an explicit AI marker, and then "
        "frozen in `fm.Created` / `fm.CreatedBy`. Nothing in the "
        "service ever mutates those fields again."
    ): (
        "`createdBy` 在**创建那一刻**从已登录用户 *或者* "
        "一个显式的 AI 标记中选出，"
        "然后冻结到 `fm.Created` / `fm.CreatedBy` 里。"
        "service 之后**再也不会**改这些字段。"
    ),
    (
        "After the page is written, the service asks the Git "
        "layer for the current commit hash and writes it back "
        "into `fm.Commit`. The page literally carries its birth "
        "commit in its header. This is `where-provenance` in the "
        "Buneman sense {cite}`buneman2001provenance`, and it is "
        "what lets a reader or an agent ask \"which version of "
        "the code does this doc describe?\" without leaving the "
        "file."
    ): (
        "页面写下去之后，"
        "service 向 Git 层要当前 commit 哈希，"
        "把它写回 `fm.Commit` 。"
        "这一页**字面上把自己诞生时那个 commit 写进了自己的头里**。"
        "这就是 Buneman 意义下的 `where-provenance` "
        "{cite}`buneman2001provenance` ，"
        "也是让一个读者、或者一个 agent "
        "在**不用离开这份文件**的前提下"
        "就能回答“这份文档描述的是哪个版本的代码？”的原因。"
    ),

    # ---- How: enforcing immutability ----
    (
        "An update path is where provenance usually leaks. A "
        "naïve \"overwrite the whole frontmatter\" handler would "
        "erase `created`, `created_by`, and `source` every time "
        "somebody fixed a typo. `MergeFrontmatterUpdate` "
        "prevents that at the data-structure level:"
    ): (
        "更新路径通常是**来源泄漏**的地方。"
        "一个朴素的“把整段 frontmatter 覆盖掉”的 handler ，"
        "会在每次有人修个错别字的时候"
        "把 `created` 、 `created_by` 、 `source` 全擦掉。"
        "`MergeFrontmatterUpdate` 在**数据结构这一层**就拦住它："
    ),
    "`MergeFrontmatterUpdate` — immutable fields are physically copied back from the existing record.": (
        "`MergeFrontmatterUpdate` —— 不可变字段从原记录里物理拷贝回来。"
    ),
    (
        "\n// DefaultVerificationStatus returns the appropriate default verification status\n// based on who created the page.\nfunc DefaultVerificationStatus(createdBy string) VerificationStatus {\n\tif createdBy == \"ai\" {\n\t\treturn VerificationUnreviewed\n\t}\n\treturn VerificationSupported\n}\n\n// MergeFrontmatterUpdate applies update fields to an existing frontmatter,\n// preserving immutable fields (created_by, created, source).\nfunc MergeFrontmatterUpdate(existing, update *Frontmatter) *Frontmatter {\n\tmerged := *update\n\n\t// Immutable fields — always preserve from existing\n\tmerged.Created = existing.Created\n"
    ): (
        "\n// DefaultVerificationStatus returns the appropriate default verification status\n// based on who created the page.\nfunc DefaultVerificationStatus(createdBy string) VerificationStatus {\n\tif createdBy == \"ai\" {\n\t\treturn VerificationUnreviewed\n\t}\n\treturn VerificationSupported\n}\n\n// MergeFrontmatterUpdate applies update fields to an existing frontmatter,\n// preserving immutable fields (created_by, created, source).\nfunc MergeFrontmatterUpdate(existing, update *Frontmatter) *Frontmatter {\n\tmerged := *update\n\n\t// Immutable fields — always preserve from existing\n\tmerged.Created = existing.Created\n"
    ),
    (
        "The update struct is the *starting* value of the merged "
        "result, so callers can freely pass anything. But "
        "`Created`, `CreatedBy`, and `Source` are then "
        "overwritten with the pre-existing values, and `Updated` "
        "is bumped to `time.Now().UTC()`. A malicious or "
        "careless caller cannot rewrite history even if they "
        "try. This is the single invariant that keeps the audit "
        "trail honest as the page evolves."
    ): (
        "更新结构体是合并结果的 *起始值* ，"
        "所以调用方可以**随便传**。"
        "但 `Created` 、 `CreatedBy` 、 `Source` "
        "随后会被**已有记录里的值**覆盖回去，"
        "而 `Updated` 会被顶到 `time.Now().UTC()` 。"
        "一个恶意或者粗心的调用方，"
        "**就算想**也改不了历史。"
        "**这是那个让审计轨迹在页面演化时仍然诚实的唯一不变式。**"
    ),

    # ---- Frontmatter vs footer ----
    (
        "So far the chapter has treated the frontmatter as *the* "
        "metadata record. In practice, two very different "
        "questions keep arriving at that one block and crowd "
        "each other out:"
    ): (
        "到目前为止，本章都把 frontmatter 当成 *那份* 元数据记录。"
        "但实践中，有**两种截然不同的问题**"
        "一直挤向同一个块，互相排挤："
    ),
    (
        "**Where did this page come from?** — `created_by`, "
        "`source`, `commit`. Lineage. Rarely changes after "
        "creation."
    ): (
        "**这一页从哪儿来？** —— "
        "`created_by` 、 `source` 、 `commit` 。"
        "**来源信息。** 创建之后很少变。"
    ),
    (
        "**Is this page still trusted, right now, by whom, and "
        "how much?** — `verification_status` is a single field "
        "trying to answer all of that. It is not enough."
    ): (
        "**这一页现在还值不值得信？被谁信？信到什么程度？** —— "
        "`verification_status` 是一个字段，"
        "**想一个人扛下这一整串问题**。"
        "扛不住。"
    ),
    (
        "The author's private project-knowledge-base toolkit "
        "{cite}`fanyamin_pkb_skill` resolves the crowding by "
        "putting review state into a second block: an "
        "HTML-comment **footer** at the bottom of the page, with "
        "six fields that every page must carry. This book adopts "
        "that split as its canonical shape. The frontmatter "
        "stays a *provenance* record; the footer is a *review* "
        "record:"
    ): (
        "作者的一个私人 project-knowledge-base 工具集 "
        "{cite}`fanyamin_pkb_skill` 是这样解决这个挤占问题的："
        "把**评审状态**放进第二块 —— "
        "页面最底部的一段 HTML-comment **footer** ，"
        "有六个**每一页都必须带**的字段。"
        "本书把这种拆分作为**规范形态**。"
        "frontmatter 仍然是一份 *来源* 记录；"
        "footer 是一份 *评审* 记录："
    ),
    (
        "<!-- PKB-metadata\nlast_updated: 2026-04-14\ncommit: "
        "4a1c92b\nupdated_by: ai\nreview_status: "
        "pending\nreview_score: 0\nreviewed_by:\n-->\n"
    ): (
        "<!-- PKB-metadata\nlast_updated: 2026-04-14\ncommit: "
        "4a1c92b\nupdated_by: ai\nreview_status: "
        "pending\nreview_score: 0\nreviewed_by:\n-->\n"
    ),
    "Six fields, each answering one narrow question:": (
        "六个字段，每一个回答一个很窄的问题："
    ),
    "Field": "字段",
    "Type": "类型",
    "What it answers": "它回答什么",
    "`last_updated`": "`last_updated`",
    "`YYYY-MM-DD`": "`YYYY-MM-DD`",
    "When was the page's body last touched by *anyone*?": (
        "这一页的正文最近一次被 *任何人* 动过是什么时候？"
    ),
    "`commit`": "`commit`",
    "short SHA": "短 SHA",
    (
        "Against which code commit? (Same semantics as "
        "frontmatter `commit`; co-located for cheap staleness "
        "checks.)"
    ): (
        "对着哪个代码 commit 写的？"
        "（语义和 frontmatter 里的 `commit` 一致；"
        "在这里共处一地，"
        "是为了让过时检查便宜。）"
    ),
    "`updated_by`": "`updated_by`",
    "`human` / `ai` / `ai+human`": "`human` / `ai` / `ai+human`",
    (
        "Who did the most recent change? Mirrors the YAML "
        "`updated_by` but uses a closed three-value vocabulary "
        "so a gate can match on it."
    ): (
        "最近一次改动是谁做的？"
        "和 YAML 里的 `updated_by` 相对应，"
        "但**这里用的是一套封闭的三值词汇表**，"
        "让闸可以精确地匹配。"
    ),
    "`review_status`": "`review_status`",
    "`pending` / `approved`": "`pending` / `approved`",
    "Has a human signed off on the current content?": (
        "有没有人为当前这份内容**签过字**？"
    ),
    "`review_score`": "`review_score`",
    "`0`–`5`": "`0`–`5`",
    (
        "How good is it, in the reviewer's judgement? `0` means "
        "not yet reviewed."
    ): (
        "在评审人看来，这页有多好？ `0` 表示还没被评审过。"
    ),
    "`reviewed_by`": "`reviewed_by`",
    "username or empty": "用户名，或空",
    "Which human reviewed it? Empty until reviewed.": (
        "是哪一个人评审的？评审之前为空。"
    ),
    (
        "**Why two blocks, not one.** Frontmatter and footer "
        "move at different rates and are touched by different "
        "actors. Frontmatter records *lineage*: it is written "
        "once at creation, patched carefully on update (see "
        "`MergeFrontmatterUpdate`), and should read cleanly in "
        "`git log` as an almost-unchanged header. Footer records "
        "*review state*: it resets to `pending` every time the "
        "body changes, and flips to `approved` only when a human "
        "acts. Co-locating both in frontmatter conflates the two "
        "rates of change — every review-state flip shows up as a "
        "provenance diff — and makes staleness harder to detect "
        "mechanically because a tool has to decide which fields "
        "are \"the lineage ones\" and which are \"the review "
        "ones\" field-by-field."
    ): (
        "**为什么是两块、不是一块。** "
        "frontmatter 和 footer 的**变化频率不同**，"
        "**动它们的人也不同**。"
        "frontmatter 记录的是 *来源* ："
        "创建时写一次，"
        "更新时小心打补丁（见 `MergeFrontmatterUpdate` ），"
        "在 `git log` 里应当看起来像一个**几乎不变**的干净头部。"
        "footer 记录的是 *评审状态* ："
        "正文一改，"
        "它就被重置为 `pending` ；"
        "只有**人出手**，它才翻到 `approved` 。"
        "把两者挤在一个 frontmatter 里，"
        "会混淆这两种变化速率 —— "
        "每一次评审状态翻转都会呈现为一次来源 diff —— "
        "还会让**过时检测**更难机械化，"
        "因为工具必须一字段一字段地判断“这个是血缘、那个是评审”。"
    ),
    (
        "**The AI-always-sets-pending rule.** When an LLM — or "
        "any automated path, including the L1 mechanical "
        "rewriter in Chapter 16 — modifies a page, "
        "`review_status` MUST be set to `pending`, "
        "`review_score` MUST be reset to `0`, and `reviewed_by` "
        "MUST be cleared. Only a *human* reviewer may set "
        "`approved` or a non-zero score. This is the single rule "
        "that makes human attention *auditable*: if the KB's "
        "gate system (Chapter 15) ever sees an `approved` state "
        "without a matching human `reviewed_by`, something "
        "bypassed the rule and the gate fails. Without this "
        "discipline, the word \"approved\" loses meaning the "
        "first time an LLM is allowed to write it."
    ): (
        "**“AI 永远设回 pending” 这条规则。** "
        "当一个 LLM —— "
        "或**任何**自动化路径，"
        "包括第 16 章那个 L1 机械改写器 —— 改动一张页时，"
        "`review_status` **必须**被设为 `pending` ，"
        "`review_score` **必须**重置为 `0` ，"
        "`reviewed_by` **必须**被清空。"
        "**只有** *人类* 评审可以把 `approved` 或非零分数写上去。"
        "这就是那条让人类注意力变得 *可审计* 的唯一规则："
        "一旦知识库的闸系统（第 15 章）"
        "看到一个 `approved` 状态却没有对应的人类 `reviewed_by` ，"
        "就说明有东西绕过了这条规则，闸就会失败。"
        "**没有这条纪律，“approved”这个词**在第一次让 LLM 写它的时候**就失去了意义**。**"
    ),
    (
        "**What the footer is *not*.** It is not a replacement "
        "for `verification_status`. The frontmatter field "
        "records the *editorial* trust signal (\"is this content "
        "supported, contradicted, superseded?\") and is about "
        "content correctness. The footer records the *review* "
        "signal (\"has a human looked at this version?\") and is "
        "about review cadence. A page can have "
        "`verification_status: supported` in the frontmatter and "
        "`review_status: pending` in the footer — meaning \"we "
        "believed it when it was written; no one has checked it "
        "since an LLM rewrote it yesterday\". Both signals "
        "matter; they answer different questions."
    ): (
        "**footer *不是* 什么。** "
        "它**不是** `verification_status` 的替代品。"
        "frontmatter 里的那个字段记录的是 *编辑层面的信任信号* "
        "（“这份内容是 supported，还是 contradicted，还是 superseded？”），"
        "关心的是**内容正确性**。"
        "footer 记录的是 *评审信号* "
        "（“有没有人看过当前这个版本？”），"
        "关心的是**评审节奏**。"
        "一页可以同时带着 `verification_status: supported` "
        "和 `review_status: pending` —— "
        "意思是：“这一页被写下来时我们是信的；"
        "昨天一个 LLM 把它重写了之后，还没人看过。”"
        "两种信号都重要；"
        "它们回答的是**不同的问题**。"
    ),
    (
        "Chapter 15 makes the footer a hard build gate; Chapter "
        "16 uses it to route changes through the three-level "
        "update strategy; Chapter 18 extends single-axis "
        "document layering (L0–L4) into a four-tuple `(layer, "
        "updated_by, review_status, review_score)` so a "
        "retrieval system can filter on review state without "
        "losing the lineage axis. The footer is the load-bearing "
        "hinge between this chapter and all three."
    ): (
        "第 15 章会把 footer 做成一道**硬构建闸**；"
        "第 16 章会用它把变更**路由**进三级更新策略；"
        "第 18 章会把单轴的文档分层（L0–L4）"
        "扩展成一个四元组 "
        "`(layer, updated_by, review_status, review_score)` ，"
        "让一个检索系统可以在**不丢失血缘这根轴**的前提下"
        "按评审状态筛选。"
        "**footer 是这一章与上面三章之间的承重铰链。**"
    ),

    # ---- Example ----
    "Here is the lifecycle of a single page, told through its frontmatter.": (
        "下面用一张页的 frontmatter 把它的完整生命周期讲一遍。"
    ),
    (
        "**Stage 1 — a human creates the page through the API.** "
        "Frontmatter and footer agree: Alice wrote it, she is "
        "its reviewer of record, it is approved at its birth "
        "commit."
    ): (
        "**阶段 1 —— 一个人通过 API 创建了这一页。** "
        "frontmatter 和 footer 意见一致："
        "Alice 写的，她是这一页的评审人，"
        "这一页在**诞生 commit** 上就是 approved 。"
    ),
    (
        "---\ntitle: How to enable TLS on the wiki\nslug: "
        "how-to-enable-tls-on-the-wiki\ncreated: "
        "2026-04-10T14:03:11Z\ncreated_by: alice\nupdated: "
        "2026-04-10T14:03:11Z\nupdated_by: alice\nstatus: "
        "published\ndoc_type: how-to\nverification_status: "
        "supported\ncommit: a1b2c3d4e5f6\n---\n"
    ): (
        "---\ntitle: How to enable TLS on the wiki\nslug: "
        "how-to-enable-tls-on-the-wiki\ncreated: "
        "2026-04-10T14:03:11Z\ncreated_by: alice\nupdated: "
        "2026-04-10T14:03:11Z\nupdated_by: alice\nstatus: "
        "published\ndoc_type: how-to\nverification_status: "
        "supported\ncommit: a1b2c3d4e5f6\n---\n"
    ),
    (
        "<!-- PKB-metadata\nlast_updated: 2026-04-10\ncommit: "
        "a1b2c3d4\nupdated_by: human\nreview_status: "
        "approved\nreview_score: 3\nreviewed_by: alice\n-->\n"
    ): (
        "<!-- PKB-metadata\nlast_updated: 2026-04-10\ncommit: "
        "a1b2c3d4\nupdated_by: human\nreview_status: "
        "approved\nreview_score: 3\nreviewed_by: alice\n-->\n"
    ),
    (
        "**Stage 2 — an LLM agent rewrites the body for "
        "clarity.** Frontmatter demotes `verification_status` to "
        "`unreviewed` (the existing Chapter-5 rule). Footer, "
        "enforcing the AI-always-sets-pending rule, resets "
        "`review_status` to `pending`, zeros `review_score`, and "
        "clears `reviewed_by`. The two blocks reinforce each "
        "other:"
    ): (
        "**阶段 2 —— 一个 LLM agent 为了让正文更清晰，把它重写了一遍。** "
        "frontmatter 按第 5 章原有规则"
        "把 `verification_status` 降为 `unreviewed` 。"
        "footer 按“AI 永远设回 pending”规则："
        "`review_status` 重置为 `pending` ，"
        "`review_score` 清零，"
        "`reviewed_by` 清空。"
        "**两块互相印证：**"
    ),
    (
        "---\ntitle: How to enable TLS on the wiki\nslug: "
        "how-to-enable-tls-on-the-wiki\ncreated: "
        "2026-04-10T14:03:11Z      # preserved\ncreated_by: "
        "alice                   # preserved\nupdated: "
        "2026-04-14T09:27:00Z      # bumped\nupdated_by: ai                      "
        "# new signal\nstatus: published\ndoc_type: "
        "how-to\nverification_status: unreviewed     # demoted "
        "by default\ncommit: 9f8e7d6c5b4a\n---\n"
    ): (
        "---\ntitle: How to enable TLS on the wiki\nslug: "
        "how-to-enable-tls-on-the-wiki\ncreated: "
        "2026-04-10T14:03:11Z      # 保持不变\ncreated_by: "
        "alice                   # 保持不变\nupdated: "
        "2026-04-14T09:27:00Z      # 已更新\nupdated_by: ai                      "
        "# 新信号\nstatus: published\ndoc_type: "
        "how-to\nverification_status: unreviewed     # 默认降级\n"
        "commit: 9f8e7d6c5b4a\n---\n"
    ),
    (
        "<!-- PKB-metadata\nlast_updated: 2026-04-14\ncommit: "
        "9f8e7d6c\nupdated_by: ai                 # matches "
        "frontmatter\nreview_status: pending         # reset: "
        "human has not seen this\nreview_score: 0                "
        "# reset\nreviewed_by:                   # cleared\n-->\n"
    ): (
        "<!-- PKB-metadata\nlast_updated: 2026-04-14\ncommit: "
        "9f8e7d6c\nupdated_by: ai                 # 与 frontmatter 一致\n"
        "review_status: pending         # 重置：人还没看过\n"
        "review_score: 0                # 重置\n"
        "reviewed_by:                   # 清空\n-->\n"
    ),
    (
        "Notice: `created_by` is still `alice`. The update did "
        "not rewrite history. But `verification_status` fell to "
        "`unreviewed` automatically *and* `review_status` fell "
        "to `pending`, so any reader or retriever that cares "
        "about trust can filter on either signal — or both."
    ): (
        "注意：`created_by` 仍然是 `alice` 。"
        "这次更新**没有**改写历史。"
        "但 `verification_status` 自动掉到了 `unreviewed` ， "
        "*同时* `review_status` 掉到了 `pending` ，"
        "所以任何**在意信任**的读者或者检索器，"
        "可以用这两个信号里的**任何一个** —— "
        "或者两个一起 —— "
        "来筛选。"
    ),
    (
        "**Stage 3 — a human approves the rewrite.** The "
        "frontmatter logs the reviewer as the most recent "
        "`updated_by`; the footer logs the separate act of "
        "*approval*, which is not the same thing as the act of "
        "editing:"
    ): (
        "**阶段 3 —— 一个人批准了这次重写。** "
        "frontmatter 把最近的 `updated_by` 记成这个评审人；"
        "footer 则单独记录了 *批准* 这一动作 —— "
        "它**和“编辑”这个动作不是一件事**："
    ),
    (
        "verification_status: supported\nupdated_by: "
        "alice\nupdated: 2026-04-14T10:15:42Z\n# created_by: "
        "alice  (still)\n"
    ): (
        "verification_status: supported\nupdated_by: "
        "alice\nupdated: 2026-04-14T10:15:42Z\n# created_by: "
        "alice  （仍然是）\n"
    ),
    (
        "<!-- PKB-metadata\nlast_updated: 2026-04-14\ncommit: "
        "9f8e7d6c\nupdated_by: ai+human           # AI wrote "
        "the body; a human approved it\nreview_status: "
        "approved\nreview_score: 4\nreviewed_by: alice\n-->\n"
    ): (
        "<!-- PKB-metadata\nlast_updated: 2026-04-14\ncommit: "
        "9f8e7d6c\nupdated_by: ai+human           # AI 写的正文；人批准的\n"
        "review_status: approved\nreview_score: 4\nreviewed_by: alice\n-->\n"
    ),
    (
        "The `ai+human` value on `updated_by` is deliberate: it "
        "records that the current state of the page is an LLM "
        "draft that a human has validated, which is a genuinely "
        "different provenance claim from either `ai` alone (LLM "
        "wrote it, no one has checked) or `human` alone (a human "
        "wrote it themselves). Chapter 18's document-layering "
        "tuple reads this value when it classifies a page."
    ): (
        "`updated_by` 上的 `ai+human` 这个值是**故意**的："
        "它记录的是 —— 当前这一页是一个 LLM 的草稿、"
        "一个人验证过。"
        "这和**单独的 `ai`**（LLM 写的，没人看过）"
        "以及**单独的 `human`**（人自己写的）"
        "是**真正不同的来源声明**。"
        "第 18 章那个文档分层元组在对一页分类时，"
        "会读这个值。"
    ),
    (
        "Three states, one file, a full provenance trail *and* a "
        "full review trail — and no side tables. `git log -p "
        "content/how-to/enable-tls.md` tells you the whole story "
        "for both."
    ): (
        "三个状态、一份文件、"
        "一条完整的**来源轨迹** *以及* 一条完整的**评审轨迹** —— "
        "**没有任何附表**。"
        "`git log -p content/how-to/enable-tls.md` "
        "就能把两条轨迹一次讲完。"
    ),

    # ---- Competing approaches ----
    "System": "系统",
    "Provenance model": "来源模型",
    "Immutability of authorship": "作者身份的不可变性",
    "Review state": "评审状态",
    "The prose-layer reference implementation": "文稿层参考实现",
    "YAML frontmatter + Git commit SHA + `PKB-metadata` footer": (
        "YAML frontmatter + Git commit SHA + `PKB-metadata` footer"
    ),
    "Enforced in `MergeFrontmatterUpdate`.": (
        "由 `MergeFrontmatterUpdate` 强制执行。"
    ),
    "Explicit six-field footer (see §\"Frontmatter versus footer\").": (
        "一段显式的六字段 footer（见 §“frontmatter 与 footer”）。"
    ),
    "Pandoc / MyST {cite}`pandoc,myst_parser`": (
        "Pandoc / MyST {cite}`pandoc,myst_parser`"
    ),
    "YAML metadata block": "一段 YAML 元数据块",
    "Convention only; no enforcement.": "**只是约定**；没有强制。",
    "None.": "没有。",
    "Notion AI {cite}`notion_ai`": "Notion AI {cite}`notion_ai`",
    "Proprietary audit log": "专有审计日志",
    "Opaque; vendor-controlled.": "不透明；由厂商控制。",
    "Per-block comments.": "逐块评论。",
    "Confluence": "Confluence",
    "Revision history table": "版本历史表",
    "Good; coupled to a proprietary DB.": (
        "做得不错；和专有数据库耦合在一起。"
    ),
    "Page status / labels.": "页面状态 / 标签。",
    "Plain Markdown + Git": "纯 Markdown + Git",
    "Git history only": "**只有** Git 历史",
    "Strong for *git blame*, but no explicit \"this was AI\" field.": (
        "*git blame* 很强，但**没有**显式的“这是 AI 写的”字段。"
    ),
    "W3C PROV-O {cite}`w3c_prov`": "W3C PROV-O {cite}`w3c_prov`",
    "Full RDF/OWL ontology": "完整的 RDF / OWL 本体",
    "Academic rigour; rarely adopted in docs tools.": (
        "学术上严谨；**在文档工具里极少被采用**。"
    ),
    "`prov:wasInvalidatedBy` models deprecation.": (
        "`prov:wasInvalidatedBy` 用来建模“被废弃”。"
    ),
    (
        "The reference implementation's stance is deliberately "
        "narrow: a tiny subset of PROV's vocabulary "
        "(`wasGeneratedBy`, `wasDerivedFrom`, "
        "`generatedAtTime`), encoded as plain YAML keys in the "
        "frontmatter and a six-field HTML-comment footer for "
        "review state, so authors and agents can read both "
        "without learning a new framework."
    ): (
        "**参考实现的立场是故意窄的：** "
        "只取 PROV 词汇表里**很小**的一个子集"
        "（ `wasGeneratedBy` 、 `wasDerivedFrom` 、 `generatedAtTime` ），"
        "把它们编码成 frontmatter 里的几条**普通 YAML 键**，"
        "再加上一段六字段 HTML-comment footer 来承载评审状态 —— "
        "这样**作者和 agent 都不用学一个新框架**，"
        "就能把两块读懂。"
    ),

    # ---- Common mistakes ----
    "Common mistakes, and how each one quietly breaks trust": (
        "常见错误，以及每一种怎样**悄无声息地**把信任层搞坏"
    ),
    (
        "Provenance schemas are failure-prone in a specific way: "
        "they degrade *silently*. A broken search box announces "
        "itself; a broken trust layer keeps serving pages that "
        "happen to be wrong. Five failure patterns show up in "
        "almost every real deployment, and each one has a "
        "corrective rule worth stating explicitly."
    ): (
        "**来源类 schema 的失败方式有一种很特别的共性：它们 *静默地* 退化。** "
        "一个坏掉的搜索框会**主动自报家门**；"
        "一个坏掉的信任层却会继续把**恰好是错的**页面端给你。"
        "在几乎每一个真实部署里都能看到五种失败形态，"
        "每一种都配有一条值得**显式写出来**的纠正规则。"
    ),
    (
        "**Treating `created_by` as mutable.** A well-intentioned "
        "bulk migration (\"let's re-stamp the author field now "
        "that we have real user accounts\") silently rewrites "
        "every page's `created_by`, and an entire audit trail "
        "evaporates. The rule is that authorship is "
        "*historical*, not *administrative*: once written, "
        "`created`, `created_by`, and `source` are frozen, and "
        "the only legitimate way to change them is to correct a "
        "genuine mistake *with a PR that records the correction "
        "in Git*. `MergeFrontmatterUpdate` enforces this at the "
        "data-structure level precisely because well-intentioned "
        "code paths cannot be trusted to remember the invariant "
        "{cite}`buneman2001provenance`."
    ): (
        "**把 `created_by` 当可变字段。** "
        "一次出发点很好的批量迁移"
        "（“我们现在有真正的用户账号了，"
        "把所有页的作者字段重新盖一遍章吧”）"
        "会**静默地**重写每一页的 `created_by` ，"
        "**一整条审计轨迹蒸发掉**。"
        "规则是：作者身份是 *历史性的* ，**不是** *行政性的* 。"
        "一旦写下，`created` 、 `created_by` 、 `source` **就被冻结**，"
        "**唯一**合法的修改方式是 "
        "*用一份在 Git 里记录这次改正的 PR 来纠正一个真正的错误* 。"
        "`MergeFrontmatterUpdate` 在数据结构这一层就强制执行这一点 —— "
        "恰恰因为**好意的代码路径不值得信任**，"
        "它们记不住这条不变式 {cite}`buneman2001provenance` 。"
    ),
    (
        "**Cramming review state into frontmatter.** The most "
        "common shape in the wild is a single `status: reviewed "
        "| pending` field in the frontmatter, and nothing else. "
        "It fails for the reason §\"Frontmatter versus footer\" "
        "already covered: review state flips every time an LLM "
        "touches the body, and a flipping review field in `git "
        "log` buries the *real* lineage changes under "
        "review-state noise. The two-block split is not a "
        "stylistic preference; it is what lets `git log` stay "
        "readable as the KB ages."
    ): (
        "**把评审状态**硬塞进 frontmatter 。 "
        "野外最常见的形态是："
        "frontmatter 里一个孤零零的 `status: reviewed | pending` ，"
        "再没有别的。"
        "它失败的原因 §“frontmatter 与 footer” 已经讲过："
        "评审状态**每次** LLM 碰正文都要翻转，"
        "一个在 `git log` 里不停翻转的评审字段"
        "会把 *真正的* 来源改动**埋在评审噪声之下**。"
        "**两块拆分不是风格偏好**；"
        "这是**让 `git log` 在知识库变老之后仍然可读**的那条线。"
    ),
    (
        "**No hard gate on `approved`.** A schema that permits "
        "any actor to write `review_status: approved` is a "
        "schema that, within a year, has LLM-approved pages in "
        "it. The AI-always-sets-pending rule is necessary but "
        "not sufficient — a build gate must additionally refuse "
        "to publish any page whose `approved` state lacks a "
        "matching human `reviewed_by`. Chapter 15 wires that "
        "gate in; the common failure is shipping the schema "
        "without the gate and *assuming* the rule will hold by "
        "convention."
    ): (
        "**`approved` 上没有硬闸。** "
        "一个允许**任何行动者**写 `review_status: approved` 的 schema，"
        "**不出一年里面就会有 LLM 批准的页**。"
        "“AI 永远设回 pending” 是**必要条件**，但**不充分** —— "
        "构建闸还必须额外拒绝发布"
        "**任何 `approved` 状态却没有对应人类 `reviewed_by` 的页**。"
        "第 15 章会把这道闸接进来；"
        "**常见的失败**是："
        "只上线了 schema 没上线闸，"
        "然后 *假设* 规则会**凭约定**自己站住。"
    ),
    (
        "**Ontology drift in `source.type`, `doc_type`, and "
        "status enumerations.** A team starts with a small "
        "closed vocabulary (`tutorial | how-to | reference | "
        "explanation`), and six months later the index has "
        "accreted `guide`, `docs`, `ref`, `manual`, and an empty "
        "string — because nobody refused the pull requests that "
        "introduced them. The rule is that closed vocabularies "
        "must be *syntactically* closed, i.e. the frontmatter "
        "validator must reject unknown values. A soft gate that "
        "merely warns is eaten by the review queue within weeks."
    ): (
        "**`source.type` 、 `doc_type` 、各种状态枚举上的本体漂移。** "
        "团队一开始用的是一套很小的**封闭词汇表**"
        "（ `tutorial | how-to | reference | explanation` ），"
        "半年之后索引里多出了 `guide` 、 `docs` 、 `ref` 、 `manual` "
        "和一个空字符串 —— "
        "**因为没人拒绝那些把它们引入进来的 PR**。"
        "规则是：**封闭词汇表必须 *在语法层* 封闭** —— "
        "也就是说，frontmatter 校验器**必须**拒绝未知值。"
        "一道“仅告警”的软闸会在几周内被评审队列**吃掉**。"
    ),
    (
        "**The re-verification cliff.** A page created in April "
        "with `verification_status: supported` is still "
        "`supported` in October, even though the code it "
        "describes has been rewritten twice. The frontmatter "
        "looks honest; the content is stale. This is the "
        "failure the Chapter 7a operational model is designed to "
        "surface: `verification_status` is a *point-in-time* "
        "claim tied to `commit`, and an automated staleness "
        "detector must mechanically demote pages whose `commit` "
        "no longer matches the code they reference (Chapter "
        "14). Trust that does not degrade automatically turns "
        "into fiction."
    ): (
        "**重验证悬崖。** "
        "一张 4 月创建的页，`verification_status: supported` ，"
        "到了 10 月仍然是 `supported` —— "
        "**尽管它描述的那段代码已经被重写了两次**。"
        "frontmatter 看上去很诚实；内容却**早就过时**了。"
        "这正是第 7a 章那套运维模型要**把它暴露出来**的那种失败："
        "`verification_status` 是一条**绑在 `commit` 上的 *时间点* 声明**，"
        "一个自动化的过时检测器**必须**机械地"
        "把那些 `commit` 已经不再与它们引用的代码对齐的页面"
        "降级（第 14 章）。"
        "**一份不会自动退化的信任，迟早变成虚构。**"
    ),
    (
        "**`source` fields that lie by omission.** A page "
        "imported from an external URL carries `source.uri` "
        "pointing at that URL — until the URL 404s or silently "
        "rewords the source. The rule is that `source.ref` (a "
        "commit-like identifier) must accompany `source.uri` "
        "whenever the source has one: for code imports, the code "
        "commit; for article imports, the Wayback Machine "
        "snapshot timestamp; for API specs, the OpenAPI file's "
        "content hash. A `source` without a `ref` is a moving "
        "target and, for audit purposes, no better than no "
        "source at all."
    ): (
        "**`source` 字段 *以省略的方式* 撒谎。** "
        "一份从外部 URL 导进来的页面，"
        "`source.uri` 指向那个 URL —— "
        "直到那个 URL 返回 404，"
        "或者**悄悄把原文换了个说法**。"
        "规则是：**只要来源有一个 commit-like 的标识符，"
        "`source.ref` 就必须伴随 `source.uri` 出现** —— "
        "代码类导入给代码 commit ；"
        "文章类导入给 Wayback Machine 的快照时间戳；"
        "API 规格给 OpenAPI 文件的内容哈希。"
        "**一个没有 `ref` 的 `source` 是一个移动靶** —— "
        "就审计目的而言，**它不比“完全没有来源”更好**。"
    ),
    (
        "The common thread across all six is that *provenance "
        "needs enforcement, not only expression*. A trust schema "
        "with no validator is decoration; a validator with no "
        "hard gate is a warning light no one reads. The "
        "chapter's whole argument is that frontmatter + footer"
    ): (
        "这六条的**共同线索**是： "
        "*来源需要强制执行，而不只是表达* 。"
        "**一个没有校验器的信任 schema 是装饰；"
        "一个没有硬闸的校验器是一盏没人看的警示灯。**"
        "这一章的整体论点就是：frontmatter + footer"
    ),
    (
        "merge invariants + build gates together form a single "
        "machine, and removing any corner collapses the other "
        "three."
    ): (
        "+ 合并不变式 + 构建闸合在一起**才是一台完整的机器**，"
        "**抽掉任何一个角，其他三个都会坍塌。**"
    ),

    # ---- Conclusion ----
    (
        "Frontmatter and footer are not decoration. Together "
        "they are the contract between the prose layer and every "
        "downstream consumer — retrieval, publishing, the code "
        "graph, an AI coding assistant — about *where a page "
        "came from* and *how much to trust it right now*. "
        "`SCHEMA.md` declares the contract; `frontmatter.go` and "
        "`service_write.go` enforce the lineage half; the "
        "`PKB-metadata` footer carries the review half; Git "
        "records both as physical diffs. Together they give a "
        "software KB something traditional wikis struggle to "
        "articulate: an explicit, machine-checkable answer to "
        "\"who wrote this, against which commit, is it still "
        "trusted, and by whom?\""
    ): (
        "**frontmatter 和 footer 不是装饰。** "
        "把它们合起来看，"
        "就是文稿层和每一个下游消费者"
        "（检索、发布、代码图谱、一个 AI 编码助手）"
        "之间的**契约**："
        "关于 *这一页从哪儿来* 、"
        "以及 *现在该信它多少* 的契约。"
        "`SCHEMA.md` **声明**这份契约；"
        "`frontmatter.go` 和 `service_write.go` 强制执行**来源**那一半；"
        "`PKB-metadata` footer 承载**评审**那一半；"
        "Git 把两者都**作为物理 diff 记录下来**。"
        "合在一起，它们就给了一个软件知识库一件"
        "传统 wiki 难以说清楚的东西："
        "对“**这页是谁写的、对着哪个 commit、现在是否仍被信任、被谁信任**？”"
        "**显式的、可机器检查的回答**。"
    ),
    (
        "The next chapter takes that contract and walks through "
        "the pipeline that produces well-formed frontmatter — "
        "and an honest `pending` footer — even when the input is "
        "a messy folder of dumped files."
    ): (
        "下一章把这份契约拿过来，"
        "走一遍那条流水线："
        "**即使输入是一整个乱糟糟的、被随手倾倒进来的文件夹，**"
        "它也要产出**规格良好的 frontmatter** 和**一份诚实的 `pending` footer**。"
    ),

    # ---- Hook opening ----
    (
        "You are on a video call with the security team. They "
        "have the wiki page for the authentication flow open in "
        "one window and your Postgres schema in another. \"This "
        "says the reset token is a UUID,\" they say. \"It's been "
        "an HMAC since March.\" Then: \"Who wrote this? When?\" "
        "You scroll up. You scroll down. The wiki tells you it "
        "was \"last edited by the system\", four months ago, "
        "with no diff. It does not tell you whether a human "
        "wrote it, whether a human ever read it, or against "
        "which commit of the backend it was supposed to be true."
    ): (
        "你正和安全团队开视频会议。"
        "他们**一边**开着 wiki 上那页"
        "描述**认证流程**的页面，"
        "**另一边**开着你这边的 Postgres schema。"
        "“这上面**写的是**重置 token 是 UUID，”他们说，"
        "“但这东西**从三月起就已经是 HMAC 了**。”"
        "接着：“**谁写的？什么时候写的？**”"
        "你往上翻，你往下翻。"
        "wiki 告诉你的是：这页"
        "“**四个月前、由系统最后编辑**”，"
        "**没有 diff**。"
        "它**并不告诉你**：是不是有人类写的？"
        "有没有人类**看过**？"
        "它**本应对标**的、**后端的哪一次 commit**？"
    ),
    (
        "This chapter is about the second smallest change a "
        "software KB can make and the largest payoff it can "
        "extract from that change: a YAML frontmatter block at "
        "the top of every file and a six-field HTML comment at "
        "the bottom. Together, those two blocks force the KB "
        "to answer four questions — *who, when, against what, "
        "and has anyone checked* — at the beginning of every "
        "conversation rather than the middle of the bad ones."
    ): (
        "这一章讲的是：**一个软件知识库能做的第二小的改动**，"
        "以及从这个改动里**能兑换到的最大的回报** —— "
        "每一份文件**顶上**一段 YAML frontmatter，"
        "**底上**一段带六个字段的 HTML 注释。"
        "这**两块东西**加在一起，"
        "就会**强迫**知识库在**每一次对话开始**时"
        "（而不是**在糟糕对话的半截**）"
        "回答**四个问题** —— "
        " *谁写的、什么时候、对标的是什么、有没有人核对过* 。"
    ),
}
