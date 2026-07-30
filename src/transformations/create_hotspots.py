from src.database.connection import get_connection


def create_hotspots():

    conn = get_connection()

    cur = conn.cursor()


    sql = """

    TRUNCATE gold.current_hotspots;


    INSERT INTO gold.current_hotspots (

        km_faixa_label,
        ranking,
        indice_risco,
        acidentes_total,
        acidentes_graves

    )

    SELECT

        km_faixa_label,

        ROW_NUMBER() OVER(
            ORDER BY indice_risco DESC
        ),

        indice_risco,

        acidentes_total,

        acidentes_graves


    FROM gold.km_risk_aggregates


    ORDER BY indice_risco DESC

    LIMIT 10;


    """


    cur.execute(sql)

    conn.commit()


    print(
        f"{cur.rowcount} hotspots atualizados"
    )


    cur.close()
    conn.close()


if __name__ == "__main__":
    create_hotspots()
