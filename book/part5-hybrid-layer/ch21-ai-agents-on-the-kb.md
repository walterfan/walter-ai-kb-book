---
title: 'Chapter 21 — AI Agents on the KB'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - hybrid
  - agents
  - mcp
---

# Chapter 21 — AI Agents on the KB

## Why

A knowledge base has two kinds of readers. A human reader opens a
browser, types a query, scans a page, and closes the tab. An agent
reader — an LLM-backed assistant in an IDE, a chat client, a CI job —
does not open a browser. It calls a function, receives a structured
response, and keeps going. For most of this book the reader has been
human. This chapter is about the other kind.

The move is not new. The blog post that seeded this book
{cite}`fanyamin2026deepwiki` already argues that the KB's value
compounds when an LLM can call it instead of a human having to
read it. What has changed since that post is the arrival of a
*protocol* for such calls — the Model Context Protocol
{cite}`mcp_spec` — and the arrival of a common *deployment
pattern*, the edge function, that turns a KB into something an agent
can reach from anywhere. Agents on a KB have two halves, and this
chapter treats them in turn: the protocol half (how agents talk to a
KB) and the pattern half (how a KB gets close enough to an agent to
be worth talking to).

Recent literature also makes the design space easier to name. RepoAgent
shows the **producer side** of repository intelligence: a system that
analyzes global repository structure, generates documentation, and keeps
that documentation updated over time
{cite}`luo2024repoagentllmpoweredopensourceframework`. CGM shows a
different **consumer side**: repository-level tasks solved by a
graph-integrated model, without an explicit tool-using agent loop
{cite}`tao2025codegraphmodelcgm`. This chapter is about the third
position in that triangle: a **tool-using agent** that treats the KB as
external memory. Zhu et al.'s survey is the reason that position is not
merely a product choice but a technical one: LLMs tend to reason more
reliably over structured context than they extract structure from raw
corpora on demand {cite}`zhu2024llmsknowledgegraphconstruction`.

## What

### Where this chapter sits in the design space

Repository-level AI systems now come in three shapes that are easy to
confuse unless they are named explicitly:

1.  **Producer-side automation.** Systems like RepoAgent generate and
    update repository documentation. Their centre of gravity is the
    *maintenance loop*.
2.  **Agentless graph-aware readers.** Systems like CGM consume code
    graphs and repository context inside one model stack. Their centre
    of gravity is the *reader model*.
3.  **Tool-using agents over an explicit KB.** The pattern in this
    chapter keeps the KB outside the model and exposes it via tools.
    Its centre of gravity is the *retrieval interface*.

The book chooses the third shape as the architectural default because
it keeps provenance, filtering policy, and update cadence inspectable.
But it is designed to compose with the first two rather than compete
with them. A RepoAgent-like pipeline can keep the prose layer fresh; a
CGM-like reader can consume the same graph exports offline; the MCP
surface is the online contract that ordinary IDE agents use.

### The protocol half: MCP plus the tuple

The Model Context Protocol is, for the purposes of this chapter, a
simple idea made precise: an agent can enumerate *tools* exposed by
a server, and it can call those tools with typed arguments. A KB can
be a MCP server; a well-scoped KB exposes three tools:

| Tool | Input | Output |
|:--|:--|:--|
| `kb.search(query, k, filter)` | natural-language query, top-k, filter expression | list of $\{page\_id, score, \text{tuple}, snippet\}$ |
| `kb.read(page_id)` | stable page id | full body, frontmatter, footer |
| `kb.cite(query, k)` | natural-language query, top-k | list of $\{page\_id, \text{file:line} \text{ anchors}\}$ |

The important detail is the **filter argument on `kb.search`**, which
accepts a predicate over the document-layer tuple from Chapter 18.
An agent that wants only approved content writes
`filter: review_status == approved`. An agent that wants only
L0–L1 (code and ADRs, no AI-drafted prose) writes
`filter: layer in {L0, L1}`. An agent that wants "reviewed prose or
code" writes the conjunction. The KB does not have to trust the
agent; it simply filters deterministically at retrieval time.

This is the payoff of the tuple model. Without it, a KB exposed to
agents would either include AI-drafted-unreviewed content in every
answer (dangerous) or exclude it blanket (wasteful). With it, the
decision is pushed to the caller, and the KB's responsibility
reduces to *honest labelling* — which, as Chapter 7a argued, is the
thing the operational model was built to deliver.

### The pattern half: edge-deployed KBs

