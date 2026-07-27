from prefect import flow

from src.ingestion.prf_loader import ingest_to_bronze


@flow(name="prf-bronze-ingestion")
def ingest_prf():

    ingest_to_bronze(
        "data/raw/prf_accidentes_2026.csv"
    )


if __name__ == "__main__":
    ingest_prf()
