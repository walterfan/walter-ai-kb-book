#!/usr/bin/env python3
"""Enforce the blog non-copy policy.

Reads the vendored blog snapshot under
`source/sources/blog-deepwiki-methodology/snapshot.html`, extracts the
plain text, and scans every chapter under `book/` for any contiguous
verbatim span of ≥ MIN_RUN characters that also appears in the blog text
and is NOT inside a fenced quote block whose caption contains a {cite} to
`fanyamin2026deepwiki`.

Non-zero exit => build fails. Integrates into `make book-build` and CI.

If the snapshot does not exist yet (early scaffolding phase), the script
exits 0 with a warning so the build can still run.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

MIN_RUN = 80  # characters, matches specs/book-authoring/spec.md

BOOK_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = BOOK_ROOT / "sources" / "blog-deepwiki-methodology" / "snapshot.html"
OUTLINE = BOOK_ROOT / "sources" / "blog-deepwiki-methodology" / "outline.md"

SKIP_PREFIXES = (
    BOOK_ROOT / "_build",
    BOOK_ROOT / "_tools",
    BOOK_ROOT / "_static",
    BOOK_ROOT / "sources",
    BOOK_ROOT / "examples",
    BOOK_ROOT / "locale",
    BOOK_ROOT / ".venv",
    BOOK_ROOT / "venv",
    BOOK_ROOT / "node_modules",
)

CITE_RE = re.compile(r"\{cite\}`fanyamin2026deepwiki`")

try:
    from bs4 import BeautifulSoup  # type: ignore
except ImportError:
    BeautifulSoup = None


def read_declared_sha256() -> str | None:
    """Return the ``captured_sha256`` recorded in outline.md, or None."""
    if not OUTLINE.exists():
        return None
    raw = OUTLINE.read_text(encoding="utf-8")
    m = re.search(r"^captured_sha256:\s*([0-9a-fA-F]{64})\s*$", raw, re.M)
    return m.group(1).lower() if m else None


def verify_snapshot_integrity() -> str | None:
    """Compare the snapshot's SHA-256 to the value recorded in outline.md.

    Returns an error message on mismatch, or None on success / when the
    snapshot is absent (that is a warning, not an error).
    """
    if not SNAPSHOT.exists():
        return None
    declared = read_declared_sha256()
    if declared is None:
        return (
            f"snapshot exists but outline.md has no 'captured_sha256' "
            f"field; refusing to validate."
        )
    actual = hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest()
    if actual != declared:
        return (
            f"snapshot SHA-256 mismatch:\n"
            f"  declared (outline.md): {declared}\n"
            f"  actual   (snapshot.html): {actual}\n"
            f"The snapshot is supposed to be immutable. If you intentionally "
            f"re-captured it, open a separate openspec change to bump the "
            f"hash; do NOT edit outline.md silently."
        )
    return None


def load_snapshot_text() -> str | None:
    if not SNAPSHOT.exists():
        return None
    raw = SNAPSHOT.read_text(encoding="utf-8", errors="ignore")
    if BeautifulSoup is not None:
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
    else:
        text = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", text).strip()


def strip_code_fences(text: str) -> str:
    """Remove fenced code blocks and {epigraph}/{cite} quote blocks."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", "", text, flags=re.DOTALL)
    # Strip MyST admonition-style blocks that look like cited quotes.
    text = re.sub(
        r":::\{epigraph\}.*?:::",
        "",
        text,
        flags=re.DOTALL,
    )
    return text


def iter_runs(haystack: str, needle: str, n: int):
    """Yield every length-n substring of needle that appears in haystack."""
    seen: set[str] = set()
    for i in range(0, len(needle) - n + 1):
        run = needle[i : i + n]
        if run in seen:
            continue
        seen.add(run)
        if run in haystack:
            yield run


def main() -> int:
    integrity_err = verify_snapshot_integrity()
    if integrity_err is not None:
        print(f"FAIL  integrity: {integrity_err}", file=sys.stderr)
        return 1

    blog_text = load_snapshot_text()
    if blog_text is None:
        print(
            f"warning: {SNAPSHOT.relative_to(BOOK_ROOT)} not present yet; "
            "skipping blog-quote check.",
            file=sys.stderr,
        )
        return 0

    # Normalize whitespace so line wrapping does not defeat the check.
    blog_norm = re.sub(r"\s+", " ", blog_text)

    failures: list[tuple[Path, str]] = []

    for md in sorted(BOOK_ROOT.rglob("*.md")):
        if any(md.is_relative_to(p) for p in SKIP_PREFIXES):
            continue
        text = md.read_text(encoding="utf-8")
        stripped = strip_code_fences(text)
        # Also remove the frontmatter block itself.
        stripped = re.sub(r"^---\n.*?\n---\n", "", stripped, flags=re.DOTALL)
        if not stripped.strip():
            continue
        prose_norm = re.sub(r"\s+", " ", stripped)

        for run in iter_runs(blog_norm, prose_norm, MIN_RUN):
            # Allow the run if the chapter cites the blog nearby.
            # Nearby = same chapter, any location. (Stricter policies
            # could require proximity, but that is noisier for drafts.)
            if not CITE_RE.search(text):
                failures.append((md, run))
                break
            # If the chapter cites the blog, still fail if the long span
            # is not inside an explicit quote block.
            # Heuristic: the run must appear inside a line starting with
            # "> " (markdown blockquote) OR inside an {epigraph} block.
            if not any(
                line.lstrip().startswith(">")
                and run[:40] in " ".join(text.splitlines()[max(0, idx - 2): idx + 3])
                for idx, line in enumerate(text.splitlines())
                if run[:40] in line
            ):
                failures.append((md, run))
                break

    if failures:
        for path, run in failures:
            snippet = run[:60].replace("\n", " ")
            print(
                f"FAIL  {path.relative_to(BOOK_ROOT)}: long verbatim span "
                f"({len(run)} chars) also in blog snapshot: "
                f"{snippet!r}…",
                file=sys.stderr,
            )
        print(
            f"\n{len(failures)} file(s) violate the blog non-copy policy.",
            file=sys.stderr,
        )
        return 1

    print("OK — no long verbatim blog copies detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
