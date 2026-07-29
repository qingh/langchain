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

r1 = add.invoke({"a": 12, "b": 41})
r2 = multiply.invoke({"a": 12, "b": 41})
print(r1)
print(r2)
