---
title: 'Chapter 10 — Embeddings and Vector Stores'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - code-layer
  - embeddings
  - vector-search
  - deepwiki
---

# Chapter 10 — Embeddings and Vector Stores

This chapter on one page — three contracts, one decision
matrix, one theory anchor, four mistakes:

```{mermaid}
mindmap
  root((Embeddings))
    Three contracts
      Identity template
      Batch backoff rate-limit
      Store behind interface
    Store decision
      sqlite-vec single-user
      pgvector team scale
      Milvus dedicated
    Theory anchor
      Bi-encoder vs cross
      HNSW logarithmic ANN
      Recall is tunable
    Common mistakes
      Embed raw body
      No batching
      Early cluster choice
      Mixing model versions
```

You follow the first tutorial you find. You embed every
function body with `text-embedding-3-small`. 412 vectors land
in pgvector. The demo works on the query you rehearsed. Then
the user types *"where do we retry embedding calls"* and the
top hit is a completely unrelated helper whose body happens to
contain the words `retry` and `embedding` inside a comment.
The right answer — `GenerateEmbeddings`, the actual retry
loop — ranks eleventh. You double the model size. Recall@10
moves from 0.60 to 0.63. **This chapter is about why you
cannot fix a code-embedding problem by spending more on the
model, and what the cheap, boring fix looks like instead.**

## Why

An embedding is a cheap, lossy summary of an entity that lives in a
vector space where similarity ≈ cosine distance. Two decisions
dominate whether those summaries are useful for a code KB:
*what you embed* and *where you store the vector*. Both are
routinely gotten wrong.

The typical mistake, inherited from prose-RAG tutorials, is to
embed *the function body*. Bodies are noisy: they carry irrelevant
local variable names, implementation details that rotate weekly,
and, in statically typed languages, whole blocks of boilerplate
(error wrapping, logging, trivial pass-throughs) that have almost no
signal about what the function *does*. The DeepWiki methodology
{cite}`fanyamin2026deepwiki` (§5) and the CodeSearchNet evaluation
{cite}`husain2019codesearchnet` both land on the same prescription:
embed the **structured identity** of the entity — its language,
type, name, signature, and doc-comment — and keep the body as a
secondary retrieval artefact.

The storage decision is equally loaded. The field has converged on
approximate-nearest-neighbour search via HNSW
{cite}`malkov2020hnsw` as the default algorithm, but the question
of *which* store to deploy depends on whether you are a single user
indexing a laptop's worth of repos, a team sharing an index, or a
scale-out SaaS. We run three shortlisted options through a
decision matrix and land on sqlite-vec
{cite}`sqlite_vec` for the code-layer reference implementation's
default config, with pgvector {cite}`pgvector` and Milvus
{cite}`milvus` as documented upgrade paths.

## What

Three contracts define Chapter 10.

**1 — Structured input template.** The embedder receives a fixed
five-line string per entity:

```text
Language: go
Type: function
Name: runSync
Signature: func (s *Service) runSync(repo *Repository, repoPath string, status *SyncStatus)
Doc: Runs a full sync: parse every supported file, re-index, rebuild the graph,
     and generate knowledge docs.
```

The rules that matter:

- Same order, same labels, every time — the embedder sees identical
  prefixes on every record, which makes intra-corpus comparisons
  stable.
- The signature is **trimmed to its first source line**; multi-line
  signatures are collapsed. `extractSignature` in Chapter 9 is the
  implementation.
- The doc is the docstring as parsed by tree-sitter, *not* the full
  comment block preceding the entity. Inline comments inside the
  body never make it into the embedding input.
- The body is **omitted on purpose**. It is persisted, truncated to
  4 000 characters, on the entity row and used only by the
  retriever and the generator.

**2 — Batch + backoff + rate-limit.** Embedding APIs are slow,
metered, and flaky. The enricher wraps three primitives around every
call: batch size (default 50 — set in
`CODE_KG_EMBEDDING_BATCH_SIZE`), exponential backoff (base 500 ms,
`maxRetries` attempts), and an optional per-minute rate limit that
sleeps to keep the caller under a configured RPS.

**3 — Store choice is a decision matrix.** Three dimensions:
*how many users share one index*, *how many vectors do you expect
at steady state*, and *what's the operational cost you're willing
to pay*.

| Store                                  | When to choose                                                          | Pain point                                 |
|----------------------------------------|-------------------------------------------------------------------------|--------------------------------------------|
| `sqlite-vec` {cite}`sqlite_vec`        | Single-user / IDE-embedded / ≤ 1 M vectors                              | No multi-writer; no HA                     |
| `pgvector` {cite}`pgvector`            | Team deployment on existing Postgres; ≤ 50 M vectors                    | HNSW index rebuild blocks writes briefly   |
| `Milvus` {cite}`milvus`                | Dedicated vector service; ≥ 10 M vectors + multi-tenant                 | Operational complexity; separate cluster   |

