import numpy as np
from extended_network_model import STATES as states
from policy import Policy


class QuarrantineDepo:
    def __init__(self, size, leave_cond=None):
        self.quarrantine = np.zeros(size)
        self.leave_cond = leave_cond
        self.waiting_room = np.zeros(size, dtype=bool)
        self.waiting_for_test = np.zeros(size, dtype="uint8")

    def wait(self, nodes):
        #        print("nodes w", nodes)
        if len(nodes) == 0:
            return
        self.waiting_room[nodes] = True

    def get_waiting(self):
        released = np.nonzero(self.waiting_room)[0]
        print("released w", released)
        self.waiting_room.fill(False)
        return released

    def wait_for_test(self, nodes):
        if len(nodes) == 0:
            return
        self.waiting_for_test[nodes] = 2

    def get_retested(self):
        released = np.nonzero(self.waiting_for_test == 1)[0]
        self.waiting_for_test[self.waiting_for_test > 0] -= 1
        return released

    def lock_up(self, nodes, duration):
        self.quarrantine[nodes] = duration

    def tick_and_get_released(self, memberships):
        if self.quarrantine[29691] > 0:
            print(f"ACTION LOG(?): node {29691} in quarantine, sentence {self.quarrantine[29691]}")
        released = np.nonzero(self.quarrantine == 1)[0]
        # if 29691 in released:
        #     print("LOG in released") 
        # release only if leave_cond is true
        if len(released) > 0 and self.leave_cond is not None:
            print("Applying security check")
            print(released)
            print(self.leave_cond(released, memberships))
            really_released = released[self.leave_cond(
                released, memberships) == 1]
        else:
            really_released = released
        # if 29691 in really_released:
        #     print("LOG in really_released") 
        # for those who are staying tick one day
        self.quarrantine[self.quarrantine > 1] -= 1
#        print("LOG after change 1", self.quarrantine[29691])
        # == 1 are on leave, those who are leased are set to zero
        # others are left with 1 day sentence
        self.quarrantine[really_released] -= 1
#        print("LOG after change 2", self.quarrantine[29691])
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


class QuarantinePolicy(Policy):

    def __init__(self, graph, model):
        super().__init__(graph, model)
        self.depo = QuarrantineDepo(graph.number_of_nodes)
        self.coefs = None
        self.duration = None
        self.stopped = False

    def stop(self):
        self.stopped = True

    def get_last_day(self):
        current_day = int(self.model.t)
        start = np.searchsorted(
            self.model.tseries[:self.model.tidx+1], current_day, side="left")
        if start == 0:
            start = 1
        end = np.searchsorted(
            self.model.tseries[:self.model.tidx+1], current_day+1, side="left")
        return self.model.history[start:end]

    def quarrantine_nodes(self, detected_nodes, depo=None):
        if depo is None:
            depo = self.depo
        if detected_nodes:
            self.graph.modify_layers_for_nodes(detected_nodes,
                                               self.coefs)
            depo.lock_up(detected_nodes, self.duration)

    def tick(self):
        released = self.depo.tick_and_get_released(self.model.memberships)
        return released

    def release_nodes(self, released):
        if len(released) > 0:
            print(f"Released nodes: {released}")
            self.graph.recover_edges_for_nodes(released,
                                               None)

    def do_testing(self, released):
        print("Release candidates", len(released))
        if not len(released) > 0:
            return np.array([]), np.array([])

        # recovered release, other stay
        # todo first and second testing
        node_is_R = is_R(released, self.model.memberships) == 1
        really_released = released[node_is_R]
        still_ill = released[node_is_R == False]

        return really_released,  still_ill

    def filter_contact_history(self, detected_nodes):

        if self.riskiness is None:
            return [
                contact[1]
                for contact_list in self.model.contact_history
                for contact in contact_list
                if contact[0] in detected_nodes
            ]
        else:
            relevant_contacts = [
                (contact[1], _riskiness(contact[2], self.graph, self.riskiness))
                for contact_list in self.model.contact_history
                for contact in contact_list
                if contact[0] in detected_nodes
            ]

            if not relevant_contacts:
                return relevant_contacts

            r = np.random.rand(len(relevant_contacts))
            return [
                contact
                for i, (contact, threashold) in enumerate(relevant_contacts)
                if r[i] < threashold
            ]

    def select_contacts(self, detected_nodes):
        if not self.model.contact_history:
            return []

        my_contact_history = self.model.contact_history[-self.days_back:]

        relevant_contacts = self.filter_contact_history(detected_nodes)
        return set(relevant_contacts)


class WeeCold(QuarantinePolicy):

    def __init__(self, graph, model):
        super().__init__(graph, model)
        self.depo.leave_cond = is_R
        self.coefs = WEE_COLD_COEFS
        self.duration = 7
        self.threshold = 0.7

    def run(self):
        print("Hello, this is the wee cold policy")

        last_day = self.get_last_day()

        # those who became infected today
        detected_nodes = [
            node
            for node, _, e in last_day
            if e == states.I_s
            if np.random.rand() < self.threshold
        ]

        if 29691 in list(detected_nodes):
            print(f"ACTION LOG({int(self.model.t)}): node {29691} does not feel well and stays home.")

        print(f"Nodes with a wee cold: {len(detected_nodes)}")

        self.quarrantine_nodes(detected_nodes)

        released = self.tick()
        if 29691 in list(released):
            print(f"ACTION LOG({int(self.model.t)}: node {29691} feels well again and stops staying home.")

            to_change = self.release_nodes(released)


