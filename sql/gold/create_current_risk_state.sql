CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.current_risk_state (
    km_faixa_label TEXT PRIMARY KEY,
    temperature_2m NUMERIC,
    precipitation NUMERIC,
    wind_speed_10m NUMERIC,
    hora INTEGER,
    periodo_noturno INTEGER,
    probability NUMERIC,
    risk_class TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

