CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.alert_history (
    id BIGSERIAL PRIMARY KEY,
    km_faixa_label TEXT,
    probability NUMERIC,
    risk_class TEXT,
    alert_hash TEXT,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_alert_history_alert_hash ON gold.alert_history (alert_hash);
CREATE INDEX IF NOT EXISTS idx_alert_history_sent_at ON gold.alert_history (sent_at DESC);