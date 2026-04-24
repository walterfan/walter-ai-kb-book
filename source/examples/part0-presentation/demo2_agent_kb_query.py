#!/usr/bin/env python3
"""Demo 2 — Agent KB Query Simulation.

Simulates an MCP-style agent querying the knowledge base with three tools:
  kb.search(query, k, filter)  →  ranked pages
  kb.read(page_id)             →  body + frontmatter + footer
  kb.cite(query, k)            →  file:line anchors

Replays the "ingest pipeline + CSV" scenario from the Part 0 presentation,
then opens an interactive REPL.

Usage:
    poetry run python source/examples/part0-presentation/demo2_agent_kb_query.py
"""

from __future__ import annotations

import json
import math
import re
import readline  # noqa: F401  — enables arrow-key history in input()
import sys
import textwrap
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
KB_DIR = SCRIPT_DIR / "kb_data"

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


def mcp_call(tool: str, params: dict) -> None:
    print(f"  {DIM}→ MCP call:{RESET}  {BOLD}{tool}{RESET}")
    for k, v in params.items():
        print(f"    {DIM}{k}:{RESET} {v}")


def mcp_result(data: str) -> None:
    for line in data.strip().splitlines():
        print(f"    {GREEN}{line}{RESET}")


def agent_says(text: str) -> None:
    wrapped = textwrap.fill(text, width=72, initial_indent="  🤖 ",
                            subsequent_indent="     ")
    print(f"\n{BOLD}{wrapped}{RESET}\n")


# ── Page model ──────────────────────────────────────────────────────

class Page:
    def __init__(self, page_id: str, title: str, body: str,
                 frontmatter: dict, footer: dict):
        self.page_id = page_id
        self.title = title
        self.body = body
        self.frontmatter = frontmatter
        self.footer = footer
        self._tokens = Counter(re.findall(r"[a-z_]+", body.lower()))

    def tfidf_score(self, query_tokens: list[str], idf: dict[str, float]) -> float:
        score = 0.0
        for t in query_tokens:
            tf = self._tokens.get(t, 0)
            score += tf * idf.get(t, 0)
        return score


# ── KB engine ───────────────────────────────────────────────────────

class KnowledgeBase:
    def __init__(self, pages: list[Page]):
        self.pages = {p.page_id: p for p in pages}
        doc_count = len(pages)
        all_tokens: set[str] = set()
        for p in pages:
            all_tokens |= set(p._tokens.keys())
        self._idf: dict[str, float] = {}
        for t in all_tokens:
            df = sum(1 for p in pages if t in p._tokens)
            self._idf[t] = math.log((doc_count + 1) / (df + 1))

    def search(self, query: str, k: int = 5,
               filter_expr: str | None = None) -> list[dict]:
        tokens = re.findall(r"[a-z_]+", query.lower())
        scored = []
        for p in self.pages.values():
            if filter_expr and not self._matches_filter(p, filter_expr):
                continue
            s = p.tfidf_score(tokens, self._idf)
            if s > 0:
                scored.append((s, p))
        scored.sort(key=lambda x: -x[0])
        results = []
        for score, p in scored[:k]:
            results.append({
                "page_id": p.page_id,
                "score": round(score, 3),
                "tuple": self._format_tuple(p),
                "snippet": p.body[:120].replace("\n", " ") + "...",
            })
        return results

    def read(self, page_id: str) -> dict | None:
        p = self.pages.get(page_id)
        if not p:
            return None
        return {
            "page_id": p.page_id,
            "title": p.title,
            "body": p.body,
            "frontmatter": p.frontmatter,
            "footer": p.footer,
        }

    def cite(self, query: str, k: int = 3) -> list[dict]:
        tokens = re.findall(r"[a-z_]+", query.lower())
        file_line_re = re.compile(r"(`[a-zA-Z_/]+\.go:\d+`)")
        results = []
        scored = []
        for p in self.pages.values():
            s = p.tfidf_score(tokens, self._idf)
            if s > 0:
                scored.append((s, p))
        scored.sort(key=lambda x: -x[0])
        for _, p in scored:
            for m in file_line_re.finditer(p.body):
                anchor = m.group(1).strip("`")
                results.append({"page_id": p.page_id, "file_line": anchor})
                if len(results) >= k:
                    return results
        return results

    def _matches_filter(self, page: Page, expr: str) -> bool:
        if "==" in expr:
            field, value = expr.split("==", 1)
            field, value = field.strip(), value.strip()
            return page.footer.get(field) == value
        return True

    def _format_tuple(self, p: Page) -> str:
        f = p.footer
        return (f"<{f.get('layer', '?')}, {f.get('updated_by', '?')}, "
                f"{f.get('review_status', '?')}, {f.get('review_score', '?')}>")


# ── Page loader ─────────────────────────────────────────────────────

def load_pages(kb_dir: Path) -> list[Page]:
    pages = []
    for md in sorted(kb_dir.glob("*.md")):
        text = md.read_text()
        fm, body, footer = parse_page(text)
        page_id = md.stem
        pages.append(Page(
            page_id=page_id,
            title=fm.get("title", page_id),
            body=body,
            frontmatter=fm,
            footer=footer,
        ))
    return pages


def parse_page(text: str) -> tuple[dict, str, dict]:
    frontmatter: dict = {}
    footer: dict = {}
    body = text

    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        fm_raw = text[4:end]
        body = text[end + 5:]
        for line in fm_raw.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                frontmatter[k.strip()] = v.strip().strip('"')

    for m in re.finditer(r"<!--\s*(\w+):\s*(.+?)\s*-->", text):
        key, val = m.group(1), m.group(2)
        footer[key] = val

    return frontmatter, body.strip(), footer


