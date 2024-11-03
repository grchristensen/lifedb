"""Functions/variables for working with APIs."""

import json
import os
from datetime import date
from io import StringIO
from math import ceil
from typing import Optional

import httpx
import polars as pl

BUXFER_API_URL = "https://www.buxfer.com/api"


class APIError(Exception):
    """Any errors related to interacting with APIs."""


def _get_buxfer_api_token_env_var() -> str:
    api_token = os.getenv("LIFEDB_BUXFER_API_TOKEN")

    if api_token is None:
        raise APIError(
            "Environment variable LIFEDB_BUXFER_API_TOKEN is required to connect to "
            "Buxfer API."
        )

    return api_token


BUXFER_API_TRANSACTIONS_SCHEMA = {
    "id": pl.datatypes.Int64,
    "description": pl.datatypes.String,
    "date": pl.datatypes.String,
    "type": pl.datatypes.String,
    "transaction_type": pl.datatypes.String,
    "amount": pl.datatypes.Float64,
    "expense_amount": pl.datatypes.Float64,
    "account_id": pl.datatypes.Int64,
    "account_name": pl.datatypes.String,
    "tags": pl.datatypes.String,
    "tag_names": pl.datatypes.List(pl.datatypes.String),
    "status": pl.datatypes.String,
    "is_future_dated": pl.datatypes.Boolean,
    "is_pending": pl.datatypes.Boolean,
    "from_account": pl.datatypes.Struct(
        [
            pl.Field("id", pl.datatypes.Int64),
            pl.Field("name", pl.datatypes.String),
        ]
    ),
    "to_account": pl.datatypes.Struct(
        [
            pl.Field("id", pl.datatypes.Int64),
            pl.Field("name", pl.datatypes.String),
        ]
    ),
}

BUXFER_API_TRANSACTIONS_CAMELCASE_RENAMES = {
    "id": "id",
    "description": "description",
    "date": "date",
    "type": "type",
    "transactionType": "transaction_type",
    "amount": "amount",
    "expenseAmount": "expense_amount",
    "accountId": "account_id",
    "accountName": "account_name",
    "tags": "tags",
    "tagNames": "tag_names",
    "status": "status",
    "isFutureDated": "is_future_dated",
    "isPending": "is_pending",
    "fromAccount": "from_account",
    "toAccount": "to_account",
}


def _parse_buxfer_api_data(api_json, *, camelcase_renames, schema) -> pl.DataFrame:
    reverse_renames = {rename: name for name, rename in camelcase_renames.items()}

    # Following code will break if camelcase_renames and schema don't have matching keys
    if sorted(list(reverse_renames.keys())) != sorted(list(schema.keys())):
        raise ValueError("Rename dict must map schema dict.")

    # Schemas in this module are defined based on their data's final names (so they can
    # be reused outside this module). Therefore we have to create a version for the data
    # as it arrives from the API (which will be camelcase).
    norename_schema = {
        reverse_renames[field]: data_type for field, data_type in schema.items()
    }

    df = pl.read_json(StringIO(json.dumps(api_json)), schema=norename_schema)

    df = df.rename(camelcase_renames)

    return df


def get_buxfer_transactions(
    *,
    start_date: Optional[date] = None,
    page_limit: int = 1,
    allow_partial_data: bool = False,
) -> pl.DataFrame:
    """Retrieve transactions from Buxfer API.

    Parameters
    ----------
    start_date: Optional[date]
        The date to filter transactions from (filter includes start date).
    page_limit: int
        Restricts the number of pages that will be queried from the API. Buxfer returns
        transactions in pages of 100, so the max transactions returned by this function
        will be `100 * page_limit`.
    allow_partial_data: bool
        If True, will not throw error when the queried data returns more pages than
        `page_limit`, and will instead return transactions up to `page_limit`.
    """
    if page_limit < 1:
        raise ValueError("page_limit must be a positive integer of at least 1.")

    request_url = BUXFER_API_URL + "/transactions"
    api_token = _get_buxfer_api_token_env_var()

    request_params = {"token": api_token}
    if start_date is not None:
        request_params["startDate"] = start_date.strftime("%Y-%m-%d")

    def get_transactions_page(page=None):
        page_params = {key: value for key, value in request_params.items()}

        if page is not None:
            page_params["page"] = page

        raw_response = httpx.get(request_url, params=page_params)
        response = raw_response.raise_for_status()
        response_json = response.json()

        response_transaction_count = int(response_json["response"]["numTransactions"])
        page_transactions = _parse_buxfer_api_data(
            response_json["response"]["transactions"],
            camelcase_renames=BUXFER_API_TRANSACTIONS_CAMELCASE_RENAMES,
            schema=BUXFER_API_TRANSACTIONS_SCHEMA,
        )

        return response_transaction_count, page_transactions

    transaction_count, first_page_transactions = get_transactions_page()

    page_count = ceil(transaction_count / 100)

    if page_count > page_limit:
        if not allow_partial_data:
            raise APIError(
                "More pages returned than allowed by page_limit. Increase page_limit "
                "or query a shorter period of time to avoid incomplete data."
            )
        else:
            page_count = page_limit

    if page_count > 1:
        transaction_dfs = [first_page_transactions]

        for page_index in range(2, page_count + 1):
            _, next_page_transactions = get_transactions_page(page=page_index)
            transaction_dfs.append(next_page_transactions)

        all_transactions = pl.concat(transaction_dfs)
    else:
        all_transactions = first_page_transactions

    return all_transactions
