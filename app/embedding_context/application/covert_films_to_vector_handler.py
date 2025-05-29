import logging
import pymysql
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from app.shared.infrastructure.settings import get_settings
from qdrant_client import QdrantClient
from app.database_context.infrastructure.persistence.mysql.client.mysql_database_client import (
    get_mysql_database_client,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def covert_films_to_vector_handler():
class CovertFilmsToVectorHandler:
    def __init__(self):
        self.db = get_mysql_database_client()

    def handle(self):
        settings = get_settings()

        query = """
        SELECT f.film_id, f.title, f.description, f.release_year,
            GROUP_CONCAT(DISTINCT c.name) AS genres,
            GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name)) AS actors,
            f.rating, f.length
        FROM film f
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category c ON fc.category_id = c.category_id
        LEFT JOIN film_actor fa ON f.film_id = fa.film_id
        LEFT JOIN actor a ON fa.actor_id = a.actor_id
        GROUP BY f.film_id;
        """

        df = pd.read_sql(query, self.db)
        logger.info(f"Recuperadas {len(df)} películas de la base de datos")

        # Crear texto para embeddings combinando campos relevantes
        df["text_for_embedding"] = df.apply(
            lambda row: f"Título: {row['title']}\n"
            f"Descripción: {row['description']}\n"
            f"Año: {row['release_year']}\n"
            f"Géneros: {row['genres']}\n"
            f"Actores: {row['actors']}\n"
            f"Rating: {row['rating']}\n"
            f"Duración: {row['length']} minutos",
            axis=1,
        )

        # Generar embeddings usando OpenAI
        settings = get_settings()
        api_key = settings.openai_api_key
        if not api_key:
            logger.error(
                "OPENAI_API_KEY no está configurada en las variables de entorno"
            )
            self.db.close()
            return

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)

        qdrant_client = QdrantClient(url="http://qdrant:6333")

        # Procesar cada película y generar su embedding
        films_with_embeddings = []
        for idx, row in df.iterrows():
            try:
                film_id = row["film_id"]
                text = row["text_for_embedding"]

                # Generar embedding
                embedding_vector = embeddings.embed_query(text)

                # Agregar a la lista
                films_with_embeddings.append(
                    {
                        "film_id": film_id,
                        "title": row["title"],
                        "embedding": embedding_vector,
                    }
                )

                logger.info(
                    f"Generado embedding para película {film_id}: {row['title']}"
                )

                # Guardar en Qdrant
                qdrant_client.upsert(
                    collection_name="films",
                    points=[
                        {
                            "id": film_id,
                            "vector": embedding_vector,
                            "payload": {
                                "title": row["title"],
                                "description": row["description"],
                                "release_year": row["release_year"],
                                "genres": row["genres"],
                                "actors": row["actors"],
                                "rating": row["rating"],
                                "length": row["length"],
                            },
                        }
                    ],
                )
            except Exception as e:
                logger.error(
                    f"Error al generar embedding para película {row['film_id']}: {str(e)}"
                )

        logger.info(f"Generados embeddings para {len(films_with_embeddings)} películas")

        # Guardar resultados en Excel para visualización
        excel_path = "/code/data/films_data_embeddings2.xlsx"
        pd.DataFrame(
            [
                {
                    "film_id": f["film_id"],
                    "title": f["title"],
                    "embedding_dimension": len(f["embedding"]),
                }
                for f in films_with_embeddings
            ]
        ).to_excel(excel_path, index=False)
        logger.info(f"Información de embeddings guardada en {excel_path}")

        self.db.close()
        return films_with_embeddings
