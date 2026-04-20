---
source_url: https://www.fanyamin.com/gei-dai-ma-cang-ku-zao-yi-ge-deepwikitree-sitter-embedding-tu-pu-llm-de-fang-fa-lun.html
version: v1.2
captured_at: 2026-04-17T20:54:01Z
captured_sha256: f5ad6d7610037e93f9cb51a5233323e754fd802f84b8fc6b9c7adb5c09b1fb13
captured_bytes: 69473
captured_via: "curl -fsSL --compressed"
bibtex_key: fanyamin2026deepwiki
---

# Outline of the blog post

This file records the *section structure* and the *key arguments* of the
vendored blog post. It is used as a writing brief by chapters that cite
the blog (see `design.md` D8 for the mapping).

The outline is mutable, but it MUST reflect only the blog's structure —
not the book's prose. Book prose lives in the chapter files, not here.

## §1 — A scene from onboarding

New-hire asks "where is `runSync` called from?"; senior says "just read
the code." Matured codebases make that impossible. Dumping the repo into
a chat LLM leads to confident hallucinations.

## §2 — Why code is not prose

`RecursiveCharacterTextSplitter` plus dense retrieval fails on code
because (a) splitting breaks semantics, (b) structural filtering is lost,
(c) call relations are dropped.

## §3 — Four-piece architecture (flowchart + UML data model)

Ingest → dual-store → retrieve+generate. Key ideas: dual stack (vector +
graph), Entity as first-class citizen, incremental sync. UML: Repository
→ Entity → EmbeddingVector / Relation / KnowledgeDoc; Entity ID =
hash(repo+path+type+name+start_line).

## §4 — Tree-sitter parsing

Multi-language uniform API, incremental, error-tolerant. Output = a
language-neutral `CodeMetadata`. Preserve `start_line / end_line`. Body
truncation at 3–4k chars. Skip `vendor/`, `node_modules/`, etc. Pitfalls:
`tree.Close()`, anonymous functions, one thin visitor per language.

## §5 — Embedding layer

Structured input beats raw body. sqlite-vec vs pgvector decision matrix.
Batch + exponential backoff + rate limit.

## §6 — Graph layer

Bounded edge taxonomy (`CONTAINS`, `IMPORTS`, `CALLS`, `IMPLEMENTS`,
`EMBEDS`, `DEPENDS_ON`, `RETURNS`, `ACCEPTS`). Regex-based call
extraction as the "poor man's" version. Noise filter: built-in types and
short lowercase symbols. Full-graph `DETACH DELETE` rebuild per repo.

## §7 — Retrieval layer

Hybrid: vector-primary → keyword fallback → graph expansion (1–2 hops).
BM25 + vector via RRF as upgrade path.

## §8 — Generation layer

Two hard prompt rules: always cite `file:line`; allow to say unknown.
Structured context header per snippet. Structured overview prompt.

## §9 — Sequence diagram

Indexing phase (write-heavy) vs query phase (read-heavy). Different
bottlenecks, different optimisations.

## §10 — Incremental sync (the key to production)

`git diff --name-status`, not `git log` aggregation. State machine:
full-scan vs incremental. A/M/D/R handlers; `M` must delete-then-insert
because Entity ID depends on `start_line`. "Dangling edge" pitfall →
vector-incremental + graph-full rebuild. >30% files changed ⇒ fall back
to full. `SyncJob` status/phase book-keeping. `defer recover()` on
panics. Measured 36× / 180× / 9× speedups on a real repo.

## §11 — Document layering (L0–L4)

L0 code + comments + tests; L1 AI-generated wiki (never hand-edit); L2
runbook; L3 ADR (the only place "why-not" survives); L4 vision.
Minimum ADR template. "Ask the wiki" becomes the daily workflow.

## §12 — Harnessing AI coding with the KB

Four AI-coding pain points = context underfeeding. Closed-loop: Context
Builder → hard-constraint prompt → generate → review → feedback rule →
Context Builder. Per-task-type context recipes. Hard-constraint prompt
template (no hallucinated APIs, mandatory `file:line`, prefer reuse).
Three-phase rollout: `.cursor/rules` → MCP Server → CI AI gate. "AI is a
junior teammate." Sensitive ops need human gates.

## §13 — Thinking map + checklist

Mind-map summary plus a ~20-item build-your-own checklist covering every
stage, plus four open questions for the reader.
