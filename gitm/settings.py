from enum import StrEnum
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLM(StrEnum):
    CLAUDE = "claude"
    GEMINI = "gemini"
    GPT = "gpt"


default_model_map = {
    LLM.CLAUDE: "claude-3-opus-20240229",
    LLM.GEMINI: "gemini-pro",
    LLM.GPT: "gpt-4",
}


class LLMConfiguration(BaseSettings):
    LLM_PROVIDER: LLM = LLM.GPT
    LLM_MODEL: str = default_model_map[LLM.GPT]
    LLM_API_KEY: SecretStr = SecretStr("notset")
    LLM_TEMPERATURE: float = 0.5


class Settings(
    LLMConfiguration,
):
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
