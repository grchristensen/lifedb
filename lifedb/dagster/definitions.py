"""Dagster definitions."""

from dagster import (
    AssetSelection,
    DefaultScheduleStatus,
    Definitions,
    ScheduleDefinition,
    load_assets_from_modules,
)

from . import assets  # noqa: TID252

all_assets = load_assets_from_modules([assets])

batch_update_schedule = ScheduleDefinition(
    name="batch_update_schedule",
    target=AssetSelection.all(),
    cron_schedule="0 * * * *",  # every hour
    default_status=DefaultScheduleStatus.RUNNING,
)

defs = Definitions(
    assets=all_assets,
    schedules=[batch_update_schedule],
)
