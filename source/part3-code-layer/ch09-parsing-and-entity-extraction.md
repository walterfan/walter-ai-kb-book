---
title: 'Chapter 9 — Parsing and Entity Extraction'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - code-layer
  - parsing
  - deepwiki
---

# Chapter 9 — Parsing and Entity Extraction

This chapter on one page — one entity model, one adapter per
language, three pitfalls the parser itself must handle:

```{mermaid}
mindmap
  root((Parser))
    Entity model
      Stable ID
      Four kinds
      Location-aware
      Signature and doc
    Per-language adapters
      Go via tree-sitter
      Python via tree-sitter
      Java via tree-sitter
      Add new in 150 LoC
    Pitfalls
      Resource leaks
      Anonymous functions
      Multi-line signatures
    Common mistakes
      Regex MVP
      Unstable IDs
      Too many entity kinds
```

You wrote the first version yesterday evening. Sixty lines of
regex. `func `, `def `, `class ` — how hard could it be? This
morning the indexer emitted 15 000 "functions" in a 4 kLOC
repo. Half the hits are closure literals inside `map(...)` calls.
Three of them are the word `function` inside a string literal.
The call graph you built off of those entities is a beautiful
fiction: 80 % of the edges point at anonymous `func1`, `func2`,
`func3`. Every chapter after this one — embeddings, graph,
retrieval, generation — is downstream of what this module
emits. **This chapter is about why the parser is the single
most leverage-positive component in a code KB, and what a
boringly correct one actually looks like.**

## Why

Everything downstream — embeddings (ch10), graph (ch11), retrieval
(ch12), answers (ch13) — is a function of what the parser emits. If
the parser drops a method, no retriever can find it. If the parser
confuses a signature with a body, every embedding is off. The parser
is the single most leverage-positive component in a code-KB; it is
also the one most likely to be written in a hurry and never touched
again.

A naive parser — "split on `func ` for Go, `def ` for Python, regex
for Java" — collapses at the first nested generic, first
multi-line signature, first anonymous function literal, first
heredoc, or first one of several dozen other language-specific
eccentricities. The DeepWiki methodology
{cite}`fanyamin2026deepwiki` argues (§4) that shipping *one thin
extractor per language* on top of a **real** parser is both cheaper
and more robust than the grep-shaped alternative.

## What

Three design decisions define the extraction contract in the
code-layer reference implementation's `reference-impl/code-kg/parser`
package.

**1 — One parser, many languages.** Tree-sitter
{cite}`brunsfeld_treesitter` gives a uniform parse-tree API over
Go, Java, and Python, along with an incremental parsing model and
the error-tolerance property that matters in a KB: files that are
mid-edit should still produce usable trees. The alternative stack
(per-language toolchains: `go/ast`, `javaparser`, `libcst`) triples
both dependencies and the surface area of "one-off bugs".

**2 — A language-neutral intermediate representation.** Whatever
tree-sitter emits is collapsed to a `CodeMetadata` struct: a list of
files, each with functions and classes, each entity carrying
`name`, `start_line`, `end_line`, `signature`, `docstring`, `body`.
That IR is small enough to reason about, large enough to feed every
downstream stage, and — critically — *language-free*. Chapter 10
embeds it, Chapter 11 graphs it, Chapter 14 diffs it.

**3 — Supported extensions and skip directories are configured, not
inferred.** The parser refuses to walk `vendor/`, `node_modules/`,
`.git/`, `__pycache__/`, `dist/`, `build/`, `target/`, `.next/`.
Every one of those defaults is a scar from somebody's first run
choking on a monorepo. `allamanis2018survey`
{cite}`allamanis2018survey` catalogues the same pathology at
research scale: most "big code" corpora need aggressive vendoring
filters before any model survives training.

## How

The parser service is 66 lines. Vendored from
`reference-impl/code-kg/parser/parser.go` at the commit recorded in
the header:

```{literalinclude} ../examples/part3-code-layer/ch09/parser.go
:language: go
:lines: 11-50
:caption: parser.Service — supported extensions, skip dirs, single Walk.
```

Three things are worth naming on that listing:

- Line-range `26-30` (`supportedExtensions`) is the closed set of
  file types the KB indexes. Adding a fourth language is a one-line
  change — and a downstream review obligation, because the
  tree-sitter grammar must be linked in too.

- Line-range `32-50` (`CollectSupportedFiles`) shows the
  `filepath.Walk` with the `SkipDir` shortcut. In a 120 k-file
  monorepo the `node_modules/` branch alone holds 95 % of the inode
  count; skipping it lazily (before descending) is what makes first
  sync tolerable.

- `CollectGoFiles` (line 52 in the source) is a legacy alias that
  has widened over time: it now returns *all* supported files, not
  just Go. Renames are risky in a library used by many call-sites,
  so the project leaves the name and adds a new method — a common
  pattern with clear provenance in the Git blame.

### The entity model

The IR that downstream stages consume is the `CodeEntity` struct:

```{literalinclude} ../examples/part3-code-layer/ch09/domain_types.go
:language: go
:lines: 3-30
:caption: CodeEntityType enum plus the canonical CodeEntity record.
```

Three aspects of that definition have structural consequences:

- `EntityType` is a small closed enum (`package`, `file`,
  `function`, `class`, `struct`, `interface`, `variable`,
  `constant`). New entity types require a migration; that is a
  feature, not a bug. See §*Bounded relation taxonomy* in
  Chapter 11 for the symmetric argument on edges.

- `StartLine` and `EndLine` are first-class fields on every entity.
  They make the entity ID (Chapter 11) stable across re-indexes,
  and they let Chapter 13's generator cite results as
  `file.ext:L12-L47`. Every downstream affordance in the KB
  ultimately rests on the parser having preserved the original
  source coordinates.

