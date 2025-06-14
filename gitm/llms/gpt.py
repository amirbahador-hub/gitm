import os

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def get_gpt_llm(
    model_name: str, api_key: SecretStr, temperature: float
) -> BaseChatModel:
    os.environ["OPENAI_API_KEY"] = api_key.get_secret_value()
    return ChatOpenAI(model=model_name, temperature=temperature)


get_llm = get_gpt_llm
