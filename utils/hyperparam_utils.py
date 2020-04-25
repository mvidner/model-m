import json
import time
from functools import partial
from sklearn.model_selection import ParameterGrid

from joblib import delayed, Parallel
from typing import Iterable, Dict, Callable

from config_utils import ConfigFile
from load_model import load_model_from_config
from model_zoo import model_zoo
from policy import bound_policy


def run_single_model(model, ndays, print_interval=10, verbose=False, return_func=None):
    model.run(T=ndays, verbose=verbose, print_interval=print_interval)

    # extract information to return or do some postprocessing
    if return_func is not None:
        return return_func(model)

    return model


def run_hyperparam_search(model_config: str, hyperparam_config: str, model_random_seed=42, use_policy=None, **kwargs):
    cf = ConfigFile()
    cf.load(model_config)

    model_func = partial(load_model_from_config, cf, model_random_seed=model_random_seed, use_policy=use_policy)
    hyperparam_search_func = _init_hyperparam_search(hyperparam_config)

    return hyperparam_search_func(model_func=model_func, **kwargs)


def _init_hyperparam_search(hyperparam_file: str):
    with open(hyperparam_file, 'r') as json_file:
        config = json.load(json_file)

    return partial(hyperparam_search_zoo[config["method"]], hyperparam_config=config)


def _run_model_with_hyperparams(model_func, hyperparams):
    model, run_params = model_func(hyperparams=hyperparams)
    return model.run(**run_params)


def perform_gridsearch(model_func, hyperparam_config, n_jobs=1):
    grid = hyperparam_config["MODEL"]
    res = Parallel(n_jobs=n_jobs)(
        delayed(_run_model_with_hyperparams)(model_func, hp)
        for hp in ParameterGrid(grid)
    )

    return res



hyperparam_search_zoo = {
    'GridSearch': perform_gridsearch
}

# TODO json with hyperparam list, method specification (search strategy)

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
# TODO multiple models - again a generator; init is pairs of config files - orig and hyperparam one
# TODO and different search strategies