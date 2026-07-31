import logging

from prefect import flow, get_run_logger

from src.ml.current_risk import predict_current_risk


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(name="current-risk", log_prints=True)
def current_risk_flow():
    logger = _get_logger()
    logger.info("Iniciando flow current-risk.")

    try:
        predict_current_risk()
        logger.info("Flow current-risk concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow current-risk.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    current_risk_flow()