import numpy as np
from quarrantine_policy import quarrantine_policy_setup, quarrantine_with_contact_tracing_policy, simple_quarrantine_policy
from quarrantine_policy import wee_cold_policy, wee_cold_policy_setup



RISK_FOR_LAYERS = {
        1: 1,  # family_inside
        2: 1,  # family_in_house
        3: 0.8,  # family_visitsors_to_visited
}



def setup(graph, normal_life=None):


    policy_coefs = setup_baseline(graph)

    wee_cold_coefs = wee_cold_policy_setup(graph, normal_life)
    policy_coefs["duration"]  = 300
    policy_coefs["wee_cold"] = wee_cold_coefs

    return policy_coefs

def setup_baseline(graph, normal_life=None):
    policy_coefs = quarrantine_policy_setup(graph, normal_life)

    riskiness = np.array([RISK_FOR_LAYERS.get(i, 0) for i in range(0, 32)])
    policy_coefs["riskiness"] = riskiness

    return policy_coefs



def policy(graph, policy_coefs, history, tseries, time, contact_history=None):

    if "wee_cold" in policy_coefs:
        ret_wee = wee_cold_policy(graph, policy_coefs["wee_cold"], history, tseries, time, None)
    else:
        ret_wee = {}
    ret = quarrantine_with_contact_tracing_policy(graph, policy_coefs, history,
                                                  tseries, time, contact_history)

    return {**ret_wee, **ret}
