"""Chinese translations for book/part2-prose-layer/ch07a-prose-operational-model.md.

See book/_tools/translations/ch02-ir-rag-primer.zh.py for the full
style guide. Chapter-specific notes:

- C1/C2/C3/C4 labels kept as-is (they are identifiers referenced
  across the book).
- L1/L2/L3 (level) labels kept as-is.
- review_status, review_score, reviewed_by, updated_by, last_updated,
  commit: keep English because they are field names in the YAML/HTML
  footer schema.
- `approved` / `pending` / `human` / `ai` / `ai+human`: keep English
  because they are enum values authors and scripts match against.
- "footer" kept in English (paired concept with "frontmatter").
- "PKB-metadata" kept in English (literal token in the HTML comment).
- CLI, Git, CI, ADR, LLM, SHA, API, JSON, SSE, Mermaid kept in English.
- Alice kept as a proper noun (demo user); not localised.
- CommonMark emphasis rule: insert ASCII space around `*...*` when
  flanked by CJK characters.
"""

PO_PATH = "part2-prose-layer/ch07a-prose-operational-model.po"

TRANSLATIONS: dict[str, str] = {
    # ---- Title / section headings ----
    "Chapter 7a — The Prose-Layer Operational Model": (
        "第 7a 章 —— 文稿层的运维模型"
    ),
    (
        "This chapter at a glance — the four corners that together "
        "let a KB answer *\"is the prose correct, at this commit, "
        "and does anyone know?\"*, the single worked scenario that "
        "traces an API change through all four, and an honest list "
        "of what the model does *not* claim to solve:"
    ): (
        "本章一页速览 —— "
        "四个角合在一起，"
        "让一个知识库可以回答 *“这段文稿在当前 commit 上是不是正确的？"
        "有没有人知道？”* ；"
        "再走一个具体场景，"
        "把一次 API 变更怎么穿过这四个角**一笔画完**；"
        "最后再诚实地列一份 —— "
        "这个模型 *并不* 声称自己能解决的那些问题："
    ),
    "Why": "为什么",
    "What": "是什么",
    "How": "怎么做",
    "Example": "示例",
    "Conclusion": "结论",
    "References": "参考文献",
    "C1 — Opinionated page set": "C1 —— 固定的页面集",
    "C2 — Metadata footer": "C2 —— 元数据 footer",
    "C3 — Three-level update strategy": "C3 —— 三级更新策略",
    "C4 — Verification gates": "C4 —— 校验闸",

    # ---- Why ----
    (
        "Chapters 4–7 have been about *getting prose in*: a "
        "file-based wiki, a frontmatter-plus-footer contract, a "
        "classification pipeline, a built site with search. "
        "Everything in those four chapters is a one-way pipeline "
        "— something arrives, something is produced, and the "
        "chapter ends."
    ): (
        "第 4 到第 7 章讲的都是 *把文稿收进来* ："
        "基于文件的 wiki，"
        "frontmatter 加 footer 的契约，"
        "分类流水线，"
        "以及一个带搜索的已构建站点。"
        "这四章里的一切都是单向流水线 —— "
        "进来一个东西，产出一个东西，"
        "章节就结束了。"
    ),
    (
        "A real knowledge base does not end there. The code "
        "underneath the prose changes every day. A function the "
        "architecture page describes gets renamed. A workflow the "
        "runbook describes gains a new step. A public API the "
        "reference page claims returns JSON now also emits "
        "Server-Sent Events. None of this is news to anyone who "
        "has maintained documentation. What is news, now that "
        "LLMs can rewrite pages for pennies, is that the "
        "constraint has shifted. The question is no longer *\"is "
        "it cheap enough to update the docs?\"* — it almost "
        "always is. The question is *\"did a human sign off on "
        "the update, and if so, which human, and when?\"* The "
        "bottleneck is not embedding cost or LLM cost; at "
        "`text-embedding-3-small`'s 2024 prices, a full re-embed "
        "of a 100-kLOC repo is under a dollar "
        "{cite}`openai_embeddings_v3`. The bottleneck is **human "
        "attention**. A KB that burns that attention with a "
        "400-file pull request every week ends up trusted by no "
        "one — not because it is wrong, but because nobody has "
        "the time to confirm it is right."
    ): (
        "真实世界的知识库不会到这里就结束。"
        "文稿底下的代码每天都在变。"
        "架构页描述的那个函数被改名了。"
        "runbook 描述的那个流程多了一个步骤。"
        "reference 页声称返回 JSON 的公开 API，"
        "现在还会发 Server-Sent Events。"
        "这些东西对任何维护过文档的人来说都不是新闻。"
        "**真正的新闻**是：既然 LLM 已经便宜到可以用几分钱改写一页文档，"
        "**约束条件已经转移了**。"
        "问题不再是 *“改文档还划不划算？”* —— "
        "几乎一直划算。"
        "问题变成了 *“这次改动有没有被人签字确认？"
        "如果有，是哪位人，在什么时候签的？”* "
        "瓶颈不是 embedding 成本，也不是 LLM 成本；"
        "以 `text-embedding-3-small` 在 2024 年的价格来算，"
        "把一个 10 万行代码的仓库整体重新 embed 一遍"
        "也就一美元以内 {cite}`openai_embeddings_v3` 。"
        "瓶颈是 **人类的注意力**。"
        "一个每周扔出 400 文件 pull request 的知识库，"
        "最后谁都不信 —— "
        "不是因为它写错了，"
        "而是因为没人有空去确认它写对了。"
    ),
    (
        "This chapter introduces the operational model the rest "
        "of the book relies on. It is an instantiation of "
        "discipline the author has refined in a private "
        "project-knowledge-base toolkit {cite}`fanyamin_pkb_skill`; "
        "this chapter names and explains the structure, and "
        "Chapters 14–16 unpack each piece in operational detail. "
        "The model has exactly four corners. Every later claim "
        "about how the prose layer stays correct reduces to one "
        "of them."
    ): (
        "这一章要介绍的是本书后面所有章节都要依赖的那个**运维模型**。"
        "它是作者在一个私人"
        "project-knowledge-base 工具集里"
        "一点点打磨出来的那套纪律的一个具象化"
        "{cite}`fanyamin_pkb_skill` ；"
        "这一章负责给那套结构起名字、讲清楚骨架，"
        "第 14–16 章再把每一块展开到可运维的颗粒度。"
        "这套模型**刚好有四个角**。"
        "本书后面一切关于“文稿层怎么保持正确”的论断，"
        "归根结底都能归约到其中某一个角。"
    ),

    # ---- What ----
    (
        "The model is a set of four corners. Together they answer "
        "*\"is the prose correct, at the current commit, and does "
        "anyone know?\"* Each corner has a short label (C1–C4) "
        "that other chapters use to refer to it without "
        "re-stating the model:"
    ): (
        "这个模型就是四个角的集合。"
        "把它们摆在一起，要回答的是 "
        "*“这段文稿在当前这个 commit 上是不是正确的？"
        "有没有人知道？”* "
        "每个角都有一个短标签（C1–C4），"
        "其他章节在引用它们时用标签就够了，"
        "不用把模型再重述一遍："
    ),
    "**C1 — Opinionated page set.** *Which pages should a KB have?*": (
        "**C1 —— 固定的页面集。** *一个知识库应该有哪些页面？*"
    ),
    "**C2 — Metadata footer.** *Is this specific page still trusted?*": (
        "**C2 —— 元数据 footer。** *这一页，现在还值不值得信？*"
    ),
    "**C3 — Three-level update strategy.** *Who pays to keep it correct?*": (
        "**C3 —— 三级更新策略。** *让它保持正确，代价由谁来付？*"
    ),
    "**C4 — Verification gates.** *What must be true before we publish?*": (
        "**C4 —— 校验闸。** *发布之前，有哪些条件必须成立？*"
    ),

    # ---- C1 body ----
    (
        "A KB that ships with free-form directories quickly grows "
        "a folder called `misc/` that no one searches. A KB that "
        "commits to a small, fixed set of pages gives readers a "
        "shape to remember and tools a shape to target. Chapter "
        "3's *One opinionated instantiation* section proposed "
        "ten pages (`overview`, `quick-start`, `architecture`, "
        "`repo-map`, `data-and-api`, `workflows`, `conventions`, "
        "`testing`, `runbook`, `observability`). C1 is that list, "
        "elevated to a corner of the operational model. The "
        "substance lives in Chapter 3; the rule lives here. "
        "**Having *some* stable page set is more important than "
        "arguing about which set.**"
    ): (
        "一个让目录随便长的知识库，"
        "很快就会长出一个谁都不搜的 `misc/` 文件夹。"
        "一个肯承诺“就这几页”的知识库，"
        "则给了读者一个能记住的形状、"
        "也给了工具一个可以瞄准的形状。"
        "第 3 章 *One opinionated instantiation* 那一节"
        "已经提过十页的建议清单"
        "（ `overview` 、 `quick-start` 、 `architecture` 、"
        "`repo-map` 、 `data-and-api` 、 `workflows` 、"
        "`conventions` 、 `testing` 、 `runbook` 、 `observability` ）。"
        "C1 就是那张清单 —— 被抬到运维模型里的一个角的位置。"
        "内容留在第 3 章，**规则**留在这里。"
        "**有 *某一套* 稳定的页面集，"
        "比争论“到底哪一套”要重要得多。**"
    ),

    # ---- C2 body ----
    (
        "Every content page ends with an HTML-comment footer "
        "with six fields, introduced in Chapter 5:"
    ): (
        "第 5 章已经介绍过："
        "每一张内容页都以一段 HTML-comment footer 收尾，"
        "这段 footer 有六个字段："
    ),
    (
        "<!-- PKB-metadata\n"
        "last_updated: 2026-04-14\n"
        "commit: 4a1c92b\n"
        "updated_by: ai            # human | ai | ai+human\n"
        "review_status: pending    # pending | approved\n"
        "review_score: 0           # 0-5\n"
        "reviewed_by:              # empty until a human reviews\n"
        "-->\n"
    ): (
        "<!-- PKB-metadata\n"
        "last_updated: 2026-04-14\n"
        "commit: 4a1c92b\n"
        "updated_by: ai            # human | ai | ai+human\n"
        "review_status: pending    # pending | approved\n"
        "review_score: 0           # 0-5\n"
        "reviewed_by:              # empty until a human reviews\n"
        "-->\n"
    ),
    (
        "C2's purpose is making staleness **observable**. Without "
        "the footer, a KB can only answer \"is this page stale?\" "
        "by re-reading the body and asking a human — which is "
        "expensive, slow, and exactly the thing the KB was "
        "supposed to eliminate. With the footer, a script can "
        "check `commit:` against `git rev-parse --short HEAD`, a "
        "reviewer can filter every page with `review_status: "
        "pending`, and an LLM agent (Chapter 21) can refuse to "
        "cite a page whose `review_score` is below a threshold. "
        "The full schema is in Chapter 5; C4 makes the footer's "
        "presence a build gate; C3 specifies who is allowed to "
        "set which values."
    ): (
        "C2 的目的是让**过时这件事变得可观测**。"
        "没有 footer 时，"
        "一个知识库要回答“这页是不是过期了？”"
        "只能把正文再读一遍、再找个人问一问 —— "
        "这件事**又贵又慢**，"
        "而它恰恰是当初建知识库时想解决的事。"
        "有了 footer 之后，"
        "一段脚本就可以把 `commit:` 和 `git rev-parse --short HEAD` 对一下，"
        "一个评审人可以一眼筛出所有 `review_status: pending` 的页，"
        "一个 LLM agent（第 21 章）"
        "甚至可以拒绝引用 `review_score` 低于某个阈值的页。"
        "完整的 schema 在第 5 章；"
        "C4 让“footer 必须存在”变成一道构建闸；"
        "C3 规定哪些值**可以**由谁来设置。"
    ),

    # ---- C3 body ----
    (
        "When something changes, *who* — or *what* — updates the "
        "docs? Naive approaches collapse to two: \"a human writes "
        "the update\" (too slow, almost never done) or \"an LLM "
        "regenerates everything\" (too noisy, floods review). "
        "Neither works. The author's skill "
        "{cite}`fanyamin_pkb_skill` splits updates into three "
        "levels, by the cost and the actor each level requires:"
    ): (
        "当底下发生变化时，"
        "到底**由谁**（或者**由什么**）来更新文档？"
        "朴素的做法往往坍塌到两种："
        "“让人写”（太慢，基本没人真在做），"
        "或者“让 LLM 把全部重新生成一遍”"
        "（太吵，评审人淹没在改动里）。"
        "两种都不成立。"
        "作者在那个私人 skill {cite}`fanyamin_pkb_skill` 里"
        "把更新拆成了**三级**，"
        "每一级对应的成本和所需的执行者都不同："
    ),
    "Level": "级别",
    "Trigger": "触发条件",
    "Actor": "执行者",
    "Token cost": "Token 成本",
    "Typical example": "典型例子",
    "**L1** Mechanical": "**L1** 机械级",
    (
        "File renamed; link broken; commit SHA drifted; repo-map "
        "files added or removed"
    ): (
        "文件重命名；链接失效；"
        "commit SHA 漂了；"
        "repo-map 里多了或少了文件"
    ),
    "Script (no LLM)": "脚本（不用 LLM）",
    "**0**": "**0**",
    (
        "Re-stamp `commit:` in the footer; fix broken `]()` "
        "link; regenerate `repo-map.md` from `git ls-files`"
    ): (
        "重新盖章 footer 里的 `commit:` ；"
        "修掉坏掉的 `]()` 链接；"
        "用 `git ls-files` 重新生成 `repo-map.md`"
    ),
    "**L2** Bounded-LLM": "**L2** 受限 LLM",
    (
        "Content drifted *but* the drift is localised to one "
        "page's diff"
    ): (
        "内容漂了， *但是* 这次漂移只局限在某一页的 diff 里"
    ),
    "LLM with narrow context: one page + its diff + its footer": (
        "上下文非常窄的 LLM：一页内容 + 它的 diff + 它的 footer"
    ),
    "~1–5 k tokens": "~1–5 k tokens",
    (
        "Function signature changed; regenerate the one "
        "paragraph of `data-and-api.md` that referenced it"
    ): (
        "函数签名改了；"
        "重新生成 `data-and-api.md` 里引用到它的那**一段**"
    ),
    "**L3** Human-led": "**L3** 人工主导",
    (
        "Architectural change, new ADR, cross-cutting refactor, "
        "security-sensitive content"
    ): (
        "架构变更、新写一份 ADR、"
        "横跨多个模块的重构、"
        "涉及安全性的内容"
    ),
    "Human writes; LLM copy-edits": "人写，LLM 做文字润色",
    "Variable; human-bounded": "浮动；受人本身的上限约束",
    "Rewrite `architecture.md` after splitting one service into two": (
        "把一个服务拆成两个之后，"
        "重写 `architecture.md`"
    ),
    "Two rules make the levels safe:": "有两条规则让这三级用起来是安全的：",
    (
        "**Rule first, LLM second.** Every change starts at L1. "
        "If L1 can handle it, no tokens are spent. Only changes "
        "that L1 cannot resolve fall through to L2; only changes "
        "too structural for L2 fall through to L3."
    ): (
        "**规则先，LLM 后。** "
        "每一次改动都先从 L1 开始。"
        "L1 能搞定的，一个 token 都不花。"
        "L1 搞不定的才往 L2 漏；"
        "L2 处理不了、太结构性的改动，才继续往 L3 漏。"
    ),
    (
        "**AI always sets pending.** When any automated path "
        "(L1 or L2) modifies a page, `review_status` goes to "
        "`pending`, `review_score` goes to `0`, and `reviewed_by` "
        "is cleared. Only a human — L3 or a later review — sets "
        "`approved` or a non-zero score. The rule is stated in "
        "Chapter 5 and enforced in Chapter 15."
    ): (
        "**AI 永远设回 pending。** "
        "任何自动化路径（L1 或者 L2）改过一页之后，"
        "`review_status` 必须回到 `pending` ，"
        "`review_score` 必须清零，"
        "`reviewed_by` 必须清空。"
        "只有**人**（L3，或之后的一次评审）"
        "才能把它置为 `approved` 、或者给出非零分数。"
        "这条规则在第 5 章定下，第 15 章强制执行。"
    ),
    (
        "Chapter 16 gives the full treatment, including a "
        "decision tree for routing changes through the three "
        "levels and a worked cost comparison against the naive "
        "\"re-embed everything\" baseline."
    ): (
        "第 16 章会完整展开这个主题，"
        "包括一棵决策树，用来把每次改动分流到三级里的某一级，"
        "还有一张对比表："
        "把这套策略和“一改就把整个仓库重新 embed 一遍”的朴素做法"
        "在成本上算给你看。"
    ),

    # ---- C4 body ----
    (
        "A gate that no one enforces is not a gate. C4 says: "
        "every claim the operational model makes — *\"the "
        "footer is present\", \"its fields are valid\", \"every "
        "file-line reference resolves at the current commit\", "
        "\"no raw `[TODO]` markers remain\"* — is a mechanical "
        "check that runs on CI, either as a hard gate (blocks "
        "publish) or a soft gate (warns without blocking). The "
        "full catalogue is in Chapter 15."
    ): (
        "**一道没人强制执行的闸，就不是闸。** "
        "C4 要讲的是：运维模型嘴上说出的每一条承诺 —— "
        "*“footer 必须存在”、"
        "“footer 里的字段必须合法”、"
        "“每一个 file-line 引用在当前 commit 上都能解析出来”、"
        "“不能留下任何裸的 `[TODO]` 标记”* —— "
        "都是一段跑在 CI 上的机械检查，"
        "要么作为**硬闸**（不通过就拦住发布），"
        "要么作为**软闸**（只报警、不拦）。"
        "完整的清单在第 15 章。"
    ),
    (
        "The gate system is what makes C2 and C3 real. Without "
        "gates, the footer is a suggestion; with gates, it is a "
        "contract. Without gates, the \"AI always sets pending\" "
        "rule is a hope; with gates, any page whose "
        "`review_status: approved` lacks a matching human "
        "`reviewed_by` fails the build."
    ): (
        "是**闸系统**让 C2 和 C3 从文字变成现实。"
        "没有闸，footer 只是**建议**；"
        "有了闸，footer 是**契约**。"
        "没有闸，"
        "“AI 永远设回 pending”只是**一个愿望**；"
        "有了闸，"
        "任何一页如果带着 `review_status: approved` "
        "却没有对应的人类 `reviewed_by` ，"
        "构建就会失败。"
    ),

    # ---- How ----
    (
        "The four corners connect through a single worked "
        "scenario. Suppose a public API route changes in the "
        "codebase — the endpoint `/api/v1/pages` gains a new "
        "query parameter. Here is what happens, in order:"
    ): (
        "这四个角怎么串起来？"
        "我们走一个具体的场景就清楚了。"
        "假设代码库里一个公开 API 路由改了 —— "
        "`/api/v1/pages` 这个 endpoint 多了一个查询参数。"
        "接下来按顺序会发生什么："
    ),
    (
        "**Change detection (Chapter 14 via C2).** A nightly "
        "job diffs `git HEAD` against the set of `commit:` "
        "values in every footer. It finds that `data-and-api.md` "
        "and `api-reference.md` both list the old commit, and "
        "that the diff touches code the `api-reference.md` page "
        "cites by `file:line`. Two candidate pages."
    ): (
        "**变更检测（第 14 章，靠的是 C2）。** "
        "一个夜间任务把 `git HEAD` 和每一张 footer 里的 `commit:` 值比一遍，"
        "发现 `data-and-api.md` 和 `api-reference.md` 登记的都是旧 commit ，"
        "而这次 diff 刚好改到了 `api-reference.md` 用 `file:line` 引用过的代码。"
        "两张候选页。"
    ),
    (
        "**L1 dispatch (C3).** The job runs L1 checks on both "
        "candidates. For `data-and-api.md` the only drift is the "
        "footer SHA — the body still describes the route "
        "correctly. L1 re-stamps the footer: `commit:` bumps, "
        "`last_updated:` bumps, `updated_by: ai`, "
        "`review_status: pending` (the AI-always-sets-pending "
        "rule), `review_score: 0`. Zero tokens spent. For "
        "`api-reference.md` the drift is real — a paragraph "
        "references the old parameter list. L1 cannot fix that; "
        "it escalates."
    ): (
        "**L1 分流（C3）。** "
        "任务对两张候选页都跑一遍 L1 检查。"
        "`data-and-api.md` 的漂移只在 footer 的 SHA 上 —— "
        "正文还在正确地描述这个路由。"
        "L1 把 footer 重新盖一遍章： "
        "`commit:` 更新、 `last_updated:` 更新、"
        "`updated_by: ai` 、"
        "`review_status: pending` （AI 永远设回 pending 那条规则）、"
        "`review_score: 0` 。"
        "花费 0 个 token 。"
        "`api-reference.md` 则是真漂移 —— "
        "有一段引用了旧的参数列表。"
        "L1 处理不了，向上升级。"
    ),
    (
        "**L2 dispatch (C3).** An LLM is invoked with narrow "
        "context: the current `api-reference.md` body (~2 kB), "
        "the relevant code diff (~300 B), and the page's footer. "
        "It returns a new version of the one affected paragraph. "
        "The footer is re-stamped by the same rule: "
        "`review_status: pending`, `reviewed_by:` cleared. Cost: "
        "~2.3 k tokens — under a cent."
    ): (
        "**L2 分流（C3）。** "
        "用**很窄的上下文**调一次 LLM："
        "`api-reference.md` 现在的正文（大约 2 kB），"
        "相关代码 diff（大约 300 B），"
        "还有这一页的 footer 。"
        "LLM 返回受影响的**那一段**的新版本。"
        "footer 按同样的规则重新盖章： "
        "`review_status: pending` 、 `reviewed_by:` 清空。"
        "代价：大约 2.3 k tokens —— 不到一美分。"
    ),
    (
        "**Gate run (C4).** Before publish, hard gates fire. "
        "The footer is present on both pages and well-formed: "
        "pass. Every `file:line` reference in `api-reference.md` "
        "resolves at the current commit (including the new "
        "parameter, which L2 just referenced): pass. No `[TODO]` "
        "markers were introduced: pass. Mermaid is unchanged and "
        "still parses: pass. Publish proceeds."
    ): (
        "**闸检查（C4）。** "
        "发布前，硬闸全部触发。"
        "两张页面的 footer 都在、且字段合法：通过。"
        "`api-reference.md` 里所有 `file:line` 引用"
        "在当前 commit 上都解得出来"
        "（包括 L2 刚刚引用的那个新参数）：通过。"
        "没有引入新的 `[TODO]` 标记：通过。"
        "Mermaid 没动过，仍然能解析：通过。"
        "发布继续。"
    ),
    (
        "**Human review (C3 L3 → C2).** A reviewer sees two "
        "pages with `review_status: pending` in the KB's review "
        "dashboard, reads the two diffs (not 400 files — just "
        "two), approves both, and sets `review_score: 4` on "
        "each. The next L1 check against either page will leave "
        "`review_status` at `approved` because no body change "
        "has occurred."
    ): (
        "**人工评审（C3 里的 L3 → 写回 C2）。** "
        "评审人在知识库的评审面板上看到两张 `review_status: pending` 的页，"
        "把两份 diff 读一遍（不是 400 文件 —— 就两份），"
        "两张都 approve ，"
        "各给一个 `review_score: 4` 。"
        "下一次 L1 对这两张页再检查时，"
        "`review_status` 会继续停在 `approved` —— "
        "因为正文根本没被动过。"
    ),
    (
        "Nothing in that sequence is an experiment. Every step "
        "is a script or a rule that exists because one of the "
        "four corners puts it there. Change detection works "
        "because C2 made staleness observable. Routing works "
        "because C3 gave the levels a stable meaning. Publish "
        "only happens because C4 refused to let a malformed page "
        "through. And the next human who reads the docs can look "
        "at either page's footer and know, without asking "
        "anyone, that an LLM touched it and a named human has "
        "signed off."
    ): (
        "以上这段序列里，没有任何一步是实验。"
        "每一步不是一段脚本就是一条规则，"
        "而它们存在的唯一原因是四个角里某一个角把它安排在那里。"
        "变更检测能跑起来，是因为 C2 让过时这件事变得可观测。"
        "分流能跑起来，是因为 C3 给三级都赋予了稳定的含义。"
        "发布能发出去，是因为 C4 拒绝放行任何一张格式不对的页。"
        "而下一个打开这份文档的人，"
        "只要看任何一张页的 footer ，"
        "就能在不问任何人的情况下知道："
        "这一页被 LLM 改过，"
        "而且有一个具名的人已经签过字了。"
    ),

    # ---- Example ----
    (
        "Here is the minimal viable shape of the loop, told "
        "through one page's footer over a week:"
    ): (
        "把这个循环收缩到最小可用形态："
        "跟踪一张页的 footer 在一周里的变化，"
        "讲的就是下面这段："
    ),
    (
        "Monday  08:00  commit: a1b2c3d4  updated_by: human  "
        "review_status: approved   reviewed_by: alice\n"
        "                 (page written by Alice; nothing else "
        "changes all week)\n"
        "\n"
        "Monday  08:15  commit: a1b2c3d4  updated_by: human  "
        "review_status: approved   reviewed_by: alice\n"
        "                 (L1 runs against HEAD; commit still "
        "matches; no change)\n"
        "\n"
        "Wednesday 14:30  commit: 4a1c92b  updated_by: ai    "
        "review_status: pending    reviewed_by:\n"
        "                 (API changed; L2 regenerated one "
        "paragraph; footer reset)\n"
        "\n"
        "Thursday 10:05  commit: 4a1c92b  updated_by: ai+human  "
        "review_status: approved  review_score: 4  reviewed_by: "
        "alice\n"
        "                 (Alice read the L2 diff and approved)\n"
        "\n"
        "Friday  23:00  commit: 9f8e7d6c  updated_by: human  "
        "review_status: pending   reviewed_by:\n"
        "                 (an unrelated refactor moved a linked "
        "file; L1 fixed the broken link;\n"
        "                  review resets because the body was "
        "touched)\n"
    ): (
        "Monday  08:00  commit: a1b2c3d4  updated_by: human  "
        "review_status: approved   reviewed_by: alice\n"
        "                 （Alice 写了这一页；一整周再没动过）\n"
        "\n"
        "Monday  08:15  commit: a1b2c3d4  updated_by: human  "
        "review_status: approved   reviewed_by: alice\n"
        "                 （L1 对 HEAD 跑一次；commit 仍然一致；没变化）\n"
        "\n"
        "Wednesday 14:30  commit: 4a1c92b  updated_by: ai    "
        "review_status: pending    reviewed_by:\n"
        "                 （API 变了；L2 重新生成了一段；footer 被重置）\n"
        "\n"
        "Thursday 10:05  commit: 4a1c92b  updated_by: ai+human  "
        "review_status: approved  review_score: 4  reviewed_by: "
        "alice\n"
        "                 （Alice 读了 L2 的 diff 并批准）\n"
        "\n"
        "Friday  23:00  commit: 9f8e7d6c  updated_by: human  "
        "review_status: pending   reviewed_by:\n"
        "                 （一个无关的重构移动了一个被链接引用的文件；"
        "L1 修掉了坏链；\n"
        "                  正文被动过了，所以评审状态也重置）\n"
    ),
    (
        "Five states, one page, a full audit trail in its own "
        "footer. No side tables, no CI database, no review "
        "spreadsheet. A human reading the file in `cat` or `vim` "
        "learns the entire history. A script querying the KB "
        "gets a closed vocabulary (`approved | pending`, `human "
        "| ai | ai+human`, `0–5`) it can filter on with zero "
        "ambiguity."
    ): (
        "五个状态、一张页、一段完整的审计轨迹，"
        "全都躺在它自己的 footer 里。"
        "没有任何附表，没有任何 CI 数据库，没有任何评审电子表。"
        "一个人用 `cat` 或 `vim` 打开文件，"
        "就能把整段历史看完。"
        "一个脚本在查询这个知识库时，"
        "拿到的是一套**封闭词汇表**："
        "`approved | pending` ， `human | ai | ai+human` ， `0–5` —— "
        "可以零歧义地筛选。"
    ),
    (
        "The full L1/L2/L3 dispatcher, the change-detection "
        "layers that decide which pages are candidates, and the "
        "complete gate catalogue are the subjects of the next "
        "three chapters."
    ): (
        "L1/L2/L3 完整的分流器、"
        "决定哪些页面算候选的变更检测层、"
        "以及闸规则的完整清单，"
        "是接下来三章的主题。"
    ),

    # ---- What this model does NOT solve ----
    "What this model does *not* solve": "这个模型 *并没有* 解决的问题",
    (
        "The four corners make a KB's claims about its own "
        "correctness auditable. They do not, on their own, make "
        "the claims *true*. This distinction matters enough to "
        "state explicitly, because teams that treat the "
        "operational model as the whole job — rather than as the "
        "scaffolding for the job — drift into a specific and "
        "avoidable failure mode: a KB whose every page's footer "
        "says `approved` and whose content is still wrong."
    ): (
        "四个角做的事，"
        "是让一个知识库**关于自己正确性的那些说法**变得可审计。"
        "它们**并不**因此就让那些说法 *变成真话* 。"
        "这个区分值得专门说一遍，"
        "因为很多团队把运维模型当成**全部的活**，"
        "而不是**支撑那些活的脚手架**，"
        "结果漂到一种具体而又可避免的失败形态："
        "每一页的 footer 都写着 `approved` ，"
        "而内容仍然是错的。"
    ),
    "Four limits are worth naming.": "有四条边界值得点名说清楚。",
    (
        "**Gates check *form*, not *truth*.** The verification "
        "gates in C4 can mechanically confirm that the footer is "
        "present, that `file:line` references resolve at the "
        "current commit, and that no `[TODO]` markers remain. "
        "They cannot confirm that the paragraph *next to* a "
        "`file:line` anchor is a correct description of the "
        "function it points at. That check requires either a "
        "human reading the page or an LLM cross-reading the code "
        "— which is exactly what the three-level update strategy "
        "(C3) dispatches, but the dispatcher itself can no more "
        "verify semantic truth than the compiler can verify that "
        "a function does what its name claims."
    ): (
        "**闸只能检查 *形式* ，不能检查 *真相* 。** "
        "C4 里的校验闸可以机械地确认："
        "footer 在、 "
        "`file:line` 在当前 commit 上能解析出来、"
        "没有裸的 `[TODO]` 标记。"
        "但它们没法确认： "
        "`file:line` 锚点 *旁边* 的那一段，"
        "是否在正确地描述它指向的那个函数。"
        "这种检查需要一个人把页面读一遍，"
        "或者一个 LLM 把代码和文档交叉对读一遍 —— "
        "这恰恰是三级更新策略（C3）要分流的活；"
        "但**分流器本身**能验证的语义真相，"
        "不会比编译器能验证“一个函数是否真的做了它名字说的事”多多少。"
    ),
    (
        "**`approved` means \"a human read this diff\", not "
        "\"this is correct\".** The AI-always-sets-pending rule "
        "ensures that an `approved` page was signed off by a "
        "named human, and the gate catalogue ensures the human "
        "was looking at the current commit. Neither mechanism "
        "prevents a reviewer from approving a subtly-wrong L2 "
        "rewrite — because the reviewer was rushed, or because "
        "the wrongness is in a corner of the domain the reviewer "
        "does not know. The model makes review *traceable*, not "
        "*infallible*. Chapter 15 adds a second-reviewer rule "
        "for security-sensitive pages; lower-stakes pages stay "
        "on the single-reviewer path, with the audit trail as "
        "the compensating control."
    ): (
        "**`approved` 的意思是“有人读过这一 diff”，不是“这东西是对的”。** "
        "“AI 永远设回 pending”这条规则保证了"
        "每一张 `approved` 的页都有一个具名人签了字，"
        "而闸规则保证了这个人是对着**当前 commit** 签的。"
        "但这两条机制都拦不住**一个评审人去批准一份微妙错误的 L2 改写** —— "
        "可能因为他赶时间，"
        "也可能因为错误出在他不熟悉的那个领域角落里。"
        "这个模型让评审 *可追溯* ，"
        "而**不是**让评审 *不会出错* 。"
        "第 15 章对涉及安全性的页面加了一条“必须双评审”的规则；"
        "低风险的页仍然走单评审路径，"
        "让审计轨迹作为补偿性控制。"
    ),
    (
        "**The model does not prioritise reader attention.** A "
        "KB with 10 000 pages whose footers are all `approved` "
        "still forces the reader to decide which page to read "
        "first. Ranking, curation, deprecation, and the Diátaxis "
        "structure (Chapter 3) are what make a KB *usable*; the "
        "operational model makes it *trustworthy*. These are "
        "independent properties, and either alone is "
        "insufficient. A book's index is not a table of "
        "contents."
    ): (
        "**这个模型不负责为读者的注意力排优先级。** "
        "一个有一万张页、每一张 footer 都是 `approved` 的知识库，"
        "仍然要逼读者自己决定先读哪一页。"
        "排序、精选、淘汰、以及 Diátaxis 结构（第 3 章）"
        "是让一个知识库 *好用* 的东西；"
        "运维模型让它 *可信* 。"
        "这两种属性是独立的，"
        "任何一个单独存在都不够。"
        "**一本书的索引，不是它的目录。**"
    ),
    (
        "**Cross-page conflicts are out of scope.** If "
        "`architecture.md` and `runbook.md` describe the same "
        "system and disagree with each other, both can sit in "
        "the KB with `review_status: approved` and "
        "`verification_status: supported`. Detecting the "
        "disagreement requires comparing pages to each other, "
        "which the four-corner model does not do. Chapter 18's "
        "document-layering tuple and Chapter 21's "
        "agent-accessible KB together begin to address this — an "
        "agent reading both pages can *notice* the conflict — "
        "but the prose-layer operational model alone cannot. A "
        "KB with contradictory pages is a KB whose operational "
        "model is working; it is the *editorial* model that has "
        "to catch the contradiction."
    ): (
        "**跨页之间的冲突不在这个模型的处理范围里。** "
        "如果 `architecture.md` 和 `runbook.md` 描述的是同一个系统、"
        "但彼此互相矛盾，"
        "它们两张都可以在知识库里并存、"
        "都带着 `review_status: approved` 和 `verification_status: supported` 。"
        "要检测出这种矛盾，"
        "需要把**页与页**放到一起比较，"
        "而四角模型**不做这件事**。"
        "第 18 章的文档分层元组"
        "和第 21 章的 agent 可访问知识库"
        "合在一起才开始解决这个问题 —— "
        "一个能同时读到两张页的 agent "
        "**可以 *注意到* 这种冲突** —— "
        "但仅靠文稿层的运维模型是办不到的。"
        "一个内部自相矛盾的知识库，"
        "说明它的 *运维* 模型仍然在正常工作；"
        "是它的 *编辑* 模型必须去抓到这个矛盾。"
    ),
    (
        "The healthy way to hold the four corners is: they are "
        "the discipline a KB needs to stop lying *about itself*. "
        "Whether it also says true things about the software it "
        "describes is a separate, larger question — and, because "
        "that question cannot be answered mechanically, the "
        "scaffolding that makes human attention accountable is "
        "the thing that, over time, answers it for you."
    ): (
        "把这四个角看得恰当的方式是：它们是一个知识库"
        "**为了不再对自己说谎**所需要的那套纪律。"
        "至于它**关于它所描述的那个软件**是不是也在说真话，"
        "那是另一个更大的问题 —— "
        "因为那个问题没法机械回答，"
        "所以“让人类的注意力变得可追责”的那套脚手架，"
        "才是一个随着时间推移、**替你一点点把那个问题答出来**的东西。"
    ),

    # ---- Conclusion ----
    (
        "Part II's four corners (page set, metadata footer, "
        "three-level updates, verification gates) are the "
        "prose-layer analogue of Part III's four corners "
        "(parsing, embeddings, graph, prompt). Each layer has a "
        "stable *structure* the book returns to; each layer has "
        "a stable *set of mechanisms* that make that structure "
        "real. The rest of Part IV is how you wire the "
        "prose-layer mechanisms together; Part V is how the two "
        "layers talk to each other."
    ): (
        "第二部分的四个角（页面集、元数据 footer 、"
        "三级更新策略、校验闸）"
        "是第三部分那四个角（解析、embedding、图谱、prompt）"
        "在文稿层的对应物。"
        "每一层都有一个**本书会反复回来的稳定 *结构*** ，"
        "以及一个**让这个结构变成现实的稳定 *机制集*** 。"
        "第四部分剩下的内容，"
        "是**怎么把文稿层的这些机制接起来**；"
        "第五部分讲的是**两层之间怎么互相对话**。"
    ),
    (
        "The four corners do not themselves claim to produce "
        "correct docs. They claim only that a KB which "
        "implements them can *answer honestly* about its own "
        "correctness — including, when required, the answer "
        "*\"we don't know; this page hasn't been reviewed.\"* "
        "That answer is the foundation on which Chapter 18 "
        "builds the document-layering tuple and Chapter 21 "
        "builds the agent-callable surface."
    ): (
        "这四个角本身并不自称能**产出正确的文档**。"
        "它们只承诺：一个实现了这四个角的知识库，"
        "可以 *诚实地回答* 关于它自己正确性的问题 —— "
        "在必要时，"
        "包括回答一句 *“我们不知道；这一页还没被评审过。”* "
        "第 18 章的文档分层元组、"
        "以及第 21 章那个可被 agent 调用的知识库接口，"
        "都是建在这句诚实的回答之上的。"
    ),

    # ---- Hook opening ----
    (
        "An LLM just rewrote 412 pages of your KB. They all "
        "build, all have well-formed frontmatter, all render "
        "without a single broken link. On Friday afternoon your "
        "manager sends a message — three lines — asking a "
        "single question: *can we trust them now?*"
    ): (
        "一个 LLM**刚刚重写了**你知识库里 **412 个页面**。"
        "它们**全部能 build**、"
        "**全部有规格良好的 frontmatter**、"
        "**全部渲染时一条坏链接都没有**。"
        "周五下午，你的 manager 发了一条消息 —— "
        "**三行字，一个问题**："
        " *这些页面现在，我们能信了吗？*"
    ),
    (
        "You read the first three pages. They look fine. You "
        "open a fourth. It describes a workflow that was "
        "retired six weeks ago. The fifth uses a function name "
        "that was renamed in the same PR that triggered the "
        "regeneration. The sixth is perfect. You have 406 pages "
        "left and roughly 90 minutes before the 17:00 standup. "
        "Which ones does a human need to read before Monday "
        "morning, and how do you tell your manager *\"we don't "
        "know yet\"* in a way that sounds like competence and "
        "not helplessness?"
    ): (
        "你读了前三页，看上去没问题。"
        "你打开**第四页**。"
        "它描述的是**六周前就已经废弃的一套工作流**。"
        "**第五页**用的**函数名**，"
        "是**在同一个触发这次重生成的 PR 里被改掉的**。"
        "**第六页**完美。"
        "你**还有 406 页**，"
        "离 17:00 的 standup **大约 90 分钟**。"
        "**哪几页**必须让人**在周一早晨之前看过**？"
        "你又怎么**告诉你的 manager** *“我们还不知道”* —— "
        "让这句话**听起来像专业**，"
        "**不像束手无策**？"
    ),
    (
        "Chapters 4–7 got the prose in. This chapter is about "
        "the thing that happens the first Monday after the "
        "honeymoon ends: a KB whose contents are **cheap to "
        "generate** and **expensive to trust**. The four-corner "
        "model below is what lets you answer your manager's "
        "question in three lines — and, more importantly, lets "
        "you answer it honestly."
    ): (
        "**第 4–7 章**把文稿**装了进来**。"
        "这一章讲的是**蜜月期结束之后那第一个周一发生的事**："
        "**一个内容廉价、信任昂贵的知识库**。"
        "下面这个**四角模型**，"
        "就是让你**用三行字回答你 manager 的那个问题** —— "
        "并且**更重要的是**：**让你诚实地回答它**。"
    ),

    # ---- Theory anchor "Why exactly four corners?" ----
    "Why exactly four corners?": "**为什么恰好是四个角？**",
    (
        "A reader who has come this far has a fair question: "
        "*why four, and why these four?* \"Because experience "
        "taught me so\" is the honest answer but not a "
        "satisfying one. The structural answer is that the "
        "four corners are the four phases of the "
        "Plan–Do–Check–Act cycle {cite}`deming1986outofcrisis` "
        "specialised to a prose-layer artefact. Each corner "
        "answers one phase; drop any one and the cycle breaks."
    ): (
        "**读到这里的读者，有一个合理的问题**："
        " *为什么是四？又为什么是这四个？* "
        "“**因为经验告诉我是这样**”是**诚实的答案**，"
        "但**不是一个令人满足的答案**。"
        "**结构性的答案**是："
        "这**四个角**，**恰好是**"
        "**戴明 Plan–Do–Check–Act 循环** "
        "{cite}`deming1986outofcrisis` "
        "**特化到一份文稿层制品上**的**四个相位**。"
        "**每个角**回答**一个相位**；"
        "**任意拆掉一个**，**整个循环就断掉**。"
    ),
    "PDCA phase": "PDCA 相位",
    "Question it answers": "它回答的问题",
    "The corner that answers it": "回答它的那个角",
    "If the corner is missing": "如果缺了这个角",
    "**Plan** — what should exist?": "**Plan** —— 应该存在哪些东西？",
    (
        "Free-form folders; a `misc/` directory that "
        "metastasises."
    ): "**自由形式的文件夹**；一个**会扩散转移**的 `misc/` 目录。",
    "**Do** — how does it get updated?": "**Do** —— 它怎么被更新？",
    "*Who — or what — performs the update, at what cost?*":
        " *谁 —— 或者什么 —— 在做这次更新，代价是多少？* ",
    (
        "Every change goes through an LLM or none do; cost is "
        "unbounded or the KB goes stale."
    ): (
        "**要么**每一次变更都过一遍 LLM，**要么一次都不过**；"
        "**要么代价无界**，**要么知识库变腐**。"
    ),
    "**Check** — is the update acceptable?":
        "**Check** —— 这次更新可以被接受吗？",
    (
        "Rules that are \"policy\" but not enforced, i.e. "
        "eventually ignored."
    ): "规则停留在“**政策**”层面、**不被强制** —— 也就是**最终被忽略**。",
    "**Act** — what did we learn about this page?":
        "**Act** —— 关于这一页，我们学到了什么？",
    (
        "*Is this specific page still trusted, right now, by "
        "whom, and how much?*"
    ): (
        " *这一页，此时此刻，还被相信吗？"
        "被谁相信？"
        "相信到什么程度？* "
    ),
    (
        "Staleness is invisible; review state lives in an "
        "engineer's memory."
    ): "**腐化是不可见的**；**评审状态活在某个工程师的脑子里**。",
    "Three observations follow from this mapping.":
        "**从这张映射**出发，可以**得出三点观察**。",
    (
        "**The model is structurally complete, not "
        "contingently so.** Any operational discipline built "
        "around \"the docs must stay correct as the code "
        "changes\" needs exactly one answer to each phase. "
        "Two-corner systems (just *Plan + Do*: \"we have a "
        "template, we write updates\") are the default "
        "industry shape and the default failure shape — "
        "without *Check* the template silently rots, and "
        "without *Act* the KB cannot tell itself from its own "
        "exhaust. Three-corner systems (*Plan + Do + Check*: "
        "template + process + CI) are where most mature teams "
        "land; they remain brittle because *Act*, the per-page "
        "memory, is not mechanised. Adding C2 — a footer a "
        "human can read and a script can filter — is the last "
        "corner, and it is the cheapest."
    ): (
        "**这个模型是结构性地完整的，不是偶然地完整。** "
        "**任何**一套围绕"
        "“**代码在变，文档得保持正确**”"
        "构建的运维纪律，"
        "都**必须**对每一个相位"
        "**恰好给出一个答案**。"
        "**两角系统**（**只有** *Plan + Do* ："
        "“**我们有模板，我们写更新**”）"
        "是**业界默认的形状**，"
        "也是**默认的失败形状** —— "
        "**缺了** *Check* ，**模板会悄无声息地腐烂**；"
        "**缺了** *Act* ，"
        "**知识库分不清自己和自己产生的排泄物**。"
        "**三角系统**（ *Plan + Do + Check* ："
        "**模板 + 流程 + CI**）"
        "是**多数成熟团队能走到的位置**；"
        "但**它们依然脆弱** —— "
        "**因为** *Act* ，**那份按页记忆的功能**，**没有被机械化**。"
        "**加上 C2** —— "
        "**一段人能读、脚本能过滤的 footer** —— "
        "**就是最后那一个角**，**也是最便宜的那一个**。"
    ),
    (
        "**The corners are independent and load-bearing.** "
        "They are independent because each answers a different "
        "PDCA phase, and no corner's mechanics substitute for "
        "another's: a rich footer (C2) does not tell you what "
        "should exist (C1); a strict gate (C4) does not tell "
        "you who pays to update (C3). And they are "
        "load-bearing because, like the four legs of a stool, "
        "removing any one collapses the structure. A KB with "
        "opinionated pages, footers, and gates but no update "
        "strategy (no C3) works until the first code change "
        "and then fills with `pending` pages no one has the "
        "budget to fix. A KB with all three mechanics but no "
        "opinionated shape (no C1) cannot tell a reader "
        "*where* to look, so neither C2, C3, nor C4 gets "
        "exercised often enough to stay honest."
    ): (
        "**四个角是相互独立的，也是全都承重的。** "
        "它们**相互独立** —— "
        "**因为每一个都回答 PDCA 的一个不同相位**，"
        "而**任何一个角的机制**"
        "**都没法替代另一个角**："
        "**一份信息丰富的 footer** （C2）**不会告诉你**"
        "**应该存在什么东西**（C1）；"
        "**一道严格的校验闸**（C4）**不会告诉你**"
        "**谁来付这次更新的代价**（C3）。"
        "它们**都承重** —— "
        "**像一张凳子的四条腿** —— "
        "**抽掉任意一条**，**整个结构就塌**。"
        "**有固定页面集、有 footer、有闸**，"
        "**但没有更新策略**的知识库（**缺 C3**），"
        "**在第一次代码变更之前都能工作**，"
        "**然后立刻被无人预算去修的 `pending` 页面淹没**。"
        "**三套机制都有、但没有固定形状**的知识库（**缺 C1**），"
        "**没法告诉读者 *该到哪里看*** ，"
        "于是**C2、C3、C4 都没有被足够频繁地行使**，"
        "**也就无法保持诚实**。"
    ),
    (
        "**The correspondence also explains the *order* the "
        "rest of Part IV unpacks them.** Chapter 14 walks "
        "change detection, which is a *Do* operation (C3) "
        "triggered by an *Act* observation (C2 footer SHA "
        "diff). Chapter 15 makes gates real (C4). Chapter 16 "
        "wires the three update levels (C3 proper). The book "
        "builds the cycle Do → Check → Act → back-to-Plan "
        "because that is the sequence the cycle actually runs "
        "at operational time; the *Plan* corner (C1) is the "
        "boundary condition rather than a recurring step."
    ): (
        "**这组对应也解释了第四部分接下来讲述它们的 *次序* 。** "
        "**第 14 章**走**变更检测**，"
        "这本身是**一次由** *Act* 观测（C2 footer 的 SHA diff）"
        "**所触发的** *Do* 操作（C3）。"
        "**第 15 章**把**闸变成真**（C4）。"
        "**第 16 章**把**三级更新**连起来（**真正意义上的 C3**）。"
        "这本书搭建的循环是 "
        "**Do → Check → Act → 再回到 Plan** —— "
        "**因为这才是**"
        "**这个循环在运维时间上真正运行的次序**；"
        " *Plan* 角（C1）"
        "**是边界条件，不是周期性的一步**。"
    ),
    (
        "The mapping is not a formal proof of minimality — "
        "PDCA itself is a heuristic, not a theorem. But it "
        "gives the four corners a shape the reader can reason "
        "about and, more importantly, a shape the reader can "
        "*reject*: if a team finds a fifth corner their KB "
        "actually needs, the productive response is not to "
        "squeeze it into one of C1–C4 but to extend the cycle. "
        "The model is a floor, not a ceiling."
    ): (
        "**这张映射并不是一次关于最小性的形式证明** —— "
        "**PDCA 本身**也**只是一套启发式、不是一个定理**。"
        "但它**给了四个角一个读者可以推理的形状**，"
        "并且**更重要的是**："
        "**一个读者可以 *拒绝* 的形状**："
        "**如果一个团队**"
        "**发现自己的知识库真的需要第五个角**，"
        "**有效的做法不是把它硬塞进 C1–C4 里的某一个**，"
        "**而是扩展这个循环**。"
        "**这个模型是地板，不是天花板。**"
    ),

    # ---- Part II checklist section header ----
    "Part II in one page — a pointer checklist":
        "一页总览第二部分 —— 一张跳转清单",
    (
        "Across the five chapters, Part II has catalogued "
        "roughly two dozen failure modes, misconceptions, and "
        "wiring mistakes. For the reader who returns to the "
        "book *after* deploying a KB and is now trying to "
        "diagnose a specific symptom, the table below is a "
        "single-page index into the discussion — organised by "
        "the symptom a team actually observes, not by the "
        "chapter it lives in."
    ): (
        "**横跨这五章**，"
        "**第二部分**一共编目了**大约二十几种**"
        "**失败模式、误解、和接线错误**。"
        "**对于那些 *已经部署过一个知识库之后* 回头翻这本书**、"
        "**正在试图诊断一个具体症状的读者**，"
        "下面这张表是**一份单页索引** —— "
        "**按团队实际看到的症状组织**，"
        "**而不是按它住在哪一章组织**。"
    ),

    # ---- Checklist sub-tables headings ----
    "Storage and repository hygiene (Chapter 4)":
        "**存储与仓库卫生**（第 4 章）",
    "Provenance and trust (Chapter 5)":
        "**来源与信任**（第 5 章）",
    "Classification pipeline (Chapter 6)":
        "**分类流水线**（第 6 章）",
    "Search and publishing (Chapter 7)":
        "**搜索与发布**（第 7 章）",
    "Operational model (Chapter 7a)":
        "**运维模型**（第 7a 章）",
    "Symptom you see": "**你看到的症状**",
    "Root cause": "**根本原因**",
    "One-line remedy": "**一句话的补救**",
    "Pointer": "**去哪里看**",

    # ---- ch04 rows ----
    "Clones getting slower each month":
        "**克隆一个月比一个月慢**",
    "Binary blobs committed into `content/`":
        "`content/` 里被提交了二进制大块",
    "CI hard-limit on file size + Git LFS for the few legitimate binaries":
        "CI 对文件大小设硬上限；**少数合理的二进制**走 Git LFS",
    "ch04 §\"Common mistakes\" #1":
        "第 4 章 §“Common mistakes” #1",
    "External links from code to wiki pages break after a rename":
        "**代码里指向 wiki 页面的外链**在一次改名之后全挂",
    "Slug rename with no redirect map":
        "**改了 slug 却没有重定向表**",
    "Check in a `redirects.yaml`; CI refuses PRs that break a still-referenced URL":
        "把 `redirects.yaml` check in；**CI 拒绝任何会打破仍被引用 URL 的 PR**",
    "ch04 §\"Common mistakes\" #2":
        "第 4 章 §“Common mistakes” #2",
    "Merge conflicts that the PR UI cannot display usefully":
        "**PR UI 根本没法有效展示的合并冲突**",
    "Two authors rewrote the same file in parallel":
        "两个作者**并行重写**了同一个文件",
    "Treat high-churn pages as *owned*; for live-incident docs, use a shared doc, import afterwards":
        "把**高频变动**的页面当作 *有 owner* 的；"
        "**现场事故文档**用共享文档，**事后再导入**",
    "ch04 §\"Common mistakes\" #3":
        "第 4 章 §“Common mistakes” #3",
    "Per-reader history / autosaves / comments bloating the repo":
        "**按读者的历史/自动保存/评论**把仓库撑大",
    "Over-extending \"everything is a file\" to mutable operational state":
        "**把“万物皆文件”过度延伸到可变的运维状态上**",
    "Mutable state lives in a side database; files are for content":
        "**可变状态住在旁边的数据库里**；**文件只放内容**",
    "ch04 §\"Common mistakes\" #4":
        "第 4 章 §“Common mistakes” #4",
    "Docs still drifting from code despite PR discipline":
        "**尽管有 PR 纪律，文档依然和代码漂移**",
    "Review runs on different communication lines than code review":
        "**文档评审走在一条和代码评审不同的沟通线上**",
    "Docs-as-code realigns the two via Conway's law / Parnas co-location":
        "docs-as-code **通过康威定律 / Parnas 共处一地把两者重新对齐**",
    "ch04 §\"Why docs-as-code really works\"":
        "第 4 章 §“Why docs-as-code really works”",

    # ---- ch05 rows ----
    "An old audit trail silently lost its authorship":
        "**一份老的审计记录悄无声息地丢了作者**",
    "`created_by` was treated as mutable in a bulk migration":
        "在一次批量迁移里，`created_by` 被当作**可变的**",
    "`created`, `created_by`, `source` are frozen; only correct via explicit PR":
        "`created`、`created_by`、`source` **冻结**；"
        "**只能通过显式的 PR 更正**",
    "ch05 §\"Common mistakes\" #1":
        "第 5 章 §“Common mistakes” #1",
    "`git log` of `content/` is dominated by review-state flips":
        "`content/` 的 `git log` 被**评审状态切换**淹没",
    "Review state lives in frontmatter instead of its own block":
        "**评审状态**住在 frontmatter 里，**而不是自己的独立块里**",
    "Split into frontmatter (lineage) + footer (review state)":
        "**拆成**：frontmatter（**谱系**）+ footer（**评审状态**）",
    "ch05 §\"Common mistakes\" #2":
        "第 5 章 §“Common mistakes” #2",
    "Production KB now has `approved` pages a human never saw":
        "**生产的知识库里现在有 `approved` 页面**，**没有人类看过**",
    "No hard gate on `approved` + `reviewed_by`":
        "**`approved` + `reviewed_by` 上没有硬闸**",
    "CI gate rejects `approved` without a matching human `reviewed_by`":
        "**CI 闸拒绝**：`approved` **而没有对应的人类 `reviewed_by`**",
    "ch05 §\"Common mistakes\" #3":
        "第 5 章 §“Common mistakes” #3",
    "`doc_type` vocabulary has drifted to a long messy list":
        "`doc_type` 的**词汇表**已经漂成**一个乱糟糟的长列表**",
    "No enum closure in the validator":
        "**校验器里没有把枚举闭合**",
    "`doc_type` is a *closed* enumeration; reject unknown values at validation time":
        "`doc_type` 是一个 *封闭* 的枚举；**在校验时拒绝未知值**",
    "ch05 §\"Common mistakes\" #4":
        "第 5 章 §“Common mistakes” #4",
    "Pages marked `supported` for a commit that was rewritten twice":
        "**被标记 `supported` 的页面**，"
        "**对应的 commit 已经被 rebase 改写过两次**",
    "`verification_status` was not re-evaluated against `commit`":
        "`verification_status` **没有相对** `commit` **被重新评估**",
    "Staleness detector demotes when footer `commit` no longer matches the code it references":
        "**腐化探测器**在 footer 的 `commit`"
        "**不再匹配它所引用的代码时**，**把信任降级**",
    "ch05 §\"Common mistakes\" #5":
        "第 5 章 §“Common mistakes” #5",
    "`source.uri` points at a 404 or a silently reworded URL":
        "`source.uri` 指向**一个 404**，**或者一个悄悄被改了措辞的 URL**",
    "`source` has no `ref`": "`source` **没有 `ref`**",
    "Every `source.uri` must carry a `ref`: commit SHA, Wayback snapshot, content hash":
        "**每一个** `source.uri` **都必须带一个** `ref` ："
        "commit SHA、Wayback 快照、或内容 hash",
    "ch05 §\"Common mistakes\" #6":
        "第 5 章 §“Common mistakes” #6",

    # ---- ch06 rows ----
    "Imported page filed as `security-architecture` with `supported` trust":
        "**导入进来的页面**被归到 `security-architecture` ，**且信任是** `supported`",
    "Prompt injection via imported content":
        "**通过导入内容注入 prompt**",
    "Bound the classifier input; mark untrusted content explicitly; `verification_status` is out of the LLM's output schema":
        "**给分类器的输入上界限**；**显式标注不可信内容**；"
        " `verification_status` **不在 LLM 的输出 schema 里**",
    "ch06 §\"LLM failure modes\" #1":
        "第 6 章 §“LLM 的失败模式” #1",
    "New, made-up category appeared in `content/`":
        "**`content/` 里出现了一个新编出来的类别**",
    "Hallucinated label (closed enum not enforced)":
        "**幻觉出来的标签**（**封闭枚举没有被强制**）",
    "Caller rejects out-of-enum labels; fall back to heuristic classifier":
        "**调用方拒绝枚举之外的标签**；**回退到启发式分类器**",
    "ch06 §\"LLM failure modes\" #2":
        "第 6 章 §“LLM 的失败模式” #2",
    "Gradual shift in category distribution over months":
        "**几个月下来，类别分布在缓慢漂移**",
    "Silent model upgrade or corpus drift":
        "**模型的静默升级**，**或者语料的漂移**",
    "Check a ~50-page gold set into the repo; nightly CI diffs the labels":
        "**往仓库里 check 一个 ~50 页的 gold set**；"
        "**夜间 CI diff 标签**",
    "ch06 §\"LLM failure modes\" #3":
        "第 6 章 §“LLM 的失败模式” #3",
    "Half the weekend's ingest silently went through the heuristic":
        "**周末一半的 ingest 悄无声息地走了启发式**",
    "JSON-mode parse failures were logged but not metricised":
        "**JSON 模式解析失败被记了日志，但没有被做成度量**",
    "Use structured-output API; treat parse failures as a first-class metric":
        "**用结构化输出 API**；**把解析失败当成一等公民的度量**",
    "ch06 §\"LLM failure modes\" #4":
        "第 6 章 §“LLM 的失败模式” #4",
    "Ingest batch cost exploded overnight":
        "**ingest 批次的成本一夜之间爆炸**",
    "Provider pricing / throttling change":
        "**供应商定价 / 限流变了**",
    "Hard budget per batch: max tokens, max wall-clock, abort and commit partial":
        "**每批次硬预算**：最大 token、最大墙钟时间、"
        "**中止并 commit 部分结果**",
    "ch06 §\"LLM failure modes\" #5":
        "第 6 章 §“LLM 的失败模式” #5",
    "Imported page's images 404 a year later":
        "**一年之后，导入页面里的图片 404**",
    "Importer did not rewrite asset URLs":
        "**导入器没有重写资源 URL**",
    "The *ingest path* (one function) owns URL rewriting; every importer flows through it":
        "**由 *ingest 路径* （同一个函数）负责 URL 重写**；"
        "**每个导入器都流经它**",
    "ch06 §\"LLM failure modes\" #6":
        "第 6 章 §“LLM 的失败模式” #6",
    "Team treats Diátaxis labels as ground truth":
        "**团队把 Diátaxis 标签当作 ground truth**",
    "Classification *is* a lossy projection":
        "分类 *就是* 一次有损投影",
    "Record classifier uncertainty; route low-confidence to human review; treat `unreviewed` as the honest default":
        "**把分类器的不确定性记录下来**；"
        "**低置信度路由到人审**；"
        "**把 `unreviewed` 当作诚实的默认值**",
    "ch06 §\"A note on what classification *is*\"":
        "第 6 章 §“关于分类 *究竟是什么* 的说明”",

    # ---- ch07 rows ----
    "User searches for `throttle incoming traffic`, gets nothing":
        "**用户搜** `throttle incoming traffic` ，**零结果**",
    "Vocabulary mismatch with identifier-literal":
        "**和 identifier-literal 之间的词汇失配**",
    "Richer frontmatter `tags:` now; dense retrieval when it stops working":
        "**先把 frontmatter 的** `tags:` **变丰富**；"
        "**等这招也不行时再上 dense retrieval**",
    "ch07 §\"Where the tiny search engine fails\" #1":
        "第 7 章 §“这个小引擎会在哪里失败” #1",
    "`配置文件` query returns nothing on CJK corpus":
        "在中文语料上搜 `配置文件` **返回零结果**",
    "No segmentation; `unicode.IsLetter` does not split":
        "**没有分词**；`unicode.IsLetter` **不会切分**",
    "Swap `tokenize` for a CJK segmenter (`go-jieba`, `kagome`)":
        "把 `tokenize` **换成**一个中文分词器（`go-jieba` 、`kagome`）",
    "ch07 §\"Where the tiny search engine fails\" #2":
        "第 7 章 §“这个小引擎会在哪里失败” #2",
    "`recieve` returns nothing, users annoyed":
        "**`recieve` 返回零结果，用户抓狂**",
    "No typo tolerance": "**没有拼写容错**",
    "Fuzzy matching in-process up to ~100k terms; Meilisearch above that":
        "**词数在 ~10 万以内**：**进程内做 fuzzy matching**；**超过之后换 Meilisearch**",
    "ch07 §\"Where the tiny search engine fails\" #3":
        "第 7 章 §“这个小引擎会在哪里失败” #3",
    "Long-but-irrelevant pages outrank focused ones":
        "**冗长但不相关的页面**排在**聚焦的页面**前面",
    "Score is term-cardinality, no length normalisation":
        "**打分用的是词命中数，没有长度归一化**",
    "Field weighting on `title`; escalate to BM25 when the pattern persists":
        "**在 `title` 上做字段加权**；"
        "**这个模式持续出现时**，**升级到 BM25**",
    "ch07 §\"Where the tiny search engine fails\" #4":
        "第 7 章 §“这个小引擎会在哪里失败” #4",
    "Incremental index is stale yet debugging is hard":
        "**增量索引陈旧，但 debug 又很难**",
    "Incremental update is the failure mode of most DB-backed wikis":
        "**增量更新**就是**大多数数据库型 wiki 的失败模式**",
    "Whole-map rebuild on write; milliseconds at this scale":
        "**写的时候整张表重建**；在这个规模上只是毫秒级",
    "ch07 §\"Common mistakes in wiring up search\" #1":
        "第 7 章 §“接线搜索时的常见错误” #1",
    "Live server and static site return different results":
        "**在线服务和静态站点返回不同的结果**",
    "Two search layers running in parallel":
        "**两层搜索在并行运行**",
    "Staircase is a *sequence* — pick one layer, keep one interface":
        "**阶梯是一条 *序列* —— 只选一层，只保留一个接口**",
    "ch07 §\"Common mistakes in wiring up search\" #2":
        "第 7 章 §“接线搜索时的常见错误” #2",
    "`contradicted` pages surface in default search":
        "**`contradicted` 的页面在默认搜索里冒出来**",
    "Trust fields are not retrieval metadata yet":
        "**信任字段还没被当成检索用的元数据**",
    "Filter by `verification_status` at query time; explicit \"include superseded\" toggle":
        "**查询时按 `verification_status` 过滤**；"
        "**给一个显式的“包括已过时页面”开关**",
    "ch07 §\"Common mistakes in wiring up search\" #3":
        "第 7 章 §“接线搜索时的常见错误” #3",
    "Org relies on Sphinx client-side search for authenticated users":
        "**组织把 Sphinx 的客户端搜索给已登录用户用**",
    "Static search is blind to frontmatter / trust fields":
        "**静态搜索看不见 frontmatter / 信任字段**",
    "Server search is authoritative; static search is for public / offline":
        "**服务端搜索是权威的**；**静态搜索给的是公开 / 离线场景**",
    "ch07 §\"Common mistakes in wiring up search\" #4":
        "第 7 章 §“接线搜索时的常见错误” #4",

    # ---- ch07a rows ----
    "Every page `approved`, content still wrong":
        "**每一页都 `approved`，内容依然是错的**",
    "Gates check form, not truth": "**闸检查的是形式，不是真相**",
    "`approved` means *a human read the diff*, not *this is correct*; add second-reviewer rule for security-sensitive pages":
        "`approved` **表示** *一个人读过这次 diff* ，"
        "**不是** *这是对的* ；"
        "**对安全敏感页面加第二评审人规则**",
    "10k `approved` pages, user still can't find the right one":
        "**一万个 `approved` 页面，用户还是找不到对的那一个**",
    "Model makes KB trustworthy, not *usable*":
        "**模型让知识库变得可信，不是变得** *可用* ",
    "Prioritisation is Diátaxis + curation, independent of trust":
        "**优先排序是 Diátaxis + 策展**，**和信任是正交的**",
    "`architecture.md` and `runbook.md` disagree, both approved":
        "**`architecture.md` 和 `runbook.md` 互相矛盾，都是 `approved`**",
    "Four-corner model is per-page, not cross-page":
        "**四角模型是按页的，不是跨页的**",
    "Cross-page conflict detection is out of scope for Part II; ch18 + ch21 begin to address it":
        "**跨页冲突检测**在**第二部分的范围之外**；"
        "**第 18 章 + 第 21 章开始处理它**",
    (
        "The common thread across the whole table: *every one "
        "of these failures has a cheap mechanical fix **and** "
        "an expensive \"re-architecture\" fix, and teams "
        "consistently try the expensive one first.* The "
        "operational model is the habit of spending one hour on "
        "the cheap fix before spending a week on the expensive "
        "one."
    ): (
        "**贯穿这整张表的一条共同线索**："
        " *这些失败里的每一个，"
        "都有一个廉价的机械修法 **以及** 一个昂贵的“重新架构”的修法；"
        "而团队一贯先去尝试那个昂贵的。* "
        "**所谓运维模型**，**就是**"
        "**在花一周时间做那个昂贵修法之前**、"
        "**先花一个小时试那个廉价修法的习惯**。"
    ),

    # ---- Override fuzzy entries with fresh translations (for the new
    # PDCA-mapping table rows; the original translations were for the
    # four-corner-list prose that lived above C1–C4).
    "*Which pages should a KB have?*":
        " *一个知识库应该有哪些页面？* ",
    "**C1** Opinionated page set": "**C1** 固定的页面集",
    "**C3** Three-level update strategy": "**C3** 三级更新策略",
    "*What must be true before we publish the update?*":
        " *发布这次更新之前，哪些条件必须成立？* ",
    "**C4** Verification gates": "**C4** 校验闸",
    "**C2** Metadata footer": "**C2** 元数据 footer",
    "ch07a §\"What this model does *not* solve\" #1, #2":
        "第 7a 章 §“这个模型 *并没有* 解决的问题” #1、#2",
    "ch07a §\"What this model does *not* solve\" #3":
        "第 7a 章 §“这个模型 *并没有* 解决的问题” #3",
    "ch07a §\"What this model does *not* solve\" #4":
        "第 7a 章 §“这个模型 *并没有* 解决的问题” #4",
}
