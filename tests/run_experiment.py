import timeit
import time
import click
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

from config_utils import ConfigFile
from sparse_utils import multiply_zeros_as_ones
from graph_gen import GraphGenerator, CSVGraphGenerator, RandomSingleGraphGenerator, RandomGraphGenerator
from csv_graph import CSVGraph
from light_graph import LightGraph
from policy import bound_policy

# from seirs_extended import ExtendedNetworkModel, custom_exponential_graph
from model_zoo import model_zoo
from seirs import custom_exponential_graph


verona_available = True
try:
    from romeo_juliet_graph_gen import RomeoAndJuliet as Verona
except ModuleNotFoundError:
    verona_available = False


def magic_formula(graph):

    # rozvrtany ... nutno opravit

    N = graph.number_of_nodes()

    #    print(graph.get_layers_info())

    prob_no_contact = csr_matrix((N, N))  # empty values = 1.0

    for name, prob in graph.get_layers_info().items():
        a = nx.adj_matrix(graph.get_graph_for_layer(name))
        if len(a.data) == 0:
            continue
        a = a.multiply(prob)  # contact on layer
        not_a = a  # empty values = 1.0
        not_a.data = 1.0 - not_a.data
        prob_no_contact = multiply_zeros_as_ones(prob_no_contact, not_a)
        del a

    # probability of contact (whatever layer)
    prob_of_contact = prob_no_contact
    prob_of_contact.data = 1.0 - prob_no_contact.data
    return prob_of_contact


def create_graph(name, nodes="nodes.csv", edges="edges.csv", layers="etypes.csv", num_nodes=None):

    if name == "romeo_and_juliet":
        if not verona_available:
            raise NotImplementedError(
                "Verona not available. Contact Roman Neruda for source files.")
        else:
            return Verona(random_seed=7)

    if name == "csv":
        return CSVGraphGenerator(path_to_nodes=nodes, path_to_edges=edges, path_to_layers=layers)

    if name == "csv_petra":
        return CSVGraph(path_to_nodes=nodes, path_to_edges=edges, path_to_layers=layers)

    if name == "csv_light":
        return LightGraph(path_to_nodes=nodes, path_to_edges=edges, path_to_layers=layers)

    if name == "seirsplus_example":
        base_graph = nx.barabasi_albert_graph(n=num_nodes, m=9, seed=7)
        np.random.seed(42)
        return custom_exponential_graph(base_graph, scale=100)

    if name == "random":
        return RandomGraphGenerator()

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

        src_s, dst_s = states.get(src, src), states.get(dst, dst)
        story.append(f"{who} {name} stopped to {src_s} and started to {dst_s}.")

    story.append(
        "Well! I never wanted to do this in the first place. I wanted to be... an epidemiologist!")

    return "\n".join(story)


def matrix(graph, cf):

    if cf:
        scenario = cf.section_as_dict("SCENARIO")
    else:
        scenario = False 

    if isinstance(graph, CSVGraph):
        if scenario:
            raise NotImplementedError(
                "CSVGraph does not support closing layers yet.")
        return graph.G

    if isinstance(graph, LightGraph):
        if scenario:
            raise NotImplementedError(
                "LightGraph does not support closing layers yet.")
        return graph.A

    if isinstance(graph, RandomSingleGraphGenerator):
        if scenario:
            raise NotImplementedError(
                "RandomGraphGenerator does not support closing layers.")
        return graph.G

    if isinstance(graph, GraphGenerator):
        if scenario:
            list_of_closed_layers = scenario["closed"]
            graph.close_layers(list_of_closed_layers)
        return magic_formula(
            graph
        )
    else:
        return None


def demo(filename, test_id=None, model_random_seed=42, use_policy=None, print_interval=1):

    cf = ConfigFile()
    cf.load(filename)

    num_nodes = cf.section_as_dict("TASK").get("num_nodes", None)
    model_params = cf.section_as_dict("MODEL")

    graph_name = cf.section_as_dict("GRAPH")["name"]
    nodes = cf.section_as_dict("GRAPH").get("nodes", "nodes.csv")
    edges = cf.section_as_dict("GRAPH").get("edges", "edges.csv")
    layers = cf.section_as_dict("GRAPH").get("layers", "etypes.csv")

    start = time.time()
    graph = create_graph(graph_name, nodes=nodes, edges=edges,
                         layers=layers, num_nodes=num_nodes)

    A = matrix(graph, cf)
    end = time.time()
    print("Graph loading: ", end-start, "seconds")

    #    print(graph)

    class_name = cf.section_as_dict("TASK").get(
        "model", "ExtendedNetworkModel")
    Model = model_zoo[class_name]
    model = Model(G=graph if A is None else A,
                  **model_params,
                  random_seed=model_random_seed)

    if use_policy:  # TODO: cfg versus --policy option
        policy_cfg = cf.section_as_dict("POLICY")
        if use_policy not in policy_cfg["name"]:
            raise ValueError("Unknown policy name.")

        if policy_cfg and "filename" in policy_cfg:
            policy = getattr(__import__(
                policy_cfg["filename"]), use_policy)
            policy = bound_policy(policy, graph)
            model.set_periodic_update(policy)
        else:
            print("Warning: NO POLICY IN CFG")
            print(policy_cfg)

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

    plot = False
    if plot:
        counts = [model.state_counts[s].asarray()
                  for s in ("I_n", "I_a", "I_s", "I_d", "E")]
        y = np.sum(counts, axis=0)
        x = model.tseries.asarray()
        plt.plot(x, y)
        test_id = "_" + test_id if test_id else ""
        plt.savefig(f"num_of_ill{test_id}.png")

    # save history
    cf.save("tmpxxxx.tmp")
    with open("tmpxxxx.tmp") as f:
        config_string = "#".join(f.readlines())
    test_id = "_" + test_id if test_id else ""
    with open(f"history{test_id}.csv", "w") as f:
        f.write(f"# RANDOM_SEED = {model_random_seed}\n")
        f.write("#"+config_string)
        model.save(f)

    save_nodes = cf.section_as_dict("TASK").get("save_node_states", "No") == "Yes"
    if save_nodes:
        model.save_node_states(f"node_states{test_id}.csv")


@click.command()
@click.option('--set-random-seed/--no-random-seed', ' /-r', default=True)
@click.option('--policy', '-p', default=None)
@click.option('--print_interval',  default=1)
@click.argument('filename', default="example.ini")
@click.argument('test_id', default="")
def test(set_random_seed, policy, print_interval, filename, test_id):
    """ Run the demo test inside the timeit """

    random_seed = 42 if set_random_seed else random.randint(0, 10000)
    def demo_fce(): return demo(filename, test_id,
                                model_random_seed=random_seed, use_policy=policy, print_interval=print_interval)
    print(timeit.timeit(demo_fce, number=1))


if __name__ == "__main__":
    test()
