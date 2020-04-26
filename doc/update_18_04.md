# Update 18. 4. 2020 

- engine rewritten and optimised (need to fix policies - in progress)
- new version of Hodonin works - **1 minute per 300 days run without policy change**

Je třeba doladit pravděpodobnosti, ale nová verze je blíž původní seirsplus (s našimi stavy) 
než varianta s překlápěním po dnech.


![](https://paper-attachments.dropbox.com/s_D4FB80FB074A6BA2A23524F928967AAA3F92E9AB70FCFED18569776506998E69_1587233262321_alg_compare.png)


**Časy na hakld** (nejpomalejší ze 3 clusterů co máme, ale ariel ucpali Rkaři)
(časy jsou bez policy, ty je třeba doladit a overhead bude stejnej všude,
vzdycky 10 behu vedle sebe, bezi to pomalejc nez 1 (i kdyz je tam 64 procesoru - asi kvuli pristupum na disk (printy do souboru)?))

|                | original           | daily update of states | **daily sequential** |                  |
| -------------- | ------------------ | ---------------------- | -------------------- | ---------------- |
| load grafu     | 77.78 (std 3.42)   | 78.46 (std 4.50)       | 78.49 (std 4.22)     | (dela se stejne) |
| den            | 324.89 (std 25.27) | 1.56 (std 0.51)        | 0.16 (std  0.01)     |                  |
| total 300 days | NA                 | 616.81 (std 24.74)     | 128.70 (std 7.49)    |                  |

Na **arielu** daily sequential celkový čas **60.49** (std 1.24), 10x vedle sebe. Druhé dvě verze 
nemám, pač kolegové statistici ucpali frontu 🙂 

Ladění parametrů bez policy by mělo být OK, minuta na celkový běh (300 dní).  [v tomhle případě za minutu 10 běhů, jelo to na 10 processorech]. 

**Algoritmy**
Original - převzatý z seirsplus (original)


     t = 0
     while True:
         propensities = calculate_propensties() 
         alpha = propensities.sum() 
         r = rand()
         # Compute the time until the next event takes place
         tau = (1/alpha) * log(float(1/r))
         t += tau  
         # Compute which event takes place
         transition_node, transition_type = select(propensities) 
         # Update node states and data series
         update_states(transition_node, transition_type) 

Daily modifikace  (daily update of states)

     t = 0
     todo_list = [] 
     while True:
         propensities = calculate_propensties() 
         alpha = propensities.sum() 
         r = rand()
         
         # Compute the time until the next event takes place
         tau = (1/alpha) * log(float(1/r))
         t += tau  
         
         # Compute which event takes place
         transition_node, transition_type = select(propensities) 
         todo_list.append((transition_node, transition_type)) 
         
         if day_changed:      
             # Update node states and data series
             for transition_node, transition_type in todo_list:
                 update_states(transition_node, transition_type) 

Aktuální sekvenční “Romanovo” verze  (daily sequential)

    for t in 1, ... , T: 
         propensities = calculate_propensities()
         # for each node select one action (including X->X) based on propensities[node_id]
         trainsitions = select_transitions(propensities)
         # update node states according selected transitions
         update_states(transitions)        
# Fitování 
- našla jsem několik python knihoven na ABC
- nejlíp se mi jeví **ABCpy** https://abcpy.readthedocs.io/en/v0.5.7/


