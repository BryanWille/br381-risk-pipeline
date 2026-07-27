from psycopg2.extras import execute_values

from src.database.connection import get_connection


def insert_prf_accidents(columns, values):

    conn = get_connection()

    cur = conn.cursor()

    sql = f"""
        INSERT INTO bronze.prf_accidents_raw
        ({",".join(columns)})
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """

    execute_values(
        cur,
        sql,
        values,
        page_size=1000
    )

    conn.commit()

    cur.close()
    conn.close()
