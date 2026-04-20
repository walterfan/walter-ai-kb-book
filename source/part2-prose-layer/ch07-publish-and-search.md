---
title: "Chapter 7 — Publish and Search"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - prose-layer
  - search
  - publishing
---

# Chapter 7 — Publish and Search

This chapter at a glance — the decisive trade-off between a bespoke
in-memory index and an operational search cluster, the ten-line
tokeniser whose defaults carry surprising weight, the failure modes
prefix-match search has on identifier-literal and CJK queries, and
the staircase of scaling moves that keep `Search(...)` a single
stable interface across five orders of magnitude of corpus size:

```{mermaid}
mindmap
  root((Publish & search))
    Why
      Navigation is not search
      Search fails first at scale
      Static site must survive the server
    In-memory index
      Slug map
      Inverted postings (term -> slugs)
      Derived views (author, type, status)
      Whole-map rebuild on write
    Tokeniser
      Unicode letter/digit
      No stemming (identifier-friendly)
      Length >= 2, deduped
      Lowercase, locale-insensitive
    Query
      Prefix match (not exact)
      Score = term hits
      No BM25, no phrases
      Linear in vocabulary
    Static publishing
      Sphinx + MyST
      Client-side search (Porter stem)
      Cross-refs as hard errors
      Themeable output
    Failure modes
      CJK segmentation missing
      Identifier-literal paraphrase
      Typo intolerance
      Scale cliff at ~100k pages
    Staircase
      In-memory -> Bleve
      Bleve -> Meilisearch
      Meilisearch -> ES
      Interface unchanged
```

A new engineer joined last week. On Thursday she types
`recieve` into the wiki's search box and gets zero results. On
Friday she types `配置文件` and gets zero results. On Monday she
types `rate limit` and the first page returned is a three-year-old
blog post, while the actual runbook — whose title is literally
*"Rate limit configuration"* — is on page four. On Tuesday she
opens the JIRA ticket "the wiki's search is broken" and assigns it
to you.

The wiki's search is not broken. It is a ten-line tokeniser and a
prefix-match loop, and against that specification it is working
perfectly. What is broken is that a ten-line tokeniser is what this
team ships for the *entire* lifetime of the KB, instead of treating
it as the first step on a staircase whose later steps are easy. This
chapter is about both pieces: the tiny engine that earns its place
at the bottom of the staircase, and the honest map of which step to
climb to when which query class starts failing.

## Why

By the end of Chapter 6 we have a committed tree of well-formed
Markdown pages with honest frontmatter. Two questions remain before
Part II can close:

1.  **How do readers find a page?** Navigation is one answer (the
    Diátaxis-shaped toctree does that). *Search* is the other, and it
    is the first place a KB fails when it grows past a few hundred
    pages.
2.  **How do readers consume pages?** The backend serves dynamic
    rendering, but the same files must also build as a static site —
    so the KB survives the server, can be mirrored, and can be vendored
    into other repos.

This chapter covers both, and it tries to resist two temptations the
ecosystem pushes hard. The first: "just plug in Elasticsearch". An
operational search cluster is its own on-call rotation; a file-based
wiki with tens of thousands of pages does not earn it. The second:
"do not ship your own search". A ten-line tokeniser and a prefix-match
loop is enough to make 95 % of a software KB usable, and it is fully
under your control, debuggable, and deployable in a single binary.

## What

Two systems cooperate:

- **In-memory index** (this chapter, `backend/internal/wiki/index.go`):
  a Go struct mapping slugs to parsed pages, plus a side map
  `searchTerms: map[term]→[]slug`. It runs inside the `kb-cli serve`
  process, holds everything for live lookup, and is rebuilt from disk
  on every pipeline stage that writes.

- **Static publisher** (`wiki-template/metadata/_sphinx/`): a Sphinx
  {cite}`sphinx` + MyST-Parser {cite}`myst_parser` build target whose
  input is the same `content/` tree. Running `make sphinx-build` emits
  a fully static HTML site into `metadata/_build/html/` that can be
  hosted anywhere (GitHub Pages, S3, a laptop).

Neither system owns the content; both are *views* of the filesystem.
Delete the server, and the static build still renders. Delete the
static build, and the server still searches. The file is the
authoritative artefact, as Chapter 4 promised.

## How

### The in-memory index

The core data structure fits on one screen:

```{literalinclude} ../examples/part2-prose-layer/ch07/index.go
:language: go
:lines: 66-79
:caption: `IndexEngine` — slug map, plus a few specialised views.
```

Eight auxiliary maps — by title letter, category, word, author,
`doc_type`, source type, `verification_status` — are all derived from
`pages` and rebuilt in one pass. The only field that matters for
full-text search is `searchTerms`.

#### Tokenisation

The tokeniser is ten lines of Go:

