# model-m
Model of an imaginary town 

The model started as an extension of [seirsplus
model](https://github.com/ryansmcgee/seirsplus) adding more states. Later it
started to diverge by modifying the simulation cycle. Currently, the main
difference is the state-update only once a day and possibility of plugin callback
policy function that may modify the given graph (i.e. delete or weaken adges
for nodes in quarantine).  See [doc/model.pdf](doc/model.pdf) for more details

## Requirements 

networkx, numpy, matplotlib, seaborn, click



## Usage 
```
Usage: run_experiment.py [OPTIONS] [FILENAME] [TEST_ID]

  Run the demo test inside the timeit

Options:
  --set-random-seed / -r, --no-random-seed
  --print_interval INTEGER
  --help                          Show this message and exit.
```

See example .ini files romeo_and_juliet.ini (toy example) and seirsplus_example.ini (uses same
graph as examples in the seirsplus project)

```
(covid_env) (initial_experiments) petra@totoro:~/covid/model-m/tests$ python run_experiment.py -r romeo_and_juliet.ini
```

Output looks like:
(prints states overiew after the first event every day)
```
(covid_env) (initial_experiments) petra@totoro:~/covid/model-m/tests$ python romeo_and_juliet.py

N =  37
t = 0.03
	 S = 25
	 S_s = 5
	 E = 0
	 I_n = 2
	 I_a = 1
	 I_s = 4
	 I_d = 0
	 R_d = 0
	 R_u = 0
	 D_d = 0
	 D_u = 0

t = 1.11
	 S = 24
	 S_s = 6
	 E = 0
	 I_n = 2
	 I_a = 1
	 I_s = 3
	 I_d = 0
	 R_d = 0
	 R_u = 1
	 D_d = 0
	 D_u = 0

	.... 
	
t = 59.04
	 S = 13
	 S_s = 2
	 E = 0
	 I_n = 0
	 I_a = 0
	 I_s = 1
	 I_d = 0
	 R_d = 14
	 R_u = 7
	 D_d = 0
	 D_u = 0

t = 60.04
	 S = 12.0
	 S_s = 3.0
	 E = 0.0
	 I_n = 0.0
	 I_a = 0.0
	 I_s = 1.0
	 I_d = 0.0
	 R_d = 14.0
	 R_u = 7.0
	 D_d = 0.0
	 D_u = 0.0

Avg. number of events per day:  7.7
```


Or with more nodes:
```
(covid_env) (initial_experiments) petra@totoro:~/covid/model-m/tests$ python first_test.py 10000
t = 0.00
	 S = 7919
	 S_s = 1981
	 E = 0
	 I_n = 40
	 I_a = 20
	 I_s = 40
	 I_d = 0
	 R_d = 0
	 R_u = 0
	 D_d = 0
	 D_u = 0

...

t = 60.00
	 S = 6537
	 S_s = 1616
	 E = 155
	 I_n = 97
	 I_a = 15
	 I_s = 99
	 I_d = 263
	 R_d = 699
	 R_u = 515
	 D_d = 4
	 D_u = 0

Avg. number of events per day:  3039.8

```

## Saved history
You may wish to generate a novel from a model history. Output example: 

> Once upon a time ...<br>
> A gentleman Page stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Watchmen 1 stopped to be infectious without symptoms and started to be healthy again.<br>
> A gentleman Friar John stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Prince Escalus stopped to manifest symptoms and started to push up daisies.<br>
> A gentleman Paris stopped to have flue symptoms and started to be healthy.<br>
> A lady Lady Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Friar Lawrence stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Balthasar stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Lord Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Old Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Chorus stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Chorus stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Friar Lawrence stopped to have flue symptoms and started to be healthy.<br>
> A lady Rosaline stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Lord Capulet stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Gregory stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Balthasar stopped to manifest symptoms and started to push up daisies.<br>
> A lady Rosaline stopped to have flue symptoms and started to be healthy.<br>
> A lady Queen Mab stopped to manifest symptoms and started to push up daisies.<br>
> A gentleman Benvolio stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Mercutio stopped to manifest symptoms and started to be healthy again.<br>
> A gentleman Lord Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Lord Capulet stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Lord Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Friar John stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Benvolio stopped to be as famous as a taxidriver and started to pine for the fjords.<br>
> A gentleman Servant 2 stopped to be healthy and started to have flue symptoms.<br>
> A lady Nurse stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Servant 2 stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Servant 2 stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Servant 2 stopped to have flue symptoms and started to be healthy.<br>
> A lady Nurse stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Valentine stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Valentine stopped to have flue symptoms and started to be healthy.<br>
> A lady Nurse stopped to be healthy and started to have flue symptoms.<br>
> A lady Nurse stopped to have flue symptoms and started to be healthy.<br>
> A lady Lady Capulet stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Friar John stopped to be healthy and started to have flue symptoms.<br>
> A lady Lady Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Friar John stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Lord Capulet stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Lord Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Apothacary stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Apothacary stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Apothacary stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Apothacary stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Sampson stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Lord Capulet stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Abram stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Lord Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Sampson stopped to have flue symptoms and started to be healthy.<br>
> A lady Lady Capulet stopped to be healthy and started to have flue symptoms.<br>
> A lady Lady Capulet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Tybalt stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Tybalt stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Watchmen 2 stopped to be healthy and started to be exposed.<br>
> A gentleman Abram stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Paris stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Watchmen 3 stopped to be infectious without symptoms and started to be healthy again.<br>
> A gentleman Paris stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Page stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Watchmen 2 stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Page stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Watchmen 2 stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Watchmen 2 stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Peter stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Watchmen 2 stopped to be as famous as a taxidriver and started to pine for the fjords.<br>
> Well! I never wanted to do this in the first place. I wanted to be... an epidemiologist!<br>

## Config File Format
example.ini
```
[TASK]
num_nodes = 100
duration_in_days = 60

# print_interval  -  0:  do not print state counts during simulation
#                 -  N:  print every N-th day
print_interval = 0  

[MODEL]
beta = 0.155
sigma = 0.1923076923076923
gamma = 0.08071025020177562
mu_I = 0.0004
p = 0.2
beta_D = 0.155
gamma_D = 0.08071025020177562
mu_D = 0.0004
theta_E = 0.1
theta_Ia = 0.1
theta_Is = 0.1
phi_E = 0
phi_Ia = 0
phi_Is = 0
psi_E = 1.0
psi_Ia = 1.0
psi_Is = 1.0
q = 0.1
false_symptoms_rate = 0.2
asymptomatic_rate = 0.3
symptoms_manifest_rate = 0.9
initSSrate = 0.2
initE = 0
initI_n =  40
initI_a = 20
initI_s = 40
initI_d = 0
```

## Implementing custom network models

You can derive your customized network model.

```
import matplotlib.pyplot as plt
import numpy as np
from run_experiment import tell_the_story
from model import create_custom_model
from romeo_juliet_graph_gen import RomeoAndJuliet as Verona
from run_experiment import magic_formula
```

1. **Define whatever you need**
```
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
    propensities_list = [
        propensities[t] for t in model.transitions
    ]
    stacked_propensities = np.hstack(propensities_list)

    return stacked_propensities, model.transitions
```

2. **Create custom class**

```
CustomModel = create_custom_model("CustomModel", **model_definition,
                                  calc_propensities=calc_propensities)
```

3. **Load your graph**
```
g = Verona()
A = magic_formula(g.as_dict_of_graphs(), g.get_layers_info())
```

4. **Create model**
```
tiredability = 0.01 * np.array(g.get_attr_list("age"))
model = CustomModel(A,  wake_up_rate=0.8, init_alert=10, tiredability=tiredability,
                    init_tired=10, random_seed=35)
```

5. **Run**
```
ndays = 60
model.run(T=ndays, verbose=True, print_interval=5)
print("Avg. number of events per day: ", model.tidx/ndays)
```

6. **Inspect results**
```
x = model.tseries
population = model.N
alert = model.state_counts["alert"]
plt.plot(x, population, label="population")
plt.plot(x, alert, label="alert population")
plt.legend()
plt.savefig("alert_pop.png")
# etc
```
7. **Procrastinate**
```
# text = tell_the_story(model.history, g)
# print()
```
