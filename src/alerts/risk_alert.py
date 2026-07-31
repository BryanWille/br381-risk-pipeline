import logging

from prefect import get_run_logger
from src.database.connection import get_connection
from src.alerts.telegram_alert import send_telegram_message
from src.alerts.spam_guard import should_send_alert
from src.config.risk_config import (
    get_telegram_alert_threshold,
    get_telegram_alert_enabled,
)


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def check_high_risk_alerts():
    logger = _get_logger()
    logger.info("Iniciando verificação de alertas de alto risco.")

    try:
        if not get_telegram_alert_enabled():
            logger.info("Alertas Telegram desativados. Encerrando verificação.")
            return

        threshold = get_telegram_alert_threshold()
        logger.info(f"Threshold de alerta carregado com sucesso: {threshold}")

        conn = get_connection()
        cur = conn.cursor()
        logger.info("Conexão com banco aberta com sucesso.")

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

        logger.info("Executando consulta de trechos com risco acima do threshold.")
        cur.execute(query, (threshold,))
        rows = cur.fetchall()
        logger.info(f"Consulta concluída. {len(rows)} linha(s) retornada(s).")

        cur.close()
        conn.close()
        logger.info("Conexão com banco encerrada.")

        if not rows:
            logger.info("Nenhum risco crítico encontrado para envio de alerta.")
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
                hora,
            ) = row

            logger.info(
                f"Avaliando trecho KM {km} com probabilidade {float(probability):.2%} e classe {risk}."
            )

            if should_send_alert(km, float(probability), risk):
                alerts.append(
                    {
                        "km": km,
                        "probability": float(probability),
                        "risk": risk,
                        "temperature": temperature,
                        "precipitation": precipitation,
                        "wind": wind,
                        "hora": hora,
                    }
                )
                logger.info(f"Alerta aprovado para KM {km}.")
            else:
                logger.info(f"Alerta suprimido pelo spam_guard para KM {km}.")

        if not alerts:
            logger.info("Nenhum alerta novo elegível para envio.")
            return

        logger.info(f"{len(alerts)} alerta(s) elegível(is) para envio ao Telegram.")

        message = """
🚨 <b>ALERTA BR-381</b>

Foram detectados riscos elevados nos seguintes trechos:

"""

        for alert in alerts:
            chuva = "Sim" if alert["precipitation"] > 0 else "Não"

            message += (
                f"\n📍 <b>KM {alert['km']}</b>\n"
                f"🎯 Probabilidade: {alert['probability']:.1%}\n"
                f"⚠️ Classificação: {alert['risk']}\n"
                f"🌡 Temperatura: {alert['temperature']}°C\n"
                f"🌧 Chuva: {chuva}\n"
                f"💨 Vento: {alert['wind']} km/h\n"
                f"🕒 Hora: {alert['hora']}:00\n"
            )

        logger.info("Enviando mensagem de alerta via Telegram.")
        send_telegram_message(message)
        logger.info(f"{len(alerts)} alerta(s) enviado(s) com sucesso.")

    except Exception:
        logger.exception("Erro ao verificar ou enviar alertas de alto risco.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    check_high_risk_alerts()