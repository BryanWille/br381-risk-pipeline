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
            acidente_grave

        FROM gold.ml_accident_features
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def train():

    print("Carregando dados...")

    df = load_dataset()

    X = df.drop(columns=["acidente_grave"])

    y = df["acidente_grave"]

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
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
	class_weight="balanced"
    )

    print("\nTreinando modelo...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    print("\n===== MÉTRICAS =====")

    print(f"Accuracy : {accuracy_score(y_test, predictions):.4f}")
    print(f"Precision: {precision_score(y_test, predictions):.4f}")
    print(f"Recall   : {recall_score(y_test, predictions):.4f}")
    print(f"F1 Score : {f1_score(y_test, predictions):.4f}")
    print(f"ROC AUC  : {roc_auc_score(y_test, probabilities):.4f}")

    print("\n===== MATRIZ DE CONFUSÃO =====")
    print(confusion_matrix(y_test, predictions))

    print("\n===== CLASSIFICATION REPORT =====")
    print(classification_report(y_test, predictions))

    print("\n===== IMPORTÂNCIA DAS FEATURES =====")

    importance = (
        pd.DataFrame({
            "feature": X.columns,
            "importance": model.feature_importances_
        })
        .sort_values("importance", ascending=False)
    )

    print(importance)

    Path("models").mkdir(exist_ok=True)

    joblib.dump(model, "models/risk_model.joblib")

    print("\nModelo salvo em models/risk_model.joblib")


if __name__ == "__main__":
    train()
