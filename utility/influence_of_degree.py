# -*- coding: utf-8 -*-

import csv
import pandas as pd
from simulator.simulation import final_simulation

def influence_avg_deg(instance, h, T, lambd, n_simulations, deg, patient_zero_degree=None , first_node=None):
    
    # Creating a csv file that stores the results for every simulation.
    csv_file = "./csv_folder/influence_avg_deg_"+deg+".csv"
    # Csv columns of interests. 
    csv_columns = ["h", \
                   "T_max", \
                   "lambda", \
                   "total_healthy", \
                   "total_contagious", \
                   "total_dead"]
        
    # Name of the log file.
    log_file = "influence_avg_deg_log"
    # Dataframe storing the intermediate results.
    tmp_df = pd.DataFrame()
   
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
    # Launching a simulation letting lambda, h and T vary in the ranges specified 
    # in the settings. For each triplet (h, T, lambda) a simulation is launched.
    for i in range(n_simulations):
        
        pl = instance.pl
        results = final_simulation(log_file, lambd, h, T, pl, instance.SIM_LIM, patient_zero_degree)
        tmp_results = {"h":h, "T_max":T, "lambda":lambd, "total_healthy":results[0]["total_healthy"], "total_contagious":results[0]["total_contagious"], "total_dead":results[0]["total_dead"] }
        # Appending the intermediate results in a local DF.
        tmp_df = tmp_df.append(tmp_results, ignore_index=True)
        # Save the intermediate results of each simulation in the csv file.
        try:
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(tmp_results)
        except IOError:
            print("I/O error")
            
    averages=tmp_df.mean(axis=0)
    averages_clean=tmp_df[tmp_df["total_dead"]>1].mean(axis=0)
    
    return tmp_df, averages, averages_clean
