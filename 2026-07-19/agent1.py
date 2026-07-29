from os import getenv

from base import chat
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

llm = chat()

tavily_api_key = getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("please set your TAVILY_API_KEY in .env file")

# 1. 实例化搜索工具
search_tool = TavilySearch(
    max_results=3, topic="general", tavily_api_key=tavily_api_key
)


@tool
def search_internet(query: str) -> str:
    """搜索互联网获取最新信息。用于回答天气、新闻、实时数据等时效性问题。"""
    return search_tool.invoke({"query": query})


@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except (SyntaxError, ValueError, TypeError, NameError, ArithmeticError) as e:
        return f"计算错误：{e}"


tools = [search_internet, calculator]


agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个有帮助的助手。使用可用的工具来回答问题。",
)


# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "成都今天的天气怎么样？"}]}
# )


# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "175 乘以 23 再加上 456 等于多少？"}]}
# )

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "如果北京今天的最高温是28度，上海是32度，两地的温差是多少？",
            }
        ]
    }
)

print(result["messages"][-1].content)
