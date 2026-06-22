from base import chat
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


llm = chat()


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
