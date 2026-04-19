"""Apply Chinese translations for Part V batch 1: index + ch17 + ch19 + ch20
(these three chapters are still stubs and share most msgids).

Run with: poetry run python book/_tools/translate_part5_batch1.py

Style guide inherited from Part III & IV batches:
  - English kept for: CLI names, file paths, variable names, `{cite}` keys,
    $math$, API symbols, frontmatter field names.
  - Keep **bold** markup and `code spans` exactly as English.
  - Technical identifiers (Sphinx, MyST, MCP, Diátaxis, ADR) stay English.
"""

from __future__ import annotations

import os
import sys
import polib

LOCALE_ROOT = "book/locale/zh_CN/LC_MESSAGES/part5-hybrid-layer"


# Shared header/footer msgids that appear identically in index + stub chapters.
SHARED: dict[str, str] = {
    "Why": "Why —— 为什么",
    "What": "What —— 是什么",
    "How": "How —— 怎么做",
    "Example": "Example —— 范例",
    "Conclusion": "Conclusion —— 小结",
    "References": "参考文献",
}


INDEX: dict[str, str] = {
    **SHARED,

    "Part V — The Hybrid Layer": "第五部分 —— 混合层",

    "Prose + code + graph + agents — the layer where the KB starts paying for itself.":
        "文稿 + 代码 + 图谱 + agent —— 知识库开始给自己挣回本钱的那一层。",

    "The L0–L4 document architecture, graph-guided context, and how the KB feeds AI coding tools.":
        "L0–L4 文档架构、图引导的上下文组装，以及知识库如何喂养 AI 编码工具。",

    "Five chapters, heavily drawing on blog §§11–12 {cite}`fanyamin2026deepwiki` and expanding each into full chapter depth.":
        "五章内容，大量取材于博客 §§11–12 {cite}`fanyamin2026deepwiki`，并把每一节扩展成完整一章的深度。",

    "A round-trip where a Cursor-style agent answers with `file:line` citations, backed by MCP tools exposed by the code-layer reference implementation.":
        "一次完整往返：一个 Cursor 风格的 agent 用 `file:line` 引用作答，背后由代码层参考实现暴露出来的 MCP 工具驱动。",

    "The hybrid layer is what turns a KB into a *team member*.":
        "混合层，就是让一个知识库真正变成 * 团队成员 * 的那一层。",
}


# ch17/ch19/ch20 are stubs with identical body text for "Why/What/How/Example/Conclusion".
STUB_BODY: dict[str, str] = {
    **SHARED,

    "Stub — replace with the chapter's motivation. Draws on {cite}`fanyamin2026deepwiki` where the blog's corresponding section applies (see `design.md` D8 for the mapping).":
        "Stub —— 此处待填本章动机。对应博客小节适用时即引用 {cite}`fanyamin2026deepwiki`（映射见 `design.md` D8）。",

    "Stub — the precise definitions and scope.":
        "Stub —— 此处待填精确的定义与范围界定。",

    "Stub — the methodology, architecture, and code excerpts. Code comes via `book/examples/part3-code-layer/` with provenance from `examples/SOURCE.md`.":
        "Stub —— 此处待填方法论、架构与代码片段。代码通过 `book/examples/part3-code-layer/` 接入，来源信息见 `examples/SOURCE.md`。",

    "Stub — an end-to-end recipe a reader can reproduce.":
        "Stub —— 此处待填一份读者可复现的端到端操作步骤。",

    "Stub — what we learned and what remains open.":
        "Stub —— 此处待填“我们学到了什么、还有什么尚未回答”。",
}


CH17: dict[str, str] = {
    **STUB_BODY,
    "Chapter 17 — Prose Meets Code": "第 17 章 —— 文稿与代码相遇",
}

CH19: dict[str, str] = {
    **STUB_BODY,
    "Chapter 19 — Graph-guided Context Assembly":
        "第 19 章 —— 图引导的上下文组装",
}

CH20: dict[str, str] = {
    **STUB_BODY,
    "Chapter 20 — Harnessing AI Coding with the KB":
        "第 20 章 —— 用知识库驾驭 AI 编码",
}


def apply(batch_name: str, translations: dict[str, str]) -> tuple[int, int, list[str]]:
    po_path = os.path.join(LOCALE_ROOT, f"{batch_name}.po")
    if not os.path.exists(po_path):
        raise FileNotFoundError(po_path)
    po = polib.pofile(po_path)
    applied = 0
    po_msgids = {e.msgid for e in po}
    unmatched = [k for k in translations if k not in po_msgids]
    for e in po:
        if e.msgid in translations:
            e.msgstr = translations[e.msgid]
            if "fuzzy" in e.flags:
                e.flags.remove("fuzzy")
            applied += 1
    po.save(po_path)
    remaining = len(po.untranslated_entries()) + len(po.fuzzy_entries())
    return applied, remaining, unmatched


def main() -> int:
    batches = [
        ("index", INDEX),
        ("ch17-prose-meets-code", CH17),
        ("ch19-graph-guided-context-assembly", CH19),
        ("ch20-harnessing-ai-coding", CH20),
    ]
    failed = 0
    for name, d in batches:
        applied, remaining, unmatched = apply(name, d)
        print(f"{name:45s} applied={applied:3d}  remaining_untranslated={remaining:3d}  unmatched_keys={len(unmatched)}")
        for key in unmatched:
            print(f"   UNMATCHED: {key[:80]!r}")
            failed = 1
    return failed


if __name__ == "__main__":
    sys.exit(main())
