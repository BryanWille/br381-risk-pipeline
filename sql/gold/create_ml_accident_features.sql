CREATE TABLE
    IF NOT EXISTS gold.ml_accident_features (
        id BIGINT PRIMARY KEY,
        data_acidente DATE,
        horario TIME,
        br INTEGER,
        km NUMERIC,
        km_inicio INTEGER,
        km_fim INTEGER,
        km_faixa_label TEXT,
        municipio TEXT,
        causa_acidente TEXT,
        tipo_acidente TEXT,
        fase_dia TEXT,
        sentido_via TEXT,
        tipo_pista TEXT,
        tracado_via TEXT,
        condicao_metereologica TEXT,
        pessoas INTEGER,
        mortos INTEGER,
        feridos_graves INTEGER,
        -- target do modelo
        acidente_grave INTEGER,
        -- features derivadas
        hora INTEGER,
        periodo_noturno INTEGER,
        tem_chuva INTEGER,
        tem_curva INTEGER,
        pista_simples INTEGER,
        _created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );