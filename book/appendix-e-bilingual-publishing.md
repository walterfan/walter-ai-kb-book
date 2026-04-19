---
title: 'Appendix E — Publishing a Bilingual Knowledge Base'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - appendix
  - i18n
  - sphinx
---

# Appendix E — Publishing a Bilingual Knowledge Base

> Scope. This appendix is deliberately document-only and
> self-contained. It describes the bilingual publishing discipline
> the author has refined in a private project-knowledge-base toolkit
> {cite}`fanyamin_pkb_skill` and adapts it to the `sphinx + myst`
> toolchain this book is built with. It does not wire new `make`
> targets; use the existing `make book-i18n` / `make book-build`
> targets from this book's Makefile.

## Why publish bilingually

A knowledge base written in only the author's first language excludes
readers who are fluent in their second or third language but cannot
read the first at professional depth. A KB written in only English
excludes the large fraction of a Chinese-speaking engineering team
that prefers Chinese for technical depth (and vice versa). The
choice is not *which* language but *which discipline for keeping two
languages in sync without doubling the authoring cost*.

Three failure modes make this harder than it looks:

1.  **Translation drift.** An English page is updated; the Chinese
    translation is not. The Chinese reader sees a stale page that
    looks current.
2.  **Anchor drift.** An English H2 heading is reworded; the
    Chinese translation still carries the old anchor. Cross-document
    links break silently.
3.  **Source-of-truth drift.** Two parallel prose files exist; each
    gets edited independently; the two languages diverge in content,
    not just in wording.

The Sphinx toolchain plus a small amount of discipline addresses all
three.

## What the bilingual pipeline looks like

One source language, multiple translation targets, one build per
language:

```text
book/                            <- single source of truth (English)
  ch07a-prose-operational-model.md
  ...
  locale/
    zh_CN/
      LC_MESSAGES/
        ch07a-prose-operational-model.po  <- Chinese translation
        ...
```

The `.po` files are gettext message catalogues. Each catalogue entry
pairs one English string (the `msgid`) with one translated string
(the `msgstr`). Sphinx extracts the `msgid`s at build time; a
translator (human or machine) fills in the `msgstr`s; Sphinx
re-renders HTML for each target language from the same source.

The English prose remains the source of truth. The Chinese pages are
*rendered*, not maintained. This is the critical move: a KB with two
equal sources becomes a KB with two sources of drift.

## How to make it reliable

Four pieces of discipline, each cheap:

### 1. Turn on `gettext_uuid`

Without UUIDs, every translation entry is keyed by the English
string itself. Reword "The retrieval layer consults the tuple" to
"The retriever reads the tuple," and the translation becomes
orphaned: the old entry points at prose that no longer exists; the
new entry has no translation. The translator must re-translate
from scratch.

With `gettext_uuid = True` in `conf.py`, each entry gets a stable
UUID the first time it appears. Rewording the English leaves the
UUID intact; the Chinese translation follows the UUID, not the
string. In `conf.py`:

```python
gettext_uuid = True
gettext_compact = False   # one .pot per source file
gettext_additional_targets = ["literal-block", "image"]
```

The result: an English edit that preserves meaning preserves its
translation.

### 2. Keep `.po` edits mechanical

Editing `.po` files by hand is tedious and error-prone (a stray
quote breaks the file). Use `polib` for programmatic edits:

```python
import polib

po = polib.pofile("locale/zh_CN/LC_MESSAGES/ch07a-prose-operational-model.po")

for entry in po.untranslated_entries():
    if should_auto_translate(entry.msgid):
        entry.msgstr = call_llm_translator(entry.msgid)
        entry.flags.append("fuzzy")  # mark for review; never silently approve

po.save()
```

Two rules make this safe:

- **Every machine translation lands as `fuzzy`.** This is the
  gettext convention: a fuzzy entry is shown to the reader
  untranslated (or as the English fallback) until a human reviews
  and removes the flag. It mirrors the "AI always sets pending"
  rule from Chapter 5 for frontmatter footers.
- **Never delete a translated entry because its `msgid` changed.**
  Let `sphinx-intl update` handle it; the updater marks entries
  `fuzzy` when the English string has drifted, which preserves
  prior work and signals review.

### 3. Translate H1s through a hook

Sphinx's default behaviour renders the document title from the
frontmatter `title:` field, which is English. For Chinese output
the reader expects a Chinese title. A small `conf.py` hook handles
this without duplicating prose:

```python
def translate_h1(app, docname, source):
    """Replace the frontmatter title with the zh_CN translation when
    building for zh_CN, so the navigation sidebar shows Chinese titles.
    """
    if app.config.language != "zh_CN":
        return
    translations = load_h1_map(docname)   # tiny YAML: path -> zh_CN title
    if docname in translations:
        source[0] = re.sub(
            r"^title:\s*.+$",
            f"title: '{translations[docname]}'",
            source[0],
            count=1,
            flags=re.MULTILINE,
        )

def setup(app):
    app.connect("source-read", translate_h1)
```

