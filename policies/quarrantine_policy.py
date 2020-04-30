import numpy as np
from scipy.sparse import csr_matrix
from functools import partial
from graph_gen import GraphGenerator
from extended_network_model import STATES as states


class QuarrantineDepo:
    def __init__(self, size):
        self.quarrantine = np.zeros(size)

    def lock_up(self, nodes, duration):
        self.quarrantine[nodes] = duration

    def tick_and_get_released(self):
        released = np.nonzero(self.quarrantine == 1)[0]
        self.quarrantine[self.quarrantine > 0] -= 1
        return released

    def is_locked(self, node_id):
        return self.quarrantine[node_id] > 0


def quarrantine_policy_setup(graph, normal_life):
    return {
        "quarrantine_depo": QuarrantineDepo(graph.number_of_nodes()),
        "normal_life": normal_life,
        "quarrantine_coefs": {
            1: 100,  # family
            2: 0,  # nursary children
            3: 0,  # nursary teachers to children
            4: 0,  # elementary children
            5: 0,  # elementary teachers to children
            6: 0,  # highschool children
            7: 0,  # highschool teachers to children
            8: 0  # friend network
        },
        # "quarrantine_coefs": {
        #     1: 100,  # family
        #     2: 0,
        #     3: 0,
        #     4: 0,  # lower elementary children
        #     5: 0,  # lower elementary teachers to children
        #     6: 0,  # higher elementary children
        #     7: 0,  # higher elementary teachers to children
        #     8: 0,  # highschool children
        #     9: 0,  # highschool teachers to children
        #     10: 0.1,  # friend and relative encounetr
        #     11: 0,  # work contacts
        #     12: 0,  # workers to clients
        #     13: 0,  # public transport contacts
        #     14: 0  # contacts of customers at shops
        # },
        "duration": 14,
        "threashold": 0.1
    }


def simple_quarrantine_policy(graph, policy_coefs, history, tseries, time):

    print("Hello world! This is the policy function speaking.")

    # and not isinstance(graph, LightGraph):
    if not isinstance(graph, GraphGenerator):
        raise TypeError(
            "This policy works with GraphGenerator derived graphs only.")

    last_day = _get_last_day(history, tseries, time)

    # those who became infected today
    detected_nodes = [
        node
        for node, _, e in last_day
        if e == states.I_d
    ]

    print(f"Qurantined nodes: {detected_nodes}")

    _quarrantine_nodes(detected_nodes, policy_coefs, graph)

    to_change = {"graph": graph.final_adjacency_matrix()}
    return to_change


def quarrantine_with_contact_tracing_policy(graph, policy_coefs, history, tseries, time):

    print("Hello world! This is the policy function speaking.")
    print("Contact tracing is ON.")

    # and not isinstance(graph, LightGraph):
    if not isinstance(graph, GraphGenerator):
        raise TypeError(
            "This policy works with GraphGenerator derived graphs only.")

    last_day = _get_last_day(history, tseries, time)

    # those who became infected today
    detected_nodes = [
        node
        for node, _, e in last_day
        if e == states.I_d
    ]

    contacts = _select_contacts(
        detected_nodes, graph, policy_coefs["threashold"])

    print(f"Qurantined nodes: {detected_nodes}")
    print(f"Qurantined contacts: {contacts}")

    # friends of detected

    _quarrantine_nodes(detected_nodes+list(contacts), policy_coefs, graph)

    to_change = {"graph": graph.final_adjacency_matrix()}
    return to_change


def _get_last_day(history, tseries, time):
    current_day = int(time)
    start = np.searchsorted(tseries, current_day, side="left")

    if start == 0:
        start = 1
    end = np.searchsorted(tseries, current_day+1, side="left")
    return history[start:end]


def _quarrantine_nodes(detected_nodes, policy_coefs, graph):
    if not detected_nodes:
        # nothing to do
        return {}

    depo = policy_coefs["quarrantine_depo"]
    quarantine_coefs = policy_coefs["quarrantine_coefs"]
    normal_life = policy_coefs["normal_life"]
    duration = policy_coefs["duration"]

    for node in detected_nodes:
        # print(f"Node {node} goes to quarantine")
        graph.modify_layers_for_node(node,
                                     quarantine_coefs,
                                     depo.quarrantine)
    depo.lock_up(detected_nodes, duration)
#    print(">>>", depo.quarrantine)
    released = depo.tick_and_get_released()

    if len(released) > 0:
        print(f"Released nodes: {released}")
        graph.recover_edges_for_nodes(released,
                                      normal_life,
                                      depo.quarrantine)


def _select_contacts(detected_nodes, graph, threashold):
    matrix = graph.final_adjacency_matrix()
    active_edges = matrix[detected_nodes]

    important_values = csr_matrix(active_edges)
    important_values.data -= threashold
    detected_contacts = important_values.nonzero()[1]
    return detected_contacts
