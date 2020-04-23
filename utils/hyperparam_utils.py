from joblib import delayed, Parallel
from typing import Iterable, Dict, Callable


def run_single_model(model_cls, model, kwargs, ndays, print_interval=10, verbose=False):
    model.run(T=ndays, verbose=verbose, print_interval=print_interval)


def _hyperparam_search(model_func: Callable,
                       hyperparam_gen: Iterable[Dict] = None):
    """

    Params:
        model_func: A function of signature `func(**kwargs)` that creates the model.
        hyperparam_gen: Generates kwargs - hyperparameters - for model func.

    Returns:

    """

    for hyperparam_dict in hyperparam_gen:
        yield model_func(hyperparam_dict)


# TODO parse configs func
# TODO create model func - sth that initializes a graph and takes some hyperparams
# TODO aka this etc; it should take a graph-creating-func and call it I guess, same with policy and other things
"""

graph_name = cf.section_as_dict("GRAPH")["name"]
    nodes = cf.section_as_dict("GRAPH").get("nodes", "nodes.csv")
    edges = cf.section_as_dict("GRAPH").get("edges", "edges.csv")
    layers = cf.section_as_dict("GRAPH").get("layers", "etypes.csv")

    start = time.time()
    graph = create_graph(graph_name, nodes=nodes, edges=edges,
                         layers=layers, num_nodes=num_nodes)
"""

# TODO also better history grouping for results
# TODO multiple models - again a generator; init is pairs of config files - orig and list one
# TODO or one config and if sth is a list, its a generator, else simple model
# TODO and different search strategies