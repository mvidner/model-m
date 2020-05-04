from graphviz import Graph
import networkx as nx

from graph_new import NewGraph

prefix = '../data/newtown/'
gg = NewGraph()
gg.read_csv(prefix)
print(nx.info(gg.G))

e = gg.get_edges_for_node(5)

print(e)