```{literalinclude} ../examples/part2-prose-layer/ch07/index.go
:language: go
:lines: 285-299
:caption: `tokenize` — lowercase, letter-or-digit split, length ≥ 2, dedupe.
```

Three choices encoded here are worth defending:

1.  **Unicode letter/digit, not ASCII whitespace.** `unicode.IsLetter`
    covers CJK characters, Cyrillic, Arabic — anything with a Unicode
    letter category — so a wiki in any language tokenises correctly.
2.  **No stemming.** Porter's 1980 algorithm {cite}`porter1980stemming`
    would give better recall on English ("install" / "installing" /
    "installed" all collapse to "instal"), but it is language-specific
    and it makes search results surprising to engineers who expect
    literal matching. The trade-off goes the other way in a software
    KB.
3.  **Length ≥ 2, deduped.** Kills single-letter noise; keeps memory
    linear in document length, not quadratic.

#### Building the postings list

Index construction is a nested loop, not a B-tree:

```{literalinclude} ../examples/part2-prose-layer/ch07/index.go
:language: go
:lines: 275-283
:caption: `buildSearchIndex` — tokenise every page, invert into a map.
```

For each page, tokenise `title + body + tags`, and for every token,
append the slug. The result is a *postings list* in the classical IR
sense {cite}`manning2008introduction` — a map from term to list of
documents containing it. There is no tf/idf weight stored per token
and no positional information, which is why the query side is also
short.

#### Querying

A query is tokenised the same way, each term is prefix-matched against
the index's keys, and slugs are scored by "how many query terms hit
this document":

```{literalinclude} ../examples/part2-prose-layer/ch07/index.go
:language: go
:lines: 354-394
:caption: `Search` — prefix match, term-count score, sort, return summaries.
```

Four properties of this implementation:

- **Prefix match**, not exact. A query for `insta` matches `install`,
  `installation`, and `installer`. This is the pragmatic compromise
  that covers most of what stemming would give.
- **No BM25, no tf-idf** {cite}`manning2008introduction,robertson2009probabilistic`.
  The score is the cardinality of matching query terms. This is weaker
  than a real IR ranker, but at these document counts the user rarely
  notices.
- **No boolean operators**, no phrase queries, no fielded queries. A
  software KB's typical query is 1–3 keywords; giving up Lucene-style
  syntax buys simplicity.
- **Linear in `|searchTerms|` per query.** For the 10k-page range this
  book targets, "linear in the index" is fast enough on a single
  thread. Past that, the correct move is to reach for Bleve or
  Meilisearch, not to reinvent those inside the CLI binary.

The whole search subsystem, end to end, is under 100 lines of Go. It
is *correct* for the scale it targets, it is debuggable by any Go
programmer, and it ships with the binary. When the scale changes, the
interface does not — `SearchService` already takes a query string and
returns `SearchResult`, and a future Bleve-backed implementation can
drop in behind it without touching the HTTP or CLI layers.

### Live updates

Every write path (Chapter 5's `CreatePage`, the ingest loop of
Chapter 6, the update path, the delete path) ends by calling
`index.AddPage`, `index.UpdatePage`, or `index.DeletePage`, all of
which take the lock and rebuild the derived maps:

```{literalinclude} ../examples/part2-prose-layer/ch07/index.go
:language: go
:lines: 101-107
:caption: `AddPage` — single-writer, whole-map rebuild, simple enough to trust.
```

"Rebuild everything" sounds wasteful, but it is linear in the number
of pages and runs exactly once per write, inside a mutex. It
eliminates the traditional failure mode of incremental indexers:
stale entries that nobody realises are there until a user complains.
The cost is measured in milliseconds; the benefit is that the index
is provably consistent with `pages` after every operation.

### Static publishing with Sphinx

For publishing, the prose-layer reference implementation does not
invent a builder; it leverages Sphinx + MyST-Parser, the same stack
this book is built with.
A minimal `metadata/_sphinx/conf.py` looks like:

```python
extensions = ["myst_parser", "sphinxcontrib.mermaid"]
source_suffix = {".md": "markdown"}
html_theme    = "sphinx_rtd_theme"
master_doc    = "index"
```

The root `index.md` uses the same `INDEX.md` that `pipeline.Build()`
regenerates after every ingest. That file is the bridge between the
live server and the static site: both views consume it. A site build
is one shell command:

```bash
$ make sphinx-build WIKI_DIR=./demo
$ ls ./demo/metadata/_build/html/
index.html  search.html  _static/  _sources/  ...
```

Three things you get for free from Sphinx:

- **In-page search.** Sphinx emits a client-side JavaScript index that
  works offline, using the Porter stemmer at build time. Readers of
  the static site have a search that rivals the server's.
- **Cross-references.** `{doc}`, `{ref}`, and citation roles resolve
  across the whole tree, and the build fails if they do not. This is
  far stricter than the live server's prefix match, and it catches
  broken references that `verify` did not.
