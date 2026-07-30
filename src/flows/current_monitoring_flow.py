from prefect import flow

from src.flows.create_hotspots_flow import create_hotspots_flow
from src.flows.current_risk_flow import current_risk_flow
from src.flows.alert_flow import risk_alert_flow


@flow(
    name="current-monitoring",
    retries=2,
    retry_delay_seconds=30
)
def current_monitoring():

    print("Atualizando hotspots")
    create_hotspots_flow()

    print("Calculando risco atual")
    current_risk_flow()

    print("Enviando alertas")
    risk_alert_flow()


if __name__ == "__main__":
    current_monitoring()