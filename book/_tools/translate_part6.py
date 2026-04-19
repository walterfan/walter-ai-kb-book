"""Apply Chinese translations for Part VI: index + ch22 + ch23 + ch24.

Run with: poetry run python book/_tools/translate_part6.py

Style guide inherited from Part III, IV, V batches:
  - English kept for: CLI names, file paths, variable names, `{cite}` keys,
    $math$, API symbols, frontmatter field names.
  - Keep **bold** markup and `code spans` exactly as English.
  - Technical identifiers stay English (Sphinx, MyST, ADR, BGE, etc.).
"""

from __future__ import annotations

import os
import sys
import polib

LOCALE_ROOT = "book/locale/zh_CN/LC_MESSAGES/part6-governance-and-outlook"


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

    "Part VI — Governance & Outlook": "第六部分 —— 治理与展望",

    "Trust, cost, privacy, and where this is all going.":
        "信任、成本、隐私，以及这一切将走向何处。",

    "Cost models, red-teaming, provenance discipline, and the open research questions.":
        "成本模型、红队演练、出处纪律，以及仍然开放的研究问题。",

    "Three chapters closing the book.": "三章内容为全书收尾。",

    "A checklist of failure modes the maintainer should rehearse.":
        "一份维护者应当反复演练的失败模式清单。",

    "The KB is never done; it is maintained. This Part says how.":
        "知识库永远没有“做完”的一天；它只有被持续维护。这一部分讲的就是如何维护。",
}


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


CH23: dict[str, str] = {
    **STUB_BODY,
    "Chapter 23 — Trust, Provenance and Red-teaming":
        "第 23 章 —— 信任、出处与红队演练",
}


CH24: dict[str, str] = {
    **STUB_BODY,
    "Chapter 24 — Outlook and Open Problems":
        "第 24 章 —— 展望与尚未解决的问题",
}


