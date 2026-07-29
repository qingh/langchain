from base import chat
from langchain_core.prompts import ChatPromptTemplate

llm = chat()


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个专业的{domain}家，回答要准确且通俗易懂"),
        ("human", "{question}"),
    ]
)

# result = prompt.invoke({"domain": "机器学习", "question": "什么是梯度下降？"})
# final_result = llm.invoke(result)

chain = prompt | llm

final_result = chain.invoke({"domain": "机器学习", "question": "什么是梯度下降？"})

print(final_result.content)
