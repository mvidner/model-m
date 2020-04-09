
def bound_policy(func, graph):
    """ Bounds the given function func with the particular graph. 
    Use to create a callback function for network model from
    your policy function. 
    """
    def policy_function(*args,  **kwargs):
        return func(graph, *args, **kwargs)
    return policy_function
