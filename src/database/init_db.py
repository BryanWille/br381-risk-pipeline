from src.database.database_initializer import DatabaseInitializer


def initialize_db(sql_path: str = "sql"):
    """Inicializa o banco executando todos os arquivos SQL listados pelo DatabaseInitializer.

    Usa `sql_path` como diretório base para localizar os arquivos SQL (padrão: `sql`).
    """
    initializer = DatabaseInitializer(sql_path=sql_path)
    initializer.initialize()


if __name__ == "__main__":
    # Execução direta: inicializa o banco a partir da raiz do projeto
    initialize_db()
