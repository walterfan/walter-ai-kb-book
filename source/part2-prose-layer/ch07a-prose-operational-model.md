---
title: "Chapter 7a — The Prose-Layer Operational Model"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - prose-layer
  - operational-model
  - review
  - drift
  - gates
---

# Chapter 7a — The Prose-Layer Operational Model

This chapter at a glance — the four corners that together let a KB
answer *"is the prose correct, at this commit, and does anyone
know?"*, the single worked scenario that traces an API change
through all four, and an honest list of what the model does *not*
claim to solve:

```{mermaid}
mindmap
  root((4 corners))
    C1 Page set
      Small, stable, opinionated
      Shape readers remember
      Shape tools target
    C2 Footer
      last_updated, commit
      updated_by (human, ai, ai+human)
      review_status (pending, approved)
      review_score (0-5)
      reviewed_by
    C3 Three levels
      L1 Mechanical (script, 0 tokens)
      L2 Bounded-LLM (~1-5 k tokens)
      L3 Human-led (variable)
      Rule first, LLM second
      AI always pending
    C4 Gates
      Hard gates (block publish)
      Soft gates (warn only)
      Footer well-formed
      file:line resolves
      No TODO markers
    Not solved here
      Correctness (gates check form, not truth)
      Reader prioritisation
      Cross-page conflicts
      Semantic equivalence between prose and code
```

An LLM just rewrote 412 pages of your KB. They all build, all have
well-formed frontmatter, all render without a single broken link.
On Friday afternoon your manager sends a message — three lines —
asking a single question: *can we trust them now?*

You read the first three pages. They look fine. You open a fourth.
It describes a workflow that was retired six weeks ago. The fifth
uses a function name that was renamed in the same PR that triggered
the regeneration. The sixth is perfect. You have 406 pages left and
roughly 90 minutes before the 17:00 standup. Which ones does a
human need to read before Monday morning, and how do you tell your
manager *"we don't know yet"* in a way that sounds like competence
and not helplessness?

Chapters 4–7 got the prose in. This chapter is about the thing that
happens the first Monday after the honeymoon ends: a KB whose
contents are **cheap to generate** and **expensive to trust**. The
four-corner model below is what lets you answer your manager's
question in three lines — and, more importantly, lets you answer it
honestly.

## Why

Chapters 4–7 have been about *getting prose in*: a file-based wiki, a
frontmatter-plus-footer contract, a classification pipeline, a built
site with search. Everything in those four chapters is a one-way
pipeline — something arrives, something is produced, and the chapter
ends.

A real knowledge base does not end there. The code underneath the
prose changes every day. A function the architecture page describes
gets renamed. A workflow the runbook describes gains a new step. A
public API the reference page claims returns JSON now also emits
Server-Sent Events. None of this is news to anyone who has maintained
documentation. What is news, now that LLMs can rewrite pages for
pennies, is that the constraint has shifted. The question is no longer
*"is it cheap enough to update the docs?"* — it almost always is. The
question is *"did a human sign off on the update, and if so, which
human, and when?"* The bottleneck is not embedding cost or LLM cost;
at `text-embedding-3-small`'s 2024 prices, a full re-embed of a
100-kLOC repo is under a dollar {cite}`openai_embeddings_v3`. The
bottleneck is **human attention**. A KB that burns that attention with
a 400-file pull request every week ends up trusted by no one — not
because it is wrong, but because nobody has the time to confirm it is
right.

This chapter introduces the operational model the rest of the book
relies on. It is an instantiation of discipline the author has refined
in a private project-knowledge-base toolkit
{cite}`fanyamin_pkb_skill`; this chapter names and explains the
structure, and Chapters 14–16 unpack each piece in operational detail.
The model has exactly four corners. Every later claim about how the
prose layer stays correct reduces to one of them.

## What

The model is a set of four corners. Together they answer *"is the
prose correct, at the current commit, and does anyone know?"* Each
corner has a short label (C1–C4) that other chapters use to refer to
it without re-stating the model:

- **C1 — Opinionated page set.** *Which pages should a KB have?*
- **C2 — Metadata footer.** *Is this specific page still trusted?*
- **C3 — Three-level update strategy.** *Who pays to keep it correct?*
- **C4 — Verification gates.** *What must be true before we publish?*

### C1 — Opinionated page set

