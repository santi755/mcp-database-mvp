import logging
import pymysql
import pandas as pd
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.database_interactor.application.get_database_schema import get_database_schema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def retrieve_films_from_natural_language(question: str):
    """
    Utiliza LLM para convertir una pregunta en lenguaje natural a SQL
    y ejecuta la consulta contra la base de datos Sakila.
    """
    # Obtener el esquema real de la base de datos
    schema = get_database_schema()

    # Configurar el prompt
    template = """Based on the table schema below, write a SQL query that would answer the user's question.
    Return ONLY the SQL query without any explanation.
    
    {schema}
    
    Question: {question}
    SQL Query:"""
    prompt = ChatPromptTemplate.from_template(template)

    # Configurar el modelo
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY no está configurada en las variables de entorno"
        )

    model = ChatOpenAI(model="gpt-3.5-turbo")

    # Generar la consulta SQL
    chain = prompt | model
    result = chain.invoke({"schema": schema, "question": question})
    generated_sql = result.content.strip()

    logger.info(f"Pregunta: {question}")
    logger.info(f"SQL generado: {generated_sql}")

    # Ejecutar la consulta SQL
    try:
        connection = pymysql.connect(
            host="mysqlDB",
            port=3306,
            user="root",
            password="root",
            database="sakila",
        )

        df = pd.read_sql(generated_sql, connection)
        connection.close()

        # Guardar resultados en Excel para fácil visualización
        excel_path = "/code/data/query_results.xlsx"
        df.to_excel(excel_path, index=False)
        logger.info(f"Resultados guardados en {excel_path}")

        return {
            "query": generated_sql,
            "results": df.to_dict(orient="records"),
            "row_count": len(df),
        }

    except Exception as e:
        logger.error(f"Error al ejecutar SQL: {str(e)}")
        return {"error": str(e), "query": generated_sql}
