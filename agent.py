import numpy as np


class Agent:
    def __init__(self, type, delay, window, alpha, price_noise, steepness, capital=10000):

        self.type = type
        self.delay = delay
        self.window = window
        self.alpha = alpha
        self.price_noise = price_noise
        self.steepness = -np.log((2 / (steepness + 1)) - 1)

        if self.type == 5:
            self.capital = 0
            self.steepness = steepness
            self.shares = 100
            self.initalportion = 0.05 * self.shares
        else:
            self.capital = capital
            self.shares = 0

        self.portfolio = self.capital + self.shares * 100
        self.portion = (self.shares * 100) / self.portfolio
        self.observed_portfolio = self.capital + self.shares * 100
        self.observed_portion = (self.shares * 100) / self.portfolio

    def create_order(self, price, fundemental):
        self.portfolio = self.capital + self.shares * price[-1]
        self.portion = (self.shares * price[-1]) / self.portfolio
        number_of_shares = 0

        if self.type == 5:
            if self.initalportion != 0:
                return [-self.initalportion, price[-1]]
            else:
                signal = (price[-1] - fundemental[-1]) / fundemental[-1]
                optportion = min(1 - np.clip(self.steepness * signal, 0, 1), 1)
                number_of_shares = (optportion - self.portion) * self.portfolio / price[-1]
                return [number_of_shares, price[-1]]

        if (len(price) > self.delay):
            end = len(price) - self.delay
            start = max(0, end - self.window)
            pricearr = price[start:end]
            fundarr = fundemental[start:end]
            self.observed_portfolio = self.capital + self.shares * pricearr[-1]
            self.observed_portion = (self.shares * pricearr[-1]) / self.portfolio
            Predicted = 0
            if self.type == 1:
                Predicted = np.average(pricearr) + self.price_noise
            if self.type == 2:
                Predicted = (pricearr[-1] - pricearr[0]) / len(pricearr) + self.price_noise +pricearr[-1]
            if self.type == 3:
                Predicted = (fundarr[-1] - fundarr[0]) / len(fundarr) + self.price_noise + fundarr[-1]

            signal = (Predicted - pricearr[-1]) / pricearr[-1]
            optportion = 2 * (1 / (1 + np.exp(-self.steepness * signal))) - 1
            number_of_shares = (optportion - self.observed_portion) * self.observed_portfolio / pricearr[-1]
            return [number_of_shares,(self.alpha*Predicted+(1-self.alpha)*pricearr[-1])]
        else:
            return[0,0]

    def update(self,order):
        if self.type ==5 and self.initalportion != 0:
            self.initalportion  = self.initalportion + order[0]
        self.shares += order[0]
        self.capital += -order[0]*order[1]


