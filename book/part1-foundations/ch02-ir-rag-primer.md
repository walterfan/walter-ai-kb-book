---
title: "Chapter 2 — An IR and RAG Primer"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - foundations
  - ir-rag
  - fusion
  - evaluation
  - graph-rag
---

# Chapter 2 — An IR and RAG Primer

This chapter on one page — the retrieval primitives, the RAG
pipeline, the failure modes that motivate everything beyond vanilla
RAG, GraphRAG as a structural alternative, and the substrate-choice
matrix that translates these ideas into deployment decisions:

```{mermaid}
mindmap
  root((IR and RAG))
    Retrieval primitives
      Lexical (TF-IDF, BM25)
      Dense (embeddings + ANN)
      Hybrid (RRF)
      Re-ranking (cross-encoder)
      Evaluation (BEIR, nDCG, MRR)
    RAG pipeline
      Chunk
      Embed
      Top-k retrieve
      Prompt and generate
    Failure modes
      Lost-in-the-middle
      Multi-hop blindness
      Stale index
      Citation drift
      Cost surprise
    GraphRAG and neighbours
      Entities and relations
      Community detection (Leiden)
      Hierarchical summaries
      HippoRAG
    Retrieval substrate
      Plain full-text (rg, FTS5)
      pgvector
      Elasticsearch / OpenSearch
      Specialised vector DB
```

## Why

"Retrieval-Augmented Generation" is often described in two sentences:
*chunk your documents, embed the chunks, take the top-k nearest
neighbours of the user's query, paste them into the prompt.* This
description is not wrong, exactly. It is instead the shortest possible
description, and it lands in the same unlucky cognitive spot as "a car
is four wheels and an engine" — technically accurate, useless for
debugging.

The deeper lesson behind that description is one that a practitioner
learns the hard way: *the hardest part of a knowledge base is not
writing it, it is making it findable, usable, and up-to-date*
{cite}`fanyamin2026kb_pipeline`. Every section of this chapter is,
under the surface, a piece of that one sentence. Findable is
retrieval. Usable is fusion and evaluation. Up-to-date is every
failure mode that is downstream of a stale index.

Information retrieval as a field is roughly sixty years old
{cite}`manning2008introduction`. It has accumulated a vocabulary, a
set of evaluation disciplines, and a long catalogue of failure modes
that every practical knowledge base rediscovers the hard way if the
designers have not read them first. This chapter gives the minimum
IR / RAG vocabulary the rest of the book assumes, then does three
things most short RAG primers skip: it lists vanilla RAG's failure
modes honestly, introduces GraphRAG as a serious alternative for one
specific class of those failures, and closes with a judgment matrix
for picking a retrieval substrate — full-text, pgvector,
Elasticsearch, or a specialised vector store
{cite}`fanyamin2026elasticsearch_rag` {cite}`fanyamin2026pgvector_rag`.
Readers already fluent in BM25, dense retrieval, hybrid retrieval,
the GraphRAG literature, and substrate trade-offs can skim this
chapter for notation and move on.

## What

Six terms carry almost all the weight in the rest of the book;
defining them once precisely makes later chapters much shorter. Two
more terms — the failure mode catalogue for RAG, and GraphRAG — carry
most of the weight of the debates you will find in the literature.

### Lexical retrieval: TF-IDF and BM25

Lexical retrieval scores a document against a query as a function of
*which query terms appear*, *how often they appear* (term frequency),
and *how unusual they are across the corpus* (inverse document
frequency). TF-IDF is the original formulation
{cite}`manning2008introduction`; BM25 is the workhorse refinement that
every modern full-text search engine — Lucene, Elasticsearch, Tantivy,
PostgreSQL's `tsvector`, Bleve — ultimately descends from
{cite}`robertson2009probabilistic`. For code KBs, BM25 over identifiers
remains surprisingly strong: identifiers carry a lot of signal, and a
well-tokenised BM25 index routinely beats a poorly-tuned embedding
model on exact-symbol lookups such as *"find all call sites of
`runSync`"*.

It is worth spending a page on *why* BM25 works, because most
engineers use it through a library call and never see the shape of its
answer. For a query $q$ made of terms $t_1, t_2, \dots$, and a
document $D$ with length $|D|$ in an index whose average document
length is $\text{avgdl}$, BM25 scores the pair as a sum over query
terms:

