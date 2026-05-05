# -*- coding: utf-8 -*-
"""
app.py
======

Streamlit user interface for the Interactive Option Pricing and Hedging Dashboard.

Design goal
-----------
This file now acts primarily as the *presentation / orchestration layer*.
Core financial logic has been moved into dedicated modules so the project
keeps the modular documentation style established in the original write-up.

UI responsibilities:
• collect sidebar inputs
• call data / model / experiment helpers
• display outputs in an academic dashboard format

Model responsibilities now live in:
• src/data_loader.py
• src/volatility.py
• src/fred_loader.py
• src/binomial_model.py
• src/black_scholes.py
• src/experiments.py
• src/hedging.py
• src/tree_visualization.py
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from src.binomial_model import price_option_crr, price_option_crr_full
from src.black_scholes import option_delta, price_option
from src.data_loader import download_price_history, extract_close_series
from src.experiments import build_scenario_table, convergence_experiment, plot_convergence
from src.hedging import hedge_summary
from src.models import CONTRACT_SIZE, MarketInputs
from src.tree_visualization import lattice_to_dataframe
from src.volatility import historical_volatility_from_series


@st.cache_data(show_spinner=False)
def load_market_snapshot(ticker: str, history_period: str):
    """
    Cached market-data loader for the Streamlit dashboard.

    Returns
    -------
    tuple[pd.DataFrame, pd.Series, float, float]
        Historical table, close series, current spot, and historical sigma.
    """
    hist = download_price_history(ticker, period=history_period)
    close = extract_close_series(hist)
    spot = float(close.iloc[-1])
    sigma_hist = historical_volatility_from_series(close)
    return hist, close, spot, sigma_hist



def render_methodology_tab() -> None:
    """Render the methodology / academic framing section."""
    st.subheader("Methodology")
    st.markdown(
        r"""
        ### CRR Binomial Model
        Time is divided into discrete steps:

        $$
        \, \Delta t = \frac{T}{N}
        $$

        Up/down factors are:

        $$
        u = e^{\sigma \sqrt{\Delta t}}, \qquad d = \frac{1}{u}
        $$

        Risk-neutral probability:

        $$
        p = \frac{e^{(r-q)\Delta t} - d}{u-d}
        $$

        For a European option, backward induction uses only the discounted continuation value.
        For an American option, the model compares continuation value to immediate exercise:

        $$
        V = \max(\text{hold}, \text{exercise})
        $$

        ### Black–Scholes Benchmark
        The European Black–Scholes model provides a closed-form benchmark for comparison.

        ### Academic framing
        This dashboard is a **research prototype** designed to demonstrate how pricing,
        sensitivity analysis, and scenario-based hedging workflows can be integrated into a
        reproducible decision-support tool.
        """
    )

    st.markdown(
        """
        **Limitations**
        - Historical volatility is only one possible volatility estimate.
        - Black–Scholes is strictly a European benchmark.
        - This is not a production trading engine; it is an academic hedging dashboard.
        """
    )



def main() -> None:
    """Launch the Streamlit dashboard."""
    st.set_page_config(page_title="Option Pricing & Hedging Dashboard", layout="wide")
    st.title("Interactive Option Pricing and Hedging Dashboard")
    st.caption("Academic decision-support prototype using CRR binomial trees, Black–Scholes, and live market data.")

    with st.sidebar:
        st.header("Market & Contract Inputs")
        ticker = st.text_input("Ticker", value="SBUX").upper().strip()
        history_period = st.selectbox("History window for volatility", ["3mo", "6mo", "1y", "2y", "5y"], index=2)
        option_type = st.selectbox("Option Type", ["call", "put"])
        style = st.selectbox("Exercise Style", ["european", "american"])

        st.subheader("Model Inputs")
        strike = st.number_input("Strike (K)", min_value=1.0, value=100.0, step=1.0)
        maturity_days = st.slider("Maturity (days)", min_value=7, max_value=730, value=90, step=1)
        dividend_yield = st.number_input("Dividend Yield (q)", min_value=0.0, max_value=0.25, value=0.0, step=0.005, format="%.3f")
        rate = st.number_input("Risk-Free Rate (r)", min_value=0.0, max_value=0.20, value=0.045, step=0.0025, format="%.4f")
        steps = st.slider("Binomial Steps (N)", min_value=3, max_value=500, value=100, step=1)
        contracts = st.number_input("Contracts", min_value=1, value=1, step=1)

        st.subheader("Volatility")
        vol_method = st.radio("Volatility Input", ["Historical from yfinance", "Manual"], index=0)
        manual_sigma = (
            st.number_input("Manual Sigma", min_value=0.01, max_value=2.0, value=0.25, step=0.01)
            if vol_method == "Manual"
            else None
        )

    try:
        _hist, _close, spot, sigma_hist = load_market_snapshot(ticker, history_period)
    except Exception as exc:
        st.error(f"Could not load market data: {exc}")
        st.stop()

    sigma = float(manual_sigma) if vol_method == "Manual" else float(sigma_hist)
    inputs = MarketInputs(
        ticker=ticker,
        spot=float(spot),
        strike=float(strike),
        rate=float(rate),
        sigma=float(sigma),
        maturity_years=float(maturity_days / 365.0),
        dividend_yield=float(dividend_yield),
        steps=int(steps),
        option_type=option_type,
        style=style,
    )

    bin_result = price_option_crr_full(
        inputs.spot,
        inputs.strike,
        inputs.rate,
        inputs.sigma,
        inputs.maturity_years,
        inputs.steps,
        option_type=inputs.option_type,
        q=inputs.dividend_yield,
        style=inputs.style,
    )

    bs_price = price_option(
        inputs.spot,
        inputs.strike,
        inputs.rate,
        inputs.sigma,
        inputs.maturity_years,
        option_type=inputs.option_type,
        q=inputs.dividend_yield,
    )
    bs_delta = option_delta(
        inputs.spot,
        inputs.strike,
        inputs.rate,
        inputs.sigma,
        inputs.maturity_years,
        option_type=inputs.option_type,
        q=inputs.dividend_yield,
    )
    hedge = hedge_summary(bin_result["delta"], int(contracts))

    pricing_tab, hedge_tab, scenario_tab, trees_tab, method_tab = st.tabs(
        ["Pricing", "Hedge", "Scenarios", "Trees", "Methodology"]
    )

    with pricing_tab:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Spot (S₀)", f"{inputs.spot:.2f}")
        col2.metric("Sigma (σ)", f"{inputs.sigma:.2%}")
        col3.metric("Binomial Price", f"{bin_result['price']:.4f}")
        col4.metric("Black–Scholes", f"{bs_price:.4f}")

        err_abs = abs(bin_result["price"] - bs_price)
        err_pct = err_abs / abs(bs_price) if bs_price != 0 else float("nan")

        c1, c2, c3 = st.columns(3)
        c1.metric("Absolute Error vs BS", f"{err_abs:.4f}")
        c2.metric("Relative Error vs BS", f"{err_pct:.2%}" if pd.notna(err_pct) else "N/A")
        c3.metric("Binomial Delta", f"{bin_result['delta']:.4f}")

        st.subheader("Market Snapshot")
        snap = pd.DataFrame(
            {
                "Ticker": [inputs.ticker],
                "Latest Close": [round(inputs.spot, 2)],
                "Strike": [inputs.strike],
                "Maturity (days)": [maturity_days],
                "Rate": [inputs.rate],
                "Dividend Yield": [inputs.dividend_yield],
                "Volatility Method": [vol_method],
                "Historical Sigma": [round(sigma_hist, 4)],
            }
        )
        st.dataframe(snap, use_container_width=True)

        if inputs.style == "european":
            Ns = [5, 10, 25, 50, 100, 200, 500]
            bs_benchmark, bin_prices, _errors = convergence_experiment(
                inputs.spot,
                inputs.strike,
                inputs.rate,
                inputs.sigma,
                inputs.maturity_years,
                Ns,
                option_type=inputs.option_type,
                q=inputs.dividend_yield,
            )
            st.pyplot(plot_convergence(Ns, bin_prices, bs_benchmark, save_path="figures/convergence.png"))
        else:
            st.info("Convergence to Black–Scholes is shown only for European options, since Black–Scholes is a European closed-form benchmark.")

    with hedge_tab:
        st.subheader("Hedge Ratio")
        a, b, c = st.columns(3)
        a.metric("Root-Node Delta", f"{hedge['delta']:.4f}")
        b.metric("Contracts", f"{int(hedge['contracts'])}")
        c.metric("Shares to Hedge", f"{hedge['shares_to_hedge']:.2f}")

        st.markdown(
            """
            **Interpretation**

            - Delta measures how much the option price changes for a small move in the stock.
            - A hedge fund or portfolio manager can use delta to estimate how many shares are needed to offset first-order stock-price risk.
            - For a standard listed options contract, one contract typically controls **100 shares**.
            """
        )

        hedge_df = pd.DataFrame(
            {
                "Model": ["Binomial", "Black–Scholes"],
                "Delta": [round(bin_result["delta"], 4), round(bs_delta, 4)],
                "Shares per Contract": [
                    round(bin_result["delta"] * CONTRACT_SIZE, 2),
                    round(bs_delta * CONTRACT_SIZE, 2),
                ],
            }
        )
        st.dataframe(hedge_df, use_container_width=True)

    with scenario_tab:
        st.subheader("Scenario Analysis")
        st.markdown("Shock the underlying spot price and compare repriced values.")
        shocks = [-0.10, -0.05, 0.00, 0.05, 0.10]

        def binomial_scenario_price(S0, K, r, sigma, T, option_type="call", q=0.0):
            return price_option_crr(
                S0,
                K,
                r,
                sigma,
                T,
                inputs.steps,
                option_type=option_type,
                q=q,
                style=inputs.style,
            )

        bin_scen = build_scenario_table(inputs, binomial_scenario_price, shocks)
        bs_scen = build_scenario_table(inputs, price_option, shocks)

        left, right = st.columns(2)
        with left:
            st.markdown("**Binomial Scenario Table**")
            st.dataframe(bin_scen, use_container_width=True)
        with right:
            st.markdown("**Black–Scholes Scenario Table**")
            st.dataframe(bs_scen, use_container_width=True)

    with trees_tab:
        st.subheader("Lattice Views")
        tree_cols = st.columns(2)
        with tree_cols[0]:
            st.markdown("**Stock Price Tree**")
            st.dataframe(lattice_to_dataframe(bin_result["stock_tree"], decimals=2), use_container_width=True, height=350)
        with tree_cols[1]:
            st.markdown("**Option Value Tree**")
            st.dataframe(lattice_to_dataframe(bin_result["option_tree"], decimals=4), use_container_width=True, height=350)

        if inputs.style == "american":
            st.markdown(f"**Early exercise nodes found:** {len(bin_result['exercise_nodes'])}")
            if bin_result["exercise_nodes"]:
                st.write(bin_result["exercise_nodes"][:20])

    with method_tab:
        render_methodology_tab()


if __name__ == "__main__":
    main()
