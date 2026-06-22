from base import chat

response = chat().invoke("用一句话介绍你自己")
print("=" * 100)
print(response.content)
print("=" * 100)