CH22: dict[str, str] = {
    "Chapter 22 — Cost, Privacy, Security":
        "第 22 章 —— 成本、隐私、安全",

    "Why": "Why —— 为什么",
    "What": "What —— 是什么",
    "How": "How —— 怎么做",
    "Example": "Example —— 范例",
    "Conclusion": "Conclusion —— 小结",
    "References": "参考文献",

    "Every chapter up to this point has treated cost, privacy, and security as constraints on individual decisions — use an embedding model whose pricing makes re-embedding cheap (Chapter 10); keep L2's context bounded (Chapter 16); refuse to send `architecture/` to an LLM (Chapter 16's dispatcher). These are the right local choices. But local good choices do not guarantee a good global posture. A KB that would pass every chapter's individual rules can still burn a team's LLM budget on noise, expose private content in prompt logs, or publish a page whose content was written by an attacker.":
        "到目前为止，每一章都把成本、隐私、安全当作对 * 局部 * 决策的约束 —— 选一款定价让“重新嵌入”变便宜的嵌入模型（第 10 章）；把 L2 的上下文限制住（第 16 章）；拒绝把 `architecture/` 发给 LLM（第 16 章的派发器）。这些都是正确的局部选择。但局部正确不等于全局姿态健康。一个每一章的规则都能单独通过的知识库，仍然可能把团队的 LLM 预算烧在噪声上、在提示词日志中泄露私密内容，或发布一个由攻击者写就的页面。",

    "This chapter consolidates the three constraints into operational disciplines that bind across chapters. The centrepiece is the **token budget discipline** — the cost discipline that the three-level update strategy (Chapter 16) exists to support. Privacy and security complete the picture.":
        "本章把这三条约束整合为贯通各章的运维纪律。核心是 **token 预算纪律** —— 第 16 章三级更新策略所支撑的成本纪律。隐私和安全补全这张图景。",

    "Three related questions, kept honest:": "三个相互关联、都要诚实回答的问题：",

    "**Cost.** *What does running this KB cost per commit, per sync, per year?* Not the LLM-call-by-LLM-call question (which is trivial) but the aggregate question (which is what a budget conversation requires).":
        "**成本。** * 运营这个知识库，按每次 commit、每次同步、每年来算要花多少钱？ * 不是“逐次 LLM 调用多少钱”那种琐碎问题，而是聚合成本 —— 这才是一次预算讨论真正要的答案。",

    "**Privacy.** *What of our content leaves our walls, to whom, and under what retention?* This is not a rhetorical question; it has concrete answers a KB can enforce.":
        "**隐私。** * 我们的哪些内容离开了我们的墙、发给了谁、按什么保留策略处置？ * 这不是一个修辞性问题；它有具体答案，而且知识库可以强制执行这些答案。",

    "**Security.** *Can a page's author be trusted? Can a page's content be trusted? Can a page's citation be trusted?* These are distinct; each has its own mechanism.":
        "**安全。** * 页面的作者可不可信？页面的内容可不可信？页面的引用可不可信？ * 三者各不相同；每一个都有自己的机制。",

    "The token budget discipline": "Token 预算纪律",

    "The core move is this: **a KB's LLM cost should be a predictable function of its commit rate, not its page count.** If the cost scales with pages, the KB becomes more expensive as it gets more useful, which is the wrong incentive. If it scales with commits, the KB's cost is proportional to the project's actual change rate, which is exactly what a team is already budgeting for.":
        "核心那一步是这样说的： **一个知识库的 LLM 成本，应该是其 commit 频率的可预测函数，而不是页面数的可预测函数。** 如果成本随页面数扩，那么知识库越有用、就越贵 —— 这是错误的激励。如果成本随 commit 数扩，那么知识库的成本就与项目本身的变更率成正比 —— 而那本来就是团队已经在做预算的那个量。",

    "This is one of the operational claims the author has refined in a private project-knowledge-base toolkit {cite}`fanyamin_pkb_skill`: Chapter 16's three-level update strategy exists precisely so commit cost stays bounded as the KB grows. The arithmetic:":
        "这是作者在一个私有的 project-knowledge-base 工具包 {cite}`fanyamin_pkb_skill` 中反复打磨出的运维主张之一：第 16 章的三级更新策略存在的唯一目的，就是让 commit 成本在知识库增长时仍然保持有界。做一道算术题：",

    "**Naive baseline — \"regenerate every page whose topic changed\"**:":
        "**朴素基线 —— “每一个话题发生变化的页面都重新生成”** ：",

    "\n\\text{cost}_\\text{naive} \\approx N_\\text{candidates} \\times C_\\text{full-page}\n":
        "\n\\text{cost}_\\text{naive} \\approx N_\\text{candidates} \\times C_\\text{full-page}\n",

    "where $N_\\text{candidates}$ grows with both the KB's size and the commit's blast radius, and $C_\\text{full-page}$ is a full-page LLM call (~8–20 k tokens for context plus the regenerated body).":
        "其中 $N_\\text{candidates}$ 会同时随“知识库规模”和“commit 的爆炸半径”一起增长， $C_\\text{full-page}$ 则是一次整页 LLM 调用的成本（上下文加重新生成的正文，约 8–20 k tokens）。",

    "**Three-level discipline — \"rule first, LLM second\"**:":
        "**三级纪律 —— “rule first, LLM second”** ：",

    "\n\\text{cost}_\\text{3L} \\approx N_\\text{L1} \\times 0 + N_\\text{L2} \\times C_\\text{bounded} + N_\\text{L3} \\times 0\n":
        "\n\\text{cost}_\\text{3L} \\approx N_\\text{L1} \\times 0 + N_\\text{L2} \\times C_\\text{bounded} + N_\\text{L3} \\times 0\n",

    "where L1 and L3 spend zero LLM tokens (L1 is mechanical; L3 is human), and $C_\\text{bounded}$ is a bounded call capped by Chapter 16 at ~5 k tokens. Concretely, for the week of sync in Chapter 16's example (19 candidates, 12 → L1, 5 → L2, 2 → L3): five L2 calls at roughly 3 k tokens each. At 2024 `text-embedding-3-small` / `gpt-4o-mini` pricing {cite}`openai_embeddings_v3`, that is cents per week per repo. The naive baseline on the same 19 candidates, at 15 k tokens each, is more than ten times the spend *and* produces diffs that burn reviewer minutes — which, as the previous chapter argued, is the costlier resource.":
        "其中 L1 和 L3 花 0 个 LLM token（L1 是机械操作，L3 是人类操作）， $C_\\text{bounded}$ 是被第 16 章上限在 ~5 k tokens 的有界调用。以第 16 章例子里那一周的同步为例（19 个候选，12 → L1、5 → L2、2 → L3）：五次 L2 调用，每次约 3 k tokens。按 2024 年 `text-embedding-3-small` / `gpt-4o-mini` 的定价 {cite}`openai_embeddings_v3` 来算，每个仓库每周就是几美分的事。朴素基线在同样 19 个候选上按每个 15 k tokens 计，花费高出十倍以上， * 而且 * 会产出一堆 diff 去烧评审者的时间 —— 正如上一章所论，那才是更贵的资源。",

    "The token budget discipline has three rules:": "Token 预算纪律有三条规则：",

    "**Budget in commits, not pages.** Decide the cost-per-commit ceiling up front (e.g. $\\$0.10 per commit for a small team; pennies for a well-tuned pipeline). Track it. Alert on regression.":
        "**以 commit 为单位做预算，而不是以页面为单位。** 事先定下“每次 commit 的成本上限”（比如小团队 $\\$0.10/commit；调校良好的流水线只需几分钱）。追踪它。一旦回归就告警。",

    "**L1 ratio is a KPI.** The fraction of candidates handled by L1 is an operational metric. An L1 ratio of 50% is healthy; 90% is excellent (and usually means you have good auto-generated pages). An L1 ratio below 20% means the rules are not capturing the common cases, or the KB is unnaturally L2-heavy.":
        "**L1 比例是一项 KPI。** “由 L1 处理的候选占比”是一个运维指标。50% 算健康；90% 算优秀（通常意味着你有一批好用的自动生成页）。L1 比例低于 20% 说明规则没有捕捉到常见场景，或者这个知识库“异常偏 L2”。",

    "**L3 is bounded by human attention, not token cost.** Do not attempt to trade L3 for L2 to save dollars. The dollars were never the constraint.":
        "**L3 的约束是人的注意力，不是 token 成本。** 不要为了省钱就把本该 L3 的东西挪到 L2。钱从来不是约束。",

    "These rules make the cost line on the dashboard a *leading indicator* of KB health, not just an accounting number.":
        "这些规则让 dashboard 上的成本曲线成为知识库健康的 * 先行指标 * ，而不只是一个会计数字。",

    "Privacy: bounded context as a privacy property":
        "隐私：把“有界上下文”视作一种隐私属性",

    "The L2 bounded-LLM strategy from Chapter 16 has a property the cost argument does not exhaust: **bounded context is bounded disclosure.** Every time an LLM is called, *some* content leaves the host. Depending on the provider, it may be retained for model training, for abuse monitoring, or simply in request logs. Even with a no-data-retention contract, prompts are held transiently somewhere.":
        "第 16 章那条 L2 有界 LLM 策略，还有一个成本论证未能穷尽的性质： **有界的上下文，等于有界的披露。** 每一次调用 LLM， * 总有一些 * 内容离开宿主。视供应方不同，这些内容可能被保留用于模型训练、滥用监控，或只是进了请求日志。即使签了“无数据保留”合同，提示词仍然会在某处短暂驻留。",

    "The L2 discipline gives a direct privacy handle:":
        "L2 纪律给了我们一个直接的隐私把手：",

    "Strategy": "策略",
    "Sent per call": "每次调用发送量",
    "Annual disclosure surface": "年度披露面",

    "Naive full-regeneration": "朴素的整页重生成",
    "The whole page ~8–20 k tokens": "整个页面，约 8–20 k tokens",
    "≈ $N_\\text{pages} \\times$ weekly-regen-rate":
        "≈ $N_\\text{pages} \\times$ 每周重生成率",

    "L2 bounded": "L2 有界",
    "One page's body + one diff ~2–5 k tokens":
        "一个页面的正文 + 一份 diff，约 2–5 k tokens",
    "≈ $N_\\text{L2-candidates}$ only":
        "≈ 仅 $N_\\text{L2-candidates}$",

    "L1 only": "只走 L1",
    "Nothing": "什么都不发",
    "None": "无",

    "L3 human-led": "L3 人工主导",
    "Whatever a human pastes": "人粘贴什么就是什么",
    "Human-controlled": "由人来控制",

    "L1's zero-disclosure property is the strongest privacy argument for \"rule first, LLM second.\" Every rule that resolves a change at L1 is content that never left the host. For KBs with sensitive content — security runbooks, incident postmortems, internal architecture — the rule-first discipline is not just a cost argument but a disclosure argument.":
        "L1 的“零披露”性质是“rule first, LLM second”最有力的隐私论据。每一条在 L1 消化掉变更的规则，对应着一段“从未离开宿主”的内容。对那些含有敏感内容的知识库 —— 安全 runbook、事故复盘、内部架构 —— 而言，rule-first 纪律不只是成本论证，也是披露论证。",

    "Three concrete actions follow:": "由此可以落地三个具体动作：",

    "**Tag sensitive paths.** Paths like `security/`, `incidents/`, and `adr/` (if ADRs discuss sensitive trade-offs) are tagged `privacy: restricted` in the dispatcher config and are routed L3-only. The dispatcher rule is already in Chapter 16; the privacy framing is *why* the rule exists.":
        "**给敏感路径打标签。** `security/`、`incidents/`、以及 `adr/`（如果其中的 ADR 讨论敏感权衡）这样的路径，在派发器配置里被打上 `privacy: restricted`，只路由到 L3。派发器规则本身在第 16 章已有；隐私视角说明的是 —— 这条规则 * 为什么 * 存在。",

    "**Prefer self-hosted models for L2 on sensitive paths.** An open-weight embedding and a small open LLM on local GPUs (e.g. the BGE family {cite}`xiao2024bge`) can handle L2 for everything except the hardest L3 escalations, at zero third-party disclosure.":
        "**敏感路径上的 L2 优先使用自托管模型。** 本地 GPU 上跑一个开权重嵌入模型加一个小开源 LLM（例如 BGE 系列 {cite}`xiao2024bge`）就足以承担 L2 的所有工作 —— 除去最难的那些本来就要升级到 L3 的情况 —— 而且对第三方的披露量为零。",

    "**Log every L2 call.** Chapter 15's gate report can include a per-commit ledger of which pages went to L2. This gives the team an auditable answer to \"what did we send to the model provider this week?\" — which is both a privacy control and a debugging aid.":
        "**记录每一次 L2 调用。** 第 15 章的门禁报告可以附一份“每次 commit 有哪些页面走了 L2”的账本。这让团队有一个可审计的答案来回应“这一周我们到底向模型供应商发了什么？” —— 它既是一条隐私控制，也是调试工具。",

    "Security: three independent trust questions":
        "安全：三个互相独立的信任问题",

    "Security of a KB is not a single question. Three distinct questions, each with its own mechanism:":
        "知识库的安全性不是单一问题。它是三个各有其机制的独立问题：",

    "**Can the author be trusted?** Mechanism: `created_by` + `updated_by` fields (Chapter 5), enforced by `MergeFrontmatterUpdate`'s immutability rule. A page never loses its origin authorship. The Git history provides a second, independent record.":
        "**作者可不可信？** 机制：`created_by` + `updated_by` 字段（第 5 章），由 `MergeFrontmatterUpdate` 的不可变性规则强制执行。一个页面永远不会丢失它最初的作者身份。Git 历史提供了第二份独立记录。",

    "**Can the content be trusted?** Mechanism: the footer's `review_status` + `review_score` (Chapter 5), the hard gates (Chapter 15 H3), and the AI-always-sets-pending rule. A page whose content has been touched but not reviewed is `review_status: pending` — explicitly.":
        "**内容可不可信？** 机制：footer 里的 `review_status` + `review_score`（第 5 章）、硬门禁（第 15 章 H3），以及“AI 总是置 pending”规则。一个内容被动过、但尚未被评审的页面是 `review_status: pending` —— 显式为之。",

    "**Can the citations be trusted?** Mechanism: H4 in Chapter 15 every `file:line` anchor resolves at HEAD. An adversarial or hallucinated citation fails the gate and blocks publish.":
        "**引用可不可信？** 机制：第 15 章的 H4 —— 每一个 `file:line` 锚点都必须在 HEAD 处解析成功。任何对抗性的或幻觉出来的引用都会通不过门禁，从而阻止发布。",

    "Attacks on a KB tend to split along the same three axes. Authorship attacks are Git-level (compromised account, rogue PR); content-drift attacks are stale-page attacks (something true once is no longer true, an attacker exploits the belief it is); citation attacks are the most pernicious category — a page that claims to cite the code but does not — and these are also the most mechanically defensible because citation resolution is decidable.":
        "针对知识库的攻击也倾向于沿同样的三条轴分裂。作者攻击发生在 Git 层面（账号被盗、恶意 PR）；内容漂移攻击是“陈旧页面”攻击（从前为真的某件事如今不再为真，攻击者利用“人们仍相信它为真”这一点）；引用攻击则是其中最恶毒的一类 —— 页面声称自己引用了代码、实则没有 —— 而它们恰恰是最容易用机械手段防御的，因为“引用能不能解析”是可判定的。",

    "The three-layer threat model": "三层威胁模型",

    "Putting it together, a page in a well-run KB carries three independent attestations:":
        "把它们放在一起看：一个运作良好的知识库中的页面，背后有三份互相独立的证明：",

    "An attacker must compromise all three layers to plant a page that looks legitimate. Compromising Git is hard if the team uses signed commits; compromising the review requires the reviewer's signature in the footer; compromising citations is almost impossible because the citations are checked mechanically at publish time. Each layer is independently cheap; together they are considerably stronger than any single layer.":
        "攻击者必须同时攻破这三层，才能种下一个“看起来合法”的页面。如果团队使用签名 commit，攻破 Git 就很难；攻破评审要伪造评审者在 footer 中的签名；攻破引用则几乎不可能，因为引用在发布时是被机械式校验的。每一层单独代价都很低；三层叠加起来，比任何单层都要强得多。",

    "A concrete budget-and-disclosure sheet for one mid-sized KB (numbers anonymised but operationally realistic):":
        "一份针对某中型知识库的具体“预算与披露表”（数据已匿名化，但运维上真实合理）：",

    "Every line is a rule or a mechanism explained in one of the earlier chapters. This chapter's contribution is putting them on a single page so the governance conversation has something concrete to look at.":
        "每一行都对应之前某一章讲过的某条规则或某个机制。本章的贡献是把它们集中到同一张纸上，让“治理对话”在桌面上有个实实在在可看的东西。",

    "Cost, privacy, and security are usually treated as three separate concerns. Run through the operational model of Chapter 7a, they turn out to share a common spine: the three-level update strategy bounds tokens (cost), bounds disclosure (privacy), and leaves the hardest cases to a human (security). None of that machinery is new in this chapter. What is new is the claim that *these three properties are the same property* — the discipline of not letting an LLM touch what a rule or a human can touch better, cheaper, and more privately.":
        "成本、隐私、安全通常被当作三件独立的关切。但把它们放到第 7 章 a 节的运维模型里走一遍，就会发现它们其实共享同一条主脊：三级更新策略把 token 界住（成本）、把披露界住（隐私）、并把最棘手的情形留给人（安全）。本章提到的机制没有一条是新的；新的是这个主张 —— * 这三个性质其实是同一个性质 * ：不让 LLM 去碰那些“规则或人能够更好、更便宜、更私密地处理”的东西，这条纪律本身。",

    "The next chapter discusses trust and red-teaming: once the operational model is in place, how does a KB actually get tested against adversarial use?":
        "下一章讨论信任与红队演练：一旦运维模型就位，一个知识库到底如何在对抗性使用下被测试？",
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
        ("ch22-cost-privacy-security", CH22),
        ("ch23-trust-provenance-and-red-teaming", CH23),
        ("ch24-outlook-and-open-problems", CH24),
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
