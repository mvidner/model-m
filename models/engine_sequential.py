import pandas as pd
import numpy as np
import scipy as scipy
import scipy.integrate
import networkx as nx
import time
import os
import gc

from history_utils import TimeSeries, TransitionHistory
from engine_seirspluslike import SeirsPlusLikeEngine
# from extended_network_model import STATES as s


class STATES():
    S = 0
    S_s = 1
    E = 2
    I_n = 3
    I_a = 4
    I_s = 5
    I_ds = 6
    J_s = 11
    J_n = 12
    E_d = 13
    I_da = 14
    I_dn = 15
    J_ds = 16
    J_dn = 17
    R_d = 7
    R_u = 8
    D_d = 9
    D_u = 10

    pass


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
            self.state_increments[state][self.t] = 0
            
        self.num_tests[self.t] = 0
        self.num_qtests[self.t] = 0
        self.w_times[self.t] = 0
        self.all_positive_tests[self.t] = 0 
        
        self.durations += 1

        self.N[self.t] = self.N[self.t-1]
#        self.states_history[self.t] = self.states_history[self.t-1]
        # self.meaneprobs[self.t] = self.meaneprobs[self.t-1]
        # self.medianprobs[self.t] = self.meaneprobs[self.t-1]

        # print(self.memberships.shape)
        # print(np.all(self.memberships.sum(axis=0) == 1))
        # print(self.memberships.sum(axis=1))

        # undetected symptomatic
        symptomatic_states = [STATES.I_s, STATES.J_s]
        symptomatic_flags = self.memberships[symptomatic_states, :, :].reshape(
            len(symptomatic_states), self.num_nodes).sum(axis=0)

        self.test_waiting[symptomatic_flags == 1] += 1 
        
        plist = self.calc_propensities()

        #s_and_ss = self.memberships[0] + self.memberships[1]
        #p_infect = (plist[0] + plist[3])[s_and_ss == 1]
        # print(p_infect.mean()>0, np.median(p_infect)>0)
        # exit()
        #self.meaneprobs[self.t] = p_infect.mean()
        #self.medianeprobs[self.t] = np.median(p_infect)

        propensities = np.column_stack(plist)

        # assert np.all(propensities >= 0) and np.all(propensities <= 1), \
        #    f">=0 & <= 1 failed for {propensities[propensities >= 0]} a \
        #    {propensities[propensities<=1]} "

        # check
        # print(propensities.shape)
        # print(self.memberships.shape)
        # print("node 0", self.memberships[:, 0].flatten())
        # print(propensities[0])
        # print(propensities.sum(axis=1q))

        if not np.allclose(propensities.sum(axis=1), 1.0):
            print(propensities.sum(axis=1))
            print(np.logical_not(np.isclose(propensities.sum(axis=1), 1.0)).nonzero())
            index = np.logical_not(np.isclose(
                propensities.sum(axis=1), 1.0)).nonzero()[0][0]
            print(propensities[index])
            print(propensities[index].nonzero())
            print(self.memberships[:, index].nonzero())
            exit()
        assert np.allclose(propensities.sum(axis=1), 1.0)

        # add column with pst P[X->X]
        # what is the fastest way to add a column?
        # propensities = np.append(
        #     propensities, np.product(1.0-propensities, axis=1).reshape(-1, 1), axis=1)

        cumsum = np.cumsum(propensities, axis=1)
        #        total = np.sum(propensities, axis=1)
        r = np.random.rand(self.num_nodes).reshape(-1, 1)

        # compute which event takes place - roulette wheel selection over rows
        transition_idx = _searchsorted2d(cumsum, r)

        # udpate states
        self.delta.fill(0)
        # # filter out last transition (that means stay where you are)
        # indices = transition_idx != self.num_transitions
        # nodes = self.node_ids
        # tran_idxes = transition_idx

        # looks like list(zip()) is faster than zip(), but not sure what is the best
        # to walk through two numpy arrays
        #        for node, idx in list(zip(nodes, tran_idxes)):
        for node, idx in enumerate(transition_idx):
            # if idx == self.num_transitions:  # state in current state
            #     continue
            s, e = self.transitions[idx]
            if s == e:
                continue
            # print(f"{node} goes from {self.state_str_dict[s]} to {self.state_str_dict[e]}")
            # if self.memberships[s, node, 0] != 1:
            #     print(f"node not in state {self.state_str_dict[s]}")
            if node == 29691:
                # stalking
                print(f"ACTION LOG ({self.t}): node {node} changing state to {self.state_str_dict[e]}")

            self.states_durations[s].append(self.durations[node])
            if e in (
                    STATES.I_ds,
                    STATES.E_d,
                    STATES.I_da,
                    STATES.I_dn,
                    STATES.J_ds,
                    STATES.J_dn
            ):
                self.num_tests[self.t] += 1
                self.w_times[self.t] += self.test_waiting[node] 
                self.all_positive_tests[self.t] += 1

            self.durations[node] = 0
            self.delta[s, node, :] = -1
            self.delta[e, node, :] = 1
            self.state_counts[s][self.t] -= 1
            self.state_counts[e][self.t] += 1
            self.state_increments[e][self.t] += 1
            #self.states_history[self.t][node] = e
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

    def run(self, T, print_interval=0, verbose=False):

        # keep it, saves time
        self.delta = np.empty((self.num_states, self.num_nodes, 1), dtype=int)
        self.node_ids = np.arange(self.num_nodes)

        running = True
        self.tidx = 0
        if print_interval >= 0:
            self.print(verbose)

        for self.t in range(1, T+1):
            print("DBG graph.layer_weights", self.graph.layer_weights)
            #            os.system("free -h")
            if __debug__ and print_interval >= 0 and verbose:
                print(flush=True)
