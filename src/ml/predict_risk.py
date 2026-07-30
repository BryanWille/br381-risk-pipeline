import joblib
import pandas as pd

from collections import Counter

from src.database.connection import get_connection
from src.database.risk_repository import insert_risk_prediction
from src.config.risk_config import (
    get_high_risk_threshold,
    get_medium_risk_threshold
)

def load_features():

    conn = get_connection()

    query = """
	SELECT
	    m.*
	FROM gold.ml_accident_features m

	JOIN gold.current_hotspots h

	ON m.km_faixa_label = h.km_faixa_label

    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    return df



def prepare_features(df, features):

    categorical = [

        "municipio",
        "causa_acidente",
        "tipo_acidente",
        "fase_dia",
        "sentido_via",
        "tipo_pista",
        "tracado_via"

    ]


    X = df.drop(
        columns=["acidente_grave"]
    )


    X = pd.get_dummies(
        X,
        columns=categorical,
        dummy_na=True
    )


    X = X.reindex(
        columns=features,
        fill_value=0
    )


    return X



def classify_risk(probability):

    if probability >= get_high_risk_threshold():

        return "ALTO"

    elif probability >= get_medium_risk_threshold():

        return "MEDIO"

    else:

        return "BAIXO"



def predict_risk():

    print("Carregando modelo...")


    model_data = joblib.load(
        "models/risk_model.joblib"
    )


    model = model_data["model"]

    features = model_data["features"]


    threshold = model_data.get(
        "threshold",
        get_high_risk_threshold()
    )


    print(
        f"Threshold utilizado: {threshold}"
    )


    print("Carregando dados...")


    df = load_features()


    print(
        f"Registros para previsão: {len(df)}"
    )


    X = prepare_features(
        df,
        features
    )


    print("Executando previsão...")


    probabilities = model.predict_proba(X)[:,1]


    total = 0

    classes = Counter()


    for index, row in df.iterrows():


        probability = float(
            probabilities[index]
        )


        risk = classify_risk(
            probability
        )


        insert_risk_prediction({

            "id": int(row["id"]),

            "km": float(row["km"]),

            "municipio": row["municipio"],

            "probability": probability,

            "risk_class": risk

        })


        classes[risk] += 1

        total += 1



    print(
        f"{total} previsões geradas"
    )


    print(
        "Distribuição:"
    )


    for risk, count in classes.items():

        print(
            f"{risk}: {count}"
        )



if __name__ == "__main__":

    predict_risk()
