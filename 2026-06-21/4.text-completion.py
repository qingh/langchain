# import os
from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

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
response = llm.invoke("python是一门")

print("start")
print(response.content)
print("=" * 100)
print(repr(response.content))
print("=" * 100)
