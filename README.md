# Lazy Harness — Use AI to Build a Knowledge Base for a Software Project

> **Lazy harness** — do the *boring* scaffolding once, so the LLM-and-agent era
> doesn't catch you writing docs by hand.
>
> This repo holds the book *"Use AI to build a knowledge base for a software
> project"*: a six-part field guide to building, maintaining, and operating a
> project-level knowledge base that serves both humans and AI agents.

| | English | 中文 |
|---|---|---|
| Quickstart | [English ↓](#english-quickstart) | [中文 ↓](#中文-quickstart) |
| Source | `book/` | `book/`（MyST Markdown，zh 通过 gettext 翻译） |
| Build | `make build` | `make build` |
| Preview | `make serve` → http://localhost:8800 | `make serve` → http://localhost:8800 |

---

## What's inside

```
lazy-harness-book/
├── Makefile              # setup / check / build / serve / pdf / i18n
├── pyproject.toml        # Poetry: Sphinx, MyST, bibtex, mermaid, intl
├── poetry.lock
├── poetry.toml           # virtualenvs.in-project = true
└── book/
    ├── conf.py                       # Sphinx config (self-contained)
    ├── references.bib                # BibTeX, filtered per chapter
    ├── index.md                      # Book root
    ├── part0-presentation/           # 60-minute talk (index/outline/slides)
    ├── part1-foundations/            # What is a software KB; IR/RAG primer
    ├── part2-prose-layer/            # Markdown + Git wiki, frontmatter/footer
    ├── part3-code-layer/             # parse → embed → graph → retrieve
    ├── part4-operations-lifecycle/   # Incremental sync, drift, evaluation
    ├── part5-hybrid-layer/           # L0–L4 tuple, graph-guided context, MCP agents
    ├── part6-governance-and-outlook/ # Cost, privacy, security, open problems
    ├── appendix-*.md                 # Glossary, bilingual publishing, checklist
    ├── _tools/                       # check_frontmatter / check_blog_quotes / translate_*
    ├── _static/ _templates/          # CSS + language switcher
    ├── locale/zh_CN/LC_MESSAGES/     # gettext .po catalogs for zh
    ├── examples/ sources/            # Runnable snippets, vendored code excerpts
    └── appendix-a-example-wiki/ appendix-b-example-code-kg/
```

The book builds bilingually out of one source tree: **English is the source of
truth, zh_CN is maintained via `sphinx-intl` gettext catalogs under
`book/locale/zh_CN/LC_MESSAGES/`.** Both editions render from the same MyST
Markdown, the same mermaid diagrams, and the same BibTeX bibliography.

---

## Prerequisites

- **Python** 3.10+
- **Poetry** 1.8+ — the whole toolchain (Sphinx, MyST, bibtex, mermaid,
  intl) is declared in `pyproject.toml`.
- **ripgrep (`rg`)** — used by `make check-redaction` to scan for internal
  URL / product / ticket-key leaks before every HTML build.
- **(Optional) TeX Live / MacTeX** with `xelatex` + `xeCJK` — only needed for
  `make pdf`.

That's it. No Node, no Go, no databases. The book project is deliberately
kept to a minimal Python + Sphinx stack so it builds from a clean venv.

---

## English quickstart

```bash
# 1. Install the Sphinx toolchain (one-time)
make setup                  # → poetry install --no-root

# 2. Build both languages + landing page
make build                  # writes book/_build/html/{en,zh,index.html}

# 3. Preview locally
make serve                  # http://localhost:8800

# — or build just one language —
make html-en                # English only
make html-zh                # Chinese only (auto-compiles .po → .mo first)
```

### Day-to-day targets

| Target | What it does |
|:--|:--|
| `make check` | Validate frontmatter schema, blog-quote policy, PKB-skill non-copy policy. |
| `make check-redaction` | Scan `book/` for internal URLs, product names, Jira ticket keys, and the author's private project names. **Run before every commit.** |
| `make i18n` | Re-extract gettext strings → update `book/locale/zh_CN/LC_MESSAGES/*.po`. |
| `make intl-build` | Compile `.po` → `.mo` (required before `html-zh`; `html-zh` also runs it). |
| `make refresh-excerpts` | Re-capture vendored code excerpts with fresh commit SHAs. |
| `make check-excerpts` | Fail if any excerpt is out of date (used in CI). |
| `make pdf` | Build a single-volume PDF via xelatex. Requires a local TeX installation. |
| `make clean` | Remove `book/_build/`. |

All `book-*`-prefixed target names from the previous repo
(`book-build`, `book-check`, `book-serve`, …) still work as back-compat
aliases — see the bottom of the `Makefile`.

### Authoring rhythm

1.  Edit Markdown under `book/partN-*/`. Every page carries a frontmatter
    block (title, status, authors, `last_verified_commit`, `zh_status`,
    `keywords`) and a `<!-- PKB-metadata -->` footer (layer, `updated_by`,
    `review_status`, `review_score`, `commit`). See
    `book/appendix-e-bilingual-publishing.md` for the full schema.
2.  `make check` — fast local lint.
3.  `make html-en` — Sphinx builds with `-W --keep-going`; any reference or
    cross-link problem fails loudly.
4.  `make check-redaction` — catch any accidental leak of internal URLs /
    product names / ticket keys before pushing.
5.  `make i18n` — only when you've changed English; updates the zh_CN `.po`
    catalogs. Translate there, then `make html-zh` to preview.

---

## 中文 quickstart

```bash
# 1. 一次性安装 Sphinx 工具链
make setup                  # → poetry install --no-root

# 2. 构建双语 + 落地页
make build                  # 产出：book/_build/html/{en,zh,index.html}

# 3. 本地预览
make serve                  # http://localhost:8800

# — 或只构建某一语言 —
make html-en                # 英文
make html-zh                # 中文（会自动先把 .po 编译成 .mo）
```

### 常用 target

| Target | 作用 |
|:--|:--|
| `make check` | 校验 frontmatter、博客引用政策、PKB-skill 非复制政策 |
| `make check-redaction` | 扫描 `book/` 里**内部 URL / 产品名 / Jira ticket key / 作者私有项目名**是否泄漏。**每次提交前都应跑一遍** |
| `make i18n` | 重新提取 gettext 字符串 → 更新 `.po` |
| `make intl-build` | 把 `.po` 编译成 `.mo`（`html-zh` 会自动跑） |
| `make refresh-excerpts` | 重新抓取 vendored 代码片段，更新 commit SHA |
| `make check-excerpts` | 任何 excerpt 过期就失败（CI 用） |
| `make pdf` | xelatex 出 PDF，需要本地 TeX |
| `make clean` | 清理 `book/_build/` |

前一个 repo 用的 `book-*` 前缀的 target（`book-build`、`book-check`、
`book-serve`…）依然可用，作为兼容别名。

### 写作节奏

1.  在 `book/partN-*/` 下改 Markdown。每页都有 frontmatter
    （title / status / authors / `last_verified_commit` / `zh_status` /
    `keywords`）和 `<!-- PKB-metadata -->` footer
    （layer / `updated_by` / `review_status` / `review_score` / `commit`）。
    完整 schema 见 `book/appendix-e-bilingual-publishing.md`。
2.  `make check` —— 本地快速 lint。
3.  `make html-en` —— Sphinx 用 `-W --keep-going` 构建；任何交叉引用问题都
    会大声报错。
4.  `make check-redaction` —— 防止把内部 URL / 产品名 / 工单号推出去。
5.  `make i18n` —— 只有改了英文时才需要；会更新 zh_CN 的 `.po` 目录。翻译
    完后跑 `make html-zh` 预览。

---

## Design invariants（本书对自己的硬约束）

这六条每一条都是 `Makefile` 里的机械 gate，不是君子协定：

1.  **Frontmatter schema** —— 每一页都必须有 `status / authors /
    last_verified_commit / zh_status / keywords`。`make check` 挡住缺字段
    的页面。
2.  **No long verbatim blog copy** —— 作者博客内容可以引用一两句，但不允许
    整段复制粘贴。`check_blog_quotes.py` 负责扫描。
3.  **No PKB-skill copy** —— 作者的 skill 库内容不得搬运到书里。
    `check_pkb_quotes.py` 负责扫描。
4.  **No redaction leaks** —— 内部 URL、产品名、Jira 工单号、作者私有
    project 名字，一律不许出现在 `book/` 里。`check-redaction` 在每次
    `html-*` build 前跑。
5.  **Bilingual round-trip** —— 英文是 source of truth，中文必须通过 `.po`
    走。`html-zh` 不允许中文作为平行 Markdown 存在。
6.  **Per-chapter bibliography** —— 每章的 References 都用
    `:filter: keywords % "xxx"` 按关键字过滤 `references.bib`，不允许
    手写脚注。

---

## Project genealogy

这个 repo 是从 [`lazy-rabbit-wiki`](https://github.com/walterfan/lazy-rabbit-wiki)
抽离出来的独立项目。原仓库里 `book/` 太大，跟 wiki-cli（Go 后端 + Vue 前端）
放一起显得不伦不类；抽出来后各自职责清晰：

- **`lazy-rabbit-wiki`** —— *Prose layer* 的参考实现：Go wiki-cli + Vue 前端，
  处理 Markdown + Git 型 wiki 的导入、校验、静态构建。
- **`lazy-harness-book`**（本仓库）—— 设计笔记与教程的**文本载体**：
  把"用 AI 给软件项目造知识库"这件事的方法论、trade-off、工程纪律
  系统写下来。

原仓库下的 `book/` 现在是一个指向本 repo 的 symlink —— 历史构建命令
（`make book-build` 等）在原仓库里仍然可用，但真正的内容维护发生在这里。

## License

Content: **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
Code snippets (Makefile, `_tools/*.py`): **MIT**.
