import click
import datetime
import os
import random
import timeit
import json

from config_utils import ConfigFile
from hyperparam_search.hyperparam_utils import run_hyperparam_search


@click.command()
@click.option('--set-random-seed/--no-random-seed', ' /-r', default=True)
@click.option('--policy', '-p', default=None)
@click.option('--n_jobs', default=1)
@click.option('--run_n_times', default=1)
@click.option('--out_dir',  default=f'./search_{datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")}')
@click.argument('filename', default="town0.ini")
@click.argument('hyperparam_filename', default="example_gridsearch.json")
def test(set_random_seed, policy, n_jobs, run_n_times, out_dir, filename, hyperparam_filename):
    random_seed = 42 if set_random_seed else random.randint(0, 10000)

    cf = ConfigFile()
    cf.load(filename)

    print(f"Output directory for results: {out_dir}")
    print(f"Running with n_jobs == {n_jobs}.")

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    def search_func():
        result_file_name = os.path.join(out_dir, f'result.txt')
        results = run_hyperparam_search(
            filename,
            hyperparam_filename,
            model_random_seed=random_seed,
            use_policy=policy,
            n_jobs=n_jobs,
            return_func=return_func,
            return_func_kwargs=return_func_kwargs,
            run_n_times=run_n_times
        )

        with open(result_file_name, "w") as f:
            for params, value in results:
                param_str = json.dumps(params)
                f.write(f"{param_str}, {value}\n")

    print(timeit.timeit(search_func, number=1))


if __name__ == "__main__":
    test()