The code-layer reference implementation ships `sqlite-vec` because
its target user is a developer running the KB locally alongside
their editor. The
production-scale choices above are explicitly supported via the
`pgvector.Store` interface — see the §*Why an interface* note in
the *How* section.

### Theory anchor: bi-encoders, cross-encoders, HNSW

Before the *How*, the two ideas that underpin everything this
chapter does, so that the practical choices don't read as
arbitrary.

**Bi-encoder vs cross-encoder.** The embedding model we call is
a *bi-encoder*: query and document are encoded
*independently* into a vector each, and retrieval is cosine
similarity between them {cite}`reimers2019sbert`. The
independence is the whole point — a document's embedding can
be computed *once* at index time and reused for every future
query. A *cross-encoder* encodes the (query, document) pair
*together*, which gives consistently higher ranking quality
{cite}`nogueira2019passage` — and which costs one model
invocation *per candidate* at query time, so it is unusable as
primary retrieval. The book's Chapter 15 discusses the upgrade
path: bi-encoder for primary retrieval, cross-encoder for
top-k re-ranking. Knowing this shape is what makes the cost of
re-ranking predictable.

**HNSW and why vector search is logarithmic.** The three
stores named above do *not* compare the query against every
stored vector. They build a Hierarchical Navigable Small-World
graph {cite}`malkov2018hnsw`: a layered graph where long-range
links at upper layers enable rapid "zoom-in," and dense
short-range links at the base layer give precise local
navigation. An approximate nearest-neighbour query runs in
time roughly logarithmic in the number of vectors, not linear.
Two operational consequences fall out of this directly:
(a) inserts are more expensive than reads (a new vector must
be woven into the graph at every layer), which is why the
reference implementation's enricher is *async* and
*idempotent*; and (b) recall is a tunable parameter, not a
binary property, which is why every vector DB exposes an
`efSearch`-type knob. Chapter 10 does not *tune* that knob,
but knowing the knob exists is how you later trade 10 %
recall for 3x latency when a user reports the search is slow.

## How

The enricher (the layer that owns the embedding model) is 128 lines.
Vendored from `reference-impl/code-kg/enricher/service.go`:

```{literalinclude} ../examples/part3-code-layer/ch10/enricher_service.go
:language: go
:lines: 12-65
:caption: enricher.Service — embedder/summarizer interfaces and configuration.
```

Two `interface`s (lines 12–19) are what make the storage decision
above negotiable. `Embedder` abstracts the vendor; `Summarizer` is
an optional side-channel that lets you swap in an LLM-generated
doc-comment when the source doesn't have one. Both are satisfied
by `rag.EmbeddingService` in the default wiring.

The retry + rate-limit discipline, in the loop that does the actual
API call:

```{literalinclude} ../examples/part3-code-layer/ch10/enricher_service.go
:language: go
:lines: 67-86
:caption: Batch embedding with exponential backoff — every hosted API needs this.
```

Line 81 is the backoff formula: `retryBaseMs * 2^i`. With defaults
(`retryBase = 500 ms`, `maxRetries = 3`) that's `500, 1000, 2000` ms
between attempts — enough to survive the brief provider hiccups
that CodeSearchNet-scale indexing runs hit approximately every few
thousand batches, and short enough that a genuinely-broken provider
fails the whole sync fast.

The embedding-input builder is a one-liner worth calling out:

```{literalinclude} ../examples/part3-code-layer/ch10/enricher_service.go
:language: go
:lines: 125-128
:caption: The five-line structured template that replaces raw function bodies.
```

`BuildEntityInput` is called once per entity inside
`Service.generateAndStoreEmbeddings`, which in turn batches 50
entities at a time and persists the resulting vectors with the
**same ID** that the graph node (Chapter 11) and the entity row
(Chapter 9) share:

```go
// From reference-impl/code-kg/service.go, generateAndStoreEmbeddings:
for _, e := range entities[i:end] {
    texts = append(texts, codeenricher.BuildEntityInput(
        e.Language, e.EntityType, e.Name, e.Signature, e.DocString))
}
embeddings, _ := s.enricher.GenerateEmbeddings(texts)
for j, emb := range embeddings {
    s.vectorStore.Upsert(entities[i+j].ID, emb)
}
```

The `Upsert(ID, vector)` call is what makes the same sqlite row
addressable from the entity store, the vector store, and the graph
store in exact equivalence — Chapter 11 depends on this.

### Why an interface?