$$
\text{BM25}(q, D) \;=\; \sum_{t \in q}
  \underbrace{\text{IDF}(t)}_{\text{how rare is }t?}
  \;\cdot\;
  \underbrace{\frac{f(t, D)\,(k_1 + 1)}
                   {f(t, D) + k_1\!\left(1 - b + b\,\frac{|D|}{\text{avgdl}}\right)}}_{\text{saturating, length-normalised TF}}.
$$

Read from left to right, three design decisions fall out of the
formula:

1.  **Rare terms dominate.** The IDF factor makes a document that
    contains a term occurring in 1% of the corpus count far more than
    one containing a term that appears in half of it. This is why a
    well-built BM25 index nails identifier-literal queries: an error
    code like `ERR_QUEUE_DRAIN` appears in a handful of documents, so
    its IDF is enormous and the document that mentions it wins by a
    wide margin. It is also why BM25 tends to out-rank vector
    retrieval on "search for this exact symbol" workloads: *vectors do
    not know what "rare" means*.

2.  **Term frequency saturates.** Unlike raw TF-IDF — where
    repeating a term ten times multiplies its contribution by ten —
    BM25's TF numerator is bounded above by $(k_1 + 1)$. In the
    Elasticsearch default of $k_1 = 1.2$, the tenth occurrence of a
    term contributes almost nothing more than the third. This single
    property is why BM25 does not get tricked by
    `keyword keyword keyword keyword` filler and TF-IDF does. The
    lesson for a code KB is that *TF saturation is exactly what you
    want when an identifier legitimately appears two hundred times in
    a generated file*.

3.  **Length is normalised, but only partway.** The $b$ parameter
    (default $0.75$) controls how aggressively BM25 penalises long
    documents. At $b=0$ length does not matter; at $b=1$ a document
    twice the average length is halved in effective term frequency.
    The middle ground is deliberate: long documents really do have
    more chances to mention a term by accident, but they also
    legitimately cover more ground. For a software KB whose documents
    range from 50-word ADR stubs to 5000-word runbooks, this matters
    more than the choice of $k_1$.

In practice, $k_1 \in [1.2, 2.0]$ and $b \in [0.5, 0.9]$ covers
almost every production setting. The popular mistake is to tune these
before the tokeniser. Four well-known BM25 pathologies to keep in
mind, because each one will eventually show up in a real KB:

-   **Short-query sensitivity.** On one-word queries, BM25 degenerates
    to "which document has the highest IDF-weighted TF for that
    word", which is fine until the word is a common English verb.
    Remedy: query expansion, or a dense retriever running in
    parallel, fused at the end.
-   **Vocabulary mismatch.** *"wait for the pool to finish"* and
    *"drainOnShutdown"* share zero query terms, so BM25 scores them
    zero. This is not a bug in BM25; it is the reason dense retrieval
    exists as a complement.
-   **Compound-word breakage.** `drainOnShutdown` indexed as one token
    is invisible to the human query *"drain on shutdown"*. Three
    lines of tokeniser configuration — camel-case splitting,
    snake-case splitting, optional language-model subword fallback —
    often matter more than three weeks of embedding-model
    fine-tuning. Chapter 10 returns to this in anger.
-   **Stopword asymmetry.** Naïve stopword removal strips *not*, *or*,
    *no*, *nil* from queries, which in a software KB is the
    difference between *"does it return nil"* and *"does it return"*.
    The code-layer retriever in Part III keeps these words.

There is a second class of query where BM25 is not a fallback but the
primary winner: *identifier-literal* queries. A user searching for
order number `20260115` or HTTP status `502` or ticket
`PROJECT-1234` does not want *"paragraphs that feel like they might
discuss 502 errors"*; they want *"the paragraph that mentions
`20260115`"*. A vector retriever, confronted with `20260115`, will
happily return a general discussion of order creation because it
looks semantically adjacent; a BM25 retriever will return the
paragraph that actually contains the literal
{cite}`fanyamin2026elasticsearch_rag`. Any KB whose users ask
identifier-literal questions — and for software KBs that is almost
all of them — must keep a BM25 path, full stop.

### Dense retrieval: embeddings and ANN

