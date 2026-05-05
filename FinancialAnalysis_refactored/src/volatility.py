"""
volatility.py
=============

Volatility estimation utilities.

Volatility is one of the most important inputs in option pricing.
Both the CRR binomial model and the Black–Scholes model require an
estimate of the underlying asset's annualized volatility (σ).

This module estimates volatility from historical market data using
logarithmic returns.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.data_loader import download_price_history, extract_close_series
from src.models import TRADING_DAYS



def historical_volatility_from_series(close: pd.Series, use_log_returns: bool = True) -> float:
    """
    Estimate annualized historical volatility from a close-price series.

    Parameters
    ----------
    close : pd.Series
        Historical close prices.
    use_log_returns : bool
        When True, use log returns; otherwise use percentage returns.

    Returns
    -------
    float
        Annualized volatility estimate.
    """
    if use_log_returns:
        returns = np.log(close / close.shift(1)).dropna()
    else:
        returns = close.pct_change().dropna()

    if returns.empty:
        raise ValueError("Not enough data to compute volatility.")

    annual_volatility = returns.std() * np.sqrt(TRADING_DAYS)
    return float(annual_volatility)



def historical_volatility(ticker: str, lookback: str = "1y") -> float:
    """
    Estimate annualized historical volatility directly from Yahoo Finance.

    This function preserves the original public interface used in the project
    while reusing the shared data-loading utilities.
    """
    history = download_price_history(ticker, period=lookback)
    close = extract_close_series(history)
    return historical_volatility_from_series(close)
