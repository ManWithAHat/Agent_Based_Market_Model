import requests
import numpy as np
from main import run_simulation

url1 = "https://data.alpaca.markets/v2/stocks/bars?symbols=MP&timeframe=1T&start=2025-07-17T00%3A00%3A00Z&end=2025-07-18T00%3A00%3A00Z&limit=1000&adjustment=raw&feed=iex&sort=asc"
url2 = "https://data.alpaca.markets/v2/stocks/bars?symbols=MP&timeframe=1T&start=2025-07-17T00%3A00%3A00Z&end=2025-07-18T00%3A00%3A00Z&limit=1000&adjustment=raw&feed=sip&sort=asc"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": "PKV73S7SPHX53Y7FWSR9",
    "APCA-API-SECRET-KEY": "1VM8UesJfSJ8ZtBu47pJNV0H13sYi52BfAb1yq9T"
}

response = requests.get(url1, headers=headers)
response2 = requests.get(url2, headers=headers)

print(response.json())
print(response2.json())

time = [i['t'] for i in response.json()['bars']['MP']]
price1 = ([i['c'] for i in response.json()['bars']['MP']])
price2 = ([i['c'] for i in response2.json()['bars']['MP'] if i['t'] in time])
print(len(price1))
print(len(price2))


def normalize_prices(prices):
    prices = np.array(prices)
    return (prices / prices[0]) * 100


price1 = normalize_prices(price1)
price2 = normalize_prices(price2)

# Price 2 is non IEX data

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import kurtosis, skew
from statsmodels.tsa.stattools import acf


def compute_metrics(price_series):
    prices = np.array(price_series)
    returns = np.diff(np.log(prices))

    metrics = {
        "total_return": (prices[-1] / prices[0]) - 1,
        "mean_return": np.mean(returns),
        "volatility": np.std(returns),
        "kurtosis": kurtosis(returns),
        "skewness": skew(returns),
        "max_drawdown": np.min(prices / np.maximum.accumulate(prices) - 1),
        "acf_returns": acf(returns, nlags=20, fft=False),
        "acf_squared": acf(returns ** 2, nlags=20, fft=False),
        "returns": returns
    }

    return metrics


def compare_price_series(price1, price2, label1="Series 1", label2="Series 2"):
    # Convert to np arrays
    price1 = np.array(price1)
    price2 = np.array(price2)

    # Align series length
    length = min(len(price1), len(price2))
    price1 = price1[:length]
    price2 = price2[:length]

    # Compute metrics
    metrics1 = compute_metrics(price1)
    metrics2 = compute_metrics(price2)

    # Compute RMSE
    price_rmse = np.sqrt(np.mean((price1 - price2) ** 2))
    return_rmse = np.sqrt(np.mean((metrics1["returns"] - metrics2["returns"]) ** 2))

    # ACF difference (L2 norm)
    acf_diff = np.linalg.norm(metrics1["acf_returns"] - metrics2["acf_returns"])
    acf_sq_diff = np.linalg.norm(metrics1["acf_squared"] - metrics2["acf_squared"])

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(price1, label=label1, color="blue")
    plt.plot(price2, label=label2, color="red")
    plt.title(f"Price Series Comparison: {label1} vs {label2}")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("==== Metric Differences ====")
    print(f"Price RMSE: {price_rmse:.4f}")
    print(f"Return RMSE: {return_rmse:.4f}")
    print(f"Return Kurtosis Difference: {metrics1['kurtosis'] - metrics2['kurtosis']:.4f}")
    print(f"Return Skewness Difference: {metrics1['skewness'] - metrics2['skewness']:.4f}")
    print(f"Volatility Difference: {metrics1['volatility'] - metrics2['volatility']:.4f}")
    print(f"Autocorrelation Difference: {acf_diff:.4f}")
    print(f"Volatility Clustering Difference: {acf_sq_diff:.4f}")
    print(f"Max Drawdown Diff: {metrics1['max_drawdown'] - metrics2['max_drawdown']:.4f}")
    print("============================")

    return {
        "price_rmse": price_rmse,
        "return_rmse": return_rmse,
        "acf_diff": acf_diff,
        "acf_sq_diff": acf_sq_diff,
        "vol_diff": metrics1['volatility'] - metrics2['volatility'],
        "kurt_diff": metrics1['kurtosis'] - metrics2['kurtosis'],
        "skew_diff": metrics1['skewness'] - metrics2['skewness'],
        "drawdown_diff": metrics1['max_drawdown'] - metrics2['max_drawdown'],
    }


compare_price_series(price1, price2,'MP (IEX Only)','MP (All Exchanges)')

param_config = {'impact_coeff': 0.00001, 'steepness_mean': 0.6, 'steepness_std': 0.15, 'delay_min': 1, 'delay_max': 5,
                'window_min': 5, 'window_max': 10, 'alpha_mean': 0.1, 'alpha_std': 0.9, 'price_noise_std': 0.05,
                'company_agent_steepness': 0.2, 'n_mean_reversion_agents': 30, 'n_trend_agents': 30,
                'n_fundamental_agents': 30, 'random_seed': 3, 'steps': 409}

sim_price1 = run_simulation(param_config,policy=True)
sim_price2 = run_simulation(param_config)

compare_price_series(sim_price1,sim_price2, 'Simulated (IEX)','Simulated (Non-IEX)')

print(compute_metrics(price1))
print(compute_metrics(sim_price1))

