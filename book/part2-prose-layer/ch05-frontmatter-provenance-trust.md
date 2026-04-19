---
title: "Chapter 5 — Frontmatter as a Provenance Record"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - prose-layer
  - provenance
  - trust
  - frontmatter
---

# Chapter 5 — Frontmatter as a Provenance Record

This chapter at a glance — the four questions a trust layer must
answer, the two-block split between lineage (frontmatter) and review
state (footer), the cultural commitment that `AI → unreviewed`, and
the failure patterns that collapse even well-schemed provenance into
decoration:

```{mermaid}
mindmap
  root((Provenance & trust))
    Why
      Who wrote it?
      When, against which commit?
      Has anyone verified it?
      Where did it come from?
    Frontmatter (lineage)
      created, created_by (immutable)
      source (type, uri, ref)
      commit (birth commit)
      verification_status
    Footer (review state)
      last_updated, commit
      updated_by (human, ai, ai+human)
      review_status (pending, approved)
      review_score (0-5)
      reviewed_by (human identity)
    Invariants
      Immutable authorship
      AI -> pending (zero score)
      Only humans approve
      Two-block separation
    Common mistakes
      Mutable created_by
      Single block, conflated rates
      Missing human gate
      Ontology drift
      Re-verification cliff
```

You are on a video call with the security team. They have the wiki
page for the authentication flow open in one window and your
Postgres schema in another. "This says the reset token is a UUID,"
they say. "It's been an HMAC since March." Then: "Who wrote this?
When?" You scroll up. You scroll down. The wiki tells you it was
"last edited by the system", four months ago, with no diff. It
does not tell you whether a human wrote it, whether a human ever
read it, or against which commit of the backend it was supposed to
be true.

This chapter is about the second smallest change a software KB can
make and the largest payoff it can extract from that change: a
YAML frontmatter block at the top of every file and a six-field
HTML comment at the bottom. Together, those two blocks force the
KB to answer four questions — *who, when, against what, and has
anyone checked* — at the beginning of every conversation rather
than the middle of the bad ones.

## Why

A KB is only as useful as it is trusted. And "trust" in a software
knowledge base is not a feeling — it is a set of concrete questions
the KB must answer, every time, without a human:

1.  **Who wrote this?** A human teammate, or an LLM?
2.  **When was it written, and against which version of the software?**
3.  **Has anybody verified it is still true?**
4.  **If it came from somewhere else, where?**

A page with no answers to these questions is noise. A page with clear
answers can be reviewed, ranked, retired, or escalated automatically.
Buneman et al. call this the *provenance problem* — "the description of
the origins of a piece of data and the process by which it arrived in a
database" {cite}`buneman2001provenance` — and the W3C PROV data model
generalises it to any information artefact {cite}`w3c_prov`. This
chapter shows how the prose-layer reference implementation turns those
abstract questions into a handful of required YAML fields (plus, as
§"Frontmatter versus footer" will argue, one HTML-comment footer), and
how the code enforces invariants on them so the trust signal cannot
silently rot.

## What

Every Markdown page in `content/` begins with a YAML frontmatter block
delimited by `---` fences. The contract for that block is declared
explicitly in the repo, at `wiki-template/metadata/SCHEMA.md`, and it is
the only piece of configuration in the system that is *not* Go code:

```{literalinclude} ../examples/part2-prose-layer/ch05/SCHEMA.md
:language: markdown
:start-after: "## Frontmatter (Required)"
:end-before: "## Diátaxis Documentation Types"
:caption: The frontmatter contract, verbatim from `SCHEMA.md`.
```

Three fields in particular carry the trust signal:

- `created_by` — *who* produced the page (a username, or the literal
  string `"ai"`). **Immutable** after creation.
- `verification_status` — *how trustworthy* the content currently is
  (`supported` / `unreviewed` / `uncertain` / `contradicted` /
  `superseded`).
- `source` — *where it came from*, if not written directly in the wiki
  (`type`, `uri`, `path`, `ref`). Also **immutable**.

The remainder — `created`, `updated`, `commit`, `tags`, `summary`,
`doc_type`, `status` — support those three by answering "when", "at
which version", and "about what". The full YAML-1.2
specification {cite}`yaml_spec` governs the serialisation, and the
frontmatter-block convention itself was popularised by
Pandoc {cite}`pandoc`.

