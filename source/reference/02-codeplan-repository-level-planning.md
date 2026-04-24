---
title: "CodePlan: Repository-Level Coding using LLMs and Planning"
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - reference
  - planning
  - multi-step-editing
---

# CodePlan: Repository-Level Coding using LLMs and Planning

> **论文信息**：FSE 2024 / Microsoft Research | [论文主页](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning-2/)

---

## What — 这篇论文解决什么问题

CodePlan 研究的问题是：**当一个编程任务涉及跨文件、多步骤修改时，如何让 LLM 可靠地完成整个仓库级的代码变更**？

传统 LLM 代码生成假设任务是单文件、单步骤的。但真实开发场景中，大量任务需要：

- 修改 A 文件后，B/C 文件也需同步更新；
- 修改某个接口定义，所有调用方都要适配；
- 完成一个需求涉及数据库 Schema、API 层、业务逻辑层的联动修改。

CodePlan 将这类任务建模为"**规划（Planning）+ 多步编辑（Multi-step Editing）**"问题，而不是单次生成问题。

---

## Why — 为什么这个方向对软件知识库重要

软件知识库不只是做"问答"，更高价值的场景是**辅助跨文件代码变更**：

- **依赖传播分析**：修改一个公共接口，知识库应能预测哪些下游文件受影响；
- **变更计划生成**：用户描述需求后，知识库应能生成结构化的"修改计划"，而不是直接输出代码；
- **多步骤任务追踪**：大型任务需要分解成有序的子任务，知识库需要维护任务状态。

CodePlan 的规划框架直接对应知识库的"**智能变更助手**"场景。

---

## How — 核心方法

CodePlan 的方法论分为三个阶段：

### 1. 变更影响分析（Change Impact Analysis）

基于代码的静态依赖图（调用关系、类继承、模块导入），分析初始修改会波及哪些文件：

```
seed_edit(file_A) → impact_graph
impact_graph → [file_B, file_C, file_D, ...]
```

工具包括：
- 构建 **AST（抽象语法树）** 提取符号引用；
- 构建 **调用图（Call Graph）** 追踪函数依赖；
- 按拓扑顺序排列待修改文件。

### 2. 规划生成（Plan Generation）

将修改任务拆解成有序的子任务列表，每个子任务包含：

```yaml
- file: src/api/user_controller.py
  change_type: update_signature
  depends_on: [src/models/user.py]
  instruction: "Update get_user() to accept new `role` parameter"
```

### 3. 迭代执行（Iterative Execution）

按计划顺序逐文件调用 LLM 进行修改，每步执行后：
- 验证语法正确性（AST parse）；
- 更新影响图（新的修改可能触发新的依赖传播）；
- 将已完成的变更作为后续步骤的上下文。

```
for task in plan:
    context = build_context(task, completed_changes)
    new_code = LLM.edit(context, task.instruction)
    validate(new_code)
    update_graph(new_code)
```

---

## Example — 在软件知识库中的应用示例

**场景**：开发者在知识库中提交需求："将用户模型中的 `username` 字段重命名为 `user_handle`，并更新所有相关代码"。

**CodePlan 生成的执行计划**：

```
Plan:
  1. [models/user.py]      修改字段定义: username → user_handle
  2. [db/migrations/]      生成数据库迁移脚本
  3. [api/user_api.py]     更新序列化器字段名
  4. [services/auth.py]    更新认证逻辑中的引用
  5. [tests/test_user.py]  更新测试断言
```

每步执行时，前序步骤的变更结果会作为当前步骤的上下文输入，确保语义一致性。

---

## Conclusion — 对软件知识库建设的启示

| 启示点 | 具体应用 |
|--------|---------|
| **变更规划能力** | 知识库应具备"生成跨文件修改计划"的能力，而不只是问答 |
| **依赖图构建** | 将代码仓库的依赖关系建模为图结构，作为知识库的核心索引 |
| **任务状态维护** | 多步骤任务需要持久化中间状态，知识库需要支持会话级上下文 |
| **影响分析接口** | 提供"给定一个修改，影响哪些文件"的 API，支持变更审查 |
| **验证环节** | 每步生成后需要语法验证，知识库应集成轻量的代码校验工具 |

---

## Reference

- 论文主页：[Microsoft Research](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning-2/)
- 会议：FSE 2024
- 关键词：Repository-Level Coding, LLM Planning, Multi-step Code Editing, Change Impact Analysis
- 相关工作：RepoGraph（结构导航）、RepoAgent（文档生成）
