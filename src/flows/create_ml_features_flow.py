from prefect import flow

from src.transformations.create_ml_features import create_ml_features


@flow(name="create-ml-features",retries=3,retry_delay_seconds=30)
def ml_features():

    create_ml_features()


if __name__ == "__main__":
    ml_features()
