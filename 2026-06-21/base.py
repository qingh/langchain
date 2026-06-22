from functools import cache
from os import getenv

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

DEFAULT_TEMPERATURE = 0
DEFAULT_MAX_TOKENS = 1024


@cache
def chat() -> ChatOpenAI:
    """Build a ChatOpenAI client from environment variables.

    The instance is cached so repeated calls reuse the same client,
    avoiding redundant construction and enabling HTTP connection reuse.
    """
    openai_api_key = getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("please set your OPENAI_API_KEY in .env file")

    return ChatOpenAI(
        model=getenv("MODEL"),
        openai_api_key=openai_api_key,
        openai_api_base=getenv("OPENAI_API_BASE"),
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
    )
