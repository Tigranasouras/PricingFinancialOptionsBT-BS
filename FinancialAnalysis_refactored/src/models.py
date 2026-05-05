"""
models.py
=========

Shared data containers for the Streamlit dashboard and experiment pipeline.

Keeping the main input structure in one place makes the application easier
to maintain and helps preserve a reproducible interface across:

• app.py              -> Streamlit UI layer
• experiments.py      -> scenario / convergence analysis
• hedging.py          -> hedge calculations
• binomial_model.py   -> CRR pricing engine
• black_scholes.py    -> closed-form benchmark
"""

from __future__ import annotations

from dataclasses import dataclass


TRADING_DAYS = 252
CONTRACT_SIZE = 100


@dataclass(slots=True)
class MarketInputs:
    """
    Canonical input bundle for pricing and analysis.

    Parameters
    ----------
    ticker : str
        Underlying equity ticker.
    spot : float
        Current spot price S0.
    strike : float
        Strike price K.
    rate : float
        Risk-free rate r (annualized decimal).
    sigma : float
        Volatility sigma (annualized decimal).
    maturity_years : float
        Time to maturity in years.
    dividend_yield : float
        Continuous dividend yield q.
    steps : int
        Binomial tree depth N.
    option_type : str
        "call" or "put".
    style : str
        "european" or "american".
    """

    ticker: str
    spot: float
    strike: float
    rate: float
    sigma: float
    maturity_years: float
    dividend_yield: float
    steps: int
    option_type: str
    style: str
