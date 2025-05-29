from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI

import os


SCHEMA_RELATIONSHIPS = {
    # Film-related relationships
    "film_relationships": [
        # Actor relationships
        "actor -> film_actor -> film",
        "film -> film_actor -> actor",
        # Category relationships
        "film -> film_category -> category",
        "category -> film_category -> film",
        # Language relationship
        "film -> language (language_id)",
        # Inventory and rental relationships
        "film -> inventory -> rental -> customer",
        "customer -> rental -> inventory -> film",
        # Store and staff relationships
        "film -> inventory -> store -> staff",
        "staff -> store -> inventory -> film",
    ],
    # Customer-related relationships
    "customer_relationships": [
        "customer -> rental -> inventory -> film",
        "customer -> payment -> staff",
        "customer -> payment -> rental",
        "customer -> address -> city -> country",
    ],
    # Staff-related relationships
    "staff_relationships": [
        "staff -> store -> inventory -> film",
        "staff -> payment -> customer",
        "staff -> rental -> inventory -> film",
        "staff -> address -> city -> country",
    ],
    # Store-related relationships
    "store_relationships": [
        "store -> inventory -> film",
        "store -> staff",
        "store -> customer -> rental -> inventory",
    ],
    # Address-related relationships
    "address_relationships": [
        "address -> city -> country",
        "address -> customer",
        "address -> staff",
        "address -> store",
    ],
}


def get_relationship_chains():
    """
    Returns a formatted string containing all relationship chains in the Sakila database.
    """
    chains = []
    for category, relationships in SCHEMA_RELATIONSHIPS.items():
        chains.append(f"\n{category.upper()}:")
        for rel in relationships:
            chains.append(f"-- {rel}")

    return "\n".join(chains)


def retrieve_data_from_prompt(question: str):
    db = get_database_connection()

    response = get_response(question, db, [])

    return response


def get_database_connection():
    db = SQLDatabase.from_uri(
        "mysql+mysqlconnector://root:root@mysql:3306/sakila",
        sample_rows_in_table_info=3,
    )
    return db


def get_sql_chain(db):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)

    # llm = ChatOpenAI(model="gpt-4o-mini")
    llm = GoogleGenerativeAI(model="gemini-2.0-flash")

    def get_schema_with_relationships(_: dict) -> str:
        base_schema = db.get_table_info()
        relationships = get_relationship_chains()

        return f"{base_schema}\n\n{relationships}"

    return (
        RunnablePassthrough.assign(
            schema=get_schema_with_relationships,
            chat_history=lambda _: [],
        )
        | prompt
        | llm
        | StrOutputParser()
    )


def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)

    template = """
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, question, sql query, and sql response, write a natural language response.
        <SCHEMA>{schema}</SCHEMA>

        Conversation History: {chat_history}
        SQL Query: <SQL>{query}</SQL>
        User question: {question}
        SQL Response: {response}"""

    prompt = ChatPromptTemplate.from_template(template)

    # llm = ChatOpenAI(model="gpt-4o-mini")
    llm = GoogleGenerativeAI(model="gemini-2.0-flash")

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(
        {
            "question": user_query,
            "chat_history": chat_history,
        }
    )
