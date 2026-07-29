from pathlib import Path

import pandas as pd

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
    df = pd.read_csv(
        csv_path,
        sep=";",
        encoding="iso-8859-1",
        dtype=str,
    )

    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(f"Colunas ausentes: {missing}")

    df["_source_file"] = Path(csv_path).name

    return df

from src.database.bronze_repository import insert_prf_accidents


def ingest_to_bronze(csv_path: str):

    df = load_csv(csv_path)

    columns = list(df.columns)

    values = list(
        df.itertuples(
            index=False,
            name=None
        )
    )

    inserted = insert_prf_accidents(
        columns,
        values
    )

    print(
        f"PRF Retornou: {len(values)} registros | "
        f"Novos inseridos: {inserted} | "
        f"Ignorados: {len(values) - inserted}"
    )
