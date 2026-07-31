import logging

from prefect import flow, get_run_logger

from src.ml.predict_risk import predict_risk


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(name="predict-risk", log_prints=True)
def risk_prediction_flow():
    logger = _get_logger()
    logger.info("Iniciando flow predict-risk.")

    try:
        predict_risk()
        logger.info("Flow predict-risk concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow predict-risk.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    risk_prediction_flow()