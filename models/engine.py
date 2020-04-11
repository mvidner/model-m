import numpy as np
import scipy as scipy
import scipy.integrate
import networkx as nx

from history_utils import TimeSeries, TransitionHistory


class BaseEngine():

    def inicialization(self):
        """ model inicialization """
        if self.random_seed:
            np.random.seed(self.random_seed)

        # setup adjacency matrix
        self.update_graph(self.G)

        # create arrays for model params
        for param_name in self.model_parameters:
            param = self.__getattribute__(param_name)
            if isinstance(param, (list, np.ndarray)):
                setattr(self, param_name,
                        np.array(param).reshape((self.num_nodes, 1)))
            else:
                setattr(self, param_name,
                        np.full(fill_value=param, shape=(self.num_nodes, 1)))

    def setup_series_and_time_keeping(self):
        pass

    def states_and_counts_init(self, state_counts):
        pass

    def update_graph(self, new_G):
        """ create adjacency matrix for G """
        self.G = new_G
        if self.A:
            del self.A

        if isinstance(new_G, np.ndarray):
            self.A = scipy.sparse.csr_matrix(new_G)
        elif type(new_G) == nx.classes.graph.Graph:
            # adj_matrix gives scipy.sparse csr_matrix
            self.A = nx.adj_matrix(new_G)
        else:
            raise TypeError(
                "Input an adjacency matrix or networkx object only.")

        self.num_nodes = self.A.shape[1]
        self.degree = np.asarray(self.node_degrees(self.A)).astype(float)

        # if TF_ENABLED:
        #     self.A = to_sparse_tensor(self.A)

    def node_degrees(self, Amat):
        """ return number of degrees of  nodes,
        i.e. sums of adj matrix cols """
        # TODO FIX ME
        return Amat.sum(axis=0).reshape(self.num_nodes, 1)

    def set_periodic_update(self, callback):
        """ set callback function
        callback function is called every midnigh """
        self.periodic_update_callback = callback

    # TODO: need this???

    def update_scenario_flags(self):
        pass

    def num_contacts(self, state):
        """ return numbers of contacts from given state
        if state is a list, it is sum over all states """

        if type(state) == str:
            # if TF_ENABLED:
            #     with tf.device('/GPU:' + "0"):
            #         x = tf.Variable(self.X == state, dtype="float32")
            #         return tf.sparse.sparse_dense_matmul(self.A, x)
            # else:
            return np.asarray(
                scipy.sparse.csr_matrix.dot(self.A, self.X == state))

        elif type(state) == list:
            state_flags = np.hstack(
                [np.array(self.X == s, dtype=int) for s in state]
            )
            # if TF_ENABLED:
            #     with tf.device('/GPU:' + "0"):
            #         x = tf.Variable(state_flags, dtype="float32")
            #         nums = tf.sparse.sparse_dense_matmul(self.A, x)
            # else:

            nums = scipy.sparse.csr_matrix.dot(self.A, state_flags)
            return np.sum(nums, axis=1).reshape((self.num_nodes, 1))
        else:
            raise TypeException(
                "num_contacts(state) accepts str or list of strings")

    def current_state_count(self, state):
        return self.state_counts[state][self.tidx]

    def current_N(self):
        return self.N[self.tidx]

    def increase_data_series_length(self):
        pass

    def finalize_data_series(self):
        pass

    def run_iteration(self):
        pass

    def run(self, T, print_interval=10, verbose=False):
        pass
