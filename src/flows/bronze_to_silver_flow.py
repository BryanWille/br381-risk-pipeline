import logging

from prefect import flow, get_run_logger

from src.transformations.bronze_to_silver import transform_accidents


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(
    name="bronze-to-silver",
    retries=3,
    retry_delay_seconds=30,
    log_prints=True,
)
def bronze_to_silver():
    logger = _get_logger()
    logger.info("Iniciando flow bronze-to-silver.")

    try:
        transform_accidents()
        logger.info("Flow bronze-to-silver concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow bronze-to-silver.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bronze_to_silver()