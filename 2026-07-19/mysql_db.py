"""可复用的 MySQL 封装。

通过 .env 配置连接信息，提供单例连接 + 常用 CRUD 便捷方法。

环境变量（写入项目根目录的 .env):
    MYSQL_HOST        默认 localhost
    MYSQL_PORT        默认 3306
    MYSQL_USER        默认 root
    MYSQL_PASSWORD    必填
    MYSQL_DATABASE    默认 mydb
    MYSQL_CHARSET     默认 utf8mb4

用法：

    from mysql_db import fetch_all, fetch_one, execute, transaction

    rows = fetch_all("SELECT * FROM user_table WHERE age > %s", (18,))
    one  = fetch_one("SELECT name FROM user_table WHERE id = %s", (1,))
    n    = execute("INSERT INTO user_table (name, age) VALUES (%s, %s)", ("Tim", 30))

    with transaction() as cur:
        cur.execute("UPDATE user_table SET age = age + 1 WHERE id = %s", (1,))
        cur.execute("INSERT INTO log_table (msg) VALUES (%s)", ("done",))
"""

from collections.abc import Generator, Sequence
from contextlib import contextmanager, suppress
from os import getenv
from threading import Lock
from typing import Any

import pymysql
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PORT = 3306
DEFAULT_CHARSET = "utf8mb4"


class MySQLConfigError(RuntimeError):
    """连接配置缺失或非法时抛出。"""


def _env(name: str, default: str) -> str:
    """读取环境变量：未设置走默认值；空串也走默认值，避免下游 int() 崩溃。"""
    val = getenv(name)
    return val if val else default


def _config() -> dict[str, Any]:
    """从环境变量读取连接配置，缺关键字段直接报错。"""
    password = getenv("MYSQL_PASSWORD")
    if not password:
        raise MySQLConfigError("please set MYSQL_PASSWORD in .env file")

    try:
        port = int(_env("MYSQL_PORT", str(DEFAULT_PORT)))
    except ValueError as e:
        raise MySQLConfigError(f"MYSQL_PORT 必须是整数：{e}") from e

    return {
        "host": _env("MYSQL_HOST", "localhost"),
        "port": port,
        "user": _env("MYSQL_USER", "root"),
        "password": password,
        "database": _env("MYSQL_DATABASE", "mydb"),
        "charset": _env("MYSQL_CHARSET", DEFAULT_CHARSET),
    }


# ---------- 单例连接（线程安全） ----------

_CONN: pymysql.connections.Connection | None = None
_LOCK = Lock()


def _get_connection() -> pymysql.connections.Connection:
    """获取（或复用）一个数据库连接；断开时自动重建。"""
    global _CONN
    with _LOCK:
        if _CONN is None:
            _CONN = pymysql.connect(**_config())
            return _CONN
        try:
            _CONN.ping(reconnect=True)
            return _CONN
        except pymysql.MySQLError:
            _close_connection_unlocked()
            _CONN = pymysql.connect(**_config())
            return _CONN


def _close_connection_unlocked() -> None:
    """关闭并清空当前连接（调用方需持有 _LOCK）。"""
    global _CONN
    if _CONN is not None:
        # 关闭已死连接时不关心为什么关不上，静默吞掉
        with suppress(pymysql.MySQLError, OSError):
            _CONN.close()
        _CONN = None


# ---------- 公共 API ----------


@contextmanager
def transaction() -> Generator[pymysql.cursors.DictCursor, None, None]:
    """事务上下文管理器。

    正常退出自动 commit，异常自动 rollback。
    返回 DictCursor，可直接按列名取值，例如 row["name"]。
    """
    conn = _get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    committed = False
    try:
        yield cursor
        conn.commit()
        committed = True
    finally:
        if not committed:
            # rollback 失败不要掩盖原始异常
            with suppress(pymysql.MySQLError):
                conn.rollback()
        cursor.close()


def fetch_all(
    sql: str, params: Sequence[Any] | None = None
) -> tuple[dict[str, Any], ...]:
    """查询多条记录，无结果返回空元组。"""
    with transaction() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def fetch_one(sql: str, params: Sequence[Any] | None = None) -> dict[str, Any] | None:
    """查询单条记录，没有则返回 None。"""
    with transaction() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def execute(sql: str, params: Sequence[Any] | None = None) -> int:
    """执行 INSERT / UPDATE / DELETE，返回受影响行数。"""
    with transaction() as cur:
        return cur.execute(sql, params)


def executemany(sql: str, seq_of_params: Sequence[Sequence[Any]]) -> int:
    """批量执行同一 SQL，返回总受影响行数。"""
    with transaction() as cur:
        # pymysql 的 executemany 偶尔返回 None，用 `or 0` 收敛成 int
        return cur.executemany(sql, seq_of_params) or 0


def close() -> None:
    """关闭并清空当前连接（脚本退出前可选调用，幂等）。"""
    with _LOCK:
        _close_connection_unlocked()
