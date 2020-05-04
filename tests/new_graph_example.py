from graphviz import Graph
import networkx as nx

from graph_gen_new import NewGraphGenerator

prefix = '../data/newtown/'
gg = NewGraphGenerator()
gg.read_csv(prefix)
print(nx.info(gg.G))


