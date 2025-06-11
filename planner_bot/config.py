from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    bot_token: str = Field(..., alias="BOT_TOKEN")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_api_url: str = Field("https://api.openai.com/v1/chat/completions", alias="OPENAI_API_URL")
    openai_model: str = Field("gpt-3.5-turbo", alias="OPENAI_MODEL")
    database_dsn: str = Field(..., alias="DATABASE_DSN")
    scheduler_interval: int = Field(60, alias="SCHEDULER_INTERVAL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
