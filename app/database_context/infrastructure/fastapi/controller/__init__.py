from fastapi import APIRouter
from .get_films_from_prompt import router as get_films_from_prompt_router
from .get_data_from_prompt import router as get_data_from_prompt_router
from .post_convert_films_to_vector import router as post_convert_films_to_vector_router


def create_database_context_router() -> APIRouter:
    """
    Create the router for the database_context bounded context.
    """
    database_context_router = APIRouter(
        prefix="/database-context", tags=["Database Context"]
    )

    database_context_router.include_router(get_films_from_prompt_router)
    database_context_router.include_router(get_data_from_prompt_router)
    database_context_router.include_router(post_convert_films_to_vector_router)

    return database_context_router


database_context_router = create_database_context_router()
