import logging
from collections import Counter

import joblib
import pandas as pd
from prefect import get_run_logger

from src.config.risk_config import (
    get_high_risk_threshold,
    get_medium_risk_threshold,
)
from src.database.connection import get_connection
from src.database.risk_repository import insert_risk_prediction


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def load_features():
    logger = _get_logger()
    logger.info("Carregando dados de features para predição histórica de risco.")

    conn = get_connection()

    query = """
    SELECT
        m.*
    FROM gold.ml_accident_features m
    JOIN gold.current_hotspots h
        ON m.km_faixa_label = h.km_faixa_label
    """

    try:
        df = pd.read_sql(query, conn)
        logger.info(f"Leitura de features concluída com sucesso. {len(df)} registro(s) carregado(s).")
        return df
    finally:
        conn.close()
        logger.info("Conexão com banco encerrada após carregamento das features.")


def prepare_features(df, features):
    logger = _get_logger()
    logger.info("Iniciando preparação das features para inferência.")

    categorical = [
        "municipio",
        "causa_acidente",
        "tipo_acidente",
        "fase_dia",
        "sentido_via",
        "tipo_pista",
        "tracado_via",
    ]

    X = df.drop(columns=["acidente_grave"])
    logger.info("Coluna alvo 'acidente_grave' removida da matriz de entrada.")

    X = pd.get_dummies(
        X,
        columns=categorical,
        dummy_na=True,
    )
    logger.info("Encoding categórico concluído com pd.get_dummies.")

    X = X.reindex(
        columns=features,
        fill_value=0,
    )
    logger.info(
        f"Features alinhadas ao modelo com sucesso. Matriz final com shape {X.shape}."
    )

    return X


def classify_risk(probability):
    high_threshold = get_high_risk_threshold()
    medium_threshold = get_medium_risk_threshold()

    if probability >= high_threshold:
        return "ALTO"
    elif probability >= medium_threshold:
        return "MEDIO"
    else:
        return "BAIXO"


def predict_risk():
    logger = _get_logger()
    logger.info("Iniciando predição histórica de risco.")

    try:
        logger.info("Carregando modelo a partir de models/risk_model.joblib.")
        model_data = joblib.load("models/risk_model.joblib")

        model = model_data["model"]
        features = model_data["features"]
        threshold = model_data.get("threshold", get_high_risk_threshold())

        logger.info(f"Modelo carregado com sucesso. Total de features esperadas: {len(features)}.")
        logger.info(f"Threshold armazenado no artefato/modelo: {threshold}")

        logger.info("Carregando base para previsão.")
        df = load_features()

        logger.info(f"Registros disponíveis para previsão: {len(df)}.")

        if df.empty:
            logger.warning("Nenhum registro disponível para predição histórica.")
            return

        X = prepare_features(df, features)

        logger.info("Executando previsão de probabilidades.")
        probabilities = model.predict_proba(X)[:, 1]
        logger.info("Predição concluída com sucesso.")

        total = 0
        classes = Counter()

        for (_, row), probability in zip(df.iterrows(), probabilities):
            probability = float(probability)
            risk = classify_risk(probability)

            logger.info(
                f"Persistindo previsão para id={int(row['id'])}, km={float(row['km'])}, "
                f"município={row['municipio']}, probabilidade={probability:.2%}, classe={risk}."
            )

            insert_risk_prediction(
                {
                    "id": int(row["id"]),
                    "km": float(row["km"]),
                    "municipio": row["municipio"],
                    "probability": probability,
                    "risk_class": risk,
                }
            )

            classes[risk] += 1
            total += 1

        logger.info(f"{total} previsão(ões) gerada(s) com sucesso.")
        logger.info("Distribuição final das classes de risco:")

        for risk, count in classes.items():
            logger.info(f"{risk}: {count}")

        logger.info("Predição histórica de risco finalizada com sucesso.")

    except Exception:
        logger.exception("Erro durante a predição histórica de risco.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    predict_risk()