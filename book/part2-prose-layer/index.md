---
title: "Part II — The Prose Layer"
status: draft
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - prose-layer
---

# Part II — The Prose Layer

```{toctree}
:maxdepth: 1

ch04-file-based-wiki
ch05-frontmatter-provenance-trust
ch06-llm-classification-pipeline
ch07-publish-and-search
ch07a-prose-operational-model
```

The five chapters of Part II, on one page — a storage choice (Ch 4)
whose trust properties (Ch 5) the pipeline (Ch 6) must preserve,
served through search and a static site (Ch 7), with an operational
model (Ch 7a) that keeps the whole thing honest as the code
underneath changes:

```{mermaid}
mindmap
  root((Prose layer))
    Ch 4 File-based
      Markdown files in Git
      WikiRepository interface
      No DB, no cache
      Failure modes named
    Ch 5 Provenance
      Frontmatter (lineage)
      Footer (review state)
      AI -> pending rule
      Enforcement, not just expression
    Ch 6 Pipeline
      init, import, ingest
      verify, build, status
      Classifier pluggable
      LLM pitfalls cataloged
    Ch 7 Publish + search
      In-memory postings
      10-line tokeniser
      Sphinx static site
      Staircase to scale
    Ch 7a Operational
      C1 Page set
      C2 Footer
      C3 Three levels
      C4 Gates
      Honest about what it does not solve
```

## Why

Human-authored prose — tutorials, how-tos, runbooks, ADRs — is the oldest
layer of a software KB and the one machines cannot produce on their own.
Part II shows how the prose-layer reference implementation keeps that
layer trustworthy, searchable, and automatable without locking the content
into a proprietary system — and how to keep it correct over time.

### Where Part II sits in the book

Part II is the first of the book's two parallel "layer" parts. Part III
takes the same shape — five chapters that pick a substrate, harden its
contract, run a pipeline over it, expose it for search, and close with
an operational model — but applied to *code* rather than *prose*. Part V
then shows the two layers cooperating (a document-layering tuple that
reads both; a retrieval surface that fuses prose passages with code
embeddings). Reading Part II alone gives you a defensible prose-layer
KB; reading Parts II and III together gives you the substrate Part V
turns into a code-aware knowledge base; Part VI is governance for
everything Parts II–V produced.

```text
Part I       : the vocabulary (why a KB, what IR/RAG actually are, Diátaxis)
Part II      : the PROSE layer  — files → frontmatter → pipeline → search → op model    (this part)
Part III     : the CODE  layer  — parse → embeddings → graph → hybrid retrieval → prompt
Part IV      : the ops lifecycle — sync, eval, drift, rot (operational plumbing for Parts II and III)
Part V       : the hybrid layer — where prose and code meet
Part VI      : governance, trust, and outlook
```

The prose-layer structure is deliberately mirrored in Part III's
close: *four corners* on each side, so that the book's Parts V and
VI can talk about both layers in the same vocabulary. Noticing the
mirror is the cheap way to internalise the shape; §"How" below
names the mirror explicitly.

## What

A file-based wiki (Chapter 4), YAML frontmatter + footer as the two-block
provenance-and-review record (Chapter 5), the classification pipeline
(Chapter 6), publishing and in-memory search (Chapter 7), and an
operational model for keeping the prose correct as the code underneath it
changes (Chapter 7a).

### The five chapters as a dependency chain

The chapters are not independent essays; each is the substrate the
next one stands on. The table below makes the substrate relation
explicit — if you are deciding where to cut the part for a short
reading session, cutting *across* the dependency arrows is cheaper
than cutting *along* them.

| Chapter | Picks up from | Produces | Consumed by |
|---------|---------------|----------|-------------|
| **Ch 4** File-based wiki | Part I's "KB as code" thesis | `WikiRepository` + `FileRepository` + the "Git is your audit log" contract | Everything else in Part II; ch14 (drift detection) |
| **Ch 5** Provenance | Ch 4's filesystem contract | Frontmatter (lineage) + `PKB-metadata` footer (review) + the AI-sets-pending rule | Ch 6's ingest (writes footers); ch15 gates; ch18 document layering |
| **Ch 6** Pipeline | Ch 4 (files) + Ch 5 (schema) | Six CLI verbs; ingest that writes well-formed files with `unreviewed` trust; an append-only governance log | Ch 7 (indexes files it produced); ch14 (re-triggers ingest on drift) |
| **Ch 7** Publish + search | Ch 6's committed tree | In-memory postings list for the live server; Sphinx static build | Ch 7a's "what can gates check?" (search is *not* a gate); ch21's agent retrieval |
| **Ch 7a** Operational model | Everything above | Four-corner model C1–C4; the Part II checklist | Ch 14 (change detection, C2-driven); ch15 (gates, C4); ch16 (three-level updates, C3); ch18/ch21 (both layers) |

