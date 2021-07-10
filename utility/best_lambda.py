# -*- coding: utf-8 -*-

import csv
import pandas as pd
from simulator.simulation import simulation
import math
import random
from collections import Counter
import matplotlib.pyplot as plt

# This method, given the real h and T, finds the optimal lambda in such way that
# the death rate among ill nodes is maximized. The optimal lambda value is returned.
def find_optimal_lambda(instance, best_lambda_settings, h_real, T_max_real, patient_zero_degree=None, first_node=None):
    
    # Create csv file and its header. Each line of the csv file is relative
    # to a different simulation characterized with a different triplet (h, T, lambda).
    csv_file = "./csv_folder/lambda_search.csv"
    
    csv_columns = ["node", \
               "best_lambda", \
               "h", \
               "T_max", \
               "total_healthy", \
               "total_ill", \
               "total_dead", \
               "total_recovered"]
    
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
    # Create a local Dataframe to store the intermediate results and for
    # further analysis.
    df = pd.DataFrame(columns = csv_columns)
    
    # Name of the log file.
    log_file = "lambdasearch_log" 
    
    lambdas_opt=[]
    dead=[]
    pl = instance.pl
    
    # List of nodes of a certain degree
    neighbors_id = []
    for node in pl:
        if node.degree_cat == patient_zero_degree:
            neighbors_id.append(node.id)
            
            
    # Choosing k nodes
    num=math.floor(0.2*len(neighbors_id))
    nodes_list=random.choices(neighbors_id, k=num)
    print("total iterations: ", num)
        
    
    #i=0
    for node in nodes_list:
        # Init. empty DataFrame for each node
        df = pd.DataFrame(columns = csv_columns)
        for lambd in best_lambda_settings["lambda_range"]:
            # Since the search for the optimal lambda is based on a list of nodes, we do not pass "patient_zero_degre" as input to SImulation (we just pass the first node's id).
            results = simulation(log_file, best_lambda_settings, lambd, h_real, T_max_real, pl, instance.SIM_LIM, first_node_id=node, flag_optimal=True, flag_final_simulation=False)
            # Appending the intermediate results in a local DF.
            df = df.append(results, ignore_index=True)
            # Saving the intermediate results of each simulation in the csv file would be too much (we would need 300 csv files!).
            
        #if i%25==0:
            #print("it: ",i)
        #i+=1
        
        
        # Results are stored in two lists and a csv is created containg the info for the best lambda for each node.
        # Select the lambda that caused more deaths for the i-th starting node.
        lambda_i=df[df.total_dead == df.total_dead.max()]["lambda"].to_numpy()[0]
        dead_i=df[df.total_dead == df.total_dead.max()]["total_dead"].to_numpy()[0]
        lambdas_opt.append(lambda_i)
        dead.append(dead_i)
        # Dict. to be stored in the csv with the results for the optimal lambda.
        result={"node": node, \
                   "best_lambda":lambda_i, \
                   "h":h_real, \
                   "T_max":T_max_real, \
                   "total_healthy":df[df.total_dead == df.total_dead.max()]["total_healthy"].to_numpy()[0], \
                   "total_ill":df[df.total_dead == df.total_dead.max()]["total_ill"].to_numpy()[0], \
                   "total_dead":dead_i, \
                   "total_recovered":df[df.total_dead == df.total_dead.max()]["total_recovered"].to_numpy()[0]}
        
        try:
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(result)
        except IOError:
            print("I/O error")
    
    # Maximum number of dead among the simulations on all the nodes in the list and respective optimal lambda.
    print("patient zero category: ",patient_zero_degree)
    #max_value = max(dead)
    #i=dead.index(max_value)
    #print("max value of deaths is ", max_value, ", for lambda=", lambdas_opt[i])
    
    # Counting the most frequent lambdas
    def most_frequent(List):
        occurence_count = Counter(List)
        return occurence_count.most_common(5)
        
    most_seen=most_frequent(lambdas_opt)
    lambda_opt=most_seen[0][0]
    #print("Most frequent best lambdas: ", most_seen)
    print("Most frequent best lambda is lambda=", lambda_opt, ". Number of occurernces: ", most_seen[0][1])
    most_dead=[]
    index=0
    for x in lambdas_opt:
    	if x==lambda_opt:
    		most_dead.append(dead[index])
    	index+=1
    max_value=max(most_dead)
    print("max value of deaths is ", max_value, ", for lambda=", lambda_opt)
    tot=0
    sizes=[]
    labels=[]

    for l in most_seen:
    	tot+=l[1]
    	sizes.append(100*l[1]/num)
    	labels.append("l="+str(l[0]))

    sizes.append(num-tot)
    labels.append("l=others")

    plt.pie(sizes, autopct='%1.1f%%')
    plt.legend(labels)
    plt.show()


    
    
    return lambda_opt
