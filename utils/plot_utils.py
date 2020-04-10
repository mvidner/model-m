import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_history(filename: str):
    history = _load_history(filename)
    history.plot(x="T", y="all_infectious")
    plt.show()


def plot_histories(*args, group_days=None, group_func="mean"):
    def history_with_fname(filename):
        history = _load_history(filename)
        history = history[['day', 'all_infectious']]

        if group_days is not None and group_days > 0:
            history['day'] = history['day'] // group_days * group_days
            history = history.groupby(
                'day', as_index=False).agg(func=group_func)

        history.insert(0, 'filename', filename)
        return history

    histories = [history_with_fname(filename) for filename in args]
    history_one_df = pd.concat(histories)

    sns.lineplot(x="day", y="all_infectious", data=history_one_df)
    plt.show()


def _load_history(filename: str) -> pd.DataFrame:
    history = pd.read_csv(filename)
    history["all_infectious"] = history[[
        "I_n", "I_a", "I_s", "I_d", "E"]].sum(axis=1)
    return history


if __name__ == "__main__":

    history = pd.read_csv(
        "../result_storage/tmp/history_seirsplus_quarantine_1.csv")
    plot_history(history)
