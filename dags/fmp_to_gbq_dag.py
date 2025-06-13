from __future__ import annotations

"""Airflow DAG to ingets daily most active stoscks from FMP and load into BigQuery"""

from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.most_active import (
    fetch_most_active_stocks,
    process_data,
    upload_to_bigquery,
)

def fetch_process_upload() -> None:
    """Fetch most active stocks and load them into BIgQuery"""
    project_id = os.getenv("GCP_PROJECT_ID", "woven-amulet-453222-r8")
    dataset_id = os.getenv("BQ_DATASET", "stock_market_data")
    table_id = os.getenv("BQ_TABLE", "most_active_stocks")

    raw_data = fetch_most_active_stocks()
    if not raw_data:
        raise ValueError("Failed to fetch most active stocks")

    df = process_data(raw_data)
    if df is None or df.empty:
        raise ValueError("No data returned from processing step")
    
    success = upload_to_bigquery(df, project_id, dataset_id, table_id)
    if not success:
        raise ValueError("BigQuery upload failed")

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="fmp_to_bq_daily",
    description="Load daily most active tickers to BigQuery",
    start_date=datetime(2025, 6, 16),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=['fmp', 'stocks'],
) as dag:
    run_pipeline = PythonOperator(
        task_id="fetch_and_load_most_active",
        python_callable=fetch_process_upload,
    )

    run_pipeline


