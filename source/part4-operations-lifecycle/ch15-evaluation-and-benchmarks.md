---
title: "第 15 章 —— 评测、基准与发布门禁"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - operations
  - ir-rag
  - evaluation
---

# 第 15 章 —— 评测、基准与发布门禁

## Why —— 为什么

一个回答不了 * “我怎么知道这次 build 好不好？” * 的知识库，就不能自称被“维护着”。这个问题有两种诚实的拆解，本章把两种都讲一遍：

1.  **评测** —— *知识库所驱动的检索 + 生成系统到底好不好？* 这是 IR 文献的问题：precision at k、nDCG、回答忠实度。BEIR {cite}`thakur2021beir` 和 RAGAS {cite}`es2024ragas` 这样的基准之所以存在，正是因为不同团队在趋向同一个答案。
2.  **门禁** —— *这一次具体的 build 是否格式合规到可以发布？* 这是构建工程的问题：每一页的 footer 都在吗？引用都能解析吗？变更的页面有人类审过吗？这就是第 7a 章 C4 角所问的那个问题 —— 也是 IR 基准不能直接帮上忙的那个。

评测告诉你 * 好到什么程度 * 。门禁告诉你 * 要不要发 * 。两者互补：一个没有门禁就放出去的知识库，最终会因为结构不合规的页面不断累积，在评测上失分；一个只做评测、不做门禁的知识库，拿出来的漂亮数字，对应的是一个根本无法真正部署的快照。

本章列出的门禁目录源自作者的 project-knowledge-base 工具包 {cite}`fanyamin_pkb_skill`，并新增了一列 —— * 由谁强制执行 * —— 把每一条门禁映射到一段具体的 CI 机制。原工具包的做法对“强制”是隐式处理的；把它显式化是本书的一份贡献。

## What —— 是什么

### 评测

对代码层检索系统（第 12 章）而言，有用的指标就是那些标准的 IR 指标：在一份留出的 `(问题, 引用)` 对测试集上跑 nDCG@10、recall@10、MRR。对文稿层检索，这些指标同样适用，但有一个注脚：ground truth 更难标注（同一个问题常常对应多个正确页面），并且“部分得分”更重要。两类面板都能从 RAGAS {cite}`es2024ragas` 及其同类框架里的“端到端 answer-faithfulness”指标中获益。

一个可以直接上手的初始指标集：

| Metric | Layer | What it measures | Benchmark corpus |
|:--|:--|:--|:--|
| nDCG@10 | code | Are the top-10 retrieved entities ranked correctly? | Held-out `(question, code_entities)` pairs |
| Recall@10 | code | Did we at least find the right entities? | Same |
| Answer faithfulness (RAGAS) | prose+code | Does the generated answer cite its own context? | RAGAS pipeline on sample Q&A |
| Citation resolve-rate | prose+code | Do the `file:line` anchors in generated answers resolve at HEAD? | Every generated answer |
| BEIR-style domain scores | prose | How does retrieval quality compare against public IR corpora? | BEIR {cite}`thakur2021beir` |

评测数字应当在一个固定的基准集上沿时间线追踪；单独一个 nDCG@10 = 0.74 不是什么主张，但一次同步之后从 0.74 变成 0.71 就是了。

值得注意的是，学界已经为分层评测提供了成熟的框架。RepoBench 将评测拆成三个独立的子任务 —— 检索层（R）、补全层（C）和端到端流水线（P），使得"检索质量差还是生成质量差"这个诊断问题可以被精确回答 {cite}`liu2023repobench`。这种 R/C/P 拆解与本章"评测 + 门禁"的二元结构高度一致：R 对应代码层检索指标，C 对应生成忠实度，P 对应端到端。Long Code Arena 则把评测推向了更接近真实工作负载的尺度：它覆盖了项目级补全、CI 修复、Bug 定位、模块摘要、仓库 QA 和 Commit 消息生成六类长上下文任务，平均上下文长度在 30K–80K tokens {cite}`bogomolov2024longcodearena`。知识库的评测集设计应当参考这类多任务框架，而不只是在 nDCG 上做单一维度的追踪。

### 门禁

