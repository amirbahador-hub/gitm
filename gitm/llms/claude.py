from langchain_community.chat_models import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from pydantic import SecretStr


def get_claude_llm(
    model_name: str, api_key: SecretStr, temperature: float
) -> BaseChatModel:
    return ChatAnthropic(
        model_name=model_name,
        temperature=temperature,
        anthropic_api_key=api_key,
    )


get_llm = get_claude_llm
