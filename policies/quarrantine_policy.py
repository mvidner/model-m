import numpy as np
from scipy.sparse import csr_matrix
from functools import partial
from graph_gen import GraphGenerator
from light import LightGraph
from extended_network_model import STATES as states


class QuarrantineDepo:
    def __init__(self, size, leave_cond=None):
        self.quarrantine = np.zeros(size)
        self.leave_cond = leave_cond
        self.waiting_room = np.zeros(size, dtype=bool)

    def wait(self, nodes):
        print("nodes w", nodes)
        if len(nodes) == 0:
            return
        self.waiting_room[nodes] = True

    def get_waiting(self):
        released = np.nonzero(self.waiting_room)[0]
        print("released w", released)
        self.waiting_room.fill(False)
        return released

    def lock_up(self, nodes, duration):
        self.quarrantine[nodes] = duration

    def tick_and_get_released(self, memberships):
        released = np.nonzero(self.quarrantine == 1)[0]
        # release only if leave_cond is true
        if len(released) > 0 and self.leave_cond is not None:
            print("Applying security check")
            print(released)
            print(self.leave_cond(released, memberships))
            really_released = released[self.leave_cond(
                released, memberships) == 1]
        else:
            really_released = released
        # for those who are staying tick one day
        self.quarrantine[self.quarrantine > 1] -= 1
        # == 1 are on leave, those who are leased are set to zero
        # others are left with 1 day sentence
        self.quarrantine[really_released] -= 1
        print("REALLY RELEASED", really_released)
        return really_released

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
    13: 0,  # elementary_children_coridors
    14: 0,  # highschool_children_coridors
    15: 0,  # nursary_teachers
    16: 0,  # elementary_teachers
    17: 0,  # highschool_teachers
    18: 0,  # leasure_outdoor
    19: 0,  # leasure_visit
    20: 0,  # leasure_pub
    21: 0,  # work_contacts
    22: 0,  # work_workers_to_clients_distant
    23: 0,  # work_workers_to_clients_plysical_short
    24: 0,  # work_workers_to_clients_physical_long
    25: 0,  # public_transport
    26: 0,  # shops_customers
    27: 0,  # shops_workers_to_clients
    28: 0,  # pubs_customers
    29: 0,  # pubs_workers_to_clients
    30: 0,  # superspreader
}

WEE_COLD_COEFS = {
    0: 0,
    1: 100,  # family_inside
    2: 100,  # family_in_house
    3: 0.9,  # family_visitsors_to_visited
    4: 0,  # nursary_children_inclass
    5: 0,  # nursary_teachers_to_children
    6: 0,  # lower_elementary_children_inclass
    7: 0,  # lower_elementary_teachers_to_children
    8: 0,  # higher_elementary_children_inclass
    9: 0,  # higher_elementary_teachers_to_children
    10: 0,  # highschool_children_inclass
    11: 0,  # highschool_teachers_to_children
    12: 0,  # nursary_children_coridors
    13: 0,  # elementary_children_coridors
    14: 0,  # highschool_children_coridors
    15: 0,  # nursary_teachers
    16: 0,  # elementary_teachers
    17: 0,  # highschool_teachers
    18: 0,  # leasure_outdoor
    19: 0,  # leasure_visit
    20: 0,  # leasure_pub
    21: 0,  # work_contacts
    22: 0,  # work_workers_to_clients_distant
    23: 0,  # work_workers_to_clients_plysical_short
    24: 0,  # work_workers_to_clients_physical_long
    25: 0,  # public_transport
    26: 0,  # shops_customers
    27: 0,  # shops_workers_to_clients
    28: 0,  # pubs_customers
    29: 0,  # pubs_workers_to_clients
    30: 0,  # superspreader
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
    13: 0.8,  # elementary_children_coridors
    14: 0.8,  # highschool_children_coridors
    15: 0.8,  # nursary_teachers
    16: 0.8,  # elementary_teachers
    17: 0.8,  # highschool_teachers
    18: 0.4,  # leasure_outdoor
    19: 0.5,  # leasure_visit
    20: 0.3,  # leasure_pub
    21: 0.8,  # work_contacts
    22: 0.8,  # work_workers_to_clients_distant
    23: 0.8,  # work_workers_to_clients_plysical_short
    24: 0.8,  # work_workers_to_clients_physical_long
    25: 0.1,  # public_transport
    26: 0.1,  # shops_customers
    27: 0,  # shops_workers_to_clients
    28: 0,  # pubs_customers
    29: 0,  # pubs_workers_to_clients
    30: 0,  # superspreader
}

