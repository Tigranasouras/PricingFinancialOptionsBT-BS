"""
tree_visualization.py
=====================

Utilities for building and visualizing CRR binomial trees.

Includes:
- Building stock and option value lattices (CRR)
- Heatmap-style lattice visualization
- Node/edge "tree look" visualization with values encoded by color
- Maturity payoff comparison: intrinsic payoff vs option value at maturity
- Streamlit-friendly lattice table formatting
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.binomial_model import price_option_crr_full



def build_crr_trees(S0, K, r, sigma, T, N, option_type="call", q=0.0, american=False):
    """
    Build full CRR stock and option value lattices.
    """
    style = "american" if american else "european"
    result = price_option_crr_full(S0, K, r, sigma, T, N, option_type=option_type, q=q, style=style)
    return result["stock_tree"], result["option_tree"], result["dt"], result["u"], result["d"], result["p"]



def lattice_to_dataframe(tree: np.ndarray, decimals: int = 2) -> pd.DataFrame:
    """
    Convert a lattice array into a labeled pandas DataFrame for Streamlit.
    """
    df = pd.DataFrame(tree, columns=[f"t={i}" for i in range(tree.shape[1])])
    df.index = [f"up={i}" for i in range(tree.shape[0])]
    return df.round(decimals)



def plot_stock_lattice(S_lattice, title, save_path=None, annotate=True, value_fmt="{:.2f}"):
    """
    Plot a CRR stock-price lattice in a classic connected-node tree style.
    """
    N = S_lattice.shape[1] - 1
    plt.figure(figsize=(12, 7))

    for i in range(N):
        for j in range(i + 1):
            x, y = i, j - i / 2
            x_down, y_down = i + 1, j - (i + 1) / 2
            x_up, y_up = i + 1, (j + 1) - (i + 1) / 2
            plt.plot([x, x_down], [y, y_down], linewidth=1.5)
            plt.plot([x, x_up], [y, y_up], linewidth=1.5)

    for i in range(N + 1):
        for j in range(i + 1):
            x = i
            y = j - i / 2
            plt.scatter(x, y, s=70)
            if annotate:
                plt.text(x, y + 0.08, value_fmt.format(S_lattice[j, i]), ha="center", va="bottom", fontsize=10)

    plt.title(title)
    plt.xlabel("Time step (i)")
    plt.yticks([])
    plt.grid(True, alpha=0.25)

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()



def plot_payoff_vs_option_at_maturity(S_lattice, V_lattice, K, option_type="call", save_path=None):
    """
    Plot intrinsic payoff at maturity alongside option value at maturity.
    """
    N = S_lattice.shape[1] - 1
    ST = S_lattice[: N + 1, N]
    VT = V_lattice[: N + 1, N]

    if option_type == "call":
        payoff = np.maximum(ST - K, 0.0)
    else:
        payoff = np.maximum(K - ST, 0.0)

    order = np.argsort(ST)
    ST_sorted = ST[order]
    payoff_sorted = payoff[order]
    VT_sorted = VT[order]

    plt.figure(figsize=(8, 5))
    plt.plot(ST_sorted, payoff_sorted, marker="o", label="Intrinsic payoff at maturity")
    plt.plot(ST_sorted, VT_sorted, marker="x", linestyle="--", label="Option value at maturity (tree)")
    plt.title(f"Payoff vs Option Value at Maturity (N={N})")
    plt.xlabel("Stock price at maturity $S_T$")
    plt.ylabel("Value")
    plt.grid(True, alpha=0.3)
    plt.legend()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()
