import numpy as np
from model import create_custom_model
from engine_daily import DailyEngine

# models

# model = ENGINE + MODEL DEFINITION

# engine is not cofigurable yet
# you can specify your model definition

class STATES():
    S = 0
    S_s = 1
    E = 2
    I_n = 3
    I_a = 4
    I_s = 5 
    I_d = 6
    R_d = 7
    R_u = 8
    D_d = 9
    D_u = 10

    pass 

state_codes = {
    STATES.S:     "S",    
    STATES.S_s:   "S_s",    
    STATES.E:     "E", 
    STATES.I_n:   "I_n", 
    STATES.I_a:   "I_a", 
    STATES.I_s:   "I_s", 
    STATES.I_d:   "I_d", 
    STATES.R_d:   "R_d", 
    STATES.R_u:   "R_u", 
    STATES.D_d:   "D_d", 
    STATES.D_u:    "D_u"
}


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
        STATES.S, STATES.S_s,
        STATES.E, 
        STATES.I_n,
        STATES.I_a,
        STATES.I_s,
        STATES.I_d,
        STATES.R_d,
        STATES.R_u,
        STATES.D_d,
        STATES.D_u
    ],

    "state_str_dict": state_codes,

    "transitions":  [
        (STATES.S, STATES.S_s),
        (STATES.S, STATES.E),
        (STATES.S_s, STATES.S),
        (STATES.S_s, STATES.E),
        (STATES.E, STATES.I_n),
        (STATES.E, STATES.I_a),
        (STATES.I_n, STATES.R_u),
        (STATES.I_a, STATES.I_s),
        (STATES.I_s, STATES.R_u),
        (STATES.I_s, STATES.D_u),
        (STATES.I_s, STATES.I_d),
        (STATES.I_d, STATES.R_d),
        (STATES.I_d, STATES.D_d),
        (STATES.I_a, STATES.I_d),
        (STATES.E, STATES.I_d)
    ],

    "final_states": [
        STATES.R_d,
        STATES.R_u,
        STATES.D_d,
        STATES.D_u
    ],

    "invisible_states": [
        STATES.D_u,
        STATES.D_d
    ],

    "unstable_states": [
        STATES.E,
        STATES.I_n,
        STATES.I_a,
        STATES.I_s,
        STATES.I_d
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
            s for s in (STATES.I_n, STATES.I_a, STATES.I_s)
            if model.current_state_count(s)
        ]
        if infected:
            numContacts_I = model.num_contacts(infected)

    numContacts_Id = np.zeros(shape=(model.num_nodes, 1))
    if any(model.beta_D):
        numContacts_Id = model.num_contacts(STATES.I_d)

    # STEP 2
    # create dict of propensities
    # { transition name: probability values }

    propensities = dict()

    #  "S" ->  "S_s"
    propensities[(STATES.S, STATES.S_s)] = model.false_symptoms_rate*(model.X == STATES.S)

    #  "S" -> "E"
    numI = model.current_state_count(
        STATES.I_n) + model.current_state_count(STATES.I_a) + model.current_state_count(STATES.I_s)

    S_to_E_koef = (
        model.p * (
            model.beta * numI +
            model.q * model.beta_D * model.current_state_count(STATES.I_d)
        ) / model.current_N()
        +
        (1 - model.p) * np.divide(
            model.beta * numContacts_I +
            model.beta_D * numContacts_Id, model.degree, out=np.zeros_like(model.degree), where=model.degree != 0
        )
    )
    propensities[(STATES.S, STATES.E)] = S_to_E_koef * (model.X == STATES.S)

    propensities[(STATES.S_s, STATES.S)
                 ] = model.false_symptoms_recovery_rate*(model.X == STATES.S_s)

    # becoming exposed does not depend on unrelated symptoms
    propensities[(STATES.S_s, STATES.E)] = S_to_E_koef * (model.X == STATES.S_s)

    exposed = model.X == STATES.E
    propensities[(STATES.E, STATES.I_n)] = model.asymptomatic_rate * \
        model.sigma * exposed
    propensities[(STATES.E, STATES.I_a)] = (
        1-model.asymptomatic_rate) * model.sigma * exposed

    propensities[(STATES.I_n, STATES.R_u)] = model.gamma * (model.X == STATES.I_n)

    asymptomatic = model.X == STATES.I_a
    propensities[(STATES.I_a, STATES.I_s)
                 ] = model.symptoms_manifest_rate * asymptomatic

    symptomatic = model.X == STATES.I_s
    propensities[(STATES.I_s, STATES.R_u)] = model.gamma * symptomatic
    propensities[(STATES.I_s, STATES.D_u)] = model.mu_I * symptomatic

    detected = model.X == STATES.I_d
    propensities[(STATES.I_d, STATES.R_d)] = model.gamma_D * detected
    propensities[(STATES.I_d, STATES.D_d)] = model.mu_D * detected

    # testing  TODO
    propensities[(STATES.I_a, STATES.I_d)] = (
        model.theta_Ia + model.phi_Ia * numContacts_Id) * model.psi_Ia * asymptomatic

    propensities[(STATES.I_s, STATES.I_d)] = (
        model.theta_Is + model.phi_Is * numContacts_Id) * model.psi_Is * symptomatic

    propensities[(STATES.E, STATES.I_d)] = (
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

ExtendedDailyNetworkModel = create_custom_model("ExtendedDailyNetworkModel",
                                                **model_definition,
                                                calc_propensities=calc_propensities,
                                                engine=DailyEngine)


# TODO: inherit from ExtendedNetworkModel a new model (high level) that includes the workaround
#      about multi-graphs, manages call backs, etc.
