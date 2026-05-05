"""
binomial_model.py
=================

Cox–Ross–Rubinstein (CRR) Binomial Option Pricing Model

This module implements CRR pricing for both European and American options.
The lighter price-only function is useful for experiments, while the fuller
report function is useful for the interactive Streamlit dashboard.

Key ideas:
-----------
• Stock prices evolve on a recombining lattice
• Each time step has two possible movements: up or down
• Risk-neutral valuation is used for pricing
• Backward induction computes the option value
• American options add an early-exercise comparison at each node
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np



def _validate_inputs(T: float, N: int) -> None:
    if T <= 0:
        raise ValueError("Time to maturity T must be positive.")
    if N < 1:
        raise ValueError("Number of steps N must be at least 1.")



def build_stock_tree(S0, sigma, r, T, N, q=0.0) -> Tuple[np.ndarray, float, float, float, float]:
    """
    Build the full recombining CRR stock-price lattice.

    Returns
    -------
    tree : np.ndarray
        Stock price lattice.
    dt, u, d, p : float
        CRR parameters for reporting / downstream analysis.
    """
    _validate_inputs(T, N)
    dt = T / N
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp((r - q) * dt) - d) / (u - d)

    if not (0 < p < 1):
        raise ValueError(
            "Risk-neutral probability is outside (0, 1). Try adjusting T, sigma, r, q, or N."
        )

    tree = np.full((N + 1, N + 1), np.nan)
    tree[0, 0] = S0
    for i in range(1, N + 1):
        for j in range(i + 1):
            tree[j, i] = S0 * (u**j) * (d ** (i - j))
    return tree, dt, u, d, p



def price_option_crr(S0, K, r, sigma, T, N, option_type="call", q=0.0, style="european"):
    """
    Price an option using the CRR binomial tree.

    Parameters
    ----------
    style : str
        "european" or "american".

    Returns
    -------
    float
        Present value of the option.
    """
    result = price_option_crr_full(
        S0=S0,
        K=K,
        r=r,
        sigma=sigma,
        T=T,
        N=N,
        option_type=option_type,
        q=q,
        style=style,
    )
    return float(result["price"])



def price_option_crr_full(S0, K, r, sigma, T, N, option_type="call", q=0.0, style="european") -> Dict[str, object]:
    """
    Build the full stock and option lattices, then return a rich pricing report.

    This is the main dashboard-facing function.
    """
    stock_tree, dt, u, d, p = build_stock_tree(S0, sigma, r, T, N, q=q)
    option_tree = np.full_like(stock_tree, np.nan)

    # Terminal payoff at maturity
    for j in range(N + 1):
        terminal_spot = stock_tree[j, N]
        if option_type == "call":
            option_tree[j, N] = max(terminal_spot - K, 0.0)
        else:
            option_tree[j, N] = max(K - terminal_spot, 0.0)

    disc = math.exp(-r * dt)
    exercise_nodes: List[Tuple[int, int]] = []

    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            continuation = disc * (p * option_tree[j + 1, i + 1] + (1 - p) * option_tree[j, i + 1])
            intrinsic = max(stock_tree[j, i] - K, 0.0) if option_type == "call" else max(K - stock_tree[j, i], 0.0)

            if style == "american":
                option_tree[j, i] = max(continuation, intrinsic)
                if intrinsic > continuation:
                    exercise_nodes.append((j, i))
            else:
                option_tree[j, i] = continuation

    if N >= 1:
        delta = (option_tree[1, 1] - option_tree[0, 1]) / (stock_tree[1, 1] - stock_tree[0, 1])
    else:
        delta = float("nan")

    return {
        "price": float(option_tree[0, 0]),
        "delta": float(delta),
        "stock_tree": stock_tree,
        "option_tree": option_tree,
        "dt": float(dt),
        "u": float(u),
        "d": float(d),
        "p": float(p),
        "exercise_nodes": exercise_nodes,
    }
