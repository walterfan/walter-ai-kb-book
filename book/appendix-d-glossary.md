---
title: "Appendix D — Glossary"
status: draft
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - appendix
  - glossary
---

# Appendix D — Glossary

**Translator's note on *prose* vs. *document*.** English has two
perfectly good words that English-speaking engineers do not usually
conflate: *prose* (the human-authored narrative content) and *document*
(the file object that carries content, which may be prose or code or
both). Chinese-language software engineering tends to flatten both
words to 「文档」 , which collapses a distinction this book relies on
throughout Parts II and III. The Chinese edition therefore adopts the
convention:

- **prose → 文稿** (the narrative content itself; 文稿层 = the prose
  layer)
- **document → 文档** (the file object, Diátaxis category, or
  classified artefact — as in document-layering)
- **documentation → 文档工作 / 文档体系** (the engineering activity)

Every glossary entry and cross-reference below honours this
distinction; watch for it in particular in *Prose*, *Document*, and
*L0–L4*.

```{glossary}
ADR
  Architecture Decision Record. A short, append-only document that records
  the context, decision, and consequences of a single architectural
  choice. See MADR for a specific template. {cite}`nygard_adr`
  {cite}`madr`

BM25
  A tf-idf-descended ranking function widely used in full-text search.
  {cite}`robertson2009probabilistic`

Diátaxis
  A four-type documentation taxonomy (Tutorial, How-to, Reference,
  Explanation) used throughout Part II. {cite}`procida_diataxis`

Entity
  In the Code Knowledge Graph, a hashable unit — file, function, class,
  package — with a stable content-addressed ID.

HNSW
  Hierarchical Navigable Small World. The ANN index backing most modern
  vector stores, including pgvector. {cite}`malkov2020hnsw`

KB
  Knowledge Base. In this book, the union of prose, code, embeddings, and
  graph that a team queries to do its job.

L0–L4
  The five-tier document-layer model introduced in Chapter 18 (L0
  code and comments; L1 committed human prose such as ADRs; L2
  collaborative human prose such as wiki pages; L3 reviewed
  AI-drafted prose; L4 unreviewed AI drafts). Chapter 18 upgrades
  the single-axis model to the four-tuple ⟨L, U, R, S⟩.

Layer tuple
  The four-valued classification ⟨L, U, R, S⟩ — document layer,
  updated-by, review-status, review-score — introduced in Chapter 18
  as the operational replacement for single-axis document tiering.

L1 / L2 / L3 (update strategy)
  The three update levels from Chapter 16. **L1 mechanical**: rules
  only, zero LLM tokens. **L2 bounded-LLM**: one page's body plus one
  diff fed to an LLM, bounded to a few kilobytes. **L3 human-led**:
  human writes, LLM copy-edits. Not to be confused with the
  document-layer L0–L4 above; the number line is different.

MCP
  Model Context Protocol — the standard the book uses to let IDE agents
  query the KB. {cite}`mcp_spec`

MyST
  Markedly Structured Text — the Markdown flavour Sphinx understands
  natively via `myst-parser`.

PKB
  Project Knowledge Base — a KB scoped to a single software project,
  in contrast to a team- or organisation-wide KB. This book's
  opinionated ten-page set (`00-overview` through `09-runbook`) is a
  typical PKB shape.

PKB-metadata footer
  The HTML-comment block at the foot of every content page, carrying
  six fields (`last_updated`, `commit`, `updated_by`, `review_status`,
  `review_score`, `reviewed_by`). Introduced in Chapter 5 as the
  operational counterpart to the YAML frontmatter: frontmatter
  carries provenance (who created the page, at what commit); the
  footer carries review state (who signed off, with what score,
  when).

Prose (zh: 文稿)
  Human-authored narrative text — tutorials, how-tos, reference pages,
  explanations, ADRs, runbooks. In this book, *prose* is the material
  the **prose layer** (Part II) handles and is deliberately contrasted
  with *code* (which the **code layer** in Part III handles via
  parsing and embeddings). The distinction matters because prose has
  paragraphs as its natural chunking unit, drifts against the code it
  describes, and updates when a human decides it is wrong; code has
  functions as its natural unit, does not drift (it is the source of
  truth), and updates every commit. Chapter 8 opens with exactly this
  split. Contrast with *Document*.

Document (zh: 文档)
  The *container* for content, independent of whether the content is
  prose or code. A markdown file with YAML frontmatter is a document;
  its body may be prose, a code block, or both. *Document-layering*
  (Chapter 18, L0–L4) classifies documents by provenance and
  authority, not by their internal content type. Rule of thumb:
  *prose* (文稿) when we mean the readable content, *document*
  (文档) when we mean the file object that carries it.

RAG
  Retrieval-Augmented Generation. The pattern of grounding an LLM's output
  in retrieved context. {cite}`lewis2020rag` {cite}`gao2023retrieval`

RRF
  Reciprocal Rank Fusion. A rank-combination method used in hybrid
  retrieval. {cite}`cormack2009rrf`

tree-sitter
  Incremental, multi-language parser powering the code-KB parse stage.
  {cite}`brunsfeld2018treesitter`
```

## References

```{bibliography}
:filter: keywords % "foundations" or keywords % "ir-rag" or keywords % "adr"
```
