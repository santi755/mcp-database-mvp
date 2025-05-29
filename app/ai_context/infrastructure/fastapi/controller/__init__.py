from fastapi import APIRouter
from .post_llm_client_chat import router as llm_client_chat_router


def create_ai_context_router() -> APIRouter:
    """
    Create the router for the ai_context bounded context.
    """
    ai_context_router = APIRouter(prefix="/ai-context", tags=["AI Context"])

    ai_context_router.include_router(llm_client_chat_router)
    # TODO: Add more routers here

    return ai_context_router


ai_context_router = create_ai_context_router()
