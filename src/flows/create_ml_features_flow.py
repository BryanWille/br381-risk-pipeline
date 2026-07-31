import logging

from prefect import flow, get_run_logger

from src.transformations.create_ml_features import create_ml_features


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(
    name="create-ml-features",
    retries=3,
    retry_delay_seconds=30,
    log_prints=True,
)
def ml_features():
    logger = _get_logger()
    logger.info("Iniciando flow create-ml-features.")

    try:
        create_ml_features()
        logger.info("Flow create-ml-features concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow create-ml-features.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ml_features()