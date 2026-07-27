from prefect import flow

from src.transformations.bronze_to_silver import transform_accidents


@flow(name="bronze-to-silver")
def bronze_to_silver():

    transform_accidents()


if __name__ == "__main__":
    bronze_to_silver()
