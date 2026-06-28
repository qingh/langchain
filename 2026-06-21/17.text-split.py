from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
第一章 Python 简介

Python 是一门高级编程语言，由 Guido van Rossum 于 1991 年首次发布。
它的设计哲学强调代码的可读性和简洁性。"优雅胜于丑陋"、"显式胜于隐式"
是 Python 社区的核心价值观。

Python 广泛应用于 Web 开发、数据分析、人工智能、自动化运维等领域。
它的语法简洁优雅，学习曲线平缓，非常适合初学者入门编程。

第二章 核心数据类型

Python 中最基本的数据类型包括整数(int)、浮点数(float)、字符串(str)和布尔(bool)。
每种类型都有丰富的内置方法可供调用。

如果你的知识库主要是 Markdown 文档（如技术文档、Wiki 页面），按标题层级分割比纯字符分割更合理——它能让每个块对应一个完整的章节：
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", "。", " ", ""]
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"\n=== Chunk {i}(长度：{len(chunk)})")
    print(chunk)
