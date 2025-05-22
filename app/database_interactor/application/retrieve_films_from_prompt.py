from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from app.shared.infrastructure.settings import get_settings


def retrieve_films_from_prompt(prompt: str):
    settings = get_settings()
    api_key = settings.openai_api_key
    if not api_key:
        logger.error("OPENAI_API_KEY no está configurada en las variables de entorno")
        connection.close()
        return

    embedding = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
    query_embedding = embedding.embed_query(prompt)

    qdrant_client = QdrantClient(url="http://qdrant:6333")

    results = qdrant_client.search(
        collection_name="films",
        query_vector=query_embedding,
        limit=5,
    )

    return results
