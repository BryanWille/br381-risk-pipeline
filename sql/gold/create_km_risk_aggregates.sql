CREATE TABLE IF NOT EXISTS gold.km_risk_aggregates (

    km_faixa_label TEXT PRIMARY KEY,

    acidentes_total INTEGER,

    acidentes_graves INTEGER,

    total_mortos INTEGER,

    total_feridos_graves INTEGER,

    taxa_gravidade NUMERIC,

    indice_risco NUMERIC,

    _created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
