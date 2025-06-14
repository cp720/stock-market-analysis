"""Module to get the most active stocks by day"""

import logging
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import bigquery

logger = logging.getLogger(__name__)

def _get_base_url() -> str | None:
    """Return the API URL"""
    load_dotenv()
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    if not FMP_API_KEY:
        logger.error("FMP_API_KEY environment variable not set")
        return None
    logger.debug("API Key loaded")
    BASE_URL = f"https://financialmodelingprep.com/stable/most-actives?apikey={FMP_API_KEY}"
    return BASE_URL


def fetch_most_active_stocks():
    """Fetch most active stocks"""
    BASE_URL = _get_base_url()
    if not BASE_URL:
        return None
    try:
        logger.info("Making API request to %s", BASE_URL)
        response = requests.get(BASE_URL)
        logger.info("Response status code: %s", response.status_code)

        if response.status_code != 200:
            logger.error("Error response: %", response.text)
            return None
        
        response.raise_for_status()
        data = response.json()
        logger.debug("recieved data type: %s", type(data))
        logger.debug("Data length: %s", len(data) if isinstance(data, list) else "Not a list")
        return data
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching data: %s", e)
        return None


def process_data(raw_data):
    """Convert raw API response to clean DataFrame"""
    if not raw_data:
        return None
    
    df = pd.DataFrame(raw_data)
    # Add timestamp for when the data was fetched
    df['ingestion_timestamp'] = datetime.now()
    return df


def upload_to_bigquery(df, project_id, dataset_id, table_id):
    """Upload DataFrame to BigQuery"""
    try:
        # Initialize BigQuery client
        client = bigquery.Client()
        
        # Define the table reference
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        
        # Configure the load job
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )
        
        # Upload the DataFrame
        job = client.load_table_from_dataframe(
            df, table_ref, job_config=job_config
        )
        job.result()  # Wait for the job to complete

        logger.info("Loaded %s rows into %s", len(df), table_ref)
        return True
    except Exception as e:
        logger.error("Error uploading to BigQuery: %s", e)
        return False


if __name__=="__main__":
    print(f"Fetching data for most active stocks...")
    raw_data = fetch_most_active_stocks()

    if raw_data:
        processed_data = process_data(raw_data)
        logger.info("\n%s", processed_data.head())

        # Save locally
        #processed_data.to_csv("C:/Projects/stock-market-analysis/most_active_stocks.csv")
        out_path = os.getenv("OUTPUT_CSV", "most_active_stocks.csv")
        processed_data.to_csv(out_path, index=False)

        # Upload to BigQuery
        project_id = "woven-amulet-453222-r8"  # Replace with your GCP project ID
        dataset_id = "stock_market_data"  # Replace with your dataset ID
        table_id = "most_active_stocks"  # Replace with your table ID

        upload_success = upload_to_bigquery(processed_data, project_id, dataset_id, table_id)
        if upload_success:
            logger.info("Successfully uploaded data to BigQuery")
        else:
            logger.error("Failed to upload data to BigQuery")
