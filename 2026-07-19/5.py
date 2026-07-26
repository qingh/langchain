from base import chat
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

llm = chat()

message = [
    SystemMessage(content="你是一个 Python 助教，回答要简洁明了"),
    HumanMessage(content="什么是装饰器？"),
]

response1 = llm.invoke(message)

print(f"第一轮回复：{response1.content}")

message.append(AIMessage(content=response1.content))
message.append(HumanMessage(content="能给我一个具体例子吗？"))

response2 = llm.invoke(message)

print(f"第二轮回复：{response2.content}")
