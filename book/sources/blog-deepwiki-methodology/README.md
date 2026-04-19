# blog-deepwiki-methodology

Vendored snapshot of the author's blog post:

> **给代码仓库造一个 DeepWiki：Tree-sitter + Embedding + 图谱 + LLM 的方法论**
> Walter Fan · 2026-04-17 · v1.2
> <https://www.fanyamin.com/gei-dai-ma-cang-ku-zao-yi-ge-deepwikitree-sitter-embedding-tu-pu-llm-de-fang-fa-lun.html>

## Files

| File | Purpose | Mutability |
|------|---------|------------|
| `snapshot.html` | Verbatim HTML capture of the blog at `captured_at`. | **Immutable.** Never edit after capture. |
| `outline.md` | Parsed section outline; used as a writing brief by chapters that cite the blog. | Mutable, but tracks section structure only. |
| `LICENSE.txt` | CC-BY-NC-ND 4.0 notice and author-permission statement. | Immutable. |

## Why vendored

The blog is the book's narrative spine (see `design.md` §D10b). Vendoring
it:

1. Pins the text to a known version so chapter citations stay meaningful
   even if the online post changes.
2. Lets `_tools/check_blog_quotes.py` scan chapter prose against the
   original and enforce the non-copy policy (no contiguous verbatim span
   of ≥ 80 chars outside a fenced `{epigraph}` + `{cite}` block).

## How to (re)capture the snapshot

This is a one-time operation. To re-capture (e.g., after a major blog
update the author explicitly wants to track), follow this sequence and
open a separate openspec change for it — the capture is deliberately
manual:

```bash
curl -fsSL \
  "https://www.fanyamin.com/gei-dai-ma-cang-ku-zao-yi-ge-deepwikitree-sitter-embedding-tu-pu-llm-de-fang-fa-lun.html" \
  -o book/sources/blog-deepwiki-methodology/snapshot.html

shasum -a 256 book/sources/blog-deepwiki-methodology/snapshot.html
# → paste the hash into outline.md's captured_sha256 field.
```

The CI validator refuses to build if `snapshot.html`'s current SHA-256
does not match `outline.md`'s `captured_sha256`.
