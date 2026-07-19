from functools import cache
from os import getenv

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

DEFAULT_TEMPERATURE = 0
DEFAULT_MAX_TOKENS = 1024


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
    )
