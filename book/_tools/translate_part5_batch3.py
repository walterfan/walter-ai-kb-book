"""Apply Chinese translations for Part V batch 3: ch21.

Run with: poetry run python book/_tools/translate_part5_batch3.py
"""

from __future__ import annotations

import os
import sys
import polib

LOCALE_ROOT = "book/locale/zh_CN/LC_MESSAGES/part5-hybrid-layer"


CH21: dict[str, str] = {
    "Chapter 21 — AI Agents on the KB":
        "第 21 章 —— 在知识库上跑的 AI Agent",

    "Why": "Why —— 为什么",
    "What": "What —— 是什么",
    "How": "How —— 怎么做",
    "Example": "Example —— 范例",
    "Conclusion": "Conclusion —— 小结",
    "References": "参考文献",

    "A knowledge base has two kinds of readers. A human reader opens a browser, types a query, scans a page, and closes the tab. An agent reader — an LLM-backed assistant in an IDE, a chat client, a CI job — does not open a browser. It calls a function, receives a structured response, and keeps going. For most of this book the reader has been human. This chapter is about the other kind.":
        "一个知识库有两种读者。人类读者打开浏览器、输入查询、扫一眼页面、关掉标签页。Agent 读者 —— IDE 里的 LLM 助手、聊天客户端、CI 任务 —— 不会打开浏览器。它调用一个函数、收下一份结构化响应、然后继续跑下去。本书的大部分篇幅都以人类读者为对象，本章讨论的是另一种。",

    "The move is not new. The blog post that seeded this book {cite}`fanyamin2026deepwiki` already argues that the KB's value compounds when an LLM can call it instead of a human having to read it. What has changed since that post is the arrival of a *protocol* for such calls — the Model Context Protocol {cite}`mcp_spec` — and the arrival of a common *deployment pattern*, the edge function, that turns a KB into something an agent can reach from anywhere. Agents on a KB have two halves, and this chapter treats them in turn: the protocol half (how agents talk to a KB) and the pattern half (how a KB gets close enough to an agent to be worth talking to).":
        "这不是新思路。本书的种子博文 {cite}`fanyamin2026deepwiki` 早已主张：当 LLM 可以直接调用知识库、而不再依赖人去阅读它时，这个知识库的价值就会复利增长。那篇博文之后的新变化有两件：一是出现了这种调用的 * 协议 * —— Model Context Protocol {cite}`mcp_spec` ；二是出现了一种常见的 * 部署模式 * —— edge function，它让知识库变成一个 agent 可以从任何地方够得到的东西。“跑在知识库上的 agent”可以拆成两半，本章依次处理：协议半（agent 如何与知识库对话）和模式半（知识库如何离 agent 近到足以值得被对话）。",

    "The protocol half: MCP plus the tuple":
        "协议半：MCP + 元组",

    "The Model Context Protocol is, for the purposes of this chapter, a simple idea made precise: an agent can enumerate *tools* exposed by a server, and it can call those tools with typed arguments. A KB can be a MCP server; a well-scoped KB exposes three tools:":
        "就本章而言，Model Context Protocol 是一个被精确化了的简单思路：一个 agent 可以枚举服务器对外暴露的 * 工具 * ，并用带类型的参数调用这些工具。知识库可以成为一个 MCP 服务器；一个定义得体的知识库会暴露三个工具：",

    "Tool": "工具",
    "Input": "输入",
    "Output": "输出",

    "`kb.search(query, k, filter)`": "`kb.search(query, k, filter)`",
    "natural-language query, top-k, filter expression":
        "自然语言查询、top-k、过滤表达式",
    "list of $\\{page\\_id, score, \\text{tuple}, snippet\\}$":
        "一个列表，元素为 $\\{page\\_id, score, \\text{tuple}, snippet\\}$",

    "`kb.read(page_id)`": "`kb.read(page_id)`",
    "stable page id": "稳定的页面 id",
    "full body, frontmatter, footer": "完整正文、frontmatter、footer",

    "`kb.cite(query, k)`": "`kb.cite(query, k)`",
    "natural-language query, top-k": "自然语言查询、top-k",
    "list of $\\{page\\_id, \\text{file:line} \\text{ anchors}\\}$":
        "一个列表，元素为 $\\{page\\_id, \\text{file:line} \\text{ 锚点}\\}$",

    "The important detail is the **filter argument on `kb.search`**, which accepts a predicate over the document-layer tuple from Chapter 18. An agent that wants only approved content writes `filter: review_status == approved`. An agent that wants only L0–L1 (code and ADRs, no AI-drafted prose) writes `filter: layer in {L0, L1}`. An agent that wants \"reviewed prose or code\" writes the conjunction. The KB does not have to trust the agent; it simply filters deterministically at retrieval time.":
        "值得关注的细节是 **`kb.search` 的 filter 参数** ：它接受一个基于第 18 章文档层元组的谓词。只要经过批准内容的 agent 可以写 `filter: review_status == approved`；只要 L0–L1（代码和 ADR，不要 AI 起草的文稿）的 agent 可以写 `filter: layer in {L0, L1}`；要“已评审的文稿或代码”的 agent 写两者的合取即可。知识库 * 不必 * 信任 agent；它只要在检索阶段确定性地过滤就行。",

    "This is the payoff of the tuple model. Without it, a KB exposed to agents would either include AI-drafted-unreviewed content in every answer (dangerous) or exclude it blanket (wasteful). With it, the decision is pushed to the caller, and the KB's responsibility reduces to *honest labelling* — which, as Chapter 7a argued, is the thing the operational model was built to deliver.":
        "这就是元组模型的回报。没有它，一个对 agent 开放的知识库要么把 AI 起草、未评审的内容也塞进每个回答里（危险），要么一刀切地全部排除（浪费）。有了它，决定权被推到调用方那一侧，知识库自身的责任收敛为 * 诚实地打标签 * —— 正如第 7a 章所论证的，运维模型被建立起来，就是为了交付这件事。",

    "The pattern half: edge-deployed KBs":
        "模式半：在 edge 上部署的知识库",

    "A search tool that sits behind a VPN in a datacentre is not an agent's tool; it is a human's tool with an agent-shaped wrapper. To be useful to agents, a KB has to be reachable from wherever the agent runs — typically an IDE process on a laptop, a CI runner in the cloud, a containerised worker in another region. The common shape is the **edge function**: a small, stateless, horizontally-scalable unit that serves HTTP from many geographic points of presence.":
        "一个躲在数据中心 VPN 后面的搜索工具，不是 agent 的工具；它只是一个套着 agent 形壳子的人类工具。要对 agent 有用，知识库必须能在 agent 运行的任何地方被够得到 —— 通常是笔记本上的 IDE 进程、云上的 CI runner、另一个区域的容器化 worker。常见形态是 **edge function** ：一个小巧、无状态、可水平扩展的单元，从多个地理接入点提供 HTTP 服务。",

    "Public examples of this pattern, any of which can host the three MCP tools above:":
        "这一模式的公共示例，上述三个 MCP 工具在其中任一平台上都可以托管：",

    "**Cloudflare Workers** {cite}`cloudflare_workers` — V8 isolates, global distribution, KV and D1 for state, single-digit-ms cold start.":
        "**Cloudflare Workers** {cite}`cloudflare_workers` —— V8 isolate、全球分发、KV 与 D1 作为状态层、冷启动在个位数毫秒级。",

    "**Deno Deploy** {cite}`deno_deploy` — TypeScript-first, global distribution, `Deno.kv` for state.":
        "**Deno Deploy** {cite}`deno_deploy` —— 以 TypeScript 为主、全球分发、`Deno.kv` 作为状态层。",

    "**Vercel Edge Functions** {cite}`vercel_edge` — per-region deployment, `@vercel/edge-config` for state.":
        "**Vercel Edge Functions** {cite}`vercel_edge` —— 按区域部署、`@vercel/edge-config` 作为状态层。",

    "All three support the same operational shape: the *built HTML* from `book/_build/html/` is stored in an asset bundle; a small server function reads the bundle, answers `kb.read(page_id)` by serving the matching HTML body, and answers `kb.search(...)` by consulting an index also stored in the bundle (for a small KB) or a remote vector store (for a large one). The KB publishes; the function redeploys; the agents see fresh answers on the next call.":
        "三者支持的运维形态是一样的：来自 `book/_build/html/` 的 * 构建好的 HTML * 放进一个 asset bundle 里；一个小服务函数读取这个 bundle，用匹配的 HTML 正文来回答 `kb.read(page_id)`，并通过查询一个同样保存在 bundle 里的索引（知识库较小时）或一个远端向量存储（知识库较大时）来回答 `kb.search(...)`。知识库发布；函数重部署；agent 下一次调用时就看到新鲜答案。",

    "This abstraction is deliberately generic. The author's private skill {cite}`fanyamin_pkb_skill` has a concrete deployment recipe for one such runtime, including the build-bundle script and the function-registration manifest. Those recipes are omitted here because they are specific to employer infrastructure; the three public analogues above are drop-in replacements.":
        "这层抽象是有意做成通用的。作者的私有 skill {cite}`fanyamin_pkb_skill` 对某一具体的运行时有一份完整的部署配方，包含构建 bundle 的脚本和函数注册 manifest。这里之所以省略那些配方，是因为它们与雇主的基础设施强绑定；上面列出的三个公开同类可以作为直接替换。",

    "A minimal MCP server shape": "一份最小的 MCP 服务器骨架",

    "Pseudocode for the server side — the same shape fits any of the three runtimes above:":
        "服务端伪代码 —— 同一套骨架可以套到上面三个运行时的任意一个上：",

    "Three things to notice:": "有三点值得注意：",

    "`kb.read` returns the **footer** alongside the body. An agent that wants to cite a page responsibly looks at `review_status` and `review_score` before quoting it. The KB does not decide whether the agent should trust the page; it gives the agent the labels to decide for itself.":
        "`kb.read` 在返回正文的同时也返回 **footer** 。一个想要负责任地引用页面的 agent，会在引用前先看一眼 `review_status` 和 `review_score`。知识库并不替 agent 决定它是否应该信任这个页面；它只是把标签给 agent，让它自己决定。",

    "`kb.cite` returns `file:line` anchors, not prose. This is the Chapter 12 hard rule made into a tool. An agent that calls `kb.cite` and then fabricates a line number is doing so over the server's objection — and the CI gate at Chapter 15 H4 will catch the page if it is ever committed back to the KB.":
        "`kb.cite` 返回的是 `file:line` 锚点，不是文字。这是第 12 章那条硬规则以“工具”的形式落地。调用 `kb.cite` 后又自己编造行号的 agent，是在违背服务器意愿行事 —— 而如果这样的页面被提交回知识库，第 15 章 H4 的 CI 门禁会把它抓住。",

    "`kb.search` accepts a `filter`. The filter is the tuple predicate from Chapter 18 Section 3.2. The runtime evaluates it; the agent specifies it.":
        "`kb.search` 接受一个 `filter`。这个 filter 就是第 18 章 3.2 节里的元组谓词。运行时负责求值，agent 负责声明它。",

    "Exposing the build output": "把构建产物暴露出去",

    "For a small KB, the simplest storage for the built site is to ship it inside the function bundle itself. The build step is:":
        "对小型知识库而言，放置构建好的站点最简单的方式就是把它直接打进函数 bundle 自身。构建步骤是：",

    "Run `make book-build` to produce `book/_build/html/`.":
        "跑 `make book-build` 生成 `book/_build/html/`。",

    "Run a small packing script that reads the HTML tree and writes it to a TypeScript/JavaScript module as base64-encoded bytes (or, on runtimes that support it, as native asset files).":
        "跑一段小打包脚本，读取 HTML 树，把它作为 base64 编码的字节写入一个 TypeScript/JavaScript 模块（如果运行时支持，也可以写成原生 asset 文件）。",

    "Deploy the function with the packed module.":
        "带着打包好的模块部署函数。",

    "For a larger KB — say, more than a few megabytes of built output — the asset bundle exceeds the edge runtime's per-function size limit. The options are: (a) store assets in an object store the function can read (R2 on Cloudflare, S3-compatible elsewhere); (b) split the KB into multiple functions (one per Part); (c) keep HTML in a separate CDN and let the function serve only the search index and the MCP shim. Option (c) is usually the right answer: the HTML is already a static site that a CDN serves natively.":
        "对更大型的知识库 —— 比方说构建输出超过几 MB —— asset bundle 会超出 edge 运行时的单函数体积上限。可选方案有：(a) 把 asset 放到一个函数可读的对象存储里（Cloudflare 上的 R2，其他平台上的 S3 兼容存储）；(b) 把知识库拆成多个函数（每个 Part 一个）；(c) 把 HTML 放到一个独立的 CDN，让函数只负责提供搜索索引和 MCP shim。(c) 通常是正确答案：HTML 本来就已经是一个静态站点，CDN 原生就能伺候它。",

    "The tuple filter as a publish gate": "把元组 filter 当作发布门禁",

    "A subtle point from Chapter 18 becomes operational here. An agent that habitually passes `filter: review_status == approved` will *never see* pages that are `pending`. That is the point. But a page that stays `pending` indefinitely because no human ever reviews it is, for agent purposes, invisible — even if it is useful. The Chapter 15 soft gate S2 (stale footers) already warns humans about these pages; Chapter 16's L3 discipline routes them to human attention when an L2 update cannot cover them. The agent surface does not introduce a new problem; it makes the cost of the old problem explicit. A KB that agents cannot see is a KB that has earned its invisibility.":
        "第 18 章里一个微妙的点在此变得可操作。一个习惯性传 `filter: review_status == approved` 的 agent * 永远看不到 * `pending` 状态的页面。这正是我们要的效果。但是一个一直停留在 `pending` 的页面 —— 因为始终没人评审 —— 对 agent 来说就等于不存在，哪怕它其实很有用。第 15 章的软门禁 S2（footer 陈旧）已经在向人类发出这种页面的警告；第 16 章的 L3 纪律会在 L2 更新搞不定时把它们交到人手上。agent 这个面并没有引入新问题，它只是让老问题的成本变得显性。Agent 看不见的知识库，是它自己挣来的“看不见”。",

    "A concrete day-in-the-life for one agent, one IDE, one KB:":
        "一个 agent、一个 IDE、一个知识库的具体“一日作息”：",

    "Nothing in that sequence required the agent to trust the KB. Every filter was declarative; every cite was resolved against the build-time index; every decision the agent could have fabricated was instead bounded by a mechanical answer from the server.":
        "这一连串动作中，没有一处需要 agent * 信任 * 知识库。每一个 filter 都是声明式的；每一次 cite 都靠构建期索引来解析；每一个 agent 本来可能凭空捏造的决定，都被服务器这一端给出的机械答案约束住了。",

    "Agents on a KB are not a new layer on top of the prose and code layers; they are the natural API shape the operational model already implies. A KB that has honest layer tuples, a stable page identity, and mechanically resolved citations has exactly the three tools an agent needs. The protocol (MCP) is thin; the pattern (edge function) is off-the-shelf; the trust model is exactly the one Chapter 18 and Chapter 15 already built.":
        "“跑在知识库上的 agent” 不是叠加在文稿层和代码层之上的又一新层；它是运维模型本身早已蕴含的那种自然 API 形态。一个拥有“诚实层级元组、稳定页面标识、机械解析的引用”的知识库，恰好具备 agent 需要的那三个工具。协议（MCP）薄；模式（edge function）是现成的；信任模型就是第 18 章和第 15 章已经建好的那个。",

    "What remains — Chapter 22's token budget, Chapter 23's trust and red-teaming, Chapter 24's outlook — are the governance questions that an agent-callable KB makes newly urgent. A KB that only humans read could afford a sloppy footer. A KB that agents call at scale cannot.":
        "剩下的 —— 第 22 章的 token 预算、第 23 章的信任与红队演练、第 24 章的展望 —— 都是“一个 agent 可调用的知识库”新近变得紧迫的治理问题。只被人类阅读的知识库可以承受一个马虎的 footer。一个被 agent 大规模调用的知识库承受不起。",
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
    applied, remaining, unmatched = apply("ch21-ai-agents-on-the-kb", CH21)
    print(f"ch21-ai-agents-on-the-kb                      applied={applied:3d}  remaining_untranslated={remaining:3d}  unmatched_keys={len(unmatched)}")
    for key in unmatched:
        print(f"   UNMATCHED: {key[:80]!r}")
        failed = 1
    return failed


if __name__ == "__main__":
    sys.exit(main())
