import yfinance as yf
import pandas as pd
import numpy as np


def fetch_tickers_from_txt(file_path: str = 'Symbols_NSE.txt') -> list:
    """
    Parses the NSE symbols text file, cleans out non-standard equities
    (like block deals and mutual funds), and formats them for Yahoo Finance.
    """
    clean_tickers = []

    with open(file_path, 'r', encoding='utf-8') as file:
        # Skip the first header line
        next(file, None)

        for line in file:
            # Split by the first whitespace/tab to isolate the symbol
            parts = line.strip().split(maxsplit=1)
            if not parts:
                continue

            raw_symbol = parts[0]

            # FILTERING LOGIC:
            # Skip mutual funds (often start with 0P) and
            # skip NSE internal series tags like .BL, .ST, -SM, .RE
            if '.' in raw_symbol or '-' in raw_symbol or raw_symbol.startswith('0P'):
                continue

            # Append .NS so Yahoo Finance knows to look at the National Stock Exchange
            yf_ticker = f"{raw_symbol}.NS"
            clean_tickers.append(yf_ticker)

    # Return a unique, sorted list
    return sorted(list(set(clean_tickers)))


def fetch_and_preprocess(tickers, benchmark='^NSEI', start_date='2024-01-01', end_date='2026-05-20'):
    """
    Fetches daily stock and benchmark data, then calculates log returns.
    """
    print(f"Fetching data from {start_date} to {end_date}...")

    # Combine target stocks with the benchmark index
    all_tickers = tickers + [benchmark]

    # Download data
    data = yf.download(all_tickers, start=start_date, end=end_date, progress=False)

    # 1. DATA COLLECTION
    # Use 'Close' instead of 'Adj Close' due to yfinance API updates
    prices = data['Close']

    # We only need volume for the individual stocks, not necessarily the index
    volumes = data['Volume'].drop(columns=[benchmark], errors='ignore')

    # 2. PREPROCESSING: Log Returns
    log_returns = np.log(prices / prices.shift(1))

    # FIX: Drop rows only if ALL columns are NaN (e.g., weekends).
    # This prevents a single failed ticker from wiping out the whole dataset.
    log_returns = log_returns.dropna(how='all')
    prices = prices.dropna(how='all')

    return prices, volumes, log_returns


# Example execution using a sample of Nifty 50 heavyweights
if __name__ == "__main__":
    # Put your test code in here.
    # It will ONLY run if you execute data_loader.py directly,
    # not when you import it into another file.
    sample_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'BMWVENTLTD.NS']
    prices, volumes, log_returns = fetch_and_preprocess(sample_stocks)
    print(log_returns.head())