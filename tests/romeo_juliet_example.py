from graphviz import Graph
import networkx as nx

from romeo_juliet_graph_gen import RomeoAndJuliet
from graph_gen import RandomGraphGenerator
from graph_gen import CSVGraphGenerator

# as multigraph - print
#rj = RomeoAndJuliet()
#sl = rj.get_attr_list('label')
#print(rj.G.number_of_edges())




# as flattenned graph - get and print
#H = rj.as_one_graph()

#dot_H = nx.nx_pydot.to_pydot(H)
#print(dot_H)

# as a dictionary of simple graphs indexed by layer codes
#my_graphs=rj.as_dict_of_graphs()
#print(my_graphs)
#print(MyGraphs['D'].graph) 
#dot_D = nx.nx_pydot.to_pydot(my_graphs['K'])

#K = nx.nx_agraph.to_agraph(my_graphs['K'])
#K.layout('dot')
#K.draw('raj-K.png')

#print(dot_D)
#print(my_graphs)

#rn = RandomGraphGenerator(10)
#my_graphs = rn.as_dict_of_graphs()
#print(my_graphs)

#GG = rn.as_multigraph()
#dot_GG = nx.nx_pydot.to_pydot(GG)
#print(dot_GG)


#pok = {'D': 0.1, 'F': 0.01}
#rn.modify_layer_for_node(1, pok)

#GG = rn.as_multigraph()
#dot_GG = nx.nx_pydot.to_pydot(GG)
#print(dot_GG)

#dot_D = nx.nx_pydot.to_pydot(my_graphs['D'])
#print(dot_D)

rc = CSVGraphGenerator()
GG = rc.as_multigraph()
dot_GG = nx.nx_pydot.to_pydot(GG)
print(dot_GG)
print (rc.layer_names)
print (rc.layer_probs)