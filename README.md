# 📈 Interactive Option Pricing and Hedging Dashboard

**Language:** Python  
**Domain:** Quantitative Finance / Data Science  
**Framework:** Streamlit + Scientific Python  
**Data Sources:** Yahoo Finance (`yfinance`) + FRED  
**Author:** Daron Baltazar  
**Institution:** Belmont University – Finance & Computer Science  
**Status:** Research + Interactive Dashboard Prototype

---

# 📌 Project Overview

This project builds an interactive financial decision-support system that combines:

- Quantitative Finance
- Numerical Methods
- Stochastic Modeling
- Data Science Workflows
- Interactive Visualization
- Real Market Data

The system prices financial options using both the:

- Cox–Ross–Rubinstein (CRR) Binomial Tree Model
- Black–Scholes Analytical Model

and compares their behavior using real financial market data.

The project investigates:

- Numerical convergence
- Pricing sensitivity
- Nonlinear payoff behavior
- Early exercise decisions
- Delta hedging
- Scenario analysis

while demonstrating how theoretical financial mathematics can be translated into a real computational workflow.

---

# 🎯 Project Objectives

The goals of the project are to:

- Build a reproducible option pricing pipeline
- Compare discrete vs continuous pricing models
- Analyze convergence behavior
- Evaluate pricing sensitivity under market shocks
- Explore American option early exercise decisions
- Translate pricing outputs into hedging insights
- Demonstrate practical quantitative finance workflows

---

# 📊 Financial Models Implemented

## 1️⃣ Cox–Ross–Rubinstein (CRR) Binomial Model

The CRR model is implemented from scratch using:

- Discrete-time stock price lattices
- Recombining tree structures
- Risk-neutral valuation
- Backward induction pricing
- Configurable binomial step counts

The implementation supports:

- European options
- American options
- Tree visualization
- Early exercise detection
- Scenario analysis

### Key Equations

#### Time Step

\[
\Delta t = \frac{T}{N}
\]

#### Up / Down Factors

\[
u = e^{\sigma \sqrt{\Delta t}}
\]

\[
d = \frac{1}{u}
\]

#### Risk-Neutral Probability

\[
p = \frac{e^{(r-q)\Delta t} - d}{u-d}
\]

#### American Option Decision Rule

\[
V = \max(\text{hold}, \text{exercise})
\]

---

## 2️⃣ Black–Scholes Model

The Black–Scholes model is implemented as the continuous-time benchmark.

It is used to:

- Validate numerical convergence
- Compare pricing accuracy
- Measure approximation error

The Black–Scholes model assumes:

- European exercise
- Constant volatility
- Continuous trading
- Frictionless markets

---

# 🔬 Data Pipeline

The project integrates live financial market data.

| Data Type | Source |
|---|---|
| Stock Prices | Yahoo Finance |
| Treasury Rates | FRED |
| Volatility | Historical Log Returns |

The workflow:

1. Fetch market data
2. Estimate volatility
3. Build stock price lattice
4. Compute option payoffs
5. Apply backward induction
6. Compare against Black–Scholes
7. Run scenario analysis
8. Compute hedge ratios

---

# ⚙️ Project Architecture

The project uses a modular architecture separating:

- Computational logic
- Visualization
- Data acquisition
- UI components

```text
option-pricing-dashboard/
│
├── app.py                      # Streamlit dashboard UI
│
├── src/
│   ├── binomial_model.py       # CRR pricing engine
│   ├── black_scholes.py        # Black–Scholes model
│   ├── volatility.py           # Volatility estimation
│   ├── hedging.py              # Delta hedge calculations
│   ├── scenarios.py            # Scenario analysis
│   ├── tree_visualization.py   # Lattice visualization
│   └── data_loader.py          # Market data retrieval
│
├── figures/                    # Generated visualizations
├── notebooks/                  # Research notebooks
├── requirements.txt
└── README.md


```

# 📂 Where to Find Key Components

| Component | File |
|---|---|
| CRR Pricing Logic | `src/binomial_model.py` |
| Black–Scholes Pricing | `src/black_scholes.py` |
| Volatility Estimation | `src/volatility.py` |
| Delta / Hedging Logic | `src/hedging.py` |
| Scenario Analysis | `src/scenarios.py` |
| Tree Visualization | `src/tree_visualization.py` |
| Streamlit Dashboard | `app.py` |

