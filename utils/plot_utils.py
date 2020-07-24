import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib import animation
from typing import Dict, List


def plot_history(filename: str):
    history = _load_history(filename)
    history.plot(x="T", y="all_infectious")
    plt.show()


def plot_histories(*args, group_days: int = None, group_func: str = "max", **kwargs):
    histories = [_history_with_fname(
        filename, group_days=group_days, group_func=group_func) for filename in args]
    history_one_df = pd.concat(histories)
    _plot_lineplot(history_one_df, "day", "all_infectious", **kwargs)


def plot_mutliple_policies(policy_dict: Dict[str, List[str]],
                           group_days: int = None, group_func: str = "max", value="all_infectious", max_days=None, **kwargs):
    histories = []
    for policy_key, history_list in policy_dict.items():
        histories.extend([_history_with_fname(filename,
                                              group_days=group_days,
                                              group_func=group_func,
                                              policy_name=policy_key,
                                              max_days=max_days)
                          for filename in history_list])

    history_one_df = pd.concat(histories)
    _plot_lineplot(history_one_df, "day", value,
                   hue="policy_name", **kwargs)


def plot_mutliple_policies_everything(policy_dict: Dict[str, List[str]],
                                      group_days: int = None, group_func: str = "max",
                                      max_days=None, **kwargs):
    histories = []
    for policy_key, history_list in policy_dict.items():
        histories.extend([_history_with_fname(filename,
                                              group_days=group_days,
                                              group_func=group_func,
                                              policy_name=policy_key,
                                              max_days=max_days)
                          for filename in history_list])

    history_one_df = pd.concat(histories)
    _plot_lineplot3(history_one_df, "day",
                    hue="policy_name", **kwargs)


def plot_state_histogram(filename: str, title: str = "Simulation", states: List[str] = None, save_path: str = None):
    def animate(i):
        fig.suptitle(f"{title} - day {day_labels.iloc[i]}")

        data_i = data.iloc[i]
        for d, b in zip(data_i, bars):
            b.set_height(math.ceil(d))

    fig, ax = plt.subplots()

    history = _history_with_fname(filename, group_days=1, keep_only_all=False)
    day_labels = history["day"]
    data = history.drop(["T", "day", "all_infectious", "filename"], axis=1)
    if states is not None:
        data = data[states]

    bars = plt.bar(range(data.shape[1]),
                   data.values.max(), tick_label=data.columns)

    anim = animation.FuncAnimation(fig, animate, repeat=False, blit=False, frames=history.shape[0],
                                   interval=100)

    if save_path is not None:
        anim.save(save_path, writer=animation.FFMpegWriter(fps=10))
    plt.show()


def _plot_lineplot(history_df, x, y, hue=None, save_path=None,  **kwargs):

    title = kwargs["title"]
    del kwargs["title"]
    sns_plot = sns.lineplot(x=x, y=y, data=history_df,
                            hue=hue, estimator=np.median, ci='sd', **kwargs)
    # dirty hack (ro)
    sns_plot.set(ylim=(0, 50))
    sns_plot.set_title(title)
    if save_path is not None:
        sns_plot.get_figure().savefig(save_path)

    plt.show()


def _plot_lineplot3(history_df, x,  hue=None, save_path=None,  **kwargs):

    title = kwargs["title"]
    del kwargs["title"]

    fig, axs = plt.subplots(ncols=3)

    sns_plot = sns.lineplot(x=x, y="I_d", data=history_df,
                            hue=hue, estimator=np.median, ci='sd', ax=axs[0], **kwargs)
    # dirty hack (ro)
    axs[0].set(ylim=(0, 50))
    axs[0].set_title("detected - active cases")

    sns_plot2 = sns.lineplot(x=x, y="all_infectious", data=history_df,
                             hue=hue, estimator=np.median, ci='sd', ax=axs[1], **kwargs)
    # dirty hack (ro)
    axs[1].set(ylim=(0, 50))
    axs[1].set_title("all active cases")

    sns_plot3 = sns.lineplot(x=x, y="tests", data=history_df,
                             hue=hue, estimator=np.median, ci='sd', ax=axs[2], **kwargs)
    # # dirty hack (ro)
    # axs[2].set(ylim=(0, 25))
    axs[2].set_title("tests (without forced tests)")

    fig.suptitle(title, fontsize=20)

    if save_path is not None:
        plt.savefig(save_path)

#    plt.show()


def _history_with_fname(filename, group_days: int = None, group_func: str = "max", policy_name: str = None,
                        keep_only_all: bool = False, max_days=None):
    history = _load_history(filename, max_days=max_days)
    if keep_only_all:
        history = history[["day", "all_infectious"]]

    if group_days is not None and group_days > 0:
        history["day"] = history["day"] // group_days * group_days
        history = history.groupby(
            "day", as_index=False).agg(func=group_func)

    history.insert(0, "filename", filename)

    if policy_name is not None:
        history["policy_name"] = policy_name
    return history


def _load_history(filename: str, max_days=None) -> pd.DataFrame:
    print(filename)
    history = pd.read_csv(filename, comment="#")
    if "E" in history.columns:
        history["all_infectious"] = history[[
            "I_n", "I_a", "I_s", "E",
            "I_dn", "I_da", "I_ds", "E_d", "J_ds", "J_dn",
            "J_n", "J_s"]].sum(axis=1)
        history["I_d"] = history[[
            "I_dn", "I_da", "I_ds", "E_d", "J_ds", "J_dn"]].sum(axis=1)
        history["all_tests"] = history[[
            "tests", "quarantine_tests"]].sum(axis=1)
    if max_days is not None:
        history = history[:max_days]
    if "day" not in history.columns:
        history["day"] = range(len(history))
#    print(history)
    return history


if __name__ == "__main__":

    history = pd.read_csv(
        "../result_storage/tmp/history_seirsplus_quarantine_1.csv")
    plot_history(history)