#                input()
            #            print(f"day {self.t}")

            # print(self.t)
            # print(len(self.state_counts[0]))
            # print(len(self.states_history))
            if (self.t >= len(self.state_counts[0])):
                # room has run out in the timeseries storage arrays; double the size of these arrays
                self.increase_data_series_length()

            start = time.time()
            running = self.run_iteration()

            # run periodical update
            if self.periodic_update_callback is not None:
                self.periodic_update_callback.run()
                # changes = self.periodic_update_callback(
                #     self.history, self.tseries[:self.tidx +
                #                                1], self.t, self.contact_history,
                #     self.memberships)

                # if "graph" in changes:
                #     print("CHANGING GRAPH")
                #     self.update_graph(changes["graph"])
            end = time.time()
            if print_interval > 0:
                print("Last day took: ", end - start, "seconds")

            if print_interval > 0 and (self.t % print_interval == 0):
                self.print(verbose)

            # Terminate if tmax reached or num infectious and num exposed is 0:
            numI = sum([self.current_state_count(s)
                        for s in self.unstable_states
                        ])
            # if True:
            #     GIRL = 29691
            #     # infect the girl 29691
            #     if self.graph.layer_weights[30] == 1.0:
            #         # move node 29691 to E
            #         orig_state = self.memberships[:, GIRL].nonzero()[0][0]
            #         if orig_state == STATES.E:
            #             print(f"ACTION LOG(92): node 29691 enters the party already exposed")
            #         else:
            #             print(f"ACTION LOG(92): node 29691 feeded by infection")
            #             self.state_counts[STATES.E][self.t] += 1
            #             self.state_counts[orig_state][self.t] -= 1
            #             self.state_increments[STATES.E][self.t] += 1
            #             self.memberships[STATES.E][GIRL] = 1
            #             self.memberships[orig_state][GIRL] = 0

            #if not numI > 0:
            #    break
            # gc.collect()

        if self.t < T:
            for t in range(self.t+1, T+1):
                if (t >= len(self.state_counts[0])):
                    self.increase_data_series_length()
                for state in self.states:
                    self.state_counts[state][t] = self.state_counts[state][t-1]
                    self.state_increments[state][t] = 0

        self.t = T

        # finalize durations
        for s in self.states:
            durations = self.durations[self.memberships[s].flatten() == 1]
            self.states_durations[s].extend(list(durations))

        if print_interval >= 0:
            self.print(verbose)
        self.finalize_data_series()
        return True

    def increase_data_series_length(self):
        for state in self.states:
            self.state_counts[state].bloat(100)
            self.state_increments[state].bloat(100)
        self.num_tests.bloat(100)
        self.num_qtests.bloat(100)
        self.w_times.bloat(100)
        self.all_positive_tests.bloat(100)

        self.N.bloat(100)
        # self.states_history.bloat(100)
        self.meaneprobs.bloat(100)
        self.medianeprobs.bloat(100)

    def increase_history_len(self):
        self.tseries.bloat(10*self.num_nodes)
        self.history.bloat(10*self.num_nodes)

    def finalize_data_series(self):
        self.tseries.finalize(self.tidx)
        self.history.finalize(self.tidx)
        self.num_tests.finalize(self.t)
        self.num_qtests.finalize(self.t)
        self.w_times.finalize(self.t)
        self.all_positive_tests.finalize(self.t)
        

        for state in self.states:
            self.state_counts[state].finalize(self.t)
            self.state_increments[state].finalize(self.t)
        self.N.finalize(self.t)
        # self.states_history.finalize(self.t)
        self.meaneprobs.finalize(self.t)
        self.medianeprobs.finalize(self.t)

    def current_state_count(self, state):
        """ here current = self.t (not self.tidx as in seirsplus-derived models) """
        return self.state_counts[state][self.t]

    def current_N(self):
        """ here current = self.t (not self.tidx as in seirsplus-derived models) """
        return self.N[self.t]

    def get_state_count(self, state=None):
        if state is None:
            return self.state_counts
        return self.state_counts[state]

    def to_df(self):
        index = range(0, self.t+1)
        col_increments = {
            "inc_" + self.state_str_dict[x]: col_inc
            for x, col_inc in self.state_increments.items()
        }
        col_states = {
            self.state_str_dict[x]: count
            for x, count in self.state_counts.items()
        }
        col_tests = {
            "tests": self.num_tests,
            "quarantine_tests": self.num_qtests,
            "sum_of_waiting": self.w_times,
            "all_positive_tests": self.all_positive_tests
        }
        columns = {**col_states, **col_increments, **col_tests}
        columns["day"] = np.floor(index).astype(int)
        #        columns["mean_p_infection"] = self.meaneprobs
        #        columns["median_p_infection"] = self.medianeprobs
        df = pd.DataFrame(columns, index=index)
        df.index.rename('T', inplace=True)
        return df

    def save(self, file_or_filename):
        """ Save timeseries. They have different format than in BaseEngine,
        so I redefined save method here """
        df = self.to_df()
        df.to_csv(file_or_filename)
        print(df)

    def save_durations(self, f):
        for s in self.states:
            line = ",".join([str(x) for x in self.states_durations[s]])
            print(f"{self.state_str_dict[s]},{line}", file=f)

    def save_node_states(self, filename):
        index = range(0, self.t+1)
        columns = self.states_history.values
        df = pd.DataFrame(columns, index=index)
        df.to_csv(filename)
        # df = df.replace(self.state_str_dict)
        # df.to_csv(filename)
        # print(df)

    def detected_node(self, node_number):
        # self.num_qtests[self.t] += 1
        orig_state = self.memberships[:, node_number].nonzero()[0][0]

        if orig_state in (STATES.E_d, STATES.I_da, STATES.I_dn, STATES.I_ds, STATES.J_dn, STATES.J_ds):
            return

        transitions = (
            (STATES.E, STATES.E_d),
            (STATES.I_a, STATES.I_da),
            (STATES.I_n, STATES.I_dn),
            (STATES.I_s, STATES.I_ds),
            (STATES.J_n, STATES.J_dn),
            (STATES.J_s, STATES.J_ds)
        )

        self.w_times[self.t] += self.test_waiting[node_number]
        self.all_positive_tests[self.t] += 1 

        for t in transitions:
            if orig_state == t[0]:
                new_state = t[1]
                if 29691 == node_number:
                    print(f"ACTION LOG({self.t}): node 29691 forced to change state to {self.state_str_dict[new_state]} from {self.state_str_dict[orig_state]}")
                self.states_durations[orig_state].append(self.durations[node_number])
                self.durations[node_number] = 0 
                self.state_counts[new_state][self.t] += 1
                self.state_counts[orig_state][self.t] -= 1
                self.state_increments[new_state][self.t] += 1
                self.memberships[new_state][node_number] = 1
                self.memberships[orig_state][node_number] = 0
                return

        raise ValueError(f"Unexpected state: {self.state_str_dict[orig_state]}")
