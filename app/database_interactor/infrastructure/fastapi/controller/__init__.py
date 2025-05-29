from fastapi import APIRouter
from .get_data_from_database import router as get_data_from_database_router
from .get_films_from_prompt import router as get_films_from_prompt_router
from .get_films_from_prompt_mysql import router as get_films_from_prompt_mysql_router
from .post_convert_films_to_vector import router as post_convert_films_to_vector_router


def create_database_interactor_router() -> APIRouter:
    """
    Create the router for the database_interactor bounded context.
    """
    database_interactor_router = APIRouter(
        prefix="/database-interactor", tags=["Database Interactor"]
    )

    database_interactor_router.include_router(get_data_from_database_router)
    database_interactor_router.include_router(get_films_from_prompt_router)
    database_interactor_router.include_router(get_films_from_prompt_mysql_router)
    database_interactor_router.include_router(post_convert_films_to_vector_router)

    return database_interactor_router


database_interactor_router = create_database_interactor_router()
