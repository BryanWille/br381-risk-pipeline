CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.risk_predictions (
    id BIGINT PRIMARY KEY,
    km NUMERIC,
    municipio TEXT,
    probability NUMERIC,
    risk_class TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_risk_predictions_probability ON gold.risk_predictions (probability DESC);