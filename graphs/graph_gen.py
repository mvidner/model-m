# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import scipy.stats as stats


class GraphGenerator:
    layer_names = ['F', 'D', 'P', 'E', 'H', 'K',
                   'C', 'S', 'O', 'L', 'R', 'T', 'X', 'Z']
    layer_probs = [1.0] * len(layer_names)

    def __init__(self, random_seed=None):
        self.G = nx.MultiGraph()
        self.Graphs = {}
        self.G.graph['layer_names'] = self.layer_names
        self.G.graph['layer_probs'] = self.layer_probs

        if random_seed:
            np.random.seed(random_seed)

    def as_multigraph(self):
        return self.G

    def as_one_graph(self):
        return nx.Graph(self.G)

    def as_dict_of_graphs(self):
        self.Graphs = {}
        i = 0
        for l in self.layer_names:
            FG = nx.Graph()
            FG.graph['layer_name'] = l
            FG.graph['layer_prob'] = self.G.graph['layer_probs'][i]
            FG.add_nodes_from(self.G)
            selected_edges = [(u, v, e) for u, v, e in self.G.edges(
                data=True) if e['label'] == l]
            FG.add_edges_from(selected_edges)
            self.Graphs[l] = FG
            i = i + 1
        return self.Graphs

    def get_attr_list(self, attr):
        attr_list = []
        for (p, d) in self.G.nodes(data=True):
            attr_list.append(d[attr])
        return attr_list

    def modify_layers_for_node(self, node_id, what_by_what):
        """ changes edges' weights """

        if not what_by_what:
            return

        if not self.G.has_node(node_id):
            print(f"Warning: modify_layer_for_node called for nonexisting node_id {node_id}")
            return

        # for key in what_by_what:
        #     edges_to_modify = [
        #         (u, v, k) for u, v, k, d in self.G.edges(node, data=True, keys=True)
        #         if d['label'] == key
        #     ]
        #     print(edges_to_modify)
        #     for e in edges_to_modify:
        #         self.G.edges[e]['weight'] *= what_by_what[key]

        # for e in self.G.edges(node, data=True, keys=True):
        #     print(*e)

        for u, v, k, d in self.G.edges([node_id], data=True, keys=True):
            layer_label = d["label"]
            if layer_label in what_by_what:
                self.G.edges[(u, v, k)
                             ]['weight'] = max(self.G.edges[(u, v, k)]['weight'] * what_by_what[layer_label], 1.0)

        # for e in self.G.edges(node, data=True, keys=True):
        #     print(*e)


# returns dictionary of layer names and probabilities

    def get_layers_info(self):
        return dict(zip(self.G.graph["layer_names"], self.G.graph["layer_probs"]))

    def print_multi(self):
        dot_G = nx.nx_pydot.to_pydot(self.G)
        print(dot_G)

    def draw_multi(self, filename='empty_graph.png'):
        A = nx.nx_agraph.to_agraph(self.G)
        A.layout('dot')
        A.draw(filename)


def custom_exponential_graph(base_graph=None, scale=100, min_num_edges=0, m=9, n=None):
    """ Generate a random preferential attachment power law graph as a starting point.
    By the way this graph is constructed, it is expected to have 1 connected component.
    Every node is added along with m=8 edges, so the min degree is m=8.
    """
    if(base_graph):
        graph = base_graph.copy()
    else:
        assert(n is not None), "Argument n (number of nodes) must be provided when no base graph is given."
        graph = nx.barabasi_albert_graph(n=n, m=m)

# To get a graph with power-law-esque properties but without the fixed minimum degree,
# We modify the graph by probabilistically dropping some edges from each node.
    for node in graph:
        neighbors = list(graph[node].keys())
        quarantineEdgeNum = int(max(min(np.random.exponential(
            scale=scale, size=1), len(neighbors)), min_num_edges))
#        print(quarantineEdgeNum)
        quarantineKeepNeighbors = np.random.choice(
            neighbors, size=quarantineEdgeNum, replace=False)
        for neighbor in neighbors:
            if(neighbor not in quarantineKeepNeighbors):
                graph.remove_edge(node, neighbor)
    return graph


class RandomGraphGenerator(GraphGenerator):
    """ generating random graph aith mean degree 13 and num_nodes nodes
    both weights and layer weights are initialized randomly from trunc. norm (0.7, 0.3)
    """

    def __init__(self, num_nodes=10000, **kwargs):
        super().__init__(**kwargs)
        self.nodes = num_nodes

        i = 0
        for l in self.layer_names:
            # generate random connections
            baseGraph = nx.barabasi_albert_graph(n=num_nodes, m=9)
            FG = custom_exponential_graph(baseGraph, scale=100)
            # generate random weights from trunc norm
            lower, upper = 0, 1
            mu, sigma = 0.7, 0.3
            for (u, v, d) in FG.edges(data=True):
                FG[u][v]['weight'] = stats.truncnorm.rvs(
                    (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
                FG[u][v]['label'] = l
            # other params of the graph
            FG.graph['layer_name'] = l
            self.G.graph['layer_probs'][i] = stats.truncnorm.rvs(
                (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
            FG.graph['layer_prob'] = self.G.graph['layer_probs'][i]
            self.Graphs[l] = FG
            i = i + 1
#            dot = nx.nx_pydot.to_pydot(FG)
#            print(dot)

    def as_dict_of_graphs(self):
        return self.Graphs

    def as_multigraph(self):
        for l in self.layer_names:
            self.G.add_edges_from(self.Graphs[l].edges(data=True))
        return self.G
