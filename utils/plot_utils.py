# vzkaz pro Gabinu: smaz tu a prepis tu cokoli budes chtit

import pandas as pd

def plot_history(filename):

    history = pd.read_csv(filename)
    print(history)
    
    # counts = [model.state_counts[s].asarray()
    #           for s in ("I_n", "I_a", "I_s", "I_d", "E")]
    y = np.sum(counts, axis=0)
    x = model.tseries.asarray()
    plt.plot(x, y)
    test_id = "_" + test_id if test_id else ""
    plt.savefig(f"num_of_ill{test_id}.png")


if __name__ == "__main__":
    plot_history("../tests/history.csv")
