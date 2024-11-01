"""Entrypoint definition for web application with Typer."""

import typer

webapp_typer_app = typer.Typer()


@webapp_typer_app.command()
def run():
    """Run the web application."""
    # Only import here so that global variables in this script aren't loaded too
    # eagerly.
    from lifedb.app.sample_app import sample_app

    sample_app.run(debug=True)
