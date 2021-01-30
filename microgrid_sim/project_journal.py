DER_Sim_Journal = {
    "Opening Remarks": {
        """
        Since this is a personal fun project, its development pattern will be a little atypical. I will be deliberately coding blind (no lit review) for some portions, slowly for some portions, and probably inefficiently for a lot of it.
        """
    },
    "Version 0": {
        "start_date": "mid January 2020",
        "end_date": None,
        "comments": {
            "Design Decisions": """
            - *Object-oriented representation*: I opted to represent the nodes of my graph as objects, since this gives me the most technical flexibility (in terms of node energy I/O, characteristics, etc), and also allows me to update nodes asynchronously (if I decide a certain node has an increase in demand, that can be immediately reflected, instead of waiting for a system-wide timestep). The most obvious alternative to this OOP approach is a purely matrix-based one: a square matrix with nodes on each axis and some feature -- say, energy transactions -- in each cell. Node energy balances and other attributes could be stored in vectors. What I didn't like about this approach is that, while it would likely be faster if correctly implemented, it would likely drag me into indexing hell (i.e. how do we smoothly add or remove nodes from these matrices? It's a super solveable problem, but a little messier). For this first draft, I want my mind to be on conceptual stuff, not big-O costs. Additionally, it would probably make more sense in that case to use a timestep-based updater, which I didn't want.

            - *Node attributes*: Right now, each node can be described by a set of fundamental attributes: [storage capacity, stored energy, neighbors]. From these, we can represent several relevant features for microgrids, namely inter-node transactions (a decrease in one node's stored energy leads to a (transmission-resistance-scaled) increase in that of another). Since each node is functionally independent here, it can individually resolve imbalances in its own system (excesses or deficits), and (pending further thought about incentive structures) set its own buy/sell prices accordingly (i.e. a node with a huge excess and not much projected use should be pretty much giving away its energy).
            """,
            "Challenges Encountered": """
            
            """,
            "Next Steps": """
            
            """
        }
    }
    
}