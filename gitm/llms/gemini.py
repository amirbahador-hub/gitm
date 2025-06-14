from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr


def get_gemini_llm(
    model_name: str, api_key: SecretStr, temperature: float
) -> BaseChatModel:
    return ChatGoogleGenerativeAI(
        model=model_name, temperature=temperature, google_api_key=api_key
    )


get_llm = get_gemini_llm
