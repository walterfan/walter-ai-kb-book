---
title: "附录 A —— 端到端：从杂乱文件夹到可发布 Wiki"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - appendix
  - prose-layer
---

# 附录 A —— 端到端：从杂乱文件夹到可发布 Wiki

这个附录逐步复现了第二部分的承诺：把几份手工写出的文件变成一个结构良好的
wiki，带上 frontmatter、分类结果、信任审计，以及一个可以直接跑起来的
HTTP 服务。这里的每一条命令都在随书发布的那个 commit 上实际跑过；每一段
输出都是真实捕获自一个干净的 `/tmp` 目录，而不是编造出来的。

自己动手跑一遍，大约十五分钟，你就会对第 4 章到第 7 章所描述的一切形成一个
真正可操作的心智模型。

## 为什么

文稿层那几章论证的是：一个**基于文件、由流水线校验**的 wiki 为什么是软件
知识库的合适底座。这个附录把这套论证完整跑一遍，而且刻意选择：

- 一个非常小的输入集（三个形态不同的文件）；
- 零网络依赖（强制启用启发式分类器）；
- 零隐藏状态（每一个输出都是你能直接 `cat` 出来的文件）。

如果这份 walkthrough 在你的机器上跑不通，那说明在更深的书稿章节开始发挥作用
之前，工具链本身就已经出问题了。先把这个修好。

## 是什么

这是一份三阶段实录：

1.  准备三个形态混杂的输入文件（`.md`、`.txt`）。
2.  跑通六个 CLI 动词：`init → import dir → verify → build →
    status → serve`。
3.  观察每一个阶段都向磁盘写出了真实结果，以及最终的 `content/`
    目录已经是一份合法、可直接阅读的 wiki。

## 怎么做

### 前置条件

```bash
# From the repo root.
$ make build-backend
# → produces ./backend/wiki-cli (~35 MB statically linked Go binary)
```

在这个附录里，我们关闭 LLM 分类器，以保证不同机器上产出的结果能够做到
**逐字节一致**。启发式分类器是第 6 章里介绍的 fallback 路径；它当然没有
真正的 LLM 聪明，但正因为如此，才特别适合写进一本书。

```bash
$ export LLM_API_KEY=   # empty — force heuristic classifier
$ export LLM_BASE_URL=
```

### 阶段 1 —— 杂乱输入

```bash
$ mkdir -p /tmp/book-appx-a/input
$ cat > /tmp/book-appx-a/input/install.md <<'MD'
# How to install the service

Run `make build` and then `./bin/service --port 7500`. The binary
listens on the given port, reads config from `/etc/service.yaml`, and
emits structured JSON logs to stdout.

## Prerequisites

- Go 1.22 or later
- Make
MD

$ cat > /tmp/book-appx-a/input/api-reference.md <<'MD'
# API Reference

## GET /health
Returns 200 OK with JSON body `{"status":"ok"}`.

## POST /pages
Creates a wiki page. Body:

` ` ` json
{ "title": "...", "body": "...", "doc_type": "reference" }
` ` `

## DELETE /pages/{slug}
Removes a page. Requires `admin` role.
MD

$ cat > /tmp/book-appx-a/input/architecture-notes.txt <<'MD'
Why we chose file-based storage

Database-backed wikis couple the content to the database lifecycle.
We want the wiki tree to be a plain Git repository so every page is
diffable, reviewable, and auditable via git blame. That leaves the
search and pipeline layers as the only thing the server needs to add.
MD

$ ls /tmp/book-appx-a/input/
api-reference.md    architecture-notes.txt    install.md
```

三个文件，三种形态。一个是 how-to（标题以 "How to" 开头）；一个是
reference（结构化 endpoint）；一个是 explanation（`.txt`，没有 Markdown
标题）。一个好的流水线至少应该把前两个正确地放进各自的 Diátaxis 桶里。

### 阶段 2 —— 跑通六个动词

**`init`** 会脚手架出一份全新的 wiki，拷贝模板，并创建一个管理员账号：

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki init kb
2026/04/18 05:26:55 Copying wiki template from wiki-template to /tmp/book-appx-a/wiki
========================================
  Default admin account created
  Username: admin
  Password: [REDACTED_PASSWORD]
  Please change the password after login.
