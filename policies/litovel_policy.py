from quarrantine_policy import quarrantine_with_contact_tracing_policy, quarrantine_policy_setup, simple_quarrantine_policy
from calendar_policy import calendar_policy


def litovel_setup(*args, **kwargs):
    return quarrantine_policy_setup(*args, **kwargs)


def litovel_policy(graph, policy_coefs, history, tseries, time, contact_history=None):

    ret = quarrantine_with_contact_tracing_policy(
        graph, policy_coefs, history, tseries, time, contact_history)
    ret.update(calendar_policy(graph, policy_coefs,
                               history, tseries, time, contact_history))
    return ret

def litovel_old_policy(graph, policy_coefs, history, tseries, time, contact_history=None):

    ret = simple_quarrantine_policy(
        graph, policy_coefs, history, tseries, time, contact_history)
    ret.update(calendar_policy(graph, policy_coefs,
                               history, tseries, time, contact_history))
    return ret
