"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0

        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.qTable = np.random.uniform(low=-1.0, high=1.0, size=(num_states, num_actions))

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if np.random.random_sample() < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = self.qTable[self.s, :].argmax()

        self.a = action

        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        self.rar *= self.radr
        self.qTable[self.s,self.a] = (1 - self.alpha) * self.qTable[self.s,self.a] + \
                                     self.alpha * (r + self.gamma * self.qTable[s_prime,self.qTable[s_prime,:].argmax()])

        if np.random.random_sample() < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = self.qTable[s_prime, :].argmax()

        self.s = s_prime
        self.a = action

        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
