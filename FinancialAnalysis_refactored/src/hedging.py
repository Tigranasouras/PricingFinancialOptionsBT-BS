"""
hedging.py
==========

Lightweight hedge-calculation helpers for the Streamlit dashboard.

These functions are intentionally simple because the project focuses on
first-order (delta-based) intuition rather than a full trading engine.
"""

from __future__ import annotations

from typing import Dict

from src.models import CONTRACT_SIZE



def hedge_summary(delta: float, contracts: int) -> Dict[str, float]:
    """
    Convert option delta into an approximate stock hedge requirement.

    For a standard listed equity option, one contract typically controls
    100 shares.
    """
    shares = float(delta) * CONTRACT_SIZE * int(contracts)
    return {
        "delta": float(delta),
        "contracts": int(contracts),
        "shares_to_hedge": float(shares),
    }
