from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    google_api_key: str
    openai_api_key: str

    db_driver: str
    db_user: str
    db_password: str
    db_port: int
    db_name: str
    db_host: str

    langchain_db_connection: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()
