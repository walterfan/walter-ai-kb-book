---
title: "第 9 章 —— 解析与实体抽取"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - code-layer
  - parsing
  - deepwiki
---

# 第 9 章 —— 解析与实体抽取

本章一图览 —— 一个实体模型、每种语言一个适配器、解析器本身必须处理的三类坑：

```{mermaid}
mindmap
  root((Parser))
    Entity model
      Stable ID
      Four kinds
      Location-aware
      Signature and doc
    Per-language adapters
      Go via tree-sitter
      Python via tree-sitter
      Java via tree-sitter
      Add new in 150 LoC
    Pitfalls
      Resource leaks
      Anonymous functions
      Multi-line signatures
    Common mistakes
      Regex MVP
      Unstable IDs
      Too many entity kinds
```

昨晚你写了第一版。60 行正则。`func `、`def `、`class ` —— 这能有多难？今天早上索引器在一个 4 kLOC 的仓库里吐出了 15 000 个“函数”。其中一半的命中是 `map(...)` 里的闭包字面量。有 3 个是字符串字面量里那个单词 `function`。你基于这些实体建起来的调用图是一出漂亮的虚构：80% 的边都指向匿名的 `func1`、`func2`、`func3`。本章之后的每一章 —— 嵌入、图谱、检索、生成 —— 都在这个模块的输出下游。**本章讲的是：为什么解析器是代码知识库里“杠杆最大”的一个模块，以及一版“乏味地正确”的解析器具体长什么样。**

## Why —— 为什么

下游的一切 —— 嵌入（第 10 章）、图谱（第 11 章）、检索（第 12 章）、回答（第 13 章）—— 都是解析器输出的函数。解析器漏了一个方法，任何检索器都找不到它。解析器把签名和函数体搞混了，每一份嵌入都会偏。解析器是代码知识库中杠杆最大的一个模块；它也最容易在赶工时被仓促写完、之后再也没人碰。

朴素解析器 —— “Go 按 `func ` 切、Python 按 `def ` 切、Java 靠正则” —— 只要碰上第一个嵌套泛型、第一个多行签名、第一个匿名函数字面量、第一个 heredoc，或者几十种语言特有怪癖中的任何一个，就会当场崩溃。DeepWiki 方法论 {cite}`fanyamin2026deepwiki` 在 §4 明确说：在 * 一个真实的 * 解析器之上，为每种语言写 * 一个薄薄的抽取器 * ，比 grep 风格的替代方案既更便宜也更稳健。

## What —— 是什么

代码层参考实现中 `reference-impl/code-kg/parser` 这个包对抽取契约的定义，由三个设计决策确定。

**1 —— 一个解析器、多种语言。** Tree-sitter {cite}`brunsfeld_treesitter` 为 Go、Java、Python 提供了统一的语法树 API，附带增量解析模型，以及知识库场景很看重的容错性：一个正在被编辑中的文件，仍然能产出可用的语法树。另一条路（每种语言各自一套工具链：`go/ast`、`javaparser`、`libcst`）会把依赖和“一次性 bug”的表面积都翻三倍。

**2 —— 一份与语言无关的中间表示。** Tree-sitter 吐出的东西，一律坍缩到一个 `CodeMetadata` 结构：一张文件列表，每个文件下含其函数和类；每个实体带 `name`、`start_line`、`end_line`、`signature`、`docstring`、`body`。这份 IR 小到可被完整地讨论，大到能喂饱每一个下游阶段，而且 —— 关键是 —— * 与语言无关 * 。第 10 章拿它去嵌入，第 11 章拿它建图，第 14 章拿它做差分。

**3 —— 支持的扩展名和要跳过的目录是“配置”，不是“推断”。** 解析器拒绝深入 `vendor/`、`node_modules/`、`.git/`、`__pycache__/`、`dist/`、`build/`、`target/`、`.next/`。这份默认名单里每一条都来自某次“在 monorepo 上首次运行被噎死”的疤痕。`allamanis2018survey` {cite}`allamanis2018survey` 在学术规模上整理了同一类病症：绝大多数 “big code” 语料在模型训练前都需要一轮激进的 vendor 过滤。

## How —— 怎么做

解析器服务一共 66 行。以下代码来自 `reference-impl/code-kg/parser/parser.go`，所属 commit 记录在开头的元数据里：

