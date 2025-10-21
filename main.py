
# sim_runner.py
import matplotlib.pyplot as plt
import numpy as np
import signal
import sys
import time
from agent import Agent
from exchange import Walrasion_auction
from diagnostics import market_diagnostics
from FundementalScore import FundamentalScore

param_config = {'impact_coeff': 0.00001, 'steepness_mean': 0.6,'steps': 409 ,'steepness_std': 0.15, 'delay_min': 1,
                'delay_max': 5, 'window_min': 5, 'window_max': 10, 'alpha_mean': 0.1, 'alpha_std': 0.9,
                'price_noise_std': 0.05, 'company_agent_steepness': 0.2, 'n_mean_reversion_agents': 15 ,
                'n_trend_agents': 15, 'n_fundamental_agents': 60, 'random_seed': 3}

def run_simulation(param_config,plot = False,  reference_prices=None,policy=False):
    np.random.seed(param_config.get("random_seed", 42))

    Score = FundamentalScore(
        initial_score=100.0 ,
        impact_coeff=param_config["impact_coeff"],
    )

    agents = []

    def truncated_normal(mean, std, low, high):
        return np.clip(np.random.normal(mean, std), low, high)

    def sample_response_at_100():
        return truncated_normal(param_config["steepness_mean"],
                                 param_config["steepness_std"], 0.2, 1.0)

    # Agent creation
    for _ in range(param_config["n_mean_reversion_agents"]):
        agents.append(Agent(
            type=1,
            delay=np.random.randint(param_config["delay_min"], param_config["delay_max"]),
            window=np.random.randint(param_config["window_min"], param_config["window_max"]+1),
            alpha=np.random.uniform(param_config["alpha_mean"], param_config["alpha_std"]),
            price_noise=np.random.normal(0, param_config["price_noise_std"]),
            steepness=sample_response_at_100()
        ))

    for _ in range(param_config["n_trend_agents"]):
        agents.append(Agent(
            type=2,
            delay=np.random.randint(param_config["delay_min"], param_config["delay_max"]),
            window=np.random.randint(param_config["window_min"], param_config["window_max"]+1),
            alpha=np.random.uniform(param_config["alpha_mean"], param_config["alpha_std"]),
            price_noise=np.random.normal(0, param_config["price_noise_std"]),
            steepness=sample_response_at_100()
        ))

    for _ in range(param_config["n_fundamental_agents"]):
        agents.append(Agent(
            type=3,
            delay=np.random.randint(param_config["delay_min"], param_config["delay_max"]),
            window=np.random.randint(param_config["window_min"], param_config["window_max"]+1),
            alpha=np.random.uniform(param_config["alpha_mean"], param_config["alpha_std"]),
            price_noise=np.random.normal(0, param_config["price_noise_std"]),
            steepness=sample_response_at_100()
        ))

    # Add company agent
    agents.append(Agent(
        type=5,
        delay=0,
        window=0,
        alpha=0.5,
        price_noise=0,
        steepness=param_config["company_agent_steepness"],
    ))

    # Live plot init
    if plot:
        plt.ion()
        fig, ax = plt.subplots()
        price_line, = ax.plot([], [], label="Market Price", color='blue')
        fund_line, = ax.plot([], [], label="Fundamental", color='orange')
        if reference_prices is not None:
            ref_line, = ax.plot([], [], label="Reference Price", color='green', linestyle='--')
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)

    price = [100]
    scores = [100]
    regimes = []
    times = [0]
    all_orders = []
    t = 1

    def handle_interrupt(sig, frame):
        print("\nSimulation interrupted. Exiting...")
        if plot:
            plt.ioff()
            plt.show()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)

    while t < param_config['steps']:
        orders = [agent.create_order(price, scores) for agent in agents]
        all_orders.append(orders)

        time.sleep(0.0005)
        score, regime = Score.step(company_flow=agents[-1].capital)
        scores.append(score)
        regimes.append(regime)
        times.append(t)
        t += 1

        if t>2 and policy:
            result = Walrasion_auction(all_orders[-2])
            clearing_price = result[1]
            price.append(price[-1] if clearing_price < 0 else clearing_price)
        elif t<= 1 and policy:
            price.append(price[-1])
        else:
            result = Walrasion_auction(orders)
            clearing_price = result[1]
            price.append(price[-1] if clearing_price < 0 else clearing_price)

        for i, filled in enumerate(result[0]):
            agents[i].update(filled)

        if plot:
            fund_line.set_data(times, scores)
            price_line.set_data(times, price)
            if reference_prices is not None:
                clipped_ref = reference_prices[:len(times)]
                ref_line.set_data(times, clipped_ref)
            ax.relim()
            ax.autoscale_view()
            plt.draw()

    volume_series = [sum(abs(q) for q, _ in o) for o in all_orders]
    if plot:
        diagnostics = market_diagnostics(price, scores, volume_series, regimes)
    return price


run_simulation(param_config,plot=True)


