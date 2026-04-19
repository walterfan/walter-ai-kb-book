---
title: 'Chapter 16 — Maintenance, Drift and Link Rot'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - operations
  - drift
---

# Chapter 16 — Maintenance, Drift and Link Rot

## Why

Chapter 14 tells you which pages changed. Chapter 15 tells you which
ones cannot be published as-is. This chapter tells you what to
actually *do* about each one. In the terms of Chapter 7a, this is
Corner C3 — the three-level update strategy — written out
operationally.

The LLM era has changed the economics of maintenance, but not in the
direction people expected. Re-embedding a repo is nearly free
{cite}`openai_embeddings_v3`. Regenerating a whole page with a modern
LLM is pennies. Neither of those is the bottleneck any more. The
bottleneck is *a human understanding what changed*. If the pipeline
regenerates 400 pages in a week, a reviewer either becomes a rubber
stamp (defeating the purpose) or stops reviewing (defeating the KB).

The three-level strategy is the author's answer to this, refined in a
private project-knowledge-base toolkit {cite}`fanyamin_pkb_skill` and
presented here as the book's canonical discipline. It has one rule
that matters more than the levels: **rule first, LLM second.** If a
deterministic rule can do the job, do not call an LLM. Every call is
a page a human may need to read.

Link rot {cite}`kiesling2017linkrot` is the most common symptom of
maintenance debt and the cleanest illustration of the three levels.
This chapter uses it as a running example.

## What

### The three levels

Every candidate page produced by Chapter 14's sync is routed to
exactly one of three levels by a dispatcher whose rules are
deterministic. The levels differ by who pays and what they spend:

| Level | Who acts | Token cost | When it applies | What the reviewer sees |
|:--|:--|:--|:--|:--|
| **L1 Mechanical** | A script | **0** | Change is resolvable by rule: footer-only drift, broken link to a moved file, auto-generated page (`repo-map`), stamp refresh | Nothing, usually; the pending marker on the footer |
| **L2 Bounded-LLM** | An LLM + small context | 1–5 k tokens | Body references something that genuinely changed; the fix is localised to a paragraph or two | A small diff; a `pending` footer asking for approval |
| **L3 Human-led** | A human; LLM copy-edits | Variable | Architectural change, new ADR, security-sensitive content, or L2 repeatedly fails for the same page | A real review; sometimes a new ADR |

The levels are not a menu. A page is assigned a level; it does not
get to pick. The rules below determine assignment.

### The dispatcher rules

```text
function dispatch(candidate):
    tags = candidate.layers_that_caught_it     # from Chapter 14
    path = candidate.path

    # Policy overrides go first.
    if path is in {architecture/, adr/, security/, runbook/}:
        return L3
    if path is in {repo-map.md, api-reference.md}:
        return L1_REGENERATE

    # L1 cases — rules that mechanically finish the job.
    if tags == {L-git} and only_footer_drift(candidate):
        return L1_STAMP
    if tags & {L-link} and link_target_moved_but_still_exists(candidate):
        return L1_FIX_LINK
    if auto_generated_marker in candidate.frontmatter:
        return L1_REGENERATE

    # L2 cases — body actually changed semantics.
    if tags & {L-entity} or tags & {L-link}:
        return L2

    # Fall-through — be conservative.
    return L3
```

Four observations are worth pausing on:

1.  **Policy overrides first.** Architecture pages never get an
    automated rewrite, even if the sync thinks the change is small.
    Auto-generated pages never get an LLM pass, even if the change is
    large (it is *meant* to be mechanical).
2.  **L1 is the first positive match.** The dispatcher actively tries
    to resolve the candidate with a rule before it considers an LLM.
    This is where "rule first, LLM second" becomes real code.
3.  **L2 only fires on evidence.** The tags are the evidence — either
    a moved entity (L-entity) or a broken link (L-link) that survived
    the L1 rules. An L-git-only candidate with no body drift cannot
    reach L2.
