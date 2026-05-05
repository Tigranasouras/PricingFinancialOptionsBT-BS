"""
experiments.py
==============

Numerical experiments and convergence analysis for option pricing.

Purpose
-------
This module contains "experiment logic" used to evaluate pricing models.
It is separate from model implementations to keep the project modular:

• src/binomial_model.py   -> numerical pricing method (CRR binomial)
• src/black_scholes.py    -> analytical benchmark (Black–Scholes)
• src/experiments.py      -> tests/experiments comparing the two
"""

from __future__ import annotations

import os
from typing import Callable, Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.binomial_model import price_option_crr
from src.black_scholes import price_option
from src.models import MarketInputs



def convergence_experiment(S0, K, r, sigma, T, Ns, option_type="call", q=0.0):
    """
    Run a convergence experiment comparing CRR binomial prices to Black–Scholes.
    """
    bs_price = price_option(S0, K, r, sigma, T, option_type=option_type, q=q)
    bin_prices = [
        price_option_crr(S0, K, r, sigma, T, N, option_type=option_type, q=q, style="european")
        for N in Ns
    ]
    errors = np.abs(np.array(bin_prices) - bs_price)
    return bs_price, bin_prices, errors



def plot_convergence(Ns, bin_prices, bs_price, save_path="figures/convergence.png"):
    """
    Plot CRR binomial prices as a function of step count N and compare them
    against the Black–Scholes benchmark.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(Ns, bin_prices, marker="o", label="CRR Binomial")
    ax.axhline(bs_price, linestyle="--", label="Black–Scholes")
    ax.set_xlabel("Number of Steps (N)")
    ax.set_ylabel("Option Price")
    ax.set_title("Binomial Convergence to Black–Scholes (European)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig



def build_scenario_table(inputs: MarketInputs, price_fn: Callable[..., float], shocks: Sequence[float]) -> pd.DataFrame:
    """
    Reprice the option under a set of spot-price shocks.

    Parameters
    ----------
    inputs : MarketInputs
        Base market / contract inputs.
    price_fn : callable
        Pricing function with signature similar to the model functions.
    shocks : sequence[float]
        Spot shocks such as [-0.10, -0.05, 0.0, 0.05, 0.10].
    """
    rows = []
    base = price_fn(
        inputs.spot,
        inputs.strike,
        inputs.rate,
        inputs.sigma,
        inputs.maturity_years,
        option_type=inputs.option_type,
        q=inputs.dividend_yield,
    )

    for shock in shocks:
        shocked_spot = inputs.spot * (1.0 + shock)
        shocked_price = price_fn(
            shocked_spot,
            inputs.strike,
            inputs.rate,
            inputs.sigma,
            inputs.maturity_years,
            option_type=inputs.option_type,
            q=inputs.dividend_yield,
        )
        rows.append(
            {
                "Spot Shock": f"{shock:+.0%}",
                "Shocked Spot": round(shocked_spot, 2),
                "Option Price": round(float(shocked_price), 4),
                "P&L vs Base": round(float(shocked_price - base), 4),
            }
        )

    return pd.DataFrame(rows)
