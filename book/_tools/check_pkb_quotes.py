#!/usr/bin/env python3
"""Enforce the PKB-skill non-copy and redaction policy.

Reads a curated pattern list from ``book/_tools/pkb_skill_patterns.txt``
and scans every markdown file under ``book/**`` for violations. See
``openspec/changes/pkb-skill-absorption/design.md`` §5 for the rationale.

Two pattern modes:

- ``forbid:<string>`` — ``<string>`` MUST NOT appear anywhere in any
  book markdown file. Enforces the redaction invariants (internal URLs,
  product names, CLI names, email domains).

- ``copy:<string>`` — ``<string>`` (length ≥ ``MIN_COPY_LEN``) MUST NOT
  appear verbatim in any book markdown file outside a paragraph that
  also contains ``{cite}`fanyamin_pkb_skill```. Guards against prose
  reproduction of distinctive skill strings.

Non-zero exit means build fails. Integrates into ``make book-build``
alongside ``check_blog_quotes.py`` and ``check_frontmatter.py``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_COPY_LEN = 40

BOOK_ROOT = Path(__file__).resolve().parent.parent
PATTERN_FILE = BOOK_ROOT / "_tools" / "pkb_skill_patterns.txt"

# Directories we don't scan. ``_tools`` is excluded because this file and
# the pattern file legitimately contain the forbidden strings; ``sources``
# holds the blog snapshot; build outputs and venvs are noise.
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

CITE_RE = re.compile(r"\{cite\}`fanyamin_pkb_skill`")


def parse_patterns(path: Path) -> tuple[list[str], list[str], list[str]]:
    """Return ``(forbid, copy, errors)`` pattern lists from ``path``.

    ``forbid`` entries are lowercased literals to match case-insensitively.
    ``copy`` entries are raw (case preserved) because prose matching is
    case-sensitive on purpose. ``errors`` collects malformed lines so we
    can warn without aborting.
    """
    if not path.exists():
        return [], [], [f"pattern file not found: {path}"]

    forbid: list[str] = []
    copy: list[str] = []
    errors: list[str] = []

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("forbid:"):
            value = line[len("forbid:"):].strip()
            if value:
                forbid.append(value.lower())
            else:
                errors.append(f"{path.name}:{lineno}: empty forbid: pattern")
        elif line.startswith("copy:"):
            value = line[len("copy:"):].strip()
            if len(value) < MIN_COPY_LEN:
                errors.append(
                    f"{path.name}:{lineno}: copy: pattern shorter than "
                    f"MIN_COPY_LEN ({len(value)} < {MIN_COPY_LEN}): {value!r}"
                )
            else:
                copy.append(value)
        else:
            errors.append(f"{path.name}:{lineno}: unrecognised line: {raw!r}")

    return forbid, copy, errors


def iter_markdown() -> list[Path]:
    """Yield every markdown file under BOOK_ROOT not under a SKIP_PREFIX."""
    out = []
    for md in sorted(BOOK_ROOT.rglob("*.md")):
        if any(md.is_relative_to(p) for p in SKIP_PREFIXES):
            continue
        out.append(md)
    return out


def check_forbid(text_lower: str, patterns: list[str]) -> list[str]:
    return [p for p in patterns if p in text_lower]


def check_copy(text: str, patterns: list[str]) -> list[str]:
    if not patterns:
        return []
    if CITE_RE.search(text):
        return []
    return [p for p in patterns if p in text]


def main() -> int:
    forbid, copy, pattern_errors = parse_patterns(PATTERN_FILE)
    for err in pattern_errors:
        print(f"WARN  {err}", file=sys.stderr)

    failures: list[tuple[Path, str, str]] = []

    for md in iter_markdown():
        text = md.read_text(encoding="utf-8")
        text_lower = text.lower()
        for hit in check_forbid(text_lower, forbid):
            failures.append((md, "forbid", hit))
        for hit in check_copy(text, copy):
            failures.append((md, "copy", hit))

    if failures:
        for path, kind, hit in failures:
            rel = path.relative_to(BOOK_ROOT)
            print(
                f"FAIL  {rel}: {kind} pattern matched: {hit!r}",
                file=sys.stderr,
            )
        print(
            f"\n{len(failures)} violation(s) of the PKB non-copy/redaction policy.",
            file=sys.stderr,
        )
        return 1

    total = len(forbid) + len(copy)
    print(f"OK — {total} PKB pattern(s) checked; no violations found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
