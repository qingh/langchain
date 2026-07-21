import chainlit as cl


@cl.on_message
async def main(message: cl.Message):
    # 直接 echo
    await cl.Message(content=f"你说了: {message.content}").send()
