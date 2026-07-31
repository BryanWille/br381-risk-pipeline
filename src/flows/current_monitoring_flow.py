import logging

from prefect import flow, get_run_logger

from src.flows.alert_flow import risk_alert_flow
from src.flows.create_hotspots_flow import create_hotspots_flow
from src.flows.current_risk_flow import current_risk_flow


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(
    name="current-monitoring",
    retries=2,
    retry_delay_seconds=30,
    log_prints=True,
)
def current_monitoring():
    logger = _get_logger()
    logger.info("Iniciando flow current-monitoring.")

    try:
        logger.info("Iniciando subflow: create_hotspots_flow")
        create_hotspots_flow()
        logger.info("Subflow concluído: create_hotspots_flow")

        logger.info("Iniciando subflow: current_risk_flow")
        current_risk_flow()
        logger.info("Subflow concluído: current_risk_flow")

        logger.info("Iniciando subflow: risk_alert_flow")
        risk_alert_flow()
        logger.info("Subflow concluído: risk_alert_flow")

        logger.info("Flow current-monitoring concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow current-monitoring.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    current_monitoring()