from base import chat

llm = chat()

response = llm.invoke("python是一门")

print("start")
print(response.content)
print("=" * 100)
print(repr(response.content))
print("=" * 100)
