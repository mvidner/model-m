import cma
import numpy as np
from functools import partial
from multiprocessing import Pool

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


def cma_es(model_func, hyperparam_config, mean_of_runs=False, return_only_best=True, **kwargs):
    initial_vals = [v for v in hyperparam_config["MODEL"].values()]
    sigma = hyperparam_config["SIGMA"]
    cma_kwargs = hyperparam_config["CMA"]

    def keys_with_evolved_vals(evolved_vals):
        return {k: v for k, v in zip(hyperparam_config["MODEL"].keys(), evolved_vals)}

    def evaluate_with_params(param_array: np.ndarray):
        assert len(param_array) == len(hyperparam_config["MODEL"])
        hyperparam_dict = keys_with_evolved_vals(param_array)
        model_res = model_func(hyperparam_dict)["result"]

        return model_res if not mean_of_runs else np.mean(model_res)

    es = cma.fmin(evaluate_with_params, initial_vals, sigma, **cma_kwargs)
    x = keys_with_evolved_vals(es[0])

    if return_only_best:
        return {"result": x, "objective": es[1]}  # best evaluated solution, its objective function value
    return {"result": x, "es_data": es[1:]}  # full cma.fmin output


hyperparam_search_zoo = {
    'GridSearch': perform_gridsearch,
    'CMA-ES': cma_es
}
