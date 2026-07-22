from base import chat
from langchain_core.messages import SystemMessage, HumanMessage

llm = chat()


for chunk in llm.stream(
    [
        SystemMessage(content="你是一个 Python 助教，回答要简洁明了"),
        HumanMessage(content="什么是装饰器？"),
    ]
):
    print(chunk.content, end="", flush=True)
