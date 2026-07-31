-- Cria a tabela metadata.pipeline_runs para registrar execucoes de pipelines
CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS metadata.pipeline_runs (
    id SERIAL PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    finished_at TIMESTAMP WITH TIME ZONE,
    records_processed INTEGER,
    error_message TEXT
);

-- Indice por pipeline_name e started_at para consultas de historico
CREATE INDEX IF NOT EXISTS idx_pipeline_runs_name_started ON metadata.pipeline_runs(pipeline_name, started_at);
