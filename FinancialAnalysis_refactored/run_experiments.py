"""
run_experiments.py
==================

Main experiment pipeline for the Option Pricing research project.

This script orchestrates the full workflow:
1) Fetch real market data (spot price + risk-free rate)
2) Estimate volatility from historical returns
3) Visualize CRR lattices (stock + option value)
4) Run numerical experiments comparing pricing models
5) Output results and generate convergence plots

This file intentionally contains *no model math*.
All financial models live inside the `src/` package.

This design mirrors real research/industry workflows where:
- models are reusable modules
- experiments are separate reproducible pipelines
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from src.black_scholes import price_option
from src.data_loader import get_spot_price
from src.experiments import convergence_experiment, plot_convergence
from src.fred_loader import get_risk_free_rate
from src.tree_visualization import build_crr_trees
from src.volatility import historical_volatility


def main() -> None:
    """Run a small end-to-end experiment for the research project."""
    ticker = "SBUX"
    option_type = "call"
    K = 100.0
    T = 90 / 365
    q = 0.0
    Ns = [5, 10, 25, 50, 100, 200, 500]

    S0 = get_spot_price(ticker)
    sigma = historical_volatility(ticker, lookback="1y")
    r = get_risk_free_rate(maturity="3m", default_rate=0.045)

    print("RUNNING RESULTS")
    print("---------------")
    print(f"Ticker: {ticker}")
    print(f"Spot price: {S0:.2f}")
    print(f"Historical volatility: {sigma:.4f}")
    print(f"Risk-free rate: {r:.4f}")

    bs_price, bin_prices, errors = convergence_experiment(
        S0, K, r, sigma, T, Ns, option_type=option_type, q=q
    )

    print(f"Black-Scholes benchmark: {bs_price:.4f}")
    print("\nCRR Binomial prices:")
    for N, price, err in zip(Ns, bin_prices, errors):
        print(f"  N={N:>3}: price={price:.4f}, abs_error={err:.6f}")

    plot_convergence(Ns, bin_prices, bs_price, save_path="figures/convergence.png")

    # Small lattice build for visual inspection.
    S_tree, V_tree, dt, u, d, p = build_crr_trees(
        S0, K, r, sigma, T, N=8, option_type=option_type, q=q, american=False
    )
    print("\nSmall CRR lattice built successfully.")
    print(f"dt={dt:.6f}, u={u:.6f}, d={d:.6f}, p={p:.6f}")
    print(f"Root option value from lattice: {V_tree[0,0]:.4f}")


if __name__ == "__main__":
    main()
