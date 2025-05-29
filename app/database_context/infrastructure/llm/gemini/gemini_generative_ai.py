from langchain_google_genai import ChatGoogleGenerativeAI
from app.shared.infrastructure.settings import get_settings
from functools import lru_cache


@lru_cache()
def get_gemini_client():
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,
        google_api_key=settings.google_api_key,
    )