A KB that ships with free-form directories quickly grows a folder
called `misc/` that no one searches. A KB that commits to a small,
fixed set of pages gives readers a shape to remember and tools a
shape to target. Chapter 3's *One opinionated instantiation* section
proposed ten pages (`overview`, `quick-start`, `architecture`,
`repo-map`, `data-and-api`, `workflows`, `conventions`, `testing`,
`runbook`, `observability`). C1 is that list, elevated to a corner of
the operational model. The substance lives in Chapter 3; the rule
lives here. **Having *some* stable page set is more important than
arguing about which set.**

### C2 — Metadata footer

Every content page ends with an HTML-comment footer with six fields,
introduced in Chapter 5:

```markdown
<!-- PKB-metadata
last_updated: 2026-04-14
commit: 4a1c92b
updated_by: ai            # human | ai | ai+human
review_status: pending    # pending | approved
review_score: 0           # 0-5
reviewed_by:              # empty until a human reviews
-->
```

C2's purpose is making staleness **observable**. Without the footer, a
KB can only answer "is this page stale?" by re-reading the body and
asking a human — which is expensive, slow, and exactly the thing the
KB was supposed to eliminate. With the footer, a script can check
`commit:` against `git rev-parse --short HEAD`, a reviewer can filter
every page with `review_status: pending`, and an LLM agent (Chapter
21) can refuse to cite a page whose `review_score` is below a
threshold. The full schema is in Chapter 5; C4 makes the footer's
presence a build gate; C3 specifies who is allowed to set which
values.

### C3 — Three-level update strategy

When something changes, *who* — or *what* — updates the docs? Naive
approaches collapse to two: "a human writes the update" (too slow,
almost never done) or "an LLM regenerates everything" (too noisy,
floods review). Neither works. The author's skill
{cite}`fanyamin_pkb_skill` splits updates into three levels, by the
cost and the actor each level requires:

| Level | Trigger | Actor | Token cost | Typical example |
|------:|---------|-------|-----------:|-----------------|
| **L1** Mechanical | File renamed; link broken; commit SHA drifted; repo-map files added or removed | Script (no LLM) | **0** | Re-stamp `commit:` in the footer; fix broken `]()` link; regenerate `repo-map.md` from `git ls-files` |
| **L2** Bounded-LLM | Content drifted *but* the drift is localised to one page's diff | LLM with narrow context: one page + its diff + its footer | ~1–5 k tokens | Function signature changed; regenerate the one paragraph of `data-and-api.md` that referenced it |
| **L3** Human-led | Architectural change, new ADR, cross-cutting refactor, security-sensitive content | Human writes; LLM copy-edits | Variable; human-bounded | Rewrite `architecture.md` after splitting one service into two |

Two rules make the levels safe:

1.  **Rule first, LLM second.** Every change starts at L1. If L1 can
    handle it, no tokens are spent. Only changes that L1 cannot
    resolve fall through to L2; only changes too structural for L2
    fall through to L3.
2.  **AI always sets pending.** When any automated path (L1 or L2)
    modifies a page, `review_status` goes to `pending`,
    `review_score` goes to `0`, and `reviewed_by` is cleared. Only a
    human — L3 or a later review — sets `approved` or a non-zero
    score. The rule is stated in Chapter 5 and enforced in Chapter 15.

Chapter 16 gives the full treatment, including a decision tree for
routing changes through the three levels and a worked cost comparison
against the naive "re-embed everything" baseline.

### C4 — Verification gates

A gate that no one enforces is not a gate. C4 says: every claim the
operational model makes — *"the footer is present", "its fields are
valid", "every file-line reference resolves at the current commit",
"no raw `[TODO]` markers remain"* — is a mechanical check that runs
on CI, either as a hard gate (blocks publish) or a soft gate (warns
without blocking). The full catalogue is in Chapter 15.

The gate system is what makes C2 and C3 real. Without gates, the
footer is a suggestion; with gates, it is a contract. Without gates,
the "AI always sets pending" rule is a hope; with gates, any page
whose `review_status: approved` lacks a matching human `reviewed_by`
fails the build.

### Why exactly four corners?

A reader who has come this far has a fair question: *why four, and
why these four?* "Because experience taught me so" is the honest
answer but not a satisfying one. The structural answer is that the
four corners are the four phases of the Plan–Do–Check–Act cycle
{cite}`deming1986outofcrisis` specialised to a prose-layer
artefact. Each corner answers one phase; drop any one and the
cycle breaks.

| PDCA phase | Question it answers | The corner that answers it | If the corner is missing |
|------------|---------------------|----------------------------|--------------------------|
| **Plan** — what should exist? | *Which pages should a KB have?* | **C1** Opinionated page set | Free-form folders; a `misc/` directory that metastasises. |
| **Do** — how does it get updated? | *Who — or what — performs the update, at what cost?* | **C3** Three-level update strategy | Every change goes through an LLM or none do; cost is unbounded or the KB goes stale. |
| **Check** — is the update acceptable? | *What must be true before we publish the update?* | **C4** Verification gates | Rules that are "policy" but not enforced, i.e. eventually ignored. |
| **Act** — what did we learn about this page? | *Is this specific page still trusted, right now, by whom, and how much?* | **C2** Metadata footer | Staleness is invisible; review state lives in an engineer's memory. |

Three observations follow from this mapping.

**The model is structurally complete, not contingently so.** Any
operational discipline built around "the docs must stay correct
as the code changes" needs exactly one answer to each phase.
Two-corner systems (just *Plan + Do*: "we have a template, we
write updates") are the default industry shape and the default
failure shape — without *Check* the template silently rots, and
without *Act* the KB cannot tell itself from its own exhaust.
Three-corner systems (*Plan + Do + Check*: template + process +
CI) are where most mature teams land; they remain brittle because
*Act*, the per-page memory, is not mechanised. Adding C2 — a
footer a human can read and a script can filter — is the last
corner, and it is the cheapest.

**The corners are independent and load-bearing.** They are
independent because each answers a different PDCA phase, and no
corner's mechanics substitute for another's: a rich footer (C2)
does not tell you what should exist (C1); a strict gate (C4) does
not tell you who pays to update (C3). And they are load-bearing
because, like the four legs of a stool, removing any one collapses
the structure. A KB with opinionated pages, footers, and gates but
no update strategy (no C3) works until the first code change and
then fills with `pending` pages no one has the budget to fix. A KB
with all three mechanics but no opinionated shape (no C1) cannot
tell a reader *where* to look, so neither C2, C3, nor C4 gets
exercised often enough to stay honest.

**The correspondence also explains the *order* the rest of Part IV
unpacks them.** Chapter 14 walks change detection, which is a
*Do* operation (C3) triggered by an *Act* observation (C2 footer
SHA diff). Chapter 15 makes gates real (C4). Chapter 16 wires the
three update levels (C3 proper). The book builds the cycle
Do → Check → Act → back-to-Plan because that is the sequence the
cycle actually runs at operational time; the *Plan* corner (C1)
is the boundary condition rather than a recurring step.

The mapping is not a formal proof of minimality — PDCA itself is
a heuristic, not a theorem. But it gives the four corners a shape
the reader can reason about and, more importantly, a shape the
reader can *reject*: if a team finds a fifth corner their KB
actually needs, the productive response is not to squeeze it into
one of C1–C4 but to extend the cycle. The model is a floor, not a
ceiling.

## How

The four corners connect through a single worked scenario. Suppose a
public API route changes in the codebase — the endpoint
`/api/v1/pages` gains a new query parameter. Here is what happens, in
order:

1.  **Change detection (Chapter 14 via C2).** A nightly job diffs
    `git HEAD` against the set of `commit:` values in every footer. It
    finds that `data-and-api.md` and `api-reference.md` both list the
    old commit, and that the diff touches code the `api-reference.md`
    page cites by `file:line`. Two candidate pages.
2.  **L1 dispatch (C3).** The job runs L1 checks on both candidates.
    For `data-and-api.md` the only drift is the footer SHA — the body
    still describes the route correctly. L1 re-stamps the footer:
    `commit:` bumps, `last_updated:` bumps, `updated_by: ai`,
    `review_status: pending` (the AI-always-sets-pending rule),
    `review_score: 0`. Zero tokens spent. For `api-reference.md` the
    drift is real — a paragraph references the old parameter list. L1
    cannot fix that; it escalates.
3.  **L2 dispatch (C3).** An LLM is invoked with narrow context: the
    current `api-reference.md` body (~2 kB), the relevant code diff
    (~300 B), and the page's footer. It returns a new version of the
    one affected paragraph. The footer is re-stamped by the same rule:
    `review_status: pending`, `reviewed_by:` cleared. Cost: ~2.3 k
    tokens — under a cent.
4.  **Gate run (C4).** Before publish, hard gates fire. The footer is
    present on both pages and well-formed: pass. Every `file:line`
    reference in `api-reference.md` resolves at the current commit
    (including the new parameter, which L2 just referenced): pass.
    No `[TODO]` markers were introduced: pass. Mermaid is unchanged
    and still parses: pass. Publish proceeds.
5.  **Human review (C3 L3 → C2).** A reviewer sees two pages with
    `review_status: pending` in the KB's review dashboard, reads the
    two diffs (not 400 files — just two), approves both, and sets
    `review_score: 4` on each. The next L1 check against either page
    will leave `review_status` at `approved` because no body change
    has occurred.

Nothing in that sequence is an experiment. Every step is a script or a
rule that exists because one of the four corners puts it there.
Change detection works because C2 made staleness observable. Routing
works because C3 gave the levels a stable meaning. Publish only
happens because C4 refused to let a malformed page through. And the
next human who reads the docs can look at either page's footer and
know, without asking anyone, that an LLM touched it and a named human
has signed off.

## Example

Here is the minimal viable shape of the loop, told through one page's
footer over a week:

```text
Monday  08:00  commit: a1b2c3d4  updated_by: human  review_status: approved   reviewed_by: alice
                 (page written by Alice; nothing else changes all week)

Monday  08:15  commit: a1b2c3d4  updated_by: human  review_status: approved   reviewed_by: alice
                 (L1 runs against HEAD; commit still matches; no change)

Wednesday 14:30  commit: 4a1c92b  updated_by: ai    review_status: pending    reviewed_by:
                 (API changed; L2 regenerated one paragraph; footer reset)

Thursday 10:05  commit: 4a1c92b  updated_by: ai+human  review_status: approved  review_score: 4  reviewed_by: alice
                 (Alice read the L2 diff and approved)

Friday  23:00  commit: 9f8e7d6c  updated_by: human  review_status: pending   reviewed_by:
                 (an unrelated refactor moved a linked file; L1 fixed the broken link;
                  review resets because the body was touched)
```

Five states, one page, a full audit trail in its own footer. No side
tables, no CI database, no review spreadsheet. A human reading the
file in `cat` or `vim` learns the entire history. A script querying
the KB gets a closed vocabulary (`approved | pending`, `human | ai |
ai+human`, `0–5`) it can filter on with zero ambiguity.

The full L1/L2/L3 dispatcher, the change-detection layers that decide
which pages are candidates, and the complete gate catalogue are the
subjects of the next three chapters.

## What this model does *not* solve

The four corners make a KB's claims about its own correctness
auditable. They do not, on their own, make the claims *true*. This
distinction matters enough to state explicitly, because teams that
treat the operational model as the whole job — rather than as the
scaffolding for the job — drift into a specific and avoidable
failure mode: a KB whose every page's footer says `approved` and
whose content is still wrong.

Four limits are worth naming.

1.  **Gates check *form*, not *truth*.** The verification gates in
    C4 can mechanically confirm that the footer is present, that
    `file:line` references resolve at the current commit, and that
    no `[TODO]` markers remain. They cannot confirm that the
    paragraph *next to* a `file:line` anchor is a correct
    description of the function it points at. That check requires
    either a human reading the page or an LLM cross-reading the
    code — which is exactly what the three-level update strategy
    (C3) dispatches, but the dispatcher itself can no more verify
    semantic truth than the compiler can verify that a function
    does what its name claims.

2.  **`approved` means "a human read this diff", not "this is
    correct".** The AI-always-sets-pending rule ensures that an
    `approved` page was signed off by a named human, and the gate
    catalogue ensures the human was looking at the current commit.
    Neither mechanism prevents a reviewer from approving a
    subtly-wrong L2 rewrite — because the reviewer was rushed, or
    because the wrongness is in a corner of the domain the reviewer
    does not know. The model makes review *traceable*, not
    *infallible*. Chapter 15 adds a second-reviewer rule for
    security-sensitive pages; lower-stakes pages stay on the
    single-reviewer path, with the audit trail as the compensating
    control.

3.  **The model does not prioritise reader attention.** A KB with
    10 000 pages whose footers are all `approved` still forces the
    reader to decide which page to read first. Ranking, curation,
    deprecation, and the Diátaxis structure (Chapter 3) are what
    make a KB *usable*; the operational model makes it
    *trustworthy*. These are independent properties, and either
    alone is insufficient. A book's index is not a table of
    contents.

4.  **Cross-page conflicts are out of scope.** If
    `architecture.md` and `runbook.md` describe the same system and
    disagree with each other, both can sit in the KB with
    `review_status: approved` and `verification_status: supported`.
    Detecting the disagreement requires comparing pages to each
    other, which the four-corner model does not do. Chapter 18's
    document-layering tuple and Chapter 21's agent-accessible KB
    together begin to address this — an agent reading both pages can
    *notice* the conflict — but the prose-layer operational model
    alone cannot. A KB with contradictory pages is a KB whose
    operational model is working; it is the *editorial* model that
    has to catch the contradiction.

The healthy way to hold the four corners is: they are the
discipline a KB needs to stop lying *about itself*. Whether it also
says true things about the software it describes is a separate,
larger question — and, because that question cannot be answered
mechanically, the scaffolding that makes human attention
accountable is the thing that, over time, answers it for you.

## Part II in one page — a pointer checklist

Across the five chapters, Part II has catalogued roughly two dozen
failure modes, misconceptions, and wiring mistakes. For the reader
who returns to the book *after* deploying a KB and is now trying to
diagnose a specific symptom, the table below is a single-page
index into the discussion — organised by the symptom a team
actually observes, not by the chapter it lives in.

### Storage and repository hygiene (Chapter 4)

| Symptom you see | Root cause | One-line remedy | Pointer |
|-----------------|------------|-----------------|---------|
| Clones getting slower each month | Binary blobs committed into `content/` | CI hard-limit on file size + Git LFS for the few legitimate binaries | ch04 §"Common mistakes" #1 |
| External links from code to wiki pages break after a rename | Slug rename with no redirect map | Check in a `redirects.yaml`; CI refuses PRs that break a still-referenced URL | ch04 §"Common mistakes" #2 |
| Merge conflicts that the PR UI cannot display usefully | Two authors rewrote the same file in parallel | Treat high-churn pages as *owned*; for live-incident docs, use a shared doc, import afterwards | ch04 §"Common mistakes" #3 |
| Per-reader history / autosaves / comments bloating the repo | Over-extending "everything is a file" to mutable operational state | Mutable state lives in a side database; files are for content | ch04 §"Common mistakes" #4 |
| Docs still drifting from code despite PR discipline | Review runs on different communication lines than code review | Docs-as-code realigns the two via Conway's law / Parnas co-location | ch04 §"Why docs-as-code really works" |

### Provenance and trust (Chapter 5)

| Symptom you see | Root cause | One-line remedy | Pointer |
|-----------------|------------|-----------------|---------|
| An old audit trail silently lost its authorship | `created_by` was treated as mutable in a bulk migration | `created`, `created_by`, `source` are frozen; only correct via explicit PR | ch05 §"Common mistakes" #1 |
| `git log` of `content/` is dominated by review-state flips | Review state lives in frontmatter instead of its own block | Split into frontmatter (lineage) + footer (review state) | ch05 §"Common mistakes" #2 |
| Production KB now has `approved` pages a human never saw | No hard gate on `approved` + `reviewed_by` | CI gate rejects `approved` without a matching human `reviewed_by` | ch05 §"Common mistakes" #3 |
| `doc_type` vocabulary has drifted to a long messy list | No enum closure in the validator | `doc_type` is a *closed* enumeration; reject unknown values at validation time | ch05 §"Common mistakes" #4 |
| Pages marked `supported` for a commit that was rewritten twice | `verification_status` was not re-evaluated against `commit` | Staleness detector demotes when footer `commit` no longer matches the code it references | ch05 §"Common mistakes" #5 |
| `source.uri` points at a 404 or a silently reworded URL | `source` has no `ref` | Every `source.uri` must carry a `ref`: commit SHA, Wayback snapshot, content hash | ch05 §"Common mistakes" #6 |

### Classification pipeline (Chapter 6)

| Symptom you see | Root cause | One-line remedy | Pointer |
|-----------------|------------|-----------------|---------|
| Imported page filed as `security-architecture` with `supported` trust | Prompt injection via imported content | Bound the classifier input; mark untrusted content explicitly; `verification_status` is out of the LLM's output schema | ch06 §"LLM failure modes" #1 |
| New, made-up category appeared in `content/` | Hallucinated label (closed enum not enforced) | Caller rejects out-of-enum labels; fall back to heuristic classifier | ch06 §"LLM failure modes" #2 |
| Gradual shift in category distribution over months | Silent model upgrade or corpus drift | Check a ~50-page gold set into the repo; nightly CI diffs the labels | ch06 §"LLM failure modes" #3 |
| Half the weekend's ingest silently went through the heuristic | JSON-mode parse failures were logged but not metricised | Use structured-output API; treat parse failures as a first-class metric | ch06 §"LLM failure modes" #4 |
| Ingest batch cost exploded overnight | Provider pricing / throttling change | Hard budget per batch: max tokens, max wall-clock, abort and commit partial | ch06 §"LLM failure modes" #5 |
| Imported page's images 404 a year later | Importer did not rewrite asset URLs | The *ingest path* (one function) owns URL rewriting; every importer flows through it | ch06 §"LLM failure modes" #6 |
| Team treats Diátaxis labels as ground truth | Classification *is* a lossy projection | Record classifier uncertainty; route low-confidence to human review; treat `unreviewed` as the honest default | ch06 §"A note on what classification *is*" |

### Search and publishing (Chapter 7)

| Symptom you see | Root cause | One-line remedy | Pointer |
|-----------------|------------|-----------------|---------|
| User searches for `throttle incoming traffic`, gets nothing | Vocabulary mismatch with identifier-literal | Richer frontmatter `tags:` now; dense retrieval when it stops working | ch07 §"Where the tiny search engine fails" #1 |
| `配置文件` query returns nothing on CJK corpus | No segmentation; `unicode.IsLetter` does not split | Swap `tokenize` for a CJK segmenter (`go-jieba`, `kagome`) | ch07 §"Where the tiny search engine fails" #2 |
| `recieve` returns nothing, users annoyed | No typo tolerance | Fuzzy matching in-process up to ~100k terms; Meilisearch above that | ch07 §"Where the tiny search engine fails" #3 |
| Long-but-irrelevant pages outrank focused ones | Score is term-cardinality, no length normalisation | Field weighting on `title`; escalate to BM25 when the pattern persists | ch07 §"Where the tiny search engine fails" #4 |
| Incremental index is stale yet debugging is hard | Incremental update is the failure mode of most DB-backed wikis | Whole-map rebuild on write; milliseconds at this scale | ch07 §"Common mistakes in wiring up search" #1 |
| Live server and static site return different results | Two search layers running in parallel | Staircase is a *sequence* — pick one layer, keep one interface | ch07 §"Common mistakes in wiring up search" #2 |
| `contradicted` pages surface in default search | Trust fields are not retrieval metadata yet | Filter by `verification_status` at query time; explicit "include superseded" toggle | ch07 §"Common mistakes in wiring up search" #3 |
| Org relies on Sphinx client-side search for authenticated users | Static search is blind to frontmatter / trust fields | Server search is authoritative; static search is for public / offline | ch07 §"Common mistakes in wiring up search" #4 |

### Operational model (Chapter 7a)

| Symptom you see | Root cause | One-line remedy | Pointer |
|-----------------|------------|-----------------|---------|
| Every page `approved`, content still wrong | Gates check form, not truth | `approved` means *a human read the diff*, not *this is correct*; add second-reviewer rule for security-sensitive pages | ch07a §"What this model does *not* solve" #1, #2 |
| 10k `approved` pages, user still can't find the right one | Model makes KB trustworthy, not *usable* | Prioritisation is Diátaxis + curation, independent of trust | ch07a §"What this model does *not* solve" #3 |
| `architecture.md` and `runbook.md` disagree, both approved | Four-corner model is per-page, not cross-page | Cross-page conflict detection is out of scope for Part II; ch18 + ch21 begin to address it | ch07a §"What this model does *not* solve" #4 |

The common thread across the whole table: *every one of these
failures has a cheap mechanical fix **and** an expensive
"re-architecture" fix, and teams consistently try the expensive one
first.* The operational model is the habit of spending one hour on
the cheap fix before spending a week on the expensive one.

## Conclusion

Part II's four corners (page set, metadata footer, three-level updates,
verification gates) are the prose-layer analogue of Part III's four
corners (parsing, embeddings, graph, prompt). Each layer has a stable
*structure* the book returns to; each layer has a stable *set of
mechanisms* that make that structure real. The rest of Part IV is how
you wire the prose-layer mechanisms together; Part V is how the two
layers talk to each other.

The four corners do not themselves claim to produce correct docs. They
claim only that a KB which implements them can *answer honestly* about
its own correctness — including, when required, the answer *"we don't
know; this page hasn't been reviewed."* That answer is the foundation
on which Chapter 18 builds the document-layering tuple and Chapter 21
builds the agent-callable surface.

## References

```{bibliography}
:filter: keywords % "prose-layer" or keywords % "operational-model" or keywords % "self-citation" or keywords % "foundations"
```
