import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_usage_data(
    node, day_start="20190701", n_days=10, node_type=None, plot=False
):
    """
    Units are kW rn
    Could be nice to add variable timesteps, but that would require some inferencing on the template data
    - I think there's a sklearn package that makes this really easy
    """
    day_start = pd.to_datetime(day_start)

    node_type = node.type if node_type is None else node_type
    ts = pd.date_range(start=day_start, freq="1H", periods=24 * n_days)
    if node_type == "OldHome":
        # Total data for region. Maybe can use it as a template?
        data = pd.read_csv("./NE_energy_usage.csv").dropna()
        data["timestamp"] = pd.to_datetime(data["Timestamp (Hour Ending)"])

        # Grab one day to use as template
        # Not modeling weekend/weekday variations (yet)
        i0, i1 = 96, 120
        day_template = data.iloc[i0:i1].copy(deep=True).reset_index(drop=True)
        day_template["demand"] = (
            day_template["Demand (MWh)"] / day_template["Demand (MWh)"].max()
        )

        # According to Eversource, our average daily use is around 8 kWh, so let's enforce that here
        day_template["demand"] *= 8 / day_template.demand.sum()

        # Add some total offset and point-level noise
        node_demand_template = day_template.demand * (1 + np.random.uniform(-0.1, 0.1))
        node_demand = np.hstack(
            [
                node_demand_template
                + np.random.uniform(-0.03, 0.03, len(node_demand_template))
                for _ in range(n_days)
            ]
        )
        node_generation = np.zeros_like(node_demand)

    elif node_type == "PowerPlant":
        # Generic, so just assume flat production curve
        node_demand = np.zeros(len(ts))

        # According to EIA.gov, NG power plants range from 1-3500MW per year
        node_generation = 10000 / (365 * 24)

    out = pd.DataFrame(
        {"timestamp": ts, "demand": node_demand, "generation": node_generation}
    )
    out.set_index("timestamp", inplace=True)

    if plot:
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot_date(out.timestamp, out.demand, "-or", label="Demand")
        ax.plot_date(out.timestamp, out.generation, "-og", label="Generation")

        # TODO: These aren't the units
        ax.set_ylabel("Energy (kW)")
        ax.legend()

    return (node, out)
