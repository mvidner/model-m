import timeit
import time
import click
import random
import matplotlib.pyplot as plt
import numpy as np

from config_utils import ConfigFile
from graph_gen import GraphGenerator
from load_model import create_graph, matrix, load_model_from_config
from policy import bound_policy

from model_zoo import model_zoo


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


def demo(filename, test_id=None, model_random_seed=42, use_policy=None, print_interval=1):

    cf = ConfigFile()
    cf.load(filename)

    model, run_params = load_model_from_config(cf, model_random_seed=model_random_seed, use_policy=use_policy)

    model.run(**run_params)
    print("Avg. number of events per day: ", model.tidx/run_params["T"])

    storyfile = cf.section_as_dict("OUTPUT").get("story", None)
    if storyfile:
        story = tell_the_story(model.history, model.G)
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
    test_id = "_" + test_id if test_id else ""
    file_name = f"history{test_id}.csv"
    cf.save(file_name) 
    cfg_string = ""
    with open(file_name, "r") as f:
        cfg_string = "#" + "#".join(f.readlines()) 
    with open(file_name, "w") as f:
        f.write(cfg_string)
        f.write(f"# RANDOM_SEED = {model_random_seed}\n")
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
