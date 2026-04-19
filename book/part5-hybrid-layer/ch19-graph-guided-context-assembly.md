---
title: 'Chapter 19 — Graph-guided Context Assembly'
status: draft
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - hybrid
  - graph-rag
---

# Chapter 19 — Graph-guided Context Assembly

## Why

A retriever that returns the top 5 most relevant pages is not yet a
repository assistant. A repository question rarely wants five isolated
hits. It wants a **small connected explanation**: the function, its
callers, the ADR that justified the behaviour, the runbook that names
the failure mode, and only the reviewed pages among them. Raw top-k is
good enough for a search box; it is not good enough for an LLM that has
to answer *why*, *where else*, and *what changed* without guessing.

This chapter sits at exactly that boundary. Chapter 12 retrieved seeds:
vector for fuzzy intent, keyword for identifiers, graph for structure.
Chapter 18 gave every prose node a tuple
$\langle L, U, R, S \rangle$ that says how trustworthy it is. Chapter 21
will expose the resulting KB to agents as tools. The missing step is
the one that turns a ranked seed list into a **bounded, typed context
packet** an LLM can safely reason over.

The recent literature makes this step easier to name. GraphRAG shows
that graph structure is useful not only for storage but for
**query-focused context construction** {cite}`edge2024graphrag`.
HippoRAG pushes the same intuition toward long-term memory
{cite}`gutierrez2024hipporag`. Zhu et al.'s survey explains why this is
not just a retrieval trick: LLMs are often better at **reasoning over
structured evidence** than at extracting that structure on demand from
raw corpora {cite}`zhu2024llmsknowledgegraphconstruction`. CGM is the
model-side continuation of the same idea at repository level
{cite}`tao2025codegraphmodelcgm`. This chapter is the book's
retrieval-side answer: keep the graph explicit, but use it to assemble
the exact evidence packet the model should see.

## What

**Graph-guided context assembly** is the step between retrieval and
generation that transforms:

$$
(\text{query},\ \text{seed hits},\ \text{graphs},\ \text{tuple labels},\ \text{budget})
\rightarrow \text{context packet}
$$

The context packet is what the generator or agent actually consumes. It
is not "the top-k documents". It is a **bounded subgraph rendered as
evidence**.

Three properties define the packet:

1.  **Seeded.** Assembly starts from Chapter 12's retrieved seeds; it
    does not walk the repository graph blindly.
2.  **Typed.** Expansion preserves relation labels such as `CALLS`,
    `IMPLEMENTS`, `RETURNS`, page-to-page links, and page-to-code
    citations. The packet should explain *why* a node is present.
3.  **Filtered by authority and budget.** Tuple metadata from Chapter 18
    and a token budget decide what survives into the final packet.

This chapter deliberately scopes the problem narrowly. It is **not**
about:

- building a new graph database schema;
- replacing Chapter 12's retriever;
- summarizing an entire repository into one mega-prompt;
- learning a graph-integrated model like CGM.

It is about the operational middle step that both tool-using agents and
agentless repository readers need: converting retrieved seeds into a
small neighbourhood that matches the question.

### The heterogeneous graph the packet comes from

The assembly layer reasons over a **heterogeneous repository graph**,
not just the code graph from Chapter 11. At minimum it contains:

| Node kind | Examples | Main metadata |
|:--|:--|:--|
| Code entity | function, method, type, file | stable ID, path, signature, lines |
| Prose page | ADR, runbook, architecture note, chapter page | tuple $\langle L,U,R,S\rangle$, frontmatter, footer |
| Citation anchor | `file:line`, page section, include target | target path, line span, resolution status |

And it contains at least three families of edges:

| Edge family | Examples | Purpose |
|:--|:--|:--|
| Code structure | `CALLS`, `IMPLEMENTS`, `RETURNS`, `CONTAINS` | structural neighbourhood |
| Prose structure | page links, section references, includes | documentation neighbourhood |
| Cross-layer links | page cites entity, ADR explains file, runbook points to path | prose ↔ code bridge |

