# A Multi-Agent Market Simulation with Fundamental and Behavioral Dynamics

This repository contains the full implementation of the simulation model described in the paper  
**"A Multi-Agent Market Simulation with Fundamental and Behavioral Dynamics"** by *Aarush Singh (2025)*.

The project explores how heterogeneous trading behaviors — trend-following, mean-reversion, and fundamental value investing — interact to produce emergent market properties such as volatility clustering, heavy-tailed returns, and mispricing from intrinsic value.  
It also includes policy experiments replicating structural interventions such as exchange speed bumps and long-term holding incentives.

---

## 🧠 Overview

The simulation models a synthetic equity market consisting of multiple behavioral agent types that submit buy/sell orders based on local decision rules.  
Prices are determined through a supply-demand clearing mechanism, while the asset’s fundamental value evolves according to a **Geometric Brownian Motion (GBM)**.

Key emergent behaviors:
- Fat-tailed return distributions  
- Volatility clustering  
- Fundamental mispricing and convergence  
- Liquidity freezes under extreme shocks  

---

## ⚙️ Structure

├── main.py # Entry point of the simulation
├── agents.py # Agent class definitions and decision rules
├── market.py # Market clearing and price formation logic
├── utils.py # Statistical analysis and plotting functions
├── /results # Auto-generated charts and metrics
├── requirements.txt # Python dependencies
└── README.md # This file


## 🚀 Quick Start

### 1. Clone or Fork the Repository

git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
2. Install Dependencies
You can use a virtual environment (recommended):

bash
Copy code
pip install -r requirements.txt
3. Run the Simulation
Open main.py and modify the dictionary at the top named param_config to set your desired parameters.

Example:

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
Then run:

bash
Copy code
python main.py
Output plots and metrics will be generated in the /diagnostics folder.