Dense retrieval replaces the sparse bag-of-words representation with
a dense vector produced by a neural encoder, and finds neighbours in
that vector space. The modern ancestor is Dense Passage Retrieval
{cite}`karpukhin2020dpr`; the modern scaling trick is Hierarchical
Navigable Small World graphs for approximate-nearest-neighbour search
{cite}`malkov2020hnsw`, which is what pgvector and most other
production vector stores use under the hood. Dense retrieval shines on
paraphrases — *"which function waits for the worker pool to drain?"*
will find `drainOnShutdown` even if the query uses none of the same
words.

The counterweight to remember is that dense retrieval is only as good
as the training distribution of its encoder. A general-purpose encoder
that has seen little Go code will treat `ctx.Done()` and
`context.Background()` as closer than they should be; a code-trained
encoder like Voyage's `voyage-code` or the BGE family
{cite}`voyage_code2` {cite}`xiao2024bge` will keep them distinct. Pick
your encoder for your domain, not for its leaderboard rank on
MTEB-in-general.

### Hybrid retrieval and Reciprocal Rank Fusion

Lexical and dense retrieval have complementary failure modes, which
is exactly the setup in which fusion helps. Reciprocal Rank Fusion
{cite}`cormack2009rrf` is the rank-combination method that most
production hybrid systems use, partly because it is score-free (so
neither ranker has to be calibrated) and partly because it has
remarkably few knobs. For a code KB in particular, Part III (Chapters
10 – 12) argues that *hybrid is not optional* — lexical alone misses
paraphrases, dense alone misses exact-symbol lookups, and fusion is
cheaper than picking a side.

Two levers that properly belong to the hybrid layer — and that a
pure-vector-store pipeline usually loses — are worth naming
explicitly, because they change the character of retrieval more than
any embedding upgrade:

-   **Field weighting.** Tokens appearing in a document's *title* are
    a stronger signal of what the document is *about* than the same
    tokens buried in the body. A production Elasticsearch / Solr /
    pgvector + `tsvector` setup routinely weights the title field
    around two times the content field; the effect on nDCG@10 is
    larger than most of the choices upstream of it
    {cite}`fanyamin2026elasticsearch_rag`.
-   **Function scoring (freshness, authority, popularity).** A
    document that scores highly on lexical + dense similarity but was
    last updated three years ago is, for most KB questions, a worse
    answer than a 90%-as-similar document updated last week.
    Multiplying the fused score by a freshness decay function turns
    this intuition into a scored ranking term, not an afterthought
    {cite}`fanyamin2026elasticsearch_rag`.

Structured filtering — *"only pages in the `worker` package",
"only docs tagged `runbook`", "only the current major version"* — is
the third lever and is discussed on its own in Chapter 10. The
practical point for now: as soon as structured filters enter the
picture, the choice of retrieval substrate (pgvector? Elasticsearch?
a specialised vector database?) stops being a matter of taste. The
"How" section of this chapter gives a judgment matrix
{cite}`fanyamin2026pgvector_rag`.

### Re-ranking: the second-stage retriever

Fusion gives you a better *list*. Re-ranking gives you a better
*top-k*. The distinction is worth making carefully, because "add a
reranker" is advice so frequently given and so rarely explained that
many teams implement it as "call Cohere Rerank" and never find out
what the model is actually doing for them.

