from prefect import flow

from src.flows.prf_ingestion_flow import ingest_prf
from src.flows.bronze_to_silver_flow import bronze_to_silver
from src.flows.silver_to_gold_flow import silver_to_gold
from src.flows.create_ml_features_flow import create_ml_features
from src.flows.weather_enrichment_flow import weather_flow
from src.database.pipeline_audit_repository import (
    start_pipeline_run,
    finish_pipeline_run
)


@flow(name="br381-full-pipeline",retries=3,retry_delay_seconds=60)
def br381_pipeline():

    run_id = start_pipeline_run(
        "br381-full-pipeline"
    )

    try:

        print("Iniciando ingestão PRF")
        ingest_prf()

        print("Bronze -> Silver")
        bronze_to_silver()

        print("Silver -> Gold")
        silver_to_gold()


        print("Weather enrichment")
        weather_flow()

        print("Criando features ML")
        create_ml_features()

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

        raise e



if __name__ == "__main__":
    br381_pipeline()
