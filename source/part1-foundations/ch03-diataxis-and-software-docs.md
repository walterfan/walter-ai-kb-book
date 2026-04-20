---
title: "Chapter 3 — Diátaxis and Software Docs"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - foundations
  - diataxis
  - software-docs
  - competitor
---

# Chapter 3 — Diátaxis and Software Docs

This chapter on one page — the two classification axes the chapter
argues a software KB needs, the four Diátaxis doc types, the
opinionated ten-page instantiation this book adopts, and what is
deliberately *not* on that list:

```{mermaid}
mindmap
  root((Diataxis for software))
    Reader-intent axis
      Tutorial (learning)
      How-to (task)
      Reference (information)
      Explanation (understanding)
    Author-and-trust axis
      verification_status
      source (original / git / doc / url)
      Layers L0-L4 (ch18)
    What it replaces
      Freeform tags
      "Miscellaneous"
      Filing problems
    Ten-page instantiation
      00 overview
      01 quick-start
      02 architecture (C4)
      03 repo-map
      04 data-and-api
      05 workflows
      06 conventions
      07 testing
      08 runbook
      09 observability
    Not in the cut
      ADRs (a collection, ch18)
      changelog (subsumed by git)
```

## Why

A knowledge base without a document-type taxonomy is a search problem.
A knowledge base with the *wrong* taxonomy is a filing problem. Filing
problems are more expensive than search problems because filing
problems are authored, and authored mistakes compound.

The working engineers Lethbridge and colleagues surveyed
{cite}`lethbridge2003software` were asked, effectively, *"why do you not
read the docs?"* The answers boiled down to: *because I do not know
which document answers my question, and when I find one, it turns out
not to be the document I wanted.* Aghajani et al.
{cite}`aghajani2019software` two decades later report the same
symptom in a different register: large fractions of bug reports about
documentation are "wrong type of content for the section it lives in."

A good taxonomy makes this symptom disappear. Daniele Procida's
**Diátaxis** {cite}`procida_diataxis` is, at time of writing, the
taxonomy most likely to survive contact with a real software project.
It has four types; it is orthogonal along two axes; it is small enough
to fit on a postcard; and — most importantly for this book — it is
small enough that a classification pipeline, human or LLM-driven, can
actually be trained against it without hand-wringing over twenty-way
ties.

## What

Diátaxis divides technical documentation along two axes, producing
four quadrants {cite}`procida_diataxis`:

```{mermaid}
graph TB
  subgraph Theory
    Explanation["Explanation<br/>(understanding-oriented)"]
    Reference["Reference<br/>(information-oriented)"]
  end
  subgraph Practice
    Tutorial["Tutorial<br/>(learning-oriented)"]
    HowTo["How-to<br/>(task-oriented)"]
  end
  Tutorial <---> Explanation
  HowTo <---> Reference
```

|                   | Practical                     | Theoretical                  |
|-------------------|-------------------------------|------------------------------|
| **Studying**      | **Tutorial** — learning-oriented | **Explanation** — understanding-oriented |
| **Working**       | **How-to** — task-oriented      | **Reference** — information-oriented     |

The two axes (*practical ↔ theoretical* and *studying ↔ working*) are
not about the writer's mood; they are about the reader's state. A
reader is either studying (trying to build a mental model) or working
(trying to get something done right now). Orthogonally, they are
either seeking concrete action or seeking concepts. Any piece of
writing that honestly answers *both* axes at once is almost certainly
two pieces of writing that got glued together.

An important property of the taxonomy for our purposes is that a
document's type determines *the shape of its ideal first sentence*:

- A **tutorial** starts with what the reader will build.
- A **how-to** starts with the goal state the reader wants to reach.
- A **reference** starts with the name of the thing being described.
- An **explanation** starts with the question being answered.

This will matter in Chapter 6, where we ask an LLM to classify raw
imports into the four types.

## How

