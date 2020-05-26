import json
from policy import Policy
from policy_utils import load_scenario_dict


class CustomPolicy(Policy):

    def __init__(self,
                 graph,
                 model,
                 layer_changes_filename,
                 policy_calendar_filename
                 ):
        super().__init__(graph, model)

        self.layer_changes_calendar = load_scenario_dict(
            layer_changes_filename)

        with open(policy_calendar_filename, "r") as f:
            self.policy_calendar = json.load(f)

        self.policies = {}

    def update_layers(self, coefs):
        self.graph.set_layer_weights(coefs)

    def run(self):
        print("CustomPolicy", int(self.model.t))
        today = str(int(self.model.t))

        if today in self.policy_calendar:
            print("changing quarantine policy")
            # change the quaratine policy function
            for action, policy in self.policy_calendar[today]:
                if action == "start":
                    filename, object_name = policy.strip().split(":")
                    PolicyClass = getattr(__import__(filename), object_name)
                    self.policies[policy] = PolicyClass(self.graph, self.model)
                elif action == "stop":
                    del self.policies[policy]
                else:
                    raise ValueError(f"Unknown action {action}")

        if today in self.layer_changes_calendar:
            print(f"{today} updating layers")
            self.update_layers(self.layer_changes_calendar[today])

        # perform registred policies
        for name, policy in self.policies.items():
            print("run policy", name)
            policy.run()
