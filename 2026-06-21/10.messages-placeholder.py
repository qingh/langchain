from base import chat
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = chat()


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个有帮助的助手"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

result1 = prompt.invoke({"history": [], "question": "你好"})

print(
    "###1", [m.content for m in result1.to_messages()]
)  # ['你是一个有帮助的助手', '你好']

result2 = prompt.invoke(
    {
        "history": [("human", "你好"), ("ai", "你好！有什么可以帮你的？")],
        "question": "什么是LangChain?",
    }
)

print(
    "###2", [m.content for m in result2.to_messages()]
)  # ['你是一个有帮助的助手', '你好', '你好！有什么可以帮你的？', '什么是LangChain?']

final_result = llm.invoke(result2)
print(final_result.content)