The `h1_map.zh_CN.yml` is a small flat file the author maintains
alongside the prose:

```yaml
ch07a-prose-operational-model: 第 7a 章 — 文章层的运维模型
ch14-incremental-sync: 第 14 章 — 增量同步
ch15-evaluation-and-benchmarks: 第 15 章 — 评估、基准与发布闸门
```

This is more work than letting `.po` catalogues carry the titles,
but it produces a navigation sidebar that reads natively in each
language — which is the first thing a reader notices.

### 4. Fail the build on untranslated critical pages

Not every chapter needs same-day Chinese. Runbooks do; an overview
chapter might lag by a week. Encode this in the frontmatter:

```yaml
---
title: 'Chapter 16 — Maintenance, Drift, and Link Rot'
zh_status: required   # required | optional | none
---
```

A one-line check at build time enforces the policy:

```python
# book/_tools/check_zh_status.py  (sketch)
for doc in all_docs:
    if doc.frontmatter.get("zh_status") == "required":
        po_path = f"locale/zh_CN/LC_MESSAGES/{doc.path}.po"
        if not po_path.exists() or po_untranslated_fraction(po_path) > 0.05:
            fail(f"{doc.path}: zh_CN translation required but missing or <95% complete")
```

Three values — `required`, `optional`, `none` — give every page an
explicit translation SLA. Operationally this mirrors the hard/soft
gate split from Chapter 15: `required` is a hard gate that blocks
publish; `optional` is a soft warning; `none` is silent.

## Example — one page through the pipeline

The lifecycle of `ch07a-prose-operational-model.md` through one
editing round:

1.  Author edits the English source. Reword a section heading.
2.  `make book-i18n` runs `sphinx-build -b gettext` + `sphinx-intl
    update`. The UUID of the reworded heading is preserved; its
    Chinese translation is now marked `fuzzy`.
3.  `make book-build` builds English. Build succeeds; `zh_status` is
    `optional` on this chapter, so the build does not fail on the
    fuzzy entry.
4.  A bounded-LLM translation pass (analogous to Chapter 16's L2)
    generates a new `msgstr` for the reworded heading and writes it
    back with the `fuzzy` flag retained.
5.  A human reviewer opens the `.po` file in a PO-aware editor
    (Poedit, Lokalize), reads the new Chinese text against the
    English, and removes the `fuzzy` flag.
6.  Next `make book-build -D language=zh_CN` produces the Chinese
    HTML with the approved translation in place.

Six steps, three of which are mechanical (`make` targets), two of
which are bounded LLM work (one translation call per changed entry),
and one of which is human review on a single diff. The total cost
per English edit is cents of LLM tokens plus a minute of human time
per chapter.

## Operational failure modes and fixes

| Failure | Symptom | Fix |
|:--|:--|:--|
| UUID disabled retroactively | Mass re-translation after a casual edit | Turn on `gettext_uuid` *before* first translation pass; once on, leave it on. |
| `.po` edited by hand, syntax broken | Sphinx fails with "malformed entry near line N" | Always edit via `polib`; keep a pre-commit hook that runs `msgfmt --check` on every `.po` file. |
| Translation lags English indefinitely | Chinese readers see stale prose with no warning | `zh_status: required` on critical pages; CI hard-fails when the coverage drops below threshold. |
| Translator translates the prose but not the heading | Nav sidebar is half-Chinese, half-English | Maintain `h1_map.zh_CN.yml` and gate CI on its completeness for any chapter whose `zh_status` is `required`. |
| Machine translation silently approved | Chinese reader sees nonsense | Every machine-translated `msgstr` lands as `fuzzy`; the `fuzzy` flag must be cleared by a human. |

Each of these is a one-line rule; the appendix's point is that they
are not optional if the bilingual publishing is to stay trustworthy.

## Keep it simple

The full discipline above fits comfortably in a few hundred lines
of configuration, a small `h1_map` file per language, and a one-line
check. It does not require a translation management system, a
separate content repository, or a parallel prose tree. It does
require the four disciplines above to be in place from the first
day of bilingual publishing — the failure modes all become
expensive to fix retroactively.

The rest is routine Sphinx workflow: `make book-i18n` to refresh,
`make book-build -D language=zh_CN` to render, CI to enforce the
`zh_status` hard gate. Nothing in this appendix needs new tooling;
everything needs the disciplines to be named and enforced.

## References

```{bibliography}
:filter: keywords % "appendix" or keywords % "i18n" or keywords % "sphinx" or keywords % "self-citation"
```
