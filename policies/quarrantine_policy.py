import numpy as np
from functools import partial
from graph_gen import GraphGenerator
from extended_network_model import STATES as s


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
            layer: 0 for layer in range(len(graph.layer_names))
        },
        "duration": 14
    }


def simple_quarrantine_policy(graph, policy_coefs, history, tseries, time):

    print("Hello world! This is the policy function speaking.")

    # and not isinstance(graph, LightGraph):
    if not isinstance(graph, GraphGenerator):
        raise TypeError(
            "This policy works with GraphGenerator derived graphs only.")

    current_day = int(time)
    start = np.searchsorted(tseries, current_day-1, side="left")

    if start == 0:
        start = 1
    end = len(tseries)
    last_day = history[start:end]

    # those who became infected today
    detected_nodes = [
        node
        for node, _, e in last_day
        if e == s.I_d
    ]

    print(f"Qurantined nodes: {detected_nodes}")

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

    to_change = {"graph": graph.final_adjacency_matrix()}
    return to_change


if __name__ == "__main__":

    q = QuarrantineDepo(10)

    print(q.quarrantine)
    q.lock_up([0, 1, 2], 3)
    q.lock_up([5], 4)

    print(q.quarrantine)
    r = q.tick_and_get_released()
    print(r)
    assert len(r[0]) == 0

    r = q.tick_and_get_released()
    assert len(r[0]) == 0

    r = q.tick_and_get_released()
    print(r)

    print(q.quarrantine)
    r = q.tick_and_get_released()
    print(r)

    print(q.quarrantine)
