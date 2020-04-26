import json
import time
from functools import partial
from sklearn.model_selection import ParameterGrid

from joblib import delayed, Parallel
from typing import Iterable, Dict, Callable

from config_utils import ConfigFile
from load_model import load_model_from_config, load_graph
from model_zoo import model_zoo
from policy import bound_policy

from engine_sequential import SequentialEngine


def run_hyperparam_search(model_config: str,
                          hyperparam_config: str,
                          model_random_seed: int = 42,
                          use_policy: str = None,
                          preload_graph: bool = False,
                          run_n_times: int = 1,
                          return_func: callable = None,
                          **kwargs):
    """
    Run hyperparameter search on a model loaded from config. Hyperparameters specified in `hyperparam_config`
    overwrite those in `model_config`. Search method is defined in `hyperparam_config` as well.

    A single model run returns the model as a whole. If only a part of info is to be extracted, pass
    the callable `return_func(model, **kwargs)` to this function. In **kwargs, additional run info is passed
    like model seed or chosen hyperparameters.

    It is possible to run a single model multiple times with same hyperparameters, if `run_n_times` > 1.
    In such case, the result of the run is a list of models and the signature of `return_func` (if provided)
    should be `return_func(models: List[Model], **kwargs)`.

    Params:
        model_config: Model config filename (ini)
        hyperparam_config: Hyperparam search filename (json)
        model_random_seed: Initial random seed for every model.
        use_policy: Name of the policy to use.
        preload_graph: If True, only one graph is used for all models. CAUTION - in current implementation,
            it is the same graph instance, so modifications in a single model are carried over to all other
            models.

        run_n_times: For a single model (with specific hyperparams), repeat run multiple times. Random seed
            for i-th run is set to `model_random_seed` + i.

        return_func: Callable of signature `return_func(model, **kwargs)`. Used to modify results of runs,
            e.g. extract and save only the history.

        **kwargs: Additional keyword arguments to pass to the hyperparam search function,
            possibly specific to the given method).

    Returns: Result of hyperparameter optimization (specific to search method).
    """

    cf = ConfigFile()
    cf.load(model_config)

    # TODO handle preloading in case the graph is modified during simulation (e.g. [deep]copy)
    graph = load_graph(cf) if preload_graph else None

    # wrapper for running one model same time with different seed
    model_load_func = partial(_run_models_from_config,
                              cf,
                              preloaded_graph=graph,
                              model_random_seed=model_random_seed,
                              use_policy=use_policy,
                              run_n_times=run_n_times,
                              return_func=return_func)

    hyperparam_search_func = _init_hyperparam_search(hyperparam_config)
    return hyperparam_search_func(model_func=model_load_func, **kwargs)


def run_single_model(model, T, print_interval=10, verbose=False):
    model.run(T=T, verbose=verbose, print_interval=print_interval)
    return model


def _run_models_from_config(cf: ConfigFile,
                            hyperparams: Dict = None,
                            preloaded_graph=None,
                            model_random_seed: int = 42,
                            use_policy: str = None,
                            run_n_times: int = 1,
                            return_func: callable = None):
    # for different seeds
    def _load_run_one_model(seed):
        model, run_params = load_model_from_config(cf,
                                                   hyperparams=hyperparams,
                                                   preloaded_graph=preloaded_graph,
                                                   model_random_seed=seed,
                                                   use_policy=use_policy)
        return run_single_model(model, **run_params)

    if run_n_times > 1:
        # add 1 to seed each run
        res = [_load_run_one_model(seed) for seed in range(model_random_seed, model_random_seed + run_n_times)]
    else:
        res = _load_run_one_model(model_random_seed)

    if return_func is None:
        return res

    # optionally return additional run info
    return return_func(res,
                       hyperparams=hyperparams,
                       model_random_seed=model_random_seed,
                       use_policy=use_policy)


def _init_hyperparam_search(hyperparam_file: str):
    with open(hyperparam_file, 'r') as json_file:
        config = json.load(json_file)

    return partial(hyperparam_search_zoo[config["method"]], hyperparam_config=config)

    # , [ run_single_model(model, **run_params, return_func=None).to_df()
    # for i in range(10)
    # ])


def _run_model_with_hyperparams(model_func, hyperparams):
    print(f"Running with hyperparams: {hyperparams}", flush=True)

    res = model_func(hyperparams=hyperparams)
    print(f"Finished run with hyperparams: {hyperparams}")
    return res


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
