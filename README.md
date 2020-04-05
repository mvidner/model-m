# model-m
Model of an imaginary town 

## Requirements 

networkx, numpy, matplotlib, seaborn, click, (graphviz)

## Warning 
now we are living in initial_experiments branch 


## Usage 
 - example with graph from seirsplus examples 
```
python first_test.py [N_NODES] 
```

- example with Verona city (graph with layers)
```
python romeo_and_juliet.py 
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
