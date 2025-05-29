from fastapi import APIRouter
from .get_films_from_prompt import router as get_films_from_prompt_router
from .post_convert_films_to_vector import router as post_convert_films_to_vector_router


def create_embedding_context_router() -> APIRouter:
    """
    Create the router for the embedding_context bounded context.
    """
    embedding_context_router = APIRouter(
        prefix="/embedding-context", tags=["Embedding Context"]
    )

    embedding_context_router.include_router(get_films_from_prompt_router)
    embedding_context_router.include_router(post_convert_films_to_vector_router)

    return embedding_context_router


embedding_context_router = create_embedding_context_router()
