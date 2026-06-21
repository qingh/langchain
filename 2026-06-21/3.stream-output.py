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

prompt = ChatPromptTemplate.from_template("用三句话解释什么是 RAG ?")

for chunk in llm.stream(prompt.invoke({"input": "用三句话解释什么是 RAG ?"})):
    print(chunk.content, end="", flush=True)

print()
