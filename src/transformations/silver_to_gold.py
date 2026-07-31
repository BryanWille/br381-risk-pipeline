import logging

from prefect import get_run_logger

from src.database.connection import get_connection


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def create_risk_aggregates():
    logger = _get_logger()
    logger.info("Iniciando criação dos agregados de risco por faixa de km na Gold.")

    conn = get_connection()
    cur = conn.cursor()

    sql = """
    INSERT INTO gold.km_risk_aggregates (
        km_faixa_label,
        acidentes_total,
        acidentes_graves,
        total_mortos,
        total_feridos_graves,
        taxa_gravidade,
        indice_risco
    )
    SELECT
        km_faixa_label,
        COUNT(*) AS acidentes_total,
        COUNT(*) FILTER (
            WHERE mortos > 0
               OR feridos_graves > 0
        ) AS acidentes_graves,
        COALESCE(SUM(mortos), 0),
        COALESCE(SUM(feridos_graves), 0),
        ROUND(
            COUNT(*) FILTER (
                WHERE mortos > 0
                   OR feridos_graves > 0
            )::numeric
            /
            NULLIF(COUNT(*)::numeric, 0),
            4
        ),
        ROUND(
            (
                COALESCE(SUM(mortos), 0) * 10
                +
                COALESCE(SUM(feridos_graves), 0) * 3
                +
                COUNT(*) * 0.1
            )::numeric,
            2
        )
    FROM silver.accidents_clean
    GROUP BY km_faixa_label
    ON CONFLICT (km_faixa_label)
    DO UPDATE SET
        acidentes_total = EXCLUDED.acidentes_total,
        acidentes_graves = EXCLUDED.acidentes_graves,
        total_mortos = EXCLUDED.total_mortos,
        total_feridos_graves = EXCLUDED.total_feridos_graves,
        taxa_gravidade = EXCLUDED.taxa_gravidade,
        indice_risco = EXCLUDED.indice_risco;
    """

    try:
        logger.info("Executando SQL de consolidação dos agregados de risco.")
        cur.execute(sql)

        affected = cur.rowcount
        conn.commit()

        logger.info(f"{affected} faixa(s) de km inserida(s)/atualizada(s) em gold.km_risk_aggregates.")
        logger.info("Commit realizado com sucesso na atualização dos agregados de risco.")

    except Exception:
        conn.rollback()
        logger.exception("Erro ao criar agregados de risco na Gold. Rollback executado.")
        raise

    finally:
        cur.close()
        conn.close()
        logger.info("Conexão com banco encerrada após criação dos agregados de risco.")