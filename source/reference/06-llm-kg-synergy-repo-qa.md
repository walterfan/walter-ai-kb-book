---
title: "Synergizing LLMs and Knowledge Graphs: A Novel Approach to Software Repository-Related Question Answering"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - reference
  - knowledge-graph
  - llm-kg-synergy
---

# Synergizing LLMs and Knowledge Graphs: A Novel Approach to Software Repository-Related Question Answering

> **论文信息**：arXiv 2024，2025年10月修订版 | [arXiv:2412.03815](https://arxiv.org/abs/2412.03815)

---

## What — 这篇论文解决什么问题

本文研究的问题是：**如何将软件仓库的知识结构化为知识图谱（Knowledge Graph），并将 KG 与 LLM 结合起来，支持高质量的软件仓库问答（Repo QA）**？

纯文本 RAG 在软件仓库问答中的瓶颈：

1. **关系推理弱**：无法回答"哪些模块依赖了 X"、"Y 接口有几个实现"等结构性问题；
2. **上下文边界模糊**：检索到的文本片段缺乏精确的实体关系表示；
3. **多跳推理困难**：`A 调用 B，B 依赖 C，C 中有 bug` 这类推理链对纯文本 RAG 不友好；
4. **知识更新困难**：代码变更后，文本索引需要全量重建，而 KG 支持精确的节点/边更新。

本文提出：将软件仓库抽象为**软件知识图谱（Software Repository Knowledge Graph）**，并设计专门的 LLM + KG 协同问答框架。

---

## Why — 为什么这个方向对软件知识库最对口

在本书所有参考论文中，**本文与"软件知识库"这一主题最直接对应**：

- **研究对象完全匹配**：直接研究"软件仓库 KG + LLM 问答"，不是代码补全或文档生成；
- **适用场景最广**：Repo QA、依赖关系问答、开发流程问答、架构决策查询；
- **技术路径最成熟**：KG 是知识表示的经典范式，与 LLM 结合代表了知识库技术的前沿方向；
- **可维护性最强**：KG 的增量更新天然支持知识库的持续维护。

---

## How — 核心方法

### 1. 软件仓库知识图谱构建（Software Repo KG Construction）

定义专用的**软件本体（Software Ontology）**：

```
实体类型 (Entity Types):
  - Repository      (仓库)
  - Module          (模块/包)
  - File            (文件)
  - Class           (类)
  - Function        (函数/方法)
  - Variable        (变量/常量)
  - Dependency      (外部依赖)
  - Issue           (Bug/Feature)
  - Commit          (提交记录)
  - Developer       (开发者)

关系类型 (Relation Types):
  - contains        (包含关系)
  - imports         (导入关系)
  - calls           (调用关系)
  - inherits_from   (继承关系)
  - implements      (接口实现)
  - depends_on      (外部依赖)
  - modifies        (提交修改)
  - fixes           (修复 Issue)
  - authored_by     (作者关系)
```

### 2. LLM + KG 协同问答（Synergistic QA）

两个组件的分工：

| 组件 | 擅长 | 负责 |
|------|------|------|
| **知识图谱** | 精确关系查询、符号定位、多跳推理 | 检索结构化事实 |
| **LLM** | 自然语言理解、逻辑推理、文本生成 | 解析意图、综合答案 |

问答流程：

```python
def repo_qa(question: str) -> str:
    # Step 1: LLM 解析问题意图，生成 SPARQL/Cypher 查询
    kg_query = LLM.parse_to_query(question)
    
    # Step 2: 在知识图谱上执行查询，获取结构化事实
    kg_facts = knowledge_graph.query(kg_query)
    
    # Step 3: 必要时检索相关代码片段作为补充
    code_context = retriever.search(question, top_k=3)
    
    # Step 4: LLM 综合 KG 事实 + 代码上下文，生成最终答案
    answer = LLM.generate(
        question=question,
        kg_facts=kg_facts,
        code_context=code_context
    )
    return answer
```

### 3. 知识图谱更新（KG Incremental Update）

基于 Git 事件触发增量更新：

```
git push → webhook → 
  parse_diff() → 
  identify_changed_entities() → 
  update_kg_nodes_and_edges()
```

---

## Example — 在软件知识库中的应用示例

**场景 1：依赖关系问答**

用户提问："`PaymentService` 被哪些模块使用？它依赖了哪些外部库？"

KG 查询：
```cypher
MATCH (m)-[:imports]->(c:Class {name: "PaymentService"})
RETURN m.name AS caller_module

MATCH (c:Class {name: "PaymentService"})-[:depends_on]->(d:Dependency)
RETURN d.name AS external_dep
```

返回：
```
调用方: OrderController, SubscriptionService, RefundProcessor
外部依赖: stripe-python, requests, pydantic
```

**场景 2：开发流程问答**

用户提问："谁最近修改过认证模块？相关的 Issue 有哪些？"

KG 查询跨越 `Commit → Developer`、`Commit → File`、`Issue → Fix → Commit` 三种关系，纯文本 RAG 无法实现这类多跳查询。

---

## Conclusion — 对软件知识库建设的启示

| 启示点 | 具体应用 |
|--------|---------|
| **KG 作为知识底座** | 将代码仓库的结构信息建模为知识图谱，作为知识库的核心存储层 |
| **混合查询路由** | 结构性问题走 KG 查询，语义性问题走向量检索，两者结合生成答案 |
| **软件本体设计** | 为项目定制实体类型和关系类型，比通用本体更贴合实际使用 |
| **SPARQL/Cypher 接口** | 支持精确的图查询语言，补充自然语言检索的不足 |
| **KG + 提交记录** | 将 Git 历史、Issue 跟踪也纳入 KG，支持"谁改了什么、为什么改"的溯源问答 |

---

## Reference

- 论文原文：[arXiv:2412.03815](https://arxiv.org/abs/2412.03815)
- 发表时间：arXiv 2024，2025年10月修订
- 关键词：Knowledge Graph, LLM + KG, Repository QA, Software Ontology, Multi-hop Reasoning
- 相关工作：RepoGraph（代码图结构）、CGM（图集成 LLM）
