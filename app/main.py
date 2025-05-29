from typing import Union
from app.shared.infrastructure.settings import get_settings
from qdrant_client import QdrantClient, models
from dishka.integrations.fastapi import setup_dishka

from fastapi import FastAPI, HTTPException
from app.database_interactor.infrastructure.fastapi.controller.get_data_from_database import (
    router as gemini_router,
)
from app.database_interactor.infrastructure.fastapi.controller.post_convert_films_to_vector import (
    router as covert_films_to_vector_router,
)
from app.database_interactor.infrastructure.fastapi.controller.get_films_from_prompt import (
    router as get_films_from_prompt_router,
)
from app.database_interactor.infrastructure.fastapi.controller.get_films_from_promt_mysql import (
    router as get_films_from_promt_mysql_router,
)
from app.database_interactor.application.covert_films_to_vector_handler import (
    covert_films_to_vector_handler,
)
from app.database_interactor.application.retrieve_films_from_prompt_mysql import (
    retrieve_films_from_prompt_mysql,
)
from app.database_interactor.application.retrieve_films_from_natural_language import (
    retrieve_films_from_natural_language,
)
from pydantic import BaseModel
from app.shared.infrastructure.dependency_injection.container import setup_container
from app.ai_context.infrastructure.controller import ai_context_router

app = FastAPI()

container = setup_container(app)
setup_dishka(container, app)

app.include_router(gemini_router)
app.include_router(covert_films_to_vector_router)
app.include_router(get_films_from_prompt_router)
app.include_router(get_films_from_promt_mysql_router)
app.include_router(ai_context_router)


@app.on_event("startup")
async def startup_db_client():
    app.qdrant_client = QdrantClient(url="http://qdrant:6333")

    # Crear colecciones si no existen
    collections = app.qdrant_client.get_collections().collections
    collection_names = [c.name for c in collections]

    if "films" not in collection_names:
        app.qdrant_client.create_collection(
            collection_name="films",
            vectors_config=models.VectorParams(
                size=1536, distance=models.Distance.COSINE
            ),
        )


@app.get("/")
def read_root():
    settings = get_settings()
    return settings


@app.post("/convert-films-to-vector")
async def convert_films_to_vector():
    try:
        covert_films_to_vector_handler()
        return {"message": "Vectores creados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/retrieve-films-from-prompt-mysql/{prompt}")
async def get_films_from_prompt_mysql(prompt: str):
    films = retrieve_films_from_prompt_mysql(prompt)
    return {"films": films}


class NaturalLanguageQuery(BaseModel):
    question: str


@app.post("/query")
async def query_natural_language(query: NaturalLanguageQuery):
    """
    Endpoint para consultar la base de datos usando lenguaje natural.
    El modelo convertirá la pregunta a SQL y devolverá los resultados.
    """
    try:
        results = retrieve_films_from_natural_language(query.question)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
