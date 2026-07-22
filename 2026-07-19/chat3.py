import chainlit as cl
from base import ask
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


@cl.on_chat_start
async def start():
    cl.user_session.set(
        "history",
        [SystemMessage(content="你是资深 Python 专家")],
    )


@cl.on_message
async def main(message: cl.Message):
    history: list = cl.user_session.get("history")

    # 把这次追问追加进历史
    history.append(HumanMessage(content=message.content))

    # 把整段历史一起给 LLM，让它有上下文
    res = ask(history)

    # 把模型的回复也写回历史，下次追问时带上
    if res is not None:
        history.append(AIMessage(content=res))

    await cl.Message(content=res or "（本次调用失败，请查看终端日志）").send()
