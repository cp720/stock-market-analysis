# Stock Market Analysis

Screen publicly traded companies based on fundamental data from Financial Modeling Prep (FMP).

## Overview

This project aims to provide a simple starting point for analyzing publicly traded companies using data from the [Financial Modeling Prep](https://financialmodelingprep.com/) API. It is an ongoing effort that currently pulls data from a single FMP endpoint. The goal is to expand coverage to multiple endpoints and build tooling that allows easy screening and analysis of companies based on their fundamentals. After the data is pulled, it is loaded into Google cloud BigQuery for storage and analyis. 

## Features

- Fetches information from FMP. 
  * As of 6/19/25 there is only one endpoing being called: https://financialmodelingprep.com/stable/most-            actives` which returns the 50 most actively traded stocks through the day. 
- Designed to be easily extended with additional data endpoints.
- Dag folder contains orchestration logic
   * I use airflow to orchestrate the API request and BigQuery load daily 

## Getting Started

### Prerequisites

- **Python 3.10+** is recommended.
- A valid **FMP API key**. Sign up at [financialmodelingprep.com](https://financialmodelingprep.com/) to obtain one.

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd stock-market-analysis
   ```
2. **Create a virtual environment** (optional but recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.\.venv\Scripts\activate`
   ```
3. **Install dependencies**
  '''bash
  python -m venv .venv
  source .venv/bin/activate      # Windows: .venv\Scripts\activate
  pip install -r requirements.txt
 '''

5. **Set up your FMP API key**. Either export an environment variable or create a `.env` file:
   ```bash
   export FMP_API_KEY=<your_key>
   ```

## Usage

Run the data fetcher using the module path:

```bash
python -m <module_path>.most_active
```

The script downloads the list of most active stocks from the Financial
Modeling Prep endpoint `https://financialmodelingprep.com/stable/most-actives`
instead of requesting data for each ticker individually.

## Roadmap

- Add more FMP endpoints (historical prices, ratios, news, etc.).
- Improve error handling and add retry/backoff logic.
- Introduce data caching and persistence.
- Provide sample notebooks for analysis.
