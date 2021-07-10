# -*- coding: utf-8 -*-

import csv
import pandas as pd
import numpy as np
from simulator.simulation import simulation

# This method finds the real h and T which match the most the chosen characteristics
# of the virus. It takes as parameters the instance (including G and the list of nodes
# populating the graph G), the settings and the chosen degree of the patient zero.
def find_real_scenario_parameters(instance, real_h_T_setting, patient_zero_degree=None , first_node=None):
    
    # Creating a csv file and its header. Each line of the csv file is relative
    # to a different simulation characterized with a different triplet (h, T, lambda).
    csv_file = "./csv_folder/find_real_h_T.csv"
    csv_columns = ["N_nodes", \
                   "lambda", \
                   "h", \
                   "T_max", \
                   "total_healthy", \
                   "total_contagious", \
                   "total_ill", \
                   "total_dead", \
                   "total_recovered", \
                   "contagious_percentage", \
                   "ill_percentage", \
                   "death_percentage", \
                   "avg_iterations_to_die", \
                   "diff_contage", \
                   "diff_deaths", \
                   "sum_of_diffs"]
    
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
    # Create a local Dataframe to store the intermediate results and for
    # further analysis.
    df = pd.DataFrame(columns = csv_columns)
    
    # Name of the log file.
    log_file = "find_real_h_T_log"
        
    # Launching a simulation letting lambda, h and T vary in the ranges specified 
    # in the settings. For each triplet (h, T, lambda) a simulation is launched.
    for lambd in real_h_T_setting['lambda_range']:
        for h in real_h_T_setting['h_range']:
            for T in real_h_T_setting["T_max"]:
                pl = instance.pl
                results = simulation(log_file, real_h_T_setting, lambd, h, T, pl, instance.SIM_LIM, patient_zero_degree, first_node, False, False)            
                # Appending the intermediate results in a local DF.
                df = df.append(results, ignore_index=True)
                
                # Save the intermediate results of each simulation in the csv file.
                try:
                    with open(csv_file, 'a') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                        writer.writerow(results)
                except IOError:
                    print("I/O error")

    # Finding the h and T that match the most the chosen virus characteristics.
    # The rows of the DataFrame, that provide a gap not higher than 500 from the
    # infection and death targets jointly, are considered to discover the real h and T.
    # h and T values are evaluated by averaging their values in the selected rows.
    dfObj = df.sort_values(by='sum_of_diffs').loc[(df['sum_of_diffs'] >= 0) & (df['sum_of_diffs'] <= 500)]
    h = dfObj["h"].mean()
    T_max = int(np.floor(dfObj["T_max"].mean()))
    
    return df, h, T_max