门禁属于 * 构建工程 * 的问题。每一条门禁都是一个跑在 CI 上、只返回 pass / fail 的机械检查。目录把它们区分为 **硬门禁** （阻止发布，非零退出码）和 **软门禁** （发警告，允许发布但提醒评审者）。

#### 硬门禁 —— 阻止发布

| # | Name | What it checks | Enforced by |
|:-:|:--|:--|:--|
| H1 | Footer present | Every content page has a well-formed `PKB-metadata` footer | `check_frontmatter.py` extension |
| H2 | Footer fields valid | `review_status` ∈ {`pending`, `approved`}; `updated_by` ∈ {`human`, `ai`, `ai+human`}; `review_score` ∈ [0,5] | Same |
| H3 | AI-approval consistency | No page has `review_status: approved` with empty `reviewed_by` | Same |
| H4 | Citations resolve | Every `file:line` anchor in every page points at an existing line at HEAD | `verify` step (Chapter 7) |
| H5 | Links resolve | Every internal `](*.md#*)` link points at an existing anchor | `verify` step |
| H6 | Excerpts provenance | Every vendored excerpt's `content_sha256` matches the current file | `refresh_excerpts.py --check` |
| H7 | No `[TODO]` / `[FIXME]` in published pages | Pages with `status: published` contain no unresolved markers | grep-style check |

每条硬门禁都对应着知识库中“可能为假、且一旦为假就必须阻止发布”的一件具体事。H1–H3 强制 C2（footer 可观测且诚实）。H4–H6 强制“引用与 excerpt 持续可信”。H7 则负责抓最常见的那种“哎呀我们忘了”的失误。

#### 软门禁 —— 发警告，但允许发布

| # | Name | What it warns about | Enforced by |
|:-:|:--|:--|:--|
| S1 | Stale footers | Any page's footer `commit:` is more than N commits behind HEAD | `check-staleness.py` |
| S2 | Low review score | Any published page has `review_score` < 2 | Footer scan |
| S3 | Imbalanced Diátaxis | The published KB has no how-to pages (or no tutorial, etc.) | Histogram over `doc_type` |
| S4 | Answer-faithfulness regression | Nightly RAGAS-style scores fell > 5% from last build | CI job |
| S5 | Coverage gap | A 10-page set (C1) page is missing | `required_pages.txt` check |

软门禁是诚实的警告，不是发布阻塞项。一个带着 S3 警告的知识库仍然是知识库；它只不过多了一条评审者可见的提醒：“你正在偏离自己对页面集合做出的承诺”。

## How —— 怎么做

### 门禁 runner

整个门禁系统就是一个 CI 脚本：逐条跑每项检查并汇总结果。一个最小实现：

```text
function run_gates():
    hard_failures := []
    soft_failures := []

    for gate in HARD_GATES:
        result = gate.check()
        if not result.ok:
            hard_failures.append((gate.name, result.detail))

    for gate in SOFT_GATES:
        result = gate.check()
        if not result.ok:
            soft_failures.append((gate.name, result.detail))

    emit_report(hard_failures, soft_failures)

    if hard_failures:
        exit 1        # block publish
    exit 0            # allow publish; soft warnings in the report
```

每条门禁都暴露相同的接口：一个返回 `(ok, detail)` 的 `check()` 方法和一个稳定的 `name`。这让 CI 脚本本身很短 —— 领域知识被封装在门禁自身里 —— 并且让每条门禁都可以单独测试。

### 门禁报告

一次门禁跑完的输出是一份两段式报告：硬失败（如果有的话）在前，软警告在后。报告是 Markdown 格式的，作为 build artefact 落盘，并从触发本次构建的 PR 处链过来：

```markdown
## Hard gates

❌ H4 Citations resolve — 2 failure(s)
   content/architecture.md:47 cites internal/worker/pool.go:142
     → line 142 does not exist at commit 9f8e7d6c (file has 120 lines)
   content/data-and-api.md:23 cites cmd/sync/main.go:58
     → file does not exist at commit 9f8e7d6c

## Soft warnings

⚠ S1 Stale footers — 7 page(s)
   content/observability.md  (footer commit a1b2c3d is 42 commits behind HEAD)
   ...
⚠ S3 Imbalanced Diátaxis
   Published KB has 0 tutorials; the page-set commitment (C1) requires
   at least 1.
```

