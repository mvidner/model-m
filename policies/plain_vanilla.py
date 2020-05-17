from quarrantine_policy import quarrantine_policy_setup, quarrantine_with_contact_tracing_policy, simple_quarrantine_policy
from quarrantine_policy import wee_cold_policy, wee_cold_policy_setup
from quarrantine_policy import RISK_FOR_LAYERS
import numpy as np

class PlainVanilla:
    def __init__(self):
        # do nothing function
        self.policy = lambda *args, **kwargs: {}

    def set_policy(self, func):
        self.policy = func

    def run(self, *args):
        return self.policy(*args)


def switch_on_simple_policy(graph, policy_coefs, *args, **kwargs):
    policy_object = policy_coefs["policy_object"]
    policy_object.set_policy(quarrantine_with_contact_tracing_policy)
    return {}


def switch_on_eva_policy(graph, policy_coefs, *args, **kwargs):
    risk_for_layers = RISK_FOR_LAYERS
    riskiness = np.array([risk_for_layers[i] for i in range(0, 31)])
    policy_coefs["riskiness"] = riskiness
    return {}

def close_schools(graph, *args, **kwargs):
    close = [
        "nursary_children_inclass",
        "nursary_teachers_to_children",
        "lower_elementary_children_inclass",
        "lower_elementary_teachers_to_children",
        "higher_elementary_children_inclass",
        "higher_elementary_teachers_to_children",
        "highschool_children_inclass",
        "highschool_teachers_to_children",
        "nursary_children_coridors",
        "elementary_children_coridors",
        "highschool_children_coridors",
        "nursary_teachers",
        "elementary_teachers",
        "highschool_teachers"
    ]
    graph.close_layers(close)
    return {"graph": None}


def close_pubs(graph, *args, **kwargs):
    weaken = ["leasure_visit", "leasure_pub",
              "pubs_customers", "pubs_workers_to_clients"]
    coefs = [0.5] * len(weaken)
    graph.close_layers(weaken, coefs)
    return {"graph": None}


def close_shops(graph, *args, **kwargs):
    weaken = ["family_visitsors_to_visited",
              "work_contacts",
              "work_workers_to_clients_distant",
              "work_workers_to_clients_plysical_short",
              "work_workers_to_clients_physical_long",
              "public_transport",
              "shops_customers", "shops_workers_to_clients",
              "pubs_customers", "pubs_workers_to_clients",
              "leasure_outdoor", "leasure_pub", "leasure_visit"]
    coefs = [0.2, 0.5, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0, 0,
             0, 0, 0]
    graph.close_layers(weaken, coefs)
    return {"graph": None}


def open_some(graph, *args, **kwargs):
    change = ["leasure_outdoor",
              "work_contacts",
              "work_workers_to_clients_distant",
              "work_workers_to_clients_physical_long",
              "work_workers_to_clients_plysical_short",
              "public_transport",
              "shops_customers", "shops_workers_to_clients"
              ]
    coefs = [0.2, 
             0.5,
             0.2, 0.2, 0.2, 0.2, 
             0.3, 0.3]
    graph.close_layers(change, coefs)
    return {"graph": None}


def open_small_shops(graph, *args, **kwargs):
    change = ["public_transport",
              "shops_customers", "shops_workers_to_clients"
              ]
    coefs = [0.5, 0.6, 0.6]
    graph.close_layers(change, coefs)
    return {"graph": None}


def all_shops(graph, *args, **kwargs):
    change = ["family_visitsors_to_visited",
              "higher_elementary_children_inclass", 
              "higher_elementary_teachers_to_children",
              "highschool_children_inclass", 
              "highschool_teachers_to_children",
              "elementary_children_coridors", 
              "highschool_children_coridors",
              "elementary_teachers", 
              "highschool_teachers",
              "leasure_outdoor",
              "work_contacts", "work_workers_to_clients_distant",
              "work_workers_to_clients_physical_long", "work_workers_to_clients_plysical_short",
              "public_transport",
              "shops_customers", "shops_workers_to_clients",
              "pubs_workers_to_clients"]
    coefs = [0.5,
             0.2, 0.2,
             0.2, 0.2,
             0.2, 0.2,
             0.5, 0.5,
             0.5,
             0.5, 0.5,
             0.5, 0.5,
             0.5,
             1, 1,
             0.1]
    graph.close_layers(change, coefs)
    return {"graph": None}


def open_all(graph, *args, **kwargs):
    change = ["family_visitsors_to_visited",
              "nursary_children_inclass", "nursary_teachers_to_children",
              "lower_elementary_children_inclass", "lower_elementary_teachers_to_children",
              "higher_elementary_children_inclass", "higher_elementary_teachers_to_children",
              "highschool_children_inclass", "highschool_teachers_to_children",
              "nursary_children_coridors",
              "elementary_children_coridors",
              "highschool_children_coridors",
              "nursary_teachers", "elementary_teachers", 
              "highschool_teachers"]
    opened = ["leasure_outdoor", "leasure_pub", "leasure_visit",
              "work_contacts", "work_workers_to_clients_distant",
              "work_workers_to_clients_physical_long", "work_workers_to_clients_plysical_short",
              "public_transport",
              "shops_customers", "shops_workers_to_clients",
              "pubs_customers", "pubs_workers_to_clients"]
    coefs = [1,
             1, 1,
             0.6, 0.6,
             0.2, 0.2,
             0.2, 0.2,
             1, 
             0.5,
             0.5,
             1, 0.5, 0.5]
    graph.close_layers(change+opened, coefs+[1]*len(opened))
    return {"graph": None}


CALENDAR = {
    5: switch_on_simple_policy,
    15: close_schools,
    16: close_pubs,
    18: close_shops,
    55: open_some,
    62: open_small_shops,
    66: switch_on_eva_policy,
    76: all_shops,
    90: open_all
}

CALENDAR2 = {
    5: switch_on_simple_policy,
    66: switch_on_eva_policy,
}


def setup(graph, normal_life=None):
    policy_object = PlainVanilla()
    policy_coefs = quarrantine_policy_setup(graph, normal_life)
    wee_cold_coefs = wee_cold_policy_setup(graph, normal_life)
    return {**policy_coefs,
            **{"policy_object": policy_object,
               "calendar": CALENDAR,
               "wee_cold": wee_cold_coefs}
            }

def setup_no_close(graph, normal_life=None):
    policy_object = PlainVanilla()
    policy_coefs = quarrantine_policy_setup(graph, normal_life)
    wee_cold_coefs = wee_cold_policy_setup(graph, normal_life)
    return {**policy_coefs,
            **{"policy_object": policy_object,
               "calendar": CALENDAR2,
               "wee_cold": wee_cold_coefs}
            }





def policy(graph, policy_coefs, history, tseries, time, contact_history=None, memberships=None):

    calendar = policy_coefs["calendar"]
    today = int(time)

    ret = {}
    if today in calendar:
        # run today action
        ret = calendar[today](graph, policy_coefs, history,
                              tseries, time, contact_history)

    ret_wee = wee_cold_policy(graph, policy_coefs["wee_cold"], history, tseries, time, None, memberships)
    ret2 = policy_coefs["policy_object"].run(graph, policy_coefs, history,
                                             tseries, time, contact_history, memberships)

    return {**ret, **ret_wee, **ret2}
