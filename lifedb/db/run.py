"""Entrypoint for DB commands."""

import os

import psycopg
import typer
import yaml
from importlib_resources import files
from psycopg import sql

from lifedb.core.exceptions import DBError

db_typer_app = typer.Typer()


@db_typer_app.command()
def init():
    """Initialize database."""

    def get_db_env_var(env_var_name: str) -> str:
        env_var = os.getenv(env_var_name)

        if env_var is None:
            raise DBError(
                f"Missing environment variable {env_var_name} required for database "
                "instantiation."
            )

        return env_var

    db_user = get_db_env_var("LIFEDB_DB_USER")
    db_password = get_db_env_var("LIFEDB_DB_PASSWORD")
    db_host = get_db_env_var("LIFEDB_DB_HOST")
    db_port = get_db_env_var("LIFEDB_DB_PORT")
    db_name = get_db_env_var("LIFEDB_DB_NAME")
    init_db_name = get_db_env_var("LIFEDB_INIT_DB_NAME")

    # Need to have separate connections for each database that we connect to
    create_db_config = {
        "user": db_user,
        "password": db_password,
        "host": db_host,
        "port": db_port,
        "dbname": init_db_name,
        "autocommit": True,
    }

    create_tables_config = {
        "user": db_user,
        "password": db_password,
        "host": db_host,
        "port": db_port,
        "dbname": db_name,
        "autocommit": True,
    }

    try:
        create_db_con = psycopg.connect(**create_db_config)
        create_db_cur = create_db_con.cursor()

        create_db_cur.execute(
            sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name))
        )

        create_db_cur.close()
        create_db_con.close()

        create_tables_con = psycopg.connect(**create_tables_config)
        create_tables_cur = create_tables_con.cursor()

        schema_yaml = files("lifedb.db").joinpath("schemas.yml").read_text()
        schema_yaml = yaml.safe_load(schema_yaml)

        for schema in schema_yaml["schemas"]:
            create_tables_cur.execute(
                sql.SQL("create schema {};").format(sql.Identifier(schema))
            )

        create_tables_sql = (
            files("lifedb.db.sql").joinpath("create_sample_tables.sql").read_text()
        )
        load_data_sql = (
            files("lifedb.db.sql").joinpath("load_sample_data.sql").read_text()
        )

        create_tables_cur.execute(sql.SQL(create_tables_sql))
        create_tables_cur.execute(sql.SQL(load_data_sql))

        create_tables_cur.close()
        create_tables_con.close()
    except psycopg.Error as err:
        print(err)
        exit(1)
