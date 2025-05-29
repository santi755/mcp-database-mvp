from dishka import Provider, provide, Scope
from app.ai_context.infrastructure.llm_client.openai_llm_client import OpenAILLMClient
from app.ai_context.infrastructure.llm_client.google_llm_client import GoogleLLMClient
from app.ai_context.domain.llm_client import LLMClient


class AIContextProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_llm_client(self) -> LLMClient:
        return GoogleLLMClient()


provider_ai_context = AIContextProvider()
