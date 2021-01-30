# DER Simulator Journal

Since this is a personal fun project, its development pattern will be a little atypical. I will be deliberately coding blind (no lit review) for some portions, slowly for some portions, and probably inefficiently for a lot of it.

## Version 0: First Sketch (Mid-Late January 2021)
I wanted to start off by putting in place a purely intuitive, first-principles implementation of what I think a microgrid could look like from a software perspective. Some benefits of this are:
- Forces me to discover problem areas (and hopefully solutions!) before reading about them
- Allows me to build up, keeping my thinking simple and giving me a framework with which to approach the literature
- Avoid the I-don't-need-to-do-this trap. Often I've gone to start some sort of project, but once I start reviewing the literature, get discouraged because whatever project I do could just be done by copying someone else's excellent work. By forcing myself to implement at least something on my own, I will approach existing work through my own lens.

### Design Decisions
- *Object-oriented representation*: I opted to represent the nodes of my graph as objects, since this gives me the most technical flexibility (in terms of node energy I/O, characteristics, etc), and also allows me to update nodes asynchronously (if I decide a certain node has an increase in demand, that can be immediately reflected, instead of waiting for a system-wide timestep). The most obvious alternative to this OOP approach is a purely matrix-based one: a square matrix with nodes on each axis and some feature -- say, energy transactions -- in each cell. Node energy balances and other attributes could be stored in vectors. What I didn't like about this approach is that, while it would likely be faster if correctly implemented, it would likely drag me into indexing hell (i.e. how do we smoothly add or remove nodes from these matrices? It's a super solveable problem, but a little messier). For this first draft, I want my mind to be on conceptual stuff, not big-O costs. Additionally, it would probably make more sense in that case to use a timestep-based updater, which I didn't want.

- *Node attributes*: Right now, each node can be described by a set of fundamental attributes: [storage capacity, stored energy, neighbors]. From these, we can represent several relevant features for microgrids, namely inter-node transactions (a decrease in one node's stored energy leads to a (transmission-resistance-scaled) increase in that of another). Local generation can be represented by just increasing the `stored` value. Since each node is functionally independent here, it can individually resolve imbalances in its own system (excesses or deficits), and (pending further thought about incentive structures) set its own buy/sell prices accordingly (i.e. a node with a huge excess and not much projected use should be pretty much giving away its energy). Finally, each node keeps a log of its transactions, which will hopefully be useful for modeling later.
    - With these attributes, we can subclass our `Node` objects into different characteristic structures: a power planet has high storage capabilities, whereas an old house has none.

- *Transmission losses*: As briefly mentioned above, I am representing transmission losses with a  

- *Grid orchestration*: While all the nodes _can_ be run async, the reality is that simulations are a lot nicer when you move everything along in timesteps, so our `microgrid_sim.grid.EnergyGrid` object (our simulation orchestrator) does that. I think that's fine.

### Challenges:
- *Test data* I've simulated some noisy residential energy usage curves based on some data I scraped (see tools.generate_usage_data), but it's pretty repetitive and not representative in the way I want. 

### Next Steps:
- *Forecasting*: The obvious end goal here is to get good at forecasting usage -- the representations only have value if they, well, have value.
- *Units*: Sort them out! Not convinced everything is in the same unit right now.


## Version 1: First Implementation ()
