<!--
<!-- BOOK EXCERPT — vendored for citation, do not hand-edit
<!-- source_repo:     prose-layer-reference-impl
<!-- source_path:     reference-impl/prose-wiki-template/metadata/SCHEMA.md
<!-- commit_sha:      working-tree  (dirty — uncommitted changes)
<!-- captured_at:     2026-04-17T21:13:41Z
<!-- content_sha256:  a1742989d00ec4c4d0f139f974a1e942381609073f62f920b8cf5cb9273d05fe
<!-- regenerate with: make book-refresh-excerpts
-->

# Wiki Schema

*Conventions for humans and LLMs contributing to this knowledge base.*

## Naming Convention

All file and directory names MUST use only: **lowercase letters (`a-z`), digits (`0-9`), underscores (`_`), and hyphens (`-`)**.

- **Files**: e.g. `go-concurrency.md`, `my_notes.md`
- **Categories**: directory names, e.g. `programming/go`, `dev_ops`
- **Slugs**: auto-generated from filename, used for URLs
- Chinese characters are transliterated to pinyin during sanitization
- Other unsupported non-ASCII characters are stripped during sanitization
- Spaces become hyphens, underscores are preserved, uppercase is lowered

## Frontmatter (Required)

```yaml
---
title: "Page Title"           # Required
slug: page-title               # Auto-generated from title
tags: [tag1, tag2]             # Optional
summary: "Brief description"   # Recommended
created: 2026-01-01T00:00:00Z # Auto-set
created_by: alice              # Immutable after creation
updated: 2026-01-01T00:00:00Z # Auto-set
updated_by: alice              # Updated on each edit
status: published              # draft | published | archived
doc_type: reference            # tutorial | how-to | reference | explanation
verification_status: supported # supported | unreviewed | uncertain | contradicted | superseded
source:                        # Optional, immutable
  type: original               # original | git_repo | doc | url
  uri: ""
  path: ""
  ref: ""
---
```

## Diátaxis Documentation Types

| Type | Purpose | Orientation |
|------|---------|-------------|
| **tutorial** | Learning-oriented | Practical steps for beginners |
| **how-to** | Task-oriented | Steps to solve a specific problem |
| **reference** | Information-oriented | Technical description of the machinery |
| **explanation** | Understanding-oriented | Clarification and discussion of a topic |

## Trust Model

- Human-authored pages default to `verification_status: supported`
- AI-authored pages default to `verification_status: unreviewed`
- `created_by` and `source` are immutable after creation
- AI content must be clearly marked with `created_by: ai` or `updated_by: ai`

## Wiki Links

Use `[[Page Title]]` to link to other pages. Use `[[Page Title|Display Text]]` for custom link text.

## TDD Convention

- Test naming: `Test<Domain>_<Behavior>_<ExpectedResult>`
- Every feature has co-located tests
- Phase gates require 100% test pass rate
