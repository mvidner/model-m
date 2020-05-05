import pandas as pd
import numpy as np
import scipy as scipy
import scipy.integrate
import networkx as nx
import time
from operator import itemgetter

from history_utils import TimeSeries, TransitionHistory
from engine_sequential import SequentialEngine
# from extended_network_model import STATES as s
from sparse_utils import prop_of_row


def _searchsorted2d(a, b):
    m, n = a.shape
    max_num = np.maximum(a.max() - a.min(), b.max() - b.min()) + 1
    r = max_num * np.arange(a.shape[0])[:, None]
    p = np.searchsorted((a+r).ravel(), (b+r).ravel())
    return p - n*np.arange(m)


class EngineM(SequentialEngine):
    """ be the final one for model-m
        + operates on multigraph
        + iterates in days
    """

    def update_graph(self, new_G):
        """ create adjacency matrix for G """
        self.graph = new_G
        self.num_nodes = self.graph.num_nodes

    def node_degrees(self, Amat):
        raise NotImplementedError("We use the graph directly, not matrix.")

    def prob_of_contact(self, source_states, source_candidate_states, dest_states, dest_candidate_states, beta):

        assert type(dest_states) == list and type(source_states) == list

        # 1. select active edges
        # candidates for active edges are edges between source_candidate_states and dest_candidate_states
        # source (the one who is going to be infected)
        # dest (the one who can offer infection)

        source_candidate_flags = self.memberships[source_candidate_states, :, :].reshape(
            len(source_candidate_states), self.num_nodes).sum(axis=0)
        source_candidate_indices = source_candidate_flags.nonzero()[0]

        dest_candidate_flags = self.memberships[dest_candidate_states, :, :].reshape(
            len(dest_candidate_states), self.num_nodes).sum(axis=0)
        dest_candidate_indices = dest_candidate_flags.nonzero()[0]

        possibly_active_edges, possibly_active_edges_dirs = self.graph.get_edges(
            source_candidate_flags,
            dest_candidate_flags
        )
        num_possibly_active_edges = len(possibly_active_edges)

        if num_possibly_active_edges == 0:
            return np.zeros((self.num_nodes, 1))

        # for each possibly active edge flip coin
        r = np.random.rand(num_possibly_active_edges)
        # edges probs
        p = self.graph.get_edges_probs(possibly_active_edges)

        active_indices = list((r < p).nonzero()[0])
        num_active_edges = len(active_indices)
        if num_active_edges == 0:
            return np.zeros((self.num_nodes, 1))

        # select active edges
        if num_active_edges == 1:
            active_edges = [possibly_active_edges[active_indices[0]]]
            active_edges_dirs = [possibly_active_edges_dirs[active_indices[0]]]
        else:
            active_edges = list(itemgetter(*active_indices)
                                (possibly_active_edges))
            active_edges_dirs = list(itemgetter(
                *active_indices)(possibly_active_edges_dirs))

        # get source and dest nodes for active edges
        # source and dest met today, dest is possibly infectious, source was possibly infected
        source_nodes, dest_nodes = self.graph.get_edges_nodes(
            active_edges, active_edges_dirs)
        # add to contact_history (infectious node goes first!!!)
        contact_indices = list(zip(dest_nodes, source_nodes))
        self.contact_history.append(contact_indices)

        print("Potkali se u kolina:", contact_indices)

        # restrict the selection to only relevant states
        # (ie. candidates can be both E and I, relevant are only I)
        # candidates are those who will be possibly relevant in future
        dest_flags = self.memberships[dest_states, :, :].reshape(
            len(dest_states), self.num_nodes).sum(axis=0)
        source_flags = self.memberships[source_states, :, :].reshape(
            len(source_states), self.num_nodes).sum(axis=0)

        relevant_edges, relevant_edges_dirs = self.graph.get_edges(
            source_flags, dest_flags)

        # get intersection
        active_relevant_edges = list(set(active_edges) & set(relevant_edges))

        if len(active_relevant_edges) == 0:
            return np.zeros((self.num_nodes, 1))

        # always one index! (sources and dest must be disjunct)
        active_relevant_edges_dirs = [
            relevant_edges_dirs[relevant_edges.index(e)]
            for e in active_relevant_edges
        ]

        intensities = self.graph.get_edges_intensities(
            active_relevant_edges).reshape(-1, 1)
        relevant_sources, relevant_dests = self.graph.get_edges_nodes(
            active_relevant_edges, active_relevant_edges_dirs)

        #        assert len(relevant_sources) == len(set(relevant_sources))
        # TOD beta - b_ij
        # new beta depands on the one who is going to be infected
        b_intensitites = beta[relevant_sources]

        assert b_intensitites.shape == intensities.shape
        # print(b_intensitites.shape, intensities.shape,
        #      prob_of_no_infection.shape)
        relevant_sources_unique = np.unique(relevant_sources)
        relevant_sources = relevant_sources.reshape(-1, 1)

        A = scipy.sparse.csr_matrix(
            (np.ones(len(b_intensitites)),
             np.where((relevant_sources == relevant_sources_unique).T)
             )
        )
        assert A.shape[0] == len(
            relevant_sources_unique) and A.shape[1] == len(b_intensitites)

        prob_of_no_infection = scipy.sparse.csr_matrix(
            A.multiply(1 - b_intensitites * intensities)
        )

        prob_of_no_infection = prop_of_row(prob_of_no_infection)

        result = np.zeros(self.num_nodes)
        result[relevant_sources_unique] = 1 - prob_of_no_infection
        return result.reshape(self.num_nodes, 1)
