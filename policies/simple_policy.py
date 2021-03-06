import numpy as np
from run_experiment import matrix  # TODO what to DO?
from graph_gen import GraphGenerator
from light_graph import LightGraph
from extended_network_model import STATES as s


def simple_policy(policy_func):
    """ decorarotor for creation of simple policies 
    that only change weights of contacts of detected people """

    def wrapper(graph, policy_coefs, history, tseries, time, contact_history=None):
        print("Hello world! This is the policy function speaking.")

        # print("Current time:", time)
        # print("Current day:", int(time))
        # print("whole", tseries)
        current_day = int(time)
        start = np.searchsorted(tseries, current_day-1, side="left")
        if start == 0:
            start = 1
        end = np.searchsorted(tseries, current_day, side="left")
        # print(start, end, len(tseries))
        # print("today", tseries[start:end])

        if not isinstance(graph, GraphGenerator) and not isinstance(graph, LightGraph):
            raise TypeError(
                "This policy works with GraphGenerator derived graphs only.")

        # overkill,  budou se brat jen ty, co se presli do Id dnes
        #nodes = list(graph.nodes)
        history = history[start:end]
        #        print(start, end)
        print("Historie", history)

        detected_nodes = [
            node
            for node, _, e in history
            if e == s.I_d
        ]

        print(f"Qurantined nodes: {detected_nodes}")
        if detected_nodes:

            quarantine = policy_func(graph, policy_coefs, history, tseries, time, contact_history)

            for node in detected_nodes:
                # print(f"Node {node} goes to quarntine")
                graph.modify_layers_for_node(node, quarantine)

            #                if isinstance(graph, GraphGenerator):
            #                    A = graph.G
            #                else:
            A = matrix(graph, None)

            to_change = {"graph": A}
            return to_change
        else:
            return {}

    return wrapper
