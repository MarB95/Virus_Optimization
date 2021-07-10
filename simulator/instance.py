# -*- coding: utf-8 -*-

import logging
import math

# The class to generate an Instance object of the problem.
class Instance():
    def __init__(self, G, nodes_list, simulation_settin):
        
        self.SIM_LIM = simulation_settin['SIM_LIM']
        self.G = G
        self.pl = nodes_list
        
        # Adding the drawn parameters values to the log file of the main.
        logging.info("Parameters of the simulation:")
        logging.info(f"n_nodes: {self.G.number_of_nodes()}")
        logging.info(f"SIM_LIM: {self.SIM_LIM}")
    
    # To evaluate average and standard deviation of the node degree for the whole graph. 
    def getMeanStdGraphDegree(self):
        logging.info("getting mean and std of the node graph degree from instance...")
        tot = 0
        for person in self.pl:
            tot = tot + len(person.neighborhood)
        self.degree_mean = round(tot / len(self.pl),2)
        tot = 0
        for person in self.pl:
            tot = tot + abs(pow(len(person.neighborhood) - self.degree_mean, 2))
        self.degree_std = round(math.sqrt(tot/len(self.pl)),2)
        
        logging.info(f"Graph degree average: {self.degree_mean}")
        logging.info(f"Graph degree std: {self.degree_std}")
        return self.degree_mean, self.degree_std