- **A themeable output.** Read the Docs theme, Furo, book theme, PDF
  via xelatex — one Markdown source tree renders to all of them.

What you give up is *interactivity*: the static site cannot create
pages, rerank search by click-through, or show "recent changes in the
last hour". For a software KB that is deliberately versioned in Git,
that is the right trade-off. Mutation lives in the repo and in the
server; publishing is a derived, immutable artefact.

## Example

Three queries against the same pages, walked through by hand.

Given these three pages under `content/`:

- `how-to/enable-tls.md` — `title: How to enable TLS`, tags `[tls, security]`
- `reference/api.md` — `title: API Reference`, body mentions "install" and "tokenization"
- `explanation/auth-model.md` — `title: Authentication Model`, body discusses "TLS" and "tokens"

Query `tls`:

- tokens: `["tls"]`
- prefix match on `tls` → hits `tls` in pages 1 and 3.
- scores: `{how-to/enable-tls: 1, explanation/auth-model: 1}`
- sort by score desc, return both.

Query `token`:

- tokens: `["token"]`
- prefix match on `token` → hits `tokenization` (page 2) and `tokens` (page 3).
- scores: `{reference/api: 1, explanation/auth-model: 1}`
- both returned.

Query `tls token`:

- tokens: `["tls", "token"]`
- page 3 hits both prefixes → score 2
- pages 1 and 2 hit one prefix each → score 1
- order: `explanation/auth-model`, then the other two.

No query is more clever than the user expects, which is a feature.

## Where the tiny search engine fails — and why that is still fine

Chapter 2 built the vocabulary — TF-IDF, BM25, hybrid retrieval,
re-ranking — for a reason: *that* is the retrieval surface a
serious RAG pipeline hands to an LLM. The search engine in this
chapter is its much humbler cousin, a few kilobytes of Go that a
human at a search box uses directly. It is worth being explicit
about what this engine cannot do, because the temptation to "just
add a reranker" to it is exactly the temptation a team should
resist until the problem actually appears.

Four query classes defeat the prefix-match index in predictable
ways. Each has a cheap workaround and an expensive one; almost every
team reaches for the expensive one first.

1.  **Identifier-literal queries that paraphrase.** A user searches
    for `"rate limit ingest"` when the symbol in the code is
    `ingestRateLimit`. The tokeniser split the identifier at case
    boundaries in the postings list, so `rate`, `limit`, and
    `ingest` all land as separate terms — but the user's query tokens
    also land as the same three terms, so this case actually works.
    The case that *does* fail is the inverse: the user searches for
    the paraphrase `"throttle incoming traffic"`, which shares zero
    tokens with either the identifier or the prose that describes it.
    This is the classic vocabulary-mismatch failure Chapter 2 names;
    the cheap fix is an aggressive tag set on the page itself (the
    frontmatter `tags:` field is already in the postings list), the
    expensive fix is dense retrieval (Chapter 8). A small team
    should almost always try the cheap fix first.

2.  **CJK queries on a tree with no segmentation.** The tokeniser
    uses `unicode.IsLetter` to split on anything that is not a
    letter or digit — which in Chinese or Japanese means *every
    character is a letter, so nothing splits*. A page containing
    `配置文件路径` and a query `配置文件` match only if the page's
    *full sequence* begins with the query, which it usually does
    not. The honest fix is a segmenter: `go-jieba` for Chinese,
    `kagome` for Japanese, both a `go get` away. The dishonest fix
    is to declare CJK support out of scope; teams that do this
    regret it when the first non-English user arrives. The hook is
    already there — the `tokenize` function is the only place that
    turns body text into terms, so swapping it for a
    language-aware tokeniser is a localised change.

3.  **Typo tolerance.** A search for `recieve` returns nothing,
    because the postings list only contains `receive`. Stemming
    would not fix this (both words stem differently); edit distance
    would. The library answer is `fuzzy` matching at query time,
    typically with a Damerau-Levenshtein distance of 1 or 2 on
    terms above some minimum length. The in-memory implementation
    can add this in a dozen lines of Go for the 10k-page scale, but
    it does so at a quadratic cost (every query term is compared to
    every postings-list term) that matters above ~100k terms.
    Meilisearch's typo tolerance is excellent and its operational
    cost is a single binary; at that scale it is the right move.

