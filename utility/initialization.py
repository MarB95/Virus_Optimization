# -*- coding: utf-8 -*-

import logging
import os
import networkx as nx
import json
import pickle
import random
import matplotlib.pyplot as plt
import numpy as np
from person import Person

# Get main script path on local machine.
cwd = os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(cwd)

# Reading the simulation setting json file containing the graph properties.
fp = open(path+"/etc/graph_setting.json", 'r')
graph_setting = json.load(fp)["small_graph_low_deg"]
fp.close()

# Reading the simulation setting json file containing the nodes' properties.
fp = open(path+"/etc/nodes_setting.json", 'r')
nodes_setting = json.load(fp)
fp.close()

# Parameters to generate and populate the graph.
nodes = graph_setting['N_nodes']
prob_matrix = graph_setting['prob_matrix']
# Defining the empty list of nodes.
pl = []

# Defining the groups and generating the stochastic graph G with the proper parameters.
group_1 = int(nodes*graph_setting['pop_group_1'])
group_2 = int(nodes*graph_setting['pop_group_2'])
group_3 = nodes - group_1 - group_2
sizes = [group_1, group_2, group_3]
G = nx.stochastic_block_model(sizes, prob_matrix, seed=graph_setting['seed'])

# Finding the list of nodes of the graph.
list_of_nodes = list(G.nodes())
        
# Forcing the isolated nodes to connect to 3 random nodes in the graph,
# the nodes with 1 neighbor to other 2 nodes and the node with 2 neighbor
# with another node. In this way, every node in the graph is going to have
# at least 3 neighbors.

if graph_setting["id"] == "small_graph_high_deg" or \
    graph_setting["id"] == "small_graph_low_deg" or\
    graph_setting["id"] == "small_graph":
    for node in list(G.nodes()):
        if len(list(G.neighbors(node))) == 0:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=3)]
        elif len(list(G.neighbors(node))) == 1:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=2)]
        elif len(list(G.neighbors(node))) == 2:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=1)]
        
elif graph_setting["id"] == "big_graph":
    for node in list(G.nodes()):
        if len(list(G.neighbors(node))) == 0:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=6)]
        elif len(list(G.neighbors(node))) == 1:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=5)]
        elif len(list(G.neighbors(node))) == 2:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=4)]
        elif len(list(G.neighbors(node))) == 3:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=3)]
        elif len(list(G.neighbors(node))) == 4:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=2)]
        elif len(list(G.neighbors(node))) == 5:
            available_ids = [id for id in list_of_nodes if id not in list(G.neighbors(node))]
            [G.add_edge(node, x) for x in random.choices(available_ids, k=1)]
        
# Initialize the Person (nodes) objects.
for node in range(len(G)):
    neighbors = list(G.neighbors(node))
    pl.append(Person(node, \
                     nodes_setting['infecting_P_a'], \
                     nodes_setting['infecting_P_b'], \
                     nodes_setting['death_P_a'], \
                     nodes_setting['death_P_b'], \
                     neighbors))

# Once the nodes of the graph are initialized, the degree category of each node
# is found. In order to do so, all the possible neighborhood sizes in the graph
# are stored in a list and then sorted from smallest to greater value.
node_degrees = []
for node in pl:
    if len(node.neighborhood) not in node_degrees:
        node_degrees.append(len(node.neighborhood))
node_degrees.sort()

# Then, the list of neighborhood sizes is subdivided into five portions (with
# approximately equal size, supposing the number of nodes is larger than 5).
# The first portion includes the smallest neighborhood sizes, while the last 
# portion includes the largest neighborhood sizes. The node degree category 
# is assigned to each node accordingly.
size = int(len(node_degrees)/5)
for node in pl:
    if len(node.neighborhood) in node_degrees[0:size]:
        node.degree_cat = "VERY LOW"
    elif len(node.neighborhood) in node_degrees[size:2*size]:
        node.degree_cat = "LOW"
    elif len(node.neighborhood) in node_degrees[2*size:3*size]:
        node.degree_cat = "MEDIUM"
    elif len(node.neighborhood) in node_degrees[3*size:4*size]:
        node.degree_cat = "HIGH"
    elif len(node.neighborhood) in node_degrees[4*size:len(node_degrees)]:
        node.degree_cat = "VERY HIGH"
        
        
# Adding the parameters drawn values to the log file of the main.
logging.info("Parameters of the simulation:")
logging.info(f"n_nodes: {nodes}")
logging.info(f"edge_probability: {prob_matrix}")

# Plotting the instance stochastic graph G.
fig = plt.figure(figsize=(18,15))
nx.draw(G, with_labels=True, node_size=100, font_color='white')

for node in pl:
    if len(node.neighborhood) == 2:
        print(node.id)

# Plotting node degree histogram.
degrees = [len(node.neighborhood) for node in pl]
fig2 = plt.figure(figsize=(18,15))
labels, counts = np.unique(degrees, return_counts=True)
plt.bar(labels, counts, align='center')
plt.gca().set_xticks(labels)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("Node degree", fontsize=20)
plt.ylabel("Number of nodes", fontsize=20)

# Saving the variable G (the generated graph) to be used in the main.
with open(path+'/pickle files/'+graph_setting["id"]+'.pkl', 'wb') as f:
    pickle.dump([G, pl], f)
