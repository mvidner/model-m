# -*- coding: utf-8 -*-


from engine import BaseEngine

from bisect import bisect_left
from itertools import accumulate
import random

# constants for Models

MAGIC_SEED_BY_PETRA = 42
TIME_OF_SIMULATION = 30
NUMBER_OF_PEOPLE = 10
NUMBER_OF_INFECTED = 3

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
FATAL = 4

SEIRSNAMES = [ 'S', 'E', 'I', 'R', 'F' ]

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
        self.state = init_state
        self.time_of_state = 0
        self.id = id
        
    def get_state(self):
        return self.state

    def set_state(self, s=SUSCEPTIBLE):
        old_state = self.state
        self.state = s
        print (self.id, ':', SEIRSNAMES[old_state], '->', SEIRSNAMES[s])
        
    def prob_change_state(self, probs):
        su = sum(probs)
        if su < 1 :
            probs[self.state] = 1 - su
        cum_p   = list(accumulate(probs))
        total_p = cum_p[-1]
        value = random.random() * total_p
        new_state = bisect_left(cum_p, value)
        if new_state != self.state :
            self.set_state(new_state)


class NoModel(BaseEngine):

    def __init__(self, T_time=TIME_OF_SIMULATION, number_of_people=NUMBER_OF_PEOPLE, number_of_infected=NUMBER_OF_INFECTED, avg_contacts=AVG_CONTACTS, avg_trans=TRANS_RATE,
                 random_seed=42):

        if random_seed:
            random.seed(random_seed)

        self.N = number_of_people
        self.Ni = number_of_infected
        self.contacts_per_day = avg_contacts
        self.transmission_rate = avg_trans
        self.T = T_time

        self.People = []
        inf_idx = random.sample(range(self.N), self.Ni)
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
    def do_statistics(self):
        print("t = %.2f" % self.t)
        
    def run_iteration(self):
        for p in self.People:
            if p.state == HEALTHY:
                contacts = random.sample(range(self.N), self.contacts_per_day)
                for c in contacts:
                    if self.is_it_transmission(p, self.People[c]):
                        p.infect(c)
            if p.state == INFECTED:
                p.stay_infected()

    def run(self):
        for self.t in range(1, self.T + 1):
            self.do_statistics()
            self.run_iteration()

class NoSEIRSModel(NoModel):
    def __init__(self, T_time=TIME_OF_SIMULATION, number_of_people=NUMBER_OF_PEOPLE, number_of_infected=NUMBER_OF_INFECTED, prob=1, beta=BETA, sigma=SIGMA, gamma=GAMMA, xi=XI, mju_i=MJU_I,
                 random_seed=MAGIC_SEED_BY_PETRA):

        if random_seed:
            random.seed(random_seed)

        self.N = number_of_people
        self.Ni = number_of_infected
        self.p = prob
        self.beta = beta
        self.sigma = sigma
        self.gamma = gamma
        self.xi = xi
        self.mju_i = mju_i
        self.T = T_time
        self.People = []
        inf_idx = random.sample(range(self.N), self.Ni)
        for p in range(self.N):
            new_person = SEIRSPerson(p)
            if p in inf_idx:
                new_person.set_state(INFECTIOUS)
            else:
                new_person.set_state(SUSCEPTIBLE)
            self.People.append(new_person)
 
    def run_iteration(self):
        inf_p = [ x for x in self.People if x.get_state() == INFECTIOUS ]
        self.Ni = len(inf_p)
        
        for p in self.People:
            probs = [0, 0, 0, 0, 0]
            if p.state == SUSCEPTIBLE:
                probs[EXPOSED] = self.beta * self.Ni / self.N
#                print (self.beta * self.Ni / self.N)
            if p.state == EXPOSED:
                probs[INFECTIOUS] = self.sigma
            if p.state == INFECTIOUS:
                probs[RECOVERED] = self.gamma
                probs[FATAL] = self.mju_i
            if p.state == RECOVERED:
                probs[SUSCEPTIBLE] = self.xi
            p.prob_change_state(probs)    
    
 
class NoGraphModel(NoModel):
    def __init__ (self, graph, **kwargs):
        super().__init__(**kwargs)
        self.G = graph

if __name__ == "__main__":
    m = NoSEIRSModel(100, 100, 30)
    m.run()
