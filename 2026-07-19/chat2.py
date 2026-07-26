import chainlit as cl
from langchain_core.messages import HumanMessage, SystemMessage


@cl.on_chat_start
async def start():
    print("\n\n\n@@@on chat start")
    cl.user_session.set("history", [SystemMessage(content="你是资深前端")])


@cl.on_message
async def main(message: cl.Message):
    history: list = cl.user_session.get("history")

    history.append(HumanMessage(content=message.content))

    print("\n\n\n###", history)

    await cl.Message(content="haha").send()
