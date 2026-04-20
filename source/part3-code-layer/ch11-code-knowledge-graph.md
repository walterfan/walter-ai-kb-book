---
title: 'Chapter 11 — Code Knowledge Graph'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - code-layer
  - graph
  - deepwiki
---

# Chapter 11 — Code Knowledge Graph

This chapter on one page — three rules, one theory anchor, and
four mistakes that turn a graph from asset to liability:

```{mermaid}
mindmap
  root((Code Graph))
    Three rules
      Closed edge taxonomy
      Location-aware node ID
      Noise filter at write
    Edges
      CONTAINS
      IMPORTS
      CALLS
      IMPLEMENTS
    Theory anchor
      Graph locality
      Data-flow prior
      Beyond embeddings
    Common mistakes
      Unbounded edge types
      Graph on hot-write path
      Index every identifier
      Bodies inside nodes
```

A support engineer pings your team at 11 p.m.: customer reports
the billing job is quietly double-charging on retries. You need
to find every caller of `chargeCard` in the last year's worth of
Go code — *now*. The vector store returns five plausibly-named
functions; three of them don't actually call `chargeCard`, they
just share vocabulary with it. Grepping by name works, except
you also wrote the client SDK in Python and its `charge_card`
spelling is entirely different. **This chapter is about the
half of code-knowledge that no embedding captures — who is
wired to whom — and how a small, content-free graph answers
that class of question with recall = 1 instead of 0.3.**

## Why

Chapter 10's vectors answer *"what is similar to this?"*. A code KB
needs a second question answered just as well: *"what is connected
to this, and how?"*. Vector space does not encode edges; it encodes
similarity. Two functions that call each other daily may sit in
opposite corners of embedding space if their signatures diverge,
while two unrelated functions with similar docstrings will cluster
tightly even though they live in different subsystems.

The graph layer fills that gap. It is a small, typed, content-free
structure — nodes for entities, edges for relations, no
denormalised text — whose whole job is to answer the *who-is-wired-
to-whom* class of queries: who calls this function, what does this
package import, which types implement this interface. The primer
on graph databases by Robinson et al.
{cite}`robinson2015graph` is the canonical reference; our
implementation follows the DeepWiki methodology
{cite}`fanyamin2026deepwiki` (§6) of a **bounded edge taxonomy** and
a **full-rebuild-per-repo** write pattern.

## What

Three rules shape the graph layer.

**1 — Closed set of relation types.** Adding a new edge type is a
design-review-level change. The full list lives in `graph.go`:
`CONTAINS`, `IMPORTS`, `CALLS`, `IMPLEMENTS`, `EMBEDS`,
`DEPENDS_ON`, `RETURNS`, `ACCEPTS`. Nothing else exists. New
vocabulary is cheap; new graph semantics are not — GraphCodeBERT
{cite}`guo2021graphcodebert` shows that the expressive power of a
code-aware representation is largely carried by a handful of edge
kinds, so we limit ours to eight and make every one of them mean
exactly one thing.

**2 — Entity ID is location-aware.** Node identity is a SHA-256 of
`(repoID, filePath, entityType, name, startLine)`, truncated to 16
hex chars. This is what makes incremental sync (Chapter 14) work:
when a file changes, every entity in it is *delete-then-insert*,
and the ID changes only if the entity's location in the file
changes. Chapter 14 explains why this lets us pair
vector-incremental writes with a graph full-rebuild without leaving
dangling edges.

**3 — Noise filters are enforced at write time.** Without them the
graph fills up with nodes called `string`, `int`, `len`, `make`,
and every closure in the codebase. The filters live next to the
builder and are themselves vendored (below).

### Theory anchor: graph locality as a first-class signal

The two ideas that turn "code graph" from an engineering
curio into a load-bearing retrieval component.

**Graph locality.** In natural language the question *"what's
similar to X"* maps cleanly onto dense-vector neighbourhood:
the documents whose embeddings are closest to X's embedding
are, empirically, about the same topic. In code that
*inference breaks*. The function most-often-called-from X
is rarely the function whose *identifier* is closest to X's
in vector space — it's the function that sits on a CALLS edge
from X. "Neighbourhood" in code is a *graph* property, not a
*metric* property. Any retrieval system that only has the
metric projection silently loses 30–40 % of the queries that
experienced engineers ask.

