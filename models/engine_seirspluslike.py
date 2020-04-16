import pandas as pd
import numpy as np
import scipy as scipy
import scipy.integrate
import networkx as nx
import time

from history_utils import TimeSeries, TransitionHistoryInt
from engine import BaseEngine


class SeirsPlusLikeEngine(BaseEngine):

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

        self.num_transitions = 100  # TO: change to our situation
        tseries_len = (self.num_transitions + 1) * self.num_nodes

        self.tseries = TimeSeries(tseries_len, dtype=float)

        self.history = TransitionHistoryInt(tseries_len)

        # state_counts ... numbers of inidividuals in given states
        self.state_counts = {
            state: TimeSeries(tseries_len, dtype=int)
            for state in self.states
        }

        # N ... actual number of individuals in population
        self.N = TimeSeries(tseries_len, dtype=float)

        # float time
        self.t = 0
        self.tmax = 0  # will be set when run() is called
        self.tidx = 0  # time index to time series
        self.tseries[0] = 0

    def states_and_counts_init(self, state_counts):
        """ Initialize Counts of inidividuals with each state """

        for state, init_value in state_counts.items():
            self.state_counts[state][0] = init_value

        nodes_left = self.num_nodes - sum(
            [self.state_counts[s][0] for s in self.states]
        )

        self.state_counts[self.states[0]][0] += nodes_left

        # invisible nodes does not count to population (death ones)
        self.N[0] = self.num_nodes - sum(
            [self.state_counts[s][0] for s in self.invisible_states]
        )

        # X ... array of states
        tempX = []
        for state, count in self.state_counts.items():
            tempX.extend([state]*count[0])
        self.X = np.array(tempX).reshape((self.num_nodes, 1))
        # distribute the states randomly
        np.random.shuffle(self.X)

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
        testing_infected = np.any(self.theta_Ia) or np.any(
            self.theta_Is) or np.any(self.phi_Ia) or np.any(self.phi_Is)
        positive_test_for_I = np.any(self.psi_Ia) or np.any(self.psi_Is)

        testing_exposed = np.any(self.theta_E) or np.any(self.phi_E)
        positive_test_for_E = np.any(self.psi_E)

        self.testing_scenario = (
            (positive_test_for_I and testing_infected) or
            (positive_test_for_E and testing_exposed)
        )

        tracing_E = np.any(self.phi_E)
        tracing_I = np.any(self.phi_Ia) or np.any(self.phi_Is)
        self.tracing_scenario = (
            (positive_test_for_E and tracing_E) or
            (positive_test_for_I and tracing_I)
        )

    def num_contacts(self, state):
        """ return numbers of contacts from given state
        if state is a list, it is sum over all states """

        if type(state) == int:
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

        self.tseries.bloat()
        self.history.bloat()
        for state in self.states:
            self.state_counts[state].bloat()
        self.N.bloat()

    def finalize_data_series(self):

        self.tseries.finalize(self.tidx)
        self.history.finalize(self.tidx)
        for state in self.states:
            self.state_counts[state].finalize(self.tidx)
        self.N.finalize(self.tidx)

    def save(self, file_or_filename):
        index = self.tseries
        columns = self.state_counts
        columns["day"] = np.floor(index).astype(int)
        df = pd.DataFrame(self.state_counts, index=self.tseries)
        df.index.rename('T', inplace=True)
        df.columns = [self.state_str_dict[x] for x in self.states] + ["day"]
        df.to_csv(file_or_filename)
        print(df)

    def run_iteration(self):

        if (self.tidx >= self.tseries.len()-1):
            # Room has run out in the timeseries storage arrays; double the size of these arrays
            self.increase_data_series_length()

        # 1. Generate 2 random numbers uniformly distributed in (0,1)
        r1 = np.random.rand()
        r2 = np.random.rand()

        # 2. Calculate propensities
        propensities, transition_types = self.calc_propensities()

        # Terminate when probability of all events is 0:
        if propensities.sum() <= 0.0:
            self.finalize_data_series()
            return False

        # 3. Calculate alpha
        propensities_flat = propensities.ravel(order='F')
        cumsum = propensities_flat.cumsum()
        alpha = propensities_flat.sum()

        # 4. Compute the time until the next event takes place
        tau = (1/alpha)*np.log(float(1/r1))
        self.t += tau

        # 5. Compute which event takes place
        transition_idx = np.searchsorted(cumsum, r2*alpha)
        transition_node = transition_idx % self.num_nodes
        transition_type = transition_types[int(transition_idx/self.num_nodes)]

        # 6. Update node states and data series
        assert(self.X[transition_node] == transition_type[0] and self.X[transition_node] not in self.final_states), "Assertion error: Node " + \
            str(transition_node)+" has unexpected current state " + \
            str(self.X[transition_node]) + \
            " given the intended transition of "+str(transition_type)+"."

        self.X[transition_node] = transition_type[1]

        self.tidx += 1
        self.tseries[self.tidx] = self.t
        self.history[self.tidx] = (transition_node, *transition_type)

        for state in self.states:
            self.state_counts[state][self.tidx] = self.state_counts[state][self.tidx-1]
        self.state_counts[transition_type[0]][self.tidx] -= 1
        self.state_counts[transition_type[1]][self.tidx] += 1

        self.N[self.tidx] = self.N[self.tidx-1]
        # if node died
        if transition_type[1] in (self.invisible_states):
            self.N[self.tidx] = self.N[self.tidx-1] - 1

        # Terminate if tmax reached or num infectious and num exposed is 0:
        numI = sum([self.current_state_count(s)
                    for s in self.unstable_states
                    ])

        if self.t >= self.tmax or numI < 1:
            self.finalize_data_series()
            return False

        return True

    def run(self, T, print_interval=10, verbose=False):

        if not T > 0:
            return False

        self.tmax += T

        running = True
        day = -1
        start = time.time()

        while running:

            running = self.run_iteration()

            # true after the first event after midnight
            day_changed = day != int(self.t)
            day = int(self.t)
            if day_changed:
                end = time.time()
                print("Last day took: ", end - start, "seconds")
                start = time.time()

            # run periodical update
            if self.periodic_update_callback and day != 0 and day_changed:
                print(self.periodic_update_callback)
                changes = self.periodic_update_callback(
                    self.X, self.history, self.tseries[:self.tidx+1], self.t)

                if "graph" in changes:
                    print("CHANGING GRAPH")
                    self.update_graph(changes["graph"])

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # print only if print_interval is set
            # prints always at the beginning of a new day
            if print_interval or not running:
                if day_changed:
                    day = int(self.t)

                if not running or (day_changed and (day % print_interval == 0)):
                    print("t = %.2f" % self.t)
                    if verbose or not running:
                        for state in self.states:
                            print(f"\t {self.state_str_dict(state)} = {self.current_state_count(state)}")
                    print(flush=True)

        return True

        pass
