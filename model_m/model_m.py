import random
import copy

from model_zoo import model_zoo

from graph_gen import GraphGenerator, CSVGraphGenerator, RandomSingleGraphGenerator
from light_graph import LightGraph
from policy import bound_policy
from config_utils import ConfigFile


def load_model_from_config(cf, use_policy, model_random_seed):

    # load model hyperparameters
    model_params = cf.section_as_dict("MODEL")

    # load graph as described in config file
    graph = _load_graph(cf)

    # apply policy on model
    policy, policy_setup = _load_policy_function(
        cf, use_policy) if use_policy else (None, None)

    # sceanario
    scenario = cf.section_as_dict("SCENARIO")
    scenario = scenario["closed"] if scenario else None

    # model type
    model_type = cf.section_as_dict("TASK").get(
        "model", "ExtendedNetworkModel")

    model = ModelM(graph,
                   policy, policy_setup,
                   model_params,
                   scenario,
                   random_seed=model_random_seed,
                   model_type=model_type
                   )
    return model


class ModelM():

    def __init__(self,
                 graph,
                 policy, policy_setup,
                 model_params: dict = None,
                 scenario: list = None,
                 model_type: str = "ExtendedSequentialNetworkModel",
                 random_seed: int = 42):

        self.random_seed = 42

        # original state
        self.start_graph = graph

        # scenario (list of closed layers)
        self.scenario = scenario

        # working copy of graph and matrix
        self.graph = copy.deepcopy(self.start_graph)
        self.A = self.init_matrix()

        # model
        Model = model_zoo[model_type]
        self.model = Model(self.A,
                           **model_params,
                           random_seed=random_seed)

        if policy_setup:
            policy_coefs = policy_setup(self.graph, self.start_graph)
        if policy:
            policy_function = bound_policy(
                policy, self.graph, coefs=policy_coefs)
            self.model.set_periodic_update(policy_function)

    def set_model_params(self, model_params: dict):
        self.model.setup_model_params(model_params)

    def run(self, *args, **kwargs):
        self.model.run(*args, **kwargs)

    def reset(self):
        del self.graph
        self.graph = copy.deepcopy(self.start_graph)
        del self.A
        self.A = self.init_matrix()
        # self.set_model_params() TODO

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
            raise NotImplementedError(
                "LighGraph not  supported at the moment, waits for fixes.")

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


def _load_graph(cf: ConfigFile):
    num_nodes = cf.section_as_dict("TASK").get("num_nodes", None)

    graph_name = cf.section_as_dict("GRAPH")["name"]
    nodes = cf.section_as_dict("GRAPH").get("nodes", "nodes.csv")
    edges = cf.section_as_dict("GRAPH").get("edges", "edges.csv")
    layers = cf.section_as_dict("GRAPH").get("layers", "etypes.csv")

    if graph_name == "csv":
        return CSVGraphGenerator(path_to_nodes=nodes, path_to_edges=edges, path_to_layers=layers)

    if graph_name == "csv_light":
        return LightGraph(path_to_nodes=nodes, path_to_edges=edges, path_to_layers=layers)

    if graph_name == "random":
        return RandomGraphGenerator()

    raise ValueError(f"Graph {graph_name} not available.")


def _load_policy_function(cf: ConfigFile, policy_name: str):
    policy_cfg = cf.section_as_dict("POLICY")
    if policy_name not in policy_cfg["name"]:
        raise ValueError("Unknown policy name.")

    if policy_cfg and "filename" in policy_cfg:
        policy = getattr(__import__(
            policy_cfg["filename"]), policy_name)
        setup = policy_cfg.get("setup", None)
        policy_setup = getattr(__import__(
            policy_cfg["filename"]), setup) if setup else None
        return policy, policy_setup
    else:
        print("Warning: NO POLICY IN CFG")
        print(policy_cfg)
        raise ValueError("Unknown policy.")