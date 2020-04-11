# -*- coding: utf-8 -*-

import random

from engine import BaseEngine


# constants for Models
TIME_OF_SIMULATION = 30
NUMBER_OF_PEOPLE = 10

# constants for Person
HEALTHY = 0
INFECTED = 1
TIME_OF_INFECTION = 3
AVG_CONTACTS = 3
TRANS_RATE = 0.8


# constants for SEIRPerson
SUSCEPTIBLE = 0
EXPOSED = 1
INFECTIOUS = 2
RECOVERED = 3
DEAD = 4
# β: rate of transmission (transmissions per S-I contact per time)
# σ: rate of progression (inverse of incubation period)
# γ: rate of recovery (inverse of infectious period)
# ξ: rate of re-susceptibility (inverse of temporary immunity period; 0 if permanent immunity)
# μI: rate of mortality from the disease (deaths per infectious individual per time)
BETA = 0.5
SIGMA = 0.5
GAMMA = 0.05
XI = 0
MJU_I = 0.01
MJU_ALL = 0.00003 # 11 ppl per 1000 ppl per year ... 3 ppl per day per 100k ppl

class Person():
    def __init__ (self, id, init_state=HEALTHY):
        self.state = init_state
        self.time_of_state = 0
        self.id = id
        
    def infect(self, by_whom):
        self.state = INFECTED
        self.time_of_state = 0
        if by_whom == -1:
            print(self.id, " infected initially")
        else:
            print(self.id, " infected by", by_whom)

    def heal(self):
        self.state = HEALTHY
        self.time_of_state = 0
        print(self.id, " is healed")
        
    def stay_infected(self):
        self.time_of_state += 1
        if self.time_of_state == TIME_OF_INFECTION:
            self.heal()
            
    def stay_healthy(self):
        self.time_of_state += 1
         
class SEIRSPerson(Person):
    def __init__ (self, id, init_state=SUSCEPTIBLE):
        super.__init(self, id, init_state)
        
    


class NoModel(BaseEngine):

    def __init__ (self, number_of_people = NUMBER_OF_PEOPLE, number_of_infected = 1, avg_contacts = AVG_CONTACTS, avg_trans= TRANS_RATE):
        self.N = number_of_people
        self.Ni = number_of_infected
        self.contacts_per_day = avg_contacts
        self.transmission_rate = avg_trans
        
        self.People = []
        inf_idx = random.sample(range(self.N),self.Ni)
        for p in range(self.N):
            new_person = Person(p)
            if p in inf_idx: 
                new_person.infect(-1)
            else:
                new_person.heal()                
            self.People.append(new_person)  
    
    def is_it_transmission(self, a, b):
        # ignore everything, just toss a coin with transmission_rate if b is infected
        if b.state == HEALTHY:
            return False
        else:
            if random.random() < self.transmission_rate:
                return True
            else:
                return False

    def run_iteration(self):
        for p in self.People:
            if p.state == HEALTHY:
                contacts = random.sample(range(self.N),self.contacts_per_day)
                for c in contacts:
                    if self.is_it_transmission(p,self.People[c]):
                        p.infect(c)
            if p.state == INFECTED:
                p.stay_infected()                            
    
    def run(self, T=TIME_OF_SIMULATION):
        for self.t in range(1, T+1):
            print("t = %.2f" % self.t)
            self.run_iteration()

class NoSEIRSModel(NoModel):
    def __init__(self, number_of_people = NUMBER_OF_PEOPLE):
        super.__init__(self)    
 
class NoGraphModel(NoModel):
    def __init__ (self, graph, **kwargs):
        super().__init__(**kwargs)
        self.G = graph

m = NoModel()
m.run()        