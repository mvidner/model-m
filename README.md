# model-m
Model of an imaginary town 

## Requirements 

networkx, numpy, matplotlib, seaborn, click

## Warning 
now we are living in initial_experiments branch 


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
You may with to generate a novel from a model history. Output example: 

> Once upon a time ...<br>
> A gentleman Anthony stopped to be symptomatic and infectious with no  manifest of symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Tybalt stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Lord Capulet stopped to have flue symptoms and started to be healthy.<br>
> A lady Rosaline stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Abram stopped to be infectious without symptoms and started to be healthy again.<br>
> A gentleman Balthasar stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Apothacary stopped to be infectious without symptoms and started to be healthy again.<br>
> A gentleman Old Capulet stopped to be healthy and started to be exposed.<br>
> A gentleman Gregory stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Anthony stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Watchmen 1 stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Servant 2 stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Servant 2 stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Watchmen 1 stopped to have flue symptoms and started to be healthy.<br>
> A lady Lady Capulet stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Old Capulet stopped to be exposed and started to be as famous as a taxidriver.<br>
> A lady Lady Capulet stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Balthasar stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A lady Juliet stopped to be healthy and started to have flue symptoms.<br>
> A lady Lady Montague stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Valentine stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Lord Montague stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Old Capulet stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Servant 2 stopped to be healthy and started to be exposed.<br>
> A lady Juliet stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Friar Lawrence stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Friar Lawrence stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Peter stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Gregory stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Servant 2 stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Peter stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Servant 2 stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Valentine stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Gregory stopped to have flue symptoms and started to be healthy.<br>
> A lady Juliet stopped to be healthy and started to be exposed.<br>
> A gentleman Friar Lawrence stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Prince Escalus stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Romeo stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Tybalt stopped to be healthy and started to be exposed.<br>
> A gentleman Romeo stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Prince Escalus stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Servant 2 stopped to manifest symptoms and started to be healthy again.<br>
> A gentleman Friar Lawrence stopped to have flue symptoms and started to be healthy.<br>
> A lady Juliet stopped to be exposed and started to be as famous as a taxidriver.<br>
> A gentleman Valentine stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Musician 3 stopped to be healthy and started to be exposed.<br>
> A gentleman Valentine stopped to have flue symptoms and started to be healthy.<br>
> A lady Rosaline stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Friar Lawrence stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Musician 3 stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Musician 1 stopped to be healthy and started to be exposed.<br>
> A gentleman Valentine stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Watchmen 3 stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Peter stopped to be healthy and started to be exposed.<br>
> A lady Nurse stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Chorus stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Mercutio stopped to manifest symptoms and started to be healthy again.<br>
> A gentleman Friar John stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Musician 3 stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Friar Lawrence stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Chorus stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Watchmen 3 stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Tybalt stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Ghost Petruchio stopped to be healthy and started to have flue symptoms.<br>
> A lady Nurse stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Ghost Petruchio stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Friar John stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Tybalt stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Valentine stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Friar Lawrence stopped to be healthy and started to be exposed.<br>
> A gentleman Potpan stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Friar Lawrence stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Tybalt stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Friar Lawrence stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Potpan stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Musician 2 stopped to be healthy and started to be exposed.<br>
> A gentleman Musician 1 stopped to be exposed and started to be infectious without symptoms.<br>
> A gentleman Peter stopped to be exposed and started to be as famous as a taxidriver.<br>
> A gentleman Potpan stopped to be healthy and started to be exposed.<br>
> A gentleman Musician 3 stopped to manifest symptoms and started to be healthy again.<br>
> A gentleman Potpan stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Servant 1 stopped to be healthy and started to be exposed.<br>
> A gentleman Friar Lawrence stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Potpan stopped to be symptomatic and infectious with no  manifest of symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Potpan stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Friar Lawrence stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A lady Rosaline stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Romeo stopped to be healthy and started to be exposed.<br>
> A gentleman Friar John stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Peter stopped to be as famous as a taxidriver and started to pine for the fjords.<br>
> A gentleman Friar John stopped to have flue symptoms and started to be healthy.<br>
> A lady Juliet stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Romeo stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Musician 2 stopped to be exposed and started to be infectious without symptoms.<br>
> A gentleman Tybalt stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Ghost Petruchio stopped to be healthy and started to be exposed.<br>
> A gentleman Paris stopped to be healthy and started to be exposed.<br>
> A gentleman Servant 1 stopped to be exposed and started to be as famous as a taxidriver.<br>
> A gentleman Paris stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A lady Lady Montague stopped to be healthy and started to be exposed.<br>
> A gentleman Lord Montague stopped to be healthy and started to be exposed.<br>
> A gentleman Benvolio stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Servant 1 stopped to be as famous as a taxidriver and started to pine for the fjords.<br>
> A gentleman Benvolio stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Paris stopped to be symptomatic and infectious with no  manifest of symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Lord Capulet stopped to be healthy and started to be exposed.<br>
> A gentleman Lord Capulet stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Lord Capulet stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Benvolio stopped to be healthy and started to have flue symptoms.<br>
> A lady Rosaline stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Romeo stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Watchmen 1 stopped to be healthy and started to have flue symptoms.<br>
> A lady Rosaline stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Lord Montague stopped to be exposed and started to be as famous as a taxidriver.<br>
> A gentleman Watchmen 1 stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Sampson stopped to be healthy and started to be exposed.<br>
> A gentleman Benvolio stopped to have flue symptoms and started to be healthy.<br>
> A gentleman Valentine stopped to be healthy and started to be exposed.<br>
> A gentleman Lord Capulet stopped to manifest symptoms and started to be healthy again.<br>
> A gentleman Gregory stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Ghost Petruchio stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Gregory stopped to have flue symptoms and started to be healthy.<br>
> A lady Lady Montague stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A lady Lady Montague stopped to be symptomatic and infectious with no  manifest of symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Ghost Petruchio stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Chorus stopped to be healthy and started to be exposed.<br>
> A gentleman Prince Escalus stopped to be healthy and started to be exposed.<br>
> A gentleman Prince Escalus stopped to be exposed and started to be infectious without symptoms.<br>
> A gentleman Chorus stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Chorus stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Romeo stopped to manifest symptoms and started to be healthy again.<br>
> A gentleman Ghost Petruchio stopped to manifest symptoms and started to be healthy again.<br>
> A gentleman Valentine stopped to be exposed and started to be as famous as a taxidriver.<br>
> A gentleman Page stopped to be healthy and started to be exposed.<br>
> A gentleman Paris stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Lord Montague stopped to be as famous as a taxidriver and started to pine for the fjords.<br>
> A gentleman Page stopped to be exposed and started to be infectious without symptoms.<br>
> A gentleman Prince Escalus stopped to be infectious without symptoms and started to be healthy again.<br>
> A gentleman Watchmen 1 stopped to be healthy and started to have flue symptoms.<br>
> A gentleman Chorus stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Gregory stopped to be healthy and started to be exposed.<br>
> A gentleman Gregory stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Gregory stopped to be symptomatic and infectious with no  manifest of symptoms and started to manifest symptoms.<br>
> A gentleman Gregory stopped to manifest symptoms and started to be as famous as a taxidriver.<br>
> A gentleman Sampson stopped to be exposed and started to be as famous as a taxidriver.<br>
> A gentleman Page stopped to be infectious without symptoms and started to be healthy again.<br>
> A gentleman Sampson stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Chorus stopped to be as famous as a taxidriver and started to be an expert on epidemy.<br>
> A gentleman Watchmen 3 stopped to be healthy and started to be exposed.<br>
> A gentleman Watchmen 3 stopped to be exposed and started to be symptomatic and infectious with no  manifest of symptoms.<br>
> A gentleman Watchmen 1 stopped to have flue symptoms and started to be healthy.<br>
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

