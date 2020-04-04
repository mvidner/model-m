from graphviz import Graph
import networkx as nx

import romeo-juliet-graph-gen

rj = RomeoAndJuliet()
rj.printMulti()

H = rj.asOneGraph()
dot_H = nx.nx_pydot.to_pydot(H)
print(dot_H)
