from pathlib import Path
import logging

import joblib
import pandas as pd
from prefect import get_run_logger
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


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def load_dataset():
    logger = _get_logger()
    logger.info("Carregando dataset de treinamento do banco.")

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

    try:
        df = pd.read_sql(query, conn)
        logger.info(f"Dataset carregado com sucesso. {len(df)} registro(s) encontrados.")
        return df
    finally:
        conn.close()
        logger.info("Conexão com banco encerrada após carregamento do dataset.")


def prepare_features(df):
    logger = _get_logger()
    logger.info("Preparando features e target para treinamento.")

    y = df["acidente_grave"]
    X = df.drop(columns=["acidente_grave"])

    categorical = [
        "municipio",
        "causa_acidente",
        "tipo_acidente",
        "fase_dia",
        "sentido_via",
        "tipo_pista",
        "tracado_via",
    ]

    X = pd.get_dummies(
        X,
        columns=categorical,
        dummy_na=True,
    )

    logger.info(f"Features preparadas com sucesso. Shape final: {X.shape}.")
    return X, y


def train():
    logger = _get_logger()
    logger.info("Iniciando treinamento do modelo de risco.")

    try:
        logger.info("Carregando dados de treinamento.")
        df = load_dataset()

        logger.info(f"Dataset bruto recebido com {len(df)} registro(s).")

        if df.empty:
            logger.warning("Dataset vazio. Treinamento será interrompido.")
            return

        X, y = prepare_features(df)

        logger.info("Separando dados em treino e teste.")
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y,
        )

        logger.info(f"Conjunto de treino: {len(X_train)} registro(s).")
        logger.info(f"Conjunto de teste: {len(X_test)} registro(s).")

        model = RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",
            max_depth=12,
        )

        logger.info("Treinando modelo RandomForestClassifier.")
        model.fit(X_train, y_train)
        logger.info("Treinamento concluído com sucesso.")

        probabilities = model.predict_proba(X_test)[:, 1]
        threshold = 0.35
        predictions = (probabilities >= threshold).astype(int)

        logger.info("Calculando métricas de avaliação.")
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions)
        recall = recall_score(y_test, predictions)
        f1 = f1_score(y_test, predictions)
        roc_auc = roc_auc_score(y_test, probabilities)

        logger.info(f"Threshold adotado: {threshold}")
        logger.info(f"Accuracy: {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall: {recall:.4f}")
        logger.info(f"F1 Score: {f1:.4f}")
        logger.info(f"ROC AUC: {roc_auc:.4f}")

        logger.info("Gerando matriz de confusão.")
        logger.info(f"\n{confusion_matrix(y_test, predictions)}")

        logger.info("Gerando classification report.")
        logger.info(f"\n{classification_report(y_test, predictions)}")

        logger.info("Calculando top features mais importantes.")
        importance = (
            pd.DataFrame(
                {
                    "feature": X.columns,
                    "importance": model.feature_importances_,
                }
            )
            .sort_values("importance", ascending=False)
            .head(20)
        )

        logger.info("Top 20 features:")
        for _, row in importance.iterrows():
            logger.info(f"{row['feature']}: {row['importance']:.6f}")

        Path("models").mkdir(exist_ok=True)

        model_path = "models/risk_model.joblib"
        joblib.dump(
            {
                "model": model,
                "features": X.columns.tolist(),
                "threshold": threshold,
            },
            model_path,
        )

        logger.info(f"Modelo salvo com sucesso em {model_path}.")

    except Exception:
        logger.exception("Erro durante o treinamento do modelo de risco.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train()