#!/usr/bin/env python3
"""Demo 3 — Publish Gates.

Demonstrates the hard gates and soft warnings that block or flag KB pages
before publishing.  Uses intentionally broken pages to show each gate type.

The output format matches `make book-check` from the presentation:
  ✗ H<n>  <description>
  ⚠ S<n>  <description>
  → publish blocked: N hard, M soft

Usage:
    poetry run python source/examples/part0-presentation/demo3_publish_gates.py
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEMO_REPO = SCRIPT_DIR / "demo_repo"

# ── ANSI helpers ────────────────────────────────────────────────────

BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RED = "\033[31m"
DIM = "\033[2m"
RESET = "\033[0m"


def heading(text: str) -> None:
    print(f"\n{BOLD}{CYAN}{'─' * 60}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{BOLD}{CYAN}{'─' * 60}{RESET}\n")


# ── Test page generator ─────────────────────────────────────────────

GOOD_FOOTER = """\
<!-- PKB-metadata -->
<!-- layer: L2 -->
<!-- updated_by: human -->
<!-- review_status: approved -->
<!-- review_score: 4 -->
<!-- reviewed_by: alice -->
<!-- commit: a1b2c3d -->"""

PENDING_FOOTER = """\
<!-- PKB-metadata -->
<!-- layer: L3 -->
<!-- updated_by: ai -->
<!-- review_status: pending -->
<!-- review_score: 0 -->
<!-- reviewed_by: null -->
<!-- commit: a1b2c3d -->"""

BIB_ENTRIES = {"fanyamin2026deepwiki", "cormack2009rrf", "robertson2009bm25"}

PAGES: dict[str, str] = {
    "page-ok-1.md": f"""\
---
title: "A healthy page"
---

# Healthy Page

Everything is fine here. Reference: `service.go:32`.

{GOOD_FOOTER}
""",
    "page-ok-2.md": f"""\
---
title: "Another healthy page"
---

# Another Healthy Page

This page is also fine. See `config.go:10`.

{GOOD_FOOTER}
""",
    "page-no-footer.md": """\
---
title: "Missing footer"
---

# Page Without Footer

This page has no metadata footer at all.
""",
    "page-broken-anchor.md": f"""\
---
title: "Broken file:line anchor"
---

# Broken Anchor

See the implementation at `service.go:9999` — this line does not exist.

{GOOD_FOOTER}
""",
    "page-todo.md": f"""\
---
title: "Page with TODO"
---

# Work in Progress

[TODO] Add the detailed explanation here.

[FIXME] The diagram below is wrong.

{PENDING_FOOTER}
""",
    "page-bad-cite.md": f"""\
---
title: "Undefined cite key"
---

# Bad Citation

As shown in {{cite}}`huang2024graphpagerank`, the algorithm works.

{PENDING_FOOTER}
""",
    "page-pending-1.md": f"""\
---
title: "AI draft 1"
---

# AI-Generated Summary

This was written by LLM and not reviewed.

{PENDING_FOOTER}
""",
    "page-pending-2.md": f"""\
---
title: "AI draft 2"
---

# AI-Generated Overview

Another AI draft awaiting human review.