========================================
Wiki initialized (kind=kb) in /tmp/book-appx-a/wiki

$ ls /tmp/book-appx-a/wiki/
content    metadata

$ ls /tmp/book-appx-a/wiki/content/
_assets    devops    home.md    productivity    programming
$ ls /tmp/book-appx-a/wiki/metadata/
SCHEMA.md   index.md   log.md    skills/    sources/    users.yaml    wiki.yaml
```

`content/` 里已经有模板预置的几页；`metadata/` 里有 `SCHEMA.md`
契约（第 5 章）、带生成后 admin hash 的 `users.yaml`，以及一个骨架
`wiki.yaml` 配置。每一个字节都是纯文本。

**`import dir`** 会遍历输入树，对每个文件做分类，在 `content/` 下写出页面，
并记录导入日志：

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki import dir /tmp/book-appx-a/input
ImportDir complete: 3 created, 0 skipped, 0 errors
```

三个输入文件，三个创建出的页面。我们来看其中一个：

```
$ cat /tmp/book-appx-a/wiki/content/install.md
---
title: How to install the service
slug: install
summary: |-
    Run `make build` and then `./bin/service --port 7500`. The binary
    listens on the given port, reads c
created: 2026-04-17T21:26:55.152331Z
created_by: human
updated: 2026-04-17T21:26:55.152331Z
status: published
doc_type: reference
verification_status: unreviewed
source:
    type: doc
    path: /tmp/book-appx-a/input/install.md
---
# How to install the service

Run `make build` and then `./bin/service --port 7500`. The binary
listens on the given port, reads config from `/etc/service.yaml`, and
emits structured JSON logs to stdout.

## Prerequisites

- Go 1.22 or later
- Make
```

注意看，流水线哪些地方做得**完全正确**，哪些地方只是**近似正确**。两者都很有
价值，因为它们能告诉你启发式分类器到底在哪儿停止帮忙：

- 正确：`title` 从第一行 `# ` 标题里提取；`slug` 由文件名推导；
  `summary` 截取前 100 个字符；`source.path` 记录精确输入文件；
  `verification_status` 被设为 `unreviewed`（第 5 章里的默认信任状态，
  即便输入是人写的也照样适用）。
- 近似：`doc_type: reference`。真正的 LLM 分类器会从
  "How to install…" 这个标题中判断出它是 `how-to`。启发式分类器不会把标题
  与 Diátaxis 桶做交叉校验。这是一个**发现**，不是 bug：人类
  （或者后面更聪明的分类器）可以把 `doc_type` 提升上去，而下面的 `verify`
  会把这件事标出来。

**`verify`** 会审计每一页，并输出一份结构化报告：

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki verify | python3 -c \
    'import sys,json; r=json.load(sys.stdin); \
     print(json.dumps(r["summary"], indent=2)); \
     print("categories used:", \
           sorted([k for k,v in r.items() if isinstance(v,list) and v]))'
{
  "total_issues": 6,
  "auto_fixable": 0,
  "categories": 1
}
categories used: ['consistency']
```

六个问题，全部都属于 `consistency`：模板预置的样例页里，slug 与文件名并不一致
（例如一个叫 `concurrency.md` 的文件，其 slug 写的是
`go-concurrency-patterns`），这只是模板作者的风格。我们刚导入的三个页面没有
触发任何问题。生产环境里，要么重命名这些种子页，要么直接跑
`verify --auto-fix`。

关键在于：`verify` 在一秒以内跑完，并输出了机器可读的结果。把它接进 CI，
例如 `wiki-cli verify | jq '.summary.total_issues'`，然后在这个数字上升时
让构建失败，就是最自然的下一步。

**`build`** 会重建内存索引，以及那份供静态发布路径使用的 `INDEX.md`
（第 7 章）：

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki build
Build complete
```

