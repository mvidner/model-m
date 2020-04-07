class Policy():

    def __init__(self, graph):
        self.graph = graph

    def apply_policy(self, states, history):
        # ?? do changes in place or shall I make a copy of a graph?
        # to do go through history

        detected_states = [
            idx for idx, x in enumerate(states) if x == "I_d"
        ]
        for node in detected_states:
            self.graph.isolate_node(node)

        to_change = {"graph": self.graph}
        return to_change

    def get_policy_function(self):
        return self.apply_policy
