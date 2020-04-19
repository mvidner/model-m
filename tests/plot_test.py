from plot_utils import plot_histories, plot_mutliple_policies, plot_state_histogram, plot_history
import matplotlib.pyplot as plt


# policy_dict = {
#     "low": ["history_low.csv"],
#     "high": ["history_high.csv"],
# }

# save_path = "village0" + "low_test_rate" + "Id" + '.png'


# plot_mutliple_policies(policy_dict, group_days=2,
#                        group_func="max", save_path=save_path, column="I_d")
# exit()

# import sys

# plot_history(sys.argv[1], savepath=sys.argv[1]+".png")
# exit()


BASEDIR = "/home/petra/covid/model-m-result-storage/hodonin_18_04"
CITY = "town0"

files_daily = [
    f"{BASEDIR}/history_town0_daily_{i}.csv"
    for i in range(10)
]

files_seq = [
    f"{BASEDIR}/history_town0_seq_{i}.csv"
    for i in range(10)
]

files_old = [
    f"{BASEDIR}/history_town0_orig_{i}.csv"
    for i in range(10)
]


policy_dict = {
    "orig_alg":  files_old,
    "daily_alg": files_daily,
    "seq_alg": files_seq
}


save_path = 'alg_compare.png'

plt.rcParams["figure.figsize"] = (20, 15)
plot_mutliple_policies(policy_dict, group_days=2,
                       group_func="max", save_path=save_path)

exit()

files_no_policy = [
    f"{BASEDIR}/{CITY}/test_rate/historytown0__low_test_rate_{i}.csv"
    for i in range(10)
]

files_strong_policy = [
    f"{BASEDIR}/{CITY}/test_rate/historytown0_strong_policy_low_test_rate_{i}.csv"
    for i in range(10)
]

files_weighted_policy = [
    f"{BASEDIR}/{CITY}/test_rate/historytown0_weighted_policy_low_test_rate_{i}.csv"
    for i in range(10)
]


policy_dict = {
    "no_policy": files_no_policy,
    "weighted_policy": files_weighted_policy,
    "strong_policy": files_strong_policy
}

save_path = CITY + "low_test_rate" + "Id" + '.png'

plt.rcParams["figure.figsize"] = (20, 15)
plot_mutliple_policies(policy_dict, group_days=2,
                       group_func="max", save_path=save_path, column="I_d")
