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
def main(filename, outputname):
    """ Load the graph and pickle. """

    cf = ConfigFile()
    cf.load(filename)

    graph = _load_graph(cf)
    with open(outputname, 'wb') as f:
        pickle.dump(graph, f)


if __name__ == "__main__":
    main()
