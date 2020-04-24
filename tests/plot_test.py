from plot_utils import plot_histories, plot_mutliple_policies, plot_state_histogram, plot_history
import matplotlib.pyplot as plt
import sys 


# import sys

# plot_history(sys.argv[1], savepath=sys.argv[1]+".png")
# exit()


BASEDIR = "."
CITY = "town0"

filename = sys.argv[1]
variants_list = sys.argv[2:] 

variant_dict = {}

for variant in variants_list:
    variant_dict[variant] = [
        f"{BASEDIR}/history_{variant}_{i}.csv"
        for i in range(100)
    ]


plt.rcParams["figure.figsize"] = (20, 15)
plot_mutliple_policies(variant_dict, group_days=2,
                       group_func="max", save_path=filename)


