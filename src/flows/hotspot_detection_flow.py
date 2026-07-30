from prefect import flow

from src.transformations.create_hotspots import create_hotspots


@flow(name="hotspot-detection")
def hotspot_flow():

    create_hotspots()


if __name__ == "__main__":

    hotspot_flow()