4.  **Fall-through is conservative.** When the rules are ambiguous,
    route to a human. The cost of a wrong human review is an
    annoyance; the cost of a wrong LLM rewrite is a silent trust
    regression.

### What each level actually does

**L1 Mechanical** runs pure Python or shell:

- `L1_STAMP` updates `commit:` and `last_updated:` in the footer;
  leaves everything else untouched.
- `L1_FIX_LINK` rewrites one markdown link or `file:line` anchor to
  point at the new location of the target. If the target no longer
  exists at all, escalates to L2.
- `L1_REGENERATE` re-runs the page's generator (e.g. `repo-map.md`
  from `git ls-files`) and overwrites the body. Footer resets per
  the AI-always-sets-pending rule — yes, even though no LLM was
  involved; any automated touch counts.

Every L1 action resets the footer: `review_status: pending`,
`review_score: 0`, `reviewed_by:`, `updated_by: ai` (or `human` if a
human ran the script). The name is a convention, not a claim that a
model was called.

**L2 Bounded-LLM** calls one LLM with a carefully bounded context:

- The *current* body of the one candidate page (~2 kB).
- The *one diff* that triggered the change (~300 B – 2 kB).
- The page's footer, as a reminder of C2's vocabulary.
- A *system prompt* that says: you may edit only the paragraphs that
  cite things in the diff; you may not invent citations; you must
  leave an explicit `pending` footer.

This bounds the token cost at roughly 5 k per call, and — more
importantly — bounds the *scope* of the change. L2 cannot rewrite
the whole page, because the prompt and the context do not contain
the whole page's intent. It can only fix the paragraphs it was
pointed at. Drift confined to one localised area is exactly the case
L2 exists for.

**L3 Human-led** is a human writing or editing, with the LLM used
(at most) for copy-editing passes the human explicitly invokes.
Every L3 change is a real review in the normal git-and-PR sense.
There is no special machinery here — the discipline is that the
other levels *stay out* of L3's territory.

## How

### Link rot as the canonical worked example

Link rot {cite}`kiesling2017linkrot` deserves a dedicated walk-through
because it is the failure most readers have personally seen and
because it exercises all three levels in one scenario.

**Setup.** A repo-level refactor renames `cmd/sync/main.go` to
`cmd/sync-tool/main.go` and simultaneously splits the old `runSync`
function into `runSync` and `runSyncBatch`. Three pages cite the old
path:

- `repo-map.md` — auto-generated; just needs regeneration.
- `runbook.md` — one paragraph says "run `cmd/sync/main.go`"; the
  rest of the page is fine.
- `architecture.md` — two paragraphs explain *why* `runSync` was
  structured the way it was; the split is a structural change.

**Sync (Chapter 14).** L-git and L-link both flag all three pages.
L-entity flags `runbook.md` and `architecture.md` (both cite the
function whose entity ID changed when the file moved and split).

**Dispatcher.**

- `repo-map.md`: path is in `{repo-map.md, api-reference.md}` →
  **L1_REGENERATE.**
- `runbook.md`: path is not in any policy-override set. Tags
  include L-link; is the link target still a file that exists?
  Yes — `cmd/sync-tool/main.go` exists. **L1_FIX_LINK.**
- `architecture.md`: path is in `{architecture/}` →
  **L3** immediately. The dispatcher does not even inspect the tags.

**Execution.**

- L1 regenerates `repo-map.md` from `git ls-files` (zero tokens,
  deterministic).
- L1 rewrites the one link in `runbook.md` from
  `cmd/sync/main.go` to `cmd/sync-tool/main.go` (zero tokens,
  localised edit).
- L3 opens a human-reviewable task: *"`architecture.md` cites
  `runSync`, which has been split. Does the architectural
  explanation in §3 need rewriting, or just a sentence about the new
  `runSyncBatch`? Please review."* A human decides; an ADR may
  follow; the LLM is involved only if the human asks.