class PetraQuarantinePolicy(QuarantinePolicy):

    def __init__(self, graph, model):
        super().__init__(graph, model)
        self.stayhome_depo = QuarrantineDepo(graph.number_of_nodes)
        self.coefs = QUARANTINE_COEFS
        self.duration = 14
        self.threshold = 0.7
        self.days_back = 7
        self.riskiness = RISK_FOR_LAYERS_FOR_SIMPLE

    def run(self):

        print(f"Hello world! This is the petra policy function speaking. {'(STOPPED)' if self.stopped else ''}")
        if self.model.contact_history is not None:
            print("Contact tracing is ON.")
        else:
            print("Warning: Contact tracing is OFF.")

        if not self.stopped:
            last_day = self.get_last_day()

            # those who became infected today
            detected_nodes = [
                node
                for node, _, e in last_day
                if e == states.I_d and not self.depo.is_locked(node)
            ]
            if 29691 in detected_nodes:
                print(f"ACTION LOG({int(self.model.t)}): node {29691} was dectected and qurantined by petra.")

            if self.model.contact_history is not None:
                contacts = self.select_contacts(detected_nodes)
            else:
                contacts = []

            print(f"Qurantined nodes: {len(detected_nodes)}")
            print(f"Quaratinted contacts: {len(contacts)}")
            if 29691 in list(contacts):
                print(f"ACTION LOG({int(self.model.t)}): node {29691} has detected family member and stays home.")

            self.quarrantine_nodes(detected_nodes)
            self.quarrantine_nodes(list(contacts), depo=self.stayhome_depo)

        released = self.tick()
        really_released, prisoners = self.do_testing(released)

        # prisoners back to quarrantine
        if len(prisoners) > 0:
            self.depo.lock_up(prisoners, 2)

            if 29691 in list(prisoners):
                print(f"ACTION LOG({int(self.model.t)}): node {29691} tested and stays in quarantine by petra.")

        if 29691 in list(really_released):
            print(f"ACTION LOG({int(self.model.t)}): node {29691} was released from quarantine by petra.")

        released = self.stayhome_depo.tick_and_get_released(
            self.model.memberships)
        if 29691 in list(released):
            print(f"ACTION LOG({int(self.model.t)}): node {29691} stops staying home.")

        to_change = self.release_nodes(
            list(really_released)+list(released))

        return to_change


class EvaQuarantinePolicy(QuarantinePolicy):

    def __init__(self, graph, model):
        super().__init__(graph, model)
        self.coefs = QUARANTINE_COEFS
        self.duration = 14
        self.threshold = 0.7
        self.days_back = 7
        self.riskiness = RISK_FOR_LAYERS

    def run(self):

        print(f"Hello world! This is the eva policy function speaking.  {'(STOPPED)' if self.stopped else ''}")
        if self.model.contact_history is not None:
            print("Contact tracing is ON.")
        else:
            print("Warning: Contact tracing is OFF.")

        last_day = self.get_last_day()

        # those who became infected today
        detected_nodes = [
            node
            for node, _, e in last_day
            if e == states.I_d and not self.depo.is_locked(node)
        ]

        if 29691 in detected_nodes:
            print(f"ACTION LOG({int(self.model.t)}): node {29691} was detected and is quarantined by eva and asked for contacts.")

        if self.model.contact_history is not None:
            contacts = self.select_contacts(detected_nodes)
        else:
            contacts = []

        print(f"Qurantined nodes: {len(detected_nodes)}")
        print(f"Found contacts: {len(contacts)}")
        if 29691 in list(contacts):
            print(f"ACTION LOG({int(self.model.t)}): node {29691} was marked as contact.")

        released_waiting_nodes = [
            x
            for x in self.depo.get_waiting()
            if not self.depo.is_locked(x)
        ]

        self.depo.wait(list(contacts))
        print(f"Quaratinted contacts: {len(released_waiting_nodes)}")
        if 29691 in list(released_waiting_nodes):
            print(f"ACTION LOG({int(self.model.t)}): node {29691} was quarantined by Eva (because beeing contact).")

        released = self.tick()
        self.quarrantine_nodes(detected_nodes+list(released_waiting_nodes))

        release_candidates, prisoners = self.do_testing(released)

        # prisoners back to quarrantine
        if len(prisoners) > 0:
            self.depo.lock_up(prisoners, 2)
        if 29691 in list(prisoners):
            print(f"ACTION LOG({int(self.model.t)}): node {29691} waits for negative test in eva quarantine.")


        really_released = self.depo.get_retested()

            
        # realease candidates are waiting for the second test
        if len(release_candidates) > 0:
            self.depo.wait_for_test(release_candidates)
            if 29691 in list(release_candidates):
                print(f"ACTION LOG({int(self.model.t)}): node {29691} has negative test and waits for second one  in eva quarantine.")


        if 29691 in list(really_released):
            print(f"ACTION LOG({int(self.model.t)}): node {29691} was released from quarantine by eva.")

        self.release_nodes(really_released)


def is_R(node_ids, memberships):
    if memberships is None:
        return np.ones(len(node_ids), dtype="bool")
    recovered_states_flags = (memberships[states.R_u] +
                              memberships[states.R_d] +
                              memberships[states.S] +
                              memberships[states.S_s])
    release_recovered = recovered_states_flags.ravel()[node_ids]
    return release_recovered


def _riskiness(contact, graph, riskiness):
    return riskiness[graph.get_layer_for_edge(contact)]
