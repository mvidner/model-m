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


def run_single_model(model, T, print_interval=10, verbose=False, return_func=None):
    model.run(T=T, verbose=verbose, print_interval=print_interval)

    # extract information to return or do some postprocessing
    if return_func is not None:
        return return_func(model)

    return model


def run_hyperparam_search(model_config: str, hyperparam_config: str, model_random_seed=42, use_policy=None, **kwargs):
    cf = ConfigFile()
    cf.load(model_config)

    # TODO preload graph only once
    model_func = partial(load_model_from_config, cf, model_random_seed=model_random_seed, use_policy=use_policy)
    hyperparam_search_func = _init_hyperparam_search(hyperparam_config)

    return hyperparam_search_func(model_func=model_func, **kwargs)


def _init_hyperparam_search(hyperparam_file: str):
    with open(hyperparam_file, 'r') as json_file:
        config = json.load(json_file)

    return partial(hyperparam_search_zoo[config["method"]], hyperparam_config=config)


def _run_model_with_hyperparams(model_func, hyperparams, return_func=None):
    print(f"Running with hyperparams: {hyperparams}")

    model, run_params = model_func(hyperparams=hyperparams)
    return run_single_model(model, **run_params, return_func=return_func)


def perform_gridsearch(model_func, hyperparam_config, n_jobs=1, return_func=None):
    grid = hyperparam_config["MODEL"]
    res = Parallel(n_jobs=n_jobs)(
        delayed(_run_model_with_hyperparams)(model_func, hp, return_func=return_func)
        for hp in ParameterGrid(grid)
    )

    return res


hyperparam_search_zoo = {
    'GridSearch': perform_gridsearch
}