The setup is a two-stage pipeline. Stage one is your fused
BM25 + dense retriever, which is fast, operates over the whole index,
and is asked to return a *generous* top-k — typically 50 or 100
candidates. Stage two is the reranker, which is slow, operates only
over those candidates, and is asked to reorder them into the final
top-k (typically 5 to 10) that the LLM will actually see. The first
stage optimises *recall* ("did the right document make the top-100?");
the second optimises *precision at small k* ("is the right document
at position 1?"). Neither stage can do the other's job well, which is
why the two-stage shape is the dominant production pattern
{cite}`nogueira2019passage`.

The technical reason stage two needs to be separate comes down to a
single architectural choice: **bi-encoder** vs **cross-encoder**
{cite}`reimers2019sbert`.

-   A **bi-encoder** — which is what every dense retriever in this
    chapter has been so far — encodes the query and the document
    *independently* into two vectors, then scores them by a cheap
    similarity function (cosine, dot product). The encoding cost of
    the document is paid once at index time; at query time you only
    encode the query, then do an ANN search against millions of
    precomputed vectors. Billions of documents are feasible. The cost
    is representational: the model can only compare the two fixed
    vectors, never the *interaction* of specific tokens across the
    query and the document.
-   A **cross-encoder** concatenates the query and the document into
    one input — something like `[CLS] query [SEP] document [SEP]` —
    and runs the whole concatenation through a transformer that
    outputs a single relevance score. Because attention runs across
    both sides, the model can directly weigh *which query token
    aligns with which document token*, which is exactly the signal
    needed to separate "talks about rate limiting in general" from
    "talks about rate limiting on the ingest endpoint". The cost is
    computational: every (query, document) pair is a separate
    transformer forward pass, so you cannot afford to run a
    cross-encoder over the whole index. You *can* afford to run it
    over 100 candidates.

This is the whole reason re-ranking is a separate stage. The bi-encoder
gives you recall on the corpus scale; the cross-encoder gives you
precision on the shortlist. Trying to do either job with the other
model costs either quality or money.

For a rough order-of-magnitude feel: a modern cross-encoder reranker
on CPU might score 50 – 200 (query, document) pairs per second, and
on a single commodity GPU 500 – 2000 pairs per second. With a stage-1
top-100 and a per-query budget under 100ms, that comfortably fits.
With a stage-1 top-1000 and the same budget, it does not. The
practical consequence is that *the stage-1 top-k is a cost dial*, not
an accuracy dial — past some point, more recall costs more latency
without helping the end-to-end answer.

Three open-weight reranker families are worth knowing about, because
they cover most of the design space without lock-in:

-   **MS MARCO cross-encoders** — the sentence-transformers family,
    trained on Microsoft's 8.8M-passage MS MARCO dataset
    {cite}`nogueira2019passage`. Robust, well-understood, widely
    benchmarked. A good default for English KBs.
-   **BGE rerankers** — part of the BGE family already cited for
    embeddings {cite}`xiao2024bge`; multilingual, and the small
    variants (≈300M parameters) fit on a single GPU. A good choice
    when the KB is mixed-language or when you want one vendor across
    embeddings and reranking.
-   **Hosted APIs** (Cohere Rerank, Voyage Rerank, Jina Rerank). The
    quality-per-dollar is usually fine, the integration cost is
    trivial, and the operational concern is straightforward:
    *every query now talks to an external service*. For a KB that
    deliberately avoids sending proprietary code off-prem, this is
    disqualifying; for a public-docs KB it is often the right
    first-cut choice.

Four honest caveats before adopting one:

1.  **A reranker makes a mediocre retriever look good, not a broken
    one look good.** If stage one has poor recall — the right
    document is not in its top-100 — the cross-encoder cannot
    retrieve something that was never shown to it. Teams that report
    "we added reranking and quality *dropped*" have almost always
    tuned stage one to return fewer, more confident candidates after
    the rerank, starving stage two.
2.  **Latency is additive, not hidden.** A 50ms cross-encoder pass
    on top of a 30ms hybrid retrieval is 80ms to first LLM token, not
    30ms. For agent loops with many retrievals per turn this
    accumulates fast. Chapter 21 on agents returns to this budget.
3.  **Evaluation matters more, not less, with a reranker in the
    loop.** A reranker can reorder a list in ways that look right on
    three sample queries and are wrong on the long tail. The BEIR-style
    evaluation in Chapter 15 stays in place; it moves downstream of
    the reranker, not around it.
4.  **Rerankers do not replace the other levers.** Field weighting
    and freshness decay, applied at the fusion stage, still matter;
    the cross-encoder has no idea that the document it scored highly
    was last updated three years ago. The healthy mental model is:
    *fusion assembles a candidate list with the right structural
    biases; the reranker reorders within those biases*.

For the workloads this book targets, the honest recommendation is:
do not add a reranker until hybrid retrieval with field weighting and
freshness decay is measured and clearly leaving precision on the
table. When you do add one, measure on the same BEIR-style harness
the first stage uses, cap the stage-1 top-k at something you can
actually afford, and keep the reranker interchangeable behind an
interface so you can swap MS MARCO for BGE for a hosted API without
rewriting the retrieval layer. The code-layer reference implementation
in Chapter 12 wires in a cross-encoder exactly this way.

### Retrieval-Augmented Generation

Retrieval-Augmented Generation, as formalised by Lewis et al.
{cite}`lewis2020rag`, is the pattern of composing a retriever and a
generator in series so that the retrieved context conditions the
generator's output. The modern RAG survey by Gao and colleagues
{cite}`gao2023retrieval` catalogues the variants — Naive RAG, Advanced
RAG with query rewriting and re-ranking, Modular RAG — and is a good
map of the design space. This book is, under a thin coat of paint, an
applied-RAG book; the prose layer (Part II) and the code layer (Part
III) are two specialisations of the same pattern.

### Evaluation: BEIR and friends

Retrieval without evaluation is superstition. BEIR
{cite}`thakur2021beir` is the benchmark suite that made zero-shot
retrieval evaluation concretely testable across domains, and the
methodology it uses — labelled queries, nDCG@10, Recall@k — transfers
directly to a home-grown code KB. Chapter 15 builds a mini-BEIR for a
code-layer instance; readers who want to compare a BM25 baseline
against a pgvector-backed system without that scaffolding risk
mistaking "the answer looks nice" for "the answer is right".

### The limits of vanilla RAG

"Vanilla RAG" — in this book's usage — means: split documents into
roughly-paragraph-sized chunks, embed each chunk, retrieve top-k by
vector similarity, concatenate into a prompt, call the LLM. This
baseline works well enough for the demo that it has absorbed the
entire popular imagination of what RAG *is*. It also has a well-known
catalogue of failure modes that show up as soon as real users ask
real questions. Five are worth naming here:

1.  **The chunk-boundary problem.** A 200-word chunk cuts a paragraph
    in half; the sentence that explains *why* an API returns `nil`
    lives in chunk `k`, the sentence that shows *what* it returns
    lives in chunk `k+1`, and a retriever scoring by individual-chunk
    similarity returns one without the other. Symptom: the answer is
    plausible but missing the qualifier. Mitigations include
    overlapping chunks, parent-document retrieval, and late-chunking
    schemes; none of them fully solve it, and any code-aware KB has
    to chunk on *syntactic* rather than character boundaries
    (Chapter 10).

2.  **Semantic match ≠ semantic relevance.** Vector similarity finds
    *things that look like* the query, which is not the same as
    *things that answer* the query. A query "how do I rate-limit the
    ingest endpoint?" retrieves, via vector similarity, the five
    paragraphs in the repo that talk most about rate limiting — none
    of which is the paragraph about *the ingest endpoint specifically*.
    The fix is almost always hybrid retrieval plus a cross-encoder
    re-ranker (see the *Re-ranking* subsection above); re-ranking is
    the honest step many "just add vectors" stacks skip.

3.  **The multi-hop / global-question problem.** Vanilla RAG retrieves
    a flat set of top-k chunks. Questions of the form *"what are the
    three main themes of this codebase?"* or *"summarise how the ingest
    pipeline has evolved across the last ten commits"* require
    reasoning over structure the top-k chunks do not carry. The honest
    answer for this class of question is: *vanilla RAG cannot answer
    it*. This is the gap GraphRAG (next section) is designed for
    {cite}`edge2024graphrag`.

4.  **The stale-index problem.** An embedding index built at commit
    `a1b2c3d` is, by definition, a snapshot. Between that snapshot and
    the user's query the repo has moved; functions were renamed,
    pages were rewritten. Unless the pipeline re-embeds on every
    change (expensive) or detects and re-embeds only affected files
    (operationally complex), the retrieved chunk is a pre-image of a
    file that no longer exists. Chapter 14 is entirely about
    bounding this gap.

5.  **The faithfulness problem.** Even with perfect retrieval, the
    generator can still fabricate. Code-LLMs in particular are
    documented to generate plausible-looking `file:line` references
    that do not correspond to any actual file or line
    {cite}`chen2023faithfulness`. The only durable mitigation is
    *mechanical citation verification*: every `file:line` the LLM
    emits has to resolve at the build's HEAD commit, or the answer is
    rejected by the gate (Chapter 15).

None of these is a reason to give up on RAG — they are reasons to
stop calling "vanilla RAG" *the RAG*. The literature calls the
mitigation layer "Advanced RAG" {cite}`gao2023retrieval`; this book
calls it *the work*.

### GraphRAG and its neighbours

GraphRAG, introduced by Edge et al. at Microsoft Research
{cite}`edge2024graphrag`, is a specific answer to the third limit
above: the global-question, multi-hop problem. The intuition is
straightforward even if the engineering is not. Instead of retrieving
flat chunks and hoping the LLM stitches them back together, GraphRAG
*pre-computes* the stitching at index time by building a graph over
entities and relations extracted from the corpus, and then answers
global questions by summarising the graph, not the chunks.

Concretely, GraphRAG as described in the paper runs in four stages:

| Stage | Input | Output | Who pays |
|:--|:--|:--|:--|
| **1. Entity extraction** | Raw chunks | Typed entities + relations (via LLM extraction prompt) | Index-time LLM calls, O(chunks) |
| **2. Graph construction** | Entities and relations | A knowledge graph (nodes = entities, edges = relations with provenance) | Cheap |
| **3. Community detection** | The graph | Hierarchical clusters ("communities") via algorithms such as Leiden | Cheap |
| **4. Community summarisation** | Each community | An LLM-generated summary at each level of the hierarchy | Index-time LLM calls, O(communities) |

At query time, GraphRAG has two modes: **local** search (start from
the entities the query mentions, walk the graph, retrieve their
summaries) and **global** search (run the query against *every*
top-level community summary, map-reduce the answers). The global
mode is the thing vanilla RAG literally cannot do: every community
summary was produced with full visibility of its community's chunks,
so the map step has a fighting chance of returning a globally correct
answer to a globally framed question.

Two practical consequences follow:

1.  **GraphRAG is not cheaper than vanilla RAG. It is a different
    cost curve.** Indexing costs rise sharply — typically one to two
    orders of magnitude more LLM calls at index time — in exchange
    for query-time answers to questions vanilla RAG cannot answer at
    all. If your queries are all "what does `drainOnShutdown` do?",
    GraphRAG is wasted effort. If a non-trivial fraction of queries
    are "what are the three main subsystems of this codebase, and how
    do they talk to each other?", GraphRAG earns its indexing cost
    back on the first dozen queries.
2.  **The extracted graph is the product, not a byproduct.** The
    graph is human-inspectable, correctable, and re-usable for
    non-RAG purposes (visualisation, impact analysis, onboarding).
    Teams that adopt GraphRAG often end up valuing the graph more
    than the summarisation.

A neighbour worth knowing about is **HippoRAG**
{cite}`gutierrez2024hipporag`, which keeps the knowledge-graph
structure of GraphRAG but replaces Leiden + LLM-summarisation with a
personalised-PageRank-based retrieval step inspired by the
hippocampus's memory-indexing model. HippoRAG reports competitive
multi-hop answer quality at substantially lower index-time cost.
Whether it generalises to code KBs specifically is, as of 2025, an
open question — but the direction (graph structure + cheap
graph-algorithmic retrieval, instead of expensive LLM
pre-summarisation) is worth tracking.

This book does not ask you to pick a side in the GraphRAG-vs-vanilla
debate. Part V (Chapter 19) uses a small knowledge graph for a narrow
purpose — guided context assembly for code — which is closer in
spirit to GraphRAG-local than GraphRAG-global. The design choice is
always: *what class of question is hard for me, and what is the
cheapest structure that makes that class answerable?*

## How

Seven definitions do not yet tell you *which retriever to build
first*. A reasonable order of operations, and the order this book
takes, is:

0.  **Start with plain full-text search** — `rg` over the repo, or
    SQLite FTS5 over a collection of markdown notes — before you even
    write a chunker {cite}`fanyamin2026kb_pipeline`. If this does
    not already work, nothing downstream will rescue you: embeddings
    do not make bad file organisation findable. The vast majority of
    personal KBs, and an uncomfortable share of project KBs, are
    still operating below this line.
1.  **Upgrade to BM25** as soon as the full-text stage stops
    keeping up — when you want ranking by term rarity, field
    weighting, or phrase matching. BM25 is almost free, and it is a
    real baseline: *if the BM25 baseline beats you, you do not yet
    have a retrieval system, you have a vector store with
    decorations.*
2.  **Add dense retrieval** when you can afford embeddings and you
    have at least one query class that BM25 clearly fails on. For
    code KBs, that class is "paraphrased intent" (Chapter 10).
3.  **Fuse lexical and dense with RRF** {cite}`cormack2009rrf` once
    both retrievers independently work. Fusion makes both systems
    better and *almost never* makes either worse — but only if both
    rankers are individually sane.
4.  **Add a cross-encoder reranker** only when fusion with field
    weighting and freshness decay is measured and *still leaving
    precision on the table*
    {cite}`nogueira2019passage` {cite}`reimers2019sbert`. The
    reranker replaces the top-k slice of the fused list, not the
    fused list itself; a stage-1 top-100 reranked down to a stage-2
    top-10 is the canonical shape. Skip this step on a KB whose
    precision at top-3 is already good enough — adding a cross-encoder
    only buys latency in that regime.
5.  **Add a generator** only after retrieval and re-ranking are
    measured. A well-retrieved-but-badly-generated answer is a
    citation problem; a badly-retrieved-but-fluently-spoken answer is
    a hallucination problem. The book treats the second as the more
    expensive failure mode and delays generator tuning until Chapter
    13.
6.  **Evaluate before tuning anything** {cite}`thakur2021beir`. This
    is the step everyone skips. The book does not.
7.  **Consider GraphRAG only when the query workload demands it**
    {cite}`edge2024graphrag`. If more than, say, 20% of real queries
    are globally framed — *"what are the main components", "how has X
    evolved", "which modules depend on which"* — the cost curve
    favours a graph. If they are mostly local — *"where is X called",
    "what does Y return"* — it does not.

The blog post underlying this book {cite}`fanyamin2026deepwiki` uses
the same core ordering, and uses it as an argument against what it
calls the "Demo-grade approach": ingest-then-LLM, with neither a
ranking baseline nor an evaluation harness. This chapter adds steps
0, 4, 6, and 7, which the blog treats implicitly.

### Choosing the retrieval substrate

At some point between step 2 and step 3, you will stop being able to
hide behind *"we'll pick a vector store later"*. The choice of
substrate — the thing that actually stores and searches your index —
materially constrains every lever in this chapter. Field weighting,
freshness decay, structured filtering, hybrid fusion: each is either
a one-line feature or a ground-up engineering project, depending on
the substrate. The four realistic options as of 2026, and the
workloads each earns
{cite}`fanyamin2026pgvector_rag` {cite}`fanyamin2026elasticsearch_rag`:

| Substrate | Best when | Pays for itself when | Skip if |
|:--|:--|:--|:--|
| **Plain full-text** (`rg`, SQLite FTS5, PostgreSQL `tsvector`) | You are one person; the corpus fits on one machine; the hard question is *find the file*, not *rank the paragraph*. | Cost is zero; latency is sub-second; no model dependency. | You need paraphrase matching or ranked top-k across dozens of documents. |
| **pgvector on PostgreSQL** | You already run PostgreSQL; corpus is under a few million vectors; you want vectors and business rows to `JOIN`. | Zero new operational surface; ACID; one `CREATE EXTENSION vector`. HNSW + cosine distance handles most paraphrase queries at millisecond latency. | You need first-class BM25, field weighting, or function-scoring built in (you can layer them on with `tsvector`, but you are now writing the features Elasticsearch ships). |
| **Elasticsearch / OpenSearch** | You need BM25 *and* vectors *and* structured filtering *and* field weighting *and* freshness scoring in one query; your users search with identifier literals as often as with paraphrases. | Native hybrid retrieval with RRF, Function Score for decay, bool queries for filtering, Kibana for quality inspection. | You do not have JVM capacity; a single node is not enough for your traffic; the team has no operational experience with it. |
| **Specialised vector DB** (Pinecone, Milvus, Qdrant, Weaviate, …) | Corpus is tens of millions of vectors or more; you need multi-tenant isolation, auto-sharding, or managed SLAs. | Scale and managed-service SLAs beyond what a single pgvector or ES cluster will give you. | Corpus is under a few million; cost transparency matters; you do not need the scale knobs. |

The book's running prose-layer example fits comfortably in pgvector;
the running code-layer example is larger but still lives inside a
pgvector + BM25 hybrid. Neither needs Elasticsearch, let alone a
specialised vector database. That is not an accident — it is the
*typical* scale of a software project's knowledge base. The
"defaults-first" heuristic is: **start with pgvector, add
Elasticsearch when mixed identifier-literal and paraphrase queries
force your hand, and keep specialised vector stores in reserve for
the scale cliff you will probably never hit**
{cite}`fanyamin2026pgvector_rag`.

## Example

A toy corpus will do. Imagine four snippets in a Go repository:

```text
D1  func runSync(ctx context.Context) error { ... }   // internal/worker/pool.go:40
D2  defer func() { if r := recover(); r != nil { ... } }  // internal/worker/pool.go:55
D3  func drainOnShutdown() { ... }                     // internal/worker/pool.go:287
D4  // how to safely shut the worker pool down        // doc/runbook/shutdown.md:12
```

Now three queries, and how each retriever would score them:

| Query | BM25 winner | Dense winner | RRF winner | GraphRAG winner |
|-------|-------------|--------------|------------|-----------------|
| *"who calls `runSync`"* | D1, then D3 (identifier match) | D1, then D3 | D1 — agreement is cheap | D1 via the call-graph edge `caller → runSync` |
| *"how do we wait for workers to finish"* | D4 (keyword "wait"/"workers") but misses D3 | D3 (paraphrase of "drain on shutdown") | D3 and D4 both rank highly | D3 via graph walk from `worker-pool` community |
| *"what are the main shutdown concerns in this package"* | none of the four is obviously best | same — dense over-weights any single chunk | same — RRF cannot invent a global view | a pre-computed summary of the `shutdown` community |

The first two rows are the case for hybrid retrieval: neither retriever
alone answers both queries well. The third row is the case for
GraphRAG: neither BM25 nor dense nor their fusion can answer a global
question from four disconnected chunks. You can force an LLM to guess
an answer; you cannot force any of those retrievers to *find* it.
Chapter 12 walks through an actual RRF implementation from the
code-layer reference implementation and measures the effect on real
queries; Chapter 19 does the equivalent walkthrough for a
GraphRAG-local-style graph over code.

A competing view a reader should weigh is **dense-only retrieval with
long context packing** — the shape that many *"just throw the repo at
Gemini 2.5 or Claude Opus 4"* approaches take. For small, low-traffic
repositories this can be perfectly adequate, and it has the clear
advantage of needing no infrastructure. Its disadvantages are latency,
cost, and — critically — that it loses structural filtering: *"only
functions in package `worker`"* is a one-line predicate over a BM25
index and a prompt-engineering nightmare in a context-only pipeline
{cite}`fanyamin2026deepwiki`. It also cannot, in principle, answer
the third row of the table above any better than vanilla RAG: a
million-token context without structure is still a bag of chunks.

## Conclusion

Four claims summarise the chapter and set up the rest of the book.

*Ranking is the hard part of retrieval; generation is the easy part.*
Teams that optimise the generator before the ranker end up with fast
nonsense. The book assumes this lesson has been learnt — every
retriever before every generator, every benchmark before every
retriever, every citation before every answer.

*Vanilla RAG is a baseline, not a destination.* Its five limits —
chunk boundaries, similarity-vs-relevance, multi-hop gaps, staleness,
and faithfulness — are engineering problems with engineering answers.
The rest of this book is the long form of those answers.

*GraphRAG is not an upgrade to vanilla RAG; it is a different cost
curve for a different class of question.* Adopt it when your queries
are globally framed, skip it when they are not, and in either case
remember that the graph is itself an asset — it outlives any one
retrieval strategy.

*Substrate is a workload choice, not a fashion choice.* The decision
between `rg`, pgvector, Elasticsearch, and a specialised vector
database is driven by the shape of your queries and the size of your
corpus, not by which project trended on Hacker News last month. The
most common mistake is to skip the first option and pay for the
last.

## References

```{bibliography}
:filter: keywords % "ir-rag" or keywords % "fusion" or keywords % "evaluation" or keywords % "graph-rag" or keywords % "foundations" or keywords % "deepwiki"
```
