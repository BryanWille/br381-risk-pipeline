import logging

from prefect import flow, get_run_logger

from src.ingestion.prf_loader import ingest_to_bronze


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(
    name="prf-bronze-ingestion",
    retries=3,
    retry_delay_seconds=30,
    log_prints=True,
)
def ingest_prf():
    logger = _get_logger()
    logger.info("Iniciando flow prf-bronze-ingestion.")

    try:
        ingest_to_bronze("data/raw/prf_accidentes_2026.csv")
        logger.info("Ingestão da PRF para a camada bronze concluída com sucesso.")

    except Exception:
        logger.exception("Erro no flow prf-bronze-ingestion.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ingest_prf()