Why YAML and not, say, a sidecar JSON file or a database row? Three
reasons:

1.  **Co-location.** The metadata travels with the content in a single
    file. A reader who `cat`s the page sees the provenance without
    opening a separate tool.
2.  **Diffability.** A metadata change is a line diff in Git, reviewable
    alongside a body change. Sidecar files split the review across two
    filenames; database rows across two systems.
3.  **Human-writable.** The first author types the YAML by hand when
    they create a page. Machines read and patch it later, but the schema
    is still human-obvious, which keeps the trust contract from
    disappearing behind an ORM.

## How

### Parsing and serialising

The code lives entirely in `frontmatter.go`, and it is short enough to
read in one sitting. Parsing splits the file on the `---` delimiter and
unmarshals the YAML block:

```{literalinclude} ../examples/part2-prose-layer/ch05/frontmatter.go
:language: go
:lines: 16-42
:caption: `ParseFrontmatter` — `---` is the fence, YAML does the rest.
```

Serialisation is the inverse, building the YAML block back around the
body:

```{literalinclude} ../examples/part2-prose-layer/ch05/frontmatter.go
:language: go
:lines: 44-57
:caption: `SerializeFrontmatter` — round-trip with the standard YAML marshaller.
```

The symmetry matters. The same bytes that a human wrote can be read by
the server, patched, and written back, without any lossy projection
through a secondary schema. This is what makes "edit with `vim` and
commit with `git`" a supported workflow rather than an escape hatch.

### Inferring frontmatter for foreign files

Not every Markdown file that lands in `content/` was created by the
wiki. Imports from `raw/`, files dropped in by `cp`, files synced from
another repo — all must become first-class pages. `InferFrontmatter`
synthesises a minimal, plausible frontmatter from the filename and the
file's mtime:

```{literalinclude} ../examples/part2-prose-layer/ch05/frontmatter.go
:language: go
:lines: 59-86
:caption: `InferFrontmatter` — a sane default for files that arrived without a header.
```

Two defaults encode policy:

- `CreatedBy: "human"`. An imported file is *not* assumed to be AI
  unless the importer says so. Chapter 6 will show the pipeline
  overriding this when it knows better.
- `VerificationStatus: VerificationSupported`. A file that already
  existed in the repo has earned at least provisional trust; it is not
  automatically demoted to `unreviewed`.

### The trust default for AI content

The single most consequential line in the whole frontmatter subsystem
is three lines long:

```{literalinclude} ../examples/part2-prose-layer/ch05/frontmatter.go
:language: go
:lines: 88-95
:caption: `DefaultVerificationStatus` — one branch, one cultural commitment.
```

