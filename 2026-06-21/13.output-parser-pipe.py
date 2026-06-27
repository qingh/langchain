from base import chat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = chat()
parser = StrOutputParser()


prompt = ChatPromptTemplate.from_template("用一句话解释{topic}")

chain = prompt | llm | parser

result = chain.invoke({"topic": "RAG"})

print("###", result)
