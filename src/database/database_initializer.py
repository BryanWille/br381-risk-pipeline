from pathlib import Path

from src.database.connection import get_connection


class DatabaseInitializer:


    def __init__(self, sql_path="sql"):

        self.sql_path = Path(sql_path)



    def initialize(self):

        conn = get_connection()

        try:

            print("Criando schemas...")

            self.create_schemas(conn)


            print("Criando tabelas...")

            self.execute_files(
                conn,
                [

                    "metadata/create_pipeline_runs.sql",

                    "bronze/create_prf_accidents_raw.sql",

                    "silver/create_accidents_clean.sql",

                    "silver/create_accidents_weather_enriched.sql",

                    "gold/create_km_risk_aggregates.sql",

                    "gold/create_ml_accident_features.sql",
                    "gold/create_risk_predictions.sql",
                    "gold/create_current_risk_state.sql",
                    "gold/create_alert_history.sql",

                    "gold/create_current_hotspots.sql",
                    
                    "silver/create_weather_cache.sql",

                ]
            )


            conn.commit()

            print(
                "Banco inicializado com sucesso"
            )


        except Exception as e:

            conn.rollback()

            print(
                "Erro inicializando banco:",
                e
            )

            raise


        finally:

            conn.close()



    def create_schemas(self, conn):

        sql = """

        CREATE SCHEMA IF NOT EXISTS metadata;

        CREATE SCHEMA IF NOT EXISTS bronze;

        CREATE SCHEMA IF NOT EXISTS silver;

        CREATE SCHEMA IF NOT EXISTS gold;

        CREATE SCHEMA IF NOT EXISTS serving;

        """

        self.execute(
            conn,
            sql
        )



    def execute_files(self, conn, files):

        for filename in files:

            path = self.sql_path / filename


            if not path.exists():

                raise FileNotFoundError(
                    f"SQL não encontrado: {path}"
                )


            print(
                f"Executando {filename}"
            )


            sql = path.read_text()


            self.execute(
                conn,
                sql
            )



    def execute(self, conn, sql):

        with conn.cursor() as cur:

            cur.execute(sql)