# -*- coding: utf-8 -*-

import pandas as pd
from utility.final_network_behaviour import final_network_simulation

# Given the virus parameters and the proper input instance, the results are
# stored in the dataframes necessary for the plotting.
def retrieve_result_dataframes(instance, h_real, T_max_real, lambda_optimal):
                              
    # Initialize empty Dataframes to store the results.
    df_final_VL = pd.DataFrame(columns=('N_nodes', 'lambda', 'h','T_max','total_healthy','total_ill','total_dead','total_recovered'))
    df_final_L = pd.DataFrame(columns=('N_nodes', 'lambda', 'h','T_max','total_healthy','total_ill','total_dead','total_recovered'))
    df_final_M = pd.DataFrame(columns=('N_nodes', 'lambda', 'h','T_max','total_healthy','total_ill','total_dead','total_recovered'))
    df_final_H = pd.DataFrame(columns=('N_nodes', 'lambda', 'h','T_max','total_healthy','total_ill','total_dead','total_recovered'))
    df_final_VH = pd.DataFrame(columns=('N_nodes', 'lambda', 'h','T_max','total_healthy','total_ill','total_dead','total_recovered'))
    
    # Repeat the simulation for 100 times and store the results.
    for i in range(100):
        # VERY_LOW
        df_final_results_VL, df_plot = final_network_simulation(instance, h_real, T_max_real, lambda_optimal, "VERY LOW")
        df_final_VL.loc[i] = df_final_results_VL.loc[0]
        # LOW
        df_final_results_L, df_plot = final_network_simulation(instance, h_real, T_max_real, lambda_optimal, "LOW")
        df_final_L.loc[i] = df_final_results_L.loc[0]
        # MEDIUM
        df_final_results_M, df_plot = final_network_simulation(instance, h_real, T_max_real, lambda_optimal, "MEDIUM")
        df_final_M.loc[i] = df_final_results_M.loc[0]
        # HIGH
        df_final_results_H, df_plot = final_network_simulation(instance, h_real, T_max_real, lambda_optimal, "HIGH")
        df_final_H.loc[i] = df_final_results_H.loc[0]
        # VERY HIGH
        df_final_results_VH, df_plot = final_network_simulation(instance, h_real, T_max_real, lambda_optimal, "VERY HIGH")
        df_final_VH.loc[i] = df_final_results_VH.loc[0]
    
    return df_final_results_VL, df_final_results_L, df_final_results_M, df_final_results_H, df_final_results_VH