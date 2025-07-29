from __future__ import annotations

"""Airflow DAG to ingets daily most active stoscks from FMP and load into BigQuery"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


from stock_market_analysis.pipeline import fetch_process_upload

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


