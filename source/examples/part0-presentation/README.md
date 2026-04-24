# Part 0 — Demo Scripts

Self-contained Python scripts for the three live demos in the
60-minute presentation (Part 0).  No external services required.

## Prerequisites

```bash
# From the repo root — installs the Poetry environment (if not done already)
make setup
```

Git must be installed (Demo 1 uses it to create a temporary repo).

## Demo 1 — Incremental Sync Simulation

Simulates `code-kg sync` (full vs. incremental) and prints a comparison
table with speedup ratios.

```bash
poetry run python source/examples/part0-presentation/demo1_incremental_sync.py
```

**What it shows:** stable entity IDs + three-layer filtering (L-git /
L-entity / L-link) let incremental sync skip 99% of the work.

## Demo 2 — Agent KB Query (MCP Simulation)

Simulates an MCP agent querying the KB with `kb.search`, `kb.read`, and
`kb.cite`.  Replays the "ingest pipeline + CSV" scenario from the talk,
then opens an interactive REPL.

```bash
poetry run python source/examples/part0-presentation/demo2_agent_kb_query.py
```

**What it shows:** the agent reads the PKB-metadata footer before citing
a page — `review_status` is a machine-readable trust signal, not just
metadata.

Interactive commands in the REPL:

| Command              | Description                     |
|:---------------------|:--------------------------------|
| `search <query>`     | `kb.search()` with TF-IDF      |
| `read <page_id>`     | `kb.read()` — body + footer     |
| `cite <query>`       | `kb.cite()` — file:line anchors |
| `pages`              | list all loaded KB pages        |
| `quit`               | exit                            |

## Demo 3 — Publish Gates

Creates intentionally broken KB pages and runs the 4 hard gates +
3 soft warnings.  Then fixes one issue and re-runs to show the
gate count drop.

```bash
poetry run python source/examples/part0-presentation/demo3_publish_gates.py
```

**What it shows:** "A KB is mature not when it has no errors, but when
errors get caught."  Publish gates turn rot into a machine-visible event.

## File layout

```
demo_repo/               10-file Go project (the "target repository")
kb_data/                  4 pre-seeded KB pages with frontmatter + footer
demo1_incremental_sync.py
demo2_agent_kb_query.py
demo3_publish_gates.py
README.md                 this file
```

## Cleanup

Demo 1 creates a temporary working directory at `_work/demo1/`.
To remove it:

```bash
rm -rf source/examples/part0-presentation/_work
```
