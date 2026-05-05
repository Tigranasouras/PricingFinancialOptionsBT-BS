# 📈 Option Pricing with Binomial Trees & Black–Scholes

**Language:** Python  
**Domain:** Quantitative Finance / Data Science  
**Platform:** Google Colab  
**Data Sources:** yfinance + FRED  
**Status:** In active development (research + experiments)

---

## 📌 Project Overview

This project builds a **fully reproducible option pricing pipeline** that connects:

- Financial theory  
- Real market data  
- Numerical methods  
- Statistical analysis  

The goal is to price **European call options** using the **Cox–Ross–Rubinstein (CRR) binomial tree model** and validate the results against the **Black–Scholes closed-form solution**.

The project treats option pricing as a **data science workflow**, combining:

- Data acquisition  
- Parameter estimation  
- Numerical simulation  
- Model validation  

This creates a complete bridge between **finance, mathematics, and computation**.

---

## 🎯 Core Goals

This project investigates:

- How accurately the binomial model approximates Black–Scholes
- How binomial step count affects pricing error
- How volatility estimation impacts pricing
- The tradeoff between **accuracy vs computational cost**

---

## 📊 Key Features

- Real market data integration (stocks + interest rates)
- Binomial tree implementation from scratch
- Black–Scholes analytical pricing implementation
- Convergence analysis and error measurement
- Runtime and scalability analysis
- Fully reproducible notebook pipeline
- Visualization of pricing behavior and model convergence

---

## 🧠 Technical Implementation

### Financial Models Implemented

#### Cox–Ross–Rubinstein (CRR) Binomial Model
- Discrete-time stock price lattice
- Risk-neutral valuation
- Backward induction pricing
- Configurable number of steps (N)

#### Black–Scholes Model
- Closed-form European call pricing
- Used as the **benchmark / ground truth**

---

### Data Pipeline

The project uses **live financial data**:

- Stock prices → `yfinance`
- Risk-free rates → FRED
- Volatility estimated via:
  - Historical log returns
  - Implied volatility (optional)

---

## 🔬 Experiments & Analysis

### 1️⃣ Convergence Study
Compare binomial prices vs Black-Scholes by sweeping across step sizes:
N = {5, 10, 25, 50, 100, 200, 500}

Goal:
- Demonstrate numerical convergence
- Measure pricing error vs N

---

### 2️⃣ Volatility Sensitivity
Compare pricing using:

- Historical volatility
- Implied volatility

Shows how **parameter estimation affects pricing accuracy**.

---

### 3️⃣ Computational Efficiency
Measure runtime as tree depth increases.

Illustrates the tradeoff between:

- Computational cost  
- Pricing accuracy  

---

## 📈 Example Results

Example using Starbucks (SBUX):

| Metric | Value |
|---|---|
| Binomial Price | 6.2614 |
| Black-Scholes Price | 6.3382 |
| Relative Error | **1.21%** |

Even with a small number of steps, the binomial model closely matches the continuous solution.

---

## 🛠️ Tech Stack

- Python
- NumPy
- Pandas
- SciPy
- Matplotlib
- yfinance
- Google Colab

---

## 📂 Code Structure

option-pricing-binomial-bs
├── notebooks/ # Main research notebook

│ └── OptionPricingPipeline.ipynb

│

├── src/ # Core pricing & data modules

│ ├── binomial_model.py # CRR binomial tree implementation

│ ├── black_scholes.py # Analytical pricing model

│ ├── volatility.py # Volatility estimation utilities

│ └── data_loader.py # Market data acquisition

│

├── figures/ # Generated plots & visuals

├── requirements.txt # Project dependencies

└── README.md # Project documentation

---

## 📚 Skills Demonstrated

### Quantitative Finance
- Risk-neutral pricing
- Option valuation theory
- Volatility estimation
- Model validation

### Data Science & Numerical Methods
- Building reproducible pipelines
- Numerical convergence analysis
- Statistical parameter estimation
- Scientific visualization

### Software Engineering
- Modular Python architecture
- Reproducible research workflows
- Documentation and packaging for GitHub

---

## 🚀 Future Improvements

Planned extensions:

- American option pricing
- Monte Carlo simulation methods
- Greeks and hedging analysis
- Volatility surface modeling
- Stress testing and scenario analysis

---

---

## 🧠 Advanced Topics

This project incorporates several advanced data science techniques:

### 1. Online Database / API Integration (1 pts)
Market data is retrieved using yfinance and FRED APIs. This allows the model to operate on real-world financial data.

### 2. Markov Chains (0.5 pt)
The binomial model is a discrete-time stochastic process where each state depends only on the previous state, satisfying the Markov property.

### 3. Nonlinear Modeling (1.5 pts)
Option pricing is inherently nonlinear due to payoff functions such as max(S-K,0), which create asymmetric responses.

### 4. Interactive Visualization (1.5 pts)
Visualization tools are used to explore convergence, pricing behavior, and model outputs.

### 5. Error Analysis (0.5 pts)
The model is validated by comparing binomial outputs to Black-Scholes, computing absolute and relative error.

### 6. Feature Engineering (0.5 pts)
Volatility is estimated from historical log returns, and model parameters such as risk-neutral probabilities are derived.

Total: 4+ points satisfied

---

## 📫 Author

**Daron Baltazar**  
GitHub: https://github.com/Tigranasouras  
LinkedIn: https://www.linkedin.com/in/daron-baltazar/

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only** and does not constitute financial advice.