The important point is not whether every edge is materialised in one
physical store. The important point is that the assembly layer can
follow them as if they formed one typed graph.

## How

### Step 1 — Retrieve seeds, do not answer yet

Chapter 12 returns a ranked seed set. That seed set is a *proposal*,
not yet the context. Different query shapes produce different seed
profiles:

- **Semantic query**: seed is usually one or two entities or pages found
  by dense retrieval.
- **Identifier query**: seed is usually an exact symbol from keyword
  search.
- **Structural query**: seed is usually a symbol plus an explicit graph
  neighbourhood.
- **Why query**: seed is often mixed — one code entity plus one prose
  page or ADR.

The first discipline of this chapter is therefore simple: **do not let
the generator consume the seed list directly**. A top hit is only the
entry point into the local repository neighbourhood.

### Step 2 — Expand locally, with relation policy

Assembly then performs a bounded graph expansion around the seeds.
Bounded means both **hop-bounded** and **relation-bounded**. Two hops
over every possible edge is usually too much; one hop over the right
edges is usually enough.

A useful default policy is:

| Query shape | Preferred expansion |
|:--|:--|
| "where / who calls / what implements" | code edges first (`CALLS`, `IMPLEMENTS`, `CONTAINS`) |
| "why / how / what is the rationale" | cross-layer links first (ADR, architecture page, reviewed runbook) |
| "what changed / what breaks" | code neighbours plus pages citing the changed entities |

That relation policy is why graph-guided assembly is different from
"append the graph neighbours". The graph does not merely increase
recall. It selects the *kind* of surrounding evidence that makes the
question answerable.

### Step 3 — Filter and weight with the tuple

At this point the packet often contains more relevant material than the
context window can afford. Chapter 18's tuple becomes load-bearing
here. A page cited by the graph may still be a bad thing to feed the
model if it is AI-drafted and pending review.

A practical scoring sketch:

```text
final_score(node) =
    seed_score(node)
  * relation_weight(edge_to_node)
  * hop_decay(hops_from_seed)
  * tuple_weight(node.tuple)
  * freshness_weight(node.commit_age)
```

Where:

- `seed_score` comes from Chapter 12 (vector / keyword / graph / RRF);
- `relation_weight` prefers explanatory edges for "why" questions and
  structural edges for "where" questions;
- `hop_decay` penalizes distant nodes;
- `tuple_weight` down-ranks `pending` or low-score prose;
- `freshness_weight` is optional but useful when two pages are equally
  relevant and one is clearly newer.

The key idea is not the exact formula. It is that **context assembly is
where retrieval relevance and document authority finally meet**.

### Step 4 — Render the packet as evidence, not as a dump

The final packet should preserve provenance and relation cues. A good
packet entry says not only *what* text was included but *why*:

```text
[seed] Function runSync
  file: reference-impl/code-kg/service.go:201-248
  reason: keyword seed

[neighbor via CALLS<-] Function TriggerSync
  file: reference-impl/code-kg/service.go:161-184
  reason: caller of runSync

[neighbor via EXPLAINS] ADR-0014 Panic-safety in worker pools
  tuple: ⟨L1, human, approved, 4⟩
  reason: cited by runSync doc comment and mentions panic recovery
```

This is the bridge to Chapter 21. An MCP tool like `kb.search` does not
have to expose raw graph traversal; it can expose a ready-made packet
whose entries already contain relation labels, tuple labels, and
resolvable anchors.

### Step 5 — Reuse the same packet for both agents and agentless tasks

One reason to keep the assembly layer explicit is that it serves two
downstream consumers equally well.

**Tool-using agents.** An IDE agent asks a question, receives a packet,
reads one or two pages, then follows up. Chapter 21's `kb.search` and
`kb.cite` are this mode.

**Agentless repository tasks.** A batch evaluator, patch generator, or
CGM-style reader may prefer one-shot inference over a preassembled
neighbourhood {cite}`tao2025codegraphmodelcgm`. The packet format still
helps: it is the explicit retrieval-time representation of the local
subgraph the model should care about.