硬失败退出码会阻塞 CI 的发布步骤；软警告作为评论追加到 PR 里，这样 CI 不至于红掉，评审者仍然能看到它们。

### 一次具体的失败

假设有一个 PR 往 `internal/worker/pool.go` 里加了一个新函数 —— 诚意新增，无重命名、无破坏性改动。作者顺手编辑了 `architecture.md` 来提到这个新函数，并在那儿加了个 `<!-- TODO: add diagram -->` 标记，打算以后回来补。

跑一遍门禁：

- **H1 Footer 存在。** 通过。`architecture.md` 有 footer。
- **H2 Footer 字段合法。** 通过。字段都格式良好。
- **H3 AI 审批一致性。** 通过。作者设置了 `updated_by: human`、`review_status: pending`、`review_score: 0`、`reviewed_by:`。一切一致。
- **H4 引用可解析。** 通过。新函数的 `file:line` 可以解析。
- **H5 链接可解析。** 通过。
- **H6 excerpt 出处可验证。** 通过。
- **H7 已发布页面中无 `[TODO]`。** **失败。** `<!-- TODO -->` 标记出现在一个 `status: published` 的页面中。

门禁阻止了发布。评审者看到的是一行失败信息 + 一个指向 diff 第 47 行的指针。本次检查的成本：对 `content/**/*.md` 的一次 grep，在 30 ms 内完成。跳过这次检查的成本：线上知识库发布了一个图示写着“TODO”的页面 —— 有用户看到了，对它的信任感轻微折损。这种折损不会自己免费恢复。

## Example —— 范例

一次真实周五下午 PR 上的完整门禁跑动（数据已匿名化）：

```text
$ python build_kb_gates.py
Running 7 hard gates and 5 soft gates across 137 pages...

Hard gates:
  H1 Footer present              137/137 pass
  H2 Footer fields valid         137/137 pass
  H3 AI-approval consistency     136/137 pass — 1 FAIL
       content/runbook.md: review_status=approved but reviewed_by=''
  H4 Citations resolve           423/425 pass — 2 FAIL
       content/architecture.md:47  internal/worker/pool.go:142  (line missing)
       content/data-and-api.md:23  cmd/sync/main.go:58          (file missing)
  H5 Links resolve               612/612 pass
  H6 Excerpts provenance         18/18  pass
  H7 No [TODO] in published      137/137 pass

Soft gates:
  S1 Stale footers               7 page(s) > 30 commits behind HEAD
  S2 Low review score            0 page(s)
  S3 Imbalanced Diátaxis         WARN — published KB has 0 tutorials
  S4 Answer-faithfulness         pass — 0.81 (prev 0.82; delta −0.01)
  S5 Coverage gap                pass — all 10 required pages present

Hard failures: 3   Soft warnings: 2
FAIL — publish blocked. See report above.
```

作者看到的是三件具体要修的事，而不是一份 400 个文件的评审队列。修完这三件大约花 10 分钟：一个页面的 `reviewed_by` 字段被补上，一条引用被更新到新的行号，一条坏掉的 `file:line` 被重新指向替代 `cmd/sync/main.go` 的那个文件。重跑门禁：全部通过。发布继续。

## Conclusion —— 小结

评测（IR 指标、faithfulness 分数）告诉你：知识库一旦发布出去是否有用。门禁（硬 / 软检查）告诉你：这一次具体构建是否根本就“可以发”。两者都是机械的，都很便宜。但今天大多数知识库两者都拒绝上 —— 因为要加它们，就得对第 7a 章那四个角落做出承诺：footer 不在，H1 就跑不起来；运维模型不解析引用，H4 就跑不起来。

下一章把整条回路闭合：当硬门禁失败、或软门禁告警时， * 修复到底长什么样？ * 答案就是三级更新策略（C3）—— 它的真正机制在本章已经先铺了一下，但正经讲述属于第 16 章。

## 参考文献

```{bibliography}
:filter: keywords % "operations" or keywords % "ir-rag" or keywords % "evaluation" or keywords % "self-citation"
```
