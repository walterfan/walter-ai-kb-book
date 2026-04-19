"""Apply Chinese translations for Part IV batch 3: ch16.

Run with: poetry run python book/_tools/translate_part4_batch3.py
"""

from __future__ import annotations

import os
import sys
import polib

LOCALE_ROOT = "book/locale/zh_CN/LC_MESSAGES/part4-operations-lifecycle"


CH16: dict[str, str] = {
    "Chapter 16 — Maintenance, Drift and Link Rot":
        "第 16 章 —— 维护、漂移与链接腐化",

    "Why": "Why —— 为什么",
    "What": "What —— 是什么",
    "How": "How —— 怎么做",
    "Example": "Example —— 范例",
    "Conclusion": "Conclusion —— 小结",
    "References": "参考文献",

    "Chapter 14 tells you which pages changed. Chapter 15 tells you which ones cannot be published as-is. This chapter tells you what to actually *do* about each one. In the terms of Chapter 7a, this is Corner C3 — the three-level update strategy — written out operationally.":
        "第 14 章告诉你哪些页面变了。第 15 章告诉你其中哪些按现状无法发布。本章讲的是：对其中每一个页面，你到底要 * 干什么 * 。用第 7a 章的话说，这就是第 C3 角 —— 三级更新策略 —— 的运维版展开。",

    "The LLM era has changed the economics of maintenance, but not in the direction people expected. Re-embedding a repo is nearly free {cite}`openai_embeddings_v3`. Regenerating a whole page with a modern LLM is pennies. Neither of those is the bottleneck any more. The bottleneck is *a human understanding what changed*. If the pipeline regenerates 400 pages in a week, a reviewer either becomes a rubber stamp (defeating the purpose) or stops reviewing (defeating the KB).":
        "LLM 时代改变了“维护”的经济学，但改的方向和很多人想的不一样。重新嵌入一个仓库几乎是免费的 {cite}`openai_embeddings_v3`。用现代 LLM 把整页重新生成一遍也不过是几分钱。这些都不再是瓶颈。瓶颈是 * 一个人去理解“到底变了什么” * 。如果流水线一周重新生成 400 个页面，那评审者要么变成橡皮图章（违背评审的目的），要么干脆不评审了（违背知识库的目的）。",

    "The three-level strategy is the author's answer to this, refined in a private project-knowledge-base toolkit {cite}`fanyamin_pkb_skill` and presented here as the book's canonical discipline. It has one rule that matters more than the levels: **rule first, LLM second.** If a deterministic rule can do the job, do not call an LLM. Every call is a page a human may need to read.":
        "三级策略就是作者对此给出的答案 —— 在一个私有的 project-knowledge-base 工具包 {cite}`fanyamin_pkb_skill` 中反复打磨而来，在本书里被作为正式的纪律呈现出来。它有一条比各级本身更重要的规则： **rule first, LLM second。** 如果一条确定性规则能搞定，就不要调 LLM。每一次调用，都对应一个人可能必须要去读的 diff。",

    "Link rot {cite}`kiesling2017linkrot` is the most common symptom of maintenance debt and the cleanest illustration of the three levels. This chapter uses it as a running example.":
        "链接腐化 {cite}`kiesling2017linkrot` 是“维护债”最常见的症状，也是演示这三级最干净的例子。本章把它作为贯穿全章的范例。",

    "The three levels": "三个级别",

    "Every candidate page produced by Chapter 14's sync is routed to exactly one of three levels by a dispatcher whose rules are deterministic. The levels differ by who pays and what they spend:":
        "第 14 章同步产出的每个候选页面，都会被一个规则确定性的派发器精确地路由到三个级别中的某一个。各级别的差异在于“谁来买单”以及“买的是什么”：",

    "Level": "级别",
    "Who acts": "由谁动手",
    "Token cost": "Token 成本",
    "When it applies": "适用场景",
    "What the reviewer sees": "评审者看到什么",

    "**L1 Mechanical**": "**L1 机械化**",
    "A script": "一段脚本",
    "**0**": "**0**",
    "Change is resolvable by rule: footer-only drift, broken link to a moved file, auto-generated page (`repo-map`), stamp refresh":
        "变更可被规则消化：仅 footer 漂移、指向已移动文件的坏链、自动生成页（`repo-map`）、重打时间戳",
    "Nothing, usually; the pending marker on the footer":
        "通常什么都看不到；footer 上多一个 pending 标记",

    "**L2 Bounded-LLM**": "**L2 有界 LLM**",
    "An LLM + small context": "一次 LLM + 小上下文",
    "1–5 k tokens": "1–5 k tokens",
    "Body references something that genuinely changed; the fix is localised to a paragraph or two":
        "正文引用了确实发生变化的东西；修复本身局限在一两段之内",
    "A small diff; a `pending` footer asking for approval":
        "一段小 diff；一个标着 `pending`、等待批准的 footer",

    "**L3 Human-led**": "**L3 人工主导**",
    "A human; LLM copy-edits": "人；LLM 只做文字润色",
    "Variable": "不确定",
    "Architectural change, new ADR, security-sensitive content, or L2 repeatedly fails for the same page":
        "架构级变更、新的 ADR、安全敏感内容，或同一页面 L2 反复失败",
    "A real review; sometimes a new ADR":
        "一次真正的评审；有时还会产出一份新的 ADR",

    "The levels are not a menu. A page is assigned a level; it does not get to pick. The rules below determine assignment.":
        "这三级不是一份可以点的菜单。页面是被 * 指派 * 到某一级的，不能自选。下面的规则决定指派。",

    "The dispatcher rules": "派发器规则",

    "Four observations are worth pausing on:": "有四点值得停下来说：",

    "**Policy overrides first.** Architecture pages never get an automated rewrite, even if the sync thinks the change is small. Auto-generated pages never get an LLM pass, even if the change is large (it is *meant* to be mechanical).":
        "**策略级覆盖优先。** 架构页永远不会被自动重写，哪怕同步觉得这次变更很小。自动生成页也永远不会走 LLM 通道，哪怕变更很大（它 * 本来就该 * 是机械的）。",

    "**L1 is the first positive match.** The dispatcher actively tries to resolve the candidate with a rule before it considers an LLM. This is where \"rule first, LLM second\" becomes real code.":
        "**L1 是第一次肯定匹配。** 派发器会主动先尝试用规则消化候选页面，再考虑 LLM。这就是“rule first, LLM second”真正落成代码的地方。",

    "**L2 only fires on evidence.** The tags are the evidence — either a moved entity (L-entity) or a broken link (L-link) that survived the L1 rules. An L-git-only candidate with no body drift cannot reach L2.":
        "**L2 只在有证据时才启动。** 那些标签就是证据 —— 要么是一个移动实体（L-entity），要么是一条“在 L1 规则里活下来的”坏链（L-link）。一个只被 L-git 标记、正文没有漂移的候选，是到不了 L2 的。",

    "**Fall-through is conservative.** When the rules are ambiguous, route to a human. The cost of a wrong human review is an annoyance; the cost of a wrong LLM rewrite is a silent trust regression.":
        "**兜底是保守的。** 当规则模棱两可时，交给人。错误的人类评审的代价是“麻烦”；错误的 LLM 重写的代价是“悄无声息的信任回退”。",

    "What each level actually does": "每一级到底做什么",

    "**L1 Mechanical** runs pure Python or shell:":
        "**L1 机械化** 跑纯 Python 或 shell：",

    "`L1_STAMP` updates `commit:` and `last_updated:` in the footer; leaves everything else untouched.":
        "`L1_STAMP` 更新 footer 里的 `commit:` 和 `last_updated:`，其他一切不碰。",

    "`L1_FIX_LINK` rewrites one markdown link or `file:line` anchor to point at the new location of the target. If the target no longer exists at all, escalates to L2.":
        "`L1_FIX_LINK` 把一条 markdown 链接或 `file:line` 锚点重写到目标的新位置。如果目标已经彻底不存在，则升级到 L2。",

    "`L1_REGENERATE` re-runs the page's generator (e.g. `repo-map.md` from `git ls-files`) and overwrites the body. Footer resets per the AI-always-sets-pending rule — yes, even though no LLM was involved; any automated touch counts.":
        "`L1_REGENERATE` 重跑该页面的生成器（例如用 `git ls-files` 生成 `repo-map.md`）并覆盖正文。footer 按 “AI 总是置 pending” 的规则重置 —— 是的，即便这次完全没动 LLM；任何自动化的触碰都算。",

    "Every L1 action resets the footer: `review_status: pending`, `review_score: 0`, `reviewed_by:`, `updated_by: ai` (or `human` if a human ran the script). The name is a convention, not a claim that a model was called.":
        "所有 L1 动作都会重置 footer：`review_status: pending`、`review_score: 0`、`reviewed_by:`、`updated_by: ai`（如果是人类跑的脚本则是 `human`）。`ai` 这个名字是一个约定，并不主张“调了模型”。",

    "**L2 Bounded-LLM** calls one LLM with a carefully bounded context:":
        "**L2 有界 LLM** 用一个小心受限的上下文调一次 LLM：",

    "The *current* body of the one candidate page (~2 kB).":
        "该候选页面 * 当前 * 的正文（约 2 kB）。",

    "The *one diff* that triggered the change (~300 B – 2 kB).":
        "触发本次变更的 * 那一份 diff * （约 300 B – 2 kB）。",

    "The page's footer, as a reminder of C2's vocabulary.":
        "该页面的 footer，作为 C2 词汇表的提示。",

    "A *system prompt* that says: you may edit only the paragraphs that cite things in the diff; you may not invent citations; you must leave an explicit `pending` footer.":
        "一段 * 系统提示词 * ：你只能编辑那些引用了 diff 中内容的段落；不得凭空编造引用；必须留下一个显式的 `pending` footer。",

    "This bounds the token cost at roughly 5 k per call, and — more importantly — bounds the *scope* of the change. L2 cannot rewrite the whole page, because the prompt and the context do not contain the whole page's intent. It can only fix the paragraphs it was pointed at. Drift confined to one localised area is exactly the case L2 exists for.":
        "这把每次调用的 token 成本钉在大约 5 k —— 更重要的是，它钉住了变更的 * 作用域 * 。L2 不能重写整页，因为提示词和上下文里本来就没有“整页的意图”。它只能修它被指向的那几段。限制在一小片局部区域的漂移，正是 L2 存在的那个场景。",

    "**L3 Human-led** is a human writing or editing, with the LLM used (at most) for copy-editing passes the human explicitly invokes. Every L3 change is a real review in the normal git-and-PR sense. There is no special machinery here — the discipline is that the other levels *stay out* of L3's territory.":
        "**L3 人工主导** 是人亲自来写或来改，LLM 至多被用来做“人类明确发起”的文字润色。每一次 L3 变更都是一次正常 git-and-PR 意义上的真正评审。这里没有什么特别的机制 —— 真正的纪律是：其他级别 * 不要踏进 * L3 的地盘。",

    "Link rot as the canonical worked example":
        "以链接腐化为正宗范例",

    "Link rot {cite}`kiesling2017linkrot` deserves a dedicated walk-through because it is the failure most readers have personally seen and because it exercises all three levels in one scenario.":
        "链接腐化 {cite}`kiesling2017linkrot` 值得被单独走一遍，一是因为大多数读者都亲眼见过这种失败，二是因为它在一个场景里就能把三个级别全都练到。",

    "**Setup.** A repo-level refactor renames `cmd/sync/main.go` to `cmd/sync-tool/main.go` and simultaneously splits the old `runSync` function into `runSync` and `runSyncBatch`. Three pages cite the old path:":
        "**背景设定。** 一次仓库级重构把 `cmd/sync/main.go` 重命名为 `cmd/sync-tool/main.go`，同时把旧的 `runSync` 函数拆成 `runSync` 和 `runSyncBatch`。三个页面引用了旧路径：",

    "`repo-map.md` — auto-generated; just needs regeneration.":
        "`repo-map.md` —— 自动生成；只需要重新生成一次。",

    "`runbook.md` — one paragraph says \"run `cmd/sync/main.go`\"; the rest of the page is fine.":
        "`runbook.md` —— 其中一段写着“run `cmd/sync/main.go`”；页面其余部分一切正常。",

    "`architecture.md` — two paragraphs explain *why* `runSync` was structured the way it was; the split is a structural change.":
        "`architecture.md` —— 其中两段解释了 * 为什么 * `runSync` 以那种方式组织起来；这次拆分是一次结构性变更。",

    "**Sync (Chapter 14).** L-git and L-link both flag all three pages. L-entity flags `runbook.md` and `architecture.md` (both cite the function whose entity ID changed when the file moved and split).":
        "**同步（第 14 章）。** L-git 和 L-link 都把这三页全都标了出来。L-entity 标了 `runbook.md` 和 `architecture.md`（两者都引用了“因文件被移动和拆分而实体 ID 已变”的那个函数）。",

    "**Dispatcher.**": "**派发器。**",

    "`repo-map.md`: path is in `{repo-map.md, api-reference.md}` → **L1_REGENERATE.**":
        "`repo-map.md`：路径在 `{repo-map.md, api-reference.md}` 中 → **L1_REGENERATE。**",

    "`runbook.md`: path is not in any policy-override set. Tags include L-link; is the link target still a file that exists? Yes — `cmd/sync-tool/main.go` exists. **L1_FIX_LINK.**":
        "`runbook.md`：路径不在任何策略覆盖集合中。标签里包括 L-link；链接目标是否仍然是一个存在的文件？是的 —— `cmd/sync-tool/main.go` 存在。 **L1_FIX_LINK。**",

    "`architecture.md`: path is in `{architecture/}` → **L3** immediately. The dispatcher does not even inspect the tags.":
        "`architecture.md`：路径在 `{architecture/}` 中 → 立即走 **L3** 。派发器根本不会去看标签。",

    "**Execution.**": "**执行。**",

    "L1 regenerates `repo-map.md` from `git ls-files` (zero tokens, deterministic).":
        "L1 用 `git ls-files` 重新生成 `repo-map.md`（零 token，确定性）。",

    "L1 rewrites the one link in `runbook.md` from `cmd/sync/main.go` to `cmd/sync-tool/main.go` (zero tokens, localised edit).":
        "L1 把 `runbook.md` 里那一条链接从 `cmd/sync/main.go` 重写为 `cmd/sync-tool/main.go`（零 token，局部编辑）。",

    "L3 opens a human-reviewable task: *\"`architecture.md` cites `runSync`, which has been split. Does the architectural explanation in §3 need rewriting, or just a sentence about the new `runSyncBatch`? Please review.\"* A human decides; an ADR may follow; the LLM is involved only if the human asks.":
        "L3 开出一个可由人评审的任务： * “`architecture.md` 引用了 `runSync`，而它已被拆分。§3 里那段架构解释是需要整段重写，还是只需要加一句关于新 `runSyncBatch` 的说明？请评审。” * 由人做决定；可能随后产出一份 ADR；只有当人主动要求时，LLM 才会介入。",

    "**Gate run (Chapter 15).** After L1 and L3 complete, the publish gates run across all three pages. H4 (citations resolve) and H5 (links resolve) both pass now. H1/H2/H3 (footer shape) pass for L1's footers because the scripts wrote them correctly; pass for `architecture.md` because the human remembered to update the footer along with the body.":
        "**门禁跑动（第 15 章）。** L1 和 L3 做完之后，发布门禁会对这三页都跑一遍。H4（引用可解析）和 H5（链接可解析）现在都通过。H1/H2/H3（footer 形状）对 L1 的 footer 都通过，因为脚本本来就写对了；对 `architecture.md` 也通过，因为那位人类记得在改正文的同时把 footer 一起更新。",

    "**Cost audit.** LLM calls: zero for L1; none for L3 unless the human invoked one. Human review scope: one page (`architecture.md`), which is a genuinely structural change and *deserves* human attention. Compare with the naive baseline (\"regenerate every page that mentions `runSync`\"), which would have produced three LLM-generated diffs for the reviewer to wade through, two of which should never have been generated.":
        "**成本审计。** LLM 调用次数：L1 为零；L3 为零，除非人类主动调了一次。人工评审范围：一个页面（`architecture.md`），而那确实是一次结构性变更， * 本来就该 * 交给人。与朴素基线（“对每一个提到 `runSync` 的页面都重新生成”）对比一下：那种做法会产出三份 LLM 生成的 diff 给评审者去蹚，其中两份本来就 * 不该被生成 * 。",

    "Why \"rule first\" beats \"LLM first\"":
        "为什么“rule first”胜过“LLM first”",

    "It is tempting, with cheap LLMs, to skip L1 entirely and hand every candidate to L2. Do not. Three reasons, in decreasing order of importance:":
        "在 LLM 变便宜以后，很容易想完全跳过 L1、把每一个候选都扔给 L2。不要这么干。按重要性递减排三个理由：",

    "**Human attention.** Every LLM call produces a diff a human reviews. Ten L1 wins a week is ten reviews saved. One hundred is 100.":
        "**人类注意力。** 每一次 LLM 调用都会产出一份要被人评审的 diff。一周十次 L1 命中 = 十次被省下来的评审。一百次就是 100 次。",

    "**Determinism.** L1 rules have the same answer every time. L2 does not — the same prompt with the same model at temperature 0 can produce subtly different prose on different days as models are upgraded. For anything a rule can handle, having the rule be the source of truth is more stable.":
        "**确定性。** L1 规则每次给出的答案都相同。L2 不会 —— 同一段提示词、同一个模型、temperature 0，也可能因为模型在不断升级，在不同日子产出略有差别的文字。凡是规则能搞定的事，把规则作为 source of truth 更稳定。",

    "**Privacy.** L1 runs entirely on local filesystem and git. L2 sends page content, diffs, and prompts to a model provider. Chapter 22 unpacks the privacy implications; suffice it to say here that a rule-first discipline reduces the surface area of things sent to third parties, simply by handling more cases before the LLM is consulted.":
        "**隐私。** L1 完全跑在本地文件系统和 git 上。L2 会把页面内容、diff 和提示词发给模型提供方。第 22 章会把隐私方面的影响讲透；这里只需要说一句：rule-first 纪律会让更多案例在调 LLM 之前就被处理掉，从而直接缩小“发给第三方的东西”的表面积。",

    "When L2 is the right choice": "什么时候 L2 才是正确选择",

    "L2 is for the case that genuinely exists between L1 (too mechanical) and L3 (too structural): a localised content change where an LLM can do, in a few thousand tokens, what a human would do in ten minutes but with a higher per-minute cost. Function renames, type-signature changes, parameter additions, documentation for a straightforwardly new helper function — these all land cleanly in L2 because a human reviewer can verify the one-paragraph diff quickly.":
        "L2 对应那种确确实实落在 L1（太机械）和 L3（太结构性）之间的情形：一次局部的内容变更 —— LLM 用几千 token 就能做的事，人要花十分钟、而且每分钟成本更高。函数重命名、类型签名变更、加一个参数、为一个明显新增的 helper 函数补文档 —— 这些都能干净地落在 L2，因为人类评审者可以很快核对一份一段长度的 diff。",

    "L2 is *not* for cross-page consistency (the LLM does not see the other pages), not for architectural rewrites (not enough context), and not for new content (there is no \"page to patch\"). Putting those cases through L2 produces plausible-looking output that a reviewer has to correct anyway, so nothing is gained.":
        "L2 * 不 * 适合做跨页一致性（LLM 看不到别的页面），不适合做架构性重写（上下文不够），也不适合做“从零的新内容”（根本没有“被打补丁的页面”）。把这些情形塞进 L2，只会产出看起来像样、但评审者反正都得改一遍的输出，等于什么都没赚到。",

    "A week of real operation, summarised as a batch report — the kind of output a Friday-afternoon digest posts to the team's channel:":
        "真实运营一周之后，汇总为一份批量报告 —— 周五下午推送到团队频道的那种摘要：",

    "Two points of interest. First, L1 handled 63% of the week's candidates for zero cost. Second, the reviewer's queue was two items — both genuinely requiring human thought — not nineteen. That ratio, not the token cost, is the metric the operational model actually optimises for.":
        "有两点值得留意。其一，L1 以零成本处理掉了这一周 63% 的候选。其二，评审者的队列里只有两项 —— 两项都是真的需要人去想的 —— 而不是十九项。这个比例，而不是 token 成本，才是运维模型真正在优化的指标。",

    "Maintenance is not a single problem; it is three problems pretending to be one. L1 is a filesystem-and-git problem. L2 is an LLM problem with bounded context. L3 is a human problem that the machinery should stay out of. Routing correctly between them — rule first, LLM second, human for structural change — is what makes a KB sustainable as the code beneath it accelerates.":
        "维护不是一个问题；它是三个“伪装成一个”的问题。L1 是一个文件系统与 git 的问题。L2 是一个上下文受限的 LLM 问题。L3 是一个“机器应当退开”的人类问题。在这三者之间做正确的路由 —— rule first、LLM second、人来管结构性变更 —— 就是让一个知识库在它脚下的代码加速时仍然可持续的关键。",

    "Part IV's three chapters have now laid out the whole loop: detect candidates (ch14), check them against hard and soft gates (ch15), dispatch them through the three levels (ch16). The next two parts (V and VI) put this loop to work: Chapter 18 uses the footer's review state as the fourth axis of document layering, and Chapter 21 asks what happens when an agent — not a human — consumes the output.":
        "至此，第四部分的三章已经铺出了整条回路：检测候选（第 14 章）、用硬软门禁检验它们（第 15 章）、把它们经由三级派发出去（第 16 章）。接下来的两部分（V 和 VI）会让这条回路真正运转起来：第 18 章会把 footer 的评审状态作为文档分层的第四根轴；第 21 章会问：当“消费输出”的不是人、而是一个 agent 时，会发生什么？",
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
    applied, remaining, unmatched = apply("ch16-maintenance-drift-and-link-rot", CH16)
    print(f"ch16-maintenance-drift-and-link-rot           applied={applied:3d}  remaining_untranslated={remaining:3d}  unmatched_keys={len(unmatched)}")
    for key in unmatched:
        print(f"   UNMATCHED: {key[:80]!r}")
        failed = 1
    return failed


if __name__ == "__main__":
    sys.exit(main())
