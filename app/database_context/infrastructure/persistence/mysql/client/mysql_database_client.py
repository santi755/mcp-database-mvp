import pymysql
from app.shared.infrastructure.settings import get_settings


def get_mysql_database_client():
    settings = get_settings()

    print("---------------------------------")
    print(settings.db_host)
    print(settings.db_port)
    print(settings.db_user)
    print(settings.db_password)
    print(settings.db_name)
    print("---------------------------------")

    connection = pymysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
    )

    return connection
