# -*- coding: utf-8 -*-

import csv
import pandas as pd
from simulator.simulation import final_simulation

# This method, given the real h and T and optimal lambda, observes the behaviour 
# of the network. It returns two DataFrames, one containing the statistics of the
# final simulation, the other the evolution over time of the simulation in order to plot it.
def final_network_simulation(instance, h_real, T_max_real, lambd, patient_zero_degree=None, first_node=None):
    
    # Create csv file and its header.
    csv_file = "./csv_folder/final_network_behaviour.csv"
    csv_columns = ["N_nodes", \
                   "lambda", \
                   "h", \
                   "T_max", \
                   "total_healthy", \
                   "total_contagious", \
                   "total_ill", \
                   "total_dead", \
                   "total_recovered"]
    
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
    # Create a local Dataframe to store the simulation results, in particular,
    # the amount of healthy, contagious, ill, dead and recovered nodes.
    df_final_results = pd.DataFrame(columns = csv_columns)
    
    # Name of the log file.
    log_file = "final_network_behaviour_log"
    
    # Launching the final simulation.
    pl = instance.pl
    results, df_plot = final_simulation(log_file, lambd, h_real, T_max_real, pl, instance.SIM_LIM, patient_zero_degree, first_node)
    df_final_results = df_final_results.append(results, ignore_index=True)
    
    # Saving the csv file.
    try:
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerow(results)
    except IOError:
        print("I/O error")
    
    return df_final_results, df_plot
