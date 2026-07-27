from src.ingestion.prf_loader import load_csv

df = load_csv("data/raw/prf_accidentes_2026.csv")

print(df.head())
print()
print(df.dtypes)
print()
print(df.shape)
