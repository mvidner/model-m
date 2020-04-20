import pandas as pd
import numpy as np
import scipy as scipy
import scipy.integrate
import networkx as nx
import time

from history_utils import TimeSeries, TransitionHistory
from engine_seirspluslike import SeirsPlusLikeEngine


def _searchsorted2d(a, b):
    m, n = a.shape
    max_num = np.maximum(a.max() - a.min(), b.max() - b.min()) + 1
    r = max_num * np.arange(a.shape[0])[:, None]
    p = np.searchsorted((a+r).ravel(), (b+r).ravel())
    return p - n*np.arange(m)


class SequentialEngine(SeirsPlusLikeEngine):
    """ should work in the same way like SEIRSPlusLikeEngine
    but makes the state changes only once a day """

    def run_iteration(self):
        # add timeseries members
        for state in self.states:
            self.state_counts[state][self.t] = self.state_counts[state][self.t-1]
        self.N[self.t] = self.N[self.t-1]
        self.states_history[self.t] = self.states_history[self.t-1]

        propensities = np.column_stack(self.calc_propensities())
        # add column with pst P[X->X]
        # what is the fastest way to add a column?
        propensities = np.append(
            propensities, np.product(1.0-propensities, axis=1).reshape(-1, 1), axis=1)

        cumsum = np.cumsum(propensities, axis=1)
        total = np.sum(propensities, axis=1)
        r = (np.random.rand(self.num_nodes)*total).reshape(-1, 1)

        # compute which event takes place - roulette wheel selection over rows
        transition_idx = _searchsorted2d(cumsum, r)

        # udpate states
        self.delta.fill(0)
        # filter out last transition (that means stay where you are)
        indices = transition_idx != self.num_transitions
        nodes = self.node_ids[indices]
        tran_idxes = transition_idx[indices]

        # looks like list(zip()) is faster than zip(), but not sure what is the best
        # to walk through two numpy arrays
        for node, idx in list(zip(nodes, tran_idxes)):
            # if idx == self.num_transitions:  # state in current state
            #     continue
            s, e = self.transitions[idx]
            # print(f"{node} goes from {self.state_str_dict[s]} to {self.state_str_dict[e]}")
            # if self.memberships[s, node, 0] != 1:
            #     print(f"node not in state {self.state_str_dict[s]}")

            self.delta[s, node, :] = -1
            self.delta[e, node, :] = 1
            self.state_counts[s][self.t] -= 1
            self.state_counts[e][self.t] += 1
            self.states_history[self.t][node] = e
            self.tidx += 1
            if self.tidx >= len(self.history):
                self.increase_history_len()
            self.tseries[self.tidx] = self.t
            self.history[self.tidx] = (node, s, e)

            # if node died
            if e in (self.invisible_states):
                self.N[self.t] -= 1

        # the real states update
        self.memberships += self.delta
        return True

    def print(self, verbose=False):
        print("t = %.2f" % self.t)
        if verbose:
            for state in self.states:
                print(f"\t {self.state_str_dict[state]} = {self.current_state_count(state)}")
#                print(flush=True)

    def run(self, T, print_interval=10, verbose=False):

        # keep it, saves time
        self.delta = np.empty((self.num_states, self.num_nodes, 1), dtype=int)
        self.node_ids = np.arange(self.num_nodes)

        running = True
        self.tidx = 0
        self.print(True)

        for self.t in range(1, T+1):
            #            print(f"day {self.t}")

            print(self.t)
            print(len(self.state_counts[0]))
            print(len(self.states_history))
            if (self.t >= len(self.state_counts[0])):
                # room has run out in the timeseries storage arrays; double the size of these arrays
                self.increase_data_series_length()

            start = time.time()
            running = self.run_iteration()

            # run periodical update
            if self.periodic_update_callback:
                changes = self.periodic_update_callback(
                    self.history, self.tseries[:self.tidx+1], self.t)

                if "graph" in changes:
                    print("CHANGING GRAPH")
                    self.update_graph(changes["graph"])
            end = time.time()
            print("Last day took: ", end - start, "seconds")

            if print_interval and (self.t % print_interval == 0):
                self.print(verbose)

            # Terminate if tmax reached or num infectious and num exposed is 0:
            numI = sum([self.current_state_count(s)
                        for s in self.unstable_states
                        ])
            if not numI > 0:
                break

        self.print(verbose)
        self.finalize_data_series()
        return True

    def increase_data_series_length(self):
        for state in self.states:
            self.state_counts[state].bloat(300)
        self.N.bloat()
        self.states_history(300)

    def increase_history_len(self):
        self.tseries.bloat(100*self.num_nodes)
        self.history.bloat(100*self.num_nodes)

    def finalize_data_series(self):
        self.tseries.finalize(self.tidx)
        self.history.finalize(self.tidx)
        for state in self.states:
            self.state_counts[state].finalize(self.t)
        self.N.finalize(self.t)
        self.states_history.finalize(self.t)

    def current_state_count(self, state):
        """ here current = self.t (not self.tidx as in seirsplus-derived models) """
        return self.state_counts[state][self.t]

    def current_N(self):
        """ here current = self.t (not self.tidx as in seirsplus-derived models) """
        return self.N[self.t]

    def save(self, file_or_filename):
        """ Save timeseries. They have different format than in BaseEngine,
        so I redefined save method here """
        index = range(0, self.t+1)
        columns = self.state_counts
        columns["day"] = index
        df = pd.DataFrame(self.state_counts, index=index)
        df.index.rename('T', inplace=True)
        df.columns = [self.state_str_dict[x] for x in self.states] + ["day"]
        df.to_csv(file_or_filename)
        print(df)

    def save_node_states(self, filename):
        index = range(0, self.t+1)
        columns = self.states_history.values
        df = pd.DataFrame(columns, index=index)
        df.to_csv(filename)
        # df = df.replace(self.state_str_dict)
        # df.to_csv(filename)
        print(df)
