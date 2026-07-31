import logging

from prefect import flow, get_run_logger

from src.transformations.create_hotspots import create_hotspots


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(name="hotspot-detection", log_prints=True)
def hotspot_flow():
    logger = _get_logger()
    logger.info("Iniciando flow hotspot-detection.")

    try:
        create_hotspots()
        logger.info("Flow hotspot-detection concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow hotspot-detection.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    hotspot_flow()