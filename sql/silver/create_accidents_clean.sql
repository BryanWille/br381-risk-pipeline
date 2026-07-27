CREATE TABLE IF NOT EXISTS silver.accidents_clean (

    id BIGINT PRIMARY KEY,

    data_acidente DATE,
    horario TIME,

    br INTEGER,
    km NUMERIC,

    km_inicio INTEGER,
    km_fim INTEGER,
    km_faixa_label TEXT,

    municipio TEXT,
    uf TEXT,

    causa_acidente TEXT,
    tipo_acidente TEXT,
    classificacao_acidente TEXT,

    fase_dia TEXT,
    sentido_via TEXT,
    condicao_metereologica TEXT,

    tipo_pista TEXT,
    tracado_via TEXT,
    uso_solo TEXT,

    pessoas INTEGER,
    mortos INTEGER,
    feridos_leves INTEGER,
    feridos_graves INTEGER,
    feridos INTEGER,

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    _processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
