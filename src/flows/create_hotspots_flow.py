import logging

from prefect import flow, get_run_logger

from src.transformations.create_hotspots import create_hotspots


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(name="create-hotspots", log_prints=True)
def create_hotspots_flow():
    logger = _get_logger()
    logger.info("Iniciando flow create-hotspots.")

    try:
        create_hotspots()
        logger.info("Flow create-hotspots concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow create-hotspots.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_hotspots_flow()