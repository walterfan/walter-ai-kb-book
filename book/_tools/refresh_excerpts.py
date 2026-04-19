#!/usr/bin/env python3
"""Vendor code excerpts from the two anchor repos into ``book/examples/``.

Driven by the manifest ``book/_tools/excerpts.yaml``. Each entry names a
source repo (one of the keys in ``KNOWN_REPOS`` below — these map to the
author's private working copies and are **never** written into vendored
output; see ``DISPLAY_REPO_NAMES`` / ``DISPLAY_PATH_PREFIX`` for the
anonymised values that land in provenance headers). This tool:

1.  Reads the source file.
2.  Computes SHA-256 of the source contents and — when the source repo has
    at least one commit — resolves the current ``HEAD`` SHA via ``git``.
3.  Writes a provenance header (comment block appropriate to the source
    file's language) followed by the verbatim file body, to the destination.
4.  Regenerates ``book/examples/SOURCE.md`` with one row per captured
    excerpt.

The provenance header is the *only* thing that differs from the upstream
file, so a reviewer can verify authenticity with ``diff`` plus the recorded
SHA-256.

Usage:
    python3 book/_tools/refresh_excerpts.py              # refresh all
    python3 book/_tools/refresh_excerpts.py --check      # verify only

Called from ``make book-refresh-excerpts``.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML is required. Install with: pip install -r book/requirements.txt\n"
    )
    sys.exit(2)

BOOK_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = BOOK_ROOT.parent
MANIFEST = BOOK_ROOT / "_tools" / "excerpts.yaml"
EXAMPLES_DIR = BOOK_ROOT / "examples"
SOURCE_MD = EXAMPLES_DIR / "SOURCE.md"

# Repos we are allowed to pull excerpts from, mapped to an absolute path on
# the author's machine. Sibling-repo paths are computed lazily so CI can set
# LAZY_AI_CODER_PATH to wire them up.
KNOWN_REPOS = {
    "lazy-rabbit-wiki": REPO_ROOT,
    "lazy-ai-coder": Path(
        os.environ.get("LAZY_AI_CODER_PATH", REPO_ROOT.parent / "lazy-ai-coder")
    ),
}

# Public, anonymised names for the two reference implementations. Whatever
# the author's working copy is called, these are the only names that reach
# vendored provenance headers, SOURCE.md, or any Sphinx-rendered artefact.
# If you add a new source repo to KNOWN_REPOS, add a display mapping here
# and a path-prefix mapping below, or the build's redaction check will
# fail on the private name.
DISPLAY_REPO_NAMES = {
    "lazy-rabbit-wiki": "prose-layer-reference-impl",
    "lazy-ai-coder":    "code-layer-reference-impl",
}

# Source-path prefixes to rewrite when they land in provenance headers.
# The left-hand side is whatever the author's checkout uses internally;
# the right-hand side is the anonymised prefix the reader sees. Applied in
# declaration order, first match wins.
DISPLAY_PATH_PREFIX: list[tuple[str, str]] = [
    ("internal/codekg/", "reference-impl/code-kg/"),
    ("backend/internal/wiki/", "reference-impl/prose-wiki/"),
    ("wiki-template/", "reference-impl/prose-wiki-template/"),
]


def _display_repo(name: str) -> str:
    return DISPLAY_REPO_NAMES.get(name, name)


def _display_path(path: str) -> str:
    for src, dst in DISPLAY_PATH_PREFIX:
        if path.startswith(src):
            return dst + path[len(src):]
    return path


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def git_head(repo: Path) -> str:
    """Return the short commit SHA of ``repo``'s HEAD, or ``"working-tree"``.

    Returns ``"working-tree"`` if the repo has no commits yet or if ``git``
    is not available. Never raises.
    """
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return "working-tree"
    sha = out.stdout.strip()
    return sha if out.returncode == 0 and sha else "working-tree"


def git_is_dirty(repo: Path, path: Path) -> bool:
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--", str(path)],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return False
    return bool(out.stdout.strip())


# ---------------------------------------------------------------------------
# Language → comment style
# ---------------------------------------------------------------------------


# Keys are file suffixes; values are ("line_prefix", "block_start", "block_end").
# Block comments win where available because they keep the provenance block
# visually distinct from the code.
COMMENT_STYLES: dict[str, tuple[str, str, str]] = {
    ".go":   ("// ", "/* ", " */"),
    ".ts":   ("// ", "/* ", " */"),
    ".tsx":  ("// ", "/* ", " */"),
    ".js":   ("// ", "/* ", " */"),
    ".java": ("// ", "/* ", " */"),
    ".c":    ("// ", "/* ", " */"),
    ".cc":   ("// ", "/* ", " */"),
    ".cpp":  ("// ", "/* ", " */"),
    ".h":    ("// ", "/* ", " */"),
    ".py":   ("# ",  '"""', '"""'),
    ".rs":   ("// ", "/* ", " */"),
    ".sh":   ("# ", "", ""),
    ".yaml": ("# ", "", ""),
    ".yml":  ("# ", "", ""),
    ".toml": ("# ", "", ""),
    ".md":   ("<!-- ", "<!--", "-->"),
    ".sql":  ("-- ", "/* ", " */"),
}


def provenance_header(
    source_repo: str,
    source_path: str,
    commit_sha: str,
    captured_at: str,
    content_sha256: str,
    suffix: str,
    dirty: bool,
) -> str:
    """Return a language-appropriate provenance block for a file.

    Always placed at the top of the vendored file, before any body content.
    """
    lines = [
        "BOOK EXCERPT — vendored for citation, do not hand-edit",
        f"source_repo:     {_display_repo(source_repo)}",
        f"source_path:     {_display_path(source_path)}",
        f"commit_sha:      {commit_sha}" + ("  (dirty — uncommitted changes)" if dirty else ""),
        f"captured_at:     {captured_at}",
        f"content_sha256:  {content_sha256}",
        "regenerate with: make book-refresh-excerpts",
    ]
    line_prefix, block_start, block_end = COMMENT_STYLES.get(
        suffix, ("# ", "", "")
    )
    if block_start and block_end:
        body = "\n".join(line_prefix.strip() + " " + l for l in lines)
        return f"{block_start}\n{body}\n{block_end}\n\n"
    return "\n".join(line_prefix + l for l in lines) + "\n\n"


# ---------------------------------------------------------------------------
# Main capture loop
# ---------------------------------------------------------------------------


_SHA_IN_HEADER = re.compile(rb"content_sha256:\s*([0-9a-f]{64})")
_COMMIT_IN_HEADER = re.compile(rb"commit_sha:\s*([^\s]+(?:\+dirty)?)")
_CAPTURED_IN_HEADER = re.compile(rb"captured_at:\s*([0-9T:\-Z]+)")


def previous_metadata(dst: Path) -> tuple[str | None, str | None, str | None]:
    """Return ``(content_sha256, commit_display, captured_at)`` previously
    recorded in ``dst``'s provenance header, or ``None`` components when the
    file is missing or lacks a field. ``commit_display`` includes any
    ``+dirty`` suffix that was present.
    """
    if not dst.exists():
        return None, None, None
    head = dst.read_bytes()[:4096]
    sha_m = _SHA_IN_HEADER.search(head)
    commit_m = _COMMIT_IN_HEADER.search(head)
    captured_m = _CAPTURED_IN_HEADER.search(head)
    # commit_sha line also carries the "(dirty — ...)" annotation, but the
    # regex stops at the first whitespace. Re-apply the +dirty suffix if
    # present anywhere later on the same line.
    commit = commit_m.group(1).decode() if commit_m else None
    if commit and b"(dirty" in head and not commit.endswith("+dirty"):
        commit = commit + "+dirty"
    return (
        sha_m.group(1).decode() if sha_m else None,
        commit,
        captured_m.group(1).decode() if captured_m else None,
    )


def capture_one(entry: dict, captured_at: str, check_only: bool) -> dict:
    repo_name = entry["source_repo"]
    if repo_name not in KNOWN_REPOS:
        raise SystemExit(f"unknown source_repo: {repo_name}")
    repo_root = KNOWN_REPOS[repo_name]
    if not repo_root.exists():
        raise SystemExit(
            f"source repo {repo_name} not found at {repo_root}. "
            f"Set LAZY_AI_CODER_PATH if the sibling repo lives elsewhere."
        )

    src = repo_root / entry["source_path"]
    if not src.exists():
        raise SystemExit(f"source file not found: {src}")
    body = src.read_bytes()
    content_sha = hashlib.sha256(body).hexdigest()
    commit = git_head(repo_root)
    dirty = git_is_dirty(repo_root, src) if commit != "working-tree" else True
    commit_display = commit + ("+dirty" if dirty else "")

    dst = BOOK_ROOT / "examples" / entry["excerpt_path"]
    prev_sha, prev_commit, prev_captured = previous_metadata(dst)

    # Treat the excerpt as up-to-date iff content SHA-256 and commit SHA
    # both match what's already recorded on disk. captured_at and dirty-flag
    # alone must not trigger a rewrite — that would break idempotency.
    up_to_date = (
        dst.exists() and prev_sha == content_sha and prev_commit == commit_display
    )

    result = {
        "excerpt_path": entry["excerpt_path"],
        "source_repo": _display_repo(repo_name),
        "source_path": _display_path(entry["source_path"]),
        "commit_sha": commit_display,
        # When the excerpt is up-to-date, reuse the previously recorded
        # capture time so SOURCE.md stays byte-stable across reruns.
        "captured_at": prev_captured if up_to_date and prev_captured else captured_at,
        "content_sha256": content_sha,
        "changed": False,
    }

    if up_to_date:
        return result

    if check_only:
        result["changed"] = True
        result["reason"] = "missing" if not dst.exists() else "out-of-date"
        return result

    suffix = src.suffix
    header = provenance_header(
        source_repo=repo_name,
        source_path=entry["source_path"],
        commit_sha=commit,
        captured_at=captured_at,
        content_sha256=content_sha,
        suffix=suffix,
        dirty=dirty,
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(header.encode("utf-8") + body)
    result["changed"] = True
    return result


def write_source_md(rows: list[dict]) -> None:
    rows = sorted(rows, key=lambda r: r["excerpt_path"])
    lines = [
        "# Excerpt Source Registry",
        "",
        "Auto-generated by `make book-refresh-excerpts`. Do not hand-edit.",
        "",
        "| excerpt_path | source_repo | source_path | commit_sha | captured_at | content_sha256 |",
        "|--------------|-------------|-------------|------------|-------------|----------------|",
    ]
    for r in rows:
        lines.append(
            f"| `{r['excerpt_path']}` "
            f"| {r['source_repo']} "
            f"| `{r['source_path']}` "
            f"| `{r['commit_sha']}` "
            f"| {r['captured_at']} "
            f"| `{r['content_sha256'][:12]}…` |"
        )
    lines += [
        "",
        "## Conventions",
        "",
        "- Every vendored file opens with a provenance comment block listing",
        "  `source_repo`, `source_path`, `commit_sha`, `captured_at`, and",
        "  `content_sha256`. A reviewer can verify authenticity with `diff`",
        "  and the recorded SHA-256.",
        "- `commit_sha` of `working-tree` means the source repo had no",
        "  commits at capture time; of `<sha>+dirty` means the source file had",
        "  uncommitted changes at capture time.",
        "- Re-capture with `make book-refresh-excerpts`. The tool is",
        "  idempotent: re-running without source changes is a no-op.",
        "",
    ]
    SOURCE_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify that every excerpt is up-to-date; exit non-zero if not.",
    )
    args = parser.parse_args()

    if not MANIFEST.exists():
        print(
            f"warning: {MANIFEST.relative_to(BOOK_ROOT)} not present yet; "
            "nothing to refresh.",
            file=sys.stderr,
        )
        return 0

    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    entries = manifest.get("excerpts", [])
    if not entries:
        print("no excerpts declared in manifest; nothing to do.")
        return 0

    captured_at = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    rows: list[dict] = []
    any_changed = False
    for entry in entries:
        r = capture_one(entry, captured_at, check_only=args.check)
        rows.append(r)
        if r.get("changed"):
            any_changed = True
            if args.check:
                print(
                    f"OUT-OF-DATE {r['excerpt_path']} ({r.get('reason')})",
                    file=sys.stderr,
                )
            else:
                print(f"captured    {r['excerpt_path']}")
        else:
            if not args.check:
                print(f"unchanged   {r['excerpt_path']}")

    if args.check:
        if any_changed:
            print(
                "\nExcerpts are out of date. Run `make book-refresh-excerpts` "
                "and commit the result.",
                file=sys.stderr,
            )
            return 1
        print(f"OK — {len(rows)} excerpt(s) match their sources.")
        return 0

    write_source_md(rows)
    print(f"\nWrote {SOURCE_MD.relative_to(BOOK_ROOT)} with {len(rows)} row(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
