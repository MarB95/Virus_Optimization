# -*- coding: utf-8 -*-

import csv
import pandas as pd
from simulator.simulation import simulation

def influenceOf_h_T(instance, influenceOf_h_T_setting, patient_zero_degree=None , first_node=None, change_h = False):
    
    # Creating three csv files according to what it's done. A csv file stores
    # all the results, the other one stores the averages of the results for
    # a given value of either T or h.
    csv_file = "./csv_folder/influenceOf_h_T.csv"
    csv_file_h = "./csv_folder/mean_influenceOf_h.csv"
    csv_file_T = "./csv_folder/mean_influenceOf_T.csv"
    # Csv columns of interests. 
    csv_columns = ["h", \
                   "T_max", \
                   "total_healthy", \
                   "total_contagious", \
                   "total_dead"]
        
    # Name of the log file.
    log_file = "influenceOfhTh_T_log"
    # Dataframe storing the intermediate results.
    tmp_df = pd.DataFrame()
   
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
    # Launching a simulation letting lambda, h and T vary in the ranges specified 
    # in the settings. For each triplet (h, T, lambda) a simulation is launched.
    for lambd in influenceOf_h_T_setting['lambda_range']:
        for h in influenceOf_h_T_setting['h_range']:
            for T in influenceOf_h_T_setting["T_range"]:
                pl = instance.pl
                results = simulation(log_file, influenceOf_h_T_setting, lambd, h, T, pl, instance.SIM_LIM, patient_zero_degree, first_node, False, False)
                tmp_results = {"h":results["h"], "T_max":results["T_max"], "total_healthy":results["total_healthy"], "total_contagious":results["total_contagious"], "total_dead":results["total_dead"] }
                # Appending the intermediate results in a local DF.
                tmp_df = tmp_df.append(tmp_results, ignore_index=True)
                # Save the intermediate results of each simulation in the csv file.
                try:
                    with open(csv_file, 'a') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                        writer.writerow(tmp_results)
                except IOError:
                    print("I/O error")
    ###
    if not change_h:
        df_mean_T = pd.DataFrame(columns = csv_columns)
        for el in influenceOf_h_T_setting["list_of_T"]:
            mean_healthy = tmp_df[tmp_df.T_max == el]["total_healthy"].to_numpy().mean()
            mean_contagious = tmp_df[tmp_df.T_max == el]["total_contagious"].to_numpy().mean()
            mean_dead = tmp_df[tmp_df.T_max == el]["total_dead"].to_numpy().mean()
            tmp_res = {"h":influenceOf_h_T_setting['h_range'][0], "T_max": el, "total_healthy":mean_healthy, "total_contagious":mean_contagious, "total_dead":mean_dead}
            df_mean_T = df_mean_T.append(tmp_res, ignore_index=True)
            
            try:
                with open(csv_file_T, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writerow(tmp_res)
            except IOError:
                print("I/O error")
        return df_mean_T, tmp_df
    else:
        df_mean_h = pd.DataFrame(columns = csv_columns)
        for el in influenceOf_h_T_setting["list_of_h"]:
            mean_healthy = tmp_df[tmp_df.h == el]["total_healthy"].to_numpy().mean()
            mean_contagious = tmp_df[tmp_df.h == el]["total_contagious"].to_numpy().mean()
            mean_dead = tmp_df[tmp_df.h == el]["total_dead"].to_numpy().mean()
            tmp_res = {"h": el, "T_max":influenceOf_h_T_setting['T_range'][0], "total_healthy":mean_healthy, "total_contagious":mean_contagious, "total_dead":mean_dead}
            df_mean_h = df_mean_h.append(tmp_res, ignore_index=True)
            try:
                with open(csv_file_h, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writerow(tmp_res)
            except IOError:
                print("I/O error")
        return df_mean_h, tmp_df