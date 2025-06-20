from qdrant_client import QdrantClient, models
from dishka.integrations.fastapi import setup_dishka

from fastapi import FastAPI


from pydantic import BaseModel
from app.shared.infrastructure.dependency_injection.container import setup_container
from app.ai_context.infrastructure.fastapi.controller import ai_context_router
from app.database_context.infrastructure.fastapi.controller import (
    database_context_router,
)
from app.embedding_context.infrastructure.fastapi.controller import (
    embedding_context_router,
)

app = FastAPI()


# Setup Qdrant client
@app.on_event("startup")
async def startup_db_client():
    app.qdrant_client = QdrantClient(url="http://qdrant:6333")

    # Create collections if they don't exist
    collections = app.qdrant_client.get_collections().collections
    collection_names = [c.name for c in collections]

    if "films" not in collection_names:
        app.qdrant_client.create_collection(
            collection_name="films",
            vectors_config=models.VectorParams(
                size=1536, distance=models.Distance.COSINE
            ),
        )


# Setup dishka dependencies
container = setup_container(app)
setup_dishka(container, app)

# Setup routers
app.include_router(ai_context_router)
app.include_router(database_context_router)
app.include_router(embedding_context_router)
