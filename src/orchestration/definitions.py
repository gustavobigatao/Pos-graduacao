from dagster import (
    asset,
    Definitions,
    ScheduleDefinition,
    AssetSelection,
    RetryPolicy,
)

from src.models.database import init_db, SessionLocal
from src.jobs.discovery import discover_available_data
from src.jobs.sync import sync_month
from src.jobs.transform import transform_data
from src.jobs.load_db import load_to_postgres
from src.jobs.load_s3 import upload_parquets_to_s3

import logging

logger = logging.getLogger(__name__)

RETRY_POLICY = RetryPolicy(max_retries=3, delay=30)


@asset(retry_policy=RETRY_POLICY)
def discovery():
    init_db()
    db = SessionLocal()
    try:
        result = discover_available_data(db)
        return {"status": "completed", "result": result}
    finally:
        db.close()


@asset(deps=["discovery"], retry_policy=RETRY_POLICY)
def sync(year_month: str):
    init_db()
    db = SessionLocal()
    try:
        result = sync_month(db, year_month)
        return {"status": "completed", "year_month": year_month, "result": result}
    finally:
        db.close()


@asset(deps=["sync"], retry_policy=RETRY_POLICY)
def transform(year_month: str):
    transform_data(year_month)
    return {"status": "completed", "year_month": year_month}


@asset(deps=["transform"], retry_policy=RETRY_POLICY)
def load_database(year_month: str):
    init_db()
    db = SessionLocal()
    try:
        rows = load_to_postgres(year_month=year_month, db=db)
        return {"status": "completed", "year_month": year_month, "rows_loaded": rows}
    finally:
        db.close()


@asset(deps=["transform"], retry_policy=RETRY_POLICY)
def load_s3(year_month: str):
    result = upload_parquets_to_s3(year_month)
    return {"status": "completed", "year_month": year_month, "result": result}


cnpj_pipeline_schedule = ScheduleDefinition(
    job=AssetSelection.assets("discovery", "sync", "transform", "load_database", "load_s3").to_job(
        name="cnpj_pipeline"
    ),
    cron_schedule="0 6 * * 1",
)


defs = Definitions(
    assets=[discovery, sync, transform, load_database, load_s3],
    schedules=[cnpj_pipeline_schedule],
)