A search tool that sits behind a VPN in a datacentre is not an agent's
tool; it is a human's tool with an agent-shaped wrapper. To be
useful to agents, a KB has to be reachable from wherever the agent
runs — typically an IDE process on a laptop, a CI runner in the
cloud, a containerised worker in another region. The common shape
is the **edge function**: a small, stateless, horizontally-scalable
unit that serves HTTP from many geographic points of presence.

Public examples of this pattern, any of which can host the three MCP
tools above:

- **Cloudflare Workers** {cite}`cloudflare_workers` — V8 isolates,
  global distribution, KV and D1 for state, single-digit-ms cold
  start.
- **Deno Deploy** {cite}`deno_deploy` — TypeScript-first, global
  distribution, `Deno.kv` for state.
- **Vercel Edge Functions** {cite}`vercel_edge` — per-region
  deployment, `@vercel/edge-config` for state.

All three support the same operational shape: the *built HTML* from
`book/_build/html/` is stored in an asset bundle; a small server
function reads the bundle, answers `kb.read(page_id)` by serving
the matching HTML body, and answers `kb.search(...)` by consulting
an index also stored in the bundle (for a small KB) or a remote
vector store (for a large one). The KB publishes; the function
redeploys; the agents see fresh answers on the next call.

This abstraction is deliberately generic. The author's private
skill {cite}`fanyamin_pkb_skill` has a concrete deployment recipe for
one such runtime, including the build-bundle script and the
function-registration manifest. Those recipes are omitted here
because they are specific to employer infrastructure; the three
public analogues above are drop-in replacements.

## How

### A minimal MCP server shape

Pseudocode for the server side — the same shape fits any of the three
runtimes above:

```text
function handle(request):
    tool, args = parse(request)
    switch tool:
        case "kb.search":
            seeds      = hybrid_search(args.query, k=args.k * 3)   # ch12
            expanded   = graph_expand(seeds, max_hops=1)           # ch12/ch19
            filtered   = apply_tuple_filter(expanded, args.filter)
            top        = rerank(filtered)[:args.k]
            return [
                {
                  page_id: p.id,
                  score:   p.score,
                  tuple:   p.tuple,        # ⟨L, U, R, S⟩ from Chapter 18
                  snippet: p.snippet
                }
                for p in top
            ]
        case "kb.read":
            page = lookup(args.page_id)
            return {
                body:        page.body,
                frontmatter: page.frontmatter,
                footer:      page.footer     # full PKB-metadata block
            }
        case "kb.cite":
            candidates = vector_search(args.query, k=args.k)
            anchors    = [
                {page_id: p.id, file_line: extract_anchors(p.body)}
                for p in candidates
            ]
            return anchors
```

Three things to notice:

1.  `kb.search` is already **hybrid retrieval**, not a raw vector
    lookup. That matters because a repository agent's first query is
    often semantic (*"where do we validate tokens?"*) but its second
    query is structural (*"who calls this validator?"*). Folding
    Chapter 12's hybrid search and graph expansion behind one tool
    keeps the agent surface small while preserving repository-level
    reach.
2.  `kb.read` returns the **footer** alongside the body. An agent
    that wants to cite a page responsibly looks at `review_status`
    and `review_score` before quoting it. The KB does not decide
    whether the agent should trust the page; it gives the agent the
    labels to decide for itself.
3.  `kb.cite` returns `file:line` anchors, not prose. This is the
    Chapter 12 hard rule made into a tool. An agent that calls
    `kb.cite` and then fabricates a line number is doing so over
    the server's objection — and the CI gate at Chapter 15 H4 will
    catch the page if it is ever committed back to the KB.
4.  `kb.search` accepts a `filter`. The filter is the tuple
    predicate from Chapter 18 Section 3.2. The runtime evaluates
    it; the agent specifies it.

### Agentless readers and tool-using agents can share one KB

CGM is useful here not because this chapter should turn into a model
architecture paper, but because it marks the boundary cleanly. An
agentless repository solver wants a repository graph plus code
representations and enough structured context to solve a task in one
shot {cite}`tao2025codegraphmodelcgm`. A tool-using IDE agent wants the
same information, but incrementally: search, inspect, cite, then ask
again. An explicit KB supports both.

That means the KB should be treated as a **control plane**, not only a
tool endpoint:

- RepoAgent-like systems can write into it by keeping repository docs
  current {cite}`luo2024repoagentllmpoweredopensourceframework`;
