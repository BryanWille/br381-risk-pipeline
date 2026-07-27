from src.database.connection import get_connection


def create_schemas():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        CREATE SCHEMA IF NOT EXISTS bronze;
        CREATE SCHEMA IF NOT EXISTS silver;
        CREATE SCHEMA IF NOT EXISTS gold;
        CREATE SCHEMA IF NOT EXISTS serving;
        """
    )

    conn.commit()

    cur.close()
    conn.close()
