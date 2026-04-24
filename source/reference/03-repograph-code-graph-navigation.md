---
title: "RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - reference
  - code-graph
  - repo-level
---

# RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph

> **论文信息**：ICLR 2025 Poster | [OpenReview](https://openreview.net/forum?id=dw9VUsSHGB)

---

## What — 这篇论文解决什么问题

RepoGraph 研究的问题是：**如何为 LLM 提供一个"仓库级结构导航层"，使其能在大型代码仓库中准确定位、理解和推理代码结构**？

现有的代码 RAG 方案普遍基于文本语义相似度检索（Embedding + 向量数据库），存在三个根本性缺陷：

1. **语义相似 ≠ 结构相关**：语义相近的代码片段未必有依赖关系；
2. **丢失结构信息**：chunk 化的文本检索破坏了函数调用链、类继承等结构信息；
3. **无法导航**：LLM 无法知道"从这个函数出发，应该去看哪些相关定义"。

RepoGraph 的核心贡献是：不再只靠 chunk 检索，而是给 LLM 一个**可导航的仓库级代码图（Repository-level Code Graph）**。

---

## Why — 为什么这个方向对软件知识库重要

软件知识库的价值上限取决于它能多深度地理解代码结构。纯文本 RAG 只能做到"表面语义匹配"，而 RepoGraph 提供的图结构索引能支持：

- **符号级查询**：精确查询"哪个类实现了 IUserService 接口"；
- **依赖链追踪**：从一个模块出发，沿调用关系遍历相关代码；
- **结构感知问答**：回答"这个函数被哪些地方调用"、"这个类的继承层次是什么"；
- **精准上下文组装**：为 LLM 提供结构正确的上下文，而不是随机相似的文本片段。

RepoGraph 代表了软件知识库从"文本检索"升级到"**结构理解**"的架构跃迁。

---

## How — 核心方法

### 1. 代码图构建（Code Graph Construction）

RepoGraph 从仓库源码中提取多层图结构：

```
节点类型:
  - File（文件）
  - Class（类）
  - Function（函数/方法）
  - Variable（模块级变量）

边类型:
  - imports（文件间导入）
  - defines（文件→类/函数定义）
  - calls（函数调用关系）
  - inherits（类继承关系）
  - uses（变量引用关系）
```

构建工具：静态分析（AST 解析 + 符号解析），不需要运行时信息。

### 2. 图增强检索（Graph-Enhanced Retrieval）

查询时不仅做语义相似检索，还进行**图遍历扩展**：

```python
# 伪代码
seed_nodes = semantic_search(query)  # 传统向量检索
expanded_nodes = graph_traverse(
    seed_nodes,
    strategy="BFS",
    depth=2,
    edge_types=["calls", "imports"]
)
context = serialize(expanded_nodes)
```

这样得到的上下文既有语义相关性，又有结构完整性。

### 3. 结构感知提示（Structure-Aware Prompting）

将图结构信息以结构化文本形式注入 prompt：

```
# 上下文：UserService.get_user()
# 调用者：AuthController.login(), UserController.profile()
# 被调用：Database.query(), Cache.get()
# 所在文件：services/user_service.py
# 依赖：models/user.py, utils/cache.py
```

---

## Example — 在软件知识库中的应用示例

**场景**：开发者在知识库中提问"为什么 `AuthController.login()` 有时会抛出 `CacheError`"。

**传统 RAG 的局限**：只能检索到包含 "CacheError" 关键词的文件，可能错过真正的调用链。

**RepoGraph 的处理流程**：

```
1. 定位节点: AuthController.login()
2. 图遍历: login() → calls → UserService.get_user()
                              → calls → Cache.get()
                                        → raises → CacheError
3. 组装上下文: 完整的调用链代码
4. LLM 回答: "CacheError 来自 Cache.get()，被 UserService.get_user() 调用，
              而 get_user() 在 login() 中被调用。原因是..."
```

---

## Conclusion — 对软件知识库建设的启示

| 启示点 | 具体应用 |
|--------|---------|
| **图索引层** | 在向量索引之外，建立代码结构图索引作为知识库的第二层索引 |
| **混合检索** | 语义检索（dense retrieval）+ 图遍历（graph traversal）结合使用 |
| **符号级查询** | 支持"查找接口实现"、"查找函数调用者"等结构性查询 |
| **上下文质量** | 用图扩展的上下文比纯相似度检索的上下文更有结构完整性 |
| **增量更新** | 代码变更时，只需更新图中受影响的节点和边，而不是重新索引全库 |

---

## Reference

- 论文链接：[OpenReview ICLR 2025](https://openreview.net/forum?id=dw9VUsSHGB)
- 会议：ICLR 2025 Poster
- 关键词：Repository-level Code Graph, Graph-Enhanced Retrieval, Structure-Aware Context, Code Navigation
- 相关工作：CGM（图集成 LLM）、RepoCoder（迭代检索）、Repoformer（选择性检索）
