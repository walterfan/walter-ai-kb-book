---
title: 'Chapter 12 — Hybrid Retrieval and RRF'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - code-layer
  - search
  - ir
  - deepwiki
---

# Chapter 12 — Hybrid Retrieval and RRF

This chapter on one page — three tiers, one upgrade path, and
four mistakes that undo the design:

```{mermaid}
mindmap
  root((Hybrid Retrieval))
    Three tiers
      Vector primary
      Keyword fallback
      Graph expansion
    Query routing
      Semantic goes vector
      Identifier goes keyword
      Structural goes graph
    Theory anchor
      Ranks not scores
      RRF formula
      Upgrade path
    Common mistakes
      Score-level fusion
      Run all three always
      Graph as primary
      Caching at wrong layer
```

Three engineers, three complaints. Alice says the search is
too literal — she typed *"how does the sync retry"* and got a
500-line file named `retry_utils.go` with nothing to do with
sync. Bob says it's too fuzzy — he typed `runSync` verbatim
and the function of that exact name ranked *fourth*. Carol
says it refuses to answer *"who calls `runSync`"* at all —
and both Alice and Bob are right and Carol is also right,
because all three are asking different questions that need
different retrievers. **This chapter is about the three-tier
strategy that routes each query to the stack best suited to
it — and how Reciprocal Rank Fusion eventually replaces the
fallback with a single, consistently good answer.**

## Why

Chapter 10 gave us a vector index that is excellent at fuzzy,
natural-language queries and merely adequate at identifier
queries. Chapter 11 gave us a graph that is excellent at
structural queries and near-useless at natural-language queries.
The retriever in Chapter 12 is the thin layer that routes each
query to the stack best suited to answer it — and, when in doubt,
combines their answers.

Three empirical facts drive the design:

1.  *Identifier queries beat vector recall.* When a developer types
    `entityID`, a BM25-style {cite}`robertson2009bm25` scorer
    outperforms a dense model by a wide margin. CodeSearchNet
    {cite}`husain2019codesearchnet` documented this; every
    subsequent code-RAG survey {cite}`gao2023retrieval` has
    repeated it.
2.  *Structural queries beat both.* Anything of the form *"who
    calls X"*, *"what implements Y"*, *"what does Z return"* is
    trivially served from the graph (Chapter 11) with recall = 1.
3.  *Fuzzy queries benefit from fusion.* Reciprocal Rank Fusion
    {cite}`cormack2009rrf` combines ranked lists from heterogeneous
    retrievers using only their ranks — no score calibration
    needed. Hybrid search over prose has been shown to outperform
    either system alone; GraphRAG {cite}`edge2024graphrag` extended
    the principle to graph traversal as the third retriever.

Recent repository-level work clarifies what this means for code. Zhu et
al.'s survey of LLMs for KG construction and reasoning argues that
frontier models are generally stronger as **reasoners over structured
evidence** than as few-shot extractors of that evidence from raw inputs
{cite}`zhu2024llmsknowledgegraphconstruction`. In Chapter 12 terms, the
retriever's job is therefore not just "find similar text", but
"assemble a small typed evidence set the model can reason over without
guessing." CGM sharpens the same claim at repository scale: once code
graphs become part of the model's input or attention, repository-level
tasks improve {cite}`tao2025codegraphmodelcgm`. Our hybrid retriever is
the external, operations-friendly version of that same bet.

The DeepWiki methodology {cite}`fanyamin2026deepwiki` (§7)
prescribes the exact strategy we implement today: **vector-primary,
keyword-fallback, graph-expansion**, with fusion-based hybrid search
left as a marked upgrade path.

## What

The retriever has three tiers.

**1 — Vector primary.** If the embedding service is configured and
the vector store has entries for this repo, we query by KNN over
the embedding of the user's query (Chapter 10). Returns up to
`TopK` entity IDs in similarity order.

