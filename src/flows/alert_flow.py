import logging

from prefect import flow, get_run_logger

from src.alerts.risk_alert import check_high_risk_alerts


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(name="risk-alert", log_prints=True)
def risk_alert_flow():
    logger = _get_logger()
    logger.info("Iniciando flow risk-alert.")

    try:
        check_high_risk_alerts()
        logger.info("Flow risk-alert concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow risk-alert.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    risk_alert_flow()