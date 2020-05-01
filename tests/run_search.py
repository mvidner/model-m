import click
import datetime
import os
import pandas as pd
import random
import timeit
import json

from config_utils import ConfigFile
from hyperparam_search.hyperparam_utils import run_hyperparam_search


def load_gold_data(csv_path):
    df = pd.read_csv(csv_path)
    dates = pd.to_datetime(df["datum"])
    dates = dates - dates[0]
    dates = dates.apply(lambda t: t.days + 1)

    result = pd.DataFrame({"day": range(1, dates.max() + 1), "infected": pd.NA})
    result.loc[result["day"].isin(dates), "infected"] = df.iloc[:, 1].to_list()

    result.fillna(method='ffill', inplace=True)

    return pd.DataFrame({"day": dates, "infected": df.iloc[:, 1]})


@click.command()
@click.option('--set-random-seed/--no-random-seed', ' /-r', default=True)
@click.option('--policy', '-p', default=None)
@click.option('--n_jobs', default=1)
@click.option('--run_n_times', default=1)
@click.option('--return_func', default='rmse')
@click.option('--fit_data', default='litovel.csv')
@click.option('--out_dir',  default=f'./search_{datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")}')
@click.argument('filename', default="town0.ini")
@click.argument('hyperparam_filename', default="example_gridsearch.json")
def test(set_random_seed, policy, n_jobs, run_n_times, return_func, fit_data, out_dir, filename, hyperparam_filename):
    random_seed = 42 if set_random_seed else random.randint(0, 10000)

    cf = ConfigFile()
    cf.load(filename)

    print(f"Output directory for results: {out_dir}")
    print(f"Running with n_jobs == {n_jobs}.")

    def search_func():
        result_file_name = os.path.join(out_dir, f'result.txt')
        results = run_hyperparam_search(
            filename,
            hyperparam_filename,
            model_random_seed=random_seed,
            use_policy=policy,
            n_jobs=n_jobs,
            return_func=return_func,
            return_func_kwargs={"y_true": load_gold_data(fit_data)["infected"].to_numpy()},
            run_n_times=run_n_times
        )

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        
        with open(result_file_name, "w") as f:
            for params, value in results:
                param_str = json.dumps(params)
                f.write(f"{param_str}, {value}\n")

    print(timeit.timeit(search_func, number=1))


if __name__ == "__main__":
    test()
