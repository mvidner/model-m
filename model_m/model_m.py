import random
import copy
import pickle
from model_zoo import model_zoo

import numpy as np

from graph_gen import GraphGenerator, CSVGraphGenerator, RandomSingleGraphGenerator
#from light_graph import LightGraph
from light import LightGraph
from config_utils import ConfigFile


def load_model_from_config(cf, use_policy, model_random_seed, preloaded_graph=None, hyperparams=None):

    # load model hyperparameters
    model_params = cf.section_as_dict("MODEL")
    if hyperparams is not None:
        model_params = {**model_params, **hyperparams}

    # load graph as described in config file
    if preloaded_graph is not None:
        graph = preloaded_graph
    else:
        graph = load_graph(cf)

    # apply policy on model
    policy = _load_policy_function(cf)

    # sceanario
    scenario = cf.section_as_dict("SCENARIO")
    scenario = scenario["closed"] if scenario else None

    # model type
    model_type = cf.section_as_dict("TASK").get(
        "model", "TGMNetworkModel")

    model = ModelM(graph,
                   policy,
                   model_params,
                   scenario,
                   random_seed=model_random_seed,
                   model_type=model_type
                   )
    return model


class ModelM():

    def __init__(self,
                 graph,
                 policy,
                 model_params: dict = None,
                 scenario: list = None,
                 model_type: str = "ExtendedSequentialNetworkModel",
                 random_seed: int = 42):

        # self.random_seed = 42

        # original state
        self.start_graph = graph

        # scenario (list of closed layers)
        self.scenario = scenario

        self.model_type = model_type
        self.model_params = model_params
        self.random_seed = random_seed
        self.policy = policy

        self.model = None
        self.ready = False

    def setup(self):
 #       print("DBD setup")
        # working copy of graph and matrix
        self.graph = self.start_graph.copy()
        self.A = self.init_matrix()

        # model
        Model = model_zoo[self.model_type]
        self.model = Model(self.A,
                           **self.model_params,
                           random_seed=self.random_seed)
        if self.policy[0] is not None:
            self.policy_object = self.policy[0](
                self.graph, self.model, **self.policy[1])
        else:
            self.policy_object = None
        self.model.set_periodic_update(self.policy_object)
        self.ready = True

    def duplicate(self, random_seed=None):
#        pritn("DBD duplicate")

        if self.ready: 
            raise NotImplementedError("We duplicate only newbie models")
        twin = ModelM(
            self.start_graph,
            self.policy,
            self.model_params,
            self.scenario,
            random_seed=self.random_seed if random_seed is None else random_seed,
            model_type=self.model_type
        )
        twin.graph = twin.start_graph.copy()
        twin.A = twin.init_matrix()
        twin.ready = False
        return twin

    def set_model_params(self, model_params: dict):
        self.model.setup_model_params(model_params)

    def run(self, *args, **kwargs):
        if not self.ready:
            self.setup()
        self.model.run(*args, **kwargs)

    def reset(self, random_seed=None):
#        print("DBD reset")
        if not self.ready:
            self.setup()
        else:
            del self.graph
            self.graph = self.start_graph.copy()
            del self.A
            self.A = self.init_matrix()
            self.model.update_graph(self.graph)

            if self.policy_object is not None:
                del self.policy_object 
            if self.policy[0] is not None:
                self.policy_object = self.policy[0](
                    self.graph, self.model, **self.policy[1])
            else:
                self.policy_object = None
            self.model.set_periodic_update(self.policy_object)

        if random_seed:
            self.model.set_seed(random_seed)

        self.model.inicialization()
        self.model.setup_series_and_time_keeping()
        self.model.states_and_counts_init()


    def get_results(self,
                    states):
        if type(states) == list:
            return [self.model.get_state_count(s) for s in states]
        else:
            return self.model.get_state_count(states)

    def save_history(self, file_or_filename):
        self.model.save(file_or_filename)

    def save_node_states(self, filename):
        self.model.save(filename)

    def init_matrix(self):
        if isinstance(self.graph, LightGraph):
            #            raise NotImplementedError(
            #                "LighGraph not  supported at the moment, waits for fixes.")
            return self.graph

        if isinstance(self.graph, RandomSingleGraphGenerator):
            if self.scenario:
                raise NotImplementedError(
                    "RandomGraphGenerator does not support layers.")
            return grahp.G

        # this is what we currently used
        if isinstance(self.graph, GraphGenerator):
            if self.scenario:
                self.graph.close_layers(self.scenario)
            return self.graph.final_adjacency_matrix()

        raise TypeError("Unknown type of graph")


def save_arrays(g):
    arrs = {"e_types": g.e_types, 'e_subtypes': g.e_subtypes, 'e_probs': g.e_probs,
            'e_intensities': g.e_intensities, 'e_source': g.e_source, 'e_dest': g.e_dest, 'e_valid': g.e_valid,
            'edges_repo': g.edges_repo, 'edges_directions': g.edges_directions}
    np.savez('graph_arrays.npz', **arrs)
    np.savez_compressed('graph_arrays_compressed.npz', **arrs)


def load_graph(cf: ConfigFile):
    num_nodes = cf.section_as_dict("TASK").get("num_nodes", None)

    graph_name = cf.section_as_dict("GRAPH")["name"]
    filename = cf.section_as_dict("GRAPH").get("file", None)
    nodes = cf.section_as_dict("GRAPH").get("nodes", "nodes.csv")
    edges = cf.section_as_dict("GRAPH").get("edges", "edges.csv")
    layers = cf.section_as_dict("GRAPH").get("layers", "etypes.csv")

    if graph_name == "csv":
        return CSVGraphGenerator(path_to_nodes=nodes, path_to_edges=edges, path_to_layers=layers)

#    if graph_name == "csv_light":
#        return LightGraph(path_to_nodes=nodes, path_to_edges=edges, path_to_layers=layers)

    if graph_name == "light":
        g = LightGraph()
        g.read_csv(path_to_nodes=nodes, path_to_edges=edges,
                   path_to_layers=layers)
        return g

    if graph_name == "random":
        return RandomGraphGenerator()

    if graph_name == "pickle":
        with open(filename, "rb") as f:
            g = pickle.load(f)
            # save_arrays(g)
            if isinstance(g, GraphGenerator):
                if g.A_valid:
                    print("Wow, matrix A is ready.")
            else:
                assert isinstance(g, LightGraph), f"Something weird ({type(g)}) was loaded."
            return g

    raise ValueError(f"Graph {graph_name} not available.")


def _load_policy_function(cf: ConfigFile):
    policy_cfg = cf.section_as_dict("POLICY")

    policy_name = policy_cfg.get("name", None)
    if policy_name is None:
        return None, None

    if "filename" in policy_cfg:
        PolicyClass = getattr(__import__(
            policy_cfg["filename"]), policy_name)
        setup = cf.section_as_dict("POLICY_SETUP")
        return PolicyClass, setup
    else:
        print("Warning: NO POLICY IN CFG")
        print(policy_cfg)
        raise ValueError("Unknown policy.")