RISK_FOR_LAYERS_FOR_SIMPLE = {
    0: 0,
    1: 1,  # family_inside
    2: 1,  # family_in_house
    3: 0,  # family_visitsors_to_visited
    4: 0.0,  # nursary_children_inclass
    5: 0.0,  # nursary_teachers_to_children
    6: 0.0,  # lower_elementary_children_inclass
    7: 0.0,  # lower_elementary_teachers_to_children
    8: 0.0,  # higher_elementary_children_inclass
    9: 0.0,  # higher_elementary_teachers_to_children
    10: 0.0,  # highschool_children_inclass
    11: 0.0,  # highschool_teachers_to_children
    12: 0.0,  # nursary_children_coridors
    13: 0.0,  # elementary_children_coridors
    14: 0.0,  # highschool_children_coridors
    15: 0.0,  # nursary_teachers
    16: 0.0,  # elementary_teachers
    17: 0.0,  # highschool_teachers
    18: 0.0,  # leasure_outdoor
    19: 0.0,  # leasure_visit
    20: 0.0,  # leasure_pub
    21: 0.0,  # work_contacts
    22: 0.0,  # work_workers_to_clients_distant
    23: 0.0,  # work_workers_to_clients_plysical_short
    24: 0.0,  # work_workers_to_clients_physical_long
    25: 0.0,  # public_transport
    26: 0.0,  # shops_customers
    27: 0,  # shops_workers_to_clients
    28: 0,  # pubs_customers
    29: 0,  # pubs_workers_to_clients
    30: 0,  # superspreader
}


def is_R(node_ids, memberships):
    if memberships is None:
        return np.ones(len(node_ids), dtype="bool")
    recovered_states_flags = memberships[states.R_u] + memberships[states.R_d]
    release_recovered = recovered_states_flags.ravel()[node_ids]
    return release_recovered


def quarrantine_policy_setup(graph, normal_life):

    risk_for_layers = RISK_FOR_LAYERS_FOR_SIMPLE
    riskiness = np.array([risk_for_layers[i] for i in range(0, 31)])

    return {
        "quarrantine_depo": QuarrantineDepo(graph.number_of_nodes),
        "stayhome_depo": QuarrantineDepo(graph.number_of_nodes),
        "release_depo": QuarrantineDepo(graph.number_of_nodes),
        "normal_life": normal_life,
        "quarrantine_coefs": QUARANTINE_COEFS,
        "duration": 16,
        "threashold": 0.7,
        "days_back": 7,
        "riskiness": riskiness
    }


