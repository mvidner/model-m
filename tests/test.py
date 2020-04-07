import numpy as np
from model import create_model_base
from romeo_juliet_graph_gen import RomeoAndJuliet as Verona
from run_experiment import magic_formula


states = ["S", "I", "R", "D"]
transitions = [("S", "I"), ("I", "R"), ("R", "S"), ("I", "D")]
final_states = ["D"]
invisible_states = ["D"]
params = {}
model_params = {"beta": (0.5, "pst of transition to anather state"),
                "gamma": (0.02, "death rate")}


def calc_propensities(self):
    """ example of propensities function 
    you will typically use information from graph here 
    use self.A, self.num_contacts, etc.  
    """
    propensities = {}
    for t in self.transitions:
        propensities[t] = self.beta * \
            (self.X == t[0]) * self.num_contacts("I") / self.current_N()
    propensities[("I", "D")] = self.gamma * (self.X == "I")

    propensities_list = []
    for t in self.transitions:
        propensities_list.append(propensities[t])
    stacked_propensities = np.hstack(propensities_list)

    return stacked_propensities, self.transitions


SIRDModel = create_model_base("SIRDModel", states, transitions,
                              final_states=final_states,
                              invisible_states=invisible_states,
                              init_arguments=params, model_parameters=model_params,
                              calc_propensities=calc_propensities)


g = Verona()
A = magic_formula(g.as_dict_of_graphs(), g.get_layers_info())


model = SIRDModel(A, beta=0.5, gamma=0.2, init_I=5)
print(model.__doc__)

print(model.states)
model.run(60, verbose=True, print_interval=5)
