import numpy as np
from model import create_custom_model
from engine_daily import DailyEngine
from engine_sequential import SequentialEngine
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


# constants - have to be consisten with transtion list
S_to_S_s = 0
S_to_E = 1
S_s_to_S = 2
S_s_to_E = 3
E_to_I_n = 4
E_to_I_a = 5
I_n_to_R_u = 6
I_a_to_I_s = 7
I_s_to_R_u = 8
I_s_to_D_u = 9
I_s_to_I_d = 10
I_d_to_R_d = 11
I_d_to_D_d = 12
I_a_to_I_d = 13
E_to_I_d = 14


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


def calc_propensities(model, use_dict=True):

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
    propensity_S_to_S_s = model.false_symptoms_rate * \
        (model.memberships[STATES.S])

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

    propensity_S_to_E = S_to_E_koef * \
        (model.memberships[STATES.S])

    propensity_S_s_to_S = model.false_symptoms_recovery_rate * \
        (model.memberships[STATES.S_s])

    # becoming exposed does not depend on unrelated symptoms
    propensity_S_s_to_E = S_to_E_koef * \
        (model.memberships[STATES.S_s])

    exposed = model.memberships[STATES.E]
    propensity_E_to_I_n = model.asymptomatic_rate * \
        model.sigma * exposed
    propensity_E_to_I_a = (
        1-model.asymptomatic_rate) * model.sigma * exposed

    propensity_I_n_to_R_u = model.gamma * \
        (model.memberships[STATES.I_n])

    asymptomatic = model.memberships[STATES.I_a]
    propensity_I_a_to_I_s = model.symptoms_manifest_rate * asymptomatic

    symptomatic = model.memberships[STATES.I_s]
    propensity_I_s_to_R_u = model.gamma * symptomatic
    propensity_I_s_to_D_u = model.mu_I * symptomatic

    detected = model.memberships[STATES.I_d]
    propensity_I_d_to_R_d = model.gamma_D * detected
    propensity_I_d_to_D_d = model.mu_D * detected

    # testing  TODO
    propensity_I_a_to_I_d = (
        model.theta_Ia + model.phi_Ia * numContacts_Id) * model.psi_Ia * asymptomatic

    propensity_I_s_to_I_d = (
        model.theta_Is + model.phi_Is * numContacts_Id) * model.psi_Is * symptomatic

    propensity_E_to_I_d = (
        model.theta_E + model.phi_E * numContacts_Id) * model.psi_E * exposed

    return [
        propensity_S_to_S_s,
        propensity_S_to_E,
        propensity_S_s_to_S,
        propensity_S_s_to_E,
        propensity_E_to_I_n,
        propensity_E_to_I_a,
        propensity_I_n_to_R_u,
        propensity_I_a_to_I_s,
        propensity_I_s_to_R_u,
        propensity_I_s_to_D_u,
        propensity_I_s_to_I_d,
        propensity_I_d_to_R_d,
        propensity_I_d_to_D_d,
        propensity_I_a_to_I_d,
        propensity_E_to_I_d,
    ]


# 3. model class
ExtendedNetworkModel = create_custom_model("ExtendedNetworkModel",
                                           **model_definition,
                                           calc_propensities=calc_propensities)

ExtendedDailyNetworkModel = create_custom_model("ExtendedDailyNetworkModel",
                                                **model_definition,
                                                calc_propensities=calc_propensities,
                                                engine=DailyEngine)

ExtendedSequentialNetworkModel = create_custom_model("ExtendedSequentialNetworkModel",
                                                     **model_definition,
                                                     calc_propensities=calc_propensities,
                                                     engine=SequentialEngine)

# TODO: inherit from ExtendedNetworkModel a new model (high level) that includes the workaround
#      about multi-graphs, manages call backs, etc.
