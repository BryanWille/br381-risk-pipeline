from src.database.connection import get_connection


def create_ml_features():

    conn = get_connection()

    cur = conn.cursor()

    sql = """

    INSERT INTO gold.ml_accident_features (

        id,
        data_acidente,
        horario,
        br,
        km,
        km_inicio,
        km_fim,
        km_faixa_label,
        municipio,
        causa_acidente,
        tipo_acidente,
        fase_dia,
        sentido_via,
        tipo_pista,
        tracado_via,
        condicao_metereologica,
        pessoas,
        mortos,
        feridos_graves,
        acidente_grave,
        hora,
        periodo_noturno,
        tem_chuva,
        tem_curva,
        pista_simples

    )

    SELECT

        id,

        data_acidente,

        horario,

        br,

        km,

        km_inicio,

        km_fim,

        km_faixa_label,

        municipio,

        causa_acidente,

        tipo_acidente,

        fase_dia,

        sentido_via,

        tipo_pista,

        tracado_via,

        condicao_metereologica,

        pessoas,

        mortos,

        feridos_graves,


        CASE
            WHEN mortos > 0 
              OR feridos_graves > 0
            THEN 1
            ELSE 0
        END,


        EXTRACT(HOUR FROM horario),


        CASE
            WHEN fase_dia = 'Plena Noite'
            THEN 1
            ELSE 0
        END,


        CASE
            WHEN condicao_metereologica ILIKE '%Chuva%'
            THEN 1
            ELSE 0
        END,


        CASE
            WHEN tracado_via ILIKE '%Curva%'
            THEN 1
            ELSE 0
        END,


        CASE
            WHEN tipo_pista = 'Simples'
            THEN 1
            ELSE 0
        END


    FROM silver.accidents_clean


    ON CONFLICT (id)
    DO UPDATE SET

        acidente_grave = EXCLUDED.acidente_grave,
        hora = EXCLUDED.hora,
        periodo_noturno = EXCLUDED.periodo_noturno,
        tem_chuva = EXCLUDED.tem_chuva,
        tem_curva = EXCLUDED.tem_curva,
        pista_simples = EXCLUDED.pista_simples;

    """

    cur.execute(sql)

    conn.commit()

    print(
        f"{cur.rowcount} registros preparados para ML"
    )

    cur.close()
    conn.close()
