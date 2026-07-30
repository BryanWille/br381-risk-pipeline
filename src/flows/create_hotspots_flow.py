from prefect import flow

from src.transformations.create_hotspots import create_hotspots


@flow(name="create-hotspots")
def create_hotspots_flow():

    create_hotspots()


if __name__ == "__main__":
    create_hotspots_flow()
