import timeit
from seirs_extended import ExtendedNetworkModel, custom_exponential_graph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from romeo_juliet_graph_gen import RomeoAndJuliet as Verona


def magic_formula(gdict, wdict):

    g = next(iter(gdict.values()))
    a_shape = nx.adj_matrix(g).shape
    ones = np.ones(shape=a_shape)

    prob_no_contact = ones
    for name, g in gdict.items():
        a = nx.adj_matrix(g)
        a = wdict[name] * a
        prob_no_contact = np.multiply(prob_no_contact, (ones-a))

    # probability of contact (whatever layer)
    return 1 - prob_no_contact


def demo():

    verona = Verona(random_seed=7)
    numNodes = verona.G.number_of_nodes()
    print("N = ", numNodes)

    A = magic_formula(
        verona.as_dict_of_graphs(),
        dict(zip(verona.G.graph["layer_names"], verona.G.graph["layer_probs"]))
    )

    model = ExtendedNetworkModel(G=A,
                                 beta=0.155,
                                 sigma=1/5.2,
                                 gamma=1/12.39,
                                 mu_I=0.0004,
                                 p=0.2,
                                 beta_D=0.155,
                                 gamma_D=1/12.39,
                                 mu_D=0.0004,
                                 theta_E=0.1,
                                 theta_Ia=0.1,
                                 theta_Is=0.1,
                                 phi_E=0,
                                 phi_Ia=0,
                                 phi_Is=0,
                                 psi_E=1.0,
                                 psi_Ia=1.0,
                                 psi_Is=1.0,
                                 q=0.1,
                                 false_symptoms_rate=0.2,
                                 asymptomatic_rate=0.3,
                                 symptoms_manifest_rate=0.9,
                                 initSSrate=0.2,
                                 initE=0,
                                 initI_n=2,
                                 initI_a=1,
                                 initI_s=4,
                                 initI_d=0,
                                 random_seed=42)

    ndays = 60
    model.run(T=ndays, verbose=True, print_interval=1)
    print("Avg. number of events per day: ", model.tidx/ndays)


def test():
    # demo_fce = lambda: demo(n_nodes)
    # print(timeit.timeit(demo_fce, number=1))
    demo()


if __name__ == "__main__":
    test()
