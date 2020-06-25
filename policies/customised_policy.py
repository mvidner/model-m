import numpy as np
import json
from policy import Policy
from policy_utils import load_scenario_dict


class CustomPolicy(Policy):

    def __init__(self,
                 graph,
                 model,
                 layer_changes_filename = None,
                 param_changes_filename = None, 
                 policy_calendar_filename = None
             ):
        super().__init__(graph, model)

        if layer_changes_filename is not None:
            self.layer_changes_calendar = load_scenario_dict(
                layer_changes_filename)
        else:
            self.layer_changes_calendar = None 

        if policy_calendar_filename is not None:
            with open(policy_calendar_filename, "r") as f:
                self.policy_calendar = json.load(f)
        else:
            self.policy_calendar = None 

        if  param_changes_filename is not None:
            with open(param_changes_filename, "r") as f:
                self.param_changes_calendar = json.load(f)

        self.policies = {}

    def update_layers(self, coefs):
        self.graph.set_layer_weights(coefs)

    def run(self):
        print("CustomPolicy", int(self.model.t))
        today = str(int(self.model.t))

        if self.policy_calendar is not None and today in self.policy_calendar:
            print("changing quarantine policy")
            # change the quaratine policy function
            for action, policy in self.policy_calendar[today]:
                if action == "start":
                    filename, object_name = policy.strip().split(":")
                    PolicyClass = getattr(__import__(filename), object_name)
                    self.policies[policy] = PolicyClass(self.graph, self.model)
                elif action == "stop":
                    self.policies[policy].stop()
                else:
                    raise ValueError(f"Unknown action {action}")

        if self.param_changes_calendar is not None and today in self. param_changes_calendar:
            for action, param, new_value in self.param_changes_calendar[today]: 
                if action == "set":
                    if isinstance(new_value, (list)):
                        np_new_value = np.array(new_value).reshape((self.model.num_nodes, 1))
                    else:
                        np_new_value = np.full(fill_value=new_value, shape=(self.model.num_nodes, 1))
                    setattr(self.model, param, np_new_value)
                elif action == "*":
                    attr = getattr(self.model, param)
                    if type(new_value) == str:
                        new_value = getattr(self.model, new_value)
                    setattr(self.model, param, attr * new_value) 
                else:
                    raise ValueError("Unknown value")

        if self.layer_changes_calendar is not None and today in self.layer_changes_calendar:
            print(f"{today} updating layers")
            self.update_layers(self.layer_changes_calendar[today])

        # perform registred policies
        for name, policy in self.policies.items():
            print("run policy", name)
            policy.run()
