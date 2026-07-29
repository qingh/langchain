from base import chat
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = chat()

prompt = ChatPromptTemplate.from_template("说一个{color}色的水果")

chain1 = prompt | llm

result1 = chain1.invoke({"color": "红"})
print("###-1", result1)
print("###-1-content", result1.content)
print("###-1-type", type(result1))  # <class 'langchain_core.messages.ai.AIMessage'>


#########################################################################################################


chain2 = prompt | llm | StrOutputParser()

result2 = chain2.invoke({"color": "红"})

print("###-2-content", result2)
print(
    "###-2-type",
    type(result2),  # <class 'langchain_core.messages.base.TextAccessor'>
)
