from base import chat
from langchain_core.prompts import ChatPromptTemplate

llm = chat()

prompt = ChatPromptTemplate.from_template("用三句话解释什么是 RAG ?")

for chunk in llm.stream(prompt.invoke({"input": "用三句话解释什么是 RAG ?"})):
    print(chunk.content, end="", flush=True)

print()
