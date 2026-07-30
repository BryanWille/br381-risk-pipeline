from prefect import flow

from src.alerts.risk_alert import check_high_risk_alerts



@flow(name="risk-alert")
def risk_alert_flow():

    check_high_risk_alerts()



if __name__ == "__main__":

    risk_alert_flow()
