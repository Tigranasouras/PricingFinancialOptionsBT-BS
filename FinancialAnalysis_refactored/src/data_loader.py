"""
data_loader.py
==============

Market data acquisition utilities.

This module provides a clean interface for fetching real market data
used throughout the option pricing pipeline.

Why this exists
---------------
Separating data acquisition from modeling:
• keeps models reusable and testable
• makes experiments reproducible
• mirrors real data science / quant workflows
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf



def download_price_history(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Download recent historical price data from Yahoo Finance.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol.
    period : str
        Yahoo Finance lookback window such as "3mo", "1y", or "5y".
    interval : str
        Sampling interval. The dashboard uses daily data by default.

    Returns
    -------
    pd.DataFrame
        Historical OHLCV data.
    """
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'.")

    # yfinance can sometimes return a MultiIndex even for a single ticker.
    if isinstance(df.columns, pd.MultiIndex):
        if len(df.columns.levels[-1]) == 1:
            df.columns = df.columns.get_level_values(0)
        else:
            df = df.xs(df.columns.levels[-1][0], axis=1, level=-1)

    return df



def extract_close_series(df: pd.DataFrame) -> pd.Series:
    """
    Extract a clean Close-price series from a historical-data DataFrame.
    """
    close_data = df["Close"]
    if isinstance(close_data, pd.DataFrame):
        close_data = close_data.iloc[:, 0]
    return close_data.astype(float).dropna()



def get_spot_price(ticker: str) -> float:
    """
    Fetch the most recent closing price of a stock.

    This preserves the spirit of the original project helper while routing
    through the shared history loader so the Streamlit app and notebooks use
    the same data-access path.
    """
    data = download_price_history(ticker, period="5d", interval="1d")
    close = extract_close_series(data)
    return float(close.iloc[-1])
