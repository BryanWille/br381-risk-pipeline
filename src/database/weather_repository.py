from src.database.connection import get_connection


def insert_weather_accident(data):

    conn = get_connection()

    cur = conn.cursor()


    sql = """
    INSERT INTO silver.accidents_weather_enriched (

        id,
        data_acidente,
        horario,
        br,
        km,
        km_faixa_label,
        latitude,
        longitude,
        municipio,
        causa_acidente,
        tipo_acidente,
        classificacao_acidente,
        fase_dia,
        tipo_pista,
        tracado_via,
        mortos,
        feridos_graves,
        acidente_grave,
        temperature_2m,
        precipitation,
        wind_speed_10m

    )

    VALUES (

        %(id)s,
        %(data_acidente)s,
        %(horario)s,
        %(br)s,
        %(km)s,
        %(km_faixa_label)s,
        %(latitude)s,
        %(longitude)s,
        %(municipio)s,
        %(causa_acidente)s,
        %(tipo_acidente)s,
        %(classificacao_acidente)s,
        %(fase_dia)s,
        %(tipo_pista)s,
        %(tracado_via)s,
        %(mortos)s,
        %(feridos_graves)s,
        %(acidente_grave)s,
        %(temperature_2m)s,
        %(precipitation)s,
        %(wind_speed_10m)s

    )

    ON CONFLICT (id)
    DO UPDATE SET

        temperature_2m = EXCLUDED.temperature_2m,
        precipitation = EXCLUDED.precipitation,
        wind_speed_10m = EXCLUDED.wind_speed_10m;

    """


    cur.execute(sql, data)

    conn.commit()

    cur.close()
    conn.close()
