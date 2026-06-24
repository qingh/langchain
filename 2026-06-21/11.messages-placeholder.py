from base import chat
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import HumanMessage, AIMessage

llm = chat()


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个简洁的python助教"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

chain = prompt | llm

chat_history = []

while True:
    user_input = input("\n你: ")
    if user_input.lower() in ["退出", "exit", "quit"]:
        break
    response = chain.invoke({"chat_history": chat_history, "question": user_input})

    print(f"\n助手: {response.content}")

    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response.content))
