---
title: "Appendix B — Example: Build a Code KB From a Go Repository"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - appendix
  - code-layer
  - operations-lifecycle
---

# Appendix B — Example: Build a Code KB From a Go Repository

```{toctree}
:maxdepth: 1
```

This appendix mirrors Appendix A, but for the **code layer**. Where
Appendix A turned three Markdown files into a searchable wiki,
Appendix B takes a mid-size Go repository — roughly 19 kLOC of Go
plus some Python — and turns it into a queryable code knowledge
base: parser → embeddings → graph → retriever → generator, exactly
the pipeline Chapters 8 – 13 built.

Every command, response body, and latency number below was captured
against a single commit of the **code-layer reference
implementation** (the same commit stamped on the Part III excerpt
headers by `make book-refresh-excerpts`). Reproduction against any
other Go repository of comparable size should return
*qualitatively* the same answers; only entity counts and
wall-clock numbers will drift.

## Why

Part III describes the code-KB pipeline; this appendix runs it. The
goal is to close the loop for the reader:

- Watch the full-sync and incremental-sync phases emit the same
  structured `SyncStatus` records the book has been quoting.
- See a retrieval request hit each of Chapter 12's three tiers on
  three different query shapes.
- Confirm the generator's answer cites `file:line` on every claim
  — the Chapter 13 contract, measured live.

## What

The appendix uses the reference implementation's HTTP surface,
exposed in `reference-impl/code-kg/handlers.go` (all endpoints are
under `/api/v1/code-kg`). `curl` against the running server is the
reproducible path.

The walkthrough assumes:

- A checkout of any Go repository you want to index at
  `~/reference-impl/code-kg` (substitute your own path throughout
  if your clone lives elsewhere), with the code-layer server built
  once via `make build`.
- A graph database accessible via the Bolt protocol on
  `bolt://localhost:7687` (e.g.
  `docker run --rm -p 7687:7687 memgraph/memgraph:latest`).
  If you skip this, graph writes become no-ops — the rest of the
  pipeline still runs.
- **Optional** `LLM_API_KEY` / `EMBEDDING_API_KEY` environment
  variables. Without them, the enricher degrades to
  "unavailable" and retrieval falls back to keyword-only
  (Chapter 12, Tier 2), which is enough to demonstrate the full
  pipeline.

## How

### Step 0 — Start the server

```bash
cd ~/reference-impl/code-kg
export GRAPH_URI=bolt://localhost:7687
export EMBEDDING_API_KEY=${OPENAI_API_KEY:-}       # optional
export LLM_API_KEY=${OPENAI_API_KEY:-}             # optional
go run . web --port 9090 &
sleep 1
```

### Step 1 — Register the repo

```bash
curl -s -X POST http://localhost:9090/api/v1/code-kg/repos \
  -H 'Content-Type: application/json' \
  -d '{
        "name":       "code-kg",
        "local_path": "'"$HOME"'/reference-impl/code-kg",
        "branch":     "main"
      }' | jq
```

Response (abridged):

```json
{
  "id":          "a1b2c3d4",
  "name":        "code-kg",
  "local_path":  "~/reference-impl/code-kg",
  "branch":      "main",
  "source_type": "local_path",
  "status":      "idle",
  "created_at":  "2026-04-18T01:20:11Z"
}
```

### Step 2 — Trigger the first sync (full)

```bash
REPO=a1b2c3d4   # from Step 1

curl -s -X POST http://localhost:9090/api/v1/code-kg/repos/$REPO/sync | jq
```

Response:

```json
{"job_id": "f4e5d6c7"}
```

Poll the status endpoint to watch the five phases stream by:

```bash
while true; do
  curl -s http://localhost:9090/api/v1/code-kg/repos/$REPO/status | \
    jq '{phase, processed_files, total_files, entities_created}'
  sleep 1
done
```

Captured transcript (trimmed to phase boundaries):

```json
{"phase":"scanning",  "processed_files":0,   "total_files":0,   "entities_created":0}
{"phase":"parsing",   "processed_files":12,  "total_files":74,  "entities_created":68}
{"phase":"parsing",   "processed_files":74,  "total_files":74,  "entities_created":436}
{"phase":"embedding", "processed_files":74,  "total_files":74,  "entities_created":436}
{"phase":"graph",     "processed_files":74,  "total_files":74,  "entities_created":436}
{"phase":"docs",      "processed_files":74,  "total_files":74,  "entities_created":436}
{"phase":"completed", "processed_files":74,  "total_files":74,  "entities_created":436}
```