The prose-layer reference implementation lifts Diátaxis directly into
its frontmatter schema. From `wiki-template/metadata/SCHEMA.md`:

```yaml
---
title: "Page Title"
doc_type: reference            # tutorial | how-to | reference | explanation
verification_status: supported # supported | unreviewed | uncertain | contradicted | superseded
created_by: alice
updated_by: alice
source:
  type: original               # original | git_repo | doc | url
  uri: ""
---
```

Two observations are worth pausing on.

**First**, `doc_type` is a first-class *field*, not a free-form tag. It
has four legal values, not a hundred. That constraint is load-bearing.
Every downstream component — the search index (Chapter 7), the
LLM-assisted classifier (Chapter 6), the ADR-vs-runbook separation
(Chapter 18) — assumes that `doc_type` is one of exactly four labels.
The moment the project admits a fifth, the classifier has to be
retrained, the index has to be re-weighted, and every rule in the
layer model has to be audited. Staying at four is cheap; growing to
five is never cheap.

**Second**, the schema bundles `doc_type` with a *trust* field
(`verification_status`) and a *provenance* field (`source`). This is
not incidental. The blog post the book builds on
{cite}`fanyamin2026deepwiki` argues in its §11 that *document layering*
(L0 – L4, which Chapter 18 unpacks in full) is the mechanism that
keeps AI-generated pages, human-authored runbooks, and architectural
decisions from getting confused for one another. Diátaxis classifies a
document along the *reader-intent* axis; `verification_status` and
`source` classify it along the *author-and-trust* axis. Both axes have
to be present for a software KB to stay honest.

A specific competing view deserves direct engagement. **DITA**
{cite}`oasis_dita`, the OASIS-maintained "Darwin Information Typing
Architecture", is the formal taxonomy that the large technical-writing
industry uses. DITA is richer than Diátaxis, has XML schemas, and
supports arbitrary content types (`task`, `concept`, `reference`,
`troubleshooting`, plus specialisations). For a technical-writing team
producing printed manuals across multiple products, DITA is the right
tool. For a software team producing wiki pages alongside code, DITA
imposes a tooling cost — XML editors, DITA-OT build pipelines,
specialised authors — that outweighs its flexibility. Diátaxis's
willingness to be *small* is, in our context, a feature, not a
limitation. The Write-the-Docs community style-guide corpus
{cite}`wtd_write_the_docs` comes to a similar practical conclusion.

## Example

A dump of the pages under `wiki-template/content/` — the template this
repo uses to seed a new wiki — falls cleanly into the four Diátaxis
types:

| File | Diátaxis type | Reader's state | Why |
|------|---------------|-----------------|------|
| `content/devops/kubernetes.md` | **reference** | working | surveys Kubernetes primitives with signatures and examples |
| `content/devops/docker.md` | **reference** | working | same pattern, focused on Docker CLI + Compose |
| `content/programming/go/concurrency.md` | **explanation** | studying | "understanding-oriented" — why goroutines, channels, and `sync` are shaped the way they are |
| `content/programming/go/interfaces.md` | **explanation** | studying | discusses the *idea* of structural typing in Go rather than a step-by-step recipe |
| `content/programming/python/asyncio.md` | **explanation** | studying | same shape as the Go concurrency page |
| `content/programming/python/decorators.md` | **explanation** | studying | discusses what decorators *are* and when to reach for them |

The template folder, as it ships, contains mostly explanations and one
reference section — there are no tutorials or how-tos yet. That is a
*feature-state* observation about this template (it is a starter set,
not a finished KB), not a bug. The classification exercise makes the
gap visible immediately: a mature project using this wiki should
acquire tutorials (onboarding paths) and how-tos (runbooks) over time.
Chapter 6's classification pipeline flags exactly that kind of
imbalance when it reports doc-type histograms.

