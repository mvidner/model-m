import timeit
import click
import random
from seirs_extended import ExtendedNetworkModel, custom_exponential_graph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from config_utils import ConfigFile

def demo(filename, test_id=None, model_random_seed=42, print_interval=1):

    cf = ConfigFile()
    cf.load(filename)

    num_nodes = cf.section_as_dict("TASK")["num_nodes"]
    model_params = cf.section_as_dict("MODEL")

    print(model_params)
    
    base_graph = nx.barabasi_albert_graph(n=num_nodes, m=9, seed=7)
    np.random.seed(42)
    G_normal = custom_exponential_graph(base_graph, scale=100)

    model = ExtendedNetworkModel(G=G_normal,
                                 **model_params,
                                 random_seed=model_random_seed)

    ndays =  cf.section_as_dict("TASK")["duration_in_days"]
    print_interval = cf.section_as_dict("TASK")["print_interval"]
    
    model.run(T=ndays, verbose=True, print_interval=print_interval)
    print("Avg. number of events per day: ", model.tidx/ndays)

    plot = True
    if plot:
        counts = [model.state_counts[s]
                  for s in ("I_n", "I_a", "I_s", "I_d", "E")]
        y = np.sum(counts, axis=0)
        x = model.tseries
        plt.plot(x, y)
        test_id = "_" + test_id if test_id else ""
        plt.savefig(f"num_of_ill{test_id}.png")



@click.command()
@click.option('--set-random-seed/--no-random-seed', ' /-r', default=True)
@click.option('--print_interval',  default=1)
@click.argument('filename', default="example.ini")
@click.argument('test_id', default="")
def test(set_random_seed, print_interval, filename, test_id):
    """ Run the demo test inside the timeit """
    
    random_seed = 42 if set_random_seed else random.randint(0,10000)
    demo_fce = lambda: demo(filename, test_id, model_random_seed=random_seed, print_interval=print_interval)
    print(timeit.timeit(demo_fce, number=1))
    
    


if __name__ == "__main__":
    test()
