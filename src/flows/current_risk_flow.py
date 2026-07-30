from prefect import flow

from src.ml.current_risk import predict_current_risk


@flow(name="current-risk")
def current_risk_flow():

    predict_current_risk()


if __name__ == "__main__":

    current_risk_flow()
