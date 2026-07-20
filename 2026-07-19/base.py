from functools import cache
from os import getenv

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompt_values import PromptValue

load_dotenv()

DEFAULT_TEMPERATURE = 0
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_MAX_RETRIES = 2


@cache
def chat() -> BaseChatModel:
    """Build a chat model client from environment variables.

    The instance is cached so repeated calls reuse the same client,
    avoiding redundant construction and enabling HTTP connection reuse.
    """
    api_key = getenv("API_KEY")
    if not api_key:
        raise ValueError("please set your API_KEY in .env file")

    return init_chat_model(
        model=getenv("MODEL"),
        model_provider="openai",
        api_key=api_key,
        base_url=getenv("BASE_URL"),
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
        timeout=DEFAULT_TIMEOUT,
        max_retries=DEFAULT_MAX_RETRIES,
    )


def ask(prompt: str | PromptValue | list[BaseMessage]) -> str | None:
    """调用 LLM 并把常见异常收敛成一行人话提示。

    成功时返回模型回复内容；失败时打印一行错误提示并返回 None。
    """
    try:
        return chat().invoke(prompt).content
    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "rate_limit" in msg or "用量上限" in msg:
            print("❌ 模型已达用量上限，请升级套餐或购买积分后再试。")
        elif "401" in msg or "api_key" in msg or "unauthorized" in msg:
            print("❌ API Key 无效或已过期，请检查 .env 中的 API_KEY。")
        elif "timeout" in msg or "timed out" in msg:
            print("❌ 请求超时，请稍后重试。")
        else:
            print(f"❌ 调用失败：{type(e).__name__}: {e}")
        return None
