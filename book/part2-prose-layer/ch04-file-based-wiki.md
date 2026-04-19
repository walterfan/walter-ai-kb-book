---
title: "Chapter 4 — A File-based Wiki"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - prose-layer
  - file-based
  - competing-tools
---

# Chapter 4 — A File-based Wiki

This chapter on one page — the storage choice that every later
prose-layer chapter takes for granted, the Git-as-infrastructure
payoff it unlocks, the tiny Go interface that hides the filesystem
from the rest of the codebase, and the failure modes file-based
wikis actually exhibit in the wild:

```{mermaid}
mindmap
  root((File-based wiki))
    Why
      Provenance (git blame)
      Review (PR-diffable)
      Automation (pipelines)
      Longevity (plain text)
    What
      content/ (pages)
      metadata/ (schema, config)
      raw/ (staging)
      _assets/ (binaries)
    How
      WikiRepository interface
      FileRepository (5 methods)
      In-memory rebuild on boot
      No DB, no cache invalidation
    Git gets you
      Revision history
      Blame
      Diff, review, rollback
      Branching, offline edit
    Failure modes
      Binary blobs in tree
      Merge-conflict storms
      Slug rename churn
      Large repo clone time
    Not the right fit
      Multi-thousand concurrent editors
      WYSIWYG-only authors
      Realtime collaboration (Figma-like)
```

It is Monday morning, and three things have happened over the
weekend. A senior engineer quit, taking with her the only account
that could edit two pages on the company wiki. A sibling team's
release notes were silently reverted when the wiki engine's
background job "resolved a conflict" at 03:14. And someone is asking
you, in a calendar invite for 10:00, whether you can "just export
the whole wiki" so an AI agent can read it. The wiki has no export.

Each of those problems is a symptom of the same decision — the
decision to put the organisation's prose in a database you do not
own. This chapter is about the opposite decision: a tree of
Markdown files in Git, with the rest of the KB treating the
filesystem as the authoritative surface. The payoff is not
aesthetic; it is that every one of those Monday morning problems
turns back into a problem you can *fix* rather than
*escalate*.

## Why

Part I argued that a software KB should behave like code: versioned,
reviewable, diffable, automatable. Chapter 3 narrowed the prose layer to
four Diátaxis genres. This chapter answers the next question: *where does
that prose physically live?*

Database-backed wikis optimise for editing. They give you live rendering,
concurrent sessions, WYSIWYG toolbars, and revision history — at the cost
of pulling every document into an opaque table whose schema you do not
own {cite}`notion_ai,obsidian`. Three things break when you do that:

1.  **Provenance.** "Who wrote this paragraph, under which commit of the
    code?" becomes a database query against a proprietary audit log,
    instead of `git blame` on a Markdown file.
2.  **Review.** A pull request can show a code change and a doc change
    side by side *only if* the doc is a file in the same repo. Otherwise
    the review splits across two systems and drifts apart
    {cite}`gruver2016starting,docs_as_code`.
3.  **Automation.** The `init → import → verify → build → serve` pipeline
    that Part II is about needs an input it can read, write, diff, and
    version. A file is all of those; a database row is none of them.

So the prose-layer reference implementation this book uses is a tree
of plain Markdown files under `content/`, one page per file, governed
by the same Git repository as the code that describes the software.
The wiki *is* the repo {cite}`gitit,dokuwiki,moinmoin`.

## What

Concretely, an instance of the prose-layer reference implementation is
a directory with four conventions:

```
wiki-root/
├── content/              # Markdown files, one per page
│   ├── getting-started/
│   │   └── install.md
│   ├── reference/
│   │   └── api.md
│   └── _assets/          # images, downloaded binaries
├── metadata/
│   ├── SCHEMA.md         # frontmatter contract (see ch05)
│   ├── wiki.yaml         # instance config
│   ├── users.yaml        # auth
│   └── _sphinx/          # publishing toolchain
└── raw/                  # staging area for unprocessed imports
```

Every page is a Markdown file with a YAML frontmatter block. Every
category is a directory. Underscore-prefixed directories
(`_assets/`, `_sphinx/`) are reserved for infrastructure and are invisible
to readers. The wiki has no database, no object store, no hidden index:
everything observable is a file you can `cat`, `grep`, or `git log`
against.

The code that enforces this lives in `backend/internal/wiki/`. Two files
carry the weight:

