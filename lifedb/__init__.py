"""Top-level package for lifedb."""

__author__ = """Gage Christensen"""
__email__ = "49492919+grchristensen@users.noreply.github.com"
__version__ = "0.1.0"

from dotenv import find_dotenv, load_dotenv

from lifedb.run import main_typer_app


def main():
    """Entrypoint."""
    load_dotenv(find_dotenv())

    main_typer_app()
