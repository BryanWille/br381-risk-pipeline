from src.database.connection import get_connection


def create_risk_aggregates():

    conn = get_connection()

    cur = conn.cursor()

    sql = """

    INSERT INTO gold.km_risk_aggregates (

        km_faixa_label,
        acidentes_total,
        acidentes_graves,
        total_mortos,
        total_feridos_graves,
        taxa_gravidade,
        indice_risco

    )

    SELECT

        km_faixa_label,

        COUNT(*) AS acidentes_total,

        COUNT(*) FILTER (
            WHERE mortos > 0
            OR feridos_graves > 0
        ) AS acidentes_graves,

        COALESCE(SUM(mortos), 0),

        COALESCE(SUM(feridos_graves), 0),

        ROUND(
            COUNT(*) FILTER (
                WHERE mortos > 0
                OR feridos_graves > 0
            )::numeric
            /
            NULLIF(COUNT(*)::numeric, 0),
            4
        ),

        ROUND(
            (
                COALESCE(SUM(mortos), 0) * 10
                +
                COALESCE(SUM(feridos_graves), 0) * 3
                +
                COUNT(*) * 0.1
            )::numeric,
            2
        )

    FROM silver.accidents_clean

    GROUP BY km_faixa_label

    ON CONFLICT (km_faixa_label)

    DO UPDATE SET

        acidentes_total = EXCLUDED.acidentes_total,

        acidentes_graves = EXCLUDED.acidentes_graves,

        total_mortos = EXCLUDED.total_mortos,

        total_feridos_graves = EXCLUDED.total_feridos_graves,

        taxa_gravidade = EXCLUDED.taxa_gravidade,

        indice_risco = EXCLUDED.indice_risco;

    """

    cur.execute(sql)

    conn.commit()

    print(
        f"{cur.rowcount} faixas atualizadas na Gold"
    )

    cur.close()
    conn.close()
