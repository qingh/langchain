from os import getenv

from base import chat
from langchain.agents import create_agent
from langchain_tavily import TavilySearch

llm = chat()

tavily_api_key = getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("please set your TAVILY_API_KEY in .env file")

# 1. 实例化搜索工具
search_tool = TavilySearch(max_results=3, topic="news", tavily_api_key=tavily_api_key)

# 2. 构建 Agent（langchain v1：create_agent 直接返回 CompiledStateGraph）
agent = create_agent(
    model=llm,
    tools=[search_tool],
    system_prompt="你是一个善于使用搜索工具回答最新资讯的 AI 助手。",
)

# 3. 调用 —— 输入输出统一走 messages 列表
result = agent.invoke({"messages": [{"role": "user", "content": "我想了解openai近况"}]})
print(result["messages"][-1].content)
