---
title: "参考文献：仓库级代码理解与软件知识库论文导读"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - reference
  - repo-level
  - survey
---

# 参考文献：仓库级代码理解与软件知识库论文导读

本目录收录了 10 篇对构建和使用**软件知识库（Software Knowledge Base）**具有重要参考价值的学术论文，按照"What / Why / How / Example / Conclusion / Reference"的结构进行解析，重点阐述每篇论文对软件知识库建设的具体启示。

---

## 论文列表

| 编号 | 论文 | 会议/年份 | 核心贡献 | 对知识库的价值 |
|------|------|----------|---------|--------------|
| [01](01-repoformer-selective-retrieval.md) | **Repoformer**: Selective Retrieval for Repository-Level Code Completion | ICML 2024 | 选择性检索，先判断是否需要检索再触发 | 检索路由层设计，降低噪声和延迟 |
| [02](02-codeplan-repository-level-planning.md) | **CodePlan**: Repository-level Coding using LLMs and Planning | FSE 2024 | 将仓库级代码变更建模为"规划 + 多步编辑" | 支持跨文件变更辅助，不只做问答 |
| [03](03-repograph-code-graph-navigation.md) | **RepoGraph**: Enhancing AI Software Engineering with Repository-level Code Graph | ICLR 2025 | 仓库级代码图作为结构导航层 | 图索引 + 语义检索双层架构 |
| [04](04-repoagent-documentation-generation.md) | **RepoAgent**: LLM-Powered Repository-level Code Documentation Generation | arXiv 2024 | 自动生成并增量维护仓库文档 | 文档自动化，知识库内容生产 |
| [05](05-repocoder-iterative-retrieval-generation.md) | **RepoCoder**: Repository-Level Code Completion Through Iterative Retrieval and Generation | EMNLP 2023 | 检索-生成-再检索的迭代流程 | 多轮检索架构，提升复杂问答质量 |
| [06](06-llm-kg-synergy-repo-qa.md) | **Synergizing LLMs and KGs** for Software Repository-Related Question Answering | arXiv 2024 | 软件仓库知识图谱 + LLM 协同问答 | 与"软件知识库"最直接对应的研究 |
| [07](07-repo-level-prompt-generation.md) | **Repository-Level Prompt Generation** for Large Language Models of Code | ICML 2023 | 从整个仓库组织最优上下文 | 上下文构建策略，Repo RAG 起点 |
| [08](08-repobench-benchmarking.md) | **RepoBench**: Benchmarking Repository-Level Code Auto-Completion Systems | arXiv 2023 | 三层评测体系：检索/补全/端到端 | 知识库质量评估框架 |
| [09](09-long-code-arena-benchmarks.md) | **Long Code Arena**: A Set of Benchmarks for Long-Context Code Models | arXiv 2024 | 6 类长上下文代码任务评测基准 | 大仓库、跨模块场景的评测标准 |
| [10](10-cgm-graph-integrated-llm.md) | **CGM**: Code Graph Model — A Graph-Integrated LLM for Repository-Level SE | NeurIPS 2025 | 图结构直接集成到 LLM 注意力层 | 开源可部署的前沿知识库后端方案 |

---

## 按知识库建设阶段分类

### 阶段一：基础索引层（索引代码仓库）

| 论文 | 贡献 |
|------|------|
| [07 RLPG](07-repo-level-prompt-generation.md) | 仓库上下文的分类体系（导入、相似代码、使用示例等） |
| [04 RepoAgent](04-repoagent-documentation-generation.md) | 自动生成多层次文档作为索引内容 |
| [03 RepoGraph](03-repograph-code-graph-navigation.md) | 构建代码结构图作为第二层索引 |
| [06 LLM+KG](06-llm-kg-synergy-repo-qa.md) | 将仓库抽象为知识图谱，支持精确关系查询 |

### 阶段二：检索与上下文组装

| 论文 | 贡献 |
|------|------|
| [01 Repoformer](01-repoformer-selective-retrieval.md) | 选择性检索，降低无效检索的成本和噪声 |
| [05 RepoCoder](05-repocoder-iterative-retrieval-generation.md) | 迭代检索，用初步生成改善二次检索质量 |
| [10 CGM](10-cgm-graph-integrated-llm.md) | 子图上下文单元，精准的结构化上下文组装 |

### 阶段三：生成与规划

| 论文 | 贡献 |
|------|------|
| [02 CodePlan](02-codeplan-repository-level-planning.md) | 跨文件变更的规划与多步执行 |
| [10 CGM](10-cgm-graph-integrated-llm.md) | 图集成注意力机制，结构感知的代码生成 |

### 阶段四：评测与质量保证

| 论文 | 贡献 |
|------|------|
| [08 RepoBench](08-repobench-benchmarking.md) | 三层评测体系，分层诊断系统瓶颈 |
| [09 Long Code Arena](09-long-code-arena-benchmarks.md) | 长上下文、多任务的综合评测标准 |

---

## 技术演进脉络

```
2023 ─────────────────────────────────────────────────────────── 2025

ICML 2023              EMNLP 2023           ICML 2024        ICLR 2025    NeurIPS 2025
[07 RLPG]    →    [05 RepoCoder]    →   [01 Repoformer]  →  [03 RepoGraph]  →  [10 CGM]
"仓库上下文        "迭代检索-生成"       "选择性检索"         "图结构导航"       "图集成LLM"
 的价值"                                                                      "43% SWE-bench"

                 arXiv 2023              FSE 2024         arXiv 2024
                 [08 RepoBench]    →   [02 CodePlan]  →  [04 RepoAgent]
                 "评测体系"             "规划+多步编辑"    "文档自动化"
                                                         [06 LLM+KG]
                                                         "KG+LLM 问答"
                 arXiv 2024
                 [09 Long Code Arena]
                 "长上下文评测"
```

---

## 推荐阅读顺序

**如果你要快速入门**：07 → 05 → 01（理解 Repo RAG 的基础概念和演进）

**如果你要构建生产系统**：01 → 08 → 03 → 06（检索路由 + 评测 + 图索引 + KG问答）

**如果你要支持代码变更辅助**：02 → 03 → 10（规划 + 图导航 + 图集成模型）

**如果你要建立评测体系**：08 → 09（三层评测 + 长上下文评测）

**如果你关注最前沿方向**：10 → 03 → 06（图集成LLM + 图检索 + KG协同）

```{toctree}
:maxdepth: 1
:hidden:

01-repoformer-selective-retrieval
02-codeplan-repository-level-planning
03-repograph-code-graph-navigation
04-repoagent-documentation-generation
05-repocoder-iterative-retrieval-generation
06-llm-kg-synergy-repo-qa
07-repo-level-prompt-generation
08-repobench-benchmarking
09-long-code-arena-benchmarks
10-cgm-graph-integrated-llm
```
