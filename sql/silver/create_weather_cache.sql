-- Cria tabela silver.weather_cache para guardar previsoes/observacoes de clima
CREATE SCHEMA IF NOT EXISTS silver;

CREATE TABLE IF NOT EXISTS silver.weather_cache (
    id SERIAL PRIMARY KEY,
    latitude NUMERIC NOT NULL,
    longitude NUMERIC NOT NULL,
    data DATE NOT NULL,
    hora INTEGER NOT NULL,
    temperature_2m NUMERIC,
    precipitation NUMERIC,
    wind_speed_10m NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    UNIQUE(latitude, longitude, data, hora)
);
