import requests

from prefect.blocks.system import Secret



def get_telegram_credentials():

    token = Secret.load(
        "telegram-token"
    ).get()


    chat_id = Secret.load(
        "telegram-chat-id"
    ).get()


    return token, chat_id



def send_telegram_message(message):

    token, chat_id = get_telegram_credentials()


    url = (
        f"https://api.telegram.org/"
        f"bot{token}/sendMessage"
    )


    payload = {

        "chat_id": chat_id,

        "text": message,

        "parse_mode": "HTML"

    }


    response = requests.post(
        url,
        json=payload,
        timeout=30
    )


    response.raise_for_status()