The same exercise on the `wiki-template/metadata/SCHEMA.md` file itself
is interesting: it is a **reference** (it documents the schema) that
also contains a small **explanation** ("Trust Model" section, lines
48–53). This is a useful reminder that Diátaxis is a classifier over
*files*, not over *paragraphs*. A document-layer review (Chapter 18)
should flag files whose body spans two quadrants and consider whether
to split them.

## One opinionated instantiation

Diátaxis tells you the *kinds* of page. It does not tell you *which
specific pages* a software project should ship. Two teams can both be
"Diátaxis-compliant" and still end up with wildly different tables of
contents: one writes five tutorials and no runbook; the other writes a
runbook, a reference, and nothing else. Both are defensible. Neither
helps a new engineer who has to figure out *where the runbook lives*
in a project they have never seen before.

The author's private project-knowledge-base toolkit
{cite}`fanyamin_pkb_skill` resolves this by committing to a small,
stable set of pages — one concrete answer to "which specific pages
should a software KB have?" — with numbers that fix the reading order.
This book adopts a ten-page cut of that set as its canonical
instantiation. Teams are free to diverge; the claim is not that these
ten are the *only* valid pages, but that picking *some* stable set,
early, is more valuable than arguing about which set:

| # | Page | Diátaxis type | Reader's state | What it answers |
|---:|------|---------------|-----------------|-----------------|
| 00 | `overview` | explanation | studying | *"What is this project, in five minutes?"* |
| 01 | `quick-start` | tutorial | studying | *"How do I get to 'hello world' in ten minutes?"* |
| 02 | `architecture` | explanation | studying | *"What are the containers, components, and why?"* (C4; see Chapter 4) |
| 03 | `repo-map` | reference | working | *"Where is what, at the current commit?"* |
| 04 | `data-and-api` | reference | working | *"What is the public contract?"* |
| 05 | `workflows` | reference | working | *"What does the code actually do, step by step?"* |
| 06 | `conventions` | reference | working | *"Naming, layout, style rules."* |
| 07 | `testing` | how-to + reference | working | *"How do I run tests, and what do they cover?"* |
| 08 | `runbook` | how-to | working | *"When it breaks, what do I do?"* |
| 09 | `observability` | reference | working | *"What do I watch, and where do I look?"* |

Two notes on what is *not* on this list. There is no `adr/` page,
because ADRs are a *collection*, not one page; they live under their
own directory and are layered separately in Chapter 18. There is no
`changelog`, because a well-kept Git history plus release notes
subsumes it for most teams.

The numbering matters more than it looks. A reader landing cold on a
project's docs should be able to read `00` through `04` in order and
be ready to touch the code; `05` through `09` are what they return to
when they are working. A tool scanning the KB — the classification
pipeline in Chapter 6, the document-layering tuple in Chapter 18 —
gets a stable directory shape to target. And a maintainer deciding
whether to accept a new page has a simple test: *does this fit into
one of the ten slots, or does it want to be an eleventh?* The moment
the answer is "an eleventh", the discussion is "is this page worth
restructuring the taxonomy for?" — a productive question — rather than
"where shall I put this?" — a filing problem.

This is one concrete answer. Chapter 7a ("The prose-layer operational
model") makes it Corner C1 of the book's four-corner operational
model.

## Conclusion

Once `doc_type` is a first-class, four-valued field, downstream
problems shrink. Search weighting can prefer how-tos for "how do I"
queries. The LLM classifier has a closed vocabulary. The document-layer
model has something to hang its rules on. ADRs, vision documents, and
runbooks — none of which are pure Diátaxis types — get their own
first-class layer in Chapter 18, rather than being shoehorned into a
"Miscellaneous" category no one searches. Keeping the taxonomy small
is not parsimony for parsimony's sake; it is what makes every
downstream chapter in this book implementable.

## References

```{bibliography}
:filter: keywords % "diataxis" or keywords % "software-docs" or keywords % "competitor" or keywords % "deepwiki"
```
