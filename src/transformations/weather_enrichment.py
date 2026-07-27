from src.database.connection import get_connection
from src.database.weather_repository import insert_weather_accident
from src.weather.open_meteo import get_historical_weather


def enrich_accidents_weather():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM silver.accidents_clean
    """)

    columns = [
        desc[0]
        for desc in cur.description
    ]

    rows = cur.fetchall()

    total = 0

    for row in rows:

        accident = dict(
            zip(columns, row)
        )

        weather = get_historical_weather(
            float(accident["latitude"]),
            float(accident["longitude"]),
            accident["data_acidente"].strftime("%Y-%m-%d")
	)

        if weather is None:
            print(f"Sem clima para acidente {accident['id']}")
            continue

        hour = accident["horario"].hour

        temperature = weather["hourly"]["temperature_2m"][hour]

        precipitation = weather["hourly"]["precipitation"][hour]

        wind = weather["hourly"]["wind_speed_10m"][hour]


        acidente_grave = (
            1
            if int(accident["mortos"]) > 0
            or int(accident["feridos_graves"]) > 0
            else 0
        )


        payload = {

            "id": accident["id"],

            "data_acidente": accident["data_acidente"],

            "horario": accident["horario"],

            "br": accident["br"],

            "km": accident["km"],

            "km_faixa_label": accident["km_faixa_label"],

            "latitude": accident["latitude"],

            "longitude": accident["longitude"],

            "municipio": accident["municipio"],

            "causa_acidente": accident["causa_acidente"],

            "tipo_acidente": accident["tipo_acidente"],

            "classificacao_acidente": accident["classificacao_acidente"],

            "fase_dia": accident["fase_dia"],

            "tipo_pista": accident["tipo_pista"],

            "tracado_via": accident["tracado_via"],

            "mortos": accident["mortos"],

            "feridos_graves": accident["feridos_graves"],

            "acidente_grave": acidente_grave,

            "temperature_2m": temperature,

            "precipitation": precipitation,

            "wind_speed_10m": wind

        }


        insert_weather_accident(payload)

        total += 1


    cur.close()

    conn.close()


    print(
        f"{total} acidentes enriquecidos"
    )
