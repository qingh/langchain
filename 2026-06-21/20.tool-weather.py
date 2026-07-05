from os import getenv

from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from base import chat


llm = chat()

""" tavily_api_key = getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("please set your TAVILY_API_KEY in .env file")

# 1. 实例化搜索工具
search_tool = TavilySearch(max_results=3, topic="news", tavily_api_key=tavily_api_key) """


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}"


# 2. 构建 Agent（langchain v1：create_agent 直接返回 CompiledStateGraph）
agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="you are a helpful assistant",
)

# 3. 调用 —— 输入输出统一走 messages 列表
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what's the weather in San francisco?"}]}
)
print(result["messages"][-1].content)
