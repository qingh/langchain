from base import chat
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


llm = chat()


prompt = ChatPromptTemplate.from_template(
    "你是一个{role}。\n\n请回答：{question}", partial_variables={"role": "数据分析师"}
)

question = prompt.invoke({"question": "解释一下 SQL 的 JOIN"})

result = llm.invoke(question)

print(result.content)