4.  **Ranking by relevance, not cardinality.** The `Search` function
    scores by "how many query terms hit this document". A
    sufficiently long page that *mentions* every term beats a
    focused page that *is about* the term. This is exactly the
    pathology BM25 was designed to fix via its length-normalisation
    term $b$ (Chapter 2): long documents should not dominate just
    because they are long. The cheap fix in the in-memory
    implementation is field weighting — boost title matches over
    body matches, as Chapter 2 also names — which the `searchTerms`
    map could implement by keeping a per-term origin ("was this
    token in the title or the body?") and adding a small coefficient
    at query time. The in-repo implementation does not do this
    today; the interface supports it without a migration. Chapter 2's
    *Advanced RAG* section shows why field weighting matters more
    than most tuning knobs below it.

The common thread is that the right moment to reach for Chapter 2's
heavier machinery is *when a specific query class stops working*,
not before. A software KB whose live search is a prefix-match index
and whose agent-facing retrieval is a BM25+dense+rerank pipeline is
not a contradiction — it is the healthy design. Different consumers
have different budgets and different expectations; serving both from
the same storage layer (files on disk) is the architectural win that
makes the disagreement cheap.

## Common mistakes in wiring up search

Beyond the query-class failures, four scaling and wiring mistakes
are frequent enough to warrant their own list:

1.  **Trying to keep an incremental index correct.** The prose
    layer uses whole-map rebuild on write for a reason: incremental
    update is the source of almost every "search is stale" bug in
    database-backed wikis. At the scale this chapter targets, the
    whole rebuild is milliseconds; giving that up to chase
    constant-factor performance is the classic over-engineering
    failure.

2.  **Bolting on a second search system "for the production site".**
    A team adds Elasticsearch "because the in-memory one is not
    serious enough" and ends up with two search layers that
    sometimes disagree — readers on the live server see one result
    set, readers on the published static site see another. The
    staircase in Competing approaches is a *sequence*, not a
    choice: pick the lowest step that currently fails, migrate the
    whole KB to it, and keep a single `Search(...)` interface.

3.  **Indexing content the trust layer disavows.** A naïve
    `LoadAndIndex` indexes every file under `content/`, including
    pages whose `verification_status` is `contradicted` or
    `superseded`. Those pages then surface in search results with no
    visible signal that they are stale. The right move is to index
    them but filter them out of the default query (and surface them
    via an explicit "include superseded" toggle for archaeologists).
    Chapter 5's trust fields are retrieval metadata, not just
    display metadata.

4.  **Treating the Sphinx in-page search as the "production"
    search.** Sphinx's client-side search is excellent for a
    static mirror; it is a disaster if an organisation relies on it
    exclusively. It does not see frontmatter, it cannot filter by
    `verification_status`, and its ranking is driven by Porter
    stemming {cite}`porter1980stemming` — which is a good signal on
    English prose and a *noisy* signal on identifier-literal
    queries. Keep the live server's search authoritative for
    authenticated readers; let the static build's search exist for
    the public or offline case, and for those readers only.

## Competing approaches

| System | Index size for 10k pages | Setup cost | Fit for a file-based KB |
|--------|---------------------------|------------|--------------------------|
| In-memory prefix index (this chapter) | ~20 MB | 0 (built-in) | Great below 10k pages. |
| Bleve {cite}`bleve` | ~100 MB on disk | `go get` + a few lines | Natural scale-up; still embedded, no server. |
| Meilisearch {cite}`meilisearch` | Separate process | Docker + an API key | Excellent ranking, typo tolerance; operational cost. |
| Algolia DocSearch {cite}`algolia_docsearch` | Crawled, hosted | Signup + crawl config | Free for open source; locks you in for private KBs. |
| Elasticsearch / OpenSearch | JVM cluster | High | Overkill for a KB at this scale. |
| Sphinx in-page search only | Build-time | 0 | Good for static docs; no live updates. |

The book's recommendation is the staircase:

1.  Start with the in-memory index. It is good enough for any team KB.
2.  Add Sphinx's static search in parallel for the published site.
3.  Swap Bleve in behind the `Search` interface if the in-memory
    version becomes CPU-bound.
4.  Only promote to Meilisearch or Elasticsearch when you have an
    explicit product reason (typo tolerance, fielded boosts,
    multi-tenant ranking).

Each step up preserves the `Search(query, type) → SearchResult`
contract, so client code does not change.

## Conclusion

A file-based wiki earns its "as simple as possible, but no simpler"
badge when the search layer is also simple enough to audit. An
in-memory postings map + a ten-line tokeniser is a complete, honest
search engine for a small-to-medium software KB. Sphinx handles the
static view, with its own stemmer-based search for the published site.
Every page is indexed consistently because every write path ends in
the same `AddPage` call, inside the same mutex.

Part II ends here. The prose layer has all its moving parts:
files (Chapter 4), frontmatter as provenance (Chapter 5), the
pipeline (Chapter 6), and publish + search (this chapter). Part III
turns from prose to code — embeddings, code graphs, and the hybrid
retrieval that makes a software KB different from a document
warehouse.

## References

```{bibliography}
:filter: keywords % "prose-layer" or keywords % "search" or keywords % "publishing"
```