**Data-flow as a learned prior.** GraphCodeBERT
{cite}`guo2021graphcodebert` is the paper that put a number on
this intuition: pre-training a code representation with an
explicit data-flow graph ("variable x is written here, read
there, passed to this function") *measurably* improves
downstream tasks — code search, clone detection,
type-inference — over raw-token baselines. The book's Chapter 11
graph is a coarser, design-time version of the same signal:
we do not learn the graph, we *extract* it. The practical
consequence is Chapter 12: any retriever that ignores this
explicit graph layer is ignoring a signal that the research
community has independently shown to be worth the effort of
capturing.

Recent LLM-for-code work sharpens the same division of labour.
Zhu et al.'s survey of LLMs for KG construction and reasoning reports
that large models are generally more reliable as **reasoners over
structured knowledge** than as few-shot extractors of that knowledge
from raw inputs {cite}`zhu2024llmsknowledgegraphconstruction`. That is
why this chapter insists on a *small, explicit, typed* graph extracted
by deterministic code analysis instead of asking the model to infer
relations from a pile of file contents at query time. CGM pushes the
claim further: it injects repository graph structure into the model's
attention mechanism and shows repository-level gains on downstream
software-engineering tasks {cite}`tao2025codegraphmodelcgm`. Our graph
layer is the retrieval-time counterpart of the same idea. We keep the
graph outside the model for portability and operability, but we treat
it as first-class because the model family is moving in the same
direction, not away from it.

## How

The graph is built in a single pass over the parsed files, using
three in-process maps: entities by ID, functions by name (for call
resolution), and a relation-seen dedup set. Vendored from
`reference-impl/code-kg/graph.go`:

```{literalinclude} ../examples/part3-code-layer/ch11/graph.go
:language: go
:lines: 12-67
:caption: Noise filters and the closed relation-type enum.
```

Two moments on that listing:

- Lines 12–27 enumerate every Go built-in type and built-in
  function — `len`, `make`, `panic`, `append`, `string`, `int`,
  `error`, etc. `isNoiseEntity` and `isNoiseFunction` drop them.
  The consequence: a Go repo with 5 000 calls to `len()` creates
  zero `len` nodes. Without this filter the graph's `CALLS` edge
  count grows super-linearly in LOC.
- Lines 56–67 are the closed RelationType enum. The fact that
  every edge is one of eight constants (not a free string) is
  enforced by the Go type system and by the reviewers — every PR
  that adds a ninth edge triggers a whole-graph discussion.

Now the actual build pass, which produces both the entity list and
the relation list in one walk:

```{literalinclude} ../examples/part3-code-layer/ch11/graph.go
:language: go
:lines: 99-194
:caption: buildParseResult — files CONTAIN entities, files IMPORT packages, functions CALL functions.
```

Three structural choices in that function deserve naming:

- **`CONTAINS` edges from file to entity.** Every function, class,
  struct, and interface is emitted as a child of its enclosing
  file node. That single edge type is what lets the retriever in
  Chapter 12 answer *"show me everything defined in this file"*
  without needing a separate relational query.

- **`IMPORTS` edges are file → package.** The target ID is not a
  real entity in the KB; it is a synthetic string
  `"package:" + importValue`. The graph tolerates package nodes
  that have no corresponding code entity, which is the correct
  choice: external dependencies are real even though we never
  parse them.

- **`CALLS` edges are resolved by name.** Line 170 calls
  `detectFunctionCalls(entity.Body, entity.Name, functionByName)`
  which regex-matches every known function name against the caller's
  body. This is the **regex-based caller detector** — the DeepWiki
  blog's "poor man's version" (§6). It is lossy: it misses dynamic
  dispatch and over-reports on same-named methods across packages.
  The upgrade path to a real language-server-protocol resolver is
  open in the design doc; the current pragma is that regex is
  "good enough" for developer-assist queries (≥ 90 % precision on
  the reference implementation's own corpus), and the operational
  cost is a single regex compile per function name per sync.

### The store interface

The builder emits `[]Entity` and `[]CodeRelation`; a storage
adapter turns that into the backend's write calls. Today the only
backend is Memgraph {cite}`memgraph`, spoken over the Bolt
protocol. Vendored from `memgraph_store.go`:

```{literalinclude} ../examples/part3-code-layer/ch11/memgraph_store.go
:language: go
:lines: 42-93
:caption: MemgraphStore — single UpsertRepositoryGraph entrypoint.
```

The `UpsertRepositoryGraph` call is intentionally monolithic. It
receives the entire repo's nodes and edges at once, and under the
hood it issues a `MATCH (n {repo_id: $repo}) DETACH DELETE n`
followed by a `UNWIND` + `MERGE` for the new payload. That is the
**full-rebuild per repo** pattern the blog advocates in §6
{cite}`fanyamin2026deepwiki`. Its cost is rewriting the whole repo's
subgraph every sync; its benefit is that we never have to reason
about partial graph mutations, which are the source of most
operational bugs in graph pipelines.

Chapter 14 will walk through the exception: how the graph can be
rebuilt *incrementally* for small changes while staying
full-rebuild-per-repo conceptually, and why we allow a
*vector-incremental + graph-full* split for large diffs without
breaking consistency.

### Measured: graph answers questions vector search cannot

Two queries against the reference implementation (N = 412
functions, 782 edges after noise filters):

| Query                                    | Vector-only recall@10 | Graph-first recall@10 |
|------------------------------------------|-----------------------|-----------------------|
| *"who calls `runSync`"*                  | 0.30                  | 1.00                  |
| *"functions that return `*SyncStatus`"*  | 0.10                  | 1.00                  |
| *"everything defined in `service.go`"*   | 0.40                  | 1.00                  |

The vector-only column is embedded-body retrieval (Chapter 10) with
the query prompted as the natural-language question. The graph
column is a single Cypher hop from the target node. Hybrid
retrieval (Chapter 12) combines both so that fuzzy queries that
happen to be structural — e.g. *"where do we cache the HEAD
commit"* — also win.

## Example

Once a sync has completed (Chapter 9's example), the live graph is
queryable with any Bolt client. A one-liner using the bundled
`code-kg query` subcommand:

```bash
export GRAPH_URI=bolt://localhost:7687
go run ./cmd/code-kg graph-query \
  --repo-id demo \
  --cypher "MATCH (f:Function {name:'runSync'})<-[:CALLS]-(caller)
            RETURN caller.name, caller.file_path, caller.start_line"
```

Output on our reference commit:

```
TriggerSync    | reference-impl/code-kg/service.go | 161
runIncrementalSync (recursion guard) | reference-impl/code-kg/service.go | 278
```

That structural precision is unreachable from embeddings alone.

## Common mistakes

Four anti-patterns in code-graph design account for most of
the failures we see. Each is the result of importing a prior
from *document* graph work into a domain where the prior does
not hold.

**1 — Unbounded edge taxonomy.** The symptom is a graph schema
with 40 relation types — `USES`, `NEEDS`, `REFERS_TO`,
`DEPENDS_ON`, `TOUCHES`, `READS`, `WRITES`, … — each with
slightly overlapping semantics. Query authors stop trusting the
graph because the same real-world edge shows up under three
different labels. Start with the four-edge core from the *What*
section (`CONTAINS`, `IMPORTS`, `CALLS`, `IMPLEMENTS`). Add a
new edge type only when there is a query you can't answer
without it.

**2 — Graph on hot-write path.** The symptom is that committing
a one-line code change triggers a 200-ms round-trip to the
graph database. The temptation is to keep the graph
"always consistent" via mutation. The fix is the full-rebuild
pattern of Chapter 11: accept 30–60 seconds of staleness in
exchange for a one-line clear-and-insert that never leaves the
graph in a half-written state. For repos above ~500 kLOC, the
upgrade path is per-file invalidation — but it is an
*upgrade*, not a starting point.

**3 — Indexing every identifier as a node.** The symptom is a
graph with 200 k nodes for a 4 kLOC repo, most of them
built-ins like `len`, `append`, `make`, `fmt`, `errors`. The
noise drowns the signal. The fix is a per-language noise
filter applied at parse time (Chapter 9) — treat standard
library names as edges-to-nothing, not as nodes. The reference
implementation ships a ~200-name stoplist per language; it
reduces node count by 60–80 % on typical Go code with no loss
of query utility.

**4 — Storing function bodies inside graph nodes.** The
symptom is a 4 GB graph database for a project whose source
code is 40 MB. The temptation is to "have everything in one
place." The graph's job is *identity + relations*; the vector
store's job is *content*. Keep the node small (name, file,
start/end line, kind, signature). Bodies belong in the vector
store or — if you need full-text — in a third column. Graph
queries that accidentally scan 4 GB of body text are 100x
slower than queries that walk a 40 MB identity index.

## Conclusion

The graph carries the half of code-knowledge that survives no
lossy projection: who is wired to whom. With a bounded edge
taxonomy, a content-free node identity, and a full-rebuild-per-repo
write pattern, the store stays conceptually simple even as the
repo grows. Chapter 12 unifies the two stacks — vector and graph —
behind a single retriever interface.

## References

```{bibliography}
:filter: keywords % "graph" or keywords % "code-layer"
```
