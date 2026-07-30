from src.database.connection import get_connection


def insert_risk_prediction(data):

    conn = get_connection()

    cur = conn.cursor()

    sql = """
    INSERT INTO gold.risk_predictions (

        id,
        km,
        municipio,
        probability,
        risk_class

    )

    VALUES (

        %(id)s,
        %(km)s,
        %(municipio)s,
        %(probability)s,
        %(risk_class)s

    )

    ON CONFLICT (id)

    DO UPDATE SET

        probability = EXCLUDED.probability,
        risk_class = EXCLUDED.risk_class;

    """

    cur.execute(sql, data)

    conn.commit()

    cur.close()

    conn.close()
