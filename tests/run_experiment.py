import timeit
import click
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from config_utils import ConfigFile
from graph_gen import GraphGenerator

# from seirs_extended import ExtendedNetworkModel, custom_exponential_graph
from model_zoo import model_zoo
from seirs import custom_exponential_graph

verona_available = True
try:
    from romeo_juliet_graph_gen import RomeoAndJuliet as Verona
except ModuleNotFoundError:
    verona_available = False


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


def create_graph(name, num_nodes=None):

    if name == "romeo_and_juliet":
        if not verona_available:
            raise NotImplementedError(
                "Verona not available. Contact Roman Neruda for source files.")
        else:
            return Verona(random_seed=7)

    if name == "seirsplus_example":
        base_graph = nx.barabasi_albert_graph(n=num_nodes, m=9, seed=7)
        np.random.seed(42)
        return custom_exponential_graph(base_graph, scale=100)

    raise ValueError(f"Graph {name} not available.")


def tell_the_story(history, graph):

    story = ["Once upon a time ..."]

    states = {
        "S": "be healthy",  "S_s":  "have flue symptoms",
        "E": "be exposed", "I_n": "be infectious without symptoms",
        "I_a":  "be symptomatic and infectious with no  manifest of symptoms",
        "I_s": "manifest symptoms",
        "I_d": "be as famous as a taxidriver",
        "R_d": "be an expert on epidemy",
        "R_u":  "be healthy again",
        "D_d":  "push up daisies",
        "D_u":  "pine for the fjords"
    }

    if isinstance(graph, GraphGenerator):
        sexes = graph.get_attr_list("sex")
        names = graph.get_attr_list("label")
    else:
        sexes = None
        names = None

    for t in range(1, len(history)):
        node, src, dst = history[t]
        node, src, dst = node.decode(), src.decode(), dst.decode()

        if sexes:
            who = "A lady" if sexes[int(node)] else "A gentleman"
        else:
            who = "A node"

        if names:
            name = names[int(node)]
        else:
            name = node

        src_s, dst_s = states[src], states[dst]
        story.append(f"{who} {name} stopped to {src_s} and started to {dst_s}.")

    story.append(
        "Well! I never wanted to do this in the first place. I wanted to be... an epidemiologist!")

    return "\n".join(story)


def matrix(graph):
    if isinstance(graph, GraphGenerator):
        return magic_formula(
            graph.as_dict_of_graphs(),
            graph.get_layers_info()
        )
    else:
        return None


def demo(filename, test_id=None, model_random_seed=42, print_interval=1):

    cf = ConfigFile()
    cf.load(filename)

    num_nodes = cf.section_as_dict("TASK").get("num_nodes", None)
    model_params = cf.section_as_dict("MODEL")

    graph_name = cf.section_as_dict("GRAPH")["name"]

    graph = create_graph(graph_name, num_nodes)
    print(graph)

    A = matrix(graph)

    class_name = cf.section_as_dict("TASK").get(
        "model", "ExtendedNetworkModel")
    Model = model_zoo[class_name]
    model = Model(G=graph if A is None else A,
                  **model_params,
                  random_seed=model_random_seed)

    policy_cfg = cf.section_as_dict("POLICY")
    if policy_cfg and policy_cfg.get("filename", None):
        Policy = getattr(__import__(
            policy_cfg["filename"]), "Policy")
        policy = Policy(graph)

        model.set_periodic_update(policy.get_policy_function())

    print(model.__class__.__name__)
    print(model)

    ndays = cf.section_as_dict("TASK").get("duration_in_days", 60)
    print_interval = cf.section_as_dict("TASK").get("print_interval", 1)
    verbose = cf.section_as_dict("TASK").get("verbose", "Yes") == "Yes"

    model.run(T=ndays, verbose=verbose, print_interval=print_interval)
    print("Avg. number of events per day: ", model.tidx/ndays)

    storyfile = cf.section_as_dict("OUTPUT").get("story", None)
    if storyfile:
        story = tell_the_story(model.history, graph)
        with open(storyfile, "w") as f:
            f.write(story)

    plot = True
    if plot:
        counts = [model.state_counts[s].asarray()
                  for s in ("I_n", "I_a", "I_s", "I_d", "E")]
        y = np.sum(counts, axis=0)
        x = model.tseries.asarray()
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

    random_seed = 42 if set_random_seed else random.randint(0, 10000)
    def demo_fce(): return demo(filename, test_id,
                                model_random_seed=random_seed, print_interval=print_interval)
    print(timeit.timeit(demo_fce, number=1))


if __name__ == "__main__":
    test()
