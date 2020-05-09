import numpy as np
from scipy.sparse import csr_matrix
from functools import partial
from graph_gen import GraphGenerator
from light import LightGraph
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

QUARANTINE_COEFS = {
        0: 0,
        1: 100,  # family_inside
        2: 100,  # family_in_house
        3: 0.2,  # family_visitsors_to_visited
        4: 0,  # nursary_children_inclass
        5: 0,  # nursary_teachers_to_children
        6: 0,  # lower_elementary_children_inclass
        7: 0,  # lower_elementary_teachers_to_children
        8: 0,  # higher_elementary_children_inclass
        9: 0,  # higher_elementary_teachers_to_children
        10: 0,  # highschool_children_inclass
        11: 0,  # highschool_teachers_to_children
        12: 0,  # nursary_children_coridors
        13: 0,  # lower_elementary_children_coridors
        14: 0,  # higher_elementary_children_coridors
        15: 0,  # highschool_children_coridors
        16: 0,  # nursary_teachers
        17: 0,  # lower_elementary_teachers
        18: 0,  # higher_elementary_teachers
        19: 0,  # highschool_teachers
        20: 0,  # leasure_outdoor
        21: 0,  # leasure_visit
        22: 0,  # leasure_pub
        23: 0,  # work_contacts
        24: 0,  # work_workers_to_clients_distant
        25: 0,  # work_workers_to_clients_plysical_short
        26: 0,  # work_workers_to_clients_physical_long
        27: 0,  # public_transport
        28: 0,  # shops_customers
        29: 0.0,  # shops_workers_to_clients
        30: 0.0,  # pubs_customers
        31: 0.0,  # pubs_workers_to_clients
}

RISK_FOR_LAYERS = {
        0: 0,
        1: 1,  # family_inside
        2: 1,  # family_in_house
        3: 1,  # family_visitsors_to_visited
        4: 0.8,  # nursary_children_inclass
        5: 0.8,  # nursary_teachers_to_children
        6: 0.8,  # lower_elementary_children_inclass
        7: 0.8,  # lower_elementary_teachers_to_children
        8: 0.8,  # higher_elementary_children_inclass
        9: 0.8,  # higher_elementary_teachers_to_children
        10: 0.8,  # highschool_children_inclass
        11: 0.8,  # highschool_teachers_to_children
        12: 0.8,  # nursary_children_coridors
        13: 0.8,  # lower_elementary_children_coridors
        14: 0.8,  # higher_elementary_children_coridors
        15: 0.8,  # highschool_children_coridors
        16: 0.8,  # nursary_teachers
        17: 0.8,  # lower_elementary_teachers
        18: 0.8,  # higher_elementary_teachers
        19: 0.8,  # highschool_teachers
        20: 0.4,  # leasure_outdoor
        21: 0.5,  # leasure_visit
        22: 0.3,  # leasure_pub
        23: 0.8,  # work_contacts
        24: 0.8,  # work_workers_to_clients_distant
        25: 0.8,  # work_workers_to_clients_plysical_short
        26: 0.8,  # work_workers_to_clients_physical_long
        27: 0.1,  # public_transport
        28: 0.1,  # shops_customers
        29: 0.0,  # shops_workers_to_clients
        30: 0.0,  # pubs_customers
        31: 0.0,  # pubs_workers_to_clients
}



def quarrantine_policy_setup(graph, normal_life):

    risk_for_layers = RISK_FOR_LAYERS
    riskiness = np.array([risk_for_layers[i] for i in range(0, 32)])

    return {
        "quarrantine_depo": QuarrantineDepo(graph.number_of_nodes),
        "normal_life": normal_life,
        "quarrantine_coefs": QUARANTINE_COEFS,
        "duration": 14,
        "threashold": 0.7,
        "days_back": 7,
        "riskiness": riskiness
    }

