# fundamental_model.py

import numpy as np
import random

class FundamentalScore:
    def __init__(self, initial_score=100.0, impact_coeff=0.00001):
        # Hardcoded regime parameters (mean and vol for daily returns)
        self.regime_params = {
            0: {'mu': 0.0007015040171695818, 'sigma': 0.004093662304506883},   # Low volatility
            1: {'mu': 0.0003544907479842397, 'sigma': 0.007379604031489026},    # Mid volatility
            2: {'mu': 0.0008542049452281508, 'sigma': 0.02608454782305211}     # High volatility
        }
        self.regime_probs = [0.3, 0.4, 0.3]  # Adjustable transition likelihood
        self.current_regime = random.choices(
            population=list(self.regime_params.keys()),
            weights=self.regime_probs,
            k=1
        )[0]

        self.score = initial_score
        self.impact_coeff = impact_coeff

    def switch_regime(self):
        # Regime switching via a categorical draw
        self.current_regime = np.random.choice(
            list(self.regime_params.keys()), p=self.regime_probs
        )

    def step(self, company_flow=0.0, dt=1, auto_switch=True):
        if auto_switch:
            self.switch_regime()

        mu = self.regime_params[self.current_regime]['mu']
        sigma = self.regime_params[self.current_regime]['sigma']
        dW = np.random.normal(0, np.sqrt(dt))
        geometric_update = ((mu) - 0.5 * sigma**2) * dt + sigma * dW + company_flow*self.impact_coeff
        self.score *= np.exp(geometric_update)


        return self.score, self.current_regime