**2 — Keyword fallback.** If (a) the enricher is not available
(no embedding API key), (b) the vector KNN call fails, or (c) the
vector result is empty, we fall back to an in-process keyword
ranker. Entity *name* matches are weighted 3× body matches.

**3 — Graph expansion.** After the vector/keyword stage returns its
seed set, 1–2 hops of the KB graph are optionally added so the
generator sees not only the best-matching entity but its callers,
its callees, and (for a class) its methods. This is the graph's
payoff at query time, not just at build time.

That third tier is where Chapter 12 touches **graph-RAG** proper. The
graph is not a decoration on top of vector search; it is the mechanism
that turns a semantically matched seed into a *query-shaped local
subgraph*. GraphRAG in document QA uses entity and community structure
to assemble context {cite}`edge2024graphrag`; in a code KB the same
pattern becomes stricter and more local: start from an entity, expand
typed edges such as `CALLS`, `IMPLEMENTS`, and `RETURNS`, and pass the
result downstream as evidence rather than prose alone.

The upgrade path, explicitly flagged in the codebase, is to
combine the vector and keyword lists via Reciprocal Rank Fusion
{cite}`cormack2009rrf` — giving the retriever BM25's identifier
sensitivity *and* dense retrieval's generalisation, simultaneously.
We have not shipped it; Chapter 15 explains why (measured) the
fallback strategy is Pareto-dominant for our current corpus size.

### Theory anchor: RRF fuses ranks, not scores

The single load-bearing idea behind every serious hybrid
retriever shipped since 2009.

**The problem with weighted-score fusion.** Multiplying a
cosine similarity (range $[-1, 1]$) by $0.7$ and a BM25 score
(range $[0, \infty)$, shifts with IDF and corpus length) by
$0.3$, and adding them, produces a number that is *not
comparable across queries*. The same document can score 0.82
on one retriever and 14.7 on another while being the same
document for the same query; the weighted sum reflects the
*retrievers' score distributions*, not the document's
relevance. Practitioners who do this end up quietly tuning
weights per-corpus and per-model-version, then watching their
tuning evaporate on the next upgrade.

**Why ranks are different.** Cormack, Clarke and Büttcher
{cite}`cormack2009rrf` observed that the *position* a
document occupies in each retriever's output — its rank — is
a dimensionless quantity bounded by $k$ (the top-k cutoff).
Ranks are therefore comparable across retrievers *without any
per-retriever calibration*. Reciprocal Rank Fusion simply
sums reciprocals:
$$\text{RRF}(d) = \sum_{r \in R} \frac{1}{k_0 + \text{rank}_r(d)}$$
where $k_0 \approx 60$ is a small constant that damps the
weight of very-high-rank documents. The original paper shows
RRF matching or beating every learning-based rank-fusion
method of its era; the intervening fifteen years have not
produced a consistently better *simple* fusion.

Chapter 12's practical take: once the reference
implementation's corpus grows past the size where the
fallback strategy still wins (Chapter 15 measures the
threshold), RRF is the surgical upgrade. Replace
`vector_empty ? keyword : vector` with
`RRF(vector.top(50), keyword.top(50)).top(TopK)`. The
implementation is fifteen lines; the theoretical guarantee is
why those fifteen lines outperform a week of weight-tuning.

## How

The keyword ranker is the simplest, most boring component in the
entire KB — and it has survived every refactor. Vendored in full
from `reference-impl/code-kg/retriever/keyword.go`:

```{literalinclude} ../examples/part3-code-layer/ch12/retriever_keyword.go
:language: go
:lines: 1-50
:caption: RankByKeyword — name hits count 3× body hits, then bubble-sort to topK.
```

Two things the listing makes concrete:

- Line 27 (name match) weighs **3 points**, line 30 (body match)
  weighs **1 point**. That 3:1 ratio — not some BM25-calibrated
  value — is what mimics the effect of IDF-style identifier
  boosting without the implementation burden. The project uses
  this for both Chapter 7's prose index and Chapter 12's code
  fallback; *consistency is more valuable than tuning per layer*.
- Lines 38–44 are a bubble sort because `topK` is small (≤ 50 in
  all measured code paths). We deliberately keep it O(n²); the
  `sort.Slice` refactor would shave microseconds on a 50-element
  slice and cost an import. This is the canonical
  engineering-grade call the book makes over and over: pick the
  obvious, boring implementation when the scaling ceiling is
  low.

### The orchestration

The `Search` method in the reference implementation's `Service`
stitches the three tiers:

```{literalinclude} ../examples/part3-code-layer/ch12/service_search.go
:language: go
:lines: 486-596
:caption: Search orchestration — vector primary, keyword fallback, answer generation.
```

Four lines matter most:

- **494** — the tier-selection condition: both the enricher and
  the vector store must be available. If either is nil, we never
  even try the vector path; we skip straight to the fallback
  (505). This is what makes a locally-running KB without any API
  keys still useful.
- **498** — on any vector error, we downgrade to the keyword
  fallback. The downgrade is logged at Warn level, so operations
  can detect chronic embedding failures by log rate.
- **517–562** — the vector path itself: embed the query,
  `vectorStore.Search(queryEmb, TopK)` (a KNN call), pull the
  matching `Entity` rows by ID, preserve the similarity order
  (`idOrder` map). The database filter is applied *after* the
  KNN; we trade a small amount of KNN recall for the ability to
  filter by `repo_id` or `entity_type`.
- **564–575** — the fallback: pull every candidate from the DB
  (filtered), run the keyword ranker above. This is trivially
  slow on large corpora; the §*Upgrade path* section below
  explains how we plan to change it.

The result set flows into `generateAnswer` — the subject of
Chapter 13 — which calls the LLM with a prompt that obliges it to
cite `file:line` on every claim it returns.

### Graph expansion (separate entry point)

Graph expansion is not folded into the default `Search` call today;
it is invoked explicitly through the `AnalyzeEntity` /
`GraphQuery` service methods, which take a seed entity ID and a
`MaxHops`. The reason for separation: the graph query is *much*
more expensive than vector KNN (a Cypher query with
`shortestPath` traversal vs. an HNSW lookup), so we let the caller
decide when to pay the cost. The CLI frontends
(`code-kg callers <name>`, `code-kg callees <name>`) are thin
wrappers around this.

### Upgrade path: RRF

When the corpus grows past (say) 50 000 entities, the fallback
keyword ranker's full-table scan stops being acceptable. The
upgrade path is:

