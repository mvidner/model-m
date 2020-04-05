# model-m
Model of an imaginary town 

## Requirements 

networkx, numpy, matplotlib, seaborn, click, (graphviz)

## Warning 
now we are living in initial_experiments branch 


## Usage 

- example with graph from seirsplus examples 
```
$ python first_test.py 10000
$ python first_test.py --help
Usage: first_test.py [OPTIONS] [N_NODES] [TEST_ID]

Options:
  --set-random-seed / -r, --no-random-seed
  --help                          Show this message and exit.

```
- or using .ini file (so far with seirsplus exmaple graph,
 but intended for future usage)

```
Usage: run_experiment.py [OPTIONS] [FILENAME] [TEST_ID]

Options:
  --set-random-seed / -r, --no-random-seed
  --print_interval INTEGER
  --help                          Show this message and exit.

i.e. python run_experiment.py -r example.ini 
```

- example with Verona city (graph with layers)
```
$ python romeo_and_juliet.py 
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

