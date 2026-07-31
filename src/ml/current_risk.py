import logging
from datetime import datetime

import joblib
import pandas as pd
from prefect import get_run_logger

from src.config.risk_config import (
    get_high_risk_threshold,
    get_medium_risk_threshold,
)
from src.database.connection import get_connection
from src.database.current_risk_repository import insert_current_risk
from src.weather.open_meteo import get_current_weather


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def get_current_hotspots():
    logger = _get_logger()
    logger.info("Buscando hotspots atuais para análise de risco.")

    conn = get_connection()

    query = """
        SELECT
            h.km_faixa_label,
            AVG(a.latitude) AS latitude,
            AVG(a.longitude) AS longitude,
            AVG(a.km) AS km,
            AVG(m.pessoas) AS pessoas,
            MAX(m.tem_curva) AS tem_curva,
            MAX(m.pista_simples) AS pista_simples
        FROM gold.current_hotspots h
        JOIN silver.accidents_clean a
            ON a.km_faixa_label = h.km_faixa_label
        JOIN gold.ml_accident_features m
            ON m.id = a.id
        GROUP BY
            h.km_faixa_label,
            h.indice_risco
        ORDER BY h.indice_risco DESC
        LIMIT 10
    """

    try:
        df = pd.read_sql(query, conn)
        logger.info(f"Consulta de hotspots concluída com sucesso. {len(df)} registro(s) carregado(s).")
        return df
    finally:
        conn.close()
        logger.info("Conexão com banco encerrada após leitura de hotspots.")


def classify_risk(probability):
    high_threshold = get_high_risk_threshold()
    medium_threshold = get_medium_risk_threshold()

    if probability >= high_threshold:
        return "ALTO"
    elif probability >= medium_threshold:
        return "MEDIO"

    return "BAIXO"


def get_current_time_features():
    logger = _get_logger()

    now = datetime.now()
    hora = now.hour
    periodo_noturno = 1 if hora >= 18 or hora < 6 else 0

    logger.info(
        f"Features temporais calculadas. Hora atual: {hora}. Período noturno: {periodo_noturno}."
    )

    return hora, periodo_noturno


def predict_current_risk():
    logger = _get_logger()
    logger.info("Iniciando predição de risco atual.")

    try:
        logger.info("Carregando modelo de risco a partir de models/risk_model.joblib.")
        model_data = joblib.load("models/risk_model.joblib")

        model = model_data["model"]
        features = model_data["features"]

        logger.info(f"Modelo carregado com sucesso. Total de features esperadas: {len(features)}.")

        hotspots = get_current_hotspots()
        hora, periodo_noturno = get_current_time_features()

        logger.info(f"Hotspots analisados nesta execução: {len(hotspots)}.")

        if hotspots.empty:
            logger.warning("Nenhum hotspot encontrado para análise de risco atual.")
            return

        results = []

        for _, row in hotspots.iterrows():
            km_label = row["km_faixa_label"]
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])

            logger.info(f"Iniciando análise do hotspot {km_label}.")
            logger.info(f"Consultando clima atual para latitude={latitude}, longitude={longitude}.")

            weather = get_current_weather(latitude, longitude)

            if weather:
                current = weather["current"]
                temperature = current["temperature_2m"]
                precipitation = current["precipitation"]
                wind = current["wind_speed_10m"]

                logger.info(
                    f"Clima obtido com sucesso para {km_label}: "
                    f"temperatura={temperature}, precipitação={precipitation}, vento={wind}."
                )
            else:
                temperature = 25
                precipitation = 0
                wind = 0

                logger.warning(
                    f"Clima indisponível para {km_label}. Aplicando valores padrão: "
                    f"temperatura=25, precipitação=0, vento=0."
                )

            payload = {
                "km": float(row["km"]),
                "hora": hora,
                "periodo_noturno": periodo_noturno,
                "tem_chuva": 1 if precipitation > 0 else 0,
                "tem_curva": int(row["tem_curva"]),
                "pista_simples": int(row["pista_simples"]),
                "pessoas": float(row["pessoas"]),
                "temperature_2m": temperature,
                "precipitation": precipitation,
                "wind_speed_10m": wind,
            }

            logger.info(f"Payload de features montado para {km_label}.")

            X = pd.DataFrame([payload])
            X = X.reindex(columns=features, fill_value=0)

            logger.info(f"DataFrame de features alinhado ao modelo para {km_label}.")

            probability = float(model.predict_proba(X)[:, 1][0])
            risk = classify_risk(probability)

            logger.info(
                f"Predição concluída para {km_label}: probabilidade={probability:.2%}, classe={risk}."
            )

            insert_current_risk(
                {
                    "km_faixa_label": km_label,
                    "temperature_2m": temperature,
                    "precipitation": precipitation,
                    "wind_speed_10m": wind,
                    "hora": hora,
                    "periodo_noturno": periodo_noturno,
                    "probability": probability,
                    "risk_class": risk,
                }
            )

            logger.info(f"Resultado de risco atual persistido com sucesso para {km_label}.")

            results.append(
                {
                    "km": km_label,
                    "temperature": temperature,
                    "rain": precipitation,
                    "wind": wind,
                    "probability": probability,
                    "risk": risk,
                }
            )

        logger.info("Resumo final da predição de risco atual:")
        for item in results:
            logger.info(
                f"KM={item['km']} | temp={item['temperature']} | chuva={item['rain']} | "
                f"vento={item['wind']} | prob={item['probability']:.2%} | risco={item['risk']}"
            )

        logger.info(f"Predição de risco atual finalizada com sucesso. {len(results)} hotspot(s) processado(s).")

    except Exception:
        logger.exception("Erro durante a predição de risco atual.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    predict_current_risk()