def quarrantine_policy_setup2(graph, normal_life):

    risk_for_layers = RISK_FOR_LAYERS
    # 4 .. 19  schools 
    for layer in range(4, 20):
        risk_for_layers[layer] = 0.5 
    
    # leasure pub 
    risk_for_layers[22] = 0.15 

    # 23 .. 26 work contacts 
    for layer in range(23, 27):
        risk_for_layers[layer] = 0.5 

    # publick transport 
    risk_for_layers[27] = 0.05 

    # shops cumtomers 
    risk_for_layers[28] = 0.05 

    riskiness = np.array([risk_for_layers[i] for i in range(0, 32)])

    return {
        "quarrantine_depo": QuarrantineDepo(graph.number_of_nodes),
        "normal_life": normal_life,
        "quarrantine_coefs":  QUARANTINE_COEFS,
        "duration": 14,
        "threashold": 0.7,
        "days_back": 7,
        "riskiness": riskiness
    }




def simple_quarrantine_policy(graph, policy_coefs, history, tseries, time, contact_history=None):

    print("Hello world! This is the policy function speaking.")

    if not isinstance(graph, GraphGenerator) and not isinstance(graph, LightGraph):
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

    to_change = _quarrantine_nodes(detected_nodes, policy_coefs, graph)

    return to_change


def quarrantine_with_contact_tracing_policy(graph, policy_coefs, history, tseries, time, contact_history=None):

    print("Hello world! This is the policy function speaking.")
    if contact_history is not None:
        print("Contact tracing is ON.")
    else:
        print("Warning: Contact tracing is OFF.")

    if not isinstance(graph, LightGraph):
        raise TypeError(
            "This policy works with LightGraph derived graphs only.")

    last_day = _get_last_day(history, tseries, time)

    # those who became infected today
    detected_nodes = [
        node
        for node, _, e in last_day
        if e == states.I_d
    ]

    if contact_history is not None:
        contacts = _select_contacts(
            detected_nodes, contact_history, graph,
            policy_coefs["threashold"], policy_coefs["days_back"], policy_coefs["riskiness"])
    else:
        contacts = []

    print(f"Qurantined nodes: {detected_nodes}")
    print(f"Qurantined contacts: {contacts}")

    # friends of detected
    to_change = _quarrantine_nodes(
        detected_nodes+list(contacts), policy_coefs, graph)
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

    #    for node in detected_nodes:
    # print(f"Node {node} goes to quarantine")
    graph.modify_layers_for_nodes(detected_nodes,
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

    return {"graph": None}


def _select_contacts(detected_nodes, contact_history, graph, threashold, days_back=7, riskiness=None):
    # matrix = graph.final_adjacency_matrix()
    # active_edges = matrix[detected_nodes]

    # important_values = active_edges > threashold
    # detected_contacts = important_values.nonzero()[1]
    # return detected_contacts
    if not contact_history:
        return []

    my_contact_history = contact_history[-days_back:]

    relevant_contacts = _filter_contact_history(
        my_contact_history, detected_nodes, graph, riskiness)

    # if relevant_contacts:
    #     print(relevant_contacts)
    #     exit()

    return set(relevant_contacts)


def _filter_contact_history(contact_history, detected_nodes, graph, riskiness):

    if riskiness is None:
        relevant_contacts = [
            contact[1]
            for contact_list in contact_history
            for contact in contact_list
            if contact[0] in detected_nodes
        ]
        return relevant_contacts
    else:
        relevant_contacts = [
            (contact[1], _riskiness(contact[2], graph, riskiness))
            for contact_list in contact_history
            for contact in contact_list
            if contact[0] in detected_nodes
        ]

        if not relevant_contacts:
            return relevant_contacts

        r = np.random.rand(len(relevant_contacts))
        # print(r)
        # print(relevant_contacts)
        # print(r[0])

        # for i, (contact, threashold) in enumerate(relevant_contacts):
        #     print(i, contact, threashold, r[i])

        filtered = [
            contact
            for i, (contact, threashold) in enumerate(relevant_contacts)
            if r[i] < threashold
        ]
        return filtered


def _riskiness(contact, graph, riskiness):
    return np.max(riskiness[graph.get_layer_for_edge(contact)])
