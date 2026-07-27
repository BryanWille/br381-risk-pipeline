from prefect import flow

from src.transformations.weather_enrichment import enrich_accidents_weather


@flow(name="weather-enrichment")
def weather_flow():

    enrich_accidents_weather()


if __name__ == "__main__":

    weather_flow()
