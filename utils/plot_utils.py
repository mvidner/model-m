from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_history(filename: str):
    history = _load_history(filename)
    history.plot(x="T", y="all_infectious")
    plt.show()


def plot_histories(*args, group_days: int = None, group_func: str = "max", **kwargs):
    histories = [_history_with_fname(filename, group_days=group_days, group_func=group_func) for filename in args]
    history_one_df = pd.concat(histories)
    _plot_lineplot(history_one_df, "day", "all_infectious", **kwargs)
    

def plot_mutliple_policies(policy_dict: Dict[str, List[str]],
                           group_days: int = None, group_func: str = "max", **kwargs):
    histories = []
    for policy_key, history_list in policy_dict.items():
        histories.extend([_history_with_fname(filename,
                                              group_days=group_days,
                                              group_func=group_func,
                                              policy_name=policy_key)
                          for filename in history_list])

    history_one_df = pd.concat(histories)
    _plot_lineplot(history_one_df, "day", "all_infectious", hue="policy_name", **kwargs)
    
    
def _plot_lineplot(history_df, x, y, hue=None, save_path=None, **kwargs):
    sns_plot = sns.lineplot(x=x, y=y, data=history_df, hue=hue, **kwargs)
    if save_path is not None:
        sns_plot.get_figure().savefig(save_path)

    plt.show()


def _history_with_fname(filename, group_days: int = None, group_func: str = "max", policy_name: str = None):
    history = _load_history(filename)
    history = history[["day", "all_infectious"]]

    if group_days is not None and group_days > 0:
        history["day"] = history["day"] // group_days * group_days
        history = history.groupby(
            "day", as_index=False).agg(func=group_func)

    history.insert(0, "filename", filename)

    if policy_name is not None:
        history["policy_name"] = policy_name
    return history


def _load_history(filename: str) -> pd.DataFrame:
    history = pd.read_csv(filename)
    history["all_infectious"] = history[[
        "I_n", "I_a", "I_s", "I_d", "E"]].sum(axis=1)
    return history


if __name__ == "__main__":

    history = pd.read_csv(
        "../result_storage/tmp/history_seirsplus_quarantine_1.csv")
    plot_history(history)
