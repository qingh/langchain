from base import chat
from langchain_core.prompts import ChatPromptTemplate

llm = chat()

prompt = ChatPromptTemplate.from_template(
    "你是一个{role}。请用{style}的风格回答问题。\n\n问题：{question}"
)

question = prompt.invoke(
    {"role": "Python助教", "style": "轻松活泼", "question": "什么是装饰器"}
)

for chunk in llm.stream(question):
    print(chunk.content, end="", flush=True)

print()
