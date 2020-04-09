# vzkaz pro Gabinu: smaz tu a prepis tu cokoli budes chtit

import pandas as pd
import matplotlib.pyplot as plt


def plot_history(filename):

    history = pd.read_csv(filename)
    history["all_infectious"] = history[[
        "I_n", "I_a", "I_s", "I_d", "E"]].sum(axis=1)
    history.plot(x="T", y="all_infectious")
    plt.show()


if __name__ == "__main__":
    plot_history("../tests/history.csv")
