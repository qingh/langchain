from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

api_key = getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")


chat = ChatOpenAI(
    model="MiniMax-M3",
    openai_api_key=api_key,
    openai_api_base="https://api.minimaxi.com/v1",
    temperature=0,
    max_tokens=1024,
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个专业的{domain}家，回答要准确且通俗易懂"),
        ("human", "{question}"),
    ]
)

# result = prompt.invoke({"domain": "机器学习", "question": "什么是梯度下降？"})
# final_result = chat.invoke(result)

chain = prompt | chat

final_result = chain.invoke({"domain": "机器学习", "question": "什么是梯度下降？"})

print(final_result.content)
