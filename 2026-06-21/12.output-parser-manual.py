from base import chat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = chat()
parser = StrOutputParser()


prompt = ChatPromptTemplate.from_template("用一句话解释{topic}")

response = prompt.invoke({"topic": "RAG"})

result = llm.invoke(response)

text = parser.parse(result)

print("result", result.content)
print("text", text)