If the author is AI, the default verification status is `unreviewed`.
If the author is human, it is `supported`. This is the policy
`SCHEMA.md` declares at the prose level ("AI-authored pages default to
`verification_status: unreviewed`"), made executable. No human reviewer
has to remember to demote an AI page; the default does it for them.

The write path honours the same rule. `CreatePage` in `service_write.go`
branches on the `wikiAuthor` parameter and then calls the helper:

```{literalinclude} ../examples/part2-prose-layer/ch05/service_write.go
:language: go
:lines: 33-80
:caption: `CreatePage` — author identity is a first-class argument, not a late inference.
```

Two things deserve attention:

1.  `createdBy` is chosen at creation time from the authenticated user
    *or* an explicit AI marker, and then frozen in `fm.Created` /
    `fm.CreatedBy`. Nothing in the service ever mutates those fields
    again.
2.  After the page is written, the service asks the Git layer for the
    current commit hash and writes it back into `fm.Commit`. The page
    literally carries its birth commit in its header. This is
    `where-provenance` in the Buneman sense {cite}`buneman2001provenance`,
    and it is what lets a reader or an agent ask "which version of the
    code does this doc describe?" without leaving the file.

### Enforcing immutability on update

An update path is where provenance usually leaks. A naïve "overwrite the
whole frontmatter" handler would erase `created`, `created_by`, and
`source` every time somebody fixed a typo. `MergeFrontmatterUpdate`
prevents that at the data-structure level:

```{literalinclude} ../examples/part2-prose-layer/ch05/frontmatter.go
:language: go
:lines: 97-113
:caption: `MergeFrontmatterUpdate` — immutable fields are physically copied back from the existing record.
```

The update struct is the *starting* value of the merged result, so
callers can freely pass anything. But `Created`, `CreatedBy`, and
`Source` are then overwritten with the pre-existing values, and
`Updated` is bumped to `time.Now().UTC()`. A malicious or careless
caller cannot rewrite history even if they try. This is the single
invariant that keeps the audit trail honest as the page evolves.

### Frontmatter versus footer: two blocks, not one

So far the chapter has treated the frontmatter as *the* metadata
record. In practice, two very different questions keep arriving at
that one block and crowd each other out:

1.  **Where did this page come from?** — `created_by`, `source`,
    `commit`. Lineage. Rarely changes after creation.
2.  **Is this page still trusted, right now, by whom, and how much?** —
    `verification_status` is a single field trying to answer all of
    that. It is not enough.

The author's private project-knowledge-base toolkit
{cite}`fanyamin_pkb_skill` resolves the crowding by putting review
state into a second block: an HTML-comment **footer** at the bottom of
the page, with six fields that every page must carry. This book adopts
that split as its canonical shape. The frontmatter stays a *provenance*
record; the footer is a *review* record:

```markdown
<!-- PKB-metadata
last_updated: 2026-04-14
commit: 4a1c92b
updated_by: ai
review_status: pending
review_score: 0
reviewed_by:
-->
```

Six fields, each answering one narrow question:

| Field | Type | What it answers |
|-------|------|-----------------|
| `last_updated` | `YYYY-MM-DD` | When was the page's body last touched by *anyone*? |
| `commit` | short SHA | Against which code commit? (Same semantics as frontmatter `commit`; co-located for cheap staleness checks.) |
| `updated_by` | `human` / `ai` / `ai+human` | Who did the most recent change? Mirrors the YAML `updated_by` but uses a closed three-value vocabulary so a gate can match on it. |
| `review_status` | `pending` / `approved` | Has a human signed off on the current content? |
| `review_score` | `0`–`5` | How good is it, in the reviewer's judgement? `0` means not yet reviewed. |
| `reviewed_by` | username or empty | Which human reviewed it? Empty until reviewed. |

**Why two blocks, not one.** Frontmatter and footer move at different
rates and are touched by different actors. Frontmatter records
*lineage*: it is written once at creation, patched carefully on update
(see `MergeFrontmatterUpdate`), and should read cleanly in `git log`
as an almost-unchanged header. Footer records *review state*: it
resets to `pending` every time the body changes, and flips to
`approved` only when a human acts. Co-locating both in frontmatter
conflates the two rates of change — every review-state flip shows up
as a provenance diff — and makes staleness harder to detect
mechanically because a tool has to decide which fields are "the
lineage ones" and which are "the review ones" field-by-field.

**The AI-always-sets-pending rule.** When an LLM — or any automated
path, including the L1 mechanical rewriter in Chapter 16 — modifies a
page, `review_status` MUST be set to `pending`, `review_score` MUST be
reset to `0`, and `reviewed_by` MUST be cleared. Only a *human*
reviewer may set `approved` or a non-zero score. This is the single
rule that makes human attention *auditable*: if the KB's gate system
(Chapter 15) ever sees an `approved` state without a matching human
`reviewed_by`, something bypassed the rule and the gate fails. Without
this discipline, the word "approved" loses meaning the first time an
LLM is allowed to write it.

**What the footer is *not*.** It is not a replacement for
`verification_status`. The frontmatter field records the *editorial*
trust signal ("is this content supported, contradicted, superseded?")
and is about content correctness. The footer records the *review*
signal ("has a human looked at this version?") and is about review
cadence. A page can have `verification_status: supported` in the
frontmatter and `review_status: pending` in the footer — meaning "we
believed it when it was written; no one has checked it since an LLM
rewrote it yesterday". Both signals matter; they answer different
questions.

Chapter 15 makes the footer a hard build gate; Chapter 16 uses it to
route changes through the three-level update strategy; Chapter 18
extends single-axis document layering (L0–L4) into a four-tuple
`(layer, updated_by, review_status, review_score)` so a retrieval
system can filter on review state without losing the lineage axis. The
footer is the load-bearing hinge between this chapter and all three.

## Example

Here is the lifecycle of a single page, told through its frontmatter.

**Stage 1 — a human creates the page through the API.** Frontmatter
and footer agree: Alice wrote it, she is its reviewer of record, it is
approved at its birth commit.

```yaml
---
title: How to enable TLS on the wiki
slug: how-to-enable-tls-on-the-wiki
created: 2026-04-10T14:03:11Z
created_by: alice
updated: 2026-04-10T14:03:11Z
updated_by: alice
status: published
doc_type: how-to
verification_status: supported
commit: a1b2c3d4e5f6
---
```

```markdown
<!-- PKB-metadata
last_updated: 2026-04-10
commit: a1b2c3d4
updated_by: human
review_status: approved
review_score: 3
reviewed_by: alice
-->
```

**Stage 2 — an LLM agent rewrites the body for clarity.** Frontmatter
demotes `verification_status` to `unreviewed` (the existing
Chapter-5 rule). Footer, enforcing the AI-always-sets-pending rule,
resets `review_status` to `pending`, zeros `review_score`, and clears
`reviewed_by`. The two blocks reinforce each other:

```yaml
---
title: How to enable TLS on the wiki
slug: how-to-enable-tls-on-the-wiki
created: 2026-04-10T14:03:11Z      # preserved
created_by: alice                   # preserved
updated: 2026-04-14T09:27:00Z      # bumped
updated_by: ai                      # new signal
status: published
doc_type: how-to
verification_status: unreviewed     # demoted by default
commit: 9f8e7d6c5b4a
---
```

```markdown
<!-- PKB-metadata
last_updated: 2026-04-14
commit: 9f8e7d6c
updated_by: ai                 # matches frontmatter
review_status: pending         # reset: human has not seen this
review_score: 0                # reset
reviewed_by:                   # cleared
-->
```

Notice: `created_by` is still `alice`. The update did not rewrite
history. But `verification_status` fell to `unreviewed` automatically
*and* `review_status` fell to `pending`, so any reader or retriever
that cares about trust can filter on either signal — or both.

**Stage 3 — a human approves the rewrite.** The frontmatter logs the
reviewer as the most recent `updated_by`; the footer logs the separate
act of *approval*, which is not the same thing as the act of editing:

```yaml
verification_status: supported
updated_by: alice
updated: 2026-04-14T10:15:42Z
# created_by: alice  (still)
```

```markdown
<!-- PKB-metadata
last_updated: 2026-04-14
commit: 9f8e7d6c
updated_by: ai+human           # AI wrote the body; a human approved it
review_status: approved
review_score: 4
reviewed_by: alice
-->
```

The `ai+human` value on `updated_by` is deliberate: it records that
the current state of the page is an LLM draft that a human has
validated, which is a genuinely different provenance claim from either
`ai` alone (LLM wrote it, no one has checked) or `human` alone (a
human wrote it themselves). Chapter 18's document-layering tuple reads
this value when it classifies a page.

Three states, one file, a full provenance trail *and* a full review
trail — and no side tables. `git log -p content/how-to/enable-tls.md`
tells you the whole story for both.

## Competing approaches

| System | Provenance model | Immutability of authorship | Review state |
|--------|------------------|----------------------------|--------------|
| The prose-layer reference implementation | YAML frontmatter + Git commit SHA + `PKB-metadata` footer | Enforced in `MergeFrontmatterUpdate`. | Explicit six-field footer (see §"Frontmatter versus footer"). |
| Pandoc / MyST {cite}`pandoc,myst_parser` | YAML metadata block | Convention only; no enforcement. | None. |
| Notion AI {cite}`notion_ai` | Proprietary audit log | Opaque; vendor-controlled. | Per-block comments. |
| Confluence | Revision history table | Good; coupled to a proprietary DB. | Page status / labels. |
| Plain Markdown + Git | Git history only | Strong for *git blame*, but no explicit "this was AI" field. | None. |
| W3C PROV-O {cite}`w3c_prov` | Full RDF/OWL ontology | Academic rigour; rarely adopted in docs tools. | `prov:wasInvalidatedBy` models deprecation. |

The reference implementation's stance is deliberately narrow: a tiny
subset of PROV's vocabulary (`wasGeneratedBy`, `wasDerivedFrom`,
`generatedAtTime`), encoded as plain YAML keys in the frontmatter and a
six-field HTML-comment footer for review state, so authors and agents
can read both without learning a new framework.

