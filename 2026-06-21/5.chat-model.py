# import os
from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

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


messages = [
    SystemMessage(content="你是一个 Python 助教，回答要简洁明了"),
    HumanMessage(content="什么是装饰器?"),
]

response = llm.invoke(messages)

print(f"第一轮回复: {response.content}")

messages.append(AIMessage(content=response.content))
messages.append(HumanMessage(content="能给我举一个例子吗？"))

response2 = llm.invoke(messages)

print(f"\n第二轮回复：{response2.content}")
