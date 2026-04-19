"""Chinese translations for book/part2-prose-layer/ch04-file-based-wiki.md.

See book/_tools/translations/ch02-ir-rag-primer.zh.py for the full
style guide. Chapter-specific notes:

- Markdown, YAML, Git, CI, CLI, PR, URL, HTTP, HTTPS, JSON, YAML,
  WYSIWYG, ORM, LFS, Vim, API, S3, Figma, Google Docs, GitHub,
  GitLab, DokuWiki, MoinMoin, Gitit, Obsidian, Notion, Confluence,
  Wikipedia, RBAC, Sphinx, Diátaxis, docs-as-code — all kept in
  English.
- "wiki" kept in English (product category noun).
- "frontmatter" / "footer" kept in English (paired formal concepts
  from the book's contract).
- `content/`, `raw/`, `metadata/`, `_assets/`, `_sphinx/` kept
  verbatim because they are on-disk layout tokens.
- "docs-as-code bargain" → "docs-as-code 的那笔交易"
  (consistent with the idiom used elsewhere in Part I).
- Go code blocks stay verbatim in the translation.
- CommonMark emphasis rule — ASCII whitespace around `*...*` when
  flanked by CJK.
"""

PO_PATH = "part2-prose-layer/ch04-file-based-wiki.po"

