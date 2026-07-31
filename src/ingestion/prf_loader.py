from pathlib import Path
import logging

import pandas as pd


logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = [
    "id",
    "data_inversa",
    "dia_semana",
    "horario",
    "uf",
    "br",
    "km",
    "municipio",
    "causa_acidente",
    "tipo_acidente",
    "classificacao_acidente",
    "fase_dia",
    "sentido_via",
    "condicao_metereologica",
    "tipo_pista",
    "tracado_via",
    "uso_solo",
    "pessoas",
    "mortos",
    "feridos_leves",
    "feridos_graves",
    "feridos",
    "ilesos",
    "ignorados",
    "veiculos",
    "latitude",
    "longitude",
    "regional",
    "delegacia",
    "uop",
]


def load_csv(csv_path: str) -> pd.DataFrame:
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    df = pd.read_csv(
        path,
        sep=";",
        encoding="iso-8859-1",
        dtype=str,
        keep_default_na=False,
    )

    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Colunas ausentes: {missing}")

    df = df[REQUIRED_COLUMNS].copy()
    df["_source_file"] = path.name

    return df


from src.database.bronze_repository import insert_prf_accidents


def ingest_to_bronze(csv_path: str):
    logger.info("Iniciando ingestão do arquivo %s", csv_path)

    df = load_csv(csv_path)

    columns = list(df.columns)
    values = list(df.itertuples(index=False, name=None))

    inserted = insert_prf_accidents(columns, values)

    logger.info(
        "PRF retornou %s registros | Novos inseridos: %s | Ignorados: %s",
        len(values),
        inserted,
        len(values) - inserted,
    )

    return inserted