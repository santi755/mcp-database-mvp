from app.shared.infrastructure.settings import get_settings
from app.database_interactor.infrastructure.gemini.gemini_generative_ai import (
    get_gemini_client,
)

settings = get_settings()


def process_with_gemini(prompt: str) -> str:
    llm = get_gemini_client()
    response = llm.invoke(prompt)
    return response.content
