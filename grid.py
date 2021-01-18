import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import geoviews as gv
from bokeh.io import output_notebook
from cartopy import crs
output_notebook()
gv.extension('bokeh')

class EnergyGrid:
    """
    A representation of a notional energy grid
    """
    
    def __init__(self, nodes):
        self.nodes = nodes
        
    
    def _update_flow_matrix(self):
        # Given some set of energy demands and a distribution policy, do something
        return
    
    def make_neighbors(self, connection_matrix=None):
        if connection_matrix is None:
            connection_matrix = np.zeros((len(self.nodes), len(self.nodes)))
        np.fill_diagonal(connection_matrix, 1)

        for row, node in zip(connection_matrix, self.nodes):
            node.add_neighbors(nodes, resistances=row)

    def build_grid(self, stored=None, resistance_network=None):
        """
        Build some stuff
        """
        if (self.nodes == None) and (stored == None) and (resistance_network == None):
            print("Need something to build nodes off of")
            return
        
        resistance_network = np.zeros((n, n)) if resistance_network is None else resistance_network
        np.fill_diagonal(resistance_network, 1)
        
        stored = np.zeros(n)
        
        
        return None
    
    def visualize(self, gif=False):
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
            }, # geometry=["lat", "lon"]
        )

        # EsriImagery, StamenWatercolor
        r = gv.tile_sources.CartoDark()
        r = gv.tile_sources.StamenWatercolor()

        # Plot the nodes
        r *= gv.Points(coords, vdims="stored").opts(
            tools=["hover"], width=1600, projection=crs.Robinson()
        )

        # Plot all the transactions
        transactions = pd.DataFrame.from_records(
            np.concatenate([n.log for n in nodes])
        ).drop_duplicates()


        # Really gross, and probably not totally accurate, but something for now
        df = pd.DataFrame.from_records(np.concatenate([n.log for n in self.nodes]))
        r *= gv.Path([[f, t] for f, t in zip(df.source.apply(lambda t: t.latlon), df.dest.apply(lambda t: t.latlon))])

        return r
    
    def run_simulation(self):
        """
        Step time forward, managing the demands of each node during that timestep
        """
        
        # Make a dict of consumption data, keyed by node
        d = [generate_usage_data(n) for n in nodes]
        consumption_data = {n[0]: n[1] for n in d}

        timesteps = np.unique(np.concatenate([ndata.index.to_numpy() for ndata in consumption_data.values()]))
        
        for t in timesteps:
            [node.evaluate_demands(*consumption_data[node].loc[t]) for node in self.nodes]
            [node.resolve_imbalances(t) for node in self.nodes]
        return
        