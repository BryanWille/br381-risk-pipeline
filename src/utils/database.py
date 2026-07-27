import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def get_engine():

    url = (
        f"postgresql://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

    return create_engine(url)
