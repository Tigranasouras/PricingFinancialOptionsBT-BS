"""
black_scholes.py
================

Black–Scholes Closed-Form Option Pricing Model
Author: Daron Baltazar

This module implements the Black–Scholes formula for pricing
European options.

The Black–Scholes model assumes:
• Stock prices follow geometric Brownian motion
• Markets are frictionless and arbitrage-free
• Volatility and interest rates are constant
• Options are European (exercise only at maturity)

The resulting formula provides the *continuous-time benchmark*
used to validate the binomial model.
"""

from __future__ import annotations

from math import erf, exp, log, sqrt



def norm_cdf(x: float) -> float:
    """
    Standard Normal Cumulative Distribution Function.

    We implement the CDF using the error function (erf)
    to avoid requiring SciPy as a dependency.
    """
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))



def price_option(S0, K, r, sigma, T, option_type="call", q=0.0):
    """
    Black–Scholes price of a European option.
    """
    if T <= 0:
        return max(S0 - K, 0.0) if option_type == "call" else max(K - S0, 0.0)

    if sigma <= 0:
        forward_intrinsic = S0 * exp(-q * T) - K * exp(-r * T)
        return max(forward_intrinsic, 0.0) if option_type == "call" else max(-forward_intrinsic, 0.0)

    d1 = (log(S0 / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    if option_type == "call":
        return S0 * exp(-q * T) * norm_cdf(d1) - K * exp(-r * T) * norm_cdf(d2)
    return K * exp(-r * T) * norm_cdf(-d2) - S0 * exp(-q * T) * norm_cdf(-d1)



def option_delta(S0, K, r, sigma, T, option_type="call", q=0.0):
    """
    Black–Scholes delta of a European option.

    Delta measures the first-order sensitivity of the option value to the
    underlying stock price.
    """
    if T <= 0 or sigma <= 0:
        if option_type == "call":
            return 1.0 if S0 > K else 0.0
        return -1.0 if S0 < K else 0.0

    d1 = (log(S0 / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    if option_type == "call":
        return exp(-q * T) * norm_cdf(d1)
    return exp(-q * T) * (norm_cdf(d1) - 1.0)