# ── Scripted scenario ───────────────────────────────────────────────

def run_scripted_scenario(kb: KnowledgeBase) -> None:
    heading("Scripted scenario — ingest pipeline + CSV")

    print(f"  {BOLD}08:15{RESET}  Developer asks:")
    print(f'         {CYAN}"ingest pipeline 是怎么处理 CSV 的?"{RESET}\n')

    mcp_call("kb.search", {
        "query": "ingest pipeline CSV",
        "k": 5,
        "filter": "review_status==approved",
    })
    results = kb.search("ingest pipeline CSV", k=5,
                        filter_expr="review_status==approved")
    mcp_result(json.dumps(results, indent=2, ensure_ascii=False))

    if results:
        top = results[0]
        print(f"\n  {DIM}Agent picks top result: {top['page_id']} "
              f"(score={top['score']}, tuple={top['tuple']}){RESET}\n")

        mcp_call("kb.read", {"page_id": top["page_id"]})
        page = kb.read(top["page_id"])
        if page:
            footer = page["footer"]
            status_color = GREEN if footer.get("review_status") == "approved" else RED
            mcp_result(f"title: {page['title']}")
            mcp_result(f"footer.review_status: "
                       f"{status_color}{footer.get('review_status', '?')}{GREEN}")
            mcp_result(f"footer.layer: {footer.get('layer', '?')}")
            mcp_result(f"body: {page['body'][:200]}...")

        agent_says(f"The ingest pipeline is described in {top['page_id']}. "
                   f"CSV files are parsed by the CSVLoader, which supports "
                   f"custom delimiters and header detection. Records then pass "
                   f"through a Transformer pipeline for normalisation.")

    print(f"\n  {BOLD}08:17{RESET}  Developer follows up:")
    print(f'         {CYAN}"具体是哪个文件 parse 的 CSV？"{RESET}\n')

    mcp_call("kb.cite", {"query": "CSV parsing", "k": 3})
    citations = kb.cite("CSV parsing", k=3)
    mcp_result(json.dumps(citations, indent=2, ensure_ascii=False))

    if citations:
        top_cite = citations[0]
        agent_says(f"{top_cite['file_line']} — this is the CSV loader's "
                   f"entry point, the parseCSV function. "
                   f"(source: {top_cite['page_id']})")


# ── Interactive REPL ────────────────────────────────────────────────

def run_repl(kb: KnowledgeBase) -> None:
    heading("Interactive REPL — type a query, or 'quit' to exit")
    print(f"  Available commands:")
    print(f"    {CYAN}search <query>{RESET}        — kb.search()")
    print(f"    {CYAN}read <page_id>{RESET}         — kb.read()")
    print(f"    {CYAN}cite <query>{RESET}           — kb.cite()")
    print(f"    {CYAN}pages{RESET}                  — list all pages")
    print(f"    {CYAN}quit{RESET}                   — exit")
    print()

    while True:
        try:
            raw = input(f"  {BOLD}kb>{RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw or raw == "quit":
            break

        if raw == "pages":
            for pid, p in kb.pages.items():
                status = p.footer.get("review_status", "?")
                color = GREEN if status == "approved" else YELLOW
                print(f"    {pid:<30} {color}{status}{RESET}  "
                      f"{DIM}{p.title}{RESET}")
            continue

        if raw.startswith("read "):
            page_id = raw[5:].strip()
            page = kb.read(page_id)
            if page:
                print(json.dumps(page, indent=2, ensure_ascii=False))
            else:
                print(f"    {RED}page not found: {page_id}{RESET}")
            continue

        if raw.startswith("cite "):
            query = raw[5:].strip()
            mcp_call("kb.cite", {"query": query, "k": 3})
            results = kb.cite(query, k=3)
            print(json.dumps(results, indent=2, ensure_ascii=False))
            continue

        query = raw
        if raw.startswith("search "):
            query = raw[7:]
        mcp_call("kb.search", {"query": query, "k": 5})
        results = kb.search(query, k=5)
        print(json.dumps(results, indent=2, ensure_ascii=False))


# ── Main ────────────────────────────────────────────────────────────

def main() -> int:
    heading("Demo 2 — Agent KB Query (MCP Simulation)")

    pages = load_pages(KB_DIR)
    print(f"  Loaded {len(pages)} KB pages from {KB_DIR.name}/\n")
    for p in pages:
        status = p.footer.get("review_status", "?")
        color = GREEN if status == "approved" else YELLOW
        print(f"    {p.page_id:<30} {color}{status}{RESET}  "
              f"layer={p.footer.get('layer', '?')}  "
              f"updated_by={p.footer.get('updated_by', '?')}")

    kb = KnowledgeBase(pages)

    run_scripted_scenario(kb)

    heading("Key observations")
    print(f"  1. {BOLD}kb.read returns the footer{RESET} — agent sees review_status")
    print(f"     before deciding whether to cite a page.")
    print(f"  2. {BOLD}kb.cite returns file:line{RESET}, not prose — this is a")
    print(f"     verifiable anchor, not a hallucinated reference.")
    print(f"  3. {BOLD}filter parameter{RESET} lets the agent enforce tuple-based")
    print(f"     policies (e.g. only approved pages).")
    print()

    run_repl(kb)
    return 0


if __name__ == "__main__":
    sys.exit(main())