The codebase is documented internally with comments and docstrings explaining pricing logic, tree construction, and numerical methods.

---

# 🔬 Experiments & Analysis

 1️⃣ Convergence Analysis

The project compares CRR binomial prices against Black–Scholes across varying step counts:

`N = {5, 10, 25, 50, 100, 200, 500}`

This demonstrates numerical convergence:

**Binomial Price → Black–Scholes Price**

 Metrics Evaluated

- Absolute Error
- Relative Error
- Runtime Performance

---

 2️⃣ Scenario Analysis

The dashboard evaluates pricing sensitivity under shocked market conditions.

 Example Shocks

- Stock Price ±5%
- Stock Price ±10%

 Outputs Include

- Repriced option values
- Profit / Loss vs baseline
- Sensitivity analysis
- Nonlinear pricing behavior

---

 3️⃣ Hedging Analysis

The project computes option delta and translates it into hedge ratios.

 Hedge Equation
 
`Shares to Hedge = Delta × 100 × Contracts`

This demonstrates how option pricing models can support portfolio risk management.

---

 4️⃣ American Option Early Exercise

The project evaluates:

- Continuation value
- Intrinsic value

at every node in the lattice.

This enables:

- Early exercise detection
- Path-dependent pricing
- American option valuation

---

# 📈 Example Results

Example using Starbucks (SBUX - around presentation day):

| Metric | Value |
|---|---|
| Binomial Price | 14.2849 |
| Black–Scholes Price | 14.2711 |
| Absolute Error | 0.0138 |
| Relative Error | 0.25% |

 Results Show That

- The CRR model converges toward Black–Scholes
- Pricing is highly sensitive to volatility
- Option behavior is nonlinear
- American puts frequently produce early exercise regions

---

# 📚 Key Technical Concepts Demonstrated

 Quantitative Finance

- Risk-neutral valuation
- Delta hedging
- Option valuation theory
- Early exercise analysis
- Sensitivity analysis

---

 Data Science & Numerical Methods

- Numerical simulation
- Convergence analysis
- Statistical parameter estimation
- Scientific visualization
- Scenario analysis

---

 Software Engineering

- Modular architecture
- Reproducible workflows
- Interactive dashboards
- Separation of UI and computational logic

---

# ⚠️ Limitations

Current limitations include:

- Historical volatility instead of implied volatility
- Simplified market assumptions
- No transaction costs
- Black–Scholes assumes European exercise
- No stochastic volatility modeling

---

# 🚀 Future Improvements

Planned extensions include:

- Monte Carlo simulation
- Greeks beyond delta
- Volatility surface modeling
- Portfolio-level aggregation
- Real-time deployment
- GPU acceleration
- Stochastic volatility models

---

# 🛠️ Tech Stack

- Python
- NumPy
- Pandas
- SciPy
- Matplotlib
- Streamlit
- yfinance
- FRED API

---

# 🚀 How to Run

```text

 1️⃣ Install dependencies
pip install -r requirements.txt


 2️⃣ Launch the dashboard
streamlit run app.py

 3️⃣ Open in browser
Streamlit will automatically launch a local server

```

# 🧠 Advanced Topics

This project incorporates several advanced data science techniques:

1. Online Database / API Integration (1 pts)
Market data is retrieved using yfinance and FRED APIs. This allows the model to operate on real-world financial data.

2. Markov Chains (0.5 pt)
The binomial model is a discrete-time stochastic process where each state depends only on the previous state, satisfying the Markov property.

3. Nonlinear Modeling (1.5 pts)
Option pricing is inherently nonlinear due to payoff functions such as max(S-K,0), which create asymmetric responses.

4. Interactive Visualization (1.5 pts)
Visualization tools are used to explore convergence, pricing behavior, and model outputs.

5. Error Analysis (0.5 pts)
The model is validated by comparing binomial outputs to Black-Scholes, computing absolute and relative error.

6. Feature Engineering (0.5 pts)
Volatility is estimated from historical log returns, and model parameters such as risk-neutral probabilities are derived.

Total: 4+ points satisfied

---

# 📫 Author

**Daron Baltazar**  
GitHub: https://github.com/Tigranasouras  
LinkedIn: https://www.linkedin.com/in/daron-baltazar/

---

# ⚠️ Disclaimer

This project is for **educational and research purposes only** and does not constitute financial advice.
