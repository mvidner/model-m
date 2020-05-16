import warnings

import cma
import numpy as np
import scipy.special
from functools import partial
from multiprocessing import Pool

from cma.optimization_tools import EvalParallel2
from sklearn.model_selection import ParameterGrid


def _run_model_with_hyperparams(model_func, hyperparams, output_file=None):
    print(f"Running with hyperparams: {hyperparams}", flush=True)

    res = model_func(hyperparams=hyperparams)
    _log_inidividual(output_file, hyperparams.values(), res, 0)
    print(f"Finished run with hyperparams: {hyperparams}")
    return res


def perform_gridsearch(model_func, hyperparam_config, n_jobs=1, output_file=None):
    grid = hyperparam_config["MODEL"]
    param_grid = ParameterGrid(grid)

    header = grid.keys()
    _init_output_file(output_file, header)

    run_model = partial(_run_model_with_hyperparams, model_func)
    with Pool(processes=n_jobs) as pool:
        res = pool.map(run_model, param_grid)

    return res


def evaluate_with_params(param_array: np.ndarray, model_func, param_keys):
    assert len(param_array) == len(param_keys)

    param_array = scipy.special.expit(param_array)  # sigmoid scaling between 0 and 1

    hyperparam_dict = _keys_with_evolved_vals(param_array, param_keys)
    model_res = model_func(hyperparam_dict)["result"]

    return np.mean(model_res)


def _keys_with_evolved_vals(evolved_vals, keys):
    return {k: v for k, v in zip(keys, evolved_vals)}


def _init_output_file(output_file, header):
    if output_file is not None:
        with open(output_file, 'w+') as of:
            key_string = ','.join(header)
            of.write(f"gen,{key_string},fitness\n")


def _log_inidividual(output_file, x, fitness, gen):
    if output_file is not None:
        with open(output_file, 'a') as of:
            of.write(f'{gen},{",".join(str(val) for val in x)},{fitness}\n')  # joined hyperparam values and fitness


def _inverse_sigmoid(x):
    return np.log(x/(1-x))


def cma_es(model_func, hyperparam_config: dict, return_only_best=False, output_file=None, n_jobs=1):
    initial_kwargs = hyperparam_config["MODEL"]
    _init_output_file(output_file, initial_kwargs.keys())

    initial_vals = np.array([v for v in initial_kwargs.values()])
    initial_vals = _inverse_sigmoid(initial_vals)

    sigma = hyperparam_config["SIGMA"]
    cma_kwargs = hyperparam_config["CMA"]

    eval_func = partial(evaluate_with_params, model_func=model_func, param_keys=list(initial_kwargs.keys()))

    es = cma.CMAEvolutionStrategy(initial_vals, sigma, cma_kwargs)
    with EvalParallel2(fitness_function=eval_func, number_of_processes=n_jobs) as eval_all:
        gen_n = 0
        while not es.stop():
            X = es.ask()
            fitnesses = eval_all(X)
            es.tell(X, fitnesses)
            es.disp()

            for x, f in zip(X, fitnesses):
                _log_inidividual(output_file, scipy.special.expit(x).tolist(), f, gen_n)

            gen_n += 1

    res = es.result
    x = _keys_with_evolved_vals(res[0], initial_kwargs.keys())
    x = scipy.special.expit(x)

    if return_only_best:
        return {"hyperparams": x, "result": res[1]}  # best evaluated solution, its objective function value
    return {"hyperparams": x, "result": res[1], "es_data": res[2:]}  # full result


hyperparam_search_zoo = {
    'GridSearch': perform_gridsearch,
    'CMA-ES': cma_es
}
