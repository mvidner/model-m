import timeit
import time
import click
import random
import pickle
from config_utils import ConfigFile
from model_m import _load_graph


@click.command()
@click.argument('filename', default="example.ini")
@click.argument('outputname', default="graph.pickle")
@click.option('--precalc_matrix/--no_matrix', default=False)
def main(filename, outputname, precalc_matrix):
    """ Load the graph and pickle. """

    cf = ConfigFile()
    cf.load(filename)

    graph = _load_graph(cf)
    if precalc_matrix:
        graph.final_adjacency_matrix()

    with open(outputname, 'wb') as f:
        pickle.dump(graph, f)


if __name__ == "__main__":
    main()
