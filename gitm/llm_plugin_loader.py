from importlib import import_module

from langchain_core.language_models import BaseChatModel
from gitm.settings import get_settings


def get_llm() -> BaseChatModel:
    settings = get_settings()
    module = import_module(f"gitm.llms.{settings.LLM_PROVIDER}")
    return module.get_llm(
        model_name=settings.LLM_MODEL,
        api_key=settings.LLM_API_KEY,
        temperature=settings.LLM_TEMPERATURE,
    )