## Common mistakes, and how each one quietly breaks trust

Provenance schemas are failure-prone in a specific way: they degrade
*silently*. A broken search box announces itself; a broken trust layer
keeps serving pages that happen to be wrong. Five failure patterns
show up in almost every real deployment, and each one has a
corrective rule worth stating explicitly.

1.  **Treating `created_by` as mutable.** A well-intentioned bulk
    migration ("let's re-stamp the author field now that we have
    real user accounts") silently rewrites every page's
    `created_by`, and an entire audit trail evaporates. The rule is
    that authorship is *historical*, not *administrative*: once
    written, `created`, `created_by`, and `source` are frozen, and
    the only legitimate way to change them is to correct a genuine
    mistake *with a PR that records the correction in Git*.
    `MergeFrontmatterUpdate` enforces this at the data-structure
    level precisely because well-intentioned code paths cannot be
    trusted to remember the invariant {cite}`buneman2001provenance`.

2.  **Cramming review state into frontmatter.** The most common
    shape in the wild is a single `status: reviewed | pending`
    field in the frontmatter, and nothing else. It fails for the
    reason §"Frontmatter versus footer" already covered:
    review state flips every time an LLM touches the body, and a
    flipping review field in `git log` buries the *real* lineage
    changes under review-state noise. The two-block split is not a
    stylistic preference; it is what lets `git log` stay readable
    as the KB ages.

3.  **No hard gate on `approved`.** A schema that permits any actor
    to write `review_status: approved` is a schema that, within a
    year, has LLM-approved pages in it. The AI-always-sets-pending
    rule is necessary but not sufficient — a build gate must
    additionally refuse to publish any page whose `approved` state
    lacks a matching human `reviewed_by`. Chapter 15 wires that gate
    in; the common failure is shipping the schema without the gate
    and *assuming* the rule will hold by convention.

4.  **Ontology drift in `source.type`, `doc_type`, and status
    enumerations.** A team starts with a small closed vocabulary
    (`tutorial | how-to | reference | explanation`), and six months
    later the index has accreted `guide`, `docs`, `ref`, `manual`,
    and an empty string — because nobody refused the pull requests
    that introduced them. The rule is that closed vocabularies must
    be *syntactically* closed, i.e. the frontmatter validator must
    reject unknown values. A soft gate that merely warns is eaten by
    the review queue within weeks.

5.  **The re-verification cliff.** A page created in April with
    `verification_status: supported` is still `supported` in October,
    even though the code it describes has been rewritten twice. The
    frontmatter looks honest; the content is stale. This is the
    failure the Chapter 7a operational model is designed to surface:
    `verification_status` is a *point-in-time* claim tied to
    `commit`, and an automated staleness detector must mechanically
    demote pages whose `commit` no longer matches the code they
    reference (Chapter 14). Trust that does not degrade automatically
    turns into fiction.

6.  **`source` fields that lie by omission.** A page imported from
    an external URL carries `source.uri` pointing at that URL —
    until the URL 404s or silently rewords the source. The rule is
    that `source.ref` (a commit-like identifier) must accompany
    `source.uri` whenever the source has one: for code imports, the
    code commit; for article imports, the Wayback Machine snapshot
    timestamp; for API specs, the OpenAPI file's content hash. A
    `source` without a `ref` is a moving target and, for audit
    purposes, no better than no source at all.

The common thread across all six is that *provenance needs
enforcement, not only expression*. A trust schema with no validator
is decoration; a validator with no hard gate is a warning light no
one reads. The chapter's whole argument is that frontmatter + footer
+ merge invariants + build gates together form a single machine, and
removing any corner collapses the other three.

## Conclusion

Frontmatter and footer are not decoration. Together they are the
contract between the prose layer and every downstream consumer —
retrieval, publishing, the code graph, an AI coding assistant — about
*where a page came from* and *how much to trust it right now*.
`SCHEMA.md` declares the contract; `frontmatter.go` and
`service_write.go` enforce the lineage half; the `PKB-metadata` footer
carries the review half; Git records both as physical diffs. Together
they give a software KB something traditional wikis struggle to
articulate: an explicit, machine-checkable answer to "who wrote this,
against which commit, is it still trusted, and by whom?"

The next chapter takes that contract and walks through the pipeline
that produces well-formed frontmatter — and an honest `pending` footer
— even when the input is a messy folder of dumped files.

## References

```{bibliography}
:filter: keywords % "provenance" or keywords % "prose-layer"
```
