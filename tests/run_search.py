import datetime
import os
import random
import timeit

import click

from config_utils import ConfigFile
from hyperparam_utils import run_hyperparam_search


def save_model_results(model):
    pass


@click.command()
@click.option('--set-random-seed/--no-random-seed', ' /-r', default=True)
@click.option('--policy', '-p', default=None)
@click.option('--n_jobs', default=1)
@click.option('--out_dir',  default=f'./search_{datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")}')
@click.argument('filename', default="town0.ini")
@click.argument('hyperparam_filename', default="example_gridsearch.json")
def test(set_random_seed, policy, n_jobs, out_dir, filename, hyperparam_filename):
    random_seed = 42 if set_random_seed else random.randint(0, 10000)

    cf = ConfigFile()
    cf.load(filename)

    print(f"Output directory for results: {out_dir}")
    print(f"Running with n_jobs == {n_jobs}.")

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    def save_history(model, hyperparams):
        hyperparam_str = ','.join(f'{k}={v}' for k, v in hyperparams.items())
        file_name = os.path.join(out_dir, f'model_{hyperparam_str}.csv')

        # TODO parameters printed incorrectly in file - not overwritten by hyperparams
        cf.save(file_name)
        with open(file_name, "r") as f:
            cfg_string = "#" + "#".join(f.readlines())
        with open(file_name, "w") as f:
            f.write(cfg_string)
            f.write(f"# RANDOM_SEED = {random_seed}\n")
            model.save(f)

        save_nodes = cf.section_as_dict("TASK").get("save_node_states", "No") == "Yes"
        if save_nodes:
            model.save_node_states(f"node_states_{hyperparam_str}.csv")

    def search_func():
        return run_hyperparam_search(filename, hyperparam_filename, model_random_seed=random_seed, use_policy=policy,
                                     n_jobs=n_jobs, return_func=save_history)

    print(timeit.timeit(search_func, number=1))


if __name__ == "__main__":
    test()
