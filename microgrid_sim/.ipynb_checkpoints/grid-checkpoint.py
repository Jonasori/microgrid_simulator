import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
import geoviews as gv
from bokeh.io import output_notebook
from cartopy import crs

output_notebook()
gv.extension("bokeh")

from microgrid_sim.tools import generate_usage_data


class EnergyGrid:
    """
    A representation of a notional energy grid
    """

    def __init__(self, nodes):
        self.nodes = nodes

    def _update_flow_matrix(self):
        # Given some set of energy demands and a distribution policy, do something
        return

    def make_neighbors(self, resistance_matrix=None):
        if resistance_matrix is None:
            resistance_matrix = np.zeros(
                (len(self.nodes), len(self.nodes))
            )
        np.fill_diagonal(resistance_matrix, 1)

        # TODO: Think about how to make this directional
        # (i.e. houses can't send energy to power plants)
        for row, node in zip(resistance_matrix, self.nodes):
            node.add_neighbors(self.nodes, resistances=row)

    def build_grid(self, stored=None, resistance_network=None):
        """
        Build some stuff
        """
        if (self.nodes == None) and (stored == None) and (resistance_network == None):
            print("Need something to build nodes off of")
            return

        resistance_network = (
            np.zeros((n, n)) if resistance_network is None else resistance_network
        )
        np.fill_diagonal(resistance_network, 1)

        stored = np.zeros(n)

        return None

    def visualize(self, gif=False, height=600, width=600):
        """
        Plot nodes and inter-node transactions.
        
        Pretty gross rn.
        Should allow either for time-flatteneed times or gif outputs
        
        A cool ex call from StackOverflow:
        f = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        gv.Polygons(f, vdims=['pop_est', ('name', 'Country')]).opts(
            tools=['hover'], width=600, projection=crs.Robinson()
        )
        """

        coords = gpd.GeoDataFrame(
            {
                "lat": [n.latlon[0] for n in self.nodes],
                "lon": [n.latlon[1] for n in self.nodes],
                "stored": [n.stored for n in self.nodes],
            },
        )

        # EsriImagery, StamenWatercolor
        r = gv.tile_sources.CartoDark()
        r = gv.tile_sources.StamenWatercolor()

        # Plot the nodes
        r *= gv.Points(coords, vdims="stored").opts(
            tools=["hover"], height=height, width=width,
        )

        # Plot all the transactions
        df = pd.concat(
            [n.get_transaction_logs() for n in self.nodes]
        ).drop_duplicates()


        r *= gv.Path(
            [
                [f, t]
                for f, t in zip(
                    df.source.apply(lambda t: t.latlon),
                    df.dest.apply(lambda t: t.latlon),
                )
            ]
        )

        return r

    def run_simulation(self):
        """
        Step time forward, managing the demands of each node during that timestep
        """

        # Make a dict of consumption data, keyed by node
        d = [generate_usage_data(n) for n in self.nodes]
        consumption_data = {n[0]: n[1] for n in d}

        timesteps = np.unique(
            np.concatenate(
                [ndata.index.to_numpy() for ndata in consumption_data.values()]
            )
        )

        for t in timesteps:
            [
                node.evaluate_demands(*consumption_data[node].loc[t])
                for node in self.nodes
            ]
            [node.resolve_imbalances(t) for node in self.nodes]
        return