def wee_cold_policy_setup(graph, normal_life):

    return {
        "quarrantine_depo": QuarrantineDepo(graph.number_of_nodes, is_R),
        "normal_life": normal_life,
        "quarrantine_coefs": WEE_COLD_COEFS,
        "duration": 100,
        "threshold": 0.5
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

    riskiness = np.array([risk_for_layers[i] for i in range(0, 31)])

    return {
        "quarrantine_depo": QuarrantineDepo(graph.number_of_nodes),
        "normal_life": normal_life,
        "quarrantine_coefs":  QUARANTINE_COEFS,
        "duration": 14,
        "threashold": 0.7,
        "days_back": 7,
        "riskiness": riskiness
    }


def wee_cold_policy(graph, policy_coefs, history, tseries, time, contact_history=None, memberships=None):

    print("Hello, this is wee cold policy")

    last_day = _get_last_day(history, tseries, time)

    # those who became infected today
    detected_nodes = [
        node
        for node, _, e in last_day
        if e == states.I_s
        if np.random.rand() < 0.7
    ]
    if 29691 in list(detected_nodes):
        print(f"ACTION LOG({int(time)}): node {29691} does not feel well and stays home.")

    print(f"Nodes with a wee cold: {len(detected_nodes)}")

    _quarrantine_nodes(
        detected_nodes, policy_coefs, graph, memberships)
    released = _tick(policy_coefs, memberships)
    if 29691 in list(released):
        print(f"ACTION LOG({int(time)}: node {29691} feels well again and stops staying home.")

    to_change = _release_nodes(released, policy_coefs, graph)

    return to_change


def simple_quarrantine_policy(graph, policy_coefs, history, tseries, time, contact_history=None, memberships=None):

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

    print(f"Qurantined nodes: {len(detected_nodes)}")

    _quarrantine_nodes(detected_nodes, policy_coefs, graph, memberships)
    released = _tick(policy_coefs, memberships)
    to_change = _release_nodes(released, policy_coefs, graph)

    return to_change


def quarrantine_with_contact_tracing_policy(graph, policy_coefs, history, tseries, time, contact_history=None, memberships=None):

    print("Hello world! This is the eva policy function speaking.")
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
    if 29691 in detected_nodes:
        print(f"ACTION LOG({int(time)}): node {29691} was detected and is quarantined by eva and asked for contacts.")

    if contact_history is not None:
        contacts = _select_contacts(
            detected_nodes, contact_history, graph,
            policy_coefs["threashold"], policy_coefs["days_back"], policy_coefs["riskiness"])
    else:
        contacts = []

    print(f"Qurantined nodes: {len(detected_nodes)}")
    print(f"Found contacts: {len(contacts)}")
    if 29691 in list(contacts):
        print(f"ACTION LOG({int(time)}): node {29691} was marked as contact.")

    depo = policy_coefs["quarrantine_depo"]
    released_waiting_nodes = depo.get_waiting()
    depo.wait(list(contacts))
    print(f"Quaratinted contacts: {len(released_waiting_nodes)}")
    if 29691 in list(released_waiting_nodes):
        print(f"ACTION LOG({int(time)}): node {29691} was quarantined by Eva (because beeing contact).")

    # friends of detected
    _quarrantine_nodes(
        detected_nodes+list(released_waiting_nodes), policy_coefs, graph, memberships)
    released = _tick(policy_coefs, memberships)

    really_released, release_candidates, prisoners = _do_testing(
        released, memberships)
    assert len(release_candidates) == 0

    # prisoners back to quarrantine
    if len(prisoners) > 0:
        policy_coefs["quarrantine_depo"].lock_up(prisoners, 2)
        if 29691 in list(prisoners):
            print(f"ACTION LOG({int(time)}): node {29691} waits for possitive tests in eva quarantine.")



    if 29691 in list(really_released):
        print(f"ACTION LOG({int(time)}): node {29691} was released from quarantine by eva.")

    #    _quarrantine_nodes(
    #        detected_nodes+list(contacts), policy_coefs, graph, memberships)

    to_change = _release_nodes(really_released, policy_coefs, graph)

    return to_change


def petra_policy(graph, policy_coefs, history, tseries, time, contact_history=None, memberships=None):

    print("Hello world! This is the petra policy function speaking.")
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
    if 29691 in detected_nodes:
        print(f"ACTION LOG({int(time)}): node {29691} was dectected and qurantined by petra.")

    if contact_history is not None:
        contacts = _select_contacts(
            detected_nodes, contact_history, graph,
            policy_coefs["threashold"], policy_coefs["days_back"], policy_coefs["riskiness"])
    else:
        contacts = []

    print(f"Qurantined nodes: {len(detected_nodes)}")
    print(f"Quaratinted contacts: {len(contacts)}")
    if 29691 in list(contacts):
        print(f"ACTION LOG({int(time)}): node {29691} has detected family member and stays home.")

    # friends of detected
    _quarrantine_nodes(
        detected_nodes, policy_coefs, graph, memberships)

    _stay_home_nodes(
        list(contacts), policy_coefs, graph, memberships)

    released = _tick(policy_coefs, memberships)

    really_released, release_candidates, prisoners = _do_testing(
        released, memberships)
    assert len(release_candidates) == 0

    # prisoners back to quarrantine
    if len(prisoners) > 0:
        policy_coefs["quarrantine_depo"].lock_up(prisoners, 2)

    if 29691 in list(prisoners):
        print(f"ACTION LOG({int(time)}): node {29691} tested and stays in quarantine by petra.")

    if 29691 in list(really_released):
        print(f"ACTION LOG({int(time)}): node {29691} was released from quarantine by petra.")

    released = _tick_home(policy_coefs, memberships)
    if 29691 in list(released):
        print(f"ACTION LOG({int(time)}): node {29691} stops staying home.")

    to_change = _release_nodes(
        list(really_released)+list(released), policy_coefs, graph)

    return to_change


def _do_testing(released, memberships):
    print("Release candidates", len(released))
    if memberships is None:
        raise ValueError("Sorry, we need states to make a decision.")
    if not len(released) > 0:
        return np.array([]), np.array([]), np.array([])

    # recovered release, other stay
    # todo first and second testing
    node_is_R = is_R(released, memberships) == 1
    really_released = released[node_is_R]
    still_ill = released[node_is_R == False]

    return really_released, np.array([]), still_ill


def _get_last_day(history, tseries, time):
    current_day = int(time)
    start = np.searchsorted(tseries, current_day, side="left")

    if start == 0:
        start = 1
    end = np.searchsorted(tseries, current_day+1, side="left")
    return history[start:end]


def _quarrantine_nodes(detected_nodes, policy_coefs, graph, memberships):

    depo = policy_coefs["quarrantine_depo"]
    quarantine_coefs = policy_coefs["quarrantine_coefs"]
    normal_life = policy_coefs["normal_life"]
    duration = policy_coefs["duration"]

    #    for node in detected_nodes:
    # print(f"Node {node} goes to quarantine")
    if detected_nodes:
        graph.modify_layers_for_nodes(detected_nodes,
                                      quarantine_coefs,
                                      depo.quarrantine)
        depo.lock_up(detected_nodes, duration)
    #    print(">>>", depo.quarrantine)


def _stay_home_nodes(detected_nodes, policy_coefs, graph, memberships):

    depo = policy_coefs["stayhome_depo"]
    quarantine_coefs = policy_coefs["quarrantine_coefs"]
    normal_life = policy_coefs["normal_life"]
    duration = policy_coefs["duration"]

    #    for node in detected_nodes:
    # print(f"Node {node} goes to quarantine")
    if detected_nodes:
        graph.modify_layers_for_nodes(detected_nodes,
                                      quarantine_coefs,
                                      depo.quarrantine)
        depo.lock_up(detected_nodes, duration)
    #    print(">>>", depo.quarrantine)


def _tick(policy_coefs, memberships):
    depo = policy_coefs["quarrantine_depo"]
    released = depo.tick_and_get_released(memberships)
    return released


def _tick_home(policy_coefs, memberships):
    depo = policy_coefs["stayhome_depo"]
    released = depo.tick_and_get_released(memberships)
    return released


def _release_nodes(released, policy_coefs, graph):

    depo = policy_coefs["quarrantine_depo"]

    if len(released) > 0:
        print(f"Released nodes: {released}")
        graph.recover_edges_for_nodes(released,
                                      None,
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
