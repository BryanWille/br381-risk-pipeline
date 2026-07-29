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

    ON CONFLICT (id) DO UPDATE SET
    	data_acidente = EXCLUDED.data_acidente,
    	horario = EXCLUDED.horario,
    	br = EXCLUDED.br,
    	km = EXCLUDED.km,
    	km_inicio = EXCLUDED.km_inicio,
    	km_fim = EXCLUDED.km_fim,
    	km_faixa_label = EXCLUDED.km_faixa_label,
    	municipio = EXCLUDED.municipio,
    	uf = EXCLUDED.uf,
    	causa_acidente = EXCLUDED.causa_acidente,
    	tipo_acidente = EXCLUDED.tipo_acidente,
    	classificacao_acidente = EXCLUDED.classificacao_acidente,
    	fase_dia = EXCLUDED.fase_dia,
    	sentido_via = EXCLUDED.sentido_via,
    	condicao_metereologica = EXCLUDED.condicao_metereologica,
    	tipo_pista = EXCLUDED.tipo_pista,
    	tracado_via = EXCLUDED.tracado_via,
    	uso_solo = EXCLUDED.uso_solo,
    	pessoas = EXCLUDED.pessoas,
    	mortos = EXCLUDED.mortos,
    	feridos_leves = EXCLUDED.feridos_leves,
    	feridos_graves = EXCLUDED.feridos_graves,
    	feridos = EXCLUDED.feridos,
    	latitude = EXCLUDED.latitude,
    	longitude = EXCLUDED.longitude;

    """

    cur.execute(sql)

    conn.commit()

    print(f"{cur.rowcount} registros transformados para Silver")

    cur.close()
    conn.close()
