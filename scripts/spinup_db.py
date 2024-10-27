import os
from pathlib import Path

import duckdb
import yaml
from dotenv import find_dotenv, load_dotenv
from importlib_resources import files

from lifedb import DBError


def main():
    db_path = os.getenv("LIFEDB_DB_PATH")
    if db_path is None:
        raise KeyError("Missing required environment variable: LIFEDB_DB_PATH")
    db_path = Path(db_path)

    if db_path.exists():
        raise DBError("Database already exists.")

    print(f"Creating database at {db_path}")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Connecting to a DuckDB database will automatically create one if it does not
    # exist.
    db = duckdb.connect(db_path)

    schema_yaml = files("lifedb").joinpath("schemas.yml").read_text()
    schema_yaml = yaml.safe_load(schema_yaml)

    for schema in schema_yaml["schemas"]:
        db.execute(f"create schema {schema}")


if __name__ == "__main__":
    load_dotenv(find_dotenv())

    main()
