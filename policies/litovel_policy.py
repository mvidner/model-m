from quarrantine_policy import quarrantine_with_contact_tracing_policy, quarrantine_policy_setup
from calendar_policy import calendar_policy


def litovel_setup(*args, **kwargs):
    return quarrantine_policy_setup(*args, **kwargs)


def litovel_policy(graph, policy_coefs, history, tseries, time, contact_history=None):

    ret = quarrantine_with_contact_tracing_policy(
        graph, policy_coefs, history, tseries, time, contact_history)
    ret.update(calendar_policy(graph, policy_coefs,
                               history, tseries, time, contact_history))
    if "graph" in ret:
        return {"graph": graph.final_adjacency_matrix()}
    else:
        return {}