**Gate run (Chapter 15).** After L1 and L3 complete, the publish
gates run across all three pages. H4 (citations resolve) and H5
(links resolve) both pass now. H1/H2/H3 (footer shape) pass for L1's
footers because the scripts wrote them correctly; pass for
`architecture.md` because the human remembered to update the footer
along with the body.

**Cost audit.** LLM calls: zero for L1; none for L3 unless the human
invoked one. Human review scope: one page (`architecture.md`), which
is a genuinely structural change and *deserves* human attention.
Compare with the naive baseline ("regenerate every page that
mentions `runSync`"), which would have produced three LLM-generated
diffs for the reviewer to wade through, two of which should never
have been generated.

### Why "rule first" beats "LLM first"

It is tempting, with cheap LLMs, to skip L1 entirely and hand every
candidate to L2. Do not. Three reasons, in decreasing order of
importance:

1.  **Human attention.** Every LLM call produces a diff a human
    reviews. Ten L1 wins a week is ten reviews saved. One hundred is
    100.
2.  **Determinism.** L1 rules have the same answer every time. L2
    does not — the same prompt with the same model at temperature 0
    can produce subtly different prose on different days as models
    are upgraded. For anything a rule can handle, having the rule be
    the source of truth is more stable.
3.  **Privacy.** L1 runs entirely on local filesystem and git. L2
    sends page content, diffs, and prompts to a model provider.
    Chapter 22 unpacks the privacy implications; suffice it to say
    here that a rule-first discipline reduces the surface area of
    things sent to third parties, simply by handling more cases
    before the LLM is consulted.

### When L2 is the right choice

L2 is for the case that genuinely exists between L1 (too mechanical)
and L3 (too structural): a localised content change where an LLM can
do, in a few thousand tokens, what a human would do in ten minutes
but with a higher per-minute cost. Function renames, type-signature
changes, parameter additions, documentation for a straightforwardly
new helper function — these all land cleanly in L2 because a human
reviewer can verify the one-paragraph diff quickly.

L2 is *not* for cross-page consistency (the LLM does not see the
other pages), not for architectural rewrites (not enough context),
and not for new content (there is no "page to patch"). Putting those
cases through L2 produces plausible-looking output that a reviewer
has to correct anyway, so nothing is gained.

## Example

A week of real operation, summarised as a batch report — the kind of
output a Friday-afternoon digest posts to the team's channel:

```text
Incremental sync summary (week of 2026-04-13 → 2026-04-20)
==========================================================

Commits scanned:   47
Candidate pages:   19
Routed to L1:      12 pages   (0 LLM calls, 0 tokens)
Routed to L2:       5 pages   (5 LLM calls, ~18k total tokens, ~$0.02)
Routed to L3:       2 pages   (human review queued)

Gate results (post-update):
  Hard gates:   137/137 pass
  Soft gates:   S1 (stale footers): 0; S3 (Diátaxis balance): pass

Human review queue:
  - architecture.md  — runSync split; needs explanation update
  - adr/0024-rate-limiting.md  — NEW (proposed; reviewer: alice)
```

Two points of interest. First, L1 handled 63% of the week's
candidates for zero cost. Second, the reviewer's queue was two items
— both genuinely requiring human thought — not nineteen. That ratio,
not the token cost, is the metric the operational model actually
optimises for.

## Conclusion

Maintenance is not a single problem; it is three problems pretending
to be one. L1 is a filesystem-and-git problem. L2 is an LLM problem
with bounded context. L3 is a human problem that the machinery should
stay out of. Routing correctly between them — rule first, LLM second,
human for structural change — is what makes a KB sustainable as the
code beneath it accelerates.

Part IV's three chapters have now laid out the whole loop: detect
candidates (ch14), check them against hard and soft gates (ch15),
dispatch them through the three levels (ch16). The next two parts
(V and VI) put this loop to work: Chapter 18 uses the footer's review
state as the fourth axis of document layering, and Chapter 21 asks
what happens when an agent — not a human — consumes the output.

## References

```{bibliography}
:filter: keywords % "operations" or keywords % "drift" or keywords % "self-citation"
```
