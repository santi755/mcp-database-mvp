from app.ai_context.domain.llm_client import LLMClient
from app.shared.infrastructure.settings import get_settings

from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI

settings = get_settings()


class OpenAILLMClient(LLMClient):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = ChatOpenAI(
            model=model,
            openai_api_key=settings.openai_api_key,
        )

    def get_client(self) -> ChatOpenAI | GoogleGenerativeAI:
        return self.client
