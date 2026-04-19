---
title: 'Part IV — Operations & Lifecycle'
status: draft
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - operations
---

# Part IV — Operations & Lifecycle

```{toctree}
:maxdepth: 1

ch14-incremental-sync
ch15-evaluation-and-benchmarks
ch16-maintenance-drift-and-link-rot
```

## Why

Keeping a code KB healthy is harder than building one.

## What

Git-diff-driven incremental sync, RAG evaluation, drift and link rot.

## How

Three chapters, anchored in blog §10 {cite}`fanyamin2026deepwiki` and in the `SyncJob` state machine.

## Example

A worked incremental-sync run reproducing the 36×/180×/9× speedups reported in the blog.

## Conclusion

Operations discipline is the line between a prototype KB and one a team actually relies on.

## References

```{bibliography}
:filter: keywords % "operations"
```