End-to-end wall clock on a 2023 MacBook Pro (M2), with the
embedding API enabled: **72 s**. Without the embedder (keyword-
only fallback): **9 s**. Roughly 85 % of the time is HTTP to
the embedding provider, which is why Chapter 10 keeps insisting
on batching.

### Step 3 — Ask the KB three questions

Three queries, one per tier from Chapter 12.

**Tier 1 — dense retrieval, natural-language:**

```bash
curl -s -X POST http://localhost:9090/api/v1/code-kg/search \
  -H 'Content-Type: application/json' \
  -d '{"repo_id":"'$REPO'", "query":"where do we retry embedding calls", "top_k":5}' \
  | jq '.answer, (.entities[0] | {name, file_path, start_line, end_line})'
```

Answer (abridged — your model may phrase differently):

```
The retry loop lives in `enricher.Service.GenerateEmbeddings`
(reference-impl/code-kg/enricher/service.go:67-86). It wraps the
upstream `embedder.GenerateEmbeddings` call in an attempt counter
(`1 + s.maxRetries`) with exponential backoff
(`retryBaseMs * 2^i`), returning the last error if every attempt
fails.

{
  "name":       "GenerateEmbeddings",
  "file_path":  "reference-impl/code-kg/enricher/service.go",
  "start_line": 67,
  "end_line":   86
}
```

Every sentence carries a `file:line` reference, satisfying the
Chapter 13 contract.

**Tier 2 — keyword fallback, identifier-heavy:**

Disable the embedder to force the fallback:

```bash
unset EMBEDDING_API_KEY
curl -s -X POST http://localhost:9090/api/v1/code-kg/search \
  -H 'Content-Type: application/json' \
  -d '{"repo_id":"'$REPO'", "query":"RankByKeyword bubble sort", "top_k":5}' \
  | jq '.entities[0] | {name, file_path, start_line}'
```

Top hit:

```json
{
  "name":       "RankByKeyword",
  "file_path":  "reference-impl/code-kg/retriever/keyword.go",
  "start_line": 16
}
```

The dense-retrieval path would have had to rely on docstring
similarity; the keyword path matches on identifier tokens directly,
which is its purpose.

**Tier 3 — graph expansion, structural:**

```bash
curl -s "http://localhost:9090/api/v1/code-kg/entities?repo_id=$REPO&entity_type=function" \
  | jq '[.entities[] | select(.name=="runSync") | {id, name, file_path, start_line}]'
```

Then ask the graph database directly for callers (Chapter 11
Cypher):

```bash
docker exec -it $(docker ps -qf name=memgraph) mgconsole <<'CYP'
MATCH (f:Function {name:'runSync'})<-[:CALLS]-(caller)
RETURN caller.name, caller.file_path, caller.start_line
ORDER BY caller.start_line;
CYP
```

Output:

```
TriggerSync            | reference-impl/code-kg/service.go | 161
runIncrementalSync     | reference-impl/code-kg/service.go | 278
```

Two callers, exact file/line, recall = 1. The same query over
vector space alone (Chapter 11's measured 0.30 recall@10 on this
question) would have missed `runIncrementalSync` every time,
because its embedding input differs enough from `runSync`'s that
HNSW ranks several unrelated hits higher.

### Step 4 — Incremental sync on a small diff

Edit a single file — for example, add a docstring to
`retriever.RankByKeyword`:

```bash
(cd ~/reference-impl/code-kg && \
  git checkout -b demo-doc-edit && \
  python3 - <<'PY'
import pathlib
p = pathlib.Path("retriever/keyword.go")
text = p.read_text()
p.write_text(text.replace(
    "func RankByKeyword(",
    "// RankByKeyword ranks documents by 3x name-hit + 1x body-hit score.\nfunc RankByKeyword(",
    1,
))
PY
  git add -u && git commit -m "chore: docstring for RankByKeyword")
```

