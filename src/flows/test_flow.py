import logging

from prefect import flow, task, get_run_logger


@task
def hello():
    logger = get_run_logger()
    message = "BR381 pipeline iniciado"
    logger.info(message)
    return message


@flow(name="br381-test-flow", log_prints=True)
def br381_flow():
    logger = get_run_logger()
    logger.info("Iniciando flow br381-test-flow.")

    try:
        result = hello()
        logger.info(f"Resultado da task hello: {result}")
        logger.info("Flow br381-test-flow concluído com sucesso.")

    except Exception:
        logger.exception("Erro no flow br381-test-flow.")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    br381_flow()