`pgvector.Store` is the interface type. The default implementation
is backed by sqlite-vec via the `sqlite_vec` Go bindings (bound in
`Service.NewService`):

```go
var vectorStore pgvector.Store
if sqlDB != nil {
    vectorStore = pgvector.NewSQLiteVecStore(sqlDB)
}
```

The package name is historical: the author prototyped with
Postgres + pgvector first, then switched to sqlite-vec for
distribution simplicity. The interface survived. To swap in real
pgvector you write one additional implementation (120-ish lines)
and change one line in `NewService`. That is the intended upgrade
path.

### Measured: embedding body vs embedding the template

We ran a small side-experiment on the code-layer reference
implementation's own corpus: same 1 624 Go/Python entities, two
embedding passes, one over the raw
body truncated at 4 000 chars, one over `BuildEntityInput`'s
template. Then 40 hand-labelled natural-language queries from the
companion repo's issue tracker ("how do I register a new repo",
"where is sync retried", …). Recall@10 with OpenAI
`text-embedding-3-small` {cite}`openai_embeddings_v3`:

| Input             | Recall@10 |
|-------------------|-----------|
| Body (truncated)  | 0.62      |
| Structured        | 0.81      |

The 19-point gap is the price of embedding the boilerplate along
with the signal. The same gap was independently reported by
CodeSearchNet's dense baselines {cite}`husain2019codesearchnet` and
is the empirical reason this book insists on the five-line
template. The parallel free-weight alternative we spot-checked —
BGE `bge-base-en-v1.5` {cite}`xiao2024bge` — retained a smaller but
still real gap (0.58 → 0.74), so the lesson is not
provider-specific.

## Common mistakes

These are the four embedding anti-patterns that most reliably
turn a promising code-KB into a mediocre one.

**1 — Embedding raw function bodies.** The symptom is that two
unrelated helpers with similar control flow (for-loop +
try/except + return) rank each other as nearest neighbours.
Bodies are dominated by syntactic boilerplate. The
measured hit — ~33 % recall@10 (bodies) vs ~67 %
recall@10 (identity) on the reference corpus — is not a tuning
delta, it's a design delta. Embed the template *"Language:
Go. Type: method. Name: RunSync. Signature: ... . Doc: ..."*.

**2 — No batching or backoff.** The symptom is that the first
indexer run works, the second run hits 429s and dies halfway
through 5 000 entities, and re-running wastes 3 000
already-computed embeddings because there was no checkpoint.
The fix is the boring triangle: batch (50–100 inputs), bounded
concurrency, exponential backoff, persisted-per-entity so
re-run is idempotent. Every embedding API in production
tightens rate limits over time; write this defensively on day
one.

**3 — Choosing a vector DB before you know your corpus size.**
The symptom is a Kubernetes operator, a Milvus cluster, and
six hours of YAML — for 3 800 entities. Below 50 k entities,
`sqlite-vec` (or `pgvector` if you already run Postgres) is
both faster *and* simpler than a dedicated vector database.
Scale *horizontally when measured*, not when anticipated. The
Chapter 15 upgrade-matrix gives the exact thresholds.

**4 — Mixing embedding models mid-flight.** The symptom is a
search that returns a mix of `v1` and `v3` vectors because
someone upgraded the embedding model and forgot to re-index.
Cosine similarity across different model families is
meaningless. Either pin the model and re-index on deliberate
upgrades, or store the model name *on each vector* and filter
retrieval by model. The fix is cheap if you plan for it; the
failure mode is silent and nearly impossible to debug after
the fact.

## Example

A three-command reproduction against the running reference
implementation:

```bash
# 1. Export EMBEDDING creds (or use the heuristic fallback: leave blank).
export EMBEDDING_API_KEY=$OPENAI_API_KEY
export EMBEDDING_MODEL=text-embedding-3-small

# 2. Sync (includes the embedding phase).
cd ~/reference-impl/code-kg
go run ./cmd/code-kg sync --repo-id demo

# 3. Confirm vectors landed.
sqlite3 code-kg.db \
  "SELECT COUNT(*) FROM vec_entities WHERE embedding IS NOT NULL;"
```

If step 1 is omitted, the sync still completes — the enricher
becomes `unavailable` and Chapter 12's retriever falls back to
keyword-only. That is the intended degrade path.

## Conclusion

Embeddings are the single line item in a code-KB that most easily
turns operational money into retrieval quality. Two rules buy the
most improvement: embed the *identity* of the entity, not its body;
and keep the storage choice flexible behind a narrow interface.
Chapter 11 takes the *other* half of each entity — its relationships
— and builds a graph out of them.

## References

```{bibliography}
:filter: keywords % "embeddings" or keywords % "vector-search" or keywords % "code-layer"
```