**`status`** 会用 JSON 报告顶层健康指标：

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki status
{
  "kind": "kb",
  "wiki_root": "/tmp/book-appx-a/wiki",
  "content_dir": "/tmp/book-appx-a/wiki/content",
  "page_count": 10,
  "source_count": 0,
  "last_init": "0001-01-01T00:00:00Z",
  "last_update": "0001-01-01T00:00:00Z",
  "last_verify": "0001-01-01T00:00:00Z",
  "last_build": "0001-01-01T00:00:00Z",
  "wiki_base_url": "http://localhost:8080",
  "git_available": false,
  "last_commit": ""
}
```

十页内容（模板里的七页 + 我们导入的三页），没有待处理的原始 sources。
`git_available: false` 是因为 `/tmp/book-appx-a/wiki` 还不是一个 Git 仓库；
如果你在里面跑一次 `git init`，它就会变成 `true`，并解锁第 5 章里描述的
auto-commit 行为。

**`serve`** 会针对同一棵树启动 HTTP 服务：

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki serve --port=7500
# → http://localhost:7500
#   pages listed at /api/v1/pages
#   single page at /pages/{slug}
#   search at /api/v1/search?q=<tokens>
```

在浏览器里访问 `http://localhost:7500/pages/install`；来自
`content/install.md` 的页面会被渲染出来，frontmatter 被隐藏，而 Markdown
正文被转成 HTML。再请求
`http://localhost:7500/api/v1/search?q=port`，第 7 章讲过的 tokenizer
就会返回 `install` 页，以及任何预置页里提到 "port" 的内容，因为此时
`content/` 下的一切都已经进入了内存索引的 postings list。

### 阶段 3 —— 把它变成 Git 仓库

基于文件的 wiki 存在的根本理由，就是让你刚刚搭出来的一切都能像代码一样被版本化。
只要两条命令：

```
$ cd /tmp/book-appx-a/wiki
$ git init -q && git add -A && git commit -q -m "init: 3 imported pages"
$ git log --oneline
4a1b2c3 init: 3 imported pages
```

重新跑一遍 `status`，然后观察：

```
$ ./backend/wiki-cli --wiki-dir=/tmp/book-appx-a/wiki status | jq '.git_available, .last_commit'
true
"4a1b2c34d5e6"
```

这个 wiki 现在会把 commit SHA 带进状态输出里；之后任何通过 API 的写操作，
都会自动 commit，写出一条描述性 message，并把新的 commit SHA 写进受影响
页面的 `frontmatter.commit` 字段。于是，第 5 章关于 where-provenance 的主张
就变成了一个真正可运行的机制。

## 示例

把这次运行中产生的一个具体 artefact 再拿出来看一遍：

```yaml
# /tmp/book-appx-a/wiki/content/install.md (frontmatter only)
title: How to install the service
slug: install
summary: |-
    Run `make build` and then `./bin/service --port 7500`. The binary
    listens on the given port, reads c
created: 2026-04-17T21:26:55.152331Z
created_by: human
updated: 2026-04-17T21:26:55.152331Z
status: published
doc_type: reference          # a smarter classifier would say how-to
verification_status: unreviewed
source:
    type: doc
    path: /tmp/book-appx-a/input/install.md
```

其中有七个字段编码了第 5 章的 provenance 记录。`verification_status:
unreviewed` 是能在往返过程中稳定保留下来的默认信任状态。`source.path`
携带了输入文件在磁盘上的精确位置。这里没有一项依赖数据库；也没有一项需要供应商。

## 结论

第二部分的四章是在抽象层面讲文稿层；这个附录则证明了，这个抽象
**小到你能拿在手里**。一个二进制、四个命令、三个输入文件，十五分钟后，
你就有了一份可工作、可审计、可搜索、可发布的 wiki。

有两点值得明确写出来：

1.  **启发式分类器是一个特性，不是弱点。** 它保证流水线能在 air-gapped
    环境中工作，让测试复现变得简单，并给出一个清晰的性能下限：LLM 分类器
    必须**比它更好**，才值得支付额外成本。
2.  **每一个阶段都向磁盘做了承诺。** 这份 walkthrough 里没有任何东西只活在
    内存里。把服务关掉，把笔记本关机，明天再回来，这个 wiki 依然还在
    `/tmp/book-appx-a/wiki/` 里，依然有效，依然能在 Git 里被 review。

从这里开始，本书会进入代码层。第三部分会把**同样的文件式纪律**
应用到编译器知道的那部分世界：source tree 的 embeddings、代码图，
以及让 AI 助手能够同时理解这个附录里的 prose 与它所描述代码的混合检索。

## 参考文献

```{bibliography}
:filter: keywords % "prose-layer"
```
