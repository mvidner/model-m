import numpy as np
from model import create_custom_model

# models

# model = ENGINE + MODEL DEFINITION

# engine is not cofigurable yet
# you can specify your model definition


# MODEL DEFINITION

# 1. states, transtion types, parameters
model_definition = {
    # define your model states and transition types
    #
    # define model arguments (arguments of constructor) and parameters (arguments of
    # constuctor)
    # arguments are dictionaries: { arg_name : (default value, description) }
    #  init_arguments   .... model parameters single value
    #                        e.g. "p": (0.2, "probability of external constact")
    #
    #  model_parameters .... model parameters: single value or np.array
    #                        those that can differ for each node
    #                        i.e. "beta": (0.2, "transmission rate")
    #
    # you do note have to define init_{STATE_NAME} arguments, you can use them
    # by default (they define numbers of individuals in individual stats,
    # the rest of population is assing the the first state)

    "states":  [
        "S",
        "S_s",
        "E",
        "I_n",
        "I_a",
        "I_s",
        "I_d",
        "R_d",
        "R_u",
        "D_d",
        "D_u"
    ],

    "transitions":  [
        ("S", "S_s"),
        ("S", "E"),
        ("S_s", "S"),
        ("S_s", "E"),
        ("E", "I_n"),
        ("E", "I_a"),
        ("I_n", "R_u"),
        ("I_a", "I_s"),
        ("I_s", "R_u"),
        ("I_s", "D_u"),
        ("I_s", "I_d"),
        ("I_d", "R_d"),
        ("I_d", "D_d"),
        ("I_a", "I_d"),
        ("E", "I_d")
    ],

    "final_states": [
        "R_d",
        "R_u",
        "D_d",
        "D_u"
    ],

    "invisible_states": [
        "D_u",
        "D_d"
    ],

    "unstable_states": [
        "E",
        "I_n",
        "I_a",
        "I_s",
        "I_d"
    ],

    "init_arguments": {
        "p": (0, "probability of interaction outside adjacent nodes"),
        "q": (0, " probability of detected individuals interaction outside adjacent nodes"),
        "false_symptoms_rate": (0, ""),
        "false_symptoms_recovery_rate": (1., ""),
        "asymptomatic_rate": (0, ""),
        "symptoms_manifest_rate": (1., ""),
    },

    "model_parameters": {
        "beta": (0,  "rate of transmission (exposure)"),
        "sigma": (0, "rate of infection (upon exposure)"),
        "gamma": (0, "rate of recovery (upon infection)"),
        "mu_I": (0, "rate of infection-related death"),
        "beta_D": (0, "rate of transmission (exposure) for detected inds"),
        "gamma_D": (0, "rate of recovery (upon infection) for detected inds"),
        "mu_D": (0, "rate of infection-related death for detected inds"),
        "theta_E": (0, "rate of baseline testing for exposed individuals"),
        "theta_Ia": (0, "rate of baseline testing for Ia individuals"),
        "theta_Is": (0, "rate of baseline testing for Is individuals"),
        "phi_E": (0, "rate of contact tracing testing for exposed individuals"),
        "phi_Ia": (0, "rate of contact tracing testing for Ia individuals"),
        "phi_Is": (0, "rate of contact tracing testing for Is individuals"),
        "psi_E": (0, "probability of positive test results for exposed individuals"),
        "psi_Ia": (0, "probability of positive test results for Ia individuals"),
        "psi_Is": (0, "probability of positive test results for Is individuals")
    }
}

# 2. propensities function


def calc_propensities(model):

    # STEP 1
    # pre-calculate matrix multiplication terms that may be used in multiple propensity calculations,
    # and check to see if their computation is necessary before doing the multiplication

    # number of infectious nondetected contacts
    # sum of all I states
    numContacts_I = np.zeros(shape=(model.num_nodes, 1))
    if any(model.beta):
        infected = [
            s for s in ("I_n", "I_a", "I_s")
            if model.current_state_count(s)
        ]
        if infected:
            numContacts_I = model.num_contacts(infected)

    numContacts_Id = np.zeros(shape=(model.num_nodes, 1))
    if any(model.beta_D):
        numContacts_Id = model.num_contacts("I_d")

    # STEP 2
    # create dict of propensities
    # { transition name: probability values }

    propensities = dict()

    #  "S" ->  "S_s"
    propensities[("S", "S_s")] = model.false_symptoms_rate*(model.X == "S")

    #  "S" -> "E"
    numI = model.current_state_count(
        "I_n") + model.current_state_count("I_a") + model.current_state_count("I_s")

    S_to_E_koef = (
        model.p * (
            model.beta * numI +
            model.q * model.beta_D * model.current_state_count("I_d")
        ) / model.current_N()
        +
        (1 - model.p) * np.divide(
            model.beta * numContacts_I +
            model.beta_D * numContacts_Id, model.degree, out=np.zeros_like(model.degree), where=model.degree != 0
        )
    )
    propensities[("S", "E")] = S_to_E_koef * (model.X == "S")

    propensities[("S_s", "S")
                 ] = model.false_symptoms_recovery_rate*(model.X == "S_s")

    # becoming exposed does not depend on unrelated symptoms
    propensities[("S_s", "E")] = S_to_E_koef * (model.X == "S_s")

    exposed = model.X == "E"
    propensities[("E", "I_n")] = model.asymptomatic_rate * \
        model.sigma * exposed
    propensities[("E", "I_a")] = (
        1-model.asymptomatic_rate) * model.sigma * exposed

    propensities[("I_n", "R_u")] = model.gamma * (model.X == "I_n")

    asymptomatic = model.X == "I_a"
    propensities[("I_a", "I_s")
                 ] = model.symptoms_manifest_rate * asymptomatic

    symptomatic = model.X == "I_s"
    propensities[("I_s", "R_u")] = model.gamma * symptomatic
    propensities[("I_s", "D_u")] = model.mu_I * symptomatic

    detected = model.X == "I_d"
    propensities[("I_d", "R_d")] = model.gamma_D * detected
    propensities[("I_d", "D_d")] = model.mu_D * detected

    # testing  TODO
    propensities[("I_a", "I_d")] = (
        model.theta_Ia + model.phi_Ia * numContacts_Id) * model.psi_Ia * asymptomatic

    propensities[("I_s", "I_d")] = (
        model.theta_Is + model.phi_Is * numContacts_Id) * model.psi_Is * symptomatic

    propensities[("E", "I_d")] = (
        model.theta_E + model.phi_E * numContacts_Id) * model.psi_E * exposed

    # STEP 3
    # return list of all propensities, list of transition names
    # TODO move this step to model.py
    propensities_list = []
    for t in model.transitions:
        propensities_list.append(propensities[t])

    stacked_propensities = np.hstack(propensities_list)

    return stacked_propensities, model.transitions


# 3. model class
ExtendedNetworkModel = create_custom_model("ExtendedNetworkModel",
                                           **model_definition,
                                           calc_propensities=calc_propensities)


# TODO: inherit from ExtendedNetworkModel a new model (high level) that includes the workaround
#      about multi-graphs, manages call backs, etc.
