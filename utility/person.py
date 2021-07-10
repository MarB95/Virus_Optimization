# -*- coding: utf-8 -*-

import numpy as np

# Each node will be a Person. This class will be used to initialize the nodes
# parameters which will be the inputs to the simulation.
class Person:

    def __init__(self, id, a_infect, b_infect, a_death, b_death, neighbors):
        #Identifier of the Node/Person in the graph.
        self.id = id
        # Starting state of the Node/Person.
        self.state = "HEALTHY"
        ''' Possible states of a node/Person:
            "HEALTHY"
            "CONTAGIOUS"
            "ILL"
            "RECOVERED"
            "DEAD"
        '''
        # Setting alpha and beta which influence, respectively, the probability to infect p 
        # and probabilitiy to die q. Alpha and beta are drawn from two
        # distinct Beta distributions, each one characterized by their own parameters.
        self.alpha = np.random.beta(a_infect, b_infect, size=None)
        self.beta = np.random.beta(a_death, b_death, size=None)
        # Probability p to infect neighbors, zero when the person is healthy.
        self.p = 0
        # Probability q to die because of the virus, zero when the person is healthy.
        self.q = 0
        # The node's neighbourhood is populated according to the generated Graph.
        self.neighborhood = neighbors
        # Local timestamps.
        self.t = -1
        # Local timestamps to heal.
        self.t_ill = -1
        # Current viral quantity for the person, 0 at the beginning.
        self.viral_q = 0
        # The category of degree of the node. According to the amount of neighbors
        # of the node, the degree category of the node will change as follows.
        self.degree_cat = ""
        ''' Possible degree categories of a node/Person:
            "VERY LOW"
            "LOW"
            "MEDIUM"
            "HIGH"
            "VERY HIGH"
        '''