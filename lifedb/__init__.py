"""Top-level package for lifedb."""

__author__ = """Gage Christensen"""
__email__ = "49492919+grchristensen@users.noreply.github.com"
__version__ = "0.1.0"

from lifedb.run import main_typer_app


class DBError(Exception):
    """Exception class for any errors managing the LifeDB."""


def main():
    """Entrypoint."""
    main_typer_app()