{PENDING_FOOTER}
""",
}


# ── Gate implementations ────────────────────────────────────────────

class GateResult:
    def __init__(self, code: str, page: str, message: str, hard: bool):
        self.code = code
        self.page = page
        self.message = message
        self.hard = hard

    def __str__(self) -> str:
        icon = f"{RED}✗{RESET}" if self.hard else f"{YELLOW}⚠{RESET}"
        tag = f"{RED}{self.code}{RESET}" if self.hard else f"{YELLOW}{self.code}{RESET}"
        return f"  {icon} {tag}  {self.page}: {self.message}"


def check_h1_footer(name: str, text: str) -> GateResult | None:
    if "<!-- PKB-metadata -->" not in text and "<!-- layer:" not in text:
        return GateResult("H1", name, "missing PKB-metadata footer", hard=True)
    return None


def check_h2_anchors(name: str, text: str, repo_root: Path) -> list[GateResult]:
    results = []
    for m in re.finditer(r"`([a-zA-Z_/]+\.go):(\d+)`", text):
        file_path = repo_root / m.group(1)
        line_num = int(m.group(2))
        if not file_path.exists():
            results.append(GateResult(
                "H2", name,
                f"broken file:line anchor: {m.group(1)}:{m.group(2)} (file not found)",
                hard=True))
        else:
            lines = file_path.read_text().splitlines()
            if line_num > len(lines):
                results.append(GateResult(
                    "H2", name,
                    f"broken file:line anchor: {m.group(1)}:{m.group(2)} "
                    f"(file has only {len(lines)} lines)",
                    hard=True))
    return results


def check_h3_placeholders(name: str, text: str) -> list[GateResult]:
    results = []
    for pattern in [r"\[TODO\]", r"\[FIXME\]"]:
        for m in re.finditer(pattern, text):
            results.append(GateResult(
                "H3", name,
                f"placeholder found: {m.group()}", hard=True))
    return results


def check_h4_cite_keys(name: str, text: str, valid_keys: set[str]) -> list[GateResult]:
    results = []
    for m in re.finditer(r"\{cite\}`(\w+)`", text):
        key = m.group(1)
        if key not in valid_keys:
            results.append(GateResult(
                "H4", name,
                f"undefined cite key: {{cite}}`{key}`", hard=True))
    return results


def check_s1_pending(pages: dict[str, str], threshold: int = 3) -> GateResult | None:
    pending = sum(1 for t in pages.values() if "review_status: pending" in t)
    if pending > threshold:
        return GateResult(
            "S1", "(global)",
            f"{pending} pages have review_status=pending (threshold: {threshold})",
            hard=False)
    return None


def check_s3_stale_commit(name: str, text: str) -> GateResult | None:
    if "last_verified_commit" not in text:
        return GateResult(
            "S3", name,
            "no last_verified_commit in frontmatter", hard=False)
    return None


def check_s5_l1_ratio(pages: dict[str, str], threshold: float = 0.20) -> GateResult | None:
    total = len(pages)
    if total == 0:
        return None
    l1_count = sum(1 for t in pages.values() if "layer: L1" in t)
    ratio = l1_count / total
    if ratio < threshold:
        return GateResult(
            "S5", "(global)",
            f"L1 ratio: {ratio:.0%} (threshold: {threshold:.0%})",
            hard=False)
    return None


# ── Gate runner ─────────────────────────────────────────────────────

def run_gates(pages_dir: Path, repo_root: Path) -> list[GateResult]:
    pages: dict[str, str] = {}
    for md in sorted(pages_dir.glob("*.md")):
        pages[md.name] = md.read_text()

    results: list[GateResult] = []

    for name, text in pages.items():
        r = check_h1_footer(name, text)
        if r:
            results.append(r)
        results.extend(check_h2_anchors(name, text, repo_root))
        results.extend(check_h3_placeholders(name, text))
        results.extend(check_h4_cite_keys(name, text, BIB_ENTRIES))

    r = check_s1_pending(pages)
    if r:
        results.append(r)
    for name, text in pages.items():
        r = check_s3_stale_commit(name, text)
        if r:
            results.append(r)
    r = check_s5_l1_ratio(pages)
    if r:
        results.append(r)

    return results


def print_results(results: list[GateResult]) -> None:
    hard = [r for r in results if r.hard]
    soft = [r for r in results if not r.hard]

    for r in results:
        print(str(r))

    print()
    if hard:
        print(f"  {RED}→ publish blocked: {len(hard)} hard, {len(soft)} soft{RESET}")
    elif soft:
        print(f"  {YELLOW}→ publish allowed with {len(soft)} warning(s){RESET}")
    else:
        print(f"  {GREEN}→ all gates passed{RESET}")


# ── Main ────────────────────────────────────────────────────────────

def main() -> int:
    heading("Demo 3 — Publish Gates")

    tmp = Path(tempfile.mkdtemp(prefix="kb-gates-"))
    try:
        pages_dir = tmp / "pages"
        pages_dir.mkdir()
        for name, content in PAGES.items():
            (pages_dir / name).write_text(content)

        print(f"  Created {len(PAGES)} test pages in {pages_dir}\n")
        print(f"  {DIM}Intentional defects:{RESET}")
        print(f"    • page-no-footer.md    — missing PKB-metadata (H1)")
        print(f"    • page-broken-anchor.md — service.go:9999 (H2)")
        print(f"    • page-todo.md         — [TODO] and [FIXME] (H3)")
        print(f"    • page-bad-cite.md     — undefined cite key (H4)")
        print(f"    • 4 pages pending      — exceeds threshold of 3 (S1)")
        print(f"    • 0 L1 pages           — ratio below 20% (S5)")

        heading("Running gates...")
        results = run_gates(pages_dir, DEMO_REPO)
        print_results(results)

        # Now fix one issue and re-run to show the count drop
        heading("Fix: adding footer to page-no-footer.md")
        broken = pages_dir / "page-no-footer.md"
        broken.write_text(broken.read_text() + "\n" + PENDING_FOOTER + "\n")
        print(f"  {GREEN}Added PKB-metadata footer{RESET}")

        heading("Re-running gates...")
        results2 = run_gates(pages_dir, DEMO_REPO)
        print_results(results2)

        hard_before = sum(1 for r in results if r.hard)
        hard_after = sum(1 for r in results2 if r.hard)
        print(f"\n  Hard gate count: {RED}{hard_before}{RESET} → {YELLOW}{hard_after}{RESET}")

        heading("Key takeaway")
        print(f'  {YELLOW}"A KB is mature not when it has no errors,')
        print(f'  but when errors get caught."{RESET}')
        print(f'\n  Publish gates turn "rot" into a {BOLD}machine-visible event{RESET}.')
        print()

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
