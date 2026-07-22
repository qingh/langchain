import chainlit as cl
from base import chat
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = chat()


@cl.on_chat_start
async def start():
    cl.user_session.set(
        "history",
        [SystemMessage(content="你是资深 Python 专家")],
    )


@cl.on_message
async def main(message: cl.Message):
    history: list = cl.user_session.get("history")
    history.append(HumanMessage(content=message.content))

    # 1. 先创建一个空的 Message，立即 send() 让前端占位
    msg = cl.Message(content="")
    await msg.send()

    async for chunk in llm.astream(history):
        await msg.stream_token(chunk.content)  # 逐 token 追加显示

    await msg.update()  # 流式结束后更新最终状态
