import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, lil_matrix

# novej light graph


class LightGraph:

    def __init__(self, random_seed=None):
        if random_seed:
            np.random.seed(random_seed)
        self.edge_repo = None
        self.A = None

    def read_csv(self,
                 path_to_nodes='p.csv',
                 path_to_external='e.csv',
                 path_to_layers='etypes.csv',
                 path_to_edges='edges.csv'):

        csv_hacking = {'na_values': 'undef', 'skipinitialspace': True}
        nodes = pd.read_csv(path_to_nodes, **csv_hacking)
        edges = pd.read_csv(path_to_edges, **csv_hacking)
        layers = pd.read_csv(path_to_layers, **csv_hacking)
        external_nodes = pd.read_csv("../data/newtown/e.csv", **csv_hacking)

        # layer names, ids and weights go to graph
        layers_to_add = layers.to_dict('list')

        self.layer_ids = layers_to_add['id']
        self.layer_name = layers_to_add['name']
        self.layer_weights = layers_to_add['weight']

        # nodes
        # select categorical columns
        cat_columns = nodes.select_dtypes(['object']).columns
        nodes[cat_columns] = nodes[cat_columns].apply(
            lambda x: x.astype('category'))

        # save codes for backward conversion
        self.cat_table = {
            col: list(nodes[col].cat.categories)
            for col in cat_columns
        }

        # covert categorical to numbers
        nodes[cat_columns] = nodes[cat_columns].apply(
            lambda x: x.cat.codes)
        # pprint(nodes)

        # just test of conversion back
        # print(cat_columns)
        # for col in list(cat_columns):
        #     nodes[[col]] = nodes[[col]].apply(
        #         lambda x: pd.Categorical.from_codes(
        #             x, categories=cat_table[col])
        #     )
        # pprint(nodes)

        for col in nodes.columns:
            setattr(self, "nodes_"+col, np.array(nodes[col]))

        self.nodes = np.array(nodes.index)
        self.num_nodes = len(self.nodes)

        self.ignored = set(external_nodes["id"])

        # edges
        # drop self edges
        indexNames = edges[edges['vertex1'] == edges['vertex2']].index
        if len(indexNames):
            print("Warning: dropping self edges!!!!")
            edges.drop(indexNames, inplace=True)

        # fill edges to a graph
        n_edges = len(edges)
        # edges data"
        self.e_types = np.empty(n_edges, dtype="uint16")
        self.e_subtypes = np.empty(n_edges, dtype="uint16")
        self.e_probs = np.empty(n_edges)
        self.e_intensities = np.empty(n_edges)
        self.e_source = np.empty(n_edges, dtype="uint32")
        self.e_dest = np.empty(n_edges, dtype="uint32")
        # edges repo
        self.edges_repo = {
            0: None
        }
        key = 1
        # working matrix
        tmpA = lil_matrix((self.num_nodes, self.num_nodes), dtype=int)

        forward_edge = (self.e_source, self.e_dest)
        backward_edge = (self.e_dest, self.e_source)

        # fill data and get indicies
        for i, row in enumerate(edges.itertuples()):
            self.e_types[i] = row.layer
            self.e_subtypes[i] = row.sublayer
            self.e_probs[i] = row.probability
            self.e_intensities[i] = row.intensity
            self.e_source[i] = row.vertex1
            self.e_dest[i] = row.vertex2

            if row.vertex1 in self.ignored or row.vertex2 in self.ignored:
                continue

            try:
                i_row = np.where(self.nodes_id == row.vertex1)[0][0]
                i_col = np.where(self.nodes_id == row.vertex2)[0][0]
            except IndexError:
                print("Node does not exist")
                print(row.vertex1, row.vertex2)
                print(np.where(self.nodes_id == row.vertex1),
                      np.where(self.nodes_id == row.vertex2))
                exit()

            if tmpA[i_row, i_col] == 0:
                # first edge between (row, col)
                self.edges_repo[key] = [(i, forward_edge)]
                self.edges_repo[key+1] = [(i, backward_edge)]
                tmpA[i_row, i_col] = key
                tmpA[i_col, i_row] = key + 1
                key += 2
            else:
                # add to existing edge list
                key_forward = tmpA[i_row, i_col]
                key_backward = tmpA[i_col, i_row]
                self.edges_repo[key_forward].append((i, forward_edge))
                self.edges_repo[key_backward].append((i, backward_edge))

            if i % 1000 == 0:
                print("Edges loaded", i)

        # create matrix (A[i,j] is an index of edge (i,j) in array of edges)
        print("Converting to csr ...", end="")
        self.A = csr_matrix(tmpA)
        print("level done")
        del tmpA

    @property
    def number_of_nodes(self):
        return self.num_nodes

    def get_edges_subset(self, source_flags, dest_flags):
        subset = self.A[source_flags == 1, :][:, dest_flags == 1]
        active_subset = self.A[source_flags == 1, :][:, dest_flags == 1]
        edge_lists = [self.edges_repo[key] for key in active_subset.data]
        return subset, sum(edge_lists, [])

    def get_edges(self, source_flags, dest_flags):
        active_subset = self.A[source_flags == 1, :][:, dest_flags == 1]
        edge_lists = [self.edges_repo[key] for key in active_subset.data]
        return sum(edge_lists, [])

    def get_edges_probs(self, edges):
        assert type(edges) == list
        return self.e_probs[edges]
