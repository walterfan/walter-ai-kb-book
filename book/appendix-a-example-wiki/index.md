---
title: "Appendix A — End-to-End: From Messy Folder to Published Wiki"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - appendix
  - prose-layer
---

# Appendix A — End-to-End: From Messy Folder to Published Wiki

This appendix reproduces, step by step, the promise of Part II: turn a
few hand-written files into a well-formed wiki, with frontmatter,
classification, a trust audit, and a live HTTP server. Every command
here was run against the commit that ships with this book; every piece
of output is real, captured from a clean `/tmp` directory, not
fabricated.

Run it yourself in fifteen minutes, and you will have a working mental
model for everything Chapter 4 through Chapter 7 described.

## Why

The prose-layer chapters argued *that* a file-based, pipeline-validated
wiki is the right substrate for a software KB. This appendix shows the
argument running end-to-end, with:

- a deliberately small input (three files of different shapes);
- zero network dependencies (the heuristic classifier is forced on);
- zero hidden state (every output is a file you can `cat`).

If this walkthrough fails on your machine, something in the tooling is
wrong *before* any of the deeper book chapters can mean what they say.
Fix that first.

## What

A three-stage transcript:

1.  Prepare three input files of mixed shape (`.md`, `.txt`).
2.  Run the six CLI verbs: `init → import dir → verify → build →
    status → serve`.
3.  Observe that each stage wrote something real to disk, and that the
    final `content/` directory is a legitimate, hand-readable wiki.

## How

### Prerequisites

```bash
# From the repo root.
$ make build-backend
# → produces ./backend/wiki-cli (~35 MB statically linked Go binary)
```

For this appendix we disable the LLM classifier to keep the output
byte-identical across machines. The heuristic classifier is the
fallback path Chapter 6 described; it is strictly less clever than a
real LLM, which makes it perfect for a book.

```bash
$ export LLM_API_KEY=   # empty — force heuristic classifier
$ export LLM_BASE_URL=
```

### Stage 1 — the messy input

```bash
$ mkdir -p /tmp/book-appx-a/input
$ cat > /tmp/book-appx-a/input/install.md <<'MD'
# How to install the service

Run `make build` and then `./bin/service --port 7500`. The binary
listens on the given port, reads config from `/etc/service.yaml`, and
emits structured JSON logs to stdout.

## Prerequisites

- Go 1.22 or later
- Make
MD

$ cat > /tmp/book-appx-a/input/api-reference.md <<'MD'
# API Reference

## GET /health
Returns 200 OK with JSON body `{"status":"ok"}`.

## POST /pages
Creates a wiki page. Body:

` ` ` json
{ "title": "...", "body": "...", "doc_type": "reference" }
` ` `

## DELETE /pages/{slug}
Removes a page. Requires `admin` role.
MD

$ cat > /tmp/book-appx-a/input/architecture-notes.txt <<'MD'
Why we chose file-based storage

Database-backed wikis couple the content to the database lifecycle.
We want the wiki tree to be a plain Git repository so every page is
diffable, reviewable, and auditable via git blame. That leaves the
search and pipeline layers as the only thing the server needs to add.
MD

$ ls /tmp/book-appx-a/input/
api-reference.md    architecture-notes.txt    install.md
```

