from src.database.connection import get_connection


def alert_already_sent(alert_hash, hours=1):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM gold.alert_history
        WHERE alert_hash = %s
          AND sent_at >= NOW() - (%s || ' hour')::interval
        LIMIT 1
        """,
        (alert_hash, hours)
    )

    exists = cur.fetchone() is not None

    cur.close()
    conn.close()

    return exists


def save_alert(
    km_faixa_label,
    probability,
    risk_class,
    alert_hash
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO gold.alert_history(

            km_faixa_label,
            probability,
            risk_class,
            alert_hash

        )
        VALUES(%s,%s,%s,%s)
        """,
        (
            km_faixa_label,
            probability,
            risk_class,
            alert_hash
        )
    )

    conn.commit()

    cur.close()
    conn.close()
