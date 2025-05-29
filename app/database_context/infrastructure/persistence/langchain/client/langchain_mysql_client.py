from langchain_community.utilities import SQLDatabase
from app.shared.infrastructure.settings import get_settings


def get_langchain_mysql_client(
    sample_rows_in_table_info: int = 3,
):
    settings = get_settings()

    db = SQLDatabase.from_uri(
        settings.langchain_db_connection,
        sample_rows_in_table_info=sample_rows_in_table_info,
    )
    return db
