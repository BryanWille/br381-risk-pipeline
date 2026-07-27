CREATE TABLE IF NOT EXISTS silver.accidents_weather_enriched (

    id BIGINT PRIMARY KEY,

    data_acidente DATE,
    horario TIME,

    br INTEGER,
    km NUMERIC,
    km_faixa_label TEXT,

    latitude NUMERIC,
    longitude NUMERIC,

    municipio TEXT,

    causa_acidente TEXT,
    tipo_acidente TEXT,
    classificacao_acidente TEXT,

    fase_dia TEXT,
    tipo_pista TEXT,
    tracado_via TEXT,

    mortos INTEGER,
    feridos_graves INTEGER,

    acidente_grave INTEGER,

    temperature_2m NUMERIC,
    precipitation NUMERIC,
    wind_speed_10m NUMERIC,

    weather_source TEXT DEFAULT 'open-meteo',

    _created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
