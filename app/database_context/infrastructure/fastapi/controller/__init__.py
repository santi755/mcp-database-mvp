from fastapi import APIRouter
from .get_data_from_prompt import router as get_data_from_prompt_router


def create_database_context_router() -> APIRouter:
    """
    Create the router for the database_context bounded context.
    """
    database_context_router = APIRouter(
        prefix="/database-context", tags=["Database Context"]
    )

    database_context_router.include_router(get_data_from_prompt_router)

    return database_context_router


database_context_router = create_database_context_router()
