import numpy as np
from model import create_custom_model
from engine_daily import DailyEngine
from engine_sequential import SequentialEngine
from engine_m import EngineM
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
        (STATES.S_s,  STATES.E),
        (STATES.S_s,  STATES.S),
        (STATES.S_s,  STATES.S_s),

        (STATES.S, STATES.E),
        (STATES.S, STATES.S_s),
        (STATES.S, STATES.S),

        (STATES.E, STATES.I_d),
        (STATES.E, STATES.I_n),
        (STATES.E, STATES.I_a),
        (STATES.E, STATES.E),

        (STATES.I_n, STATES.R_u),
        (STATES.I_n, STATES.I_d),
        (STATES.I_n, STATES.I_n),

        (STATES.I_a, STATES.I_d),
        (STATES.I_a, STATES.I_s),
        (STATES.I_a, STATES.I_a),

        (STATES.I_s, STATES.R_u),
        (STATES.I_s, STATES.D_u),
        (STATES.I_s, STATES.I_d),
        (STATES.I_s, STATES.I_s),

        (STATES.I_d, STATES.R_d),
        (STATES.I_d, STATES.D_d),
        (STATES.I_d, STATES.I_d),

        (STATES.R_d, STATES.R_d),
        (STATES.R_u, STATES.R_u),
        (STATES.D_d, STATES.D_d),
        (STATES.D_u, STATES.D_u)
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
        "save_nodes": (False, "")
    },

    "model_parameters": {
        "beta": (0,  "rate of transmission (exposure)"),
        "beta_reduction": (0,  "todo"),
        "beta_in_family": (0, "todo"),
        "beta_A": (0, "todo"),
        "beta_A_in_family": (0, "todo"),
        "sigma": (0, "rate of infection (upon exposure)"),
        "gamma_In": (0, "rate of recovery (upon infection)"),
        "gamma_Is": (0, "rate of recovery (upon infection)"),
        "gamma_Id": (0, "rate of recovery (upon infection)"),
        "mu": (0, "rate of infection-related death"),
        "beta_D": (0, "rate of transmission (exposure) for detected inds"),
        "mu_D": (0, "rate of infection-related death for detected inds"),
        "theta_E": (0, "rate of baseline testing for exposed individuals"),
        "theta_Ia": (0, "rate of baseline testing for Ia individuals"),
        "theta_Is": (0, "rate of baseline testing for Is individuals"),
        "theta_In": (0, "rate of baseline testing for In individuals"),
        "phi_E": (0, "rate of contact tracing testing for exposed individuals"),
        "phi_Ia": (0, "rate of contact tracing testing for Ia individuals"),
        "phi_Is": (0, "rate of contact tracing testing for Is individuals"),
        "psi_E": (0, "probability of positive test results for exposed individuals"),
        "psi_Ia": (0, "probability of positive test results for Ia individuals"),
        "psi_Is": (0, "probability of positive test results for Is individuals"),
        "psi_In": (0, "probability of positive test results for In individuals")
    }
}

# 2. propensities function


