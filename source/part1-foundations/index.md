---
title: "第一部分 —— 基础"
status: draft
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: complete
keywords:
  - foundations
---

# 第一部分 —— 基础

```{toctree}
:maxdepth: 1

ch01-why-kb-for-software
ch02-ir-rag-primer
ch03-diataxis-and-software-docs
```

## 为什么

软件团队积累的碎片化知识 —— 代码、工单、聊天、设计文档、runbook —— 堆积的速度远远快过人工能整理的速度。传统意义上的“写文档”根本跟不上。第一部分要把三件事讲清楚：*什么是软件知识库*、*为什么 AI 改变了构建知识库的经济账*，以及 *本书后文要站在哪些 IR / RAG / 文档研究的肩膀上*。

## 是什么

一份可用的“软件知识库”定义、一份关于信息检索（IR）与检索增强生成（RAG）基础组件的入门介绍，以及本书在分类文本内容时会反复使用的 Diátaxis {cite}`procida_diataxis` 文档类型模型。

## 怎么做

本书方法论的一个速写：三条锚定来源（文本层参考实现、代码层参考实现、作者那篇方法论博客 {cite}`fanyamin2026deepwiki`），理论与实践的配比，以及每一部分如何套用同一条 “Why → What → How → Example → Conclusion → Reference” 的骨架。

## 示例

用一页纸演示一下：当整套技术栈都就位时，“向知识库提问”大致是什么体感 —— 具体实现细节留给后面的章节展开。

## 小结

第一部分给出术语表和阅读顺序，这里还没开始“造东西” —— 动手造是从第二部分开始的。

## 参考文献

```{bibliography}
:filter: keywords % "foundations"
```
