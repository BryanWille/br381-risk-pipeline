import logging

import requests
from prefect import get_run_logger
from prefect.blocks.system import Secret


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        return logging.getLogger(__name__)


def get_telegram_credentials():
    logger = _get_logger()
    logger.info("Carregando credenciais do Telegram a partir de Prefect Secret blocks.")

    token = Secret.load("telegram-token").get()
    chat_id = Secret.load("telegram-chat-id").get()

    logger.info("Credenciais do Telegram carregadas com sucesso.")
    return token, chat_id


def send_telegram_message(message):
    logger = _get_logger()
    logger.info("Preparando envio de mensagem para o Telegram.")

    token, chat_id = get_telegram_credentials()

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }

    logger.info(
        f"Enviando mensagem ao Telegram para chat configurado. Tamanho da mensagem: {len(message)} caracteres."
    )

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30,
        )

        logger.info(f"Resposta HTTP recebida do Telegram com status code {response.status_code}.")
        response.raise_for_status()
        logger.info("Mensagem enviada ao Telegram com sucesso.")

    except requests.RequestException:
        logger.exception("Falha ao enviar mensagem para o Telegram.")
        raise