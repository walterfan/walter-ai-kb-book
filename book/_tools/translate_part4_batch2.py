"""Apply Chinese translations for Part IV batch 2: ch15.

Run with: poetry run python book/_tools/translate_part4_batch2.py
"""

from __future__ import annotations

import os
import sys
import polib

LOCALE_ROOT = "book/locale/zh_CN/LC_MESSAGES/part4-operations-lifecycle"


CH15: dict[str, str] = {
    "Chapter 15 — Evaluation, Benchmarks, and Publish Gates":
        "第 15 章 —— 评测、基准与发布门禁",

    "Why": "Why —— 为什么",
    "What": "What —— 是什么",
    "How": "How —— 怎么做",
    "Example": "Example —— 范例",
    "Conclusion": "Conclusion —— 小结",
    "References": "参考文献",

    "A KB that cannot answer *\"how do I know this build is good?\"* cannot claim to be maintained. The question has two honest decompositions, and this chapter treats both:":
        "一个回答不了 * “我怎么知道这次 build 好不好？” * 的知识库，就不能自称被“维护着”。这个问题有两种诚实的拆解，本章把两种都讲一遍：",

    "**Evaluation** — *how good is the retrieval + generation system the KB powers?* This is the IR-literature question: precision at k, nDCG, answer-faithfulness. Benchmarks like BEIR {cite}`thakur2021beir` and RAGAS {cite}`es2024ragas` exist because different teams converged on needing the same answer.":
        "**评测** —— * 这个知识库驱动的检索 + 生成系统有多好？ * 这是 IR 文献里的那个问题：precision@k、nDCG、answer-faithfulness。BEIR {cite}`thakur2021beir` 和 RAGAS {cite}`es2024ragas` 这些 benchmark 之所以存在，是因为不同团队在“需要同一个答案”这件事上独立收敛到了一起。",

    "**Gating** — *is this specific build of the KB well-formed enough to publish?* This is the build-engineering question: is every page's footer present, do references resolve, did a human review the changed pages? It is the question Chapter 7a's C4 asks, and the one IR benchmarks do not directly help with.":
        "**门禁** —— * 这次具体构建出来的知识库，足够规范以至于可以发布吗？ * 这是构建工程的那类问题：每个页面的 footer 存在吗？引用能不能解析？变更的页面有没有被人评审过？这是第 7a 章 C4 所问的问题，而 IR 类 benchmark 对这种问题并无直接帮助。",

    "Evaluation tells you *how* good. Gating tells you *whether* to ship. The two complement each other: a KB that publishes without gates will eventually fail evaluation because malformed pages accumulate; a KB that evaluates without gating produces beautiful numbers against a snapshot that cannot actually be deployed.":
        "评测告诉你 * 好到什么程度 * 。门禁告诉你 * 要不要发 * 。两者互补：一个没有门禁就放出去的知识库，最终会因为结构不合规的页面不断累积，在评测上失分；一个只做评测、不做门禁的知识库，拿出来的漂亮数字，对应的是一个根本无法真正部署的快照。",

    "The gate catalogue in this chapter is adapted from the author's project-knowledge-base toolkit {cite}`fanyamin_pkb_skill`, with one added column — *enforced by* — that maps every gate to a specific piece of CI machinery. The prior art in the toolkit leaves enforcement implicit; making it explicit is this book's contribution.":
        "本章列出的门禁目录源自作者的 project-knowledge-base 工具包 {cite}`fanyamin_pkb_skill`，并新增了一列 —— * 由谁强制执行 * —— 把每一条门禁映射到一段具体的 CI 机制。原工具包的做法对“强制”是隐式处理的；把它显式化是本书的一份贡献。",

    "Evaluation": "评测",

    "For the code-layer retrieval system (Chapter 12), the useful metrics are the standard IR ones against a held-out test set of question/citation pairs: nDCG@10, recall@10, MRR. For the prose-layer retrieval, these metrics apply with a caveat: the ground truth is harder to label (a single question often has multiple correct pages), and partial credit matters more. Both surfaces benefit from the end-to-end answer-faithfulness metrics in RAGAS {cite}`es2024ragas` and similar frameworks.":
        "对代码层检索系统（第 12 章）而言，有用的指标就是那些标准的 IR 指标：在一份留出的 `(问题, 引用)` 对测试集上跑 nDCG@10、recall@10、MRR。对文稿层检索，这些指标同样适用，但有一个注脚：ground truth 更难标注（同一个问题常常对应多个正确页面），并且“部分得分”更重要。两类面板都能从 RAGAS {cite}`es2024ragas` 及其同类框架里的“端到端 answer-faithfulness”指标中获益。",

    "A concrete starting set:": "一个可以直接上手的初始指标集：",

    "Metric": "指标",
    "Layer": "层",
    "What it measures": "它度量的是什么",
    "Benchmark corpus": "基准语料",

    "nDCG@10": "nDCG@10",
    "code": "代码",
    "Are the top-10 retrieved entities ranked correctly?":
        "前 10 个被检索出的实体排序对不对？",
    "Held-out `(question, code_entities)` pairs":
        "留出的 `(问题, code_entities)` 对",

    "Recall@10": "Recall@10",
    "Did we at least find the right entities?": "我们至少把正确的实体找到了没有？",
    "Same": "同上",

    "Answer faithfulness (RAGAS)": "Answer faithfulness（RAGAS）",
    "prose+code": "文稿 + 代码",
    "Does the generated answer cite its own context?":
        "生成的答案是否引用了它自己看到的上下文？",
    "RAGAS pipeline on sample Q&A": "在样本 Q&A 上跑 RAGAS 流水线",

    "Citation resolve-rate": "引用解析率",
    "Do the `file:line` anchors in generated answers resolve at HEAD?":
        "生成答案中的 `file:line` 锚点能否在 HEAD 处解析成功？",
    "Every generated answer": "每一条生成答案",

    "BEIR-style domain scores": "BEIR 式的领域分数",
    "prose": "文稿",
    "How does retrieval quality compare against public IR corpora?":
        "检索质量与公开 IR 语料相比如何？",
    "BEIR {cite}`thakur2021beir`": "BEIR {cite}`thakur2021beir`",

    "Evaluation numbers should be tracked over time on a fixed benchmark set; a single nDCG@10 = 0.74 is not a claim, but a move from 0.74 to 0.71 after a sync is.":
        "评测数字应当在一个固定的基准集上沿时间线追踪；单独一个 nDCG@10 = 0.74 不是什么主张，但一次同步之后从 0.74 变成 0.71 就是了。",

    "Gates": "门禁",

    "Gates are the *build-engineering* question. Every gate is a mechanical check that runs on CI and returns pass or fail. The catalogue distinguishes **hard** gates (block publish; non-zero exit) from **soft** gates (warn; allow publish but flag the reviewer).":
        "门禁属于 * 构建工程 * 的问题。每一条门禁都是一个跑在 CI 上、只返回 pass / fail 的机械检查。目录把它们区分为 **硬门禁** （阻止发布，非零退出码）和 **软门禁** （发警告，允许发布但提醒评审者）。",

    "Hard gates — block publish": "硬门禁 —— 阻止发布",

    "#": "#",
    "Name": "名称",
    "What it checks": "它检查的是什么",
    "Enforced by": "由谁强制执行",

    "H1": "H1",
    "Footer present": "Footer 存在",
    "Every content page has a well-formed `PKB-metadata` footer":
        "每个内容页都带一个格式良好的 `PKB-metadata` footer",
    "`check_frontmatter.py` extension": "`check_frontmatter.py` 扩展",

    "H2": "H2",
    "Footer fields valid": "Footer 字段合法",
    "`review_status` ∈ {`pending`, `approved`}; `updated_by` ∈ {`human`, `ai`, `ai+human`}; `review_score` ∈ [0,5]":
        "`review_status` ∈ {`pending`, `approved`}；`updated_by` ∈ {`human`, `ai`, `ai+human`}；`review_score` ∈ [0,5]",

    "H3": "H3",
    "AI-approval consistency": "AI 审批一致性",
    "No page has `review_status: approved` with empty `reviewed_by`":
        "不允许出现“`review_status: approved` 但 `reviewed_by` 为空”的页面",

    "H4": "H4",
    "Citations resolve": "引用可解析",
    "Every `file:line` anchor in every page points at an existing line at HEAD":
        "每个页面里的每一个 `file:line` 锚点在 HEAD 处都指向真实存在的行",
    "`verify` step (Chapter 7)": "`verify` 步骤（第 7 章）",

    "H5": "H5",
    "Links resolve": "链接可解析",
    "Every internal `](*.md#*)` link points at an existing anchor":
        "每一个内部 `](*.md#*)` 链接都指向真实存在的锚点",
    "`verify` step": "`verify` 步骤",

    "H6": "H6",
    "Excerpts provenance": "excerpt 出处可验证",
    "Every vendored excerpt's `content_sha256` matches the current file":
        "每段 vendored excerpt 的 `content_sha256` 与当前文件一致",
    "`refresh_excerpts.py --check`": "`refresh_excerpts.py --check`",

    "H7": "H7",
    "No `[TODO]` / `[FIXME]` in published pages":
        "已发布页面中不得出现 `[TODO]` / `[FIXME]`",
    "Pages with `status: published` contain no unresolved markers":
        "带 `status: published` 的页面里不能含有未处理的标记",
    "grep-style check": "grep 风格的检查",

    "Each hard gate corresponds to one specific thing that can be false about the KB and should block the deploy. H1–H3 enforce C2 (footer is observable and honest). H4–H6 enforce that citations and excerpts remain trustworthy. H7 catches the most common \"we forgot\" failure.":
        "每条硬门禁都对应着知识库中“可能为假、且一旦为假就必须阻止发布”的一件具体事。H1–H3 强制 C2（footer 可观测且诚实）。H4–H6 强制“引用与 excerpt 持续可信”。H7 则负责抓最常见的那种“哎呀我们忘了”的失误。",

    "Soft gates — warn but allow": "软门禁 —— 发警告，但允许发布",

    "What it warns about": "它警告的是什么",

    "S1": "S1",
    "Stale footers": "footer 陈旧",
    "Any page's footer `commit:` is more than N commits behind HEAD":
        "任何页面的 footer `commit:` 距 HEAD 超过 N 个 commit",
    "`check-staleness.py`": "`check-staleness.py`",

    "S2": "S2",
    "Low review score": "评审分数过低",
    "Any published page has `review_score` < 2":
        "任何已发布页面的 `review_score` < 2",
    "Footer scan": "扫描 footer",

    "S3": "S3",
    "Imbalanced Diátaxis": "Diátaxis 失衡",
    "The published KB has no how-to pages (or no tutorial, etc.)":
        "已发布的知识库里没有 how-to 页面（或没有 tutorial，等等）",
    "Histogram over `doc_type`": "对 `doc_type` 做直方图",

    "S4": "S4",
    "Answer-faithfulness regression": "answer-faithfulness 回归",
    "Nightly RAGAS-style scores fell > 5% from last build":
        "夜间 RAGAS 风格分数相比上一次构建下降 > 5%",
    "CI job": "CI 任务",

    "S5": "S5",
    "Coverage gap": "覆盖缺口",
    "A 10-page set (C1) page is missing": "10 页集合（C1）中缺了某一页",
    "`required_pages.txt` check": "`required_pages.txt` 检查",

    "Soft gates are honest warnings, not release blockers. A KB with an S3 warning is still a KB; it just has a reviewer-visible reminder that it is drifting away from its own page-set commitments.":
        "软门禁是诚实的警告，不是发布阻塞项。一个带着 S3 警告的知识库仍然是知识库；它只不过多了一条评审者可见的提醒：“你正在偏离自己对页面集合做出的承诺”。",

    "The gate runner": "门禁 runner",

    "The gate system is a single CI script that runs every check and aggregates results. A minimal implementation:":
        "整个门禁系统就是一个 CI 脚本：逐条跑每项检查并汇总结果。一个最小实现：",

    "Every gate exposes the same interface: a `check()` method that returns `(ok, detail)` and a stable `name`. This lets the CI script stay short — it is the gates themselves that hold the domain knowledge — and lets every gate be tested in isolation.":
        "每条门禁都暴露相同的接口：一个返回 `(ok, detail)` 的 `check()` 方法和一个稳定的 `name`。这让 CI 脚本本身很短 —— 领域知识被封装在门禁自身里 —— 并且让每条门禁都可以单独测试。",

    "The gate report": "门禁报告",

    "The output of a gate run is a two-section report: hard failures (if any) followed by soft warnings. The report is Markdown, committed to the build artefacts, and linked from the PR that triggered the build:":
        "一次门禁跑完的输出是一份两段式报告：硬失败（如果有的话）在前，软警告在后。报告是 Markdown 格式的，作为 build artefact 落盘，并从触发本次构建的 PR 处链过来：",

    "Hard-failure exit codes block the CI publish step; soft warnings are appended to the PR as a comment so the reviewer sees them without CI going red.":
        "硬失败退出码会阻塞 CI 的发布步骤；软警告作为评论追加到 PR 里，这样 CI 不至于红掉，评审者仍然能看到它们。",

    "A worked failure": "一次具体的失败",

    "Suppose a PR adds a new function to `internal/worker/pool.go` — good faith addition, no rename, no break. The author also edits `architecture.md` to mention the new function and, while there, adds a `<!-- TODO: add diagram -->` marker intending to come back later.":
        "假设有一个 PR 往 `internal/worker/pool.go` 里加了一个新函数 —— 诚意新增，无重命名、无破坏性改动。作者顺手编辑了 `architecture.md` 来提到这个新函数，并在那儿加了个 `<!-- TODO: add diagram -->` 标记，打算以后回来补。",

    "Run the gates:": "跑一遍门禁：",

    "**H1 Footer present.** Pass. `architecture.md` has a footer.":
        "**H1 Footer 存在。** 通过。`architecture.md` 有 footer。",

    "**H2 Footer fields valid.** Pass. Fields are well-formed.":
        "**H2 Footer 字段合法。** 通过。字段都格式良好。",

    "**H3 AI-approval consistency.** Pass. The author set `updated_by: human`, `review_status: pending`, `review_score: 0`, `reviewed_by:`. Everything consistent.":
        "**H3 AI 审批一致性。** 通过。作者设了 `updated_by: human`、`review_status: pending`、`review_score: 0`、`reviewed_by:`。一切自洽。",

    "**H4 Citations resolve.** Pass. The new function's `file:line` resolves.":
        "**H4 引用可解析。** 通过。新函数的 `file:line` 能解析成功。",

    "**H5 Links resolve.** Pass.": "**H5 链接可解析。** 通过。",

    "**H6 Excerpts provenance.** Pass.": "**H6 excerpt 出处可验证。** 通过。",

    "**H7 No `[TODO]` in published pages.** **FAIL.** The `<!-- TODO -->` marker is in a page with `status: published`.":
        "**H7 已发布页面不得含 `[TODO]`。** **失败。** `<!-- TODO -->` 标记出现在了一个 `status: published` 的页面里。",

    "The gate blocks publish. The reviewer sees a single-line failure and a pointer to line 47 of the diff. Cost of the check: a grep across `content/**/*.md` that finished in 30 ms. Cost of having skipped the check: a production KB that publishes a page whose diagram says \"TODO\", which a user sees and loses a small amount of trust over. That trust does not come back for free.":
        "门禁阻止了发布。评审者看到的是一行失败信息 + 一个指向 diff 第 47 行的指针。本次检查的成本：对 `content/**/*.md` 的一次 grep，在 30 ms 内完成。跳过这次检查的成本：线上知识库发布了一个图示写着“TODO”的页面 —— 有用户看到了，对它的信任感轻微折损。这种折损不会自己免费恢复。",

    "A full gate run from a real Friday-afternoon PR (numbers anonymised):":
        "一次真实周五下午 PR 上的完整门禁跑动（数据已匿名化）：",

    "The author sees three specific things to fix, not a 400-file review queue. Fixing them takes perhaps ten minutes: one page's `reviewed_by` field gets filled in, one citation gets updated to the new line number, one broken `file:line` gets repointed to the file that replaced `cmd/sync/main.go`. Re-run the gates: all pass. Publish proceeds.":
        "作者看到的是三件具体要修的事，而不是一份 400 个文件的评审队列。修完这三件大约花 10 分钟：一个页面的 `reviewed_by` 字段被补上，一条引用被更新到新的行号，一条坏掉的 `file:line` 被重新指向替代 `cmd/sync/main.go` 的那个文件。重跑门禁：全部通过。发布继续。",

    "Evaluation (IR metrics, faithfulness scores) tells you whether the KB is useful once published. Gating (hard and soft checks) tells you whether this specific build is publishable at all. Both are mechanical. Both are cheap. Both are refused by most KBs today, because adding them requires committing to the four corners of Chapter 7a — if the footer is not there, H1 cannot run; if the operational model does not resolve citations, H4 cannot run.":
        "评测（IR 指标、faithfulness 分数）告诉你：知识库一旦发布出去是否有用。门禁（硬 / 软检查）告诉你：这一次具体构建是否根本就“可以发”。两者都是机械的，都很便宜。但今天大多数知识库两者都拒绝上 —— 因为要加它们，就得对第 7a 章那四个角落做出承诺：footer 不在，H1 就跑不起来；运维模型不解析引用，H4 就跑不起来。",

    "The next chapter closes the loop: when a hard gate fails or a soft gate warns, *what does the fix look like?* The answer is the three-level update strategy (C3), the actual mechanics of which have been previewed here but belong to Chapter 16.":
        "下一章把整条回路闭合：当硬门禁失败、或软门禁告警时， * 修复到底长什么样？ * 答案就是三级更新策略（C3）—— 它的真正机制在本章已经先铺了一下，但正经讲述属于第 16 章。",
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
    applied, remaining, unmatched = apply("ch15-evaluation-and-benchmarks", CH15)
    print(f"ch15-evaluation-and-benchmarks                applied={applied:3d}  remaining_untranslated={remaining:3d}  unmatched_keys={len(unmatched)}")
    for key in unmatched:
        print(f"   UNMATCHED: {key[:80]!r}")
        failed = 1
    return failed


if __name__ == "__main__":
    sys.exit(main())
