---
title: "Chapter 1 — Why a Knowledge Base for Software?"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - foundations
  - software-docs
  - deepwiki
  - competitor
---

# Chapter 1 — Why a Knowledge Base for Software?

This chapter on one page — four kinds of material, four properties,
two reference implementations, and three forces that changed the
economics:

```{mermaid}
mindmap
  root((Software KB))
    Four kinds of material
      Code and structure
      Prose (Diataxis)
      Decisions (ADRs)
      Runbooks and ops lore
    Four properties
      Queryable (ch7, ch12)
      Provenance (ch5)
      Layered (ch18)
      Honest (ch13)
    Two reference impls
      Prose layer (file-based wiki)
      Code layer (tree-sitter + graph + pgvector)
    Why now
      Embeddings 5x cheaper
      Tree-sitter parses fast
      LLMs close the loop
```

## Why

Imagine a first-day engineer opening a mid-sized service repository. They
ask their senior teammate a question that sounds innocent: *"where is
`runSync` called from, and why does its `defer` block include a
`recover`?"*. The answer they usually get is some version of "just read
the code." The blog post that this book is built on {cite}`fanyamin2026deepwiki`
opens with exactly this scene, and it lingers on the scene for a reason:
the scene is not about that one function. It is about the shape of every
modern codebase.

A production repository today is routinely hundreds of thousands of lines
long, spread across dozens of packages and layered on top of internal
frameworks that the new-hire has never seen. The README describes the
repository as it was two years ago. The architecture diagram is in a
slide deck no one can find. The comments were written for the compiler,
not for a human. The institutional memory — *why we picked this data
store, why this function has a retry, who to page when it breaks* — lives
mostly in the heads of three senior engineers who are, at that moment,
in a meeting.

This is not a new complaint. David Parnas argued in 1986 that no real
software project follows a rational design process, but that we should
nevertheless *fake one in the documentation* so that the artifact we
leave behind is understandable to future maintainers
{cite}`parnas1986rational`. Seventeen years later, Lethbridge, Singer and
Forward surveyed working engineers and found the expected gap: engineers
acknowledge that documentation is important and simultaneously admit
they rarely read it, rarely trust it, and routinely treat source code
and personal conversations as their primary sources of truth
{cite}`lethbridge2003software`. Another sixteen years on, Aghajani and
colleagues systematically catalogued the documentation issues that show
up in issue trackers and found — unsurprisingly — that staleness,
completeness gaps, and wrong-audience material dominate the list
{cite}`aghajani2019software`.

Forty years, three papers, one uncomfortable pattern: we have known
about this problem longer than many current engineers have been alive,
and we still do not solve it. What has changed, recently, is the
economics of *not asking humans to write the KB in the first place.*
Three forces compound. Embedding-model prices dropped roughly 5× in a
single release cycle in early 2024 — OpenAI's `text-embedding-3-small`
at US \$0.00002 per 1K tokens is the public marker, and open-weights
models such as BGE {cite}`xiao2024bge` remove the per-token cost
entirely on a modest GPU. Tree-sitter {cite}`brunsfeld2018treesitter`
parses a mid-sized repository on a laptop in single-digit seconds,
across a dozen languages, without a build system. Large language
models have made the *generation* side of retrieval-augmented
workflows accessible to any team that can write a prompt. The three
together turn the question on its head: it stops being "can we afford
to write a KB" and becomes "can we afford *not* to derive one"
{cite}`openai_embeddings_v3`.

## What

A **software knowledge base** in this book is the union of the answers
a team needs in order to do its work, stored somewhere those answers
can be retrieved with high precision and verifiable provenance.
Concretely, that union contains at least four kinds of material:

1. **Code and its structure** — the files, functions, classes, call
   graphs, and type signatures that answer questions like *"where is
   `runSync` called from"* without a human interpreting. The repository
   is the authoritative source; the KB's job is to make it queryable.
2. **Prose** — the tutorials, how-to articles, reference pages, and
   explanations that answer *"how do I do X"* and *"what does this
   module actually mean"*, classified by Diátaxis type
   {cite}`procida_diataxis` (see Chapter 3).
3. **Decisions** — Architecture Decision Records
   {cite}`nygard_adr,madr` that answer *"why is it this way and not
   some other way."* Crucially, an ADR records the alternatives that
   were rejected and who was in the room when the call was made. ADRs
   are the part of the KB that survives re-orgs.
4. **Runbooks and ops lore** — how to deploy, how to debug, what an
   alert at 3 a.m. actually means, and who to page when it does.

We will call the whole thing a *KB* for short. It is not a wiki, not
an issue tracker, not a chat search. It is the union of those,
organized so that both humans and agents can ask it questions and get
grounded answers.

A KB in the sense of this book has four properties, each earning its
own chapter later: it is **queryable** (retrieval works), has
**provenance** (every fact points to a file, a commit, or an ADR),
is **layered** (machine-generated content sits next to hand-written
content and the two are distinguishable), and is **honest** (when the
KB does not know, the KB says so). Provenance is Chapter 5, layering
is Chapter 18, honesty is Chapter 13, and queryability is most of
Part III.

