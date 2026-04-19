"""Chinese translations for book/part1-foundations/index.md (Part I cover).

Style: punchy, concrete, matching ch02's voice. Technical terms kept in
English (IR, RAG, KB, Diátaxis). Part names stay bilingual: "Part I" is
rendered as "第一部分" to align with how other Part indexes will read.

See book/_tools/translations/ch02-ir-rag-primer.zh.py for the full
style guide — particularly the rule about inserting a single ASCII
space around `*emphasis*` markers that sit between CJK characters, or
CommonMark will render the asterisks as literals.
"""

PO_PATH = "part1-foundations/index.po"

TRANSLATIONS: dict[str, str] = {
    "Part I — Foundations": "第一部分 —— 基础",
    "Why": "为什么",
    (
        "Software teams accumulate fragmented knowledge — code, tickets, "
        "chats, design docs, runbooks — faster than humans can curate "
        "it. Traditional documentation cannot keep up. Part I "
        "establishes *what a software knowledge base is*, *why AI "
        "changes the economics of building one*, and *what prior IR / "
        "RAG / documentation research we will be standing on* "
        "throughout the rest of the book."
    ): (
        "软件团队积累的碎片化知识 —— 代码、工单、聊天、设计文档、runbook —— "
        "堆积的速度远远快过人工能整理的速度。"
        "传统意义上的“写文档”根本跟不上。"
        "第一部分要把三件事讲清楚："
        "*什么是软件知识库*、"
        "*为什么 AI 改变了构建知识库的经济账*，"
        "以及 *本书后文要站在哪些 IR / RAG / 文档研究的肩膀上*。"
    ),
    "What": "是什么",
    (
        "A working definition of \"software knowledge base\", a primer "
        "on the relevant information-retrieval and "
        "retrieval-augmented-generation building blocks, and the "
        "Diátaxis {cite}`procida_diataxis` doc-type model we will "
        "reuse when classifying prose content."
    ): (
        "一份可用的“软件知识库”定义、"
        "一份关于信息检索（IR）与检索增强生成（RAG）基础组件的入门介绍，"
        "以及本书在分类文本内容时会反复使用的 Diátaxis "
        "{cite}`procida_diataxis` 文档类型模型。"
    ),
    "How": "怎么做",
    (
        "A short methodological overview of the book: three anchor "
        "sources (the prose-layer reference implementation, the "
        "code-layer reference implementation, and the author's "
        "methodology blog post {cite}`fanyamin2026deepwiki`), the "
        "theory→practice ratio, and how each Part applies the same Why "
        "→ What → How → Example → Conclusion → Reference arc."
    ): (
        "本书方法论的一个速写："
        "三条锚定来源（文本层参考实现、代码层参考实现、"
        "作者那篇方法论博客 {cite}`fanyamin2026deepwiki`），"
        "理论与实践的配比，"
        "以及每一部分如何套用同一条 "
        "“Why → What → How → Example → Conclusion → Reference” 的骨架。"
    ),
    "Example": "示例",
    (
        "A one-page walkthrough illustrating what \"ask the KB\" feels "
        "like once the full stack is in place, deferring "
        "implementation details to later Parts."
    ): (
        "用一页纸演示一下：当整套技术栈都就位时，"
        "“向知识库提问”大致是什么体感 —— "
        "具体实现细节留给后面的章节展开。"
    ),
    "Conclusion": "小结",
    (
        "Part I gives the vocabulary and the reading order. It does "
        "not build anything yet — that starts in Part II."
    ): (
        "第一部分给出术语表和阅读顺序，"
        "这里还没开始“造东西” —— 动手造是从第二部分开始的。"
    ),
    "References": "参考文献",
}
