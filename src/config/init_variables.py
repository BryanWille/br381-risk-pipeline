from prefect.variables import Variable

DEFAULTS = {
    "high_risk_threshold": 0.35,
    "medium_risk_threshold": 0.15,
    "telegram_alert_threshold": 0.60,
    "telegram_alert_enabled": True,
    "hotspots_limit": 10,
}

def init_variables():
    for key, value in DEFAULTS.items():
        try:
            Variable.set(key, value, overwrite=False)
        except ValueError:
            pass