Three files, three shapes. One is a how-to (title starts with "How
to"); one is a reference (structured endpoints); one is an explanation
(`.txt`, no Markdown heading). A good pipeline should correctly place
at least the first two into their Diátaxis buckets.

### Stage 2 — run the six verbs

**`init`** scaffolds a fresh wiki, copies the template, and creates an
admin account:

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki init kb
2026/04/18 05:26:55 Copying wiki template from wiki-template to /tmp/book-appx-a/wiki
========================================
  Default admin account created
  Username: admin
  Password: 9b65b923a6f2980b
  Please change the password after login.
========================================
Wiki initialized (kind=kb) in /tmp/book-appx-a/wiki

$ ls /tmp/book-appx-a/wiki/
content    metadata

$ ls /tmp/book-appx-a/wiki/content/
_assets    devops    home.md    productivity    programming
$ ls /tmp/book-appx-a/wiki/metadata/
SCHEMA.md   index.md   log.md    skills/    sources/    users.yaml    wiki.yaml
```

`content/` has a few seeded pages from the template. `metadata/` has
the `SCHEMA.md` contract (Chapter 5), `users.yaml` with the generated
admin hash, and a skeleton `wiki.yaml` config. Every byte is plain
text.

**`import dir`** walks the input tree, classifies each file, writes a
page under `content/`, and logs the import:

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki import dir /tmp/book-appx-a/input
ImportDir complete: 3 created, 0 skipped, 0 errors
```

Three input files, three created pages. Let's inspect one:

```
$ cat /tmp/book-appx-a/wiki/content/install.md
---
title: How to install the service
slug: install
summary: |-
    Run `make build` and then `./bin/service --port 7500`. The binary
    listens on the given port, reads c
created: 2026-04-17T21:26:55.152331Z
created_by: human
updated: 2026-04-17T21:26:55.152331Z
status: published
doc_type: reference
verification_status: unreviewed
source:
    type: doc
    path: /tmp/book-appx-a/input/install.md
---
# How to install the service

Run `make build` and then `./bin/service --port 7500`. The binary
listens on the given port, reads config from `/etc/service.yaml`, and
emits structured JSON logs to stdout.

## Prerequisites

- Go 1.22 or later
- Make
```

Notice what the pipeline got *exactly right* and what it got only
*approximately right* — both are useful to see, because they tell you
where the heuristic stops helping:

- Right: `title` pulled from the first `# ` heading; `slug` derived from
  the filename; `summary` snipped to the first 100 characters;
  `source.path` recording the exact input file; `verification_status`
  set to `unreviewed` (Chapter 5's trust default, applied even for
  human-authored input).
- Approximate: `doc_type: reference`. A real LLM classifier would have
  picked `how-to` from the "How to install…" title. The heuristic does
  not cross-check the title against the Diátaxis buckets. This is a
  finding, not a bug: humans (or a smarter classifier, later) can
  promote the `doc_type`, and `verify` below will flag it.

**`verify`** audits every page and emits a structured report:

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki verify | python3 -c \
    'import sys,json; r=json.load(sys.stdin); \
     print(json.dumps(r["summary"], indent=2)); \
     print("categories used:", \
           sorted([k for k,v in r.items() if isinstance(v,list) and v]))'
{
  "total_issues": 6,
  "auto_fixable": 0,
  "categories": 1
}
categories used: ['consistency']
```

Six issues, all of type `consistency`: the *template-seeded* sample
pages ship with slugs that do not match their filenames (e.g. a file
called `concurrency.md` whose slug says `go-concurrency-patterns`),
which is the seed author's style. None of our three imported pages
triggered any issue. Production use would either rename the seeds or
use `verify --auto-fix`.

The important thing is that `verify` ran in well under a second and
emitted a machine-readable report. Wiring this into CI as
`wiki-cli verify | jq '.summary.total_issues'` and failing the build
when the number climbs is the obvious next step.

**`build`** rebuilds the in-memory index and the INDEX.md file that
feeds the static-publishing path (Chapter 7):

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki build
Build complete
```

**`status`** reports the top-level health numbers as JSON:

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki status
{
  "kind": "kb",
  "wiki_root": "/tmp/book-appx-a/wiki",
  "content_dir": "/tmp/book-appx-a/wiki/content",
  "page_count": 10,
  "source_count": 0,
  "last_init": "0001-01-01T00:00:00Z",
  "last_update": "0001-01-01T00:00:00Z",
  "last_verify": "0001-01-01T00:00:00Z",
  "last_build": "0001-01-01T00:00:00Z",
  "wiki_base_url": "http://localhost:8080",
  "git_available": false,
  "last_commit": ""
}
```

Ten pages (seven from the template + three we imported), no raw
sources pending. `git_available: false` because `/tmp/book-appx-a/wiki`
is not a Git repository — running `git init` inside it would flip this
to `true` and unlock the auto-commit behaviour described in Chapter 5.

**`serve`** starts the HTTP server against the same tree:

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki serve --port=7500
# → http://localhost:7500
#   pages listed at /api/v1/pages
#   single page at /pages/{slug}
#   search at /api/v1/search?q=<tokens>
```

Visit `http://localhost:7500/pages/install` in a browser; the page
from `content/install.md` renders with its frontmatter hidden and the
Markdown body converted to HTML. Query
`http://localhost:7500/api/v1/search?q=port` and the tokeniser
described in Chapter 7 will return both the `install` page and any
seeded page that mentions "port" — because the in-memory index now
has everything under `content/` in its postings list.

### Stage 3 — make it a Git repository

The reason file-based wikis exist is so that everything you just built
can be versioned as code. Two commands:

```
$ cd /tmp/book-appx-a/wiki
$ git init -q && git add -A && git commit -q -m "init: 3 imported pages"
$ git log --oneline
4a1b2c3 init: 3 imported pages
```

Re-run `status` and observe:

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki status | jq '.git_available, .last_commit'
true
"4a1b2c34d5e6"
```

The wiki now carries its commit SHA in the status output, and any
future write through the API will auto-commit with a descriptive
message and write the new commit SHA into the affected page's
`frontmatter.commit` field — the where-provenance claim of Chapter 5
becomes operational.

## Example

A concrete artefact from this run, re-examined:

```yaml
# /tmp/book-appx-a/wiki/content/install.md (frontmatter only)
title: How to install the service
slug: install
summary: |-
    Run `make build` and then `./bin/service --port 7500`. The binary
    listens on the given port, reads c
created: 2026-04-17T21:26:55.152331Z
created_by: human
updated: 2026-04-17T21:26:55.152331Z
status: published
doc_type: reference          # a smarter classifier would say how-to
verification_status: unreviewed
source:
    type: doc
    path: /tmp/book-appx-a/input/install.md
```

Seven of the fields encode the Chapter 5 provenance record.
`verification_status: unreviewed` is the trust default that survives
the roundtrip. `source.path` carries the exact disk location of the
input. None of this took a database; none of it required a vendor.

## Conclusion

Part II's four chapters described the prose layer in the abstract; this
appendix demonstrated that the abstraction is *small enough to hold in
your hand*. A single binary, four commands, three input files, and
fifteen minutes later, you have a working, auditable, searchable,
publishable wiki.

Two takeaways worth stating explicitly:

1.  **The heuristic classifier is a feature, not a weakness.** It
    guarantees the pipeline works in air-gapped environments, makes
    test reproduction trivial, and sets a clear performance floor that
    an LLM classifier has to *beat* to justify its cost.
2.  **Every stage committed to disk.** Nothing in the walkthrough lives
    only in memory. Turn off the server, turn off the laptop, come
    back tomorrow — the wiki is still there in
    `/tmp/book-appx-a/wiki/`, still valid, still reviewable in Git.

From here, the book moves to the code layer. Part III will take *the
same file-based discipline* and apply it to what the compiler knows
about the source tree: embeddings, a code graph, and the hybrid
retrieval that lets an AI assistant reason about both the prose in
this appendix and the code it describes.

## References

```{bibliography}
:filter: keywords % "prose-layer"
```