This is where RepoAgent matters as complementary, not competing, work.
RepoAgent improves the **producer side** of repository knowledge by
keeping global structure analysis, documentation generation, and update
in a loop {cite}`luo2024repoagentllmpoweredopensourceframework`.
Graph-guided assembly improves the **consumer side** by making that
maintained repository memory query-shaped at run time.

### The operational rule: assemble locally, never globally

The biggest failure mode in graph-RAG systems is to turn graph access
into a license to over-fetch. Repository graphs are dense enough that a
few careless hops can explode the packet. The safest operational rule
is:

> **Retrieve globally, assemble locally.**

Global search finds the right seed. Local graph assembly builds the
answerable neighbourhood. Reversing the order is how systems end up
showing the model half the repository and calling it "context".

## Example

Suppose the developer asks:

> *"Why does `runSync` recover panics instead of crashing the worker?"*

### 1. Seeds from Chapter 12

Hybrid retrieval returns:

1.  `runSync` function in `service.go`
2.  ADR page `ADR-0014 Panic-safety in worker pools`
3.  `runIncrementalSync` as a lower-ranked structural neighbour

### 2. Local graph expansion

Assembly follows:

- `CALLS` / reverse-`CALLS` edges around `runSync`
- page-to-code citation edges from `ADR-0014`
- page-to-page links from `ADR-0014` into the incident runbook

This yields a raw neighbourhood of 11 nodes.

### 3. Tuple and budget filtering

Two nodes are dropped:

- one AI-generated summary page with tuple `⟨L3, ai, pending, 0⟩`
- one stale incident retrospective outside the token budget

Five nodes survive, ordered as the final packet. The packet below is
illustrative; exact line spans vary by repository and commit:

```text
1. [seed] runSync
   file: reference-impl/code-kg/service.go:<runSync span>
   why included: exact function under discussion

2. [code neighbor] TriggerSync
   file: reference-impl/code-kg/service.go:161-184
   why included: caller of runSync

3. [prose bridge] ADR-0014
   tuple: ⟨L1, human, approved, 4⟩
   why included: rationale for panic recovery policy

4. [ops bridge] worker-pool incident runbook
   tuple: ⟨L2, ai+human, approved, 3⟩
   why included: describes failure mode and on-call handling

5. [structural neighbor] runIncrementalSync
   file: reference-impl/code-kg/service.go:278-314
   why included: recursion / re-entry context
```

### 4. Generator output

The LLM no longer has to infer the rationale from raw files alone. It
can answer:

```text
`runSync` recovers panics so a single failed sync target does not crash
the whole worker loop. The implementation is in the `runSync` span in
`reference-impl/code-kg/service.go`, and the policy rationale is
recorded in `ADR-0014`, which states that worker-pool panics should be
contained and logged rather than allowed to terminate sibling work.
`TriggerSync` is one caller (`service.go:161-184`), and
`runIncrementalSync` participates in the same control path
(`service.go:278-314`).
```

That answer is better than top-k retrieval alone not because it saw more
text, but because it saw the **right local subgraph** under an explicit
authority filter.

## Conclusion

Graph-guided context assembly is the step that turns a KB from a search
system into repository memory. Chapter 12 gave us seeds; Chapter 18 gave
us authority labels; this chapter combines the two into a bounded
evidence packet that an LLM can actually reason over.

The broader research line now looks coherent. Zhu et al. explain why
structured evidence helps LLM reasoning. GraphRAG and HippoRAG explain
why graph-shaped context beats flat top-k in many settings. RepoAgent
shows that repository knowledge must be continuously maintained. CGM
shows that the same graph signal can move closer to the model itself.
This chapter's wager is the conservative systems version of that line:
keep the graph and the tuple explicit, assemble local context packets at
query time, and let both tool-using agents and agentless repository
readers consume the same maintained substrate.

## References

```{bibliography}
:filter: keywords % "hybrid" or keywords % "graph-rag"
```
