import psycopg2

from src.database.connection import get_connection


def transform_accidents():

    conn = get_connection()

    cur = conn.cursor()

    sql = """

    INSERT INTO silver.accidents_clean (

        id,
        data_acidente,
        horario,
        br,
        km,
        km_inicio,
        km_fim,
        km_faixa_label,
        municipio,
        uf,
        causa_acidente,
        tipo_acidente,
        classificacao_acidente,
        fase_dia,
        sentido_via,
        condicao_metereologica,
        tipo_pista,
        tracado_via,
        uso_solo,
        pessoas,
        mortos,
        feridos_leves,
        feridos_graves,
        feridos,
        latitude,
        longitude

    )

    SELECT

        id,

        TO_DATE(data_inversa, 'DD/MM/YYYY'),

        horario::TIME,

        br,

        REPLACE(km, ',', '.')::NUMERIC,

        FLOOR(REPLACE(km, ',', '.')::NUMERIC / 10) * 10,

        FLOOR(REPLACE(km, ',', '.')::NUMERIC / 10) * 10 + 10,

        CONCAT(
            FLOOR(REPLACE(km, ',', '.')::NUMERIC / 10) * 10,
            '-',
            FLOOR(REPLACE(km, ',', '.')::NUMERIC / 10) * 10 + 10
        ),

        municipio,
        uf,

        causa_acidente,
        tipo_acidente,
        classificacao_acidente,

        fase_dia,
        sentido_via,
        condicao_metereologica,

        tipo_pista,
        tracado_via,
        uso_solo,

        pessoas::INTEGER,
        mortos::INTEGER,
        feridos_leves::INTEGER,
        feridos_graves::INTEGER,
        feridos::INTEGER,

        REPLACE(latitude, ',', '.')::DOUBLE PRECISION,
        REPLACE(longitude, ',', '.')::DOUBLE PRECISION

    FROM bronze.prf_accidents_raw

    WHERE br = 381

    ON CONFLICT (id) DO NOTHING;

    """

    cur.execute(sql)

    conn.commit()

    print(f"{cur.rowcount} registros transformados para Silver")

    cur.close()
    conn.close()
