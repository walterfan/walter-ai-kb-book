---
title: 'Chapter 24 — Outlook and Open Problems'
status: draft
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - governance
---

# Chapter 24 — Outlook and Open Problems

## Why

By the time a reader reaches the last chapter of this book, the
engineering question has mostly been answered: a team can build a
software KB today with parsers, a vector index, a small code graph, a
disciplined prose layer, and a maintenance loop. The open question is
no longer *"can LLMs help with repository knowledge?"* but *"where
should the structure live, who maintains it, and what is the model's
job once the structure exists?"*

The three papers that best frame that question arrived in quick
succession. Zhu et al. survey LLMs for KG construction and reasoning
and find a pattern that should make system builders pause: frontier
models are often more convincing as **reasoners over structured
context** than as few-shot extractors of structure from raw inputs
{cite}`zhu2024llmsknowledgegraphconstruction`. RepoAgent turns
repository documentation into a first-class systems problem with global
structure analysis, documentation generation, and update
{cite}`luo2024repoagentllmpoweredopensourceframework`. CGM then goes a
step beyond retrieval-time graphs and asks whether repository graph
structure should enter the model itself; its answer is yes
{cite}`tao2025codegraphmodelcgm`.

Taken together, those papers turn "AI for codebase knowledge" from a
bag of tactics into a research program. This chapter names the parts of
that program that still feel unsettled.

## What

This chapter uses **outlook** in a narrow sense: not market prediction,
but the design choices that remain open even if one accepts the book's
thesis. Five questions matter most.

1.  **Extraction vs reasoning.** Which facts should still be derived by
    deterministic parsers, and which can be left to an LLM at query
    time?
2.  **Generation vs maintenance.** Is repository documentation mainly a
    synthesis problem, or is it a lifecycle problem whose centre of
    gravity is incremental update?
3.  **External graph vs integrated graph.** Should the code graph stay
    outside the model as a retriever-side substrate, or move into the
    model's attention and hidden state?
4.  **Long context vs selective context.** As context windows get
    larger, does retrieval become less important, or merely more
    selective?
5.  **Benchmark wins vs operational trust.** What should teams optimise:
    SWE-bench-style resolution rate, documentation coverage, citation
    precision, or human review load?

The rest of the chapter argues that these are not five unrelated
questions. They are five views of the same systems boundary.

## How

### 1. The field is converging on a split architecture

Zhu et al. provide the cleanest empirical justification for a design
principle that this book treated as engineering common sense: **do not
ask the LLM to be your only extractor**. Their survey finds that large
models are often better at downstream reasoning over KG context than at
few-shot extraction of entities, relations, and events
{cite}`zhu2024llmsknowledgegraphconstruction`. For software KBs, that
translates almost directly into a division of labour:

- parsers extract entities, spans, and stable identifiers;
- verifiers check links, anchors, and provenance;
- retrievers assemble the smallest useful evidence set;
- the LLM explains, summarizes, refuses, and routes.

This split remains attractive even if models improve. The stronger the
model gets, the more valuable it becomes to spend its budget on
high-level synthesis instead of repetitive structural work that the
compiler or parser can already do deterministically.

### 2. Repository documentation is a maintenance problem

RepoAgent is important not because it proves LLMs can write Markdown,
but because it treats **repository-level documentation as a pipeline**
with explicit stages for structure analysis, generation, and update
{cite}`luo2024repoagentllmpoweredopensourceframework`. That aligns with
the book's Parts II through IV more closely than a generic "AI docs"
tool does. The open problem is not merely page quality; it is how to
keep documentation synchronized with a moving repo without producing a
review burden larger than the benefit of the docs themselves.

This is why the book spent so much space on incremental sync, tuple
metadata, and publish gates. In practice, the teams that fail at
software KBs rarely fail because the first draft is bad. They fail
because update discipline is missing, review queues stall, or citations
quietly rot.

