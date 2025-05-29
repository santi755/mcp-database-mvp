from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject
from pydantic import BaseModel
from app.ai_context.domain.llm_client import LLMClient
from app.ai_context.application.llm_client_chat_handler import llm_client_chat_handler

router = APIRouter()


class LLMRequest(BaseModel):
    prompt: str


class LLMResponse(BaseModel):
    response: str


@router.post("/llm-client-chat", response_model=LLMResponse)
@inject
async def post_llm_client_chat(
    request: LLMRequest, llm_client: FromDishka[LLMClient]
) -> LLMResponse:
    """
    Endpoint to chat with LLM
    """
    result = await llm_client_chat_handler(
        message=request.prompt, llm_client=llm_client
    )

    return LLMResponse(response=result.content)
