import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kurtosis, normaltest
from statsmodels.tsa.stattools import acf
import os
import pandas as pd

def market_diagnostics(price_series, fundamental_series, volume_series, regimes=None, window=20, output_folder = 'diagnostics'):

    returns = np.diff(np.log(price_series))
    volatility = np.std(returns)
    price_diff = np.array(price_series) - np.array(fundamental_series)

    print("\n--- Market Diagnostics ---")
    print(f"Final Price: {price_series[-1]:.2f}")
    print(f"Final Fundamental: {fundamental_series[-1]:.2f}")
    print(f"Mean Return: {np.mean(returns):.5f}")
    print(f"Volatility (std of log returns): {volatility:.5f}")
    print(f"Kurtosis of Returns: {kurtosis(returns):.2f}")
    print(f"Normality test p-value: {normaltest(returns).pvalue:.5f}")

    acf_vals = acf(returns, nlags=10)
    acf_sq = acf(returns**2, nlags=10)

    print(f"ACF of returns (lags 1-5): {acf_vals[1:6]}")
    print(f"ACF of squared returns (lags 1-5): {acf_sq[1:6]}")

    # Plot: Price vs Fundamental
    plt.figure(figsize=(12, 4))
    plt.plot(price_series, label="Price", linewidth=1.5)
    plt.plot(fundamental_series, label="Fundamental", linestyle='--', alpha=0.7)
    if regimes:
        plt.title("Price vs Fundamental with Regimes")
    else:
        plt.title("Price vs Fundamental")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot: Price Deviation from Fundamental
    plt.figure(figsize=(8, 3))
    plt.plot(price_diff, label="Price - Fundamental", color='purple')
    plt.axhline(0, color='black', linestyle='--')
    plt.title("Price Deviation from Fundamental")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot: Rolling Volatility (for clustering)
    rolling_vol = np.array([np.std(returns[max(0, i - window):i + 1]) for i in range(len(returns))])
    plt.figure(figsize=(8, 3))
    plt.plot(rolling_vol, label=f"{window}-step Rolling Volatility", color='orange')
    plt.title("Volatility Clustering (Rolling Std of Returns)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot: Volume vs Price Change Magnitude
    price_changes = np.abs(np.diff(price_series))
    plt.figure(figsize=(6, 4))
    plt.scatter(volume_series[:len(price_changes)], price_changes, alpha=0.5)
    plt.xlabel("Volume")
    plt.ylabel("Price Change Magnitude")
    plt.title("Volume vs Price Movement")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

        # Calculate log returns
    returns = np.diff(np.log(price_series))
    squared_returns = returns ** 2

    # Save time series to CSV
    df = pd.DataFrame({
        'Price': price_series,
        'Fundamental': fundamental_series[0:len(price_series)],
        'Log_Returns': np.insert(returns, 0, 0)  # insert 0 at t=0 for length match
    })
    df.to_csv(os.path.join(output_folder, "test_results.csv"), index=False)

    # 1. Plot histogram of returns
    plt.figure(figsize=(6, 4))
    plt.hist(returns, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    plt.title("Histogram of Log Returns")
    plt.xlabel("Log Return")
    plt.ylabel("Density")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "returns_histogram.png"))
    plt.figure(figsize=(8, 4))
    plt.plot(price_series, label='Market Price', linewidth=1.8)
    plt.plot(fundamental_series, label='Fundamental Value', linewidth=1.8, linestyle='--')
    plt.title("Price vs Fundamental Value")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "price_vs_fundamental.png"))
    # === 5. Autocorrelation Functions ===
    lags = 30
    acf_returns = acf(returns, nlags=lags, fft=True)
    acf_sq_returns = acf(squared_returns, nlags=lags, fft=True)

    fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax[0].stem(range(lags + 1), acf_returns, basefmt=" ")
    ax[0].set_title("ACF of Log Returns")
    ax[0].set_ylabel("ACF")
    ax[0].grid(True)

    ax[1].stem(range(lags + 1), acf_sq_returns, basefmt=" ")
    ax[1].set_title("ACF of Squared Log Returns")
    ax[1].set_xlabel("Lag")
    ax[1].set_ylabel("ACF")
    ax[1].grid(True)

    plt.suptitle("Autocorrelation Function (ACF) Analysis", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(output_folder, "acf_returns.png"))
    # Regime-specific Volatility
    if regimes:
        regime_ids = sorted(set(regimes))
        print("\n--- Regime-based Stats ---")
        for r in regime_ids:
            indices = [i for i in range(1, len(regimes)) if regimes[i] == r]
            if len(indices) < 5:
                continue
            regime_returns = [returns[i-1] for i in indices if i > 0]
            print(f"Regime {r} | Count: {len(regime_returns)} | Mean Return: {np.mean(regime_returns):.4f} | Volatility: {np.std(regime_returns):.4f}")

