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
        self.edges_directions = {
            0: None
        }
        key = 1
        # working matrix
        tmpA = lil_matrix((self.num_nodes, self.num_nodes), dtype="uint32")

        forward_edge = True
        backward_edge = False

        # fill data and get indicies
        for i, row in enumerate(edges.itertuples()):
            self.e_types[i] = row.layer
            self.e_subtypes[i] = row.sublayer
            self.e_probs[i] = row.probability
            self.e_intensities[i] = row.intensity

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

            i_row, i_col = min(i_row, i_col), max(i_row, i_col)

            self.e_source[i] = i_row
            self.e_dest[i] = i_col

            if tmpA[i_row, i_col] == 0:
                # first edge between (row, col)
                self.edges_repo[key], self.edges_directions[key] = [
                    i], forward_edge
                self.edges_repo[key +
                                1], self.edges_directions[key+1] = [i], backward_edge
                tmpA[i_row, i_col] = key
                tmpA[i_col, i_row] = key + 1
                key += 2
            else:
                # add to existing edge list
                print("+", end="")
                key_forward = tmpA[i_row, i_col]
                key_backward = tmpA[i_col, i_row]
                self.edges_repo[key_forward].append(i)
                assert self.edges_directions[key_forward] == forward_edge
                # self.edges_directions[key_forward].append(forward_edge)
                self.edges_repo[key_backward].append(i)
                # self.edges_directions[key_backward].append(backward_edge)
                assert self.edges_directions[key_backward] == backward_edge

            if i % 1000 == 0:
                print("\nEdges loaded", i)

        # create matrix (A[i,j] is an index of edge (i,j) in array of edges)
        print("\nConverting lil_matrix A to csr ...", end="")
        self.A = csr_matrix(tmpA)
        print("level done")
        del tmpA

        print("Converting edges_repo to numpy array ...", end="")
        data = [None]
        subedges_counts = [0]
        for i_key in range(1, key):
            value_list = self.edges_repo[i_key]
            # if len(value_list) > 1:
            #     print(i_key)
            data.append(np.array(value_list, dtype="uint32"))
            subedges_counts.append(len(value_list))
        self.edges_repo = np.array(data, dtype=object)
        print("level done")

        print("Converting edges_directions to numpy bool array ... ", end="")
        data = [False]
        for i_key in range(1, key):
            data.append(self.edges_directions[i_key])
        self.edges_directions = np.array(data, dtype=bool)
        # uint16 is enough, should be numbers < 100 (todo: find the max number for hodonin)
        self.subedges_counts = np.array(subedges_counts, dtype="uint16")
        print("level done")

        print("Control check ... ", end="")
        for i_key in range(1, key):
            assert len(self.edges_repo[i_key]) == self.subedges_counts[i_key]
        print("ok")
        print("LightGraph is ready to use.")

    @property
    def number_of_nodes(self):
        return self.num_nodes

    def get_edges_nodes(self, edges, edges_dirs):
        """ returns source and dest nodes numbers (not ids)
        WARNING: NOT IDs
        """
        sources = self.e_source[edges]
        dests = self.e_dest[edges]
        # sources, dests numpy vectors on node_ids
        # edges_dirs - bool vector
        # if True take source if False take dest
        flags = edges_dirs
        source_nodes = sources * flags + dests * (1 - flags)
        dest_nodes = sources * (1 - flags) + dests * flags
        return source_nodes, dest_nodes

        #    def get_edges_subset(self, source_flags, dest_flags):
        #        active_subset = self.A[source_flags == 1, :][:, dest_flags == 1]
        #        edge_lists = [self.edges_repo[key] for key in active_subset.data]
        #        return subset, sum(edge_lists, [])

    def get_edges(self, source_flags, dest_flags, dirs=True):
        active_subset = self.A[source_flags == 1, :][:, dest_flags == 1]
        active_edges_indices = active_subset.data
        edge_lists = self.edges_repo[active_edges_indices]
        result = np.concatenate(edge_lists)
        if dirs:
            dirs_values = self.edges_directions[active_edges_indices]
            print(dirs_values)
            print(len(dirs_values), len(active_edges_indices))
            exit()
            edge_dirs = [[self.edges_directions[key]] * len(self.edges_repo[key])
                         for key in active_subset.data]
            return result, sum(edge_dirs, [])
        return result

    def get_edges_probs(self, edges):
        assert type(edges) == list
        # multiply by layer weight! TODO
        return self.e_probs[edges]

    def get_edges_intensities(self, edges):
        assert type(edges) == list
        return self.e_intensities[edges]
