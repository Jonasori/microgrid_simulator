import numpy as np
import pandas as pd


class Node:
    """
    A representation of a node in an energy grid.
    
    There are two (?) forms of energy transfer cost:
        - Dollars: it costs money to take someone else's energy
        - Resistance: There is some energy loss in a transfer
        - Maybe: time delay?
        
    Can control a node's desire for energy by changing dollar cost
        - If our excess is close to storage_capacity, then our buying
            price should be low.
            
    Should excess and demand be the same variable, just negative?
    
    Likewise, what is the relationship between energy stored and energy generated?
    I think they can be treated the same; both are just excesses.
    
    Todos:
    - Update the cost functions
    - Figure out units
    - Longterm: Demand forecasting (with weather?)
        - Reflected in cost fun, i.e. desire to retain or get rid of excesses
    """

    def __init__(self, latlon, storage_capacity=None, neighbors=None, name=None):
        self.latlon = latlon
        self.storage_capacity = storage_capacity
        self.name = np.random.randint(1e5, 1e6) if name is None else name
        self._log = []
        self.verbose = True

        # Some scaling factor for a node's desire to trade energy (not just its ability to do so)
        self.cost = 1

        # Should be a pd.df with obj and cost colums?
        self.neighbors = pd.DataFrame(columns=["nodes", "resistance"])
        self.stored = 0  # W

        # In this timestep, how much demand/excess do we have?
        #         self.excess = 0  # W
        #         self.demand = 0   # W?

        """
        Could have generation/demand curves as well? Will prob need predictive stuff here
        self.
        """

    def get_transaction_logs(self, t_start=None, t_end=None):
        log = pd.DataFrame(self._log)  #.set_index("timestamp")

        if t_start is not None:
            log = log.loc[pd.to_datetime(t_start) :]

        if t_end is not None:
            log = log.loc[: pd.to_datetime(t_end)]

        return log

    def _cost_func(self, candidates, watts_reqd=None):
        """
        Metric by which to evaluate appeal of different nodes' availabilities
        
        Need to end up with watts_reqd, so overshoot to compensate for resistance
        losses, then evaluate energy price
        
        Need to extend this to multi-step energy retrievals
        Is this directional?
        """

        # Need to rethink this
        # Want it to minimize scores of nodes with low resistances and costs
        #         cost_func = lambda n: (1 - n.resistance) * watts_reqd * n.cost
        #         cost = candidates.apply(lambda n: n.resistance * n.cost)
        #         cost = candidates.resistance * candidates.apply(lambda n: n.cost)
        cost = candidates.resistance  # * candidates.apply(lambda n: n.cost)
        return cost

    def _get_sources(self, alg="1hop"):
        """
        Find all the paths we can take to get energy
        
        :return: pd.df of
            - Source node obj (if graph searching, the last node on the chain)
            - cost/resistance of getting energy from that node (sum of cost of steps)
            - Amount of energy available
        """
        if alg is "1hop":
            sources = self.neighbors.copy(deep=True)
            sources["cost"] = self._cost_func(sources)

            sources.sort_values(by="cost", ascending=True, inplace=True)

            # This assumes that other nodes are all up to date on their own supply situation
            sources["excess"] = sources.nodes.apply(lambda node: node.stored)
            return sources

        elif alg is "bfs":
            # Needs to be BFS, not DFS, so we know the range of available costs
            return

    def _send_to_neighbors(self, timestamp=None):
        """
        If we're overloaded, send out excess to neighbors with storage capacity.
        
        Should add a cost function here, too, both in dollars and watts.
        """
        excess = self.stored - self.storage_capacity
        assert excess > 0, "No excess"

    def _pull_from_neighbors(self, demand=None, max_n_sources=1, timestamp=None):
        """
        If a node has more demand than stored energy, pull from a neighbor with excess.
        
        Steps required:
        - Get list of available source nodes and their resistances
            - For anything beyond immediate neighbors, this will need to be some sort of
                graph search. Not sure when to cut it off.
        - Identify best node(s) to pull from, considering:
            - Cost
            - Amount available? Is it best to try to pull from nodes with excesses
                ~= demand? Or just pull from the biggest source?
            - If allowing for composite fulfillment, how do we handle that?
                - What is the best way to combine sources?

        - Could this just be done as a matrix op from the grid-level?
            - Philosophically that would be less good; need them to be autonomous/async
        """
        # Demand and a negative storage total are inverses of each other
        demand = -self.stored if demand is None else demand
        assert demand > 0, "No demand"

        # Pretty strikingly slow/inefficient alg here, but hopefully functional?
        sources = self._get_sources()

        # For now, no going higher before we've implemented it!
        max_n_sources = min([max_n_sources, 1])
        if max_n_sources == 1:
            # Take the lowest cost (as sorted above) neighbor with enough excess available
            source = sources.loc[sources.excess >= (demand)].iloc[0].nodes
            source.stored -= demand
            self.stored = 0

            print(f"{self.name} pulled {round(demand, 3)} watts from node {source.name}") if self.verbose else None
        else:
            print("Not implemented")

        log_vec = {
            "source": source,
            "dest": self,
            "amount": demand,
            "timestamp": timestamp,
        }
        self._log.append(log_vec)
        source._log.append(log_vec)

    def add_neighbors(self, new_nodes, resistances=None):
        # Should probably add a check to make sure we're not passing self

        if resistances is None:
            # Really simple Euclidean-distance based cost
            resistances = pd.Series(
                [n.latlon for n in new_nodes]
            ).apply(
                lambda ll: np.sqrt((ll[0] - self.latlon[0])**2 + (ll[1] - self.latlon[1])**2)
            ).to_numpy()
            resistances /= resistances.max()
            
        new_neighbors = pd.DataFrame({"nodes": new_nodes, "resistance": resistances})
        self.neighbors = pd.concat((self.neighbors, new_neighbors))
        return

    def evaluate_demands(self, new_demand=0, new_supply=0):
        # Need 0 <= self.stored <= self.storage_capacity
        self.stored += new_supply - new_demand

    def resolve_imbalances(self, timestamp):
        if self.stored < 0:
            self._pull_from_neighbors(timestamp=timestamp)

        # Down the road, should replace this with something curvier, not boxy
        elif self.stored > self.storage_capacity:
            self._send_to_neighbors(timestamp=timestamp)
        else:
            # We're good
            pass

    def step(self, new_supply, new_demand, timestamp=None):
        self.evaluate_demands(new_supply, new_demand)
        self.resolve_imbalances(timestamp)


# A couple example subclasses of the Nodes to more intuitively represent some of the nodes
class OldHome(Node):
    """
    An old home, with no storage or generation abilities of its own.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage_capacity = 0
        self.type = "OldHome"


class PowerPlant(Node):
    """
    An old home, with no storage or generation abilities of its own.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage_capacity = 1e8  # Some big number
        self.stored = 1e7  # Some big number
        self.type = "PowerPlant"