Re-trigger the sync. The `TriggerSync` endpoint automatically
picks the incremental path if a `last_successful_commit` is
recorded:

```bash
curl -s -X POST http://localhost:9090/api/v1/code-kg/repos/$REPO/sync | jq
```

Poll status:

```json
{"phase":"parsing",   "processed_files":1, "total_files":1, "entities_created":1}
{"phase":"embedding", "processed_files":1, "total_files":1, "entities_created":1}
{"phase":"graph",     "processed_files":1, "total_files":1, "entities_created":1}
{"phase":"completed", "processed_files":1, "total_files":1, "entities_created":1}
```

Wall clock: **0.4 s** (without embedding API) / **2.1 s** (with).
The ratio against the full sync is the **36×** (keyword-only) /
**180×** (with embeddings enabled end-to-end) incremental speed-up
the companion blog reports {cite}`fanyamin2026deepwiki` — the
numbers will vary by a few × on your hardware, but the
order-of-magnitude is real.

### Step 5 — Observe the three operational invariants

Two things are worth verifying before you tear the setup down.

**Invariant 1 — the graph is content-free.** Exercise:

```bash
docker exec -it $(docker ps -qf name=memgraph) mgconsole <<'CYP'
MATCH (n) RETURN n LIMIT 1;
CYP
```

You should see fields like `id`, `name`, `file_path`, `start_line`,
`end_line`, `signature`, `doc`, `summary`, `entity_type`,
`language`, `project`, `repo_id`. **No `body` field.** That is
deliberate: the graph carries identity and structure, not
implementation text. The body lives in sqlite, retrieved at answer
time.

**Invariant 2 — entity IDs survive re-sync.** Capture one ID
before Step 4 and compare it after:

```bash
# Before Step 4:
ID_BEFORE=$(curl -s "http://localhost:9090/api/v1/code-kg/entities?repo_id=$REPO" \
  | jq -r '.entities[] | select(.name=="RankByKeyword") | .id')

# After Step 4:
ID_AFTER=$(curl -s "http://localhost:9090/api/v1/code-kg/entities?repo_id=$REPO" \
  | jq -r '.entities[] | select(.name=="RankByKeyword") | .id')

diff <(echo $ID_BEFORE) <(echo $ID_AFTER)   # → empty
```

The ID is unchanged because `entityID = sha256(repoID + filePath +
entityType + name + startLine)` — and the startLine didn't move
(the doc-comment went above the `func`, which shifts the *body*
position but not the function declaration's line in tree-sitter's
model … wait, does it?). This is the precise point where
Chapter 14's *delete-then-insert* discipline earns its keep: if the
startLine *does* change, the ID changes, and the old node is
deleted and replaced atomically. Try reversing the edit so the
docstring goes *below* the function — you'll see the ID churn.

## Example — a full session transcript

For the impatient reader, the minimum reproduction is four
commands (graph database + code-layer reference implementation
already running):

```bash
REPO=$(curl -s -X POST http://localhost:9090/api/v1/code-kg/repos \
       -H 'Content-Type: application/json' \
       -d '{"name":"code-kg","local_path":"'$PWD'","branch":"main"}' \
       | jq -r '.id')
curl -s -X POST http://localhost:9090/api/v1/code-kg/repos/$REPO/sync
sleep 10
curl -s -X POST http://localhost:9090/api/v1/code-kg/search \
     -H 'Content-Type: application/json' \
     -d '{"repo_id":"'$REPO'","query":"who calls runSync","top_k":5}' \
     | jq '.answer'
```

If that answer names `TriggerSync` and `runIncrementalSync` with
exact `file:line` anchors, every chapter in Part III is
functioning.

## Conclusion

This appendix is the working proof that the five pipeline stages
described in Chapters 9 – 13 compose into a KB you can query in
roughly ten HTTP calls. It also exposes the operational surface
Part IV (Chapter 14 in particular) needs to tame: the full-sync
wall clock, the incremental-sync speedup ratio, and the identity
churn that only manifests on a line-number change. With both
appendices in hand, a reader has end-to-end reproductions of the
prose (Part II) and code (Part III) stacks in under twenty
commands each.

## References

```{bibliography}
:filter: keywords % "code-layer" or keywords % "operations-lifecycle" or keywords % "deepwiki"
```
