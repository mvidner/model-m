import click
import datetime
import numpy as np
import os
import pandas as pd
import random
import timeit

from config_utils import ConfigFile
from hyperparam_search.hyperparam_utils import run_hyperparam_search


def load_gold_data(csv_path, first_n_zeros=0):
    df = pd.read_csv(csv_path)
    dates = pd.to_datetime(df["datum"])
    dates = dates - dates[0]
    dates = dates.apply(lambda t: t.days + 1)

    result = pd.DataFrame({"day": range(1, dates.max() + 1), "infected": pd.NA})
    result.loc[result["day"].isin(dates), "infected"] = df.iloc[:, 1].to_list()

    result.fillna(method='ffill', inplace=True)

    if first_n_zeros > 0:
        result["day"] += first_n_zeros

        first_n = [{"day": i + 1, "infected": 0} for i in range(first_n_zeros)]
        result = pd.concat([pd.DataFrame(first_n), result], ignore_index=True)

    return result


@click.command()
@click.option('--set-random-seed/--no-random-seed', ' /-r', default=True)
@click.option('--policy', '-p', default=None)
@click.option('--n_jobs', default=1)
@click.option('--run_n_times', default=1)
@click.option('--first_n_zeros', default=5)
@click.option('--return_func', default='rmse')
@click.option('--fit_data', default='litovel.csv')
@click.option('--out_dir',  default=f'./search_{datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")}')
@click.argument('filename', default="town0.ini")
@click.argument('hyperparam_filename', default="example_gridsearch.json")
def test(set_random_seed, policy, n_jobs, run_n_times, first_n_zeros, return_func, fit_data, out_dir,
         filename, hyperparam_filename):

    random_seed = 42 if set_random_seed else random.randint(0, 10000)

    cf = ConfigFile()
    cf.load(filename)

    print(f"Output directory for results: {out_dir}")
    print(f"Running with n_jobs == {n_jobs}.")

    def search_func():
        gold_data = load_gold_data(fit_data, first_n_zeros=first_n_zeros)["infected"].to_numpy()

        results = run_hyperparam_search(
            filename,
            hyperparam_filename,
            model_random_seed=random_seed,
            use_policy=policy,
            n_jobs=n_jobs,
            n_days=len(gold_data),
            return_func=return_func,
            return_func_kwargs={"y_true": gold_data},
            run_n_times=run_n_times
        )

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        res_list = []
        for res in results:
            mean_val = np.mean(res['result'])

            res_row = {**res["hyperparams"], f"mean_{return_func}": mean_val}
            res_list.append(res_row)

        fit_name = os.path.split(fit_data)[1].split('.')[0]

        df = pd.DataFrame(data=res_list)
        df.to_csv(os.path.join(out_dir, f'result_{return_func}_{fit_name}_seed={random_seed}.csv'))

    print(timeit.timeit(search_func, number=1))


if __name__ == "__main__":
    test()
