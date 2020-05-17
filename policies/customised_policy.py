from quarrantine_policy import quarrantine_policy_setup, quarrantine_with_contact_tracing_policy, simple_quarrantine_policy
from quarrantine_policy import wee_cold_policy, wee_cold_policy_setup
from policy_utils import load_scenario_dict
from functools import partial


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
    policy_object = policy_coefs["policy_object"]
    policy_object.set_policy(quarrantine_with_contact_tracing_policy)
    return {}


def update_layers(coefs, graph, *args, **kwargs):
    print("--->", graph.layer_name, coefs)
    graph.close_layers(graph.layer_name[:31], coefs)
    return {"graph": None}


CALENDAR = {
    5: switch_on_simple_policy,
    66: switch_on_eva_policy,
}


def setup(graph, normal_life=None):
    policy_object = PlainVanilla()
    policy_coefs = quarrantine_policy_setup(graph, normal_life)
    wee_cold_coefs = wee_cold_policy_setup(graph, normal_life)

    calendar_adds = load_scenario_dict("../data/policy_params/sour_2.csv")
    print(calendar_adds)
    for t, clist in calendar_adds.items():
        CALENDAR[int(t)] = partial(update_layers, clist)

    print(CALENDAR)
    return {**policy_coefs,
            **{"policy_object": policy_object,
               "calendar": CALENDAR,
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

    ret_wee = wee_cold_policy(
        graph, policy_coefs["wee_cold"], history, tseries, time, None, memberships)
    ret2 = policy_coefs["policy_object"].run(graph, policy_coefs, history,
                                             tseries, time, contact_history, memberships)

    return {**ret, **ret_wee, **ret2}