- Chapter 12's hybrid retriever can export graph-guided evidence from
  it;
- MCP agents can query it online;
- graph-integrated readers can consume snapshots or graph exports from
  it offline.

The same explicit tuple labels, stable IDs, and citation anchors make
all four modes less fragile than asking each model invocation to infer
its own world state from raw files.

### Exposing the build output

For a small KB, the simplest storage for the built site is to ship
it inside the function bundle itself. The build step is:

1.  Run `make book-build` to produce `book/_build/html/`.
2.  Run a small packing script that reads the HTML tree and writes
    it to a TypeScript/JavaScript module as base64-encoded bytes
    (or, on runtimes that support it, as native asset files).
3.  Deploy the function with the packed module.

For a larger KB — say, more than a few megabytes of built output —
the asset bundle exceeds the edge runtime's per-function size limit.
The options are: (a) store assets in an object store the function
can read (R2 on Cloudflare, S3-compatible elsewhere); (b) split the
KB into multiple functions (one per Part); (c) keep HTML in a
separate CDN and let the function serve only the search index and
the MCP shim. Option (c) is usually the right answer: the HTML is
already a static site that a CDN serves natively.

### The tuple filter as a publish gate

A subtle point from Chapter 18 becomes operational here. An agent
that habitually passes `filter: review_status == approved` will
*never see* pages that are `pending`. That is the point. But a page
that stays `pending` indefinitely because no human ever reviews it
is, for agent purposes, invisible — even if it is useful. The
Chapter 15 soft gate S2 (stale footers) already warns humans about
these pages; Chapter 16's L3 discipline routes them to human
attention when an L2 update cannot cover them. The agent surface
does not introduce a new problem; it makes the cost of the old
problem explicit. A KB that agents cannot see is a KB that has
earned its invisibility.

## Example

A concrete day-in-the-life for one agent, one IDE, one KB:

```text
08:15  developer types /ask "how does the ingest pipeline handle CSVs?"
         IDE agent calls  kb.search(q=..., k=5, filter="review_status==approved")
         KB responds      [
                            {page_id: "ch06", score: 0.83, tuple: ⟨L2, human, approved, 4⟩, ...},
                            {page_id: "ch07", score: 0.79, tuple: ⟨L2, human, approved, 4⟩, ...},
                            {page_id: "ingest-runbook", score: 0.76, tuple: ⟨L2, ai+human, approved, 3⟩, ...},
                            ...
                          ]
         IDE agent calls  kb.read("ch06")
         KB responds      { body: ..., frontmatter: ..., footer: {review_status: approved, ...} }
         IDE agent answers, quoting ch06 ¶3 and linking ingest-runbook §4.

08:17  developer asks follow-up "which file actually parses the CSV?"
         IDE agent calls  kb.cite(q="CSV parsing", k=3)
         KB responds      [
                            {page_id: "ch06",  file_line: "internal/pipeline/csv_loader.go:42"},
                            ...
                          ]
         IDE agent opens that file:line in the editor. No hallucination;
         every anchor was resolved by the KB, not guessed.
```

Nothing in that sequence required the agent to trust the KB. Every
filter was declarative; every cite was resolved against the
build-time index; every decision the agent could have fabricated
was instead bounded by a mechanical answer from the server.

The same KB could also serve a non-interactive repository task. A batch
job that asks *"which modules are impacted by this interface change?"*
does not need an IDE loop; it can call the same `kb.search` entry point
or consume the exported graph neighbourhood directly. The important
thing is not whether the consumer calls itself an "agent". It is that
all consumers share one maintained substrate instead of each rebuilding
repository context from scratch.

## Conclusion

Agents on a KB are not a new layer on top of the prose and code
layers; they are the natural API shape the operational model already
implies. A KB that has honest layer tuples, a stable page identity,
and mechanically resolved citations has exactly the three tools an
agent needs. The protocol (MCP) is thin; the pattern (edge function)
is off-the-shelf; the trust model is exactly the one Chapter 18 and
Chapter 15 already built.

What remains — Chapter 22's token budget, Chapter 23's trust and
red-teaming, Chapter 24's outlook — are the governance questions
that an agent-callable KB makes newly urgent. A KB that only humans
read could afford a sloppy footer. A KB that agents call at scale
cannot.

## References

```{bibliography}
:filter: keywords % "hybrid" or keywords % "agents" or keywords % "mcp" or keywords % "self-citation"
```
