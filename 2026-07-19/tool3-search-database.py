from langchain_core.tools import tool
from mysql_db import fetch_all


@tool
def search_database(
    table: str,
):
    """
    在数据库中搜索记录

    Args:
        table: 要查询的表名（users / orders / products）
    """
    rows = fetch_all(f"SELECT id,user FROM {table}")
    return rows


result = search_database.invoke({"table": "user_table"})
print(result)
