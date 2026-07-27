import requests


lat = -19.92
lon = -44.10

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": lat,
    "longitude": lon,
    "start_date": "2026-01-01",
    "end_date": "2026-01-01",
    "hourly": [
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

print("Status:", response.status_code)

data = response.json()

print(data.keys())

print(data["hourly"].keys())

print(data["hourly"]["temperature_2m"][:5])
