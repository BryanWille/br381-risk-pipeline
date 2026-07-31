import logging

from prefect import get_run_logger

from src.database.connection import get_connection


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def create_ml_features():
    logger = _get_logger()
    logger.info("Iniciando criação da base de features para Machine Learning.")

    conn = get_connection()
    cur = conn.cursor()

    sql = """
    INSERT INTO gold.ml_accident_features (
        id,
        data_acidente,
        horario,
        br,
        km,
        km_inicio,
        km_fim,
        km_faixa_label,
        municipio,
        causa_acidente,
        tipo_acidente,
        fase_dia,
        sentido_via,
        tipo_pista,
        tracado_via,
        condicao_metereologica,
        pessoas,
        mortos,
        feridos_graves,
        acidente_grave,
        hora,
        periodo_noturno,
        tem_chuva,
        tem_curva,
        pista_simples,
        temperature_2m,
        precipitation,
        wind_speed_10m
    )
    SELECT
        a.id,
        a.data_acidente,
        a.horario,
        a.br,
        a.km,
        a.km_inicio,
        a.km_fim,
        a.km_faixa_label,
        a.municipio,
        a.causa_acidente,
        a.tipo_acidente,
        a.fase_dia,
        a.sentido_via,
        a.tipo_pista,
        a.tracado_via,
        a.condicao_metereologica,
        a.pessoas,
        a.mortos,
        a.feridos_graves,
        CASE
            WHEN a.mortos > 0
              OR a.feridos_graves > 0
            THEN 1
            ELSE 0
        END,
        EXTRACT(HOUR FROM a.horario),
        CASE
            WHEN a.fase_dia = 'Plena Noite'
            THEN 1
            ELSE 0
        END,
        CASE
            WHEN a.condicao_metereologica ILIKE '%Chuva%'
            THEN 1
            ELSE 0
        END,
        CASE
            WHEN a.tracado_via ILIKE '%Curva%'
            THEN 1
            ELSE 0
        END,
        CASE
            WHEN a.tipo_pista = 'Simples'
            THEN 1
            ELSE 0
        END,
        w.temperature_2m,
        w.precipitation,
        w.wind_speed_10m
    FROM silver.accidents_clean a
    LEFT JOIN silver.accidents_weather_enriched w
        ON a.id = w.id
    ON CONFLICT (id)
    DO UPDATE SET
        acidente_grave = EXCLUDED.acidente_grave,
        hora = EXCLUDED.hora,
        periodo_noturno = EXCLUDED.periodo_noturno,
        tem_chuva = EXCLUDED.tem_chuva,
        tem_curva = EXCLUDED.tem_curva,
        pista_simples = EXCLUDED.pista_simples,
        temperature_2m = EXCLUDED.temperature_2m,
        precipitation = EXCLUDED.precipitation,
        wind_speed_10m = EXCLUDED.wind_speed_10m;
    """

    try:
        logger.info("Executando SQL de criação/atualização das features de ML.")
        cur.execute(sql)

        affected = cur.rowcount
        conn.commit()

        logger.info(f"{affected} registro(s) preparado(s)/atualizado(s) para ML.")
        logger.info("Commit realizado com sucesso na tabela gold.ml_accident_features.")

    except Exception:
        conn.rollback()
        logger.exception("Erro ao criar features de ML. Rollback executado.")
        raise

    finally:
        cur.close()
        conn.close()
        logger.info("Conexão com banco encerrada após criação das features de ML.")