```{literalinclude} ../examples/part3-code-layer/ch09/parser.go
:language: go
:lines: 11-50
:caption: parser.Service — supported extensions, skip dirs, single Walk.
```

这段代码上有三点值得点名：

- 第 26–30 行（`supportedExtensions`）就是知识库索引的那个封闭的文件类型集合。增加第四种语言只需改一行 —— 以及一项下游的评审义务，因为 tree-sitter 语法也得跟着链接进来。

- 第 32–50 行（`CollectSupportedFiles`）展示了带 `SkipDir` 快捷路径的 `filepath.Walk`。在一个 12 万文件的 monorepo 里，光 `node_modules/` 分支就占了 95% 的 inode 数量；在下探之前就惰性地跳过它，才是让首次同步可以忍受的关键。

- `CollectGoFiles`（源码第 52 行）是一个历史遗留的别名，随时间不断拓宽：它现在返回的是*所有*支持的文件，不只是 Go。在一个被很多调用方使用的库中，重命名是有风险的，所以项目保留了旧名并添加了一个新方法 —— 这是一种在 Git blame 中有清晰谱系的常见模式。

### 实体模型

下游各阶段消费的 IR 就是 `CodeEntity` 这个结构体：

```{literalinclude} ../examples/part3-code-layer/ch09/domain_types.go
:language: go
:lines: 3-30
:caption: CodeEntityType enum plus the canonical CodeEntity record.
```

这份定义中有三个方面会带来结构性的连锁后果：

- `EntityType` 是一个小型的封闭枚举（`package`、`file`、`function`、`class`、`struct`、`interface`、`variable`、`constant`）。新增实体类型需要做一次迁移 —— 这是特性，不是 bug。关于边的对称论证参见第 11 章 §*有界的关系分类法*。

- `StartLine` 和 `EndLine` 是每个实体上的一等公民字段。它们让实体 ID（第 11 章）在跨次索引时保持稳定，并让第 13 章的生成器能以 `file.ext:L12-L47` 的形式引用结果。知识库里所有下游能力，归根结底都依赖于解析器保留了原始源码坐标。

- `Body`、`Signature` 和 `DocString` 被分别保存。body 在存储之前（在 `parseFileForSync` 中）截断到 4 000 字符，而 signature 和 docstring 从不截断。这种拆分是第 10 章 *嵌入头部而非函数体* 规则的基础：signature 和 docstring 完整地存活到嵌入器；body 只存活到检索器，且是截断的。

### 每语言适配器

Tree-sitter 吐出的是语法树，不是命名实体列表。从语法树到实体列表的转换位于另一个包里（`reference-impl/code-kg/rag` 下的每语言适配器，本书没有把它 vendor 进来，因为模板代码太多），但其模式很短，值得显式写一遍。对每种支持的语言，写一个 visitor：

1.  前序遍历整棵语法树。
2.  当它遇到一个 kind 处于每语言白名单中的节点 —— Go 的 `function_declaration`、`method_declaration`、带 `struct_type` 或 `interface_type` 的 `type_spec`；Python 的 `function_definition`、`class_definition`；Java 的 `method_declaration`、`class_declaration` —— 就记录这个实体。
3.  使用节点的 source range 来填充 `StartLine`、`EndLine` 和 `Body`。
4.  使用前导的 doc-comment 节点（如果存在）作为 `DocString`。

纪律是： * 每种语言一个 visitor，尽可能笨 * 。不做跨文件解析（那是第 11 章的图谱 builder 的事）、不维护符号表、不做类型推断。语言特有的复杂度由 tree-sitter 语法来承担；我们自己的代码保持小。

### 来自生产的坑

下面三种失败模式值得读者特别留意，因为一旦踩上，排查都要花时间：

- **资源泄漏。** Tree-sitter 的树持有一个指向 Rust 所有的 arena 的指针，必须通过 `tree.Close()`（或对应 binding 的等价方法）释放。忘记释放不会立即崩溃；它会在一个长期运行的索引器中以缓慢的内存增长浮现。`defer tree.Close()` 是强制性的。

- **闭包与匿名函数。** 每种语言都有它们，而且它们*全部*会以"类函数"节点出现在语法树里。把它们作为实体发出会用数百个叫 `func1`、`func2` 之类的匿名节点污染图谱。修复方法是加一个每语言的过滤器：只发出顶层和方法级的函数；把匿名函数当作其外围实体的 body 的一部分处理。

