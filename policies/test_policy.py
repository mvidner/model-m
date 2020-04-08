from run_experiment import matrix  # TODO what to DO?


class Policy():

    def __init__(self, graph):
        self.graph = graph

    def apply_policy(self, states, history):
        # ?? do changes in place or shall I make a copy of a graph?
        # to do go through history

        quarantine = {
            layer: 0.1 for layer in self.graph.layer_names
        }
        quarantine["F"] = 100

        # overkill,  budou se brat jen ty, co se presli do Id dnes
        nodes = list(self.graph.G.nodes)
        detected_states = [
            nodes[idx] for idx, x in enumerate(states) if x == "I_d"
        ]

        for node in detected_states:
            self.graph.modify_layers_for_node(node, quarantine)
        A = matrix(self.graph)

        to_change = {"graph": self.graph if A is None else A}
        return to_change

    def get_policy_function(self):
        return self.apply_policy
