import hashlib

from src.database.alert_repository import (
    alert_already_sent,
    save_alert
)


def build_alert_hash(
    km,
    probability,
    risk
):

    text = f"{km}|{risk}|{round(probability,2)}"

    return hashlib.sha256(
        text.encode()
    ).hexdigest()


def should_send_alert(
    km,
    probability,
    risk
):

    alert_hash = build_alert_hash(
        km,
        probability,
        risk
    )

    if alert_already_sent(alert_hash):
        return False

    save_alert(
        km,
        probability,
        risk,
        alert_hash
    )

    return True