- `repository.go` — the file-system I/O boundary.
- `service.go` — the read-side API, backed entirely by that repository
  and an in-memory index.

## How

### The repository interface

The `WikiRepository` interface is the only place in the backend that
touches the filesystem for page content. Everything above it — services,
HTTP handlers, the CLI — operates on `*Page` values and never calls
`os.ReadFile` directly. This is a classic ports-and-adapters layering,
and it means a future Git-aware or S3-backed repository can drop in
without touching any of the business logic.

```{literalinclude} ../examples/part2-prose-layer/ch04/repository.go
:language: go
:lines: 10-16
:caption: The full repository interface, five methods.
```

Notice what is *not* on this interface: no "update", no "lock", no
"transaction". A file-based wiki replaces those with
`git commit`. Writes are last-write-wins at the filesystem level; if you
want review gates, you get them from the repo hosting platform, not
from the wiki engine itself.

### Reading a page is parsing a file

`ReadPage` is the canonical path from bytes on disk to a `*Page` value:

```{literalinclude} ../examples/part2-prose-layer/ch04/repository.go
:language: go
:lines: 26-53
:caption: `FileRepository.ReadPage` — read, split, parse, derive.
```

Four steps, all local, all deterministic:

1.  **Read.** `os.ReadFile` lifts the bytes.
2.  **Split.** `ParseFrontmatter` separates the YAML header from the body
    (Chapter 5 covers the format).
3.  **Recover.** If there is no frontmatter, `InferFrontmatter` synthesises
    a minimal one from the filename and mtime. A page without metadata
    still round-trips.
4.  **Derive.** `DeriveCategory` computes the category from the file's
    path relative to `ContentDir`. The directory structure *is* the
    category hierarchy; there is no separate "tag table".

`ListFiles` codifies one more filesystem convention:

```{literalinclude} ../examples/part2-prose-layer/ch04/repository.go
:language: go
:lines: 79-103
:caption: `ListFiles` — walk the tree, skipping reserved names.
```

Directories whose names start with `_` are skipped (reserved for
infrastructure), and `_category.md` files are hidden from normal page
listings because they describe a directory rather than being a page in
their own right. Two tiny conventions carry all the weight of "what
counts as a wiki page".

### The service is a thin shell around the repository

`WikiService` layers an index, a renderer, and filter/pagination on top
of the repository, but its constructor is a dependency list, not a
database connection:

```{literalinclude} ../examples/part2-prose-layer/ch04/service.go
:language: go
:lines: 32-47
:caption: `WikiService` — three dependencies, no driver.
```

On startup, the service asks the repository for every Markdown file
under `ContentDir`, reads each into a `*Page`, and hands the whole list
to the index for a full rebuild:

```{literalinclude} ../examples/part2-prose-layer/ch04/service.go
:language: go
:lines: 57-73
:caption: `LoadAndIndex` — walk the tree, parse each file, rebuild the index from scratch.
```

This is deliberately simple. There is no incremental index, no
change-data-capture, no cache invalidation strategy. A full rescan on
boot is fast enough for tens of thousands of pages (the walk is I/O-
bound, not CPU-bound), and it eliminates an entire class of "index is
out of sync with disk" bugs that plague database-backed wikis. When you
edit a file with `vim` outside the server, `LoadAndIndex` on the next
restart will see it. When the index engine pushes a page in response to
a write, it stays in sync because there is only one writer — the
service. The filesystem is the source of truth; everything else is a
derived cache.

### What Git gets you for free

Because the content directory is a Git working tree, a great deal of
behaviour that a wiki usually has to implement itself comes from the
surrounding platform:

| Feature | Wiki engines typically ship | The file-based model delegates to |
|---------|------------------------------|-----------------------------------|
| Revision history | Custom page_revisions table | `git log` |
| Blame | Custom author field per paragraph | `git blame` |
| Diff/review | In-app diff viewer | GitHub/GitLab PR UI |
| Rollback | Custom restore endpoint | `git revert` |
| Branching | Usually absent | Native |
| Offline edit | Proprietary sync client | `git pull` / `git push` |

This is the docs-as-code bargain made concrete {cite}`gruver2016starting,docs_as_code`:
the wiki gives up "slick in-browser edit" and gains the entire Git
ecosystem. Chapter 10 will show why that bargain is decisive for the
graph layer too — a code KB that can point at a commit SHA becomes a
completely different thing from one that can only point at "the current
state of some database".

