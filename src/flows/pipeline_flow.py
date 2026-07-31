import logging

from prefect import flow, get_run_logger

from src.config.init_variables import init_variables
from src.database.init_db import initialize_db
from src.database.pipeline_audit_repository import (
    finish_pipeline_run,
    start_pipeline_run,
)
from src.flows.alert_flow import risk_alert_flow
from src.flows.bronze_to_silver_flow import bronze_to_silver
from src.flows.create_ml_features_flow import ml_features
from src.flows.current_risk_flow import current_risk_flow
from src.flows.hotspot_detection_flow import hotspot_flow
from src.flows.predict_risk_flow import risk_prediction_flow
from src.flows.prf_ingestion_flow import ingest_prf
from src.flows.silver_to_gold_flow import silver_to_gold
from src.flows.weather_enrichment_flow import weather_flow


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


@flow(
    name="br381-full-pipeline",
    retries=3,
    retry_delay_seconds=60,
    log_prints=True,
)
def br381_pipeline():
    logger = _get_logger()
    logger.info("Iniciando execução do flow principal br381-full-pipeline.")

    init_variables()
    logger.info("Variáveis do Prefect inicializadas.")

    initialize_db()
    logger.info("Banco de dados inicializado/verificado.")

    run_id = start_pipeline_run("br381-full-pipeline")
    logger.info(f"Execução de auditoria iniciada com run_id={run_id}.")

    try:
        logger.info("Iniciando subflow: ingest_prf")
        ingest_prf()
        logger.info("Subflow concluído: ingest_prf")

        logger.info("Iniciando subflow: bronze_to_silver")
        bronze_to_silver()
        logger.info("Subflow concluído: bronze_to_silver")

        logger.info("Iniciando subflow: silver_to_gold")
        silver_to_gold()
        logger.info("Subflow concluído: silver_to_gold")

        logger.info("Iniciando subflow: hotspot_flow")
        hotspot_flow()
        logger.info("Subflow concluído: hotspot_flow")

        logger.info("Iniciando subflow: weather_flow")
        weather_flow()
        logger.info("Subflow concluído: weather_flow")

        logger.info("Iniciando subflow: ml_features")
        ml_features()
        logger.info("Subflow concluído: ml_features")

        logger.info("Iniciando subflow: risk_prediction_flow")
        risk_prediction_flow()
        logger.info("Subflow concluído: risk_prediction_flow")

        logger.info("Iniciando subflow: current_risk_flow")
        current_risk_flow()
        logger.info("Subflow concluído: current_risk_flow")

        logger.info("Iniciando subflow: risk_alert_flow")
        risk_alert_flow()
        logger.info("Subflow concluído: risk_alert_flow")

        finish_pipeline_run(
            run_id,
            "SUCCESS",
            records_processed=None,
        )
        logger.info("Pipeline finalizado com sucesso.")

    except Exception as e:
        finish_pipeline_run(
            run_id,
            "FAILED",
            error_message=str(e),
        )
        logger.exception("Pipeline finalizado com erro.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    br381_pipeline()