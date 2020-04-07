import matplotlib.pyplot as plt
import numpy as np
from run_experiment import tell_the_story
from model import create_custom_model
from romeo_juliet_graph_gen import RomeoAndJuliet as Verona
from run_experiment import magic_formula

# 1. **Define whatever you need**

model_definition = {
    # model definition comes here
    "states": ["sleeping", "alert", "tired", "dead"],
    "transitions": [
        ("sleeping", "alert"),
        ("alert", "tired"),
        ("tired", "sleeping"),
        ("tired", "dead")
    ],
    # optionally:
    "final_states": ["dead"],
    "invisible_states": ["dead"],

    "model_parameters": {
        "wake_up_rate": (0.2, "wake up prob"),
        "tiredability": (0.3, "getting tired rate"),
        "mu": (0.1, "death rate"),
        "sleepiness": (0.7, "rate of falling in sleep")
    }
}


def calc_propensities(model):
    # define your calculations here
    # you may use various model utilities, as
    #       model.num_contacts(state or list of states),
    #       model.current_state_count(state), model.current_N(),
    #       etc.; access list of states, transitions, parameters.

    propensities = {}

    propensities[("sleeping", "alert")] = model.wake_up_rate * \
        (model.X == "sleeping")
    propensities[("alert",  "tired")] = (model.tiredability
                                         * (model.num_contacts(["alert", "tired"]) / model.current_N())
                                         * (model.X == "alert")
                                         )
    tired = model.X == "tired"
    propensities[("tired", "sleeping")] = model.sleepiness * tired
    propensities[("tired", "dead")] = model.mu * tired

    # TODO move this part to model.py
    propensities_list = []
    for t in model.transitions:
        propensities_list.append(propensities[t])
    stacked_propensities = np.hstack(propensities_list)

    return stacked_propensities, model.transitions


# 2. **Create custom class**


CustomModel = create_custom_model("CustomModel", **model_definition,
                                  calc_propensities=calc_propensities)
# 3. **Load your graph**

g = Verona()
A = magic_formula(g.as_dict_of_graphs(), g.get_layers_info())

# 4. **Create model**
tiredability = 0.01 * np.array(g.get_attr_list("age"))
model = CustomModel(A,  wake_up_rate=0.8, init_alert=10, tiredability=tiredability,
                    init_tired=10, random_seed=35)

# 5. **Run**
model.run(T=60, verbose=True, print_interval=5)

# 6. **Inspect results**

x = model.tseries
population = model.N
alert = model.state_counts["alert"]
plt.plot(x, population, label="population")
plt.plot(x, alert, label="alert population")
plt.legend()
plt.savefig("alert_pop.png")
# etc

# 7. **Procrastinate**

# text = tell_the_story(model.history, g)
# print()
