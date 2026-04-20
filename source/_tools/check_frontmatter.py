#!/usr/bin/env python3
"""Validate YAML frontmatter on every chapter and Part index under book/.

Enforces the fields required by specs/book-authoring/spec.md
"Per-chapter frontmatter": title, status, authors, last_verified_commit,
zh_status, keywords.

Exit code is non-zero if any file fails validation, so this script plugs
directly into `make book-build` and CI.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "PyYAML is required. Install with: pip install -r source/requirements.txt\n"
    )
    sys.exit(2)

BOOK_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FIELDS = (
    "title",
    "status",
    "authors",
    "last_verified_commit",
    "zh_status",
    "keywords",
)

ALLOWED_STATUS = {"draft", "review", "published"}
ALLOWED_ZH = {"none", "partial", "complete"}

# Files under these paths are not chapters and are skipped.
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


def extract_frontmatter(path: Path) -> tuple[dict | None, str]:
    """Return (frontmatter_dict_or_None, error_message_or_empty)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "missing YAML frontmatter (must start with '---')"
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return None, "unterminated YAML frontmatter (no closing '---')"
    raw = text[4:end]
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        return None, f"YAML parse error: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter must be a mapping"
    return data, ""


def validate(path: Path, fm: dict) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"missing required field: {field}")
    if "status" in fm and fm["status"] not in ALLOWED_STATUS:
        errors.append(
            f"status={fm['status']!r} not in {sorted(ALLOWED_STATUS)}"
        )
    if "zh_status" in fm and fm["zh_status"] not in ALLOWED_ZH:
        errors.append(
            f"zh_status={fm['zh_status']!r} not in {sorted(ALLOWED_ZH)}"
        )
    if "authors" in fm and not isinstance(fm["authors"], list):
        errors.append("authors must be a list")
    if "keywords" in fm and not isinstance(fm["keywords"], list):
        errors.append("keywords must be a list")
    return errors


def main() -> int:
    failures: list[tuple[Path, list[str]]] = []
    checked = 0

    for md in sorted(BOOK_ROOT.rglob("*.md")):
        if any(md.is_relative_to(p) for p in SKIP_PREFIXES):
            continue
        checked += 1
        fm, err = extract_frontmatter(md)
        if fm is None:
            failures.append((md, [err]))
            continue
        errs = validate(md, fm)
        if errs:
            failures.append((md, errs))

    rel = lambda p: p.relative_to(BOOK_ROOT)
    if failures:
        for path, errs in failures:
            for e in errs:
                print(f"FAIL  {rel(path)}: {e}", file=sys.stderr)
        print(
            f"\n{len(failures)} file(s) failed out of {checked} checked.",
            file=sys.stderr,
        )
        return 1

    print(f"OK — frontmatter valid in all {checked} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
