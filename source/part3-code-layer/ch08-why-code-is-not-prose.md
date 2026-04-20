---
title: 'Chapter 8 — Why Code is Not Prose'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - code-layer
  - deepwiki
  - parsing
  - ir
---

# Chapter 8 — Why Code is Not Prose

This chapter on one page — three structural claims, one
experiment, and four anti-patterns that explain why the wiki
pipeline of Part II cannot carry code:

```{mermaid}
mindmap
  root((Code != Prose))
    Structural claims
      Parse before index
      Embed identity not body
      Relations are first-class
    Experiment
      Vector-only vs hybrid
      Recall@10 on code queries
      Results in Appendix B
    Anti-patterns
      Chunked file embeddings
      Dense-only retrieval
      Graph-free design
      Boiling the ocean
    Hand-off to Part III
      ch9 Parser
      ch10 Embeddings
      ch11 Graph
      ch12 Hybrid retrieval
      ch13 Prompt and generation
```

It is Tuesday, 2 p.m. The new hire on your team has been at
it for six weeks. She opens a pull-request chat and asks: *"where
is `runSync` called from?"*. The senior engineer pastes a `grep`
screenshot with 37 hits — comments, tests, a string literal in
log output, two methods on unrelated types. She still cannot tell
what the repo actually does. The wiki has three paragraphs about
"syncing," none of which mention a function. The chat LLM
confidently invents two caller functions that don't exist. Six
weeks in, she is still guessing. **This chapter is about why the
wiki you just built in Part II cannot save her — and what shape
the code layer has to take to rescue the afternoon.**

## Why

Part II built a wiki that treats every page as a *document*: one
Markdown file per topic, tokenised as plain text, ranked by prefix
match. That model works up to a point — it solves the prose layer
completely. It fails the moment the question is about **code**.

Consider a new-hire scenario that the companion blog post opens with
{cite}`fanyamin2026deepwiki`: somebody asks *"where is `runSync`
called from?"*. In a seven-year-old Go repository that sentence has
three bad answers and one correct one. The bad answers are:

1.  `grep -r runSync` — returns every comment, every log-line, every
    test, every string literal, and every method on an unrelated type
    that happens to share the name.
2.  *"Just read the code."* — the senior engineer's answer, and a
    confession that the codebase has outgrown individual human
    capacity.
3.  Pasting the whole repository into a chat LLM — blows the context
    window, returns a confidently wrong answer, and provides no
    traceable citation.

The correct answer is *"there are five callers, all in
`reference-impl/code-kg/service.go`, lines 154, 161, 278, 364, and 376"* —
and to produce that answer at scale a KB must model **code as code**,
not as prose. That means parse it into a tree, extract entities,
store them with stable identifiers, and remember who calls whom.

This chapter explains why that is not optional, surveys the academic
literature that has been telling us so for a decade
{cite}`allamanis2018survey`, and sets up the five chapters that
follow: parsing (ch09), embedding (ch10), graphing (ch11), retrieval
(ch12), and generation (ch13).

## What

Three claims from the *naturalness of code* literature
{cite}`allamanis2018survey` shape everything in Part III.

**Claim 1 — Code has structure that prose retrievers discard.**
A function is not a bag of words. It has a name, a signature, a
docstring, a body, a start-line, an end-line, imports, and — once you
have imports — a *call graph*. A `RecursiveCharacterTextSplitter`
configured for Markdown will cheerfully cut a Java method into three
chunks, severing the signature from its implementation and the
implementation from its trailing brace. The resulting embeddings
place those chunks in three different regions of vector space. A
query for the *method* retrieves some of the fragments, in wrong
order, with no way to stitch them back.

**Claim 2 — Code search needs exact-match escape hatches that
dense retrieval cannot provide on its own.** When the user types
`entityID` they expect the function named `entityID` — not the
"semantic neighbours of *entity* and *ID*". The CodeSearchNet
evaluation {cite}`husain2019codesearchnet` made this concrete: early
dense-only code searchers lost hard to BM25 {cite}`robertson2009bm25`
on queries dominated by identifiers. The fix is hybrid retrieval
(ch12), but the prerequisite is still Claim 1 — you must have named
entities to rank.

**Claim 3 — Code has relations that no amount of embedding captures.**
Vector space encodes similarity; it does not encode *calls*,
*implements*, *imports*, *returns*. Two functions with identical
signatures and comments cluster tightly in vector space even when
one lives in the HTTP handler layer and the other in the background
worker. GraphCodeBERT {cite}`guo2021graphcodebert` showed that
injecting data-flow edges into training improves code understanding
tasks; our weaker, engineering-grade version of that insight is: if
you want to answer *who calls what*, you must build the graph
yourself (ch11) — a lesson the DeepWiki methodology
{cite}`fanyamin2026deepwiki` pushes hard in §§2 and 6.

## How

The architectural consequence is a **dual stack**: a vector store for
similarity, and a graph store for structure. Both are fed by the same
parser, and the parser is the first place the design decisions show.

Part III is organised around the pipeline that the code-layer
reference implementation actually runs inside its `Service.runSync`
and `runIncrementalSync` methods:

