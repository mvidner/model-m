
def bound_policy(func, graph, coefs=None):
    """ Bounds the given function func with the particular graph. 
    Use to create a callback function for network model from
    your policy function. 
    """
    if coefs is None:
        def policy_function(*args,  **kwargs):
            return func(graph, *args, **kwargs)
        return policy_function
    else:
        def policy_function(*args, **kwargs):
            return func(graph, coefs, *args, **kwargs)
        return policy_function
