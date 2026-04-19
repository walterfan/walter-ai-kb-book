---
title: 'Chapter 18 — Document Layering L0–L4'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - hybrid
  - adr
  - governance
---

# Chapter 18 — Document Layering L0–L4

## Why

A mature knowledge base contains pages that are not of the same *kind*
even when they are of the same Diátaxis *type* (Chapter 3). A
`runbook.md` written by an experienced on-call engineer and a
`runbook.md` regenerated yesterday by an LLM are both how-tos. They
both live under `content/`. They both have the same frontmatter
schema. But they are not equally trustworthy, and a retrieval system
that treats them as equals will eventually answer a 3 am incident
question with the wrong page.

The blog post the book builds on {cite}`fanyamin2026deepwiki`
introduces a five-tier **document-layer** model (L0 – L4) that
distinguishes pages by their *authorial provenance* — who wrote the
page and how much authority attaches to it. This chapter makes that
model precise, shows why a single-axis layering is not enough, and
upgrades it to a four-tuple that integrates the footer fields
Chapter 5 introduced.

## What

### The single-axis L0 – L4 model

The blog's original L0–L4, stated compactly:

| Tier | Authority | Who writes | Examples |
|:--:|:--|:--|:--|
| **L0** | Strongest | Code and its comments | Function bodies, docstrings, OpenAPI specs |
| **L1** | Strong | Humans, committed | ADRs, architecture docs, hand-written runbooks |
| **L2** | Moderate | Humans, collaborative | Wiki pages, design docs, retros |
| **L3** | Weak | AI, reviewed | LLM-generated summaries a human approved |
| **L4** | Conditional | AI, unreviewed | LLM-generated drafts waiting for review |

The single-axis model is good as a first move. It correctly names the
single most common confusion: that AI-drafted prose and human-written
ADRs should not be retrieved with equal weight. A retrieval layer
that weights results by tier — boost L0, boost L1, down-weight L4 —
immediately behaves better than one that does not.

### Why one axis is not enough

The single-axis model still conflates two things a KB has to treat
separately: **who wrote the current version** and **has anyone
reviewed it**. They correlate but they are not the same. Consider
four pages all of Diátaxis type `how-to`:

1.  A human wrote it three months ago; it has not been reviewed
    since.
2.  A human wrote it yesterday; another human reviewed it today.
3.  An LLM drafted it yesterday; a human reviewed and approved it
    today with a score of 4.
4.  An LLM drafted it yesterday; no one has reviewed it.

The single-axis model collapses (1) and (2) into L2 and (3) and (4)
into L3/L4. But a working retrieval layer wants to treat (3) more
like (2) than like (4): in case (3) a human has actually signed off,
which is the signal that matters. The prose is AI-drafted, but the
authority is human-verified.

This is the gap the footer's review fields close. Chapter 5's
`PKB-metadata` footer gives every page four values that together
identify its kind more precisely than any single axis can:

- `layer` ∈ {L0, L1, L2, L3, L4} — *where in the hierarchy does this
  page sit?*
- `updated_by` ∈ {`human`, `ai`, `ai+human`} — *who authored the
  current version?*
- `review_status` ∈ {`pending`, `approved`} — *has a human signed
  off?*
- `review_score` ∈ [0, 5] — *how good is it, in the reviewer's
  judgement?*

### The tuple model

The upgraded document layer is the tuple

$$
\text{layer} = \langle L, U, R, S \rangle
$$

where $L$ is the single-axis tier, $U$ is `updated_by`, $R$ is
`review_status`, and $S$ is `review_score`. The author's private
project-knowledge-base toolkit {cite}`fanyamin_pkb_skill` encodes
exactly this four-valued stance. Two pages at "the same layer" on
the old scale can now be distinguished:

| Page | Old tier | Tuple | Retrieval weight |
|:--|:--:|:--|:--:|
| L1 ADR, human-written, approved, score 4 | L1 | ⟨L1, human, approved, 4⟩ | 1.0 |
| L1 ADR, LLM-updated, pending review | L1 | ⟨L1, ai, pending, 0⟩ | 0.3 |
| L3 summary, LLM-drafted, human-approved, score 4 | L3 | ⟨L3, ai+human, approved, 4⟩ | 0.8 |
| L3 summary, LLM-drafted, no review | L3 | ⟨L3, ai, pending, 0⟩ | 0.2 |

The retrieval weight is one plausible projection; Chapter 19's
graph-guided context assembly uses a richer function, but the
principle is the same. The tuple exposes four numbers the retrieval
code can *actually use*, where the old single axis exposed one.

## How

### Assigning tuples at ingestion

