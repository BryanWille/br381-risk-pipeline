from prefect.variables import Variable


def get_high_risk_threshold():

    return float(
        Variable.get(
            "high_risk_threshold",
            default=0.35
        )
    )



def get_medium_risk_threshold():

    return float(
        Variable.get(
            "medium_risk_threshold",
            default=0.15
        )
    )



def get_telegram_alert_threshold():

    return float(
        Variable.get(
            "telegram_alert_threshold",
            default=0.60
        )
    )



def get_telegram_alert_enabled():

    value = Variable.get(
        "telegram_alert_enabled",
        default=True
    )

    return bool(value)



def get_hotspots_limit():

    value = Variable.get(
        "hotspots_limit",
        default=10
    )

    return int(value)