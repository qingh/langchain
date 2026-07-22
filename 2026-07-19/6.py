from base import ask
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

res = ask("当前是什么日期？")

print(res)
