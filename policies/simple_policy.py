from run_experiment import matrix  # TODO what to DO?
from graph_gen import GraphGenerator


def simple_policy(policy_func):
    """ decorarotor for creation of simple policies 
    that only change weights of contacts of detected people """
    
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


