from base import chat
from langchain_core.prompts import ChatPromptTemplate

llm = chat()


prompt = ChatPromptTemplate.from_template(
    "你是一个{role}。请用{style}的风格回答问题。\n\n问题: {question}"
)


chain = prompt | llm


result1 = chain.invoke(
    {"role": "Python助教", "style": "轻松活泼", "question": "什么是装饰器？"}
)

result2 = chain.invoke(
    {
        "role": "技术文档撰写专家",
        "style": "严谨专业",
        "question": "解释一下 Python 的 GIL 机制",
    }
)

print("=== 轻松版 ===")
print(result1.content)
print("\n=== 严谨版 ===")
print(result2.content)
