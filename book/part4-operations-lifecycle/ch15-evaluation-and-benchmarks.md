---
title: 'Chapter 15 — Evaluation, Benchmarks, and Publish Gates'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - operations
  - ir-rag
  - evaluation
---

# Chapter 15 — Evaluation, Benchmarks, and Publish Gates

## Why

A KB that cannot answer *"how do I know this build is good?"* cannot
claim to be maintained. The question has two honest decompositions, and
this chapter treats both:

1.  **Evaluation** — *how good is the retrieval + generation system
    the KB powers?* This is the IR-literature question: precision at
    k, nDCG, answer-faithfulness. Benchmarks like BEIR
    {cite}`thakur2021beir` and RAGAS {cite}`es2024ragas` exist because
    different teams converged on needing the same answer.
2.  **Gating** — *is this specific build of the KB well-formed enough
    to publish?* This is the build-engineering question: is every
    page's footer present, do references resolve, did a human review
    the changed pages? It is the question Chapter 7a's C4 asks, and
    the one IR benchmarks do not directly help with.

Evaluation tells you *how* good. Gating tells you *whether* to ship.
The two complement each other: a KB that publishes without gates will
eventually fail evaluation because malformed pages accumulate; a KB
that evaluates without gating produces beautiful numbers against a
snapshot that cannot actually be deployed.

The gate catalogue in this chapter is adapted from the author's
project-knowledge-base toolkit {cite}`fanyamin_pkb_skill`, with one
added column — *enforced by* — that maps every gate to a specific
piece of CI machinery. The prior art in the toolkit leaves
enforcement implicit; making it explicit is this book's contribution.

## What

### Evaluation

For the code-layer retrieval system (Chapter 12), the useful metrics
are the standard IR ones against a held-out test set of
question/citation pairs: nDCG@10, recall@10, MRR. For the prose-layer
retrieval, these metrics apply with a caveat: the ground truth is
harder to label (a single question often has multiple correct
pages), and partial credit matters more. Both surfaces benefit from
the end-to-end answer-faithfulness metrics in RAGAS
{cite}`es2024ragas` and similar frameworks.

A concrete starting set:

| Metric | Layer | What it measures | Benchmark corpus |
|:--|:--|:--|:--|
| nDCG@10 | code | Are the top-10 retrieved entities ranked correctly? | Held-out `(question, code_entities)` pairs |
| Recall@10 | code | Did we at least find the right entities? | Same |
| Answer faithfulness (RAGAS) | prose+code | Does the generated answer cite its own context? | RAGAS pipeline on sample Q&A |
| Citation resolve-rate | prose+code | Do the `file:line` anchors in generated answers resolve at HEAD? | Every generated answer |
| BEIR-style domain scores | prose | How does retrieval quality compare against public IR corpora? | BEIR {cite}`thakur2021beir` |

Evaluation numbers should be tracked over time on a fixed benchmark
set; a single nDCG@10 = 0.74 is not a claim, but a move from 0.74 to
0.71 after a sync is.

### Gates

Gates are the *build-engineering* question. Every gate is a
mechanical check that runs on CI and returns pass or fail. The
catalogue distinguishes **hard** gates (block publish; non-zero exit)
from **soft** gates (warn; allow publish but flag the reviewer).

#### Hard gates — block publish

| # | Name | What it checks | Enforced by |
|:-:|:--|:--|:--|
| H1 | Footer present | Every content page has a well-formed `PKB-metadata` footer | `check_frontmatter.py` extension |
| H2 | Footer fields valid | `review_status` ∈ {`pending`, `approved`}; `updated_by` ∈ {`human`, `ai`, `ai+human`}; `review_score` ∈ [0,5] | Same |
| H3 | AI-approval consistency | No page has `review_status: approved` with empty `reviewed_by` | Same |
| H4 | Citations resolve | Every `file:line` anchor in every page points at an existing line at HEAD | `verify` step (Chapter 7) |
| H5 | Links resolve | Every internal `](*.md#*)` link points at an existing anchor | `verify` step |
| H6 | Excerpts provenance | Every vendored excerpt's `content_sha256` matches the current file | `refresh_excerpts.py --check` |
| H7 | No `[TODO]` / `[FIXME]` in published pages | Pages with `status: published` contain no unresolved markers | grep-style check |

Each hard gate corresponds to one specific thing that can be false
about the KB and should block the deploy. H1–H3 enforce C2 (footer is
observable and honest). H4–H6 enforce that citations and excerpts
remain trustworthy. H7 catches the most common "we forgot" failure.

#### Soft gates — warn but allow

| # | Name | What it warns about | Enforced by |
|:-:|:--|:--|:--|
| S1 | Stale footers | Any page's footer `commit:` is more than N commits behind HEAD | `check-staleness.py` |
| S2 | Low review score | Any published page has `review_score` < 2 | Footer scan |
| S3 | Imbalanced Diátaxis | The published KB has no how-to pages (or no tutorial, etc.) | Histogram over `doc_type` |
| S4 | Answer-faithfulness regression | Nightly RAGAS-style scores fell > 5% from last build | CI job |
| S5 | Coverage gap | A 10-page set (C1) page is missing | `required_pages.txt` check |

Soft gates are honest warnings, not release blockers. A KB with an
S3 warning is still a KB; it just has a reviewer-visible reminder
that it is drifting away from its own page-set commitments.

