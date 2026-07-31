from prefect import flow

from src.flows.prf_ingestion_flow import ingest_prf
from src.flows.bronze_to_silver_flow import bronze_to_silver
from src.flows.silver_to_gold_flow import silver_to_gold
from src.flows.hotspot_detection_flow import hotspot_flow
from src.flows.weather_enrichment_flow import weather_flow
from src.flows.create_ml_features_flow import ml_features
from src.flows.predict_risk_flow import risk_prediction_flow
from src.flows.current_risk_flow import current_risk_flow
from src.flows.alert_flow import risk_alert_flow
from src.config.init_variables import init_variables
from src.database.init_db import initialize_db
from src.database.pipeline_audit_repository import (
    start_pipeline_run,
    finish_pipeline_run
)

@flow(
    name="br381-full-pipeline",
    retries=3,
    retry_delay_seconds=60
)
def br381_pipeline():
    init_variables()
    initialize_db()

    run_id = start_pipeline_run("br381-full-pipeline")

    try:
        print("Iniciando ingestão PRF")
        ingest_prf()

        print("Bronze -> Silver")
        bronze_to_silver()

        print("Silver -> Gold")
        silver_to_gold()

        print("Detectando hotspots")
        hotspot_flow()

        print("Weather enrichment")
        weather_flow()

        print("Criando features ML")
        ml_features()

        print("Prevendo risco histórico")
        risk_prediction_flow()

        print("Calculando risco atual")
        current_risk_flow()

        print("Enviando alertas")
        risk_alert_flow()

        finish_pipeline_run(
            run_id,
            "SUCCESS",
            records_processed=None
        )

        print("Pipeline finalizado")

    except Exception as e:
        finish_pipeline_run(
            run_id,
            "FAILED",
            error_message=str(e)
        )
        raise

if __name__ == "__main__":
    br381_pipeline()