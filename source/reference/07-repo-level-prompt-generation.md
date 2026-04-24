---
title: "Repository-Level Prompt Generation for Large Language Models of Code"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - reference
  - prompt-generation
  - context-assembly
---

# Repository-Level Prompt Generation for Large Language Models of Code

> **论文信息**：ICML 2023 | [PMLR 论文主页](https://proceedings.mlr.press/v202/shrivastava23a.html)

---

## What — 这篇论文解决什么问题

本文（又称 **RLPG**，Repository-Level Prompt Generation）研究的问题是：**即使不修改 LLM 的参数，只通过更好地"从整个仓库中组织上下文"，能否显著提升代码补全效果**？

这个问题的出发点是一个重要观察：**代码生成质量很大程度上取决于 prompt 的质量**，而代码仓库中存在大量可以利用的上下文信息，但传统工具只提供了当前文件的局部上下文。

本文的核心主张：**不改模型，改 prompt 构建策略**，从整个仓库中智能选择最相关的上下文片段，填充到 LLM 的上下文窗口中。

---

## Why — 为什么这个方向对软件知识库重要

RLPG 是后续所有 repo-level RAG 系统（RepoCoder、Repoformer、RepoGraph 等）的**概念起点**，它奠定了一个基础共识：

- **仓库上下文的价值**：代码仓库本身就是一个高质量的结构化知识库，关键是如何索引和检索；
- **Prompt 工程的边界**：展示了在不微调模型的前提下，通过 prompt 设计能达到的效果上限；
- **无侵入部署**：只需改变上下文构建方式，无需修改模型，适合在现有知识库系统上直接叠加；
- **普适性**：方法对任意代码 LLM 有效，不依赖特定模型架构。

RLPG 告诉我们：**软件知识库的第一步，是把现有代码仓库变成一个可检索的高质量上下文库**。

---

## How — 核心方法

### 1. 仓库级上下文候选（Repo-level Context Candidates）

RLPG 定义了多类可以从仓库中提取的上下文类型：

```
候选上下文类型:
  1. In-file context      当前文件的其他函数/类
  2. Import context       当前文件 import 的模块内容
  3. Similar code         仓库中与当前代码相似的片段
  4. Usage examples       当前函数在仓库其他地方的使用示例
  5. Type definitions     涉及的类型/接口定义
  6. Docstring templates  同类函数的 docstring 模板
```

### 2. 上下文选择策略（Context Selection）

给定有限的 context window（通常 2048-4096 tokens），如何从候选集中选择最有价值的片段：

```python
def build_repo_prompt(current_file, cursor_position, repo):
    candidates = []
    
    # 按优先级收集候选上下文
    candidates += get_import_context(current_file, repo)
    candidates += get_similar_snippets(current_file, cursor_position, repo)
    candidates += get_usage_examples(current_function, repo)
    
    # 按相关性评分排序
    ranked = rank_by_relevance(candidates, current_context)
    
    # 填充到 token budget 限额内
    selected = fill_context_window(ranked, budget=2048)
    
    return format_prompt(current_file, selected)
```

### 3. 相关性评估（Relevance Scoring）

综合多个信号评估候选片段的相关性：

- **词汇重叠（Token Overlap）**：BM25 类指标；
- **导入图距离（Import Graph Distance）**：模块间的导入距离越近，相关性越高；
- **标识符相似度（Identifier Similarity）**：变量名、函数名的相似程度；
- **行数接近度（Line Proximity）**：同文件中位置越近的代码通常越相关。

---

## Example — 在软件知识库中的应用示例

**场景**：开发者在 `user_service.py` 中写一个新函数 `update_user_email()`。

**传统 IDE 提供的上下文**（仅当前文件）：
```python
# 只有 user_service.py 的前几百行
class UserService:
    def get_user(self, user_id): ...
    def create_user(self, data): ...
    # cursor 在这里
```

**RLPG 从仓库中额外提取的上下文**：

```python
# 来自 email_validator.py（被 import）
def validate_email(email: str) -> bool: ...

# 来自 user_repository.py（数据库操作示例）
def update_user_field(user_id: str, field: str, value: Any) -> bool: ...

# 来自 notification_service.py（类似操作的用法示例）
def update_user_phone(self, user_id: str, phone: str):
    # 展示了项目中更新用户信息的标准模式
    user = self.repo.get(user_id)
    self.validator.validate_phone(phone)
    self.repo.update(user_id, "phone", phone)
    self.notifier.send_confirmation(user.email)
```

有了这些上下文，LLM 生成的 `update_user_email()` 会自然遵循项目约定（先 validate，用 repo.update，再发通知）。

---

## Conclusion — 对软件知识库建设的启示

| 启示点 | 具体应用 |
|--------|---------|
| **上下文多样性** | 知识库不只索引代码本身，还应索引使用示例、类型定义、导入关系 |
| **Token 预算管理** | 在有限的上下文窗口内，优先填充最高价值的知识片段 |
| **多信号排序** | 相关性评分应融合词汇、结构、语义多个维度，而不只是向量相似度 |
| **无侵入增强** | 知识库可以作为现有 LLM 工具的"上下文增强层"，无需修改底层模型 |
| **仓库作为知识源** | 代码仓库本身就是最好的知识库原材料，关键是构建高效的检索索引 |

---

## Reference

- 论文原文：[PMLR v202/shrivastava23a](https://proceedings.mlr.press/v202/shrivastava23a.html)
- 会议：ICML 2023
- 关键词：Repository-Level Prompt Generation, Context Selection, Code Completion, Prompt Engineering
- 相关工作：RepoCoder（迭代检索，直接后续工作）、Repoformer（选择性检索）、RepoBench（评测）
