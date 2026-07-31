import logging

from prefect import flow, get_run_logger

from src.transformations.weather_enrichment import enrich_accidents_weather


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(name="weather-enrichment", log_prints=True)
def weather_flow():
    logger = _get_logger()
    logger.info("Iniciando flow weather-enrichment.")

    try:
        enrich_accidents_weather()
        logger.info("Flow weather-enrichment concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow weather-enrichment.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    weather_flow()