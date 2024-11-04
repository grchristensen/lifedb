"""Dagster assets."""

import os
from datetime import datetime, timedelta

import polars as pl
from dagster import Config, asset
from pydantic import Field

from lifedb import core


class BuxferAPITransactionsConfig(Config):
    """Config for buxfer_api_transactions asset."""

    page_limit: int = Field(
        default=5, description="Limits the number of pages to search in API."
    )


@asset
def buxfer_api_transactions(config: BuxferAPITransactionsConfig):
    """Get financial transaction data from Buxfer API."""
    current_transactions = core.db.try_get_table(
        "buxfer_api_transactions", schema="landing"
    )

    if current_transactions is None or current_transactions.height == 0:
        transactions = core.api.get_buxfer_transactions(
            page_limit=config.page_limit, allow_partial_data=True
        )
    else:
        lookback_days_optional = os.getenv("LIFEDB_DAGSTER_LOOKBACK_DAYS")
        lookback_days = (
            0 if lookback_days_optional is None else int(lookback_days_optional)
        )

        latest_transaction_date_str = current_transactions.select(
            pl.col("date").max()
        ).item()
        latest_transaction_date = datetime.strptime(
            latest_transaction_date_str, "%Y-%m-%d"
        ).date()

        new_transactions = core.api.get_buxfer_transactions(
            start_date=latest_transaction_date - timedelta(days=lookback_days),
            page_limit=config.page_limit,
        )

        transactions = pl.concat(
            [
                current_transactions.filter(
                    pl.col("id").is_in(new_transactions["id"]).not_()
                ),
                new_transactions,
            ]
        )

    transactions.write_database(
        "landing.buxfer_api_transactions",
        connection=core.db.get_db_connection_uri(),
        if_table_exists="replace",
    )
