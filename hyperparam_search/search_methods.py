import cma
import numpy as np
from functools import partial
from multiprocessing import Pool

from cma.optimization_tools import EvalParallel2
from sklearn.model_selection import ParameterGrid


def _run_model_with_hyperparams(model_func, hyperparams):
    print(f"Running with hyperparams: {hyperparams}", flush=True)

    res = model_func(hyperparams=hyperparams)
    print(f"Finished run with hyperparams: {hyperparams}")
    return res


def perform_gridsearch(model_func, hyperparam_config, n_jobs=1):
    grid = hyperparam_config["MODEL"]
    param_grid = ParameterGrid(grid)

    run_model = partial(_run_model_with_hyperparams, model_func)
    with Pool(processes=n_jobs) as pool:
        res = pool.map(run_model, param_grid)

    return res


def evaluate_with_params(param_array: np.ndarray, model_func, param_keys):
    assert len(param_array) == len(param_keys)
    hyperparam_dict = _keys_with_evolved_vals(param_array, param_keys)
    model_res = model_func(hyperparam_dict)["result"]

    return np.mean(model_res)


def _keys_with_evolved_vals(evolved_vals, keys):
    return {k: v for k, v in zip(keys, evolved_vals)}


def cma_es(model_func, hyperparam_config, return_only_best=False, n_jobs=1):
    initial_kwargs = hyperparam_config["MODEL"]

    initial_vals = [v for v in initial_kwargs.values()]
    sigma = hyperparam_config["SIGMA"]
    cma_kwargs = hyperparam_config["CMA"]

    eval_func = partial(evaluate_with_params, model_func=model_func, param_keys=list(initial_kwargs.keys()))

    es = cma.CMAEvolutionStrategy(initial_vals, sigma, cma_kwargs)
    with EvalParallel2(fitness_function=eval_func, number_of_processes=n_jobs) as eval_all:
        while not es.stop():
            X = es.ask()
            es.tell(X, eval_all(X))
            es.disp()

    res = es.result
    x = _keys_with_evolved_vals(res[0], initial_kwargs.keys())

    if return_only_best:
        return {"hyperparams": x, "result": res[1]}  # best evaluated solution, its objective function value
    return {"hyperparams": x, "result": res[1], "es_data": res[2:]}  # full result


hyperparam_search_zoo = {
    'GridSearch': perform_gridsearch,
    'CMA-ES': cma_es
}