The pipeline (Chapter 7) assigns $\langle L, U, R, S \rangle$ when a
page is created or updated. Three rules cover almost every case:

1.  **At creation**, $L$ is inferred from the path: `adr/` → L1;
    `architecture/` → L1; `content/` with `created_by: human` → L2;
    `content/` with `created_by: ai` → L4. $U$ mirrors `created_by`.
    $R$ is `pending` if `created_by: ai`, else `approved`. $S$ is
    `0` if `created_by: ai`, else a default set by the author.
2.  **On L1 mechanical update** (Chapter 16): $L$ is unchanged (a
    re-stamp does not move a page between tiers); $U$ set to `ai`
    (the automated actor); $R$ to `pending`; $S$ to `0`.
3.  **On L2 bounded-LLM update** (Chapter 16): $L$ is unchanged; $U$
    set to `ai`; $R$ to `pending`; $S$ to `0`. If a human later
    approves, $U$ transitions to `ai+human`, $R$ to `approved`, $S$
    to the reviewer's score.

These rules are the **AI-always-sets-pending** rule (Chapter 5) and
the **L3 human review** path (Chapter 16), restated in the tuple's
vocabulary. They are not new policy; they are consequences of the
rules stated elsewhere, re-expressed as tuple transitions.

### Using the tuple at retrieval

A retrieval layer (Chapters 12, 19) scores a candidate page with a
function roughly like:

```text
function score(page, query):
    base   = vector_score(page, query)       # cosine, etc.
    L_w    = tier_weight(page.layer)          # e.g. L0=1.0 … L4=0.4
    R_w    = 1.0 if page.review_status == approved else 0.4
    S_w    = max(0.5, page.review_score / 5)
    return base * L_w * R_w * S_w
```

Exact weights are a tuning choice, not a claim of this book. The
interesting move is *that the score depends on four values of the
footer, not one*. A page whose layer is L1 but which is currently
unreviewed after an L2 rewrite sinks below a truly approved L2 page.
That is the behaviour a KB needs; the tuple makes it expressible in
a few lines of code.

### Using the tuple at publish time

The gates from Chapter 15 already read the footer fields directly,
but the tuple formalises one additional check: **authority
consistency.** A page whose $U = \text{ai}$ and $R = \text{approved}$
must have a non-empty `reviewed_by`; a page whose $L = \text{L0}$
must have $U = \text{human}$ because code is not LLM-generated at
this layer. Checks like these are one line each; they catch
mis-tagging before publish.

## Example

A before-and-after for the same page under the two models:

**Single-axis view.** A page `runbook/ingest-pipeline-failure.md` has
frontmatter `doc_type: how-to, status: published, verification_status:
unreviewed`. The blog's single-axis model would classify it as L3 (AI
prose, notionally reviewable). Retrieval weights it at ~0.6.
Problem: the page was actually written by a human two weeks ago; it
says `unreviewed` only because a cron job flipped the status when no
one had re-verified it. The single axis cannot tell the difference.

**Tuple view.** The same page's full footer reads:

```markdown
<!-- PKB-metadata
last_updated: 2026-04-05
commit: a1b2c3d4
updated_by: human
review_status: pending
review_score: 0
reviewed_by:
-->
```

Tuple: ⟨L2, human, pending, 0⟩. The retrieval layer reads: human
authored, not formally reviewed, score unknown. This is a different
thing from ⟨L3, ai, pending, 0⟩ (AI drafted, never reviewed), and
different again from ⟨L2, human, approved, 4⟩ (human authored,
human approved, high score). All three would have been L2 or L3 in
the old model. In the tuple model they each get a distinct score.

A soft gate (Chapter 15 S2) flags the first page to the reviewer:
*"human-authored runbook, never reviewed; please check at least once.
Takes a minute; prevents a 3 am problem."*

## Conclusion

The single-axis L0–L4 was a good first move: it made explicit that
authorial provenance is a first-class attribute of a document. The
tuple upgrade is the honest continuation: authorial provenance is
itself two separate questions — *who wrote this* and *who signed off
on it* — and a KB that wants to survive LLM-era editing has to answer
both. The four-tuple fits in a footer; it is cheap to write, cheap to
read, and cheap to enforce.

The next chapter uses the tuple at retrieval time: Chapter 19's
graph-guided context assembly uses $L$ to prioritise tier, $R$ and
$S$ to filter unreviewed or low-quality pages out of an LLM's context
window, and the relation graph to pull in whatever else the top-k
pages reference.

## References

```{bibliography}
:filter: keywords % "hybrid" or keywords % "adr" or keywords % "governance" or keywords % "self-citation"
```
