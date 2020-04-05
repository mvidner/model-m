from graphviz import Graph
import networkx as nx

from romeo_juliet_graph_gen import RomeoAndJuliet

# as multigraph - print
rj = RomeoAndJuliet()
rj.printMulti()

# as flattenned graph - get and print
H = rj.asOneGraph()
dot_H = nx.nx_pydot.to_pydot(H)
print(dot_H)

# as a dictionary of simple graphs indexed by layer codes
MyGraphs=rj.asDictOfGraphs()
#print(MyGraphs)
print(MyGraphs['D'].graph) 
dot_D = nx.nx_pydot.to_pydot(MyGraphs['D'])
print(dot_D)
