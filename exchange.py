import numpy as np
import matplotlib.pyplot as plt



fig2, ax2 = plt.subplots()
supply_line, = ax2.plot([], [], label='Supply (Cumulative)', color='red')
demand_line, = ax2.plot([], [], label='Demand (Cumulative)', color='green')
ax2.set_ylabel("Price")
ax2.set_xlabel("Cumulative Volume")
ax2.set_title("Cumulative Supply and Demand")
ax2.legend()
ax2.grid(True)


def Walrasion_auction(orders):
    buy_orders = [(q, p) for q, p in orders if q > 0]
    sell_orders = [(q, p) for q, p in orders if q < 0]
    price_points = sorted({p for _, p in orders})
    max_volume = 0
    clearing_price = price_points[0]

    for price in price_points:
        demand = sum(q for q, p in buy_orders if p >= price)
        supply = -sum(q for q, p in sell_orders if p <= price)
        volume = min(demand, supply)
        if volume >= max_volume:
            max_volume = volume
            clearing_price = price
    if max_volume == 0:
        #update_plot(buy_orders, sell_orders, None)
        return [[[0, 0] for _ in orders],-10]  # No trades possible

    # Fulfill orders
    fulfilled_orders = []
    remaining_demand = max_volume
    remaining_supply = max_volume

    for q, p in orders:
        if q > 0 and p >= clearing_price and remaining_demand > 0:
            fill = min(q, remaining_demand)
            fulfilled_orders.append([fill, clearing_price])
            remaining_demand -= fill
        elif q < 0 and p <= clearing_price and remaining_supply > 0:
            fill = max(q, -remaining_supply)
            fulfilled_orders.append([fill, clearing_price])
            remaining_supply += fill  # add because fill is negative
        else:
            fulfilled_orders.append([0, 0])

    update_plot(buy_orders, sell_orders, clearing_price)

    return [fulfilled_orders,clearing_price]


def update_plot(buy_orders, sell_orders, clearing_price):
    ax2.clear()

    prices = sorted({p for _, p in buy_orders + sell_orders})

    demand_curve = []
    supply_curve = []

    for price in prices:
        demand = sum(q for q, p in buy_orders if p >= price)
        supply = sum(-q for q, p in sell_orders if p <= price)
        demand_curve.append(demand)
        supply_curve.append(supply)

    ax2.step(demand_curve, prices, label='Demand', where='post', color='blue')
    ax2.step(supply_curve, prices, label='Supply', where='post', color='red')

    if clearing_price is not None:
        ax2.axhline(y=clearing_price, color='green', linestyle='--', label=f'Clearing Price: {clearing_price}')
    else:
        ax2.set_title("No Market Clearing Possible")

    ax2.set_xlabel("Quantity")
    ax2.set_ylabel("Price")
    ax2.set_title("Cumulative Demand and Supply")
    ax2.legend()
    ax2.grid(True)

    plt.draw()
    plt.pause(0.001)



