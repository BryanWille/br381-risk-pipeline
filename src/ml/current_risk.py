import joblib
import pandas as pd

from datetime import datetime

from src.database.connection import get_connection
from src.database.current_risk_repository import insert_current_risk
from src.weather.open_meteo import get_current_weather



def get_current_hotspots():

    conn = get_connection()

    query = """
        SELECT

            h.km_faixa_label,

            AVG(a.latitude) AS latitude,

            AVG(a.longitude) AS longitude,

            AVG(a.km) AS km

        FROM gold.current_hotspots h

        JOIN silver.accidents_clean a

        ON a.km_faixa_label = h.km_faixa_label

        GROUP BY
            h.km_faixa_label,
            h.indice_risco

        ORDER BY h.indice_risco DESC

        LIMIT 10
    """


    df = pd.read_sql(
        query,
        conn
    )


    conn.close()


    return df



def classify_risk(probability):

    if probability >= 0.35:

        return "ALTO"


    elif probability >= 0.15:

        return "MEDIO"


    return "BAIXO"



def get_current_time_features():

    now = datetime.now()

    hora = now.hour


    periodo_noturno = (

        1

        if hora >= 18 or hora < 6

        else 0

    )


    return hora, periodo_noturno



def predict_current_risk():

    print("Carregando modelo...")


    model_data = joblib.load(
        "models/risk_model.joblib"
    )


    model = model_data["model"]

    features = model_data["features"]


    hotspots = get_current_hotspots()


    hora, periodo_noturno = get_current_time_features()


    print(
        f"Hotspots analisados: {len(hotspots)}"
    )


    results = []


    for _, row in hotspots.iterrows():


        print(
            f"Consultando clima KM {row['km_faixa_label']}"
        )


        weather = get_current_weather(

            float(row["latitude"]),

            float(row["longitude"])

        )


        if weather:

            current = weather["current"]


            temperature = current["temperature_2m"]

            precipitation = current["precipitation"]

            wind = current["wind_speed_10m"]


        else:

            temperature = 25

            precipitation = 0

            wind = 0



        payload = {

            "km": float(row["km"]),

            "hora": hora,

            "periodo_noturno": periodo_noturno,

            "tem_chuva":
                1 if precipitation > 0 else 0,

            "tem_curva": 0,

            "pista_simples": 0,

            "pessoas": 1,

            "temperature_2m": temperature,

            "precipitation": precipitation,

            "wind_speed_10m": wind

        }



        X = pd.DataFrame(
            [payload]
        )


        X = X.reindex(

            columns=features,

            fill_value=0

        )



        probability = float(

            model.predict_proba(X)[:,1][0]

        )



        risk = classify_risk(
            probability
        )



        insert_current_risk({

            "km_faixa_label":
                row["km_faixa_label"],

            "temperature_2m":
                temperature,

            "precipitation":
                precipitation,

            "wind_speed_10m":
                wind,

            "hora":
                hora,

            "periodo_noturno":
                periodo_noturno,

            "probability":
                probability,

            "risk_class":
                risk

        })



        results.append({

            "km":
                row["km_faixa_label"],

            "temperature":
                temperature,

            "rain":
                precipitation,

            "wind":
                wind,

            "probability":
                probability,

            "risk":
                risk

        })



    print("\n===== RISCO ATUAL =====")


    for item in results:

        print(item)



if __name__ == "__main__":

    predict_current_risk()
