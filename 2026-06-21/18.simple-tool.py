from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """计算两个整数的和"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积"""
    return a * b


tools = [add, multiply]

result = add.invoke({"a": 5, "b": 3})

print(result)
