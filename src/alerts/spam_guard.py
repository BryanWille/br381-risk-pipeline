import hashlib
import logging

from prefect import get_run_logger
from src.database.alert_repository import (
    alert_already_sent,
    save_alert,
)


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def build_alert_hash(km, probability, risk):
    logger = _get_logger()

    text = f"{km}|{risk}|{round(probability, 2)}"
    alert_hash = hashlib.sha256(text.encode()).hexdigest()

    logger.info(
        f"Hash de alerta gerado para KM {km}, risco {risk}, probabilidade arredondada {round(probability, 2)}."
    )

    return alert_hash


def should_send_alert(km, probability, risk):
    logger = _get_logger()

    logger.info(
        f"Verificando elegibilidade de alerta para KM {km}, risco {risk}, probabilidade {probability:.2%}."
    )

    alert_hash = build_alert_hash(km, probability, risk)

    if alert_already_sent(alert_hash):
        logger.info(
            f"Alerta já enviado anteriormente para KM {km}. Envio será ignorado."
        )
        return False

    save_alert(km, probability, risk, alert_hash)
    logger.info(f"Novo alerta persistido com sucesso para KM {km}.")

    return True