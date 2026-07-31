import logging

from prefect import get_run_logger

from src.config.risk_config import get_hotspots_limit
from src.database.connection import get_connection


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def create_hotspots():
    logger = _get_logger()
    logger.info("Iniciando atualização da tabela gold.current_hotspots.")

    limit = get_hotspots_limit()
    logger.info(f"Limite de hotspots configurado: {limit}")

    conn = get_connection()
    cur = conn.cursor()

    sql = f"""
    TRUNCATE gold.current_hotspots;

    INSERT INTO gold.current_hotspots (
        km_faixa_label,
        ranking,
        indice_risco,
        acidentes_total,
        acidentes_graves
    )
    SELECT
        km_faixa_label,
        ROW_NUMBER() OVER(
            ORDER BY indice_risco DESC
        ),
        indice_risco,
        acidentes_total,
        acidentes_graves
    FROM gold.km_risk_aggregates
    ORDER BY indice_risco DESC
    LIMIT {limit};
    """

    try:
        logger.info("Executando truncamento e recarga da tabela de hotspots.")
        cur.execute(sql)

        affected = cur.rowcount
        conn.commit()

        logger.info(f"{affected} hotspot(s) atualizado(s) com sucesso.")
        logger.info("Commit realizado com sucesso na atualização de hotspots.")

    except Exception:
        conn.rollback()
        logger.exception("Erro ao atualizar hotspots. Rollback executado.")
        raise

    finally:
        cur.close()
        conn.close()
        logger.info("Conexão com banco encerrada após atualização de hotspots.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_hotspots()