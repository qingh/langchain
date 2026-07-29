from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气"""
    # 模拟天气数据
    weather_data = {"北京": "晴，28°C", "上海": "多云，32°C", "广州": "雷阵雨，30°C"}

    return weather_data.get(city, f"{city}的天气数据暂不可用")


print(get_weather.name)
print(get_weather.description)
print(get_weather.args)
