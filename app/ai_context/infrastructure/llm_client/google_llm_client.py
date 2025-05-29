from app.ai_context.domain.llm_client import LLMClient
from app.shared.infrastructure.settings import get_settings

from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI

settings = get_settings()


class GoogleLLMClient(LLMClient):
    def __init__(self, model: str = "gemini-2.0-flash"):
        self.client = GoogleGenerativeAI(
            model=model,
            google_api_key=settings.google_api_key,
        )

    def get_client(self) -> ChatOpenAI | GoogleGenerativeAI:
        return self.client
