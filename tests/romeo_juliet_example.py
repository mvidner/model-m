from graphviz import Graph
import networkx as nx

from romeo_juliet_graph_gen import RomeoAndJuliet

# as multigraph - print
rj = RomeoAndJuliet()
rj.print_multi()

# as flattenned graph - get and print
H = rj.as_one_graph()

dot_H = nx.nx_pydot.to_pydot(H)
print(dot_H)

# as a dictionary of simple graphs indexed by layer codes
my_graphs=rj.as_dict_of_graphs()
print(my_graphs)
#print(MyGraphs['D'].graph) 
dot_D = nx.nx_pydot.to_pydot(my_graphs['D'])
print(dot_D)
print(my_graphs)
