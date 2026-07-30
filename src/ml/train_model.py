from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from src.database.connection import get_connection


def load_dataset():

    conn = get_connection()

    query = """
        SELECT

        km,
        hora,
        periodo_noturno,
        tem_chuva,
        tem_curva,
        pista_simples,
        pessoas,

        temperature_2m,
        precipitation,
        wind_speed_10m,

        municipio,
        causa_acidente,
        tipo_acidente,
        fase_dia,
        sentido_via,
        tipo_pista,
        tracado_via,

        acidente_grave

        FROM gold.ml_accident_features
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def prepare_features(df):

    y = df["acidente_grave"]

    X = df.drop(
        columns=["acidente_grave"]
    )

    categorical = [
        "municipio",
        "causa_acidente",
        "tipo_acidente",
        "fase_dia",
        "sentido_via",
        "tipo_pista",
        "tracado_via"
    ]


    X = pd.get_dummies(
        X,
        columns=categorical,
        dummy_na=True
    )


    return X, y



def train():

    print("Carregando dados...")

    df = load_dataset()

    print(
        f"Dataset: {len(df)} registros"
    )


    X, y = prepare_features(df)


    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.20,

        random_state=42,

        stratify=y
    )


    print(f"Treino: {len(X_train)} registros")
    print(f"Teste : {len(X_test)} registros")


    model = RandomForestClassifier(

        n_estimators=300,

        random_state=42,

        n_jobs=-1,

        class_weight="balanced",

        max_depth=12
    )


    print("\nTreinando modelo...")


    model.fit(
        X_train,
        y_train
    )



    probabilities = model.predict_proba(
        X_test
    )[:,1]


    threshold = 0.35


    predictions = (
        probabilities >= threshold
    ).astype(int)

    print("\n===== MÉTRICAS =====")

    print(f"threshold {threshold}")

    print(
        f"Accuracy : {accuracy_score(y_test, predictions):.4f}"
    )

    print(
        f"Precision: {precision_score(y_test, predictions):.4f}"
    )

    print(
        f"Recall   : {recall_score(y_test, predictions):.4f}"
    )

    print(
        f"F1 Score : {f1_score(y_test, predictions):.4f}"
    )

    print(
        f"ROC AUC  : {roc_auc_score(y_test, probabilities):.4f}"
    )


    print("\n===== MATRIZ DE CONFUSÃO =====")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


    print("\n===== CLASSIFICATION REPORT =====")

    print(
        classification_report(
            y_test,
            predictions
        )
    )


    print("\n===== TOP FEATURES =====")


    importance = (

        pd.DataFrame({

            "feature": X.columns,

            "importance": model.feature_importances_

        })

        .sort_values(
            "importance",
            ascending=False
        )

        .head(20)

    )


    print(importance)


    Path("models").mkdir(
        exist_ok=True
    )


    joblib.dump(
        {
            "model": model,
            "features": X.columns.tolist(),
            "threshold": 0.35
        },
        "models/risk_model.joblib"
    )


    print(
        "\nModelo salvo em models/risk_model.joblib"
    )


if __name__ == "__main__":
    train()