- **泛型类型与多行签名。** 我们存储的*签名*是 body 的第一个非空行 —— 通过我们在第 10 章还会再见的 `extractSignature` 辅助函数。对于像 `func Map[K comparable, V any](m map[K]V) []K` 这样的 Go 泛型，这管用。但对于一个参数跨越五行换行的 Java 方法，它会生成一个截断的签名。我们的修复方案是把完整签名从 tree-sitter 节点的 range 中取出，而不是从朴素的按行拆分中取 —— 参见 `extractSignature` 的用法。这被标注为一个已知 bug，有跟踪的修复计划。

### 常见错误

每当团队试图在解析器阶段抄近道，下面这三种反模式就会冒出来。每一个在前期看起来都 * 挺诱人 * 的，因为好像省事；每一个在下游都会以 10 倍代价偿还。

**1 —— “MVP 用正则就够了”。** 症状是一行识别符正则 —— `/func\s+(\w+)/` —— 在一个 4 kLOC 的仓库里吐出 15 000 个实体。注释也命中。包含单词 `function` 的字符串字面量也命中。测试框架里的 `describe("function X", ...)` 也命中。正则不是 * 近似 * 的解析器 —— 它是一个完全不同的函数。每一个下游章节（嵌入、图谱、检索）都会继承并放大这些噪声。从第一次提交起就用真正的解析器（tree-sitter、语言服务、编译器前端）。它不是那条慢路径。

**2 —— 不稳定的实体 ID。** 症状是：在一个没改过的仓库上重跑 indexer，你的向量存储居然出现了 diff。为什么？因为 `id` 是 `filepath + name` 拼的，或者是一个把完整函数体一起哈希进去的 hash（于是一次空白改动就会级联），或者它里面干脆带了一个自增计数器。这样一来，图谱的边就会指向已经不存在的 ID。解决办法是第 10 章的方案：`sha256(repoID + filePath + entityType + name + startLine)[:16]`。在重建索引之间稳定；但又敏感到：把一个函数挪到新的一行就会产生新 ID（这正是正确行为）。

**3 —— 吐出“过于聪明”的实体类型。** 症状是：一个解析器吐出了 23 种实体 —— `struct-field`、`enum-variant`、`type-alias`、`const-declaration` —— 然后检索层开始要琢磨“到底哪些类型可以混在一起排”。基数爆炸，排序信号被稀释，图谱的节点类型多到画不下任何像样的可视化。就从第 9 章的四种开始 —— `package`、`type`、`method`、`function` —— 哪怕是 Java（虽然“interface”感觉和“class”不一样）。你随时可以以后再细化；但你没法把一个已经被嵌进下游 200 条规则的实体类型“撤回”。

## Example —— 范例

四行命令就能在代码层参考实现自身上复现一次演示：

```bash
cd ~/reference-impl/code-kg
go run ./cmd/code-kg register --name code-kg --path . --id demo
go run ./cmd/code-kg sync --repo-id demo
sqlite3 code-kg.db "SELECT entity_type, COUNT(*) FROM entities
                    WHERE repo_id='demo' GROUP BY entity_type;"
```

在本章节选对应的 commit 上，输出如下：

```
class|24
function|412
```

比例比绝对数字更重要：一个健康的 Go 代码库是“函数密集”的。如果你在一个 50 kLOC 的 Java 仓库上看到 5000 个“函数”，那就是你的解析器把每个闭包都当成了实体 —— 去修那个 visitor。

## Conclusion —— 小结

解析器很小，但第三部分的每一层都靠它立下的三条契约活着：跨语言统一的 IR（主张 1）、每个实体都忠实保留源码坐标（主张 2）、以及对 vendor 目录的激进默认跳过名单（主张 3）。这三条哪一条破了，下游每一章也跟着破。

第 10 章把这份 IR 作为输入，把每个实体的 * 身份 * 那一半（语言、类型、名字、签名、docstring）变成一个向量 —— 这也正是众所周知、大多数 code-RAG 教程会走偏的那一段。

## 参考文献

```{bibliography}
:filter: keywords % "parsing" or keywords % "code-layer" or keywords % "deepwiki"
```
