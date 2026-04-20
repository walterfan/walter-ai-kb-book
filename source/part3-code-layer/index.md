---
title: 'Part III — The Code Layer'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - code-layer
---

# Part III — The Code Layer

Part III on one page — six chapters turn the "wiki works, grep
doesn't" pain of Part II into a dual-stack (vector + graph)
retriever that answers structural, identifier, and fuzzy
questions with citations:

```{mermaid}
mindmap
  root((Code Layer))
    Starting point
      ch8 Why code is not prose
      Parse Embed Relate
    Indexing pipeline
      ch9 Parser and entities
      ch10 Embeddings and stores
      ch11 Graph of relations
    Retrieval pipeline
      ch12 Three-tier hybrid
      ch13 Prompt and generation
    Properties shipped
      Structural queries
      Identifier-exact queries
      Fuzzy queries
      Citations in every answer
    Hand-off to Part IV
      Drift and maintenance
      Evaluation
      Incremental sync
```

```{toctree}
:maxdepth: 1

ch08-why-code-is-not-prose
ch09-parsing-and-entity-extraction
ch10-embeddings-and-vector-stores
ch11-code-knowledge-graph
ch12-hybrid-retrieval-and-rrf
ch13-prompt-and-generation
```

## Why

Part II's prose layer solves one class of question — *"what do we
know about X?"* — and fails on the other — *"where in the code
base is X used?"*. Chapter 8 makes the failure precise; the rest
of Part III builds the dual-stack (vector + graph) pipeline that
answers the second class, grounded in the code-layer reference
implementation (paths under `reference-impl/code-kg/`).

The failure is not a gap in the wiki — it is a category error.
A human writes a wiki page about *"how sync works"* but not about
*"who calls `runSync`"*, because the first sentence is worth
writing and the second is derivable from the code. A code-layer
KB is the machine that *does* the deriving, continuously, so
that every engineer gets the answer in two seconds rather than
twenty minutes of grep-and-scroll.

## What

Everything needed to answer structural, identifier, and fuzzy
natural-language questions over a codebase with *citations* — one
chapter per stage of the pipeline introduced in the blog's
§§2–8 {cite}`fanyamin2026deepwiki`:

- **Chapter 8 — Why code is not prose.** Three structural claims
  (parse first, embed identity, graph carries relations); one
  measured experiment (vector-only vs hybrid on real code queries);
  four anti-patterns that cause first-time code-KB builds to fail.
- **Chapter 9 — Parsing and entity extraction.** A real parser
  (tree-sitter {cite}`brunsfeld_treesitter`); a closed entity
  schema (`package`, `type`, `method`, `function`); stable IDs
  from `sha256(repoID + filePath + entityType + name +
  startLine)[:16]`; resource-leak, closure-noise, and
  multi-line-signature pitfalls.
- **Chapter 10 — Embeddings and vector stores.** A five-line
  identity template (`Language / Type / Name / Signature /
  Doc`) that beats body-embedding by roughly 2x on recall@10;
  batch + backoff + rate-limit discipline; `sqlite-vec`
  {cite}`sqlite_vec` / `pgvector` {cite}`pgvector` /
  `Milvus` {cite}`milvus` decision matrix; theory anchor on
  bi-encoders {cite}`reimers2019sbert`, cross-encoders
  {cite}`nogueira2019passage`, and HNSW {cite}`malkov2018hnsw`.
- **Chapter 11 — Code knowledge graph.** A closed
  eight-edge taxonomy on a graph database (e.g.
  Memgraph {cite}`memgraph`); location-aware node IDs;
  full-rebuild-per-repo write pattern; theory anchor on
  graph locality and the GraphCodeBERT data-flow prior
  {cite}`guo2021graphcodebert`.
- **Chapter 12 — Hybrid retrieval and RRF.** Three-tier
  strategy (vector primary → keyword fallback →
  graph expansion); why score-level fusion is meaningless
  and rank-level fusion (RRF {cite}`cormack2009rrf`) is
  the upgrade path; query-routing heuristics that save
  latency.
- **Chapter 13 — Prompt and generation.** Two hard rules
  (always cite `file:line`; refuse when context is
  insufficient); structured-context format; measurable
  faithfulness {cite}`es2024ragas`; the indirect
  prompt-injection threat model {cite}`greshake2023injection`.

## How

Every chapter ships at least one `{literalinclude}` from a
vendored excerpt (see `examples/SOURCE.md`), at least three
citations, and at least one measurement the blog did not report —
the book's non-copy policy. Excerpts are refreshed with
`make book-refresh-excerpts` and verified byte-stable with
`make book-check-excerpts`.

Each chapter also follows the same Part II-inspired
five-section spine: a *Monday-morning hook* connecting the
chapter to a pain you have lived through; the *Why / What /
How* that reads as engineering, not survey; a *Theory anchor*
(ch10–ch13) that names the published results behind the
design; a *Common mistakes* section that lists the
anti-patterns; and an *Example* block reproducible against
the code-layer reference implementation in Appendix B.

## Operational model

The code layer inherits Part II's verification-first mindset
and specialises it:

- **Build** — `code-kg sync --repo-id <id>` parses, embeds,
  and rebuilds the graph. Idempotent; safe to re-run.
- **Verify** — recall@5 on a held-out query set (identifier,
  structural, fuzzy) is the primary retrieval health metric.
  Prompt metrics (citation compliance, refusal rate) are
  secondary and *only move* when recall is not the bottleneck.
- **Operate** — the retriever degrades gracefully: no
  embedding API key → keyword-only mode; no graph
  connectivity → vector + keyword only; no vectors → keyword
  only. Every mode is still useful; no mode is a hard fail.

## Example

Appendix B runs the full pipeline end-to-end: register the repo,
sync, ask three questions (one per retriever tier), then do an
incremental sync on a one-line diff to measure the speedup ratio.

## Pointer checklist

For a one-screen summary of the six key decisions you carry
forward from Part III into your own system, jump to the
**"Part III pointer checklist"** section at the end of
Chapter 13. Each item is a commit-before-coding decision,
not a retrospective.

## Conclusion

With Parts II and III in place, the KB answers both prose and
code questions with cited, reproducible responses. Parts IV–VI
make the result *operationally durable* (drift, evaluation,
governance) and extend it to hybrid workflows (AI coding
assistants, agents).

## References

```{bibliography}
:filter: keywords % "code-layer"
```
