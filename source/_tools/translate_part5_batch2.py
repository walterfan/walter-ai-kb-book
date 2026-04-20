"""Apply Chinese translations for Part V batch 2: ch18.

Run with: poetry run python source/_tools/translate_part5_batch2.py
"""

from __future__ import annotations

import os
import sys
import polib

LOCALE_ROOT = "source/locale/zh_CN/LC_MESSAGES/part5-hybrid-layer"


CH18: dict[str, str] = {
    "Chapter 18 — Document Layering L0–L4":
        "第 18 章 —— 文档分层 L0–L4",

    "Why": "Why —— 为什么",
    "What": "What —— 是什么",
    "How": "How —— 怎么做",
    "Example": "Example —— 范例",
    "Conclusion": "Conclusion —— 小结",
    "References": "参考文献",

    "A mature knowledge base contains pages that are not of the same *kind* even when they are of the same Diátaxis *type* (Chapter 3). A `runbook.md` written by an experienced on-call engineer and a `runbook.md` regenerated yesterday by an LLM are both how-tos. They both live under `content/`. They both have the same frontmatter schema. But they are not equally trustworthy, and a retrieval system that treats them as equals will eventually answer a 3 am incident question with the wrong page.":
        "一个成熟的知识库里，有些页面即便属于同一种 Diátaxis * 类型 * （第 3 章），也不是同一 * 种类 * 。一份由资深 on-call 工程师写的 `runbook.md` 和一份昨晚由 LLM 重新生成的 `runbook.md` 都是 how-to，都住在 `content/` 下，frontmatter schema 也一样 —— 但它们的可信程度并不等同。一个把它们一视同仁的检索系统，迟早会在凌晨 3 点的事故问询中拿错页面。",

    "The blog post the book builds on {cite}`fanyamin2026deepwiki` introduces a five-tier **document-layer** model (L0 – L4) that distinguishes pages by their *authorial provenance* — who wrote the page and how much authority attaches to it. This chapter makes that model precise, shows why a single-axis layering is not enough, and upgrades it to a four-tuple that integrates the footer fields Chapter 5 introduced.":
        "本书所基于的那篇博客 {cite}`fanyamin2026deepwiki` 引入了一个五层 **document-layer** 模型（L0 – L4），按 * 作者出处 * —— 页面是谁写的、它附带多少权威 —— 来区分页面。本章把这个模型精确化，说明“单轴分层”为什么不够用，并把它升级为一个四元组，与第 5 章引入的 footer 字段整合起来。",

    "The single-axis L0 – L4 model": "单轴的 L0 – L4 模型",

    "The blog's original L0–L4, stated compactly:":
        "博客原文里的 L0–L4，紧凑地重述一遍：",

    "Tier": "层级",
    "Authority": "权威度",
    "Who writes": "由谁书写",
    "Examples": "示例",

    "**L0**": "**L0**",
    "Strongest": "最强",
    "Code and its comments": "代码及其注释",
    "Function bodies, docstrings, OpenAPI specs":
        "函数体、docstring、OpenAPI 规格",

    "**L1**": "**L1**",
    "Strong": "强",
    "Humans, committed": "人写，已提交",
    "ADRs, architecture docs, hand-written runbooks":
        "ADR、架构文档、手写 runbook",

    "**L2**": "**L2**",
    "Moderate": "中等",
    "Humans, collaborative": "人写，协作修订",
    "Wiki pages, design docs, retros": "wiki 页面、设计文档、复盘",

    "**L3**": "**L3**",
    "Weak": "弱",
    "AI, reviewed": "AI 产出，已评审",
    "LLM-generated summaries a human approved":
        "经人类批准的 LLM 生成摘要",

    "**L4**": "**L4**",
    "Conditional": "有条件（待评审）",
    "AI, unreviewed": "AI 产出，未评审",
    "LLM-generated drafts waiting for review":
        "等待评审的 LLM 生成草稿",

    "The single-axis model is good as a first move. It correctly names the single most common confusion: that AI-drafted prose and human-written ADRs should not be retrieved with equal weight. A retrieval layer that weights results by tier — boost L0, boost L1, down-weight L4 — immediately behaves better than one that does not.":
        "作为第一步，单轴模型已经相当好。它正确地点名了最常见的那种混淆：“AI 起草的文稿”和“人写的 ADR”不应该以相同权重被检索出来。一个按层级给结果加权的检索层 —— L0 加权、L1 加权、L4 降权 —— 立刻就会比不分层的检索层表现更好。",

    "Why one axis is not enough": "为什么一根轴不够",

    "The single-axis model still conflates two things a KB has to treat separately: **who wrote the current version** and **has anyone reviewed it**. They correlate but they are not the same. Consider four pages all of Diátaxis type `how-to`:":
        "单轴模型仍然把知识库必须分开处理的两件事混在了一起： **当前版本是谁写的** ，以及 **有没有人评审过它** 。两者相关但不等同。考虑四个都属于 Diátaxis `how-to` 类型的页面：",

    "A human wrote it three months ago; it has not been reviewed since.":
        "人三个月前写的，从那以后无人再评审。",

    "A human wrote it yesterday; another human reviewed it today.":
        "人昨天写的，另一个人今天评审过了。",

    "An LLM drafted it yesterday; a human reviewed and approved it today with a score of 4.":
        "LLM 昨天起草，人今天评审并以 4 分通过。",

    "An LLM drafted it yesterday; no one has reviewed it.":
        "LLM 昨天起草，没有人评审过。",

    "The single-axis model collapses (1) and (2) into L2 and (3) and (4) into L3/L4. But a working retrieval layer wants to treat (3) more like (2) than like (4): in case (3) a human has actually signed off, which is the signal that matters. The prose is AI-drafted, but the authority is human-verified.":
        "单轴模型把 (1) 和 (2) 并入 L2，把 (3) 和 (4) 并入 L3/L4。但一个真正能用的检索层希望把 (3) 当作更像 (2)、而不是更像 (4) 的东西 —— 因为在 (3) 这一场景里，确实有一个人签过字，这才是真正重要的信号。文稿是 AI 起草的，但权威已经由人核实过。",

    "This is the gap the footer's review fields close. Chapter 5's `PKB-metadata` footer gives every page four values that together identify its kind more precisely than any single axis can:":
        "这正是 footer 中的评审字段所填补的那道缝隙。第 5 章的 `PKB-metadata` footer 给每个页面提供了四个值，它们合起来可以比任何单根轴更精确地指认该页面的种类：",

    "`layer` ∈ {L0, L1, L2, L3, L4} — *where in the hierarchy does this page sit?*":
        "`layer` ∈ {L0, L1, L2, L3, L4} —— * 这个页面位于层级结构的哪里？ *",

    "`updated_by` ∈ {`human`, `ai`, `ai+human`} — *who authored the current version?*":
        "`updated_by` ∈ {`human`, `ai`, `ai+human`} —— * 当前版本是谁写的？ *",

    "`review_status` ∈ {`pending`, `approved`} — *has a human signed off?*":
        "`review_status` ∈ {`pending`, `approved`} —— * 有人签过字了吗？ *",

    "`review_score` ∈ [0, 5] — *how good is it, in the reviewer's judgement?*":
        "`review_score` ∈ [0, 5] —— * 在评审者的判断里，它有多好？ *",

    "The tuple model": "元组模型",

    "The upgraded document layer is the tuple":
        "升级后的文档层是这样一个元组：",

    "\n\\text{layer} = \\langle L, U, R, S \\rangle\n":
        "\n\\text{layer} = \\langle L, U, R, S \\rangle\n",

    "where $L$ is the single-axis tier, $U$ is `updated_by`, $R$ is `review_status`, and $S$ is `review_score`. The author's private project-knowledge-base toolkit {cite}`fanyamin_pkb_skill` encodes exactly this four-valued stance. Two pages at \"the same layer\" on the old scale can now be distinguished:":
        "其中 $L$ 是单轴层级， $U$ 是 `updated_by`，$R$ 是 `review_status`，$S$ 是 `review_score`。作者的私有 project-knowledge-base 工具包 {cite}`fanyamin_pkb_skill` 正是以这种“四值立场”编码。旧刻度上“同一层”的两个页面，现在可以被区分开来：",

    "Page": "页面",
    "Old tier": "旧层级",
    "Tuple": "元组",
    "Retrieval weight": "检索权重",

    "L1 ADR, human-written, approved, score 4":
        "L1 的 ADR，人写，已批准，得分 4",
    "L1": "L1",
    "⟨L1, human, approved, 4⟩": "⟨L1, human, approved, 4⟩",
    "1.0": "1.0",

    "L1 ADR, LLM-updated, pending review":
        "L1 的 ADR，LLM 更新过，待评审",
    "⟨L1, ai, pending, 0⟩": "⟨L1, ai, pending, 0⟩",
    "0.3": "0.3",

    "L3 summary, LLM-drafted, human-approved, score 4":
        "L3 摘要，LLM 起草，人已批准，得分 4",
    "L3": "L3",
    "⟨L3, ai+human, approved, 4⟩": "⟨L3, ai+human, approved, 4⟩",
    "0.8": "0.8",

    "L3 summary, LLM-drafted, no review":
        "L3 摘要，LLM 起草，未评审",
    "⟨L3, ai, pending, 0⟩": "⟨L3, ai, pending, 0⟩",
    "0.2": "0.2",

    "The retrieval weight is one plausible projection; Chapter 19's graph-guided context assembly uses a richer function, but the principle is the same. The tuple exposes four numbers the retrieval code can *actually use*, where the old single axis exposed one.":
        "表中的“检索权重”只是一种合理的投影方式；第 19 章的图引导上下文组装用的是一个更丰富的函数，但原理相同。元组向检索代码暴露了四个 * 可以真正用得上的 * 数值，而旧单轴只暴露一个。",

    "Assigning tuples at ingestion": "在入库阶段为页面指派元组",

    "The pipeline (Chapter 7) assigns $\\langle L, U, R, S \\rangle$ when a page is created or updated. Three rules cover almost every case:":
        "流水线（第 7 章）会在页面被创建或更新时指派 $\\langle L, U, R, S \\rangle$。三条规则几乎能覆盖所有情形：",

    "**At creation**, $L$ is inferred from the path: `adr/` → L1; `architecture/` → L1; `content/` with `created_by: human` → L2; `content/` with `created_by: ai` → L4. $U$ mirrors `created_by`. $R$ is `pending` if `created_by: ai`, else `approved`. $S$ is `0` if `created_by: ai`, else a default set by the author.":
        "**创建时** ， $L$ 从路径推断：`adr/` → L1；`architecture/` → L1；`content/` 且 `created_by: human` → L2；`content/` 且 `created_by: ai` → L4。 $U$ 镜像 `created_by`。当 `created_by: ai` 时 $R$ 为 `pending`，否则为 `approved`。当 `created_by: ai` 时 $S$ 为 `0`，否则由作者给一个默认值。",

    "**On L1 mechanical update** (Chapter 16): $L$ is unchanged (a re-stamp does not move a page between tiers); $U$ set to `ai` (the automated actor); $R$ to `pending`; $S$ to `0`.":
        "**L1 机械化更新时** （第 16 章）： $L$ 不变（一次重打时间戳不会把页面挪到别的层级）； $U$ 置为 `ai`（自动化执行者）； $R$ 置为 `pending`； $S$ 置为 `0`。",

    "**On L2 bounded-LLM update** (Chapter 16): $L$ is unchanged; $U$ set to `ai`; $R$ to `pending`; $S$ to `0`. If a human later approves, $U$ transitions to `ai+human`, $R$ to `approved`, $S$ to the reviewer's score.":
        "**L2 有界 LLM 更新时** （第 16 章）： $L$ 不变； $U$ 置为 `ai`； $R$ 置为 `pending`； $S$ 置为 `0`。如果事后有人批准，则 $U$ 迁移到 `ai+human`， $R$ 迁移到 `approved`， $S$ 迁移到评审者给出的分数。",

    "These rules are the **AI-always-sets-pending** rule (Chapter 5) and the **L3 human review** path (Chapter 16), restated in the tuple's vocabulary. They are not new policy; they are consequences of the rules stated elsewhere, re-expressed as tuple transitions.":
        "这些规则就是 **“AI 总是置 pending”** 规则（第 5 章）和 **L3 人类评审** 路径（第 16 章）在元组词汇下的重述。它们不是新政策 —— 只是其他地方规则的推论，被重新表达为“元组之间的状态迁移”。",

    "Using the tuple at retrieval": "在检索阶段使用元组",

    "A retrieval layer (Chapters 12, 19) scores a candidate page with a function roughly like:":
        "检索层（第 12 章、第 19 章）用一个大致如下的函数给候选页面打分：",

    "Exact weights are a tuning choice, not a claim of this book. The interesting move is *that the score depends on four values of the footer, not one*. A page whose layer is L1 but which is currently unreviewed after an L2 rewrite sinks below a truly approved L2 page. That is the behaviour a KB needs; the tuple makes it expressible in a few lines of code.":
        "具体权重是一种调参选择，不是本书的主张。关键的一步是 * 得分依赖 footer 的四个值，而不是一个 * 。一个 layer 为 L1、但经过一次 L2 改写后仍处于 unreviewed 状态的页面，会下沉到一个真正 approved 的 L2 页面下面。这就是知识库需要的行为；元组让这一点可以用几行代码表达出来。",

    "Using the tuple at publish time": "在发布阶段使用元组",

    "The gates from Chapter 15 already read the footer fields directly, but the tuple formalises one additional check: **authority consistency.** A page whose $U = \\text{ai}$ and $R = \\text{approved}$ must have a non-empty `reviewed_by`; a page whose $L = \\text{L0}$ must have $U = \\text{human}$ because code is not LLM-generated at this layer. Checks like these are one line each; they catch mis-tagging before publish.":
        "第 15 章的门禁其实已经直接读取 footer 字段，但元组把另外一类检查形式化： **权威一致性。** 一个 $U = \\text{ai}$ 且 $R = \\text{approved}$ 的页面必须有非空的 `reviewed_by`；一个 $L = \\text{L0}$ 的页面必须 $U = \\text{human}$ ，因为在这一层代码并不是 LLM 生成的。这类检查每条一行代码即可；它们能在发布前就把错误标签抓出来。",

    "A before-and-after for the same page under the two models:":
        "同一个页面在两种模型下的“前”和“后”对比：",

    "**Single-axis view.** A page `runbook/ingest-pipeline-failure.md` has frontmatter `doc_type: how-to, status: published, verification_status: unreviewed`. The blog's single-axis model would classify it as L3 (AI prose, notionally reviewable). Retrieval weights it at ~0.6. Problem: the page was actually written by a human two weeks ago; it says `unreviewed` only because a cron job flipped the status when no one had re-verified it. The single axis cannot tell the difference.":
        "**单轴视角。** 一个页面 `runbook/ingest-pipeline-failure.md` 的 frontmatter 是 `doc_type: how-to, status: published, verification_status: unreviewed`。博客那套单轴模型会把它分类为 L3（AI 文稿，理论上可评审）。检索对它的加权约 0.6。问题是：这个页面其实是两周前由一个人写的，它之所以是 `unreviewed`，只是因为一个 cron 任务在“没人再次核验它”时把状态翻转了。单根轴看不出这种差别。",

    "**Tuple view.** The same page's full footer reads:":
        "**元组视角。** 同一个页面完整的 footer 是这样的：",

    "Tuple: ⟨L2, human, pending, 0⟩. The retrieval layer reads: human authored, not formally reviewed, score unknown. This is a different thing from ⟨L3, ai, pending, 0⟩ (AI drafted, never reviewed), and different again from ⟨L2, human, approved, 4⟩ (human authored, human approved, high score). All three would have been L2 or L3 in the old model. In the tuple model they each get a distinct score.":
        "元组：⟨L2, human, pending, 0⟩。检索层读到的是：人作者，尚未被正式评审，分数未知。这与 ⟨L3, ai, pending, 0⟩（AI 起草，从未评审）并不相同，也与 ⟨L2, human, approved, 4⟩（人写、人批、高分）不同。在旧模型里这三个本来都会被归到 L2 或 L3；在元组模型里它们各自得到一个不同的分数。",

    "A soft gate (Chapter 15 S2) flags the first page to the reviewer: *\"human-authored runbook, never reviewed; please check at least once. Takes a minute; prevents a 3 am problem.\"*":
        "一个软门禁（第 15 章 S2）会把第一个页面提交给评审者： * “人写的 runbook，从未被评审过；请至少看一次。花一分钟，防一次凌晨 3 点的问题。” *",

    "The single-axis L0–L4 was a good first move: it made explicit that authorial provenance is a first-class attribute of a document. The tuple upgrade is the honest continuation: authorial provenance is itself two separate questions — *who wrote this* and *who signed off on it* — and a KB that wants to survive LLM-era editing has to answer both. The four-tuple fits in a footer; it is cheap to write, cheap to read, and cheap to enforce.":
        "单轴的 L0–L4 是一个好的第一步：它明确把“作者出处”提为文档的一等属性。四元组升级是对这件事的诚实延续：“作者出处”本身其实是两个独立问题 —— * 这是谁写的 * 和 * 谁签了字 * —— 一个想在 LLM 时代编辑浪潮中活下来的知识库必须把两者都回答。四元组放得下一个 footer；写便宜、读便宜、强制执行也便宜。",

    "The next chapter uses the tuple at retrieval time: Chapter 19's graph-guided context assembly uses $L$ to prioritise tier, $R$ and $S$ to filter unreviewed or low-quality pages out of an LLM's context window, and the relation graph to pull in whatever else the top-k pages reference.":
        "下一章会在检索阶段使用这个元组：第 19 章的图引导上下文组装用 $L$ 决定层级优先级，用 $R$ 和 $S$ 把未评审或低质量的页面从 LLM 上下文窗口里过滤掉，并用关系图把 top-k 页面所引用的其他内容一并拉进来。",
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
    failed = 0
    applied, remaining, unmatched = apply("ch18-document-layering-L0-L4", CH18)
    print(f"ch18-document-layering-L0-L4                  applied={applied:3d}  remaining_untranslated={remaining:3d}  unmatched_keys={len(unmatched)}")
    for key in unmatched:
        print(f"   UNMATCHED: {key[:80]!r}")
        failed = 1
    return failed


if __name__ == "__main__":
    sys.exit(main())
