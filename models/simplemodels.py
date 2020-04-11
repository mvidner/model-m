# -*- coding: utf-8 -*-

import random

from engine import BaseEngine


HEALTHY = 0
INFECTED = 1
TIME_OF_INFECTION = 3
AVG_CONTACTS = 3
TRANS_RATE = 0.8
TIME_OF_SIMULATION = 30

class Person():
    def __init__(self, id, init_state=HEALTHY):
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
         

class NoModel(BaseEngine):

    def __init__(self, number_of_people = 10, number_of_infected = 1, avg_contacts = AVG_CONTACTS, avg_trans= TRANS_RATE):
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

 

m = NoModel()
m.run()        