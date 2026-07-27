from prefect import flow

from src.transformations.silver_to_gold import create_risk_aggregates


@flow(name="silver-to-gold-risk")
def silver_to_gold():

    create_risk_aggregates()


if __name__ == "__main__":
    silver_to_gold()
