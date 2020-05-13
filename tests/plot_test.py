from plot_utils import plot_histories, plot_mutliple_policies, plot_state_histogram, plot_history
import matplotlib.pyplot as plt
import sys


# import sys

# plot_history(sys.argv[1])
# exit()


BASEDIR = "."
CITY = "town0"

filename = sys.argv[1]
variants_list = sys.argv[2:]

variant_dict = {}

for variant in variants_list:
    variant_dict[variant] = [
        f"{BASEDIR}/history_{variant}_{i}.csv"
        for i in range(0, 30)
    ]

#variant_dict["gold"] = [ "../data/litovel_plot.csv" ]

plt.rcParams["figure.figsize"] = (20, 15)
plot_mutliple_policies(variant_dict, group_days=None, 
                       group_func="max",  save_path=f"{filename}_all_ill.png", max_days=55)

#plot_mutliple_policies(variant_dict, group_days=None,
#                       group_func="max", value="I_d", save_path=f"{filename}_Id.png")