### 3. Graphs are moving from retrievers into models

CGM is the clearest signal so far that repository graphs are not merely
an implementation trick for external tools. It integrates repository
graph structure into the model's attention mechanism and reports
repository-level gains when paired with graph-aware retrieval
{cite}`tao2025codegraphmodelcgm`. That result does not invalidate the
book's external-graph design; it clarifies its upgrade path.

Today, keeping the graph outside the model has three pragmatic
advantages:

- the graph is inspectable and queryable by ordinary tools;
- updates can happen on every commit without re-training a model;
- multiple agents and retrievers can share the same substrate.

But CGM suggests that a mature software KB stack may eventually become
**bi-level**: an explicit external graph for operations and provenance,
plus a graph-aware model that consumes the same structure more
efficiently than text-only prompting can.

### 4. Long context does not remove the need for retrieval

Bigger windows change *where* retrieval pressure sits, but not whether
it exists. A long-context model can ingest more files at once, yet a
repository still contains many signals that should not be flattened into
raw text: call edges, entity identity, review status, provenance,
staleness, and policy. The real competition is not "RAG versus long
context"; it is **typed context assembly versus undifferentiated
stuffing**.

That is especially true for software repositories because many useful
queries are not "summarize these files" queries. They are "which symbol
actually owns this behavior?", "what changed since the ADR?", and "is
this answer safe to trust?" questions. Those require selection,
ordering, and policy-aware filtering even when a model could, in
principle, read more bytes.

### 5. Benchmarks still underspecify operational quality

CGM's SWE-bench Lite result is valuable because it gives the field a
shared repository-level target {cite}`tao2025codegraphmodelcgm`.
RepoAgent's documentation evaluations matter because they force system
builders to measure page quality, not just code patching
{cite}`luo2024repoagentllmpoweredopensourceframework`. Yet neither kind
of benchmark captures several properties this book treats as
non-negotiable:

- whether every answer carries resolvable `file:line` citations;
- whether stale pages are down-ranked or blocked from publication;
- whether update cost scales with commit rate instead of KB size;
- whether human review remains bounded as the repo grows.

The next generation of benchmarks for software KBs should measure all
four. A system that scores well on patch resolution but cannot tell you
which commit its answer came from is impressive, but still not ready to
be an organization's memory.

## Example

A realistic three-step roadmap for a team that wants to follow the
research frontier without betting the company on it:

| Stage | Keep fixed | Add experimentally | Success criterion |
|:--|:--|:--|:--|
| **1. Durable KB** | parser, stable IDs, hybrid retrieval, citations | none | engineers get grounded answers with low review overhead |
| **2. Continuous docs** | same retrieval stack | RepoAgent-style doc-update loop over selected page classes | candidate pages per commit stay small and reviewable |
| **3. Graph-aware models** | external graph remains source of truth | CGM-style graph-conditioned reader or reranker | better repo-level task accuracy *without* losing provenance |

The sequence matters. Stage 3 is tempting, but it should sit on top of
Stage 1 and Stage 2 rather than replace them. A graph-aware model with
no stable provenance discipline is a demo. A modest retriever with
incremental maintenance and trustworthy citations is already a system.

## Conclusion

The most durable lesson from the recent literature is not that one
architecture has won. It is that the space has become legible. Zhu et
al. tell us to separate extraction from reasoning. RepoAgent tells us
that repository knowledge lives or dies by the update loop. CGM tells
us that code graphs are important enough to move closer to the model.

The book's wager is therefore a conservative one: build the explicit KB
first, because explicit structure is inspectable, maintainable, and
governable. Then let better models consume that structure in richer
ways. If the field is right, future systems will look less like
"paste the repo into a bigger window" and more like **repository memory
stacks**: parser-backed, graph-shaped, incrementally maintained, and
LLM-mediated only where LLMs are actually the best tool.

## References

```{bibliography}
:filter: keywords % "governance"
```