Two arrows are worth singling out. Chapter 5's frontmatter contract
is the *only* artefact the live server (Ch 7) and the classification
pipeline (Ch 6) *both* read — if you break the schema in Ch 5, you
break both consumers at once. And Chapter 7a's footer (C2) is the
one field every later chapter in Parts IV–VI touches, because it is
the hinge between per-page state and the operational cycle that
acts on it.

## How

Five chapters. Chapters 4–7 handle *getting prose in*. Chapter 7a closes
Part II with the four-corner operational model (opinionated page set,
metadata footer, three-level updates, verification gates) that Part IV
and ch18/ch21/ch22 later operationalise, and that mirrors Part III's
four-corner close (parsing / embeddings / graph / prompt).

### The Part II ⇄ Part III mirror

The two layers are not symmetric in their *content* — prose drifts,
code does not; prose has paragraphs, code has functions; prose is
updated by humans, code by commits. They are symmetric in their
*operational shape*, and the mirror is worth stating once so that
Parts V and VI can rely on it:

| Part II (prose) | Part III (code) | Shared shape |
|-----------------|-----------------|--------------|
| Ch 4 File-based wiki | Ch 8 Why code is not prose | *Pick a substrate and name its contract* |
| Ch 5 Frontmatter + footer | Ch 9 Parsing and entity extraction | *Make the contract machine-readable* |
| Ch 6 Classification pipeline | Ch 10 + Ch 11 Embeddings + graph | *Run a pipeline over the substrate* |
| Ch 7 Publish + search (prefix index) | Ch 12 Hybrid retrieval + RRF | *Expose the substrate for query* |
| Ch 7a Four-corner operational model | Ch 13 Prompt + generation | *Close with a stable shape the rest of the book refers to* |

The mirror is why the book's glossary (Appendix D) uses the same
vocabulary for both layers and why Chapter 18's document-layering
tuple can treat prose and code uniformly. It is also why teams that
adopt Part II first and Part III second usually *compress* Part III's
timeline — the operational shape is already in place.

### Reading paths — pick one by the problem you have

Part II is 1 600 lines of book. You do not need to read it linearly.
Three typical paths cover most readers' purposes:

- **"I have 20 minutes before a meeting and I want the thesis."**
  Read the hook opening and `## Why` of **Ch 4**, then the
  `## Why` of **Ch 7a**, then Ch 7a's `## Part II in one page —
  a pointer checklist`. That is the whole argument in three
  pages. Return for the mechanics later.

- **"I am building the tool-chain."** Read **Ch 4 → Ch 5 → Ch 6**
  in order, skipping the `## Competing approaches` tables on the
  first pass. Then read the code references in `ch04/repository.go`,
  `ch05/frontmatter.go`, and `ch06/pipeline.go`. Skim Ch 7;
  revisit Ch 7a after you have run the pipeline once against a
  real corpus and want to know which rules to enforce.

- **"I have an existing KB and I am doing a postmortem."** Skip
  the chapter `## Why` sections and go straight to:
  **Ch 6 §"How LLM classification fails in production"**,
  **Ch 7 §"Where the tiny search engine fails"**, and
  **Ch 7a §"What this model does *not* solve"**. Cross-reference
  each symptom you have seen in the wild against the Part II
  checklist in Ch 7a; that will tell you which chapter to read
  in full.

These paths are the reason the part is shaped the way it is: each
chapter has a self-contained opening, a self-contained failure
catalogue, and a self-contained "competing approaches" table, so
that a reader arriving mid-part has a complete unit of thought to
take away without reading the part in order.

## Example

End-to-end run of the CLI against a messy raw folder, producing a clean
wiki. The full walkthrough is in Appendix A.

## Conclusion

File-based + Git-backed + pipeline-validated + *operationally modelled*
= a prose layer that behaves like code: reviewable, diffable,
automatable, and auditable for staleness.

## References

```{bibliography}
:filter: keywords % "prose-layer" or keywords % "provenance"
```
