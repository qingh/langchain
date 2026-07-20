from base import ask
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "你是一个{role}。请用{style}的风格回答问题。\n\n问题：{question}"
)


q1 = prompt.invoke(
    {"role": "Python助教", "style": "轻松活泼", "question": "什么是装饰器"}
)

q2 = prompt.invoke(
    {
        "role": "技术文档撰写专家",
        "style": "严谨专业",
        "question": "解释一下 Python 的 GIL 机制",
    }
)


data1 = ask(q1)
data2 = ask(q2)

print("data1", data1)
print("\n==========================================================================\n")
print("data2", data2)