### Why docs-as-code really works: review locality

"Docs-as-code" is usually sold on its **tooling** virtues — Git,
PRs, CI. Those are the *visible* wins. The *load-bearing* win is
structural, and it takes two older ideas to see clearly.

Conway's law {cite}`conway1968committees` says that a system's
structure mirrors the communication structure of the team that
built it. The corollary for documentation is usually phrased
informally — "docs mirror the org chart" — but it is sharper than
that. *Review* is a communication structure, and in every
organisation without an explicit doc-review pipeline, the
communication line for code review and the communication line for
doc review are different. Code is reviewed by the engineers who
commit to the repo; docs are reviewed, if at all, by whoever
happens to open the wiki page. Those are different people, on
different cadences, against different baselines. The drift between
code and its documentation is not a discipline problem; it is a
Conway-law problem — two communication structures producing two
artefacts that were supposed to describe the same thing.

Parnas's 1972 note on information hiding {cite}`parnas1972decomposition`
gives the second lens. A system should be decomposed so that each
module hides a design decision likely to change, and so that the
interface to each module is stable even when the implementation is
not. The docs-as-code move is a Parnas decomposition *across the
prose/code boundary*: it forces prose and the code it describes
into the same module — the same repo, the same PR, the same
reviewer — so that *any* change that affects the interface the
prose describes forces a diff the reviewer can see. Notion pages
and their corresponding Go files are, in Parnas's sense, in
different modules; `docs/auth.md` and `internal/auth/handler.go`
in the same repo are not.

Those two lenses — Conway-law review locality and Parnas-style
co-location — are *why* the engineering-cost argument for files
over databases keeps winning in practice. The database-backed
wiki is not wrong because files are elegant; it is wrong because
it *guarantees* that the prose will be reviewed on a different
communication line from the code, and Conway's law then
guarantees that the two will drift. A file-based wiki does not
eliminate drift — nothing does — but it re-aligns the two
communication structures into one, and leaves the tooling (PR
UIs, CI, blame) to exploit that alignment.

Chapter 5 builds on this alignment by making the metadata explicit
(frontmatter as contract); Chapter 6 builds on it by pushing
classification into a pipeline the reviewer can audit; Chapters
14–16 (Part IV) exploit it for automated drift detection. All of
those chapters presuppose the Conway-law realignment this section
names. Without it, nothing downstream holds.

## Example

Here is the smallest end-to-end round-trip, enough to prove the model
works. (The full walkthrough is in Appendix A.)

```bash
$ make wiki-init WIKI_DIR=./demo-wiki
$ ls demo-wiki/
content/   metadata/   raw/

$ cat > demo-wiki/content/reference/hello.md <<'MD'
---
title: Hello
slug: hello
doc_type: reference
status: published
---

# Hello

This is a wiki page. It is also a file in a Git repository.
MD

$ cd demo-wiki && git add -A && git commit -m "add: hello"
$ cd .. && make serve WIKI_DIR=./demo-wiki
# → page appears at http://localhost:7500/pages/hello
```

Three observations, each the opposite of what a database-backed wiki
offers:

1.  The file `content/reference/hello.md` is authoritative. Delete it,
    restart the server, and the page is gone. There is no "orphaned
    row" state.
2.  The page's category (`reference`) is the parent directory. Move the
    file to `content/tutorials/`, and its category changes. No admin
    panel, no migration script.
3.  The commit that introduced the page is the page's provenance.
    `git blame content/reference/hello.md` answers every "who wrote this
    and when" question without the wiki needing its own audit subsystem.

## Competing approaches

| System | Storage | Versioning | Fit for a software KB |
|--------|---------|------------|-----------------------|
| DokuWiki {cite}`dokuwiki` | one file per page on disk | in-tree `attic/` folder | Good for ownership; weak on programmatic authoring. |
| MoinMoin {cite}`moinmoin` | per-page directories with revisions | built-in | Similar trade-offs to DokuWiki; heavier schema. |
| Gitit {cite}`gitit` | Markdown files in a Git repo | Git itself | Direct ancestor of this design; dormant project. |
| Obsidian {cite}`obsidian` | Markdown files in a "vault" | user's choice of Git | Excellent single-user tool; no server pipeline. |
| Notion / Confluence {cite}`notion_ai` | proprietary database | internal audit log | Great UI; poor alignment with a code repo. |

