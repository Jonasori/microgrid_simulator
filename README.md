## Grid Simulator

Some explorations into how an environment of Distributed Energy Resources (DERs) function. DERs are an alternative to the US's current grid-based system, where rather than using a single energy provider for many consumer can have their own storage/generation abilities (i.e. solar panels and batteries), allowing for more flexible, decentralized, and efficient energy usage and tranmission. One big issue with them is that a microgrid of them can run into generation timing issues (i.e. everybody's solar panels are only generating electricity during the day), so appropriate transmission/sharing policies must be implemented that allow for independent, asynchronous (i.e. decentralized) action at the node level, while still maintaining robust energy availability for everyone.

This is one of the more intriguing potential applications of ML/reactive algorithms in this space, ranging from graph analysis to consumption predictions to straight up optimization. I have designed this simulated system to maximize modularity, allowing us to hot swap policies (algorithms), and to be maximally flexible in graph structure (i.e. we can simulate both a traditional energy grid or totally distributed DERs here).

To try it out, simply pip install it and start playing with ```overview.ipynb```.

```pip install -e ./```

NB: It's worth noting that this was deliberately started/structured without a deep literature review. I want to build up my own system (and be forced to justify every decision on my own) before seeing what the current state-of-the-art is in this world. While this is obviously not an approach that is appropriate for professional work, it is a luxury afforded to me by virtue of this being a fun side project :)