- `Body`, `Signature`, and `DocString` are kept separate. The body
  is truncated to 4 000 characters (in `parseFileForSync`) before
  being stored, while the signature and docstring are never
  truncated. That split is the foundation of Chapter 10's
  *embed-the-header-not-the-body* rule: the signature and docstring
  survive in full to the embedder; the body survives to the
  retriever only, truncated.

### Per-language adapters

Tree-sitter emits a syntax tree, not a named-entity list. The
conversion lives in a different package (the per-language adapter
in `reference-impl/code-kg/rag`, not vendored in this book because
it is boilerplate-heavy), but the pattern is short and worth making
explicit. For each supported language, one visitor:

1.  Walks the tree in pre-order.
2.  When it sees a node whose kind is in a per-language whitelist
    — Go `function_declaration`, `method_declaration`,
    `type_spec` with a `struct_type` or `interface_type`; Python
    `function_definition`, `class_definition`; Java
    `method_declaration`, `class_declaration` — it records the
    entity.
3.  Uses the node's source range to fill `StartLine`, `EndLine`,
    and `Body`.
4.  Uses preceding doc-comment nodes (if present) as the
    `DocString`.

The discipline is: *one visitor per language, as dumb as possible*.
No cross-file resolution (that happens in Chapter 11's graph
builder), no symbol tables, no type inference. The tree-sitter
grammar carries the language-specific complexity; our code stays
small.

### Pitfalls from the field

Three failure modes are worth the reader's attention because they
all cost time to diagnose:

- **Resource leaks.** Tree-sitter trees hold a pointer into a
  Rust-owned arena and must be freed with `tree.Close()` (or the
  bindings' equivalent). Forgetting is not an immediate crash; it
  surfaces later as a slow memory creep under a long-running
  indexer. `defer tree.Close()` is mandatory.

- **Closures and anonymous functions.** Every language has them,
  and they *all* show up as "function-like" nodes in the parse
  tree. Emitting them as entities pollutes the graph with hundreds
  of anonymous nodes called `func1`, `func2`, etc. The fix is a
  per-language filter: only emit top-level and method-level
  functions; treat anonymous functions as part of their enclosing
  entity's body.

- **Generic types and multi-line signatures.** The *signature* we
  store is the first non-empty line of the body — via the
  `extractSignature` helper we see again in Chapter 10. For a Go
  generic like `func Map[K comparable, V any](m map[K]V) []K`
  that works. For a Java method whose parameters wrap across five
  lines, it produces a truncated signature. Our fix is to feed the
  full signature from the tree-sitter node range, not from a naive
  line-split — see `extractSignature` uses. This is called out as
  a known bug with a tracked fix.

### Common mistakes

Three additional anti-patterns come up whenever a team tries to
short-cut the parser stage. Each is *tempting* because it seems
cheaper up front, and each pays back the cost 10x downstream.

**1 — "Regex is enough for MVP."** The symptom is a one-line
identifier regex — `/func\s+(\w+)/` — emitting 15 000 entities in
a 4 kLOC repo. Comments match. String literals containing the
word `function` match. The test harness's `describe("function
X", ...)` matches. The regex is not *approximately* a parser — it
is a completely different function. Every chapter downstream
(embeddings, graph, retrieval) inherits the noise and amplifies
it. Use a real parser (tree-sitter, language-server, compiler
frontend) from the first commit. It is not the slow path.

**2 — Unstable entity IDs.** The symptom is that re-running the
indexer on an unchanged repo produces a diff in your vector
store. Why? The `id` was constructed from `filepath + name`, or
from a hash that included the full body (so whitespace edits
cascade), or it contained an auto-increment counter. The graph's
edges then point at IDs that no longer exist. The fix is the
scheme of Chapter 10: `sha256(repoID + filePath + entityType +
name + startLine)[:16]`. Stable across re-index, but sensitive
enough that moving a function to a new line produces a new ID
(which is correct behaviour).

**3 — Emitting "too clever" entity types.** The symptom is a
parser that emits 23 entity kinds — `struct-field`, `enum-variant`,
`type-alias`, `const-declaration`, … — and a retrieval layer
that now has to reason about which kinds to mix. Cardinality
explodes, ranking signals dilute, and the graph's node types
outgrow any reasonable visualisation. Start with the four of
Chapter 9 — `package`, `type`, `method`, `function` — even for
Java where "interface" feels different from "class." You can
always refine later; you cannot un-emit an entity type that is
already baked into 200 downstream rules.

## Example

A reproducible four-line demonstration, run against the code-layer
reference implementation itself:

```bash
cd ~/reference-impl/code-kg
go run ./cmd/code-kg register --name code-kg --path . --id demo
go run ./cmd/code-kg sync --repo-id demo
sqlite3 code-kg.db "SELECT entity_type, COUNT(*) FROM entities
                    WHERE repo_id='demo' GROUP BY entity_type;"
```

On the commit used for this chapter's excerpts, the output is:

```
class|24
function|412
```

The ratio matters more than the absolute numbers: a healthy Go
codebase is function-heavy. If you see 5 000 "functions" on a 50
kLOC Java repo, your parser is treating every closure as an
entity — go fix the visitor.

## Conclusion

The parser is small, but everything in Part III depends on three
contracts it establishes: a uniform IR across languages (Claim 1),
faithful source coordinates on every entity (Claim 2), and an
aggressive default skip-list for vendored directories (Claim 3).
Break any of the three and every downstream chapter breaks with it.

Chapter 10 takes the IR as input and turns the *identity* half of
each entity (language, type, name, signature, docstring) into a
vector — the part, famously, where most code-RAG tutorials go
wrong.

## References

```{bibliography}
:filter: keywords % "parsing" or keywords % "code-layer" or keywords % "deepwiki"
```