def calc_propensities(model, use_dict=True):

    # STEP 1
    # pre-calculate matrix multiplication terms that may be used in multiple propensity calculations,
    # and check to see if their computation is necessary before doing the multiplication

    # number of infectious nondetected contacts
    # sum of all I states
    # numContacts_I = np.zeros(shape=(model.num_nodes, 1))
    # if any(model.beta):
    #     infected = [
    #         s for s in (STATES.I_n, STATES.I_a, STATES.I_s)
    #         if model.current_state_count(s)
    #     ]
    #     if infected:
    #         numContacts_I = model.num_contacts(infected)

    # numContacts_Id = np.zeros(shape=(model.num_nodes, 1))
    # if any(model.beta_D):
    #     numContacts_Id = model.num_contacts(STATES.I_d)

    # STEP 2
    # create  propensities
    # transition name: probability values
    # see doc/Propensities.pdf

    # compute P infection
    # first part omit
        # model.p * (
        #     model.beta * numI +
        #     model.q * model.beta_D * model.current_state_count(STATES.I_d)
        # ) / model.current_N()
        # + (1 - model.p)

    P1 = model.prob_of_contact(
        [STATES.S_s, STATES.S],
        [STATES.S,
         STATES.S_s,
         STATES.E,
         STATES.I_n,
         STATES.I_a,
         STATES.I_s],
        [STATES.I_n, STATES.I_a, STATES.I_s, STATES.I_d],
        [STATES.I_n, STATES.I_a, STATES.I_s, STATES.I_d, STATES.E],
        model.beta, model.beta_in_family
    )

    #    P2 = model.prob_of_no_contact([STATES.I_d], model.beta_D)
    assert(np.all(model.beta_D == 0))

    # print("-->", P1.shape, np.any(P1.flatten() > 0), np.all(P1.flatten() <= 1))
    # print(P2.flatten())
    # assert np.all(P2.flatten() == 0)

    #    P_infection = model.prob_of_no_contact(
    #        ([STATES.I_n, STATES.I_a, STATES.I_s], [STATES.I_d])
    #        (model.beta, model.beta_D)
    #    )
    #    print("-->", P_infection.shape, np.any(P_infection.flatten() > 0), np.all(P_infection.flatten() <= 1))

    N = model.current_N()
    numIn = model.current_state_count(
        STATES.I_a) + model.current_state_count(STATES.I_n)
    numI = model.current_state_count(
        STATES.I_s) + model.current_state_count(STATES.I_d)

    P2 = (model.beta * numI/N + model.beta_A * numIn/N)

    P_infection = (1-model.p)*P1 + model.p*P2

    #    print(P_infection.shape)

    not_P_infection = 1 - P_infection
    # assert np.all(P_infection < 1.0)
    # assert np.all((not_P_infection + P_infection) == 1)

    # print(model.memberships[STATES.S_s].shape)
    # print(P_infection.shape)
    # print(not_P_infection.shape)

    # print((model.memberships[STATES.S_s] * not_P_infection).shape)
    # exit()

    #    print(model.memberships[:, 0])
    # state S_s
    propensity_S_s_to_E = model.memberships[STATES.S_s] * P_infection
    propensity_S_s_to_S = (
        model.memberships[STATES.S_s] * not_P_infection * model.false_symptoms_recovery_rate)
    propensity_S_s_to_S_s = model.memberships[STATES.S_s] * \
        (1.0 - propensity_S_s_to_S - propensity_S_s_to_E)

    # print(propensity_S_s_to_E.flatten())
    # print(propensity_S_s_to_S.flatten())
    # print(propensity_S_s_to_S_s.flatten())
    # assert np.all((propensity_S_s_to_E + propensity_S_s_to_S +
    #                propensity_S_s_to_S_s)[np.nonzero(model.memberships[STATES.S_s])] == 1)

    # state S
    propensity_S_to_E = model.memberships[STATES.S] * P_infection
    propensity_S_to_S_s = (
        model.memberships[STATES.S] * not_P_infection * model.false_symptoms_rate)
    propensity_S_to_S = model.memberships[STATES.S] * \
        (1.0 - (propensity_S_to_E + propensity_S_to_S_s))

    #    print("S->E", propensity_S_to_E[0])
    #    print("S->Ss", propensity_S_to_S_s[0])
    #    print("E+Ss", (propensity_S_to_E + propensity_S_to_S_s)[0])
    #    print("E+Ss", (1.0 - (propensity_S_to_E + propensity_S_to_S_s))[0])
    #    print(model.memberships[STATES.S][0])
    #    print("S->S", propensity_S_to_S[0])

    # state E
    propensity_E_to_I_d = (model.memberships[STATES.E] *
                           model.theta_E * model.psi_E)
    propensity_E_to_I_n = (model.memberships[STATES.E] * (
        1.0 - propensity_E_to_I_d) * model.sigma * model.asymptomatic_rate)
    propensity_E_to_I_a = (model.memberships[STATES.E] *
                           (1.0 - propensity_E_to_I_d) * model.sigma *
                           (1.0 - model.asymptomatic_rate))
    propensity_E_to_E = model.memberships[STATES.E] * (1.0
                                                       - propensity_E_to_I_d
                                                       - propensity_E_to_I_n
                                                       - propensity_E_to_I_a)

    # state I_n
    propensity_I_n_to_R_u = model.memberships[STATES.I_n] * model.gamma_In
    propensity_I_n_to_I_d = (
        model.memberships[STATES.I_n] * (1.0 - model.gamma_In) * model.theta_In * model.psi_In)
    propensity_I_n_to_I_n = model.memberships[STATES.I_n] * \
        (1.0 - propensity_I_n_to_R_u - propensity_I_n_to_I_d)

    # state I_a
    propensity_I_a_to_I_d = (
        model.memberships[STATES.I_a] * model.theta_Ia * model.psi_Ia)
    propensity_I_a_to_I_s = (
        model.memberships[STATES.I_a] * (1.0 - propensity_I_a_to_I_d) * model.symptoms_manifest_rate)
    propensity_I_a_to_I_a = model.memberships[STATES.I_a] * \
        (1.0 - propensity_I_a_to_I_d - propensity_I_a_to_I_s)

    # state I_s
    propensity_I_s_to_R_u = (model.memberships[STATES.I_s] * model.gamma_Is)
    propensity_I_s_to_D_u = (model.memberships[STATES.I_s] * model.mu)
    not_R_or_D = 1.0 - propensity_I_s_to_R_u - propensity_I_s_to_D_u
    propensity_I_s_to_I_d = (
        model.memberships[STATES.I_s] * not_R_or_D * model.theta_Is * model.psi_Is)
    propensity_I_s_to_I_s = model.memberships[STATES.I_s] * (1.0 - propensity_I_s_to_R_u -
                                                             propensity_I_s_to_D_u - propensity_I_s_to_I_d)

    # state I_d
    propensity_I_d_to_R_d = model.memberships[STATES.I_d] * model.gamma_Id
    propensity_I_d_to_D_d = model.memberships[STATES.I_d] * model.mu
    propensity_I_d_to_I_d = model.memberships[STATES.I_d] * (
        1.0 - propensity_I_d_to_R_d - propensity_I_d_to_D_d)

    # state R_d, R_u, D_d, D_u
    propensity_R_d_to_R_d = model.memberships[STATES.R_d]
    propensity_R_u_to_R_u = model.memberships[STATES.R_u]
    propensity_D_d_to_D_d = model.memberships[STATES.D_d]
    propensity_D_u_to_D_u = model.memberships[STATES.D_u]

    return [
        propensity_S_s_to_E,
        propensity_S_s_to_S,
        propensity_S_s_to_S_s,

        propensity_S_to_E,
        propensity_S_to_S_s,
        propensity_S_to_S,

        propensity_E_to_I_d,
        propensity_E_to_I_n,
        propensity_E_to_I_a,
        propensity_E_to_E,

        propensity_I_n_to_R_u,
        propensity_I_n_to_I_d,
        propensity_I_n_to_I_n,

        propensity_I_a_to_I_d,
        propensity_I_a_to_I_s,
        propensity_I_a_to_I_a,

        propensity_I_s_to_R_u,
        propensity_I_s_to_D_u,
        propensity_I_s_to_I_d,
        propensity_I_s_to_I_s,

        propensity_I_d_to_R_d,
        propensity_I_d_to_D_d,
        propensity_I_d_to_I_d,
        propensity_R_d_to_R_d,
        propensity_R_u_to_R_u,
        propensity_D_d_to_D_d,
        propensity_D_u_to_D_u
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

TGMNetworkModel = create_custom_model("TGMNetworkModel",
                                      **model_definition,
                                      calc_propensities=calc_propensities,
                                      engine=EngineM)
