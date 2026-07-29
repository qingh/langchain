from os import getenv

from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

tavily_api_key = getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("please set your TAVILY_API_KEY in .env file")

# 1. 实例化搜索工具
search_tool = TavilySearch(max_results=3, topic="news", tavily_api_key=tavily_api_key)


print(search_tool.invoke("我想了解小米公司最近的股价"))
