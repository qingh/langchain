# import chat from base
from base import chat

llm = chat()


response = llm.invoke("用一句话介绍你自己")

print(response.content)
