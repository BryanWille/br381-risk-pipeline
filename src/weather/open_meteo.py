import requests
import time


def get_historical_weather(
    latitude,
    longitude,
    date,
    retries=3
):

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {

        "latitude": latitude,

        "longitude": longitude,

        "start_date": date,

        "end_date": date,

        "hourly": [
            "temperature_2m",
            "precipitation",
            "wind_speed_10m"
        ]

    }


    for attempt in range(retries):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=(30, 180)
            )

            response.raise_for_status()

            return response.json()


        except requests.exceptions.RequestException as e:

            print(
                f"Erro Open-Meteo tentativa {attempt + 1}/{retries}: {e}"
            )


            if attempt < retries - 1:
                time.sleep(5)


    return None

def get_current_weather(
    latitude,
    longitude
):

    url = "https://api.open-meteo.com/v1/forecast"


    params = {

        "latitude": latitude,

        "longitude": longitude,

        "current": [
            "temperature_2m",
            "precipitation",
            "wind_speed_10m"
        ]

    }


    response = requests.get(
        url,
        params=params,
        timeout=30
    )


    response.raise_for_status()


    return response.json()
