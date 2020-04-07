# models

# model = engine + model definition

# engine is not cofigurable yet
# you can specify your model definition

extended_network_model_definition = {
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
