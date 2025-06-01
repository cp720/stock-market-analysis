import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")
print(f"API Key loaded: {'Yes' if FMP_API_KEY else 'No'}")
#BASE_URL = f"https://financialmodelingprep.com/stable/biggest-gainers?apikey={FMP_API_KEY}"
#BASE_URL = f"https://financialmodelingprep.com/stable/biggest-losers?apikey={FMP_API_KEY}"
BASE_URL = f"https://financialmodelingprep.com/stable/most-actives?apikey={FMP_API_KEY}"

def fetch_sector_pe_data():
    """Fetch historical P/E data for the specified sector"""
    try:
        print(f"Making API request to {BASE_URL}")
        response = requests.get(BASE_URL)
        print(f"Response status code: {response.status_code}")

        if response.status_code != 200:
            print(f"Error response: {response.text}")
            return None
        
        response.raise_for_status()
        data = response.json()
        print(f"Recieved data type: {type(data)}")
        print(f"Data length: {len(data) if isinstance(data, list) else 'Not a list'}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
def process_data(raw_data):
    """Convert raw API response to clean DataFrame"""
    if not raw_data:
        return None
    
    df = pd.DataFrame(raw_data)

    return df

if __name__=="__main__":
    print(f"fetching data for biggest gainers...")
    raw_data = fetch_sector_pe_data()
    #print(raw_data)

    if raw_data:
        processed_data = process_data(raw_data)
        print(processed_data.head())
        processed_data.to_csv("C:/Projects/stock-market-analysis/biggest_stock_gainers.csv")
