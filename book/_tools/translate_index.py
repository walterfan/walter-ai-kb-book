"""Apply Chinese translations for the top-level book index (book/index.md).

Run with: poetry run python book/_tools/translate_index.py

Style guide inherited from Part III translation batches:
  - English kept for: CLI names, file paths, variable names, `{cite}` keys.
  - Keep **bold** markup and `code spans` exactly as English.
  - Technical identifiers (Sphinx, MyST, sphinx-intl, CC-BY-NC-ND) stay English.
  - CommonMark emphasis around *...* adjacent to CJK needs ASCII spaces.
"""

from __future__ import annotations

import os
import sys
import polib

PO_PATH = "book/locale/zh_CN/LC_MESSAGES/index.po"


TRANSLATIONS: dict[str, str] = {
    # Part captions in the toctree
    "Part I — Foundations": "第一部分 —— 基础",
    "Part II — The Prose Layer": "第二部分 —— 文稿层",
    "Part III — The Code Layer": "第三部分 —— 代码层",
    "Part IV — Operations & Lifecycle": "第四部分 —— 运维与生命周期",
    "Part V — The Hybrid Layer": "第五部分 —— 混合层",
    "Part VI — Governance & Outlook": "第六部分 —— 治理与展望",
    "Appendices": "附录",

    # Title + subtitle / epigraph
    "Use AI to build a knowledge base for a software project":
        "用 AI 为软件项目构建知识库",

    "A practitioner's field manual that blends IR / RAG theory with live, measured code from two reference implementations — a prose-layer reference implementation and a code-layer reference implementation — and expands the author's methodology blog post {cite}`fanyamin2026deepwiki` into a book-length treatment.":
        "一份实战者的现场手册：把 IR / RAG 理论与两套参考实现 —— 文稿层参考实现和代码层参考实现 —— 中真正在跑、可被度量的代码结合起来，并把作者那篇方法论博客 {cite}`fanyamin2026deepwiki` 扩展成一本书的篇幅。",

    # "How to read this book"
    "How to read this book": "如何阅读本书",

    "Each Part follows the same six-section narrative arc:":
        "每一部分都沿着同一条六段式叙事弧展开：",

    "**Why** — the problem, the cost of ignoring it, a short literature survey.":
        "**Why** —— 问题是什么、忽视它要付出的代价，以及一段简短的文献综述。",

    "**What** — the precise definitions, the data model, the scope boundaries.":
        "**What** —— 精确的定义、数据模型、以及范围的边界。",

    "**How** — the methodology, the architecture, the code that actually runs.":
        "**How** —— 方法论、架构，以及真正在跑的代码。",

    "**Example** — an end-to-end recipe with commands, inputs, and expected output.":
        "**Example** —— 一条端到端的操作配方，包括命令、输入和预期输出。",

    "**Conclusion** — what we learned, what's still open, when to apply it.":
        "**Conclusion** —— 我们学到了什么、什么仍然是开放问题、什么时候适合把它用上。",

    "**References** — every citation used in that Part, rendered from the shared `references.bib`.":
        "**References** —— 该部分用到的每一条引用，由共享的 `references.bib` 渲染而来。",

    "Every chapter repeats the arc in miniature. You can read the book linearly, or you can dip straight into a single Part — each one stands on its own.":
        "每一章都会以小型化的方式重复这条叙事弧。你可以线性地读完整本书，也可以直接挑某一部分进去看 —— 每一部分都可以独立成立。",

    # "Sources"
    "Sources": "来源",

    "This book draws on three primary sources:": "本书基于三个主要来源：",

    "**The prose-layer reference implementation** — a file-based wiki engine that backs this book's prose-layer narrative.":
        "**文稿层参考实现** —— 一个基于文件的 wiki 引擎，支撑本书文稿层的叙事。",

    "**The code-layer reference implementation** — the companion Code-RAG + Knowledge-Graph engine that backs Part III.":
        "**代码层参考实现** —— 与之配套的 Code-RAG + 知识图谱引擎，支撑本书第三部分。",

    "**Blog post** *给代码仓库造一个 DeepWiki* {cite}`fanyamin2026deepwiki` — the author's pre-existing methodology article, used as the book's narrative spine. See `sources/blog-deepwiki-methodology/` for the vendored snapshot and the non-copy policy (every chapter that cites the blog adds at least one new citation, one code excerpt, and one measurement the blog did not report).":
        "**博客文章** * 给代码仓库造一个 DeepWiki * {cite}`fanyamin2026deepwiki` —— 作者此前已发表的一篇方法论文章，作为全书的叙事主干。关于 vendored 快照和“非抄录”策略，见 `sources/blog-deepwiki-methodology/`（每一章在引用博客时，都必须至少新增一条引用、一段代码摘录，以及一项博客里没有报告过的度量）。",

    # "Relationship to the blog post"
    "Relationship to the blog post": "与博客文章的关系",

    "The blog post is licensed CC-BY-NC-ND 4.0. The author holds the copyright, but we preserve the ND (no-derivatives) signal for downstream readers by:":
        "该博客采用 CC-BY-NC-ND 4.0 许可。作者持有版权；为了对下游读者保留 ND（no-derivatives，禁止演绎）的信号，我们做了以下三件事：",

    "Vendoring the blog HTML as an **immutable** snapshot under `sources/blog-deepwiki-methodology/snapshot.html`.":
        "把博客 HTML 以 **不可变** 快照的形式 vendor 在 `sources/blog-deepwiki-methodology/snapshot.html`。",

    "Paraphrasing and expanding the arguments in the author's own words.":
        "以作者自己的话，对其中的论点进行改写与扩展。",

    "Fencing any short verbatim quote inside an `{epigraph}` block with a `{cite}` to `fanyamin2026deepwiki`.":
        "任何短小的原文引用都要放进 `{epigraph}` 块中，并附上指向 `fanyamin2026deepwiki` 的 `{cite}`。",

    "A pre-build validator (`_tools/check_blog_quotes.py`) enforces rule (3) at build time.":
        "一个预构建校验器（`_tools/check_blog_quotes.py`）在构建时对第 (3) 条规则做强制检查。",

    # "How to cite this book"
    "How to cite this book": "如何引用本书",

    # "Table of contents"
    "Table of contents": "目录",

    # "Colophon"
    "Colophon": "版本说明",

    "Built with **Sphinx + MyST** using `sphinx-rtd-theme`, `sphinxcontrib-bibtex`, and `sphinxcontrib-mermaid`. Chinese translations are maintained with `sphinx-intl` under `locale/zh_CN/LC_MESSAGES/`.":
        "使用 **Sphinx + MyST** 构建，主题为 `sphinx-rtd-theme`，扩展为 `sphinxcontrib-bibtex` 与 `sphinxcontrib-mermaid`。中文翻译由 `sphinx-intl` 维护，文件位于 `locale/zh_CN/LC_MESSAGES/`。",

    "Build locally:": "本地构建：",
}


def main() -> int:
    if not os.path.exists(PO_PATH):
        print(f"FAIL: {PO_PATH} not found", file=sys.stderr)
        return 1
    po = polib.pofile(PO_PATH)
    applied = 0
    po_msgids = {e.msgid for e in po}
    unmatched = [k for k in TRANSLATIONS if k not in po_msgids]
    for e in po:
        if e.msgid in TRANSLATIONS:
            e.msgstr = TRANSLATIONS[e.msgid]
            if "fuzzy" in e.flags:
                e.flags.remove("fuzzy")
            applied += 1
    po.save(PO_PATH)
    remaining = len(po.untranslated_entries()) + len(po.fuzzy_entries())
    print(f"index.po  applied={applied:3d}  remaining_untranslated={remaining:3d}  unmatched_keys={len(unmatched)}")
    for key in unmatched:
        print(f"   UNMATCHED: {key[:80]!r}")
    return 0 if not unmatched else 1


if __name__ == "__main__":
    sys.exit(main())
