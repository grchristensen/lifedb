"""Entrypoint definition with Typer."""

import typer
from dotenv import find_dotenv, load_dotenv

from lifedb.app.run import webapp_typer_app
from lifedb.db.run import db_typer_app

main_typer_app = typer.Typer()
main_typer_app.add_typer(webapp_typer_app, name="app")
main_typer_app.add_typer(db_typer_app, name="db")


def run():
    """Entrypoint."""
    load_dotenv(find_dotenv())

    main_typer_app()
