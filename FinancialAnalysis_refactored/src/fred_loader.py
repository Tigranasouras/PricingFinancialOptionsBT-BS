"""
fred_loader.py
==============

Risk-free rate retrieval helpers.

This module fetches a Treasury-yield proxy from FRED and converts it into
a decimal annualized rate suitable for the CRR binomial model and the
Black–Scholes benchmark.

Why this exists
---------------
Keeping rate retrieval outside the UI and model files:
• preserves modularity
• makes experiments easier to reproduce
• mirrors the documentation style used across the project
"""

from __future__ import annotations

import pandas as pd


FRED_SERIES = {
    "3m": "DGS3MO",
    "2y": "DGS2",
    "5y": "DGS5",
    "10y": "DGS10",
}


def get_risk_free_rate(maturity: str = "3m", default_rate: float = 0.045) -> float:
    """
    Fetch a recent Treasury yield from FRED and return it as a decimal.

    Parameters
    ----------
    maturity : str
        Key such as "3m", "2y", "5y", or "10y".
    default_rate : float
        Fallback rate returned when the FRED request fails or no usable
        observation is available.

    Returns
    -------
    float
        Annualized decimal risk-free proxy, e.g. 0.045 for 4.5%.
    """
    series_id = FRED_SERIES.get(maturity.lower(), "DGS3MO")
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"

    try:
        df = pd.read_csv(url)
        if series_id not in df.columns:
            return float(default_rate)

        values = pd.to_numeric(df[series_id], errors="coerce").dropna()
        if values.empty:
            return float(default_rate)

        return float(values.iloc[-1]) / 100.0
    except Exception:
        return float(default_rate)
