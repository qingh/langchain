from base import chat
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = chat()


def stream_reply(messages, label: str) -> str:
    """流式打印模型回复，并把累积后的完整内容返回。"""
    print(f"{label}：", end="", flush=True)
    chunks: list[str] = []
    for chunk in llm.stream(messages):
        piece = chunk.content
        if isinstance(piece, list):
            piece = "".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in piece
            )
        if piece:
            chunks.append(piece)
            print(piece, end="", flush=True)
    print()
    return "".join(chunks)


message = [
    SystemMessage(content="你是一个 Python 助教，回答要简洁明了"),
    HumanMessage(content="什么是装饰器？"),
]

reply1 = stream_reply(message, "第一轮回复")
message.append(AIMessage(content=reply1))
message.append(HumanMessage(content="能给我一个具体例子吗？"))

reply2 = stream_reply(message, "第二轮回复")
