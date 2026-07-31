import logging

from prefect import get_run_logger

from src.database.connection import get_connection
from src.database.weather_cache_repository import (
    get_weather_cache,
    save_weather_cache,
)
from src.database.weather_repository import insert_weather_accident
from src.weather.open_meteo import get_historical_weather


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def enrich_accidents_weather():
    logger = _get_logger()
    logger.info("Iniciando enriquecimento climático dos acidentes.")

    conn = get_connection()
    cur = conn.cursor()

    try:
        logger.info("Consultando registros da tabela silver.accidents_clean.")
        cur.execute(
            """
            SELECT *
            FROM silver.accidents_clean
            """
        )

        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()

        logger.info(f"{len(rows)} acidente(s) carregado(s) para enriquecimento climático.")

        total = 0
        cache_hits = 0
        api_calls = 0
        weather_missing = 0

        for row in rows:
            accident = dict(zip(columns, row))

            accident_id = accident["id"]
            latitude = round(float(accident["latitude"]), 3)
            longitude = round(float(accident["longitude"]), 3)
            data = accident["data_acidente"]
            hour = accident["horario"].hour

            logger.info(
                f"Processando enriquecimento do acidente id={accident_id}, "
                f"lat={latitude}, lon={longitude}, data={data}, hora={hour}."
            )

            weather = get_weather_cache(latitude, longitude, data, hour)

            if weather:
                cache_hits += 1
                logger.info(f"Cache hit para acidente id={accident_id}.")

                temperature = weather["temperature_2m"]
                precipitation = weather["precipitation"]
                wind = weather["wind_speed_10m"]
            else:
                api_calls += 1
                logger.info(f"Cache miss para acidente id={accident_id}. Consultando Open-Meteo.")

                response = get_historical_weather(
                    latitude,
                    longitude,
                    data.strftime("%Y-%m-%d"),
                )

                if response is None:
                    weather_missing += 1
                    logger.warning(f"Sem dados climáticos para acidente id={accident_id}. Registro será ignorado.")
                    continue

                temperature = response["hourly"]["temperature_2m"][hour]
                precipitation = response["hourly"]["precipitation"][hour]
                wind = response["hourly"]["wind_speed_10m"][hour]

                logger.info(
                    f"Clima obtido via API para acidente id={accident_id}: "
                    f"temperatura={temperature}, precipitação={precipitation}, vento={wind}."
                )

                save_weather_cache(
                    latitude,
                    longitude,
                    data,
                    hour,
                    temperature,
                    precipitation,
                    wind,
                )
                logger.info(f"Clima salvo em cache para acidente id={accident_id}.")

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
                "wind_speed_10m": wind,
            }

            insert_weather_accident(payload)
            total += 1

            logger.info(f"Acidente id={accident_id} enriquecido e persistido com sucesso.")

        logger.info(
            f"Enriquecimento climático concluído. "
            f"Total enriquecido(s): {total} | "
            f"cache hit(s): {cache_hits} | "
            f"chamada(s) API: {api_calls} | "
            f"sem clima: {weather_missing}"
        )

    except Exception:
        logger.exception("Erro durante o enriquecimento climático dos acidentes.")
        raise

    finally:
        cur.close()
        conn.close()
        logger.info("Conexão com banco encerrada após enriquecimento climático.")