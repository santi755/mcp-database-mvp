from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    mongodb_url: str
    google_api_key: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()
