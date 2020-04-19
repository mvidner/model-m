from run_experiment import matrix  # TODO what to DO?
from graph_gen import GraphGenerator
from simple_policy import simple_policy


@simple_policy
def strong_policy(graph, history):
    """ people dected are disconnected from the graph """
    quarantine = {
        layer: 0 for layer in graph.layer_names
    }
    return quarantine


@simple_policy
def weighted_policy(graph, history):
    """ connections for detected nodes: 
       1     : family   1 
       2 - 7 : schools  0 
       8     : friends  * 0.2 
    """
    quarantine = {
        layer: 0 for layer in graph.layer_names
    }
    quarantine[8] = 0.1  # friends
    quarantine[1] = 100  # family
    return quarantine


# OLD
# no imlementation of policies for networkx graph,
# you have to use GraphGenerator objects


# def universar_policy(graph, states, history):
#     """ works both for GraphGenerator objects and netwrorkx graphs """

#     # people dected are disconnected from the graph
#     print("Hello world! This is the policy function speaking.")

#     if isinstance(graph, GraphGenerator):
#         quarantine = {
#             layer: 0 for layer in graph.layer_names
#         }
#         #    quarantine["F"] = 100

#         # overkill,  budou se brat jen ty, co se presli do Id dnes
#         nodes = list(graph.G.nodes)
#         detected_nodes = [
#             nodes[idx] for idx, x in enumerate(states) if x == "I_d"
#         ]

#         print(f"Qurantined nodes: {detected_nodes}")

#         for node in detected_nodes:
#             print(f"Node {node} goes to quarntine")
#             graph.modify_layers_for_node(node, quarantine)
#         A = matrix(graph)
#     else:
#         # just for testing seirsplus example graph
#         nodes = list(graph.nodes)
#         detected_nodes = [
#             nodes[idx] for idx, x in enumerate(states) if x == "I_d"
#         ]
#         for node in detected_nodes:
#             for e in graph.edges([node], data=True):
#                 graph.edges[e[:2]]['weight'] = 0.0
#         A = graph

#     to_change = {"graph": A}
#     return to_change
