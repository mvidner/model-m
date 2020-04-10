from run_experiment import matrix  # TODO what to DO?
from graph_gen import GraphGenerator


def simple_policy(policy_func):

    def wrapper(graph, states, history):
        print("Hello world! This is the policy function speaking.")

        if not isinstance(graph, GraphGenerator):
            raise TypeError("This policy works with GraphGenerator derived graphs only.")
        
        # overkill,  budou se brat jen ty, co se presli do Id dnes
        nodes = list(graph.G.nodes)
        detected_nodes = [
            nodes[idx] for idx, x in enumerate(states) if x == "I_d"
        ]

        print(f"Qurantined nodes: {detected_nodes}")

        quarantine = policy_func(graph, states, history)
        
        for node in detected_nodes:
            print(f"Node {node} goes to quarntine")
            graph.modify_layers_for_node(node, quarantine)

        A = matrix(graph)
        to_change = {"graph": A}
        return to_change

    return wrapper


@simple_policy
def strong_policy(graph, states, history):
    """ people dected are disconnected from the graph """
    quarantine = {
        layer: 0 for layer in graph.layer_names
    }
    #    quarantine["F"] = 100
    return quarantine




def universar_policy(graph, states, history):
    """ works both for GraphGenerator objects and netwrorkx graphs """

    # people dected are disconnected from the graph 
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

        print(f"Qurantined nodes: {detected_nodes}")
        
        for node in detected_nodes:
            print(f"Node {node} goes to quarntine")
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
