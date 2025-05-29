import requests
import pandas as pd
import os
from datetime import datetime
import time

API_KEY = "nKTEA9lSP1IZgNs3Mgqj7TE2scx9XAjw"

BASE_URL = "https://financialmodelingprep.com/stable/biggest-gainers?apikey=nKTEA9lSP1IZgNs3Mgqj7TE2scx9XAjw"

def fetch_sector_pe_data():
    """Fetch historical P/E data for the specified sector"""
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status() # Raises exception
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
def process_data(raw_data):
    """Convert raw API response to clean DataFrame"""
    if not raw_data:
        return None
    
    df = pd.DataFrame(raw_data)

    # Convert date formatting and set as index
    #df['date'] = pd.to_datetime(df['date'])
    #df.set_index('date', inplace=True)

    # Calculate additional metrics
    #df['pe_ratio'] = df['pe'].astype(float)
    #df['sector'] = SECTOR

    return df

if __name__=="__main__":
    print(f"fetching historical P/E data for biggest gainers...")
    raw_data = fetch_sector_pe_data()
    #print(raw_data)

    if raw_data:
        processed_data = process_data(raw_data)
        print(process_data)
