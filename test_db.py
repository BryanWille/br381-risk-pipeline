from src.database.init_db import create_schemas
from src.database.create_bronze import create_prf_table

create_schemas()
create_prf_table()

print("Banco inicializado com sucesso.")
