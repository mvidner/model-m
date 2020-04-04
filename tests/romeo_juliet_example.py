from graphviz import Graph
import networkx as nx

from romeo_juliet_graph_gen import RomeoAndJuliet

rj = RomeoAndJuliet()
rj.printMulti()

H = rj.asOneGraph()
dot_H = nx.nx_pydot.to_pydot(H)
print(dot_H)
