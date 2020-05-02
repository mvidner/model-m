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


hyperparam_search_zoo = {
    'GridSearch': perform_gridsearch
}
