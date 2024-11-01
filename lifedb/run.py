"""Entrypoint definition with Typer."""

import typer

from lifedb.app.run import webapp_typer_app

main_typer_app = typer.Typer()
main_typer_app.add_typer(webapp_typer_app, name="app")
