from graphviz import Graph
import networkx as nx

from romeo_juliet_graph_gen import RomeoAndJuliet
from graph_gen import RandomGraphGenerator

# as multigraph - print
rj = RomeoAndJuliet()
sl = rj.get_attr_list('label')
print(sl)
d = rj.get_layers_info()
print(d)


# as flattenned graph - get and print
#H = rj.as_one_graph()

#dot_H = nx.nx_pydot.to_pydot(H)
#print(dot_H)

# as a dictionary of simple graphs indexed by layer codes
#my_graphs=rj.as_dict_of_graphs()
#print(my_graphs)
#print(MyGraphs['D'].graph) 
#dot_D = nx.nx_pydot.to_pydot(my_graphs['D'])
#print(dot_D)
#print(my_graphs)

#rn = RandomGraphGenerator(20)
#my_graphs = rn.as_dict_of_graphs()
#print(my_graphs)

#dot_D = nx.nx_pydot.to_pydot(my_graphs['D'])
#print(dot_D)