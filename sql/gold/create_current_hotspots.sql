-- Cria tabela gold.current_hotspots para armazenar hotspots atuais
CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.current_hotspots (
    hotspot_id SERIAL PRIMARY KEY,
    km_faixa_label TEXT NOT NULL,
    ranking INTEGER,
    indice_risco NUMERIC,
    acidentes_total INTEGER DEFAULT 0,
    acidentes_graves INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_current_hotspots_km_label ON gold.current_hotspots (km_faixa_label);
