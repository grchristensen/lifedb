"""Common functions for interacting with the database."""

import os
from typing import Optional

import polars as pl
import psycopg


class DBError(Exception):
    """Exception class for any errors managing the LifeDB."""


def _get_db_env_var(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)

    if env_var is None:
        raise DBError(
            f"Missing environment variable {env_var_name} required for database "
            "connection."
        )

    return env_var


def get_db_connection(*, autocommit: bool = False) -> psycopg.Connection:
    """Get a standard connection to the LifeDB database."""
    return psycopg.connect(
        user=_get_db_env_var("LIFEDB_DB_USER"),
        password=_get_db_env_var("LIFEDB_DB_PASSWORD"),
        host=_get_db_env_var("LIFEDB_DB_HOST"),
        port=_get_db_env_var("LIFEDB_DB_PORT"),
        dbname=_get_db_env_var("LIFEDB_DB_NAME"),
        autocommit=autocommit,
    )


def get_db_connection_uri() -> str:
    """Get a standard connection URI to the LifeDB database."""
    return (
        f"postgresql://{_get_db_env_var('LIFEDB_DB_USER')}"  # noqa: E231
        f":{_get_db_env_var('LIFEDB_DB_PASSWORD')}"  # noqa: E231
        f"@{_get_db_env_var('LIFEDB_DB_HOST')}"
        f":{_get_db_env_var('LIFEDB_DB_PORT')}"  # noqa: E231
        f"/{_get_db_env_var('LIFEDB_DB_NAME')}"
    )


def try_get_table(table_name: str, *, schema: Optional[str] = None) -> pl.DataFrame:
    """Attempt to retrieve the given table, or return None if it does not exist."""
    with get_db_connection() as con:
        if schema is None:
            query = f"select * from {table_name}"
        else:
            query = f"select * from {schema}.{table_name}"

        try:
            data = pl.read_database(query, connection=con)
        except psycopg.errors.UndefinedTable:
            data = None

    return data
