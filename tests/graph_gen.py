# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np


class GraphGenerator:
    edge_names = ['F', 'D', 'P', 'E', 'H', 'K',
                  'C', 'S', 'O', 'L', 'R', 'T', 'X', 'Z']
    edge_probs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def __init__(self, random_seed=None):
        self.G = nx.MultiGraph()
        self.G.graph['edge_names'] = self.edge_names
        self.G.graph['edge_probs'] = self.edge_probs

        if random_seed:
            np.random.seed(random_seed)

    def as_multigraph(self):
        return self.G

    def as_one_graph(self):
        return nx.Graph(self.G)

    def as_dict_of_graphs(self):
        Graphs = {}
        i = 0
        for l in self.edge_names:
            FG = nx.Graph()
            FG.graph['edge_name'] = l
            FG.graph['edge_prob'] = self.G.graph['edge_probs'][i]
            FG.add_nodes_from(self.G)
            selected_edges = [(u, v, e) for u, v, e in self.G.edges(
                data=True) if e['label'] == l]
            FG.add_edges_from(selected_edges)
            Graphs[l] = FG
            i = i + 1
        return Graphs

    def print_multi(self):
        dot_G = nx.nx_pydot.to_pydot(self.G)
        print(dot_G)

    def draw_multi(self, filename='raj.png'):
        A = nx.nx_agraph.to_agraph(self.G)
        A.layout('dot')
        A.draw(filename)
