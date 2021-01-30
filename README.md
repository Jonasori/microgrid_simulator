## Grid Simulator

For the last century, our energy grids have retained the same form: a giant power plant distributes energy outwards to homes and businesses. However, as the cost of distributed energy resources (DERs; namely batteries, solar, and wind) have dropped, the possibility of dynamic, decentralized energy grids is emerging as an alternative to the old hub and spoke model, with the chance to reduce costs and improve grid resiliency. It is hard to see a clean, sustainable future that does not include DERs.

To me, this is one of the more intriguing potential applications of ML/reactive algorithms in the clean-energy space, as its problem domain ranges from graph analysis to consumption predictions to straight up optimization. I am designing this simulated system to maximize modularity, allowing us to hot swap policies (algorithms), and to be maximally flexible in graph structure (i.e. we can simulate both a traditional energy grid or totally distributed DERs here).

To try it out, simply pip install it and start playing with ```overview.ipynb```.

```pip install -e ./```

NB: It's worth noting that this was deliberately started/structured without a deep literature review. I want to build up my own system (and be forced to justify every decision on my own) before seeing what the current state-of-the-art is in this world. While this is obviously not an approach that is appropriate for professional work, it is a luxury afforded to me by virtue of this being a fun side project :) See `project_journal.md` for a little more commentary on this.
