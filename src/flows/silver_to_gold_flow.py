import logging

from prefect import flow, get_run_logger

from src.transformations.silver_to_gold import create_risk_aggregates


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(
    name="silver-to-gold-risk",
    retries=3,
    retry_delay_seconds=30,
    log_prints=True,
)
def silver_to_gold():
    logger = _get_logger()
    logger.info("Iniciando flow silver-to-gold-risk.")

    try:
        create_risk_aggregates()
        logger.info("Flow silver-to-gold-risk concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow silver-to-gold-risk.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    silver_to_gold()