---
title: 'Chapter 14 — Incremental Sync'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - operations
  - deepwiki
  - drift
---

# Chapter 14 — Incremental Sync

## Why

Chapter 7a's operational model asks a question C3 cannot answer on its
own: *which pages need updating?* Without a good answer, an
"incremental" sync is a fiction — either the pipeline re-processes
everything on every commit (cheap today, but it produces a 400-file
pull request that no human will review), or it processes nothing and
the KB rots.

Incremental sync is the mechanism that sits between "something
changed" and "some specific pages need attention". It is the interface
that makes C3's three-level update strategy (Chapter 16) affordable,
and the layer C2's metadata footer (Chapter 5) most directly depends
on. Done well, the sync turns a 1,000-commit week into a handful of
reviewable page updates. Done badly, it turns it into noise.

The blog post this book expands {cite}`fanyamin2026deepwiki`
articulates the incremental-sync state machine for the code layer
(Part III) as a Merkle-diff over tree-sitter entity IDs. This chapter
generalises the same pattern to the prose layer and explains how the
two layers share one change-detection substrate.

RepoAgent independently arrives at the same operational conclusion from
the documentation side: repository-level documentation is not useful
unless it ships with a persistent **update loop**, not just a one-shot
generation pass {cite}`luo2024repoagentllmpoweredopensourceframework`.
Where RepoAgent names three modules — global structure analysis,
documentation generation, and documentation update — this chapter makes
the update stage explicit enough to reason about: detect the smallest
safe candidate set first, then let Chapter 16 decide whether the repair
is mechanical, bounded-LLM, or human-led.

## What

An incremental sync answers a single question against a pair of
commits $(c_\text{prev}, c_\text{now})$:

$$
\text{affected pages} = f(\text{diff}(c_\text{prev}, c_\text{now}))
$$

The hard part is $f$. A naive implementation sets $f$ to "every page"
— correct but useless. A too-clever implementation sets $f$ to "only
pages whose body literally mentions a changed filename" — cheap but
unsafe, because a refactor can break a page's `file:line` references
without changing any substring of the page's body.

The operational model uses a three-layer $f$, cheapest first — a
decomposition the author has refined in a private
project-knowledge-base toolkit {cite}`fanyamin_pkb_skill` across
multiple repos. Each layer answers the affected-pages question with
increasing precision and increasing cost; a change that the first
layer resolves never reaches the second.

| Layer | Input | Output | Cost | Catches |
|:--|:--|:--|--:|:--|
| **L-git** | `git diff --name-only $prev..HEAD` | candidate files | O(1) per commit | renames, additions, deletions |
| **L-entity** | code-layer entity IDs that moved (Chapter 11) | pages whose `file:line` citations point at moved code | O(entities × citations) | refactors that preserve filenames |
| **L-link** | every `](...md)` and `file:line` anchor in every page | pages whose outgoing links no longer resolve | O(links) | link rot from any cause |

Only after all three layers have been consulted does the system hand
candidate pages to Chapter 16's L1/L2/L3 dispatcher. The sync does
*not* itself update anything; its job is purely to produce a
reviewable, deduplicated, smallest-safe set of candidate pages.

This separation — detect candidates here, update them there — is why
Chapter 7a's model scales. Detection is cheap and deterministic;
update is expensive and sometimes uses an LLM. Combining them into one
step couples the two cost models and usually picks the worst of both.

## How

### The L-git layer

The cheapest layer. Every page carries a `commit:` field in its
footer (Chapter 5 C2). On every sync, the job computes the set of
files that have changed between any page's `commit:` and `HEAD`:

```text
for each page P in content/**/*.md:
    prev := P.footer.commit
    changed := `git diff --name-only prev..HEAD`
    if changed == []:
        # page is up to date at the commit-SHA level
        continue
    add P to candidates
```

A page whose footer already points at `HEAD` is skipped entirely — no
body read, no LLM invocation. This is the L1-mechanical case in its
purest form: the cost of "this page is fine" is a git command.

The footer's `commit:` field is therefore not decorative. It is the
load-bearing datum L-git keys on. A KB that drops the field (or lets
it fall out of sync because review happens without updating it) loses
L-git and falls back to L-entity and L-link, which are both more
expensive.

### The L-entity layer

L-git only detects *which files* changed. A refactor that renames an
exported function does not rename any file — but it does break every
page that cited the function by name. L-entity catches these by
keying on the code-layer entity IDs defined in Chapter 11.

Every code entity has a stable ID:
`sha256(repoID | filePath | entityType | name | startLine)`. When the
code-layer sync runs (Chapter 11), entities whose IDs changed land in
a `moved_entities` set. L-entity then asks: *which prose pages cite
these entities?* The answer comes from a reverse index built by the
verify step (Chapter 7), which scans every page for `file:line`
anchors and records a `(page, entity_id)` edge.

```text
moved := code_sync.moved_entities(prev, HEAD)
for each entity_id in moved:
    for each page P in reverse_index[entity_id]:
        add P to candidates
```

L-entity is the layer that keeps the *prose layer in sync with the
code layer*. Without it, a function-rename refactor leaves the prose
citing a dead entity, and a retrieval agent (Chapter 21) cheerfully
quotes the dead citation. With it, the page gets flagged, routed
through Chapter 16's L2 bounded-LLM path, and re-cited against the
current code.

### The L-link layer

Catches everything the first two layers miss: a reordered section in
another page that shifts `ch05-frontmatter#foo` anchors; a moved
example file that breaks every `literalinclude` path; a deleted image
in `_static/`. L-link is a brute-force scan — every outgoing link in
every page is tested against the current commit.

```text
for each page P in content/**/*.md:
    for each link L in outgoing_links(P):
        if not resolves_at(HEAD, L):
            add P to candidates
```

L-link can feel expensive, but it is not: the checks are pure
filesystem operations and finish in seconds for a 1,000-page KB. It
runs in full on every sync — there is no incremental shortcut here,
because a link can break due to a change in the *target*, which
L-git and L-entity already knew about, but also because of a change
in the *source* that neither layer saw (e.g. a page edited manually
in `vim`).

### Producing the candidate set

The three layers emit candidate pages with some overlap. The sync
deduplicates and tags each candidate with the layer(s) that caught
it, so Chapter 16's dispatcher can use that tag to choose a level:

| Caught by | Suggested level (Chapter 16) |
|:--|:--|
| L-git only, and only the footer `commit:` drifted | **L1** re-stamp |
| L-git only, and real body-citing files changed | **L2** bounded-LLM |
| L-entity | **L2** bounded-LLM, with the moved-entity ID in context |
| L-link (target moved) | **L1** link fix if possible; else **L2** |
| Any layer + page is in `architecture/` or `adr/` | **L3** human-led |

The last row matters. Architecture pages and ADRs are
security-sensitive prose; the operational model refuses to let an LLM
silently regenerate them regardless of what the earlier layers said.
This is a policy, stated once in the dispatcher's config, not re-
litigated per page.

## Example

A concrete sync against a PR that renames a Go package from
`internal/worker` to `internal/job`:

**Input diff.** 12 files changed. 4 under `internal/worker/` (now
`internal/job/`). 8 callers that imported the old package.

**L-git.** Produces 12 candidate files. Of the pages in the KB,
three have `commit:` values predating the PR: `data-and-api.md`,
`repo-map.md`, `runbook.md`. All three are added to candidates.

**L-entity.** The code-layer sync reports 9 moved entities (the
package's 9 exported symbols kept the same `name` but now live under a
different `filePath`, so their stable ID changed). The reverse index
shows `data-and-api.md` cites 3 of them and `repo-map.md` cites 1.
Both pages were already candidates; L-entity adds nothing new — it
does attach the moved-entity IDs so L2 has them in its context.

**L-link.** Every `internal/worker/...` literal path in the KB is now
broken. `repo-map.md` had 4 such paths; `data-and-api.md` had 2. Both
were already candidates.

**Dispatcher input.** Three candidates, all tagged with the layer(s)
that caught them:

```text
repo-map.md       {L-git, L-entity, L-link}   suggest L1 (regenerate from git ls-files)
data-and-api.md   {L-git, L-entity, L-link}   suggest L2 (body cites moved entities)
runbook.md        {L-git}                     suggest L1 (commit drift only)
```

Chapter 16 takes it from here: L1 regenerates `repo-map.md` from `git
ls-files` in zero tokens; L2 invokes an LLM on `data-and-api.md` with
the moved-entity diff and the existing body; L1 re-stamps
`runbook.md`'s footer. Total cost: one LLM call, ~3 kB of context,
under a cent. Human review scope: one diff (`data-and-api.md`).
Compare with a naive "re-embed everything" baseline that would have
produced diffs across dozens of pages for the reviewer to wade through.

## Conclusion

Incremental sync is the interface between the code layer (Part III)
and the prose layer (Part II). Everything upstream of it is about
*correctness* — "does this entity ID still point at the same thing?",
"does this link resolve?" — and everything downstream is about *cost*
— "is this a free re-stamp, a cheap regeneration, or a human's
problem?" Get the interface right and both halves of the book's model
work. Get it wrong and the cheap layers end up doing expensive work.

The next chapter makes the gates explicit: a page that has been
processed by any update level still has to pass the same hard checks
(footer present, references resolve, no broken Mermaid) before it can
be published. Detection and dispatch are ch14 and ch16; gating is
ch15.

## References

```{bibliography}
:filter: keywords % "operations" or keywords % "deepwiki" or keywords % "drift" or keywords % "self-citation"
```