The reference implementation occupies the Gitit + docs-as-code
quadrant {cite}`docs_as_code`: plain files, Git-native, with the
server providing pipelines, search, and RBAC *on top of* the
filesystem rather than replacing it.

## Common mistakes, and when *not* to use a file-based wiki

"Docs-as-code" is not a universal answer, and the file-based model
exposes its own failure modes once a team moves past the honeymoon
period. Four failure patterns are worth naming because each one has
a standard, wrong remedy that makes the situation worse:

1.  **Committing binary blobs into the content tree.** A screenshot
    goes in `_assets/`, and within a year someone commits a 40 MB
    PDF, then a 2 GB training dataset — "just temporarily". Clone
    times collapse, the `FileRepository.ReadPage` loop becomes
    I/O-bound on directory listings, and bisect becomes painful. The
    wrong fix is to split into a second repo "for assets"; the right
    fix is a *soft* gate in CI (reject files over some size
    threshold unless tagged) and Git LFS for the few blobs that
    legitimately belong in-tree. Keep this problem visible, not
    deferred.

2.  **Treating slug renames as cheap.** Because the category is the
    directory path, moving a file changes its URL. In a content
    collection that is routinely cited by `file:line` from the code
    side of the KB (Part IV) or from external links, a slug rename
    silently breaks those references. The wrong fix is "never
    rename"; the right fix is a redirect map, stored in the repo,
    that the server reads on startup — and a CI check (Chapter 15)
    that refuses to publish a PR whose net effect is to break a URL
    still referenced from `content/` or from the code graph. The
    file-based model makes this check mechanical; proprietary
    wikis that renumber pages internally often cannot.

3.  **Merge-conflict storms on collaborative pages.** Two authors
    rewrite the same `runbook.md` in parallel, and Git's line-based
    merge produces a paragraph-level conflict the review UI cannot
    usefully display. A wiki UI with live cursors would dodge this;
    the file-based model cannot. The honest mitigation is to treat
    high-churn pages as *owned* — a single author, a short PR, and
    a rule that the second contributor rebases rather than merges.
    For pages that are genuinely multi-author in real time (incident
    timelines during an active outage), a file-based wiki is the
    wrong tool; use a shared doc for the duration of the event and
    import the result afterwards.

4.  **Over-indexing on the "everything is a file" aesthetic.**
    Revision history, access control, and search *can* all live in
    the filesystem, but not all of them *should*. Per-user history
    of which pages a reader has read, ephemeral draft autosaves,
    comment threads on published pages — these are operational data
    that change minute by minute and have no provenance value. Put
    them in a side database and resist the temptation to "just use
    the filesystem for those too." The filesystem wins for content;
    it loses for mutable operational state.

A file-based wiki is also the wrong substrate for three kinds of
content altogether. **Multi-thousand-editor public wikis** (the
Wikipedia shape) need merge strategies no PR UI provides;
**WYSIWYG-only teams** — writers who genuinely cannot and will not
edit Markdown — need a different authoring surface with a sync
pipeline to files; and **real-time collaborative editing** (Figma,
Google Docs) is a product category file-based wikis have never
served well. The question to ask before adopting the model is not
*"do we like Markdown?"* but *"can a pull request be the unit of
doc review in our organisation?"* If the answer is yes, Part II's
four chapters apply directly. If the answer is no, this chapter's
arguments still hold — they just apply to a different layer
(e.g. an import pipeline from a proprietary wiki into a
file-based mirror that the code graph can trust).

## Conclusion

A file-based wiki is the right substrate for a software KB because it
inherits the guarantees the software itself already needs: plain-text
diffs, version control, review, CI. The `WikiRepository` interface and
its `FileRepository` implementation show that the engineering cost of
"wiki as files" is small — a handful of functions in a single Go file —
while the payoff is that *every other layer* of the KB (frontmatter in
Chapter 5, the pipeline in Chapter 6, publishing and search in Chapter
7, the code graph in Parts III–IV) can assume a stable, observable,
diffable input.

The next chapter turns to what lives *inside* those files: YAML
frontmatter as an explicit provenance record, and why trust in a
software KB begins at that boundary.

## References

```{bibliography}
:filter: keywords % "prose-layer" or keywords % "file-based" or keywords % "docs-as-code"
```
