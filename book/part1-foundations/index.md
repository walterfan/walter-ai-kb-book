---
title: "Part I — Foundations"
status: draft
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - foundations
---

# Part I — Foundations

```{toctree}
:maxdepth: 1

ch01-why-kb-for-software
ch02-ir-rag-primer
ch03-diataxis-and-software-docs
```

## Why

Software teams accumulate fragmented knowledge — code, tickets, chats, design
docs, runbooks — faster than humans can curate it. Traditional documentation
cannot keep up. Part I establishes *what a software knowledge base is*, *why
AI changes the economics of building one*, and *what prior IR / RAG /
documentation research we will be standing on* throughout the rest of the
book.

## What

A working definition of "software knowledge base", a primer on the relevant
information-retrieval and retrieval-augmented-generation building blocks,
and the Diátaxis {cite}`procida_diataxis` doc-type model we will reuse when
classifying prose content.

## How

A short methodological overview of the book: three anchor sources (the
prose-layer reference implementation, the code-layer reference
implementation, and the author's methodology blog post
{cite}`fanyamin2026deepwiki`), the theory→practice ratio, and how each
Part applies the same Why → What → How → Example → Conclusion →
Reference arc.

## Example

A one-page walkthrough illustrating what "ask the KB" feels like once the
full stack is in place, deferring implementation details to later Parts.

## Conclusion

Part I gives the vocabulary and the reading order. It does not build
anything yet — that starts in Part II.

## References

```{bibliography}
:filter: keywords % "foundations"
```