1.  Build a token-level inverted index over `(name, body)` during
    sync (a natural extension of the existing `searchTerms` map in
    Chapter 7's wiki index).
2.  Replace `rankByKeyword` with a BM25 {cite}`robertson2009bm25`
    scorer that consults the inverted index.
3.  Fuse vector and keyword ranks via Reciprocal Rank Fusion
    {cite}`cormack2009rrf`: `score(d) = Σ_{retriever} 1/(k +
    rank(d))` with `k = 60` as the standard starting value.

Gao et al. {cite}`gao2023retrieval` surveys the full hybrid
landscape; GraphRAG {cite}`edge2024graphrag` adds the graph as a
third ranked list into the same fusion. HippoRAG
{cite}`gutierrez2024hipporag` shows the same pattern can be
extended with associative memory for long-horizon QA. The
interfaces in the retriever package are deliberately narrow so
that these upgrades drop in without touching the service or the
generator.

### Graph-RAG as the bridge to repository tasks

It is tempting to treat graph expansion as a niche answer to *"who
calls X?"*. That undersells it. Once the retriever can return a ranked
seed set plus a bounded neighbourhood with edge labels, it becomes a
general **repository-task substrate**:

- a tool-using IDE agent can call the retriever, then ask follow-up
  questions over the returned neighbourhood;
- an agentless batch solver can consume the same assembled context in a
  single prompt or model invocation;
- a graph-integrated reader such as CGM can use the same neighbourhood
  as a structured prior instead of reconstructing it from raw files
  {cite}`tao2025codegraphmodelcgm`.

This is the reason the chapter keeps graph expansion outside the
generator and inside retrieval. The graph is not merely post-processing
for a better answer; it is the control point where repository context
stops being "more text" and starts being *typed evidence*.

## Example

Three queries run against the same synced KB (Chapter 10's
example) — each designed to hit a different tier:

```bash
# Tier 1 — vector primary. Fuzzy, natural-language.
code-kg search --repo-id demo "where do we retry embedding calls"
# → top hit: enricher.Service.GenerateEmbeddings
#   reference-impl/code-kg/enricher/service.go:67

# Tier 2 — keyword fallback. Identifier-heavy.
code-kg search --repo-id demo "RankByKeyword bubble sort"
# → top hit: retriever.RankByKeyword
#   reference-impl/code-kg/retriever/keyword.go:16

# Tier 3 — graph expansion (separate command). Structural.
code-kg callers --repo-id demo --name runSync
# → [TriggerSync, runIncrementalSync (recursion guard)] as in ch11.
```

Tier 1 succeeds even though the query shares few tokens with the
result — that is the dense-retrieval value. Tier 2 would lose to
Tier 1 badly on the fuzzy query, but wins on the identifier one.
Tier 3 is the only tier that can answer the structural question
with perfect recall.

## Common mistakes

Four retrieval-layer anti-patterns that come up even on teams
who otherwise built the earlier stages correctly.

**1 — Score-level fusion across stacks.** The symptom is a
function like `final_score = 0.7*cosine + 0.3*bm25`. This looks
principled; it is actually meaningless. Cosine similarities are
in [−1, 1], BM25 scores are unbounded above and shift with
corpus statistics. The *same document* can have cosine = 0.82
and BM25 = 14.7 or BM25 = 1.4 depending only on the corpus
it shares. The fix is rank-level fusion (RRF): `score = sum_r
1/(k + rank_r(d))`. It fuses *ranks*, which are comparable
across stacks, not *scores*, which are not.

**2 — Treating all three tiers as the same query type.** The
symptom is a pipeline that always runs vector + keyword + graph
in parallel for every query, then picks top-k from the union.
You pay 3x the latency to rank three questions that each
expected a different answer. The fix is the two-stage design
of Chapter 12: a classifier (*is this a structural query?*)
routes to graph-first; everything else runs vector with a
keyword fallback *only when vector results are empty*.

**3 — Graph expansion as primary retrieval.** The symptom is a
query *"how does the sync retry work"* that returns a graph
walk from a hand-picked seed node — and misses every
legitimate hit because the seed was wrong. Graph is for
follow-up questions after a seed is already found
(*"who else calls this"*), not for first-pass semantic
matching. Keep graph expansion on a separate endpoint with a
*required* seed-entity-ID parameter. That one design choice
prevents 80 % of misuse.

**4 — Caching at the wrong layer.** The symptom is an
in-memory LRU cache of `query → top-k entityIDs` that goes
stale the moment a commit lands, because the cache has no
hook into the indexer. If you must cache, cache the *embedding*
of a query string (stable) or the graph *adjacency* at repo-ID
+ commit-SHA granularity (also stable). Never cache the final
ranked list unless you invalidate on every write.

## Conclusion

A three-tier retriever is the minimum viable design for a KB that
must answer natural-language, identifier, and structural queries
alike. The code-layer reference implementation stays small because
each tier is either a one-screen component (keyword) or a thin
wrapper over a dedicated store (vector / graph). RRF and BM25 are
the documented upgrade paths; we ship neither today, and Chapter 15
will measure whether that is still the right call.

Chapter 13 closes Part III with the last stage: turning the
retriever's structured context into a citable answer.

## References

```{bibliography}
:filter: keywords % "search" or keywords % "ir" or keywords % "code-layer"
```
