from prefect import flow

from src.ml.predict_risk import predict_risk


@flow(name="predict-risk")
def risk_prediction_flow():

    predict_risk()


if __name__ == "__main__":

    risk_prediction_flow()
