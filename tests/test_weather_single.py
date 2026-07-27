from src.weather.open_meteo import get_historical_weather


data = get_historical_weather(
    -20.0240733,
    -42.7422291,
    "2026-01-01"
)


hourly = data["hourly"]


print(
    hourly["time"][6]
)

print(
    "Temperatura:",
    hourly["temperature_2m"][6]
)

print(
    "Chuva:",
    hourly["precipitation"][6]
)

print(
    "Vento:",
    hourly["wind_speed_10m"][6]
)