Three recent papers make the timing of this book less accidental than
it would have looked two years ago. Zhu et al.'s survey of LLMs for KG
construction and reasoning finds that frontier models are generally
stronger as **reasoning assistants over structured context** than as
few-shot extractors of structure itself {cite}`zhu2024llmsknowledgegraphconstruction`.
That is almost the book's architecture in one sentence: use parsers,
schema, and verification to build the KB; use the LLM to explain,
synthesize, and route over it. RepoAgent frames repository-level
documentation as a pipeline with **global structure analysis,
documentation generation, and documentation update**
{cite}`luo2024repoagentllmpoweredopensourceframework`. That validates
the book's insistence that "write docs with AI" is not one prompt but a
maintained system. CGM goes one step further and shows that
repository-level code graphs are valuable enough to be pushed into the
model itself, not just kept beside it as an index
{cite}`tao2025codegraphmodelcgm`. In other words: the field is
converging on the same three ingredients this book treats as first-
class artifacts — structure, maintenance, and graph-guided reasoning.

## How

The next twenty-three chapters are an implementation of those four
properties on top of two real reference systems the author uses daily:

- **The prose-layer reference implementation** — a file-based wiki
  that handles prose, decisions, and runbooks. It is the repository
  you are reading this book inside.
- **The code-layer reference implementation** — a companion service
  that handles code structure via tree-sitter parsing
  {cite}`brunsfeld2018treesitter`, a property graph stored in
  Memgraph, and dense embeddings stored in pgvector.

Neither system is new or experimental. What the book adds is **the
missing tissue between them**: the IR theory (Chapter 2), the
doc-type taxonomy (Chapter 3), the provenance discipline (Chapter 5),
the document-layer model (Chapter 18), and the evaluation and
operations practice (Part IV).

The system this book describes is **strictly more flexible and
strictly more work** than a hosted service. That is the honest
trade-off; different teams will pick different sides of it. The most
visible hosted alternative today is **DeepWiki**
{cite}`cognition_deepwiki`, a closed-source SaaS that auto-generates
wiki-style pages for any public GitHub repository. DeepWiki's output
is frequently impressive as a reading experience, and the source blog
post is titled "give your repo its own DeepWiki"
{cite}`fanyamin2026deepwiki` for that reason. What DeepWiki does not
give you is ownership of the pipeline, control over the document-type
taxonomy, a place to put ADRs, or the ability to hook the KB up to
your team's IDE agents on your own terms. Other systems in this space
— Sourcegraph Cody {cite}`sourcegraph_cody` for code-level Q&A,
Notion AI {cite}`notion_ai` for prose-level Q&A — each solve a
*piece* of the problem well. The book's angle is that the pieces
belong together, and that building the integrated version is now
affordable.

### Who this book is for

This book assumes a team that owns a real codebase (on the order of
50k lines and up, three or more engineers, at least a year of
history), is willing to run a small Docker Compose stack and pay for
embedding-model calls in the low single-digit dollars per full sync,
and wants to keep the pipeline on-premises or on its own cloud
account rather than hand it to a vendor. If you can describe your
documentation problem in one sentence and a page of DokuWiki would
close it, this book is overkill. If your codebase has grown past the
point where any one person holds it all in their head, this book is
the cheap option.

## Example

Here is the shape of what we want "using the KB" to feel like by the end
of Part V. The new-hire's question — *"where is `runSync` called from,
and why does its `defer` include a `recover`?"* — should produce an
answer with the structure shown below. The repository names, line
numbers, commit, and ADR in the block are **an illustrative mock-up**;
Appendix B reproduces an answer of exactly this shape against a real
codebase using a real HTTP call, and Chapter 13 explains how the
confidence line is computed.

```text
runSync is called from 4 sites:
  - internal/worker/pool.go:142  (Pool.dispatch)
  - internal/worker/pool.go:287  (Pool.drainOnShutdown)
  - cmd/sync/main.go:58          (runCLISync)
  - internal/test/integration.go:31 (harness)

The defer/recover pattern was added in commit 4a1c92b
("handle panic in sync goroutine without killing the pool", 2024-03-02)
and is discussed in ADR-0014 ("Panic-safety in worker pools"):
> We chose to recover and log because a panic in a single sync target
> must not take down sibling targets; see incident I-2024-02-17.

Confidence: high (4 citations; ADR present; call graph up to date
as of commit 4a1c92b).
```

The shape is what matters. In the real system each of those citations
is a `file:line` anchor resolved from the call graph at the current
commit, not a paraphrase from a training corpus. The confidence line
is mechanical: it counts citations, checks whether an ADR is attached,
and compares the KB's `last_synced_commit` to `git HEAD`. If the answer
cannot meet its own bar, the KB is allowed — and required — to say so
(Chapter 13).

The machinery that produces this kind of answer is the subject of
Parts III through V. The ingredient list, however, is only four items
long: tree-sitter, an embedding model, a graph store, and a disciplined
prompt. Those are the four corners the blog post
{cite}`fanyamin2026deepwiki` names as 四件套 ("the four-piece set"), and
the book spends the middle chapters picking each corner apart.

## Conclusion

The gap between "the codebase" and "what the team needs to know about
the codebase" is older than most of the current software stack. It has
outlasted CVS, Subversion, and three generations of wiki software. What
has finally shifted is the cost of *deriving* a KB from artefacts we
already have, rather than asking humans to hand-write one in parallel
with their actual work. The rest of this book is a concrete recipe for
that derivation, written with enough citations and code that a reader
can, if they want, rebuild the whole thing and then replace every piece
they disagree with.

## References

```{bibliography}
:filter: keywords % "software-docs" or keywords % "deepwiki" or keywords % "foundations" or keywords % "competitor"
```