## How

### The gate runner

The gate system is a single CI script that runs every check and
aggregates results. A minimal implementation:

```text
function run_gates():
    hard_failures := []
    soft_failures := []

    for gate in HARD_GATES:
        result = gate.check()
        if not result.ok:
            hard_failures.append((gate.name, result.detail))

    for gate in SOFT_GATES:
        result = gate.check()
        if not result.ok:
            soft_failures.append((gate.name, result.detail))

    emit_report(hard_failures, soft_failures)

    if hard_failures:
        exit 1        # block publish
    exit 0            # allow publish; soft warnings in the report
```

Every gate exposes the same interface: a `check()` method that
returns `(ok, detail)` and a stable `name`. This lets the CI script
stay short — it is the gates themselves that hold the domain
knowledge — and lets every gate be tested in isolation.

### The gate report

The output of a gate run is a two-section report: hard failures (if
any) followed by soft warnings. The report is Markdown, committed to
the build artefacts, and linked from the PR that triggered the build:

```markdown
## Hard gates

❌ H4 Citations resolve — 2 failure(s)
   content/architecture.md:47 cites internal/worker/pool.go:142
     → line 142 does not exist at commit 9f8e7d6c (file has 120 lines)
   content/data-and-api.md:23 cites cmd/sync/main.go:58
     → file does not exist at commit 9f8e7d6c

## Soft warnings

⚠ S1 Stale footers — 7 page(s)
   content/observability.md  (footer commit a1b2c3d is 42 commits behind HEAD)
   ...
⚠ S3 Imbalanced Diátaxis
   Published KB has 0 tutorials; the page-set commitment (C1) requires
   at least 1.
```

Hard-failure exit codes block the CI publish step; soft warnings are
appended to the PR as a comment so the reviewer sees them without
CI going red.

### A worked failure

Suppose a PR adds a new function to `internal/worker/pool.go` — good
faith addition, no rename, no break. The author also edits
`architecture.md` to mention the new function and, while there, adds
a `<!-- TODO: add diagram -->` marker intending to come back later.

Run the gates:

- **H1 Footer present.** Pass. `architecture.md` has a footer.
- **H2 Footer fields valid.** Pass. Fields are well-formed.
- **H3 AI-approval consistency.** Pass. The author set `updated_by:
  human`, `review_status: pending`, `review_score: 0`,
  `reviewed_by:`. Everything consistent.
- **H4 Citations resolve.** Pass. The new function's `file:line`
  resolves.
- **H5 Links resolve.** Pass.
- **H6 Excerpts provenance.** Pass.
- **H7 No `[TODO]` in published pages.** **FAIL.** The `<!-- TODO -->`
  marker is in a page with `status: published`.

The gate blocks publish. The reviewer sees a single-line failure and
a pointer to line 47 of the diff. Cost of the check: a grep across
`content/**/*.md` that finished in 30 ms. Cost of having skipped the
check: a production KB that publishes a page whose diagram says
"TODO", which a user sees and loses a small amount of trust over.
That trust does not come back for free.

## Example

A full gate run from a real Friday-afternoon PR (numbers anonymised):

```text
$ python build_kb_gates.py
Running 7 hard gates and 5 soft gates across 137 pages...

Hard gates:
  H1 Footer present              137/137 pass
  H2 Footer fields valid         137/137 pass
  H3 AI-approval consistency     136/137 pass — 1 FAIL
       content/runbook.md: review_status=approved but reviewed_by=''
  H4 Citations resolve           423/425 pass — 2 FAIL
       content/architecture.md:47  internal/worker/pool.go:142  (line missing)
       content/data-and-api.md:23  cmd/sync/main.go:58          (file missing)
  H5 Links resolve               612/612 pass
  H6 Excerpts provenance         18/18  pass
  H7 No [TODO] in published      137/137 pass

Soft gates:
  S1 Stale footers               7 page(s) > 30 commits behind HEAD
  S2 Low review score            0 page(s)
  S3 Imbalanced Diátaxis         WARN — published KB has 0 tutorials
  S4 Answer-faithfulness         pass — 0.81 (prev 0.82; delta −0.01)
  S5 Coverage gap                pass — all 10 required pages present

Hard failures: 3   Soft warnings: 2
FAIL — publish blocked. See report above.
```

The author sees three specific things to fix, not a 400-file review
queue. Fixing them takes perhaps ten minutes: one page's
`reviewed_by` field gets filled in, one citation gets updated to the
new line number, one broken `file:line` gets repointed to the file
that replaced `cmd/sync/main.go`. Re-run the gates: all pass.
Publish proceeds.

## Conclusion

Evaluation (IR metrics, faithfulness scores) tells you whether the KB
is useful once published. Gating (hard and soft checks) tells you
whether this specific build is publishable at all. Both are
mechanical. Both are cheap. Both are refused by most KBs today,
because adding them requires committing to the four corners of
Chapter 7a — if the footer is not there, H1 cannot run; if the
operational model does not resolve citations, H4 cannot run.

The next chapter closes the loop: when a hard gate fails or a soft
gate warns, *what does the fix look like?* The answer is the
three-level update strategy (C3), the actual mechanics of which have
been previewed here but belong to Chapter 16.

## References

```{bibliography}
:filter: keywords % "operations" or keywords % "ir-rag" or keywords % "evaluation" or keywords % "self-citation"
```
