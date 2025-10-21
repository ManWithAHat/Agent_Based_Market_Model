# 🧠 A Multi-Agent Market Simulation with Fundamental and Behavioral Dynamics

This repository contains the full implementation of the simulation model described in the paper  
**“A Multi-Agent Market Simulation with Fundamental and Behavioral Dynamics”** by *Aarush Singh (2025)*.

The project explores how heterogeneous trading behaviors — **trend-following**, **mean-reversion**, and **fundamental value investing** — interact to produce emergent market features such as volatility clustering, heavy-tailed returns, and mispricing from intrinsic value.  
It also includes **policy experiments** replicating real-world structural interventions such as **exchange speed bumps** and **long-term holding incentives**.

---

## 🧩 Overview

The model simulates a synthetic equity market in discrete time.  
Agents trade based on behavioral heuristics, and prices are determined by a supply-demand clearing mechanism.  
The fundamental value evolves via a **Geometric Brownian Motion (GBM)** process with optional feedback from a company agent.

### Core Emergent Properties
- Fat-tailed return distributions  
- Volatility clustering  
- Mispricing and price reversion to fundamentals  
- Illiquidity and price stagnation during large shocks  

---

## ⚙️ Model Structure

**Key Components**
- `main.py` — Entry point and simulation runner  
- `agents.py` — Definitions of agent behaviors (trend, mean-reversion, fundamental, company)  
- `market.py` — Market-clearing mechanism and price formation  
- `utils.py` — Helper functions for plotting and analysis  
- `/results/` — Auto-generated charts and metrics  
- `requirements.txt` — Dependencies  

---

## 🚀 Running the Simulation

### 1. Clone or Fork the Repository

- git clone https://github.com/ManWithAHat/Agent_Based_Market_Model.git
- cd Agent_Based_Market_Model

2. Install Dependencies

Copy code
pip install -r requirements.txt

3. Configure Parameters
Open main.py and locate the dictionary named param_config near the top of the file.
This dictionary defines all model parameters (agent counts, volatility, delay windows, etc.):

python
Copy code
param_config = {
    'impact_coeff': 0.00001,
    'steepness_mean': 0.6,
    'steps': 409,
    'steepness_std': 0.15,
    'delay_min': 1,
    'delay_max': 5,
    'window_min': 5,
    'window_max': 10,
    'alpha_mean': 0.1,
    'alpha_std': 0.9,
    'price_noise_std': 0.05,
    'company_agent_steepness': 0.2,
    'n_mean_reversion_agents': 30,
    'n_trend_agents': 30,
    'n_fundamental_agents': 30,
    'random_seed': 3
}
4. Run the Simulation

Copy code
python main.py
All charts and metrics (price vs. fundamental, return histograms, autocorrelations) are automatically saved in the /results directory.
