from src.database.connection import get_connection


def insert_current_risk(data):

    conn = get_connection()

    cur = conn.cursor()

    sql = """
    INSERT INTO gold.current_risk_state (

        km_faixa_label,
        temperature_2m,
        precipitation,
        wind_speed_10m,
        hora,
        periodo_noturno,
        probability,
        risk_class

    )

    VALUES (

        %(km_faixa_label)s,
        %(temperature_2m)s,
        %(precipitation)s,
        %(wind_speed_10m)s,
        %(hora)s,
        %(periodo_noturno)s,
        %(probability)s,
        %(risk_class)s

    )

    ON CONFLICT (km_faixa_label)

    DO UPDATE SET

        temperature_2m = EXCLUDED.temperature_2m,
        precipitation = EXCLUDED.precipitation,
        wind_speed_10m = EXCLUDED.wind_speed_10m,
        hora = EXCLUDED.hora,
        periodo_noturno = EXCLUDED.periodo_noturno,
        probability = EXCLUDED.probability,
        risk_class = EXCLUDED.risk_class,
        created_at = CURRENT_TIMESTAMP;

    """

    cur.execute(sql, data)

    conn.commit()

    cur.close()
    conn.close()