```{mermaid}
flowchart LR
    A["Git working tree"] --> B["Parser (ch09)"]
    B --> C["Entity with<br/>stable ID"]
    C --> D["Embeddings (ch10)<br/>sqlite-vec / pgvector"]
    C --> E["Graph (ch11)<br/>Memgraph"]
    D --> F["Hybrid retriever (ch12)"]
    E --> F
    F --> G["Prompt &amp; generator (ch13)"]
```

Three properties of this stack earn their own chapters later:

- **Stable identity.** The entity ID is a content-free but
  location-aware hash — `sha256(repoID + filePath + entityType +
  name + startLine)[:16]`. That choice is what lets Chapter 11's
  graph survive a re-index and Chapter 14's incremental sync
  delete-then-insert on `M` without leaving dangling edges.

- **Structured embedding input.** We do not embed the function body.
  We embed a short, templated header — *Language / Type / Name /
  Signature / Doc* — because that is what carries the *intent* the
  user actually queries for. Chapter 10 measures the recall
  difference.

- **Bounded relation taxonomy.** We ship eight edge types
  (`CONTAINS`, `IMPORTS`, `CALLS`, `IMPLEMENTS`, `EMBEDS`,
  `DEPENDS_ON`, `RETURNS`, `ACCEPTS`) and nothing else. Adding a
  ninth is a design-review-level change — a guardrail that keeps the
  graph operationally reasonable.

Every chapter after this one works against a vendored excerpt from
the code-layer reference implementation (paths under
`reference-impl/code-kg/`), with provenance headers written by
`make book-refresh-excerpts` (see `examples/SOURCE.md`).

## Example

A one-minute demonstration makes the three claims concrete. The
inputs are two files, one per layer.

**Prose layer** (Markdown) — `runbook/onboarding.md`:

```markdown
## Syncing a new repository

To index a repo, register it with `code-kg register`, then call
`code-kg sync --repo-id <id>`. The sync pipeline parses the files,
generates embeddings, and updates the graph.
```

**Code layer** (Go) — a minimal `service_sync.go`:

```go
func (s *Service) runSync(repo *Repository, path string) error {
    files, _ := s.parser.CollectSupportedFiles(path)
    for _, f := range files {
        s.parseFileForSync(repo.ID, path, f)
    }
    return s.graphStore.UpsertRepositoryGraph(repo.ID, repo.Name, ents, rels)
}
```

Ask the prose-layer index (Part II) *"how do I sync a repo?"* — you
get the runbook back. That's correct; it's what the prose layer is
for.

Now ask the prose-layer index *"where is `runSync` called from?"*.
You get nothing useful, because:

1.  No page contains the literal string `runSync` — the runbook uses
    the CLI name `code-kg sync`, not the Go method name.
2.  Even if it did, you'd get prose describing sync, not a list of
    call sites.

Finally, ask the code layer the same question. The answer is a list
of lines — five lines — each citing `reference-impl/code-kg/service.go`
with a `file:line` anchor. That is the artefact Part III teaches you
to build.

A reproducible version of this experiment, run against the code-layer
reference implementation, appears in Appendix B.

## Common mistakes

These are the four design failures we see most often in
first-time code-KB builds. Each is the *opposite* of one of the
three claims above; the fourth is a scope failure.

**1 — Treating code as long prose.** The symptom is a single
embedding per file or per "chunk" of fixed character length.
`RecursiveCharacterTextSplitter(chunk_size=1500)` cuts a Java
method into three pieces and places them in three different
regions of vector space. The fix is Claim 1 from the *What*
section: parse first, then embed one *entity* at a time with a
stable identity. The parser (Chapter 9) is what makes this
possible; embedding-from-chunk cannot.

**2 — Dense-only retrieval.** The symptom is that typing an
exact identifier (`entityID`, `runSync`) ranks the real
definition below three unrelated neighbours. Embeddings
optimise for semantic neighbourhood, and exact identifiers
rarely live at the *closest* point in that neighbourhood. The
fix is the hybrid retriever of Chapter 12 — BM25-style scoring
as either a fallback tier or a fused rank alongside dense
retrieval.

**3 — Graph-free design.** The symptom is that queries of the
form *"who calls X"*, *"what implements Y"* simply *can't* be
asked. Vector space does not encode edges. The industry's
attempt to paper over this with larger context windows
(*"just paste the whole repo"*) scales linearly with codebase
size and collapses above roughly 20 kLOC. The fix is Chapter 11:
a bounded graph that carries identity + relations, sitting
alongside the vector store.

**4 — Boiling the ocean.** The symptom is an architecture
document that proposes a unified store with a custom embedding,
a custom index, and a custom fine-tune — before the team has
shipped a single citeable answer. Part III's construction is
deliberately boring: tree-sitter + sqlite-vec + Memgraph +
one-prompt generator. Start there. Upgrade specific stages
(Chapter 15's upgrade matrix) once you have measured what
actually moves the retrieval numbers.

## Conclusion

Prose retrievers and code retrievers look similar at the API level —
both take a query string and return ranked documents — but they fail
on different queries and for different reasons. The rest of Part III
is a construction proof that a file-based wiki (Part II) plus a
four-stage code pipeline (parse / embed / graph / retrieve) covers
*both* question classes without needing a single unified store.

Chapter 9 starts at the first stage: parsing.

## References

```{bibliography}
:filter: keywords % "code-layer" or keywords % "deepwiki" or keywords % "parsing" or keywords % "ir"
```
