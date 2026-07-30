from src.database.connection import get_connection

from src.alerts.telegram_alert import (
    send_telegram_message
)

from src.alerts.spam_guard import (
    should_send_alert
)

from src.config.risk_config import (
    get_telegram_alert_threshold,
    get_telegram_alert_enabled
)


def check_high_risk_alerts():

    if not get_telegram_alert_enabled():

        print(
            "Alertas Telegram desativados."
        )

        return
    
    threshold = get_telegram_alert_threshold()


    conn = get_connection()

    cur = conn.cursor()


    query = """

    SELECT

        km_faixa_label,
        probability,
        risk_class,
        temperature_2m,
        precipitation,
        wind_speed_10m,
        hora

    FROM gold.current_risk_state

    WHERE probability >= %s

    ORDER BY probability DESC

    """


    cur.execute(
        query,
        (threshold,)
    )


    rows = cur.fetchall()


    cur.close()
    conn.close()


    if not rows:

        print(
            "Nenhum risco crítico encontrado."
        )

        return


    alerts = []


    for row in rows:

        (
            km,
            probability,
            risk,
            temperature,
            precipitation,
            wind,
            hora

        ) = row


        if should_send_alert(
            km,
            float(probability),
            risk
        ):

            alerts.append({

                "km": km,

                "probability": float(probability),

                "risk": risk,

                "temperature": temperature,

                "precipitation": precipitation,

                "wind": wind,

                "hora": hora

            })


    if not alerts:

        print(
            "Nenhum alerta novo."
        )

        return


    message = """
🚨 <b>ALERTA BR-381</b>

Foram detectados riscos elevados nos seguintes trechos:

"""


    for alert in alerts:


        chuva = (
            "Sim"
            if alert["precipitation"] > 0
            else "Não"
        )


        message += (

            f"\n📍 <b>KM {alert['km']}</b>\n"

            f"🎯 Probabilidade: {alert['probability']:.1%}\n"

            f"⚠️ Classificação: {alert['risk']}\n"

            f"🌡 Temperatura: {alert['temperature']}°C\n"

            f"🌧 Chuva: {chuva}\n"

            f"💨 Vento: {alert['wind']} km/h\n"

            f"🕒 Hora: {alert['hora']}:00\n"

        )


    send_telegram_message(
        message
    )


    print(
        f"{len(alerts)} alerta(s) enviados."
    )


if __name__ == "__main__":

    check_high_risk_alerts()