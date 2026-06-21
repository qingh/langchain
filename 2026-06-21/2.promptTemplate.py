# import os
from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

api_key = getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")


llm = ChatOpenAI(
    model="MiniMax-M3",
    openai_api_key=api_key,
    openai_api_base="https://api.minimaxi.com/v1",
    temperature=0,
    max_tokens=1024,
)

prompt_template = ChatPromptTemplate.from_template(
    "你是一个{role}。请用{style}的风格回答问题。\n\n问题: {question}"
)

result_casual = prompt_template.invoke(
    {"role": "Python助教", "style": "轻松活泼", "question": "什么是装饰器？"}
)

result_formal = prompt_template.invoke(
    {
        "role": "技术文档撰写专家",
        "style": "严谨专业",
        "question": "解释一下 Python 的 GIL 机制",
    }
)

print("=== 轻松版 ===")
print(result_casual.to_messages())
print("\n=== 严谨版 ===")
print(result_formal.to_messages())
