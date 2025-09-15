'''Module for fetching historical price data.'''

import logging
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def _get_base_url(symbol: str, start_date: str) -> str | None:
    """Return the API URL for a given ticker and date range"""
    load_dotenv()
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    if not FMP_API_KEY:
        logger.error("FMP_API_KEY environment variable not set")
        return None
    logger.debug("API Key loaded")
    BASE_URL = f"https://financialmodelingprep.com/stable/historical-price-eod/non-split-adjusted?symbol={symbol}&from={start_date}&apikey={FMP_API_KEY}"
    return BASE_URL

def fetch_historical_price_data(symbols, start_date="2023-01-01"):
    """fetch historical price data"""
    dfs = []
    for sym in symbols:
        url = _get_base_url(sym, start_date)
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df['symbol'] = sym
            dfs.append(df)
        else:
            logger.error(f"Failed to fetch data for {sym}: {response.status_code}")
    
    return pd.concat(dfs, ignore_index=True)

def to_monthly_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert daily price data to monthly returns"""

    df['date'] = pd.to_datetime(df['date'])
    pivot = df.pivot(index='date', columns='symbol', values='adjClose')
    monthly_prices = pivot.resample('M').last()
    monthly_returns = monthly_prices.pct_change().dropna(how='all')
    return monthly_returns

def compute_momentum_scores(monthly_returns, formation=12, skip=1):
    scores = {}
    for col in monthly_returns.columns:
        formation_window = monthly_returns[col].iloc[-(formation+skip):-skip]
        Rcum = (1 + formation_window).prod() - 1
        Rmean = formation_window.mean()
        Rrisk_adj = Rmean / formation_window.std() if formation_window.std() != 0 else None
        scores[col] = {"Rcum": Rcum, "Rmean": Rmean, "Rrisk_adj": Rrisk_adj}

    return pd.DataFrame(scores).T

if __name__=="__main__":
    symbols = ["AAPL", "MSFT", "GOOGL"]
    df = fetch_historical_price_data(symbols)
    res = to_monthly_returns(df)
    scores = compute_momentum_scores(res)
    print(scores)
