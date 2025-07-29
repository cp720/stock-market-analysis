from datetime import datetime, timedelta
import os

from stock_market_analysis.most_active import fetch_most_active_stocks, process_data, upload_to_bigquery

def fetch_process_upload() -> None:
    project_id = os.getenv("GCP_PROJECT_ID", "woven-amulet-453222-r8")
    dataset_id = os.getenv("BQ_DATASET", "stock_market_data")
    table_id   = os.getenv("BQ_TABLE", "most_active_stocks")

    raw = fetch_most_active_stocks()
    if not raw:
        raise ValueError("Failed to fetch")
    df = process_data(raw)
    if df is None or df.empty:
        raise ValueError("No data")
    if not upload_to_bigquery(df, project_id, dataset_id, table_id):
        raise ValueError("Upload failed")
