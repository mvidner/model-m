from run_experiment import matrix  # TODO what to DO?
from graph_gen import GraphGenerator

def simple_policy(graph, states, history):
    # ?? do changes in place or shall I make a copy of a graph?
    # to do go through history
    print("Hello world! This is the policy function speaking.")

    if isinstance(graph, GraphGenerator):
        quarantine = {
            layer: 0 for layer in graph.layer_names
        }
        #    quarantine["F"] = 100

        # overkill,  budou se brat jen ty, co se presli do Id dnes
        nodes = list(graph.G.nodes)
        detected_nodes = [
            nodes[idx] for idx, x in enumerate(states) if x == "I_d"
        ]

        for node in detected_nodes:
            graph.modify_layers_for_node(node, quarantine)
        A = matrix(graph)
    else:
        # just for testing seirsplus example graph 
        nodes = list(graph.nodes)
        detected_nodes = [
            nodes[idx] for idx, x in enumerate(states) if x == "I_d"
        ]
        for node in detected_nodes:
            for e in graph.edges([node], data=True):
                graph.edges[e[:2]]['weight'] = 0.0
        A = graph     

        
        
    to_change = {"graph": A}
    return to_change
