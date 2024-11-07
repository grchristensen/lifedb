"""Transformation logic for dataframes."""

import uuid

import polars as pl

BUXFER_API_TRANSACTION_UUID_NAMESPACE = uuid.UUID(
    "b62cbe9b-b190-49a2-83d1-59ff13025f68"
)


def conform_buxfer_api_transactions(
    buxfer_api_transactions: pl.DataFrame,
) -> pl.DataFrame:
    """Manipulate Buxfer API transaction data into general financial transactions."""

    def generate_uuid(id: int) -> str:
        return str(uuid.uuid5(BUXFER_API_TRANSACTION_UUID_NAMESPACE, str(id)))

    financial_transactions = buxfer_api_transactions.select(
        (
            pl.col("id")
            .map_elements(generate_uuid, return_dtype=pl.datatypes.String)
            .alias("financial_txn_uuid")
        ),
        (pl.col("date").str.strptime(pl.datatypes.Date, "%Y-%m-%d").alias("txn_dt")),
        pl.col("transaction_type").alias("financial_txn_type"),
        (pl.col("expense_amount") * -1).alias("income_amt"),
        pl.col("expense_amount").alias("expense_amt"),
        pl.col("description").alias("financial_txn_desc"),
        pl.col("account_name").alias("financial_account"),
        pl.col("tags").alias("buxfer__financial_txn_tags"),
    )

    return financial_transactions
