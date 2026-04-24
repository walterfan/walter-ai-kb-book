---
title: "Code Graph Model (CGM): A Graph-Integrated Large Language Model for Repository-Level Software Engineering Tasks"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - reference
  - code-graph
  - graph-llm
---

# Code Graph Model (CGM): A Graph-Integrated Large Language Model for Repository-Level Software Engineering Tasks

> **论文信息**：NeurIPS 2025 Poster | [arXiv:2505.16901](https://arxiv.org/abs/2505.16901)

---

## What — 这篇论文解决什么问题

CGM 研究的问题是：**如何让开源 LLM 在不依赖 Agent 框架的情况下，通过直接集成仓库代码图结构，来解决仓库级软件工程任务**？

现有方案的痛点：

1. **商业模型依赖**：GPT-4、Claude 等闭源模型在 SWE-bench 上效果好，但有数据隐私和定制化问题；
2. **Agent 方案不可预测**：多步骤 Agent（Tool-calling、ReAct）引入了随机性，线上系统难以保证稳定输出；
3. **开源模型差距大**：直接用 Qwen、LLaMA 等开源模型处理 repo-level 任务，效果远不如商业模型；
4. **图信息未被充分利用**：代码仓库的结构依赖信息（调用图、导入图）在传统方法中以文本形式传递，而不是直接作为模型输入。

CGM 的突破：将代码图结构**直接集成到 LLM 的注意力机制**中，而不是转成文本再输入。

---

## Why — 为什么这个方向对软件知识库重要

CGM 代表了软件知识库技术的**前沿水位线**：

- **开源可部署**：基于 Qwen2.5-72B，可以私有化部署，解决数据隐私问题；
- **无 Agent 依赖**：不用多步骤 Agent，减少不确定性，适合生产环境的知识库系统；
- **图结构原生输入**：将代码依赖图作为模型输入，而不是上下文文本，这是架构层面的创新；
- **SWE-bench SOTA**：开源模型中最高的 43% 解决率，证明了方法的有效性；
- **Agentless Graph RAG**：无 Agent 的图 RAG 框架，兼顾检索精度和系统稳定性。

---

## How — 核心方法

### 1. 代码图构建（Repository Code Graph）

将代码仓库表示为异构图：

```
节点（Node）:
  - 每个函数/方法/类 = 一个节点
  - 节点属性: 函数签名、Docstring、代码体（作为 token 序列）

边（Edge）:
  - calls:    A 函数调用了 B 函数
  - imports:  文件 A 导入了文件 B
  - defines:  文件 A 定义了函数 B
  - inherits: 类 A 继承了类 B
```

### 2. 图集成注意力机制（Graph-Integrated Attention）

CGM 的核心创新：在 LLM 的 Transformer 注意力层中，直接注入图结构信息。

```
传统注意力:
  Attention(Q, K, V) = softmax(QK^T / √d) × V

CGM 的图增强注意力:
  Attention_graph(Q, K, V, G) = softmax((QK^T + Graph_bias(G)) / √d) × V

其中 Graph_bias(G) 是根据图结构生成的注意力偏置矩阵:
  - 如果节点 i 和节点 j 存在边 → bias(i,j) > 0（促进关注）
  - 如果节点 i 和节点 j 无关 → bias(i,j) ≈ 0
```

### 3. 节点属性映射（Node Attribute Mapping）

用专用适配器（Adapter）将图节点的代码属性映射到 LLM 的输入空间：

```python
# 图节点 → LLM 输入的映射
node_embedding = adapter(
    signature_tokens,    # 函数签名的 token 表示
    docstring_tokens,    # 文档字符串
    code_tokens          # 函数体代码
)
# adapter 是一个轻量级线性投影层，训练时只更新 adapter，冻结 LLM 主体
```

### 4. Agentless Graph RAG 框架

不依赖 Agent 的图 RAG 流程：

```
Step 1: Graph Localization
  给定 Issue 描述，在代码图中定位最相关的节点子集
  使用图神经网络（GNN）进行节点重要性打分

Step 2: Subgraph Extraction  
  以定位到的节点为种子，提取 K 跳子图
  子图包含了任务相关的完整上下文

Step 3: Graph-Conditioned Generation
  将子图输入 CGM，利用图集成注意力机制生成解决方案

Step 4: Patch Validation
  对生成的代码变更进行语法和测试验证（无 Agent，纯确定性验证）
```

---

## Example — 在软件知识库中的应用示例

**场景**：SWE-bench 任务 — 修复一个涉及多文件的 Python Bug

**Issue 描述**：
```
TypeError: 'NoneType' object is not subscriptable 
in pandas/core/indexing.py when using .loc with 
boolean indexer on MultiIndex DataFrame
```

**CGM 的处理流程**：

```
Step 1: 图定位
  定位节点: _LocIndexer.__getitem__() [相关度: 0.92]
  邻居节点: MultiIndex.get_loc() [相关度: 0.78]
             _maybe_convert_indices() [相关度: 0.71]

Step 2: 子图提取
  提取以上 3 个函数 + 它们的直接调用者/被调用者
  子图共 12 个节点，4000 tokens

Step 3: 图条件生成
  CGM 通过图集成注意力，同时"看到"所有相关函数及其关系
  生成的 patch 正确处理了 MultiIndex 时的 None 检查

Step 4: 验证
  运行相关测试用例，patch 通过 → 提交
```

**在知识库中的类比**：用 CGM 的思路，将代码知识图谱直接作为问答系统的结构化输入，而不是转化成文本后再检索。

---

## Conclusion — 对软件知识库建设的启示

| 启示点 | 具体应用 |
|--------|---------|
| **图结构原生集成** | 将代码依赖图直接融入模型推理，而不是转成文本再处理 |
| **开源替代方案** | CGM（Qwen2.5-72B）可作为知识库后端的私有化部署选项 |
| **Agentless 架构** | 减少 Agent 的不确定性，用确定性的图 RAG 流程替代多步骤 Agent |
| **适配器训练** | 冻结 LLM 主体，只训练轻量适配器，降低知识库系统的定制化成本 |
| **子图上下文** | 以任务相关子图为上下文单元，比 chunk 更精确，比全图更高效 |
| **性能基准** | CGM 在 SWE-bench Lite 上达到 43%，可作为知识库代码任务能力的参考基准 |

---

## Reference

- 论文原文：[arXiv:2505.16901](https://arxiv.org/abs/2505.16901)
- 会议：NeurIPS 2025 Poster
- 作者：Hongyuan Tao, Ying Zhang 等（共 15 位作者）
- 关键词：Code Graph Model, Graph-Integrated LLM, Repository-Level SE, SWE-bench, Agentless RAG
- 基础模型：Qwen2.5-72B（开源）
- 相关工作：RepoGraph（图导航）、RepoCoder（迭代检索）、LLM+KG 协同（论文 06）
