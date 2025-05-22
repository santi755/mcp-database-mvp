import pymysql
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_schema():
    """
    Extrae el esquema de la base de datos Sakila de manera más coherente
    usando SHOW CREATE TABLE y SHOW TABLES.
    """
    try:
        connection = pymysql.connect(
            host="mysqlDB",
            port=3306,
            user="root",
            password="root",
            database="sakila",
        )

        cursor = connection.cursor()

        # Obtener lista de tablas
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
        tables = [table[0] for table in cursor.fetchall()]

        schema_parts = []

        # Para cada tabla, obtener estructura y descripciones
        for table_name in tables:
            # Obtener la estructura de la tabla
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()

            table_schema = [f"Table: {table_name}"]
            table_schema.append("Columns:")

            for column in columns:
                # column[0]: Field, column[1]: Type, column[2]: Null, column[3]: Key
                field_name = column[0]
                field_type = column[1]
                is_nullable = "YES" if column[2] == "YES" else "NO"
                key_type = column[3]  # PRI, MUL, UNI, etc.

                col_desc = f"- {field_name} ({field_type})"

                if key_type == "PRI":
                    col_desc += ": Primary Key"
                elif key_type == "MUL":
                    col_desc += ": Foreign Key"
                elif key_type == "UNI":
                    col_desc += ": Unique Key"

                col_desc += f", Nullable: {is_nullable}"

                table_schema.append(col_desc)

            # Obtener información adicional sobre índices y claves
            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_table = cursor.fetchone()[1]

            # Extraer información sobre claves foráneas si existen
            if "FOREIGN KEY" in create_table:
                table_schema.append("\nForeign Keys:")
                for line in create_table.split("\n"):
                    if "FOREIGN KEY" in line:
                        # Limpiar y formatear la línea
                        clean_line = line.strip().rstrip(",")
                        if "CONSTRAINT" in clean_line:
                            clean_line = " ".join(
                                clean_line.split()[2:]
                            )  # Omitir CONSTRAINT `nombre`
                        table_schema.append(f"- {clean_line}")

            schema_parts.append("\n".join(table_schema))

        # Información adicional sobre la base de datos
        cursor.execute("SELECT @@character_set_database, @@collation_database")
        db_info = cursor.fetchone()
        db_metadata = [
            "Database Metadata:",
            f"- Character Set: {db_info[0]}",
            f"- Collation: {db_info[1]}",
        ]

        schema_parts.append("\n".join(db_metadata))

        cursor.close()
        connection.close()

        return "\n\n".join(schema_parts)

    except Exception as e:
        logger.error(f"Error obteniendo el esquema de la base de datos: {str(e)}")
        return f"Error: {str(e)}"


if __name__ == "__main__":
    schema = get_database_schema()
    print(schema)

    # Guardar el esquema en un archivo de texto
    with open("sakila_schema.txt", "w") as f:
        f.write(schema)
    logger.info("Esquema guardado en sakila_schema.txt")