TRANSLATIONS: dict[str, str] = {
    # ---- Title + mindmap intro ----
    "Chapter 4 — A File-based Wiki": "第 4 章 —— 一个基于文件的 wiki",
    (
        "This chapter on one page — the storage choice that every "
        "later prose-layer chapter takes for granted, the "
        "Git-as-infrastructure payoff it unlocks, the tiny Go "
        "interface that hides the filesystem from the rest of the "
        "codebase, and the failure modes file-based wikis actually "
        "exhibit in the wild:"
    ): (
        "本章浓缩成一页 —— "
        "后面所有文稿层章节都默认接受的那个**存储选择**，"
        "它所解锁的**把 Git 当基础设施**的那笔回报，"
        "那个小小的 Go 接口 —— "
        "它把文件系统挡在整个代码库的其它部分之外；"
        "以及**基于文件的 wiki 在真实世界里真正出现过的失败形态**："
    ),
    "Why": "为什么",
    "What": "是什么",
    "How": "怎么做",
    "Example": "示例",
    "Conclusion": "结论",
    "References": "参考文献",
    "Competing approaches": "其他做法",

    # ---- Why ----
    (
        "Part I argued that a software KB should behave like "
        "code: versioned, reviewable, diffable, automatable. "
        "Chapter 3 narrowed the prose layer to four Diátaxis "
        "genres. This chapter answers the next question: *where "
        "does that prose physically live?*"
    ): (
        "第一部分论证过：一个软件知识库应该**像代码一样**行事 —— "
        "有版本、可评审、可 diff、可自动化。"
        "第 3 章又把文稿层再收窄到 Diátaxis 的四种文档类型。"
        "这一章要回答的是下一个问题： "
        "*这些文稿，在物理上到底放在哪里？*"
    ),
    (
        "Database-backed wikis optimise for editing. They give "
        "you live rendering, concurrent sessions, WYSIWYG "
        "toolbars, and revision history — at the cost of pulling "
        "every document into an opaque table whose schema you do "
        "not own {cite}`notion_ai,obsidian`. Three things break "
        "when you do that:"
    ): (
        "**基于数据库的 wiki** 是为“编辑”这件事优化的。"
        "它们给你实时渲染、"
        "多人并发会话、"
        "WYSIWYG 工具栏、"
        "以及版本历史 —— "
        "代价是把每一份文档塞进一个你并不拥有其 schema 的不透明表里"
        "{cite}`notion_ai,obsidian` 。"
        "这么一搞，三件事就坏掉了："
    ),
    (
        "**Provenance.** \"Who wrote this paragraph, under which "
        "commit of the code?\" becomes a database query against "
        "a proprietary audit log, instead of `git blame` on a "
        "Markdown file."
    ): (
        "**来源。** "
        "“这一段是谁写的？基于哪个 commit 的代码写的？”"
        "变成了一次针对专有审计日志的数据库查询，"
        "而不是对一份 Markdown 文件跑 `git blame` 。"
    ),
    (
        "**Review.** A pull request can show a code change and a "
        "doc change side by side *only if* the doc is a file in "
        "the same repo. Otherwise the review splits across two "
        "systems and drifts apart "
        "{cite}`gruver2016starting,docs_as_code`."
    ): (
        "**评审。** "
        "一个 pull request 能把**代码改动**和**文档改动**放在一起看， "
        "*前提是* 文档也是同一个仓库里的文件。"
        "否则评审就被劈成两套系统、"
        "然后慢慢互相漂离 "
        "{cite}`gruver2016starting,docs_as_code` 。"
    ),
    (
        "**Automation.** The `init → import → verify → build → "
        "serve` pipeline that Part II is about needs an input it "
        "can read, write, diff, and version. A file is all of "
        "those; a database row is none of them."
    ): (
        "**自动化。** "
        "第二部分讲的那条 `init → import → verify → build → serve` 流水线，"
        "需要的是一份**可读、可写、可 diff、可版本化**的输入。"
        "一个文件四个都是；"
        "一条数据库行一个都不是。"
    ),
    (
        "So the prose-layer reference implementation this book "
        "uses is a tree of plain Markdown files under "
        "`content/`, one page per file, governed by the same Git "
        "repository as the code that describes the software. The "
        "wiki *is* the repo {cite}`gitit,dokuwiki,moinmoin`."
    ): (
        "所以本书用的**文稿层参考实现**，"
        "就是 `content/` 底下一棵纯 Markdown 文件树，"
        "一页一文件，"
        "和“描述这份软件的代码”共享同一个 Git 仓库。"
        "这里的 wiki *就是* 这个仓库 "
        "{cite}`gitit,dokuwiki,moinmoin` 。"
    ),

    # ---- What ----
    (
        "Concretely, an instance of the prose-layer reference "
        "implementation is a directory with four conventions:"
    ): (
        "具体一点：一个**文稿层参考实现**的实例，"
        "就是一个满足四条约定的目录："
    ),
    (
        "wiki-root/\n"
        "├── content/              # Markdown files, one per page\n"
        "│   ├── getting-started/\n"
        "│   │   └── install.md\n"
        "│   ├── reference/\n"
        "│   │   └── api.md\n"
        "│   └── _assets/          # images, downloaded binaries\n"
        "├── metadata/\n"
        "│   ├── SCHEMA.md         # frontmatter contract (see ch05)\n"
        "│   ├── wiki.yaml         # instance config\n"
        "│   ├── users.yaml        # auth\n"
        "│   └── _sphinx/          # publishing toolchain\n"
        "└── raw/                  # staging area for unprocessed imports\n"
    ): (
        "wiki-root/\n"
        "├── content/              # Markdown 文件，一页一文件\n"
        "│   ├── getting-started/\n"
        "│   │   └── install.md\n"
        "│   ├── reference/\n"
        "│   │   └── api.md\n"
        "│   └── _assets/          # 图片、下载下来的二进制文件\n"
        "├── metadata/\n"
        "│   ├── SCHEMA.md         # frontmatter 契约（见第 5 章）\n"
        "│   ├── wiki.yaml         # 实例配置\n"
        "│   ├── users.yaml        # 认证\n"
        "│   └── _sphinx/          # 发布用的工具链\n"
        "└── raw/                  # 尚未处理的导入件的暂存区\n"
    ),
    (
        "Every page is a Markdown file with a YAML frontmatter "
        "block. Every category is a directory. "
        "Underscore-prefixed directories (`_assets/`, `_sphinx/`) "
        "are reserved for infrastructure and are invisible to "
        "readers. The wiki has no database, no object store, no "
        "hidden index: everything observable is a file you can "
        "`cat`, `grep`, or `git log` against."
    ): (
        "**每一页**是一份带 YAML frontmatter 块的 Markdown 文件。"
        "**每一个分类**是一个目录。"
        "下划线开头的目录（ `_assets/` 、 `_sphinx/` ）"
        "留给基础设施使用，对读者不可见。"
        "这个 wiki 没有数据库，没有对象存储，没有隐藏索引："
        "所有**能观察到的东西都是一份文件**，"
        "你可以 `cat` 、 `grep` 、或对它跑 `git log` 。"
    ),
    (
        "The code that enforces this lives in "
        "`backend/internal/wiki/`. Two files carry the weight:"
    ): (
        "强制这条约定的代码放在 `backend/internal/wiki/` 。"
        "真正扛事的就两个文件："
    ),
    "`repository.go` — the file-system I/O boundary.": (
        "`repository.go` —— 文件系统 I/O 的边界。"
    ),
    (
        "`service.go` — the read-side API, backed entirely by "
        "that repository and an in-memory index."
    ): (
        "`service.go` —— 读侧 API，"
        "完全靠上面那个 repository 加一个内存索引支撑。"
    ),

    # ---- How: repository interface ----
    "The repository interface": "仓库接口",
    (
        "The `WikiRepository` interface is the only place in the "
        "backend that touches the filesystem for page content. "
        "Everything above it — services, HTTP handlers, the CLI "
        "— operates on `*Page` values and never calls "
        "`os.ReadFile` directly. This is a classic "
        "ports-and-adapters layering, and it means a future "
        "Git-aware or S3-backed repository can drop in without "
        "touching any of the business logic."
    ): (
        "`WikiRepository` 接口是整个后端**唯一**为页面内容碰文件系统的地方。"
        "它上面的一切 —— 服务、HTTP handler、CLI —— "
        "都只对 `*Page` 值打交道，"
        "**永远**不直接调 `os.ReadFile` 。"
        "这是一个经典的 ports-and-adapters 分层，"
        "带来的直接好处就是："
        "哪天想换成一个懂 Git 的实现、"
        "或者一个基于 S3 的实现，"
        "都可以**直接塞进来**，"
        "不用动任何业务逻辑。"
    ),
    "The full repository interface, five methods.": (
        "完整的仓库接口，五个方法。"
    ),
    '\npackage wiki\n\nimport (\n\t"fmt"\n\t"os"\n\t"path/filepath"\n': (
        '\npackage wiki\n\nimport (\n\t"fmt"\n\t"os"\n\t"path/filepath"\n'
    ),
    (
        "Notice what is *not* on this interface: no \"update\", "
        "no \"lock\", no \"transaction\". A file-based wiki "
        "replaces those with `git commit`. Writes are "
        "last-write-wins at the filesystem level; if you want "
        "review gates, you get them from the repo hosting "
        "platform, not from the wiki engine itself."
    ): (
        "注意看这个接口上 *没有* 什么："
        "没有“update”，"
        "没有“lock”，"
        "没有“transaction”。"
        "一个基于文件的 wiki 用 `git commit` 把这些全顶掉。"
        "在文件系统这一层，写入是 last-write-wins 的；"
        "**想要评审闸**，"
        "请去仓库托管平台上拿，"
        "**不要**找 wiki 引擎本身要。"
    ),

    # ---- How: reading pages ----
    "Reading a page is parsing a file": "读一页就是解析一份文件",
    (
        "`ReadPage` is the canonical path from bytes on disk to "
        "a `*Page` value:"
    ): (
        "`ReadPage` 是从“磁盘上的字节”到“一个 `*Page` 值”的规范路径："
    ),
    "`FileRepository.ReadPage` — read, split, parse, derive.": (
        "`FileRepository.ReadPage` —— 读、切、解析、派生。"
    ),
    (
        "}\n\ntype FileRepository struct {\n\tContentDir string\n"
        "}\n\nfunc NewFileRepository(contentDir string) "
        "*FileRepository {\n\treturn &FileRepository{ContentDir: "
        "contentDir}\n}\n\nfunc (r *FileRepository) "
        "ReadPage(filePath string) (*Page, error) {\n\tdata, err "
        ":= os.ReadFile(filePath)\n\tif err != nil {\n\t\tif "
        "os.IsNotExist(err) {\n\t\t\treturn nil, "
        "fmt.Errorf(\"page not found: %s\", "
        "filePath)\n\t\t}\n\t\treturn nil, fmt.Errorf(\"failed "
        "to read page: %w\", err)\n\t}\n\n\tcontent := "
        "string(data)\n\tfm, body, err := "
        "ParseFrontmatter(content)\n\tif err != nil "
        "{\n\t\treturn nil, fmt.Errorf(\"failed to parse "
        "frontmatter: %w\", err)\n\t}\n\n\tif fm == nil {\n\t\tfm "
        "= InferFrontmatter(filePath)\n\t}\n"
    ): (
        "}\n\ntype FileRepository struct {\n\tContentDir string\n"
        "}\n\nfunc NewFileRepository(contentDir string) "
        "*FileRepository {\n\treturn &FileRepository{ContentDir: "
        "contentDir}\n}\n\nfunc (r *FileRepository) "
        "ReadPage(filePath string) (*Page, error) {\n\tdata, err "
        ":= os.ReadFile(filePath)\n\tif err != nil {\n\t\tif "
        "os.IsNotExist(err) {\n\t\t\treturn nil, "
        "fmt.Errorf(\"page not found: %s\", "
        "filePath)\n\t\t}\n\t\treturn nil, fmt.Errorf(\"failed "
        "to read page: %w\", err)\n\t}\n\n\tcontent := "
        "string(data)\n\tfm, body, err := "
        "ParseFrontmatter(content)\n\tif err != nil "
        "{\n\t\treturn nil, fmt.Errorf(\"failed to parse "
        "frontmatter: %w\", err)\n\t}\n\n\tif fm == nil {\n\t\tfm "
        "= InferFrontmatter(filePath)\n\t}\n"
    ),
    "Four steps, all local, all deterministic:": (
        "四步，全本地、全确定性："
    ),
    "**Read.** `os.ReadFile` lifts the bytes.": (
        "**读。** `os.ReadFile` 把字节拿进来。"
    ),
    (
        "**Split.** `ParseFrontmatter` separates the YAML header "
        "from the body (Chapter 5 covers the format)."
    ): (
        "**切。** `ParseFrontmatter` 把 YAML 头和正文切开"
        "（第 5 章讲 YAML 头的格式）。"
    ),
    (
        "**Recover.** If there is no frontmatter, "
        "`InferFrontmatter` synthesises a minimal one from the "
        "filename and mtime. A page without metadata still "
        "round-trips."
    ): (
        "**补救。** "
        "如果没有 frontmatter，"
        "`InferFrontmatter` 会从文件名和 mtime 合成一份最小的 frontmatter 。"
        "**没有元数据的页面依然能 round-trip。**"
    ),
    (
        "**Derive.** `DeriveCategory` computes the category from "
        "the file's path relative to `ContentDir`. The directory "
        "structure *is* the category hierarchy; there is no "
        "separate \"tag table\"."
    ): (
        "**派生。** "
        "`DeriveCategory` 根据文件相对 `ContentDir` 的路径算出分类。"
        "**目录结构 *就是* 分类体系**；"
        "并没有另一张独立的“tag 表”。"
    ),
    "`ListFiles` codifies one more filesystem convention:": (
        "`ListFiles` 把另一条文件系统约定固化下来："
    ),
    "`ListFiles` — walk the tree, skipping reserved names.": (
        "`ListFiles` —— 遍历整棵目录树，跳过保留名字。"
    ),
    (
        "func (r *FileRepository) DeletePage(filePath string) "
        "error {\n\tif err := os.Remove(filePath); err != nil "
        "{\n\t\tif os.IsNotExist(err) {\n\t\t\treturn "
        "fmt.Errorf(\"page not found: %s\", "
        "filePath)\n\t\t}\n\t\treturn fmt.Errorf(\"failed to "
        "delete page: %w\", err)\n\t}\n\treturn "
        "nil\n}\n\nfunc (r *FileRepository) ListFiles(dir "
        "string) ([]string, error) {\n\tvar files []string\n\terr "
        ":= filepath.Walk(dir, func(path string, info "
        "os.FileInfo, err error) error {\n\t\tif err != nil "
        "{\n\t\t\treturn err\n\t\t}\n\t\tif info.IsDir() "
        "{\n\t\t\tbase := filepath.Base(path)\n\t\t\tif "
        "strings.HasPrefix(base, \"_\") && path != dir "
        "{\n\t\t\t\treturn filepath.SkipDir\n\t\t\t}\n\t\t\treturn "
        "nil\n\t\t}\n\t\tif !strings.HasSuffix(path, \".md\") "
        "{\n\t\t\treturn nil\n"
    ): (
        "func (r *FileRepository) DeletePage(filePath string) "
        "error {\n\tif err := os.Remove(filePath); err != nil "
        "{\n\t\tif os.IsNotExist(err) {\n\t\t\treturn "
        "fmt.Errorf(\"page not found: %s\", "
        "filePath)\n\t\t}\n\t\treturn fmt.Errorf(\"failed to "
        "delete page: %w\", err)\n\t}\n\treturn "
        "nil\n}\n\nfunc (r *FileRepository) ListFiles(dir "
        "string) ([]string, error) {\n\tvar files []string\n\terr "
        ":= filepath.Walk(dir, func(path string, info "
        "os.FileInfo, err error) error {\n\t\tif err != nil "
        "{\n\t\t\treturn err\n\t\t}\n\t\tif info.IsDir() "
        "{\n\t\t\tbase := filepath.Base(path)\n\t\t\tif "
        "strings.HasPrefix(base, \"_\") && path != dir "
        "{\n\t\t\t\treturn filepath.SkipDir\n\t\t\t}\n\t\t\treturn "
        "nil\n\t\t}\n\t\tif !strings.HasSuffix(path, \".md\") "
        "{\n\t\t\treturn nil\n"
    ),
    (
        "Directories whose names start with `_` are skipped "
        "(reserved for infrastructure), and `_category.md` files "
        "are hidden from normal page listings because they "
        "describe a directory rather than being a page in their "
        "own right. Two tiny conventions carry all the weight of "
        "\"what counts as a wiki page\"."
    ): (
        "目录名以 `_` 开头的被跳过（留给基础设施），"
        "`_category.md` 文件对普通页面列表不可见 —— "
        "因为它描述的是**一个目录**，"
        "而不是**一页独立的内容**。"
        "两条非常小的约定，"
        "扛起了“**什么算一页 wiki 页面**”全部的重量。"
    ),

    # ---- How: service ----
    "The service is a thin shell around the repository": (
        "service 是对 repository 的一层很薄的壳"
    ),
    (
        "`WikiService` layers an index, a renderer, and "
        "filter/pagination on top of the repository, but its "
        "constructor is a dependency list, not a database "
        "connection:"
    ): (
        "`WikiService` 在 repository 之上叠了一个索引、一个渲染器、"
        "以及筛选 / 分页能力；"
        "但它的构造函数**是一份依赖清单**，"
        "不是一条数据库连接："
    ),
    "`WikiService` — three dependencies, no driver.": (
        "`WikiService` —— 三个依赖，零 driver。"
    ),
    (
        "}\n\ntype PageFilter struct {\n\tCategory           "
        "string\n\tDocType            "
        "DocType\n\tVerificationStatus "
        "VerificationStatus\n\tCreatedBy          "
        "string\n\tTag                string\n}\n\ntype "
        "WikiService struct {\n\trepo       "
        "*FileRepository\n\trenderer   *WikiRenderer\n\tindex      "
        "*IndexEngine\n\tgit        *GitService\n\tgovernance "
        "*GovernanceManager\n"
    ): (
        "}\n\ntype PageFilter struct {\n\tCategory           "
        "string\n\tDocType            "
        "DocType\n\tVerificationStatus "
        "VerificationStatus\n\tCreatedBy          "
        "string\n\tTag                string\n}\n\ntype "
        "WikiService struct {\n\trepo       "
        "*FileRepository\n\trenderer   *WikiRenderer\n\tindex      "
        "*IndexEngine\n\tgit        *GitService\n\tgovernance "
        "*GovernanceManager\n"
    ),
    (
        "On startup, the service asks the repository for every "
        "Markdown file under `ContentDir`, reads each into a "
        "`*Page`, and hands the whole list to the index for a "
        "full rebuild:"
    ): (
        "启动时，service 向 repository 要一份 "
        "`ContentDir` 下的全部 Markdown 文件，"
        "逐个读成 `*Page` ，"
        "把整张清单交给索引去做一次**全量重建**："
    ),
    (
        "`LoadAndIndex` — walk the tree, parse each file, "
        "rebuild the index from scratch."
    ): (
        "`LoadAndIndex` —— 遍历目录树，逐个文件解析，"
        "把索引从零重建。"
    ),
    (
        "}\n\nfunc (s *WikiService) SetGitService(git "
        "*GitService) {\n\ts.git = git\n}\n\nfunc (s "
        "*WikiService) SetGovernanceManager(gov "
        "*GovernanceManager) {\n\ts.governance = "
        "gov\n}\n\nfunc (s *WikiService) LoadAndIndex() error "
        "{\n\tfiles, err := s.repo.ListFiles(s.repo.ContentDir)\n"
        "\tif err != nil {\n\t\treturn fmt.Errorf(\"failed to "
        "list files: %w\", err)\n\t}\n\n\tvar pages []*Page\n"
    ): (
        "}\n\nfunc (s *WikiService) SetGitService(git "
        "*GitService) {\n\ts.git = git\n}\n\nfunc (s "
        "*WikiService) SetGovernanceManager(gov "
        "*GovernanceManager) {\n\ts.governance = "
        "gov\n}\n\nfunc (s *WikiService) LoadAndIndex() error "
        "{\n\tfiles, err := s.repo.ListFiles(s.repo.ContentDir)\n"
        "\tif err != nil {\n\t\treturn fmt.Errorf(\"failed to "
        "list files: %w\", err)\n\t}\n\n\tvar pages []*Page\n"
    ),
    (
        "This is deliberately simple. There is no incremental "
        "index, no change-data-capture, no cache invalidation "
        "strategy. A full rescan on boot is fast enough for tens "
        "of thousands of pages (the walk is I/O- bound, not "
        "CPU-bound), and it eliminates an entire class of "
        "\"index is out of sync with disk\" bugs that plague "
        "database-backed wikis. When you edit a file with `vim` "
        "outside the server, `LoadAndIndex` on the next restart "
        "will see it. When the index engine pushes a page in "
        "response to a write, it stays in sync because there is "
        "only one writer — the service. The filesystem is the "
        "source of truth; everything else is a derived cache."
    ): (
        "**这是故意简单的。** "
        "没有增量索引、没有 change-data-capture、没有缓存失效策略。"
        "启动时全量扫一次，对几万级页面来说已经够快 —— "
        "这个遍历是 I/O-bound，不是 CPU-bound —— "
        "同时它干掉了“**索引和磁盘对不上**”这一整类 bug，"
        "而这类 bug 是基于数据库的 wiki 永远会反复踩到的那种。"
        "你用 `vim` 在服务器外面改了一份文件，"
        "下次重启时 `LoadAndIndex` 就会看到。"
        "索引引擎在“写入”这个事件里把页面推进来时，"
        "它也一直是同步的 —— "
        "因为唯一的**写入者**只有一个："
        "就是 service 自己。"
        "**文件系统是真相来源；其余的一切都是派生缓存。**"
    ),

    # ---- How: Git gets you ----
    "What Git gets you for free": "Git 白送给你什么",
    (
        "Because the content directory is a Git working tree, a "
        "great deal of behaviour that a wiki usually has to "
        "implement itself comes from the surrounding platform:"
    ): (
        "因为内容目录**本身就是一个 Git 工作树**，"
        "一个 wiki 平时需要自己实现的很多东西，"
        "这里都由外围平台直接白送给你："
    ),
    "Feature": "功能",
    "Wiki engines typically ship": "wiki 引擎通常自带的实现",
    "The file-based model delegates to": "基于文件的模型把它委托给",
    "Revision history": "版本历史",
    "Custom page_revisions table": "自建的 page_revisions 表",
    "`git log`": "`git log`",
    "Blame": "Blame",
    "Custom author field per paragraph": "每段一个自建的作者字段",
    "`git blame`": "`git blame`",
    "Diff/review": "Diff / 评审",
    "In-app diff viewer": "应用内置的 diff 查看器",
    "GitHub/GitLab PR UI": "GitHub / GitLab 的 PR UI",
    "Rollback": "回滚",
    "Custom restore endpoint": "自建的 restore 接口",
    "`git revert`": "`git revert`",
    "Branching": "分支",
    "Usually absent": "通常没有",
    "Native": "原生支持",
    "Offline edit": "离线编辑",
    "Proprietary sync client": "专有的同步客户端",
    "`git pull` / `git push`": "`git pull` / `git push`",
    (
        "This is the docs-as-code bargain made concrete "
        "{cite}`gruver2016starting,docs_as_code`: the wiki gives "
        "up \"slick in-browser edit\" and gains the entire Git "
        "ecosystem. Chapter 10 will show why that bargain is "
        "decisive for the graph layer too — a code KB that can "
        "point at a commit SHA becomes a completely different "
        "thing from one that can only point at \"the current "
        "state of some database\"."
    ): (
        "这就是把 docs-as-code 的那笔交易**具象化**出来 "
        "{cite}`gruver2016starting,docs_as_code` ："
        "wiki 放弃“在浏览器里的那种顺滑编辑”，"
        "换来**整个 Git 生态**。"
        "第 10 章会讲为什么这笔交易对**图谱层**也是决定性的 —— "
        "一个能指向某个 commit SHA 的代码知识库，"
        "和一个只能指向“某个数据库当前状态”的代码知识库，"
        "是两种完全不同的东西。"
    ),

    # ---- Example ----
    (
        "Here is the smallest end-to-end round-trip, enough to "
        "prove the model works. (The full walkthrough is in "
        "Appendix A.)"
    ): (
        "下面是**最小可行的端到端闭环**，"
        "足够证明这个模型是成立的。"
        "（完整的分步走在附录 A。）"
    ),
    (
        "$ make wiki-init WIKI_DIR=./demo-wiki\n"
        "$ ls demo-wiki/\n"
        "content/   metadata/   raw/\n\n"
        "$ cat > demo-wiki/content/reference/hello.md <<'MD'\n"
        "---\n"
        "title: Hello\n"
        "slug: hello\n"
        "doc_type: reference\n"
        "status: published\n"
        "---\n\n"
        "# Hello\n\n"
        "This is a wiki page. It is also a file in a Git "
        "repository.\n"
        "MD\n\n"
        "$ cd demo-wiki && git add -A && git commit -m \"add: "
        "hello\"\n"
        "$ cd .. && make serve WIKI_DIR=./demo-wiki\n"
        "# → page appears at http://localhost:7500/pages/hello"
    ): (
        "$ make wiki-init WIKI_DIR=./demo-wiki\n"
        "$ ls demo-wiki/\n"
        "content/   metadata/   raw/\n\n"
        "$ cat > demo-wiki/content/reference/hello.md <<'MD'\n"
        "---\n"
        "title: Hello\n"
        "slug: hello\n"
        "doc_type: reference\n"
        "status: published\n"
        "---\n\n"
        "# Hello\n\n"
        "This is a wiki page. It is also a file in a Git "
        "repository.\n"
        "MD\n\n"
        "$ cd demo-wiki && git add -A && git commit -m \"add: "
        "hello\"\n"
        "$ cd .. && make serve WIKI_DIR=./demo-wiki\n"
        "# → 页面会出现在 http://localhost:7500/pages/hello\n"
    ),
    (
        "Three observations, each the opposite of what a "
        "database-backed wiki offers:"
    ): (
        "三个观察，每一条都是“基于数据库的 wiki”提供的反面："
    ),
    (
        "The file `content/reference/hello.md` is authoritative. "
        "Delete it, restart the server, and the page is gone. "
        "There is no \"orphaned row\" state."
    ): (
        "文件 `content/reference/hello.md` 是**权威**。"
        "把它删掉、重启服务器，这一页就没了。"
        "不存在“孤儿行”那种状态。"
    ),
    (
        "The page's category (`reference`) is the parent "
        "directory. Move the file to `content/tutorials/`, and "
        "its category changes. No admin panel, no migration "
        "script."
    ): (
        "这一页的分类（ `reference` ）**就是它的父目录**。"
        "把文件挪到 `content/tutorials/` ，"
        "它的分类就变了。"
        "没有管理后台，没有迁移脚本。"
    ),
    (
        "The commit that introduced the page is the page's "
        "provenance. `git blame content/reference/hello.md` "
        "answers every \"who wrote this and when\" question "
        "without the wiki needing its own audit subsystem."
    ): (
        "**引入这一页的那个 commit，就是这一页的来源。** "
        "`git blame content/reference/hello.md` "
        "能回答所有“谁在什么时候写了这个”的问题，"
        "而 wiki 自己**根本不需要**一套审计子系统。"
    ),

    # ---- Competing approaches ----
    "System": "系统",
    "Storage": "存储",
    "Versioning": "版本化方式",
    "Fit for a software KB": "作为软件知识库的契合度",
    "DokuWiki {cite}`dokuwiki`": "DokuWiki {cite}`dokuwiki`",
    "one file per page on disk": "一页一文件，放在磁盘上",
    "in-tree `attic/` folder": "仓库内的 `attic/` 目录",
    "Good for ownership; weak on programmatic authoring.": (
        "所有权归属清晰；但在**可编程写作**上偏弱。"
    ),
    "MoinMoin {cite}`moinmoin`": "MoinMoin {cite}`moinmoin`",
    "per-page directories with revisions": "每一页一个目录，内带版本历史",
    "built-in": "内建",
    "Similar trade-offs to DokuWiki; heavier schema.": (
        "和 DokuWiki 折中取舍类似；schema 更重一些。"
    ),
    "Gitit {cite}`gitit`": "Gitit {cite}`gitit`",
    "Markdown files in a Git repo": "放在 Git 仓库里的 Markdown 文件",
    "Git itself": "Git 自己",
    "Direct ancestor of this design; dormant project.": (
        "本章这个设计的**直系祖先**；项目已停更。"
    ),
    "Obsidian {cite}`obsidian`": "Obsidian {cite}`obsidian`",
    "Markdown files in a \"vault\"": "放在一个“vault”里的 Markdown 文件",
    "user's choice of Git": "是否用 Git 由用户自己决定",
    "Excellent single-user tool; no server pipeline.": (
        "**单人用**极好的工具；没有服务端流水线。"
    ),
    "Notion / Confluence {cite}`notion_ai`": (
        "Notion / Confluence {cite}`notion_ai`"
    ),
    "proprietary database": "专有数据库",
    "internal audit log": "内部审计日志",
    "Great UI; poor alignment with a code repo.": (
        "UI 很好用；**与代码仓库的对齐度**很差。"
    ),
    (
        "The reference implementation occupies the Gitit + "
        "docs-as-code quadrant {cite}`docs_as_code`: plain "
        "files, Git-native, with the server providing pipelines, "
        "search, and RBAC *on top of* the filesystem rather than "
        "replacing it."
    ): (
        "本书的参考实现落在 "
        "**Gitit + docs-as-code** 这一象限 "
        "{cite}`docs_as_code` ："
        "纯文件、Git 原生，"
        "服务器**在文件系统之上**提供流水线、搜索和 RBAC，"
        "而**不是**去取代文件系统。"
    ),

    # ---- Common mistakes ----
    "Common mistakes, and when *not* to use a file-based wiki": (
        "常见错误，以及 *什么时候不要* 用基于文件的 wiki"
    ),
    (
        "\"Docs-as-code\" is not a universal answer, and the "
        "file-based model exposes its own failure modes once a "
        "team moves past the honeymoon period. Four failure "
        "patterns are worth naming because each one has a "
        "standard, wrong remedy that makes the situation worse:"
    ): (
        "“Docs-as-code”**不是**万金油。"
        "一个团队度过蜜月期之后，"
        "基于文件的模型也会**暴露出它自己的失败形态**。"
        "有四种失败模式值得专门点名，"
        "因为每一种都配有一个**标准的、错误的修法** —— "
        "那种修法只会让情况更糟："
    ),
    (
        "**Committing binary blobs into the content tree.** A "
        "screenshot goes in `_assets/`, and within a year "
        "someone commits a 40 MB PDF, then a 2 GB training "
        "dataset — \"just temporarily\". Clone times collapse, "
        "the `FileRepository.ReadPage` loop becomes I/O-bound on "
        "directory listings, and bisect becomes painful. The "
        "wrong fix is to split into a second repo \"for "
        "assets\"; the right fix is a *soft* gate in CI (reject "
        "files over some size threshold unless tagged) and Git "
        "LFS for the few blobs that legitimately belong in-tree. "
        "Keep this problem visible, not deferred."
    ): (
        "**把二进制大文件提交进内容目录里。** "
        "一张截图进了 `_assets/` ，"
        "不出一年就会有人往里提交一份 40 MB 的 PDF，"
        "再塞一份 2 GB 的训练数据 —— “就临时放一下”。"
        "克隆时间坍塌，"
        "`FileRepository.ReadPage` 的那个循环"
        "被目录列表的 I/O 拖成 I/O-bound，"
        "bisect 变成折磨。"
        "**错误的修法**是“再开一个专门装资产的仓库”；"
        "**正确的修法**是："
        "在 CI 里加一道 *软闸* "
        "（超过某个体积阈值的文件除非打了标签否则拒绝），"
        "并对那几份**真该放进仓库里的二进制**用 Git LFS。"
        "让这个问题**保持可见**，不要拖延。"
    ),
    (
        "**Treating slug renames as cheap.** Because the "
        "category is the directory path, moving a file changes "
        "its URL. In a content collection that is routinely "
        "cited by `file:line` from the code side of the KB (Part "
        "IV) or from external links, a slug rename silently "
        "breaks those references. The wrong fix is \"never "
        "rename\"; the right fix is a redirect map, stored in "
        "the repo, that the server reads on startup — and a CI "
        "check (Chapter 15) that refuses to publish a PR whose "
        "net effect is to break a URL still referenced from "
        "`content/` or from the code graph. The file-based "
        "model makes this check mechanical; proprietary wikis "
        "that renumber pages internally often cannot."
    ): (
        "**把 slug 重命名当成“很便宜”。** "
        "分类就是目录路径，"
        "所以**挪动一份文件就是改它的 URL** 。"
        "如果这份内容会被知识库代码侧（第四部分）"
        "或外部链接用 `file:line` 反复引用，"
        "那么 slug 重命名会**静默地**把这些引用全打断。"
        "**错误的修法**是“那就永远不要重命名”；"
        "**正确的修法**是：在仓库里维护一张重定向表，"
        "服务器启动时把它读进来 —— "
        "再加一道 CI 检查（第 15 章）："
        "任何一次 PR，"
        "只要它的净效果是打断一个仍然被 `content/` 或代码图谱引用着的 URL，"
        "就不许发布。"
        "基于文件的模型能让这个检查**机械化**；"
        "那些内部给页面重新编号的专有 wiki，"
        "通常做不到这一点。"
    ),
    (
        "**Merge-conflict storms on collaborative pages.** Two "
        "authors rewrite the same `runbook.md` in parallel, and "
        "Git's line-based merge produces a paragraph-level "
        "conflict the review UI cannot usefully display. A wiki "
        "UI with live cursors would dodge this; the file-based "
        "model cannot. The honest mitigation is to treat "
        "high-churn pages as *owned* — a single author, a short "
        "PR, and a rule that the second contributor rebases "
        "rather than merges. For pages that are genuinely "
        "multi-author in real time (incident timelines during an "
        "active outage), a file-based wiki is the wrong tool; "
        "use a shared doc for the duration of the event and "
        "import the result afterwards."
    ): (
        "**协作页面上的 merge 冲突风暴。** "
        "两个作者并行重写同一份 `runbook.md` ，"
        "Git 按行做的 merge 会产出**段级**的冲突，"
        "而评审 UI 根本显示不明白。"
        "带实时光标的 wiki UI 能躲开这种情况；"
        "基于文件的模型躲不开。"
        "**诚实的缓解办法**是："
        "把**高频改动的页面**当作 *有主* 的 —— "
        "一个作者、一份短 PR、"
        "外加一条“第二位贡献者 rebase、不 merge ”的规则。"
        "至于那些**真的需要多人实时共写的页面**"
        "（比如事故发生时正在写的时间线），"
        "基于文件的 wiki 就是错工具 —— "
        "在事件进行期间用一份共享文档，"
        "事后再把结果导进来。"
    ),
    (
        "**Over-indexing on the \"everything is a file\" "
        "aesthetic.** Revision history, access control, and "
        "search *can* all live in the filesystem, but not all "
        "of them *should*. Per-user history of which pages a "
        "reader has read, ephemeral draft autosaves, comment "
        "threads on published pages — these are operational "
        "data that change minute by minute and have no "
        "provenance value. Put them in a side database and "
        "resist the temptation to \"just use the filesystem for "
        "those too.\" The filesystem wins for content; it loses "
        "for mutable operational state."
    ): (
        "**过度迷恋“一切都是文件”那种美学。** "
        "版本历史、访问控制、搜索 *都能* 放进文件系统，"
        "但**并不都 *应该* 放**。"
        "每个读者读过哪些页的记录、"
        "短暂的草稿自动保存、"
        "已发布页面上的评论串 —— "
        "这些都是**分分钟变化**的**运维数据**，"
        "本身没有“来源”层面的价值。"
        "把它们放到一个旁挂数据库里，"
        "然后**抵抗住**“干脆连这些也塞文件系统”的诱惑。"
        "**文件系统赢在内容；输在可变的运维状态。**"
    ),
    (
        "A file-based wiki is also the wrong substrate for three "
        "kinds of content altogether. **Multi-thousand-editor "
        "public wikis** (the Wikipedia shape) need merge "
        "strategies no PR UI provides; **WYSIWYG-only teams** — "
        "writers who genuinely cannot and will not edit Markdown "
        "— need a different authoring surface with a sync "
        "pipeline to files; and **real-time collaborative "
        "editing** (Figma, Google Docs) is a product category "
        "file-based wikis have never served well. The question "
        "to ask before adopting the model is not *\"do we like "
        "Markdown?\"* but *\"can a pull request be the unit of "
        "doc review in our organisation?\"* If the answer is "
        "yes, Part II's four chapters apply directly. If the "
        "answer is no, this chapter's arguments still hold — "
        "they just apply to a different layer (e.g. an import "
        "pipeline from a proprietary wiki into a file-based "
        "mirror that the code graph can trust)."
    ): (
        "**基于文件的 wiki 对另外三类内容也根本不是对的承载。** "
        "**上万编辑者并发写的公共 wiki**（Wikipedia 这种形态）"
        "需要的 merge 策略 PR UI 提供不了；"
        "**只能用 WYSIWYG 的团队** —— "
        "那种**就是没法、也不会用 Markdown** 的作者 —— "
        "需要另一种写作界面、"
        "外加一条同步到文件的管线；"
        "**实时协作编辑**（Figma、Google Docs）"
        "则是基于文件的 wiki 从来没服务好过的**产品类别**。"
        "在采用这个模型前，"
        "你真正要问的问题**不是** *“我们喜不喜欢 Markdown？”* ，"
        "而是 *“pull request 能不能成为我们组织里**文档评审的基本单位**？”* "
        "如果答案是“能”，"
        "第二部分的四章直接适用。"
        "如果答案是“不能”，本章的论证**仍然**成立 —— "
        "只不过它应用的是另一层"
        "（比如从一个专有 wiki 导入到一个基于文件的镜像，"
        "再让代码图谱可以信任那个镜像的那条管线）。"
    ),

    # ---- Conclusion ----
    (
        "A file-based wiki is the right substrate for a software "
        "KB because it inherits the guarantees the software "
        "itself already needs: plain-text diffs, version "
        "control, review, CI. The `WikiRepository` interface and "
        "its `FileRepository` implementation show that the "
        "engineering cost of \"wiki as files\" is small — a "
        "handful of functions in a single Go file — while the "
        "payoff is that *every other layer* of the KB "
        "(frontmatter in Chapter 5, the pipeline in Chapter 6, "
        "publishing and search in Chapter 7, the code graph in "
        "Parts III–IV) can assume a stable, observable, "
        "diffable input."
    ): (
        "基于文件的 wiki 之所以是软件知识库的正确承载层，"
        "是因为它**继承**了软件本身早已需要的那些保障："
        "纯文本 diff、版本控制、评审、CI。"
        "`WikiRepository` 接口和它的 `FileRepository` 实现，"
        "说明“wiki 就是文件”这件事的工程代价很小 —— "
        "一份 Go 文件里几个函数 —— "
        "**回报却是**：知识库的 *每一层其他部分* "
        "（第 5 章的 frontmatter、"
        "第 6 章的流水线、"
        "第 7 章的发布与搜索、"
        "第三和第四部分的代码图谱）"
        "都可以假设自己拿到的输入是"
        "**稳定的、可观察的、可 diff 的**。"
    ),
    (
        "The next chapter turns to what lives *inside* those "
        "files: YAML frontmatter as an explicit provenance "
        "record, and why trust in a software KB begins at that "
        "boundary."
    ): (
        "下一章要讲的是这些文件 *里面* 装的是什么："
        "把 YAML frontmatter 当作一份显式的**来源记录**，"
        "以及为什么一个软件知识库的**信任**"
        "是从这条边界开始建立的。"
    ),

    # ---- Hook opening (between mindmap and ## Why) ----
    (
        "It is Monday morning, and three things have happened over "
        "the weekend. A senior engineer quit, taking with her the "
        "only account that could edit two pages on the company "
        "wiki. A sibling team's release notes were silently "
        "reverted when the wiki engine's background job \"resolved "
        "a conflict\" at 03:14. And someone is asking you, in a "
        "calendar invite for 10:00, whether you can \"just export "
        "the whole wiki\" so an AI agent can read it. The wiki has "
        "no export."
    ): (
        "周一早上，你发现周末发生了三件事。"
        "一位资深同事**上周五交了离职信**，"
        "而公司 wiki 上有两个页面，**只有她那个账号**能编辑。"
        "兄弟团队的 release notes，"
        "被 wiki 引擎的后台任务在凌晨 03:14 以“解决冲突”的名义"
        "**悄无声息地回滚了**。"
        "还有人给你发了一个 10:00 的日历邀请，"
        "问你能不能“**把整个 wiki 导出一下**”，"
        "好喂给一个 AI agent 去读 —— "
        "然而**这个 wiki 没有导出功能**。"
    ),
    (
        "Each of those problems is a symptom of the same decision "
        "— the decision to put the organisation's prose in a "
        "database you do not own. This chapter is about the "
        "opposite decision: a tree of Markdown files in Git, with "
        "the rest of the KB treating the filesystem as the "
        "authoritative surface. The payoff is not aesthetic; it is "
        "that every one of those Monday morning problems turns "
        "back into a problem you can *fix* rather than *escalate*."
    ): (
        "这三件事**都是同一个决定的症状** —— "
        "那个决定就是："
        "**把整个组织的文稿，放进一个你并不拥有的数据库里**。"
        "这一章要讲的是**另一个方向的决定**："
        "一棵放在 Git 里的 Markdown 文件树，"
        "然后让知识库的其他所有部分"
        "都把**文件系统**当作**权威的数据面**。"
        "这样做的回报**不是美学上的** —— "
        "而是：刚才那一个周一早上的每一个问题，"
        "都从一个需要 *向上升级* 的问题，"
        "变回了一个你可以 *自己修* 的问题。"
    ),

    # ---- Theory anchor "Why docs-as-code really works: review locality" ----
    "Why docs-as-code really works: review locality": (
        "docs-as-code 为什么真的有效：**评审 locality**"
    ),
    (
        "\"Docs-as-code\" is usually sold on its **tooling** "
        "virtues — Git, PRs, CI. Those are the *visible* wins. "
        "The *load-bearing* win is structural, and it takes two "
        "older ideas to see clearly."
    ): (
        "“docs-as-code”**被推销**的时候，卖的大多是它的**工具链好处**"
        "—— Git、PR、CI。这些是 *表面上看得见的* 胜利。"
        "而 *真正承重* 的那个胜利，是**结构性的**；"
        "要看清它，得借助两个**更老的想法**。"
    ),
    (
        "Conway's law {cite}`conway1968committees` says that a "
        "system's structure mirrors the communication structure "
        "of the team that built it. The corollary for "
        "documentation is usually phrased informally — \"docs "
        "mirror the org chart\" — but it is sharper than that. "
        "*Review* is a communication structure, and in every "
        "organisation without an explicit doc-review pipeline, "
        "the communication line for code review and the "
        "communication line for doc review are different. Code "
        "is reviewed by the engineers who commit to the repo; "
        "docs are reviewed, if at all, by whoever happens to "
        "open the wiki page. Those are different people, on "
        "different cadences, against different baselines. The "
        "drift between code and its documentation is not a "
        "discipline problem; it is a Conway-law problem — two "
        "communication structures producing two artefacts that "
        "were supposed to describe the same thing."
    ): (
        "**康威定律** {cite}`conway1968committees` 说："
        "**一个系统的结构**，会**镜像**"
        "构建它的那个团队的**沟通结构**。"
        "这个定律**套到文档上**，通常被**随口一说**成"
        "“**文档会镜像组织架构图**” —— 但其实它**比这更犀利**。"
        " *评审* 本身就是一种沟通结构；"
        "在**任何一个**没有显式文档评审流水线的组织里，"
        "**代码评审**的沟通线"
        "和**文档评审**的沟通线**不是同一条**。"
        "代码是**那些往仓库里提交的工程师**来评审的；"
        "文档 —— 如果有人评审的话 —— "
        "是**碰巧打开那个 wiki 页面的人**。"
        "这是**不同的人**，在**不同的节奏**上，"
        "对着**不同的基线**做出的判断。"
        "代码和它的文档之间那种**漂移** —— "
        "**不是纪律问题**，而是**康威定律问题**："
        "**两条沟通结构**在产出**两份制品**，"
        "而这两份制品**本应描述的是同一件事**。"
    ),
    (
        "Parnas's 1972 note on information hiding "
        "{cite}`parnas1972decomposition` gives the second "
        "lens. A system should be decomposed so that each "
        "module hides a design decision likely to change, and "
        "so that the interface to each module is stable even "
        "when the implementation is not. The docs-as-code move "
        "is a Parnas decomposition *across the prose/code "
        "boundary*: it forces prose and the code it describes "
        "into the same module — the same repo, the same PR, "
        "the same reviewer — so that *any* change that affects "
        "the interface the prose describes forces a diff the "
        "reviewer can see. Notion pages and their corresponding "
        "Go files are, in Parnas's sense, in different modules; "
        "`docs/auth.md` and `internal/auth/handler.go` in the "
        "same repo are not."
    ): (
        "**Parnas 在 1972 年关于信息隐藏的经典论文** "
        "{cite}`parnas1972decomposition` 提供了第二个视角。"
        "一个系统应该被**这样分解**："
        "**每个模块**都隐藏一个**很可能要变**的设计决策，"
        "并且**每个模块的接口**，"
        "即使在实现本身**不稳定**时，**也要稳定**。"
        "而 docs-as-code 这一步，"
        "**恰好就是**一次 Parnas 式的分解 —— "
        "**跨越** *文稿/代码* 的边界："
        "它把文稿和**它所描述的代码**，"
        "强行放进**同一个模块** —— "
        "**同一个仓库、同一个 PR、同一个评审人** —— "
        "这样 *任何一次* 影响到文稿所描述的那个接口的变更，"
        "都会**强制产出一个评审人能看到的 diff**。"
        "**Notion 页面**和**它对应的 Go 文件**"
        "—— 从 Parnas 的意义上讲 —— 是**两个模块**；"
        "而**同一个仓库里**的"
        "`docs/auth.md` 和 `internal/auth/handler.go` —— **不是**。"
    ),
    (
        "Those two lenses — Conway-law review locality and "
        "Parnas-style co-location — are *why* the "
        "engineering-cost argument for files over databases "
        "keeps winning in practice. The database-backed wiki is "
        "not wrong because files are elegant; it is wrong "
        "because it *guarantees* that the prose will be "
        "reviewed on a different communication line from the "
        "code, and Conway's law then guarantees that the two "
        "will drift. A file-based wiki does not eliminate drift "
        "— nothing does — but it re-aligns the two "
        "communication structures into one, and leaves the "
        "tooling (PR UIs, CI, blame) to exploit that alignment."
    ): (
        "这两个视角 —— **康威定律意义下的评审 locality**，"
        "和 **Parnas 意义下的共处一地**（co-location）—— "
        "就是 *为什么* “文件胜于数据库”这套**工程成本的论证**，"
        "在**实践中反复赢**。"
        "数据库型的 wiki **不是因为文件更优雅而错** —— "
        "它**错在**：它**保证了**"
        "文稿会被**在一条和代码评审不同的沟通线上**评审，"
        "然后**康威定律**会接着保证**两者必然漂移**。"
        "**基于文件的 wiki 并不能消除漂移** —— "
        "**没有任何东西能消除** —— "
        "但它能做一件事："
        "**把两条沟通结构重新对齐成同一条**，"
        "并让工具链（PR UI、CI、git blame）"
        "**去吃掉这次对齐带来的红利**。"
    ),
    (
        "Chapter 5 builds on this alignment by making the "
        "metadata explicit (frontmatter as contract); Chapter 6 "
        "builds on it by pushing classification into a pipeline "
        "the reviewer can audit; Chapters 14–16 (Part IV) "
        "exploit it for automated drift detection. All of those "
        "chapters presuppose the Conway-law realignment this "
        "section names. Without it, nothing downstream holds."
    ): (
        "第 5 章**依赖这次对齐**"
        "把元数据**显式化**（frontmatter 作为契约）；"
        "第 6 章**依赖这次对齐**"
        "把分类**推进到评审人可审计的流水线**里去；"
        "第 14–16 章（第四部分）"
        "则**利用这次对齐**做**自动化漂移检测**。"
        "这些后续章节，"
        "**全部预设**了本节所点明的**那次康威式再对齐**。"
        "没有它，**下游一切都站不住**。"
    ),
}
