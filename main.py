
# -*- coding: utf-8 -*-

import logging
import json
import pickle
from simulator.instance import Instance
from utility.find_real_h_T import find_real_scenario_parameters
from utility.influence_of_h_T import influenceOf_h_T
from utility.best_lambda import find_optimal_lambda
from utility.final_network_behaviour import final_network_simulation
from utility.compute_result_dataframes import retrieve_result_dataframes
from utility.generate_plots import *

if __name__ == '__main__':

    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
        # The format specifies the format of each line of the log, an example is
        # 14:14:27 INFO starting simulation...
    )
    # --- INTRODUCTION: READING JSON SETTINGS, PICKLE FILES STORING THE GRAPHS AND 
    # --- INITIALIZING THE INSTANCES.
    # Reading the settings json file for the research of the real h and T.
    fp = open('./etc/real_h_T_setting.json', 'r')
    real_h_T_setting = json.load(fp)
    fp.close()
    
    # Reading the settings json file including the simulation parameters.
    fp = open('./etc/simulation_setting.json', 'r')
    simulation_setting = json.load(fp)
    fp.close()
    
    # Reading the settings json file for finding the best lambda once h 
    # and T real are discovered.
    f = open('./etc/best_lambda_setting.json', 'r')
    best_lambda_setting = json.load(f)
    f.close()
    
    # Reading the settings json file for finding the best lambda once h 
    # and T real are discovered.
    f = open('./etc/influenceOf_T_setting.json', 'r')
    influenceOf_T_setting = json.load(f)
    f.close()
    
    # Reading the settings json file for finding the best lambda once h 
    # and T real are discovered.
    f = open('./etc/influenceOf_h_setting.json', 'r')
    influenceOf_h_setting = json.load(f)
    f.close()
    
    # Reading the saved variables G, which includes the stochastic graph, and 
    # pl which is the list of the nodes, each one characterized by its own parameters.
    f = open('./pickle files/small_instance.pkl', 'rb')
    G, pl= pickle.load(f)
    # Creating an instance of the simulation passing the proper parameters.
    instance_small = Instance(G, pl, simulation_setting)
    f.close()
    
    # Reading the saved variables G, which includes the stochastic graph, and 
    # pl which is the list of the nodes, each one characterized by its own parameters.
    f = open('./pickle files/big_instance.pkl', 'rb')
    G, pl= pickle.load(f)
    # Creating an instance of the simulation passing the proper parameters.
    instance_big = Instance(G, pl, simulation_setting)
    f.close() 
    
    # Reading the saved variables G, which includes the stochastic graph, and 
    # pl which is the list of the nodes, each one characterized by its own parameters.
    f = open('./pickle files/small_graph_low_deg.pkl', 'rb')
    G, pl= pickle.load(f)
    # Creating an instance of the simulation passing the proper parameters.
    instance_small_low_deg = Instance(G, pl, simulation_setting)
    f.close() 
    
    # Reading the saved variables G, which includes the stochastic graph, and 
    # pl which is the list of the nodes, each one characterized by its own parameters.
    f = open('./pickle files/small_graph_high_deg.pkl', 'rb')
    G, pl= pickle.load(f)
    # Creating an instance of the simulation passing the proper parameters.
    instance_small_high_deg = Instance(G, pl, simulation_setting)
    f.close() 
    # ------------------------------------------------------------------------
    
    # --- REAL PARAMETERS DISCOVERY.
    # The real scenario parameters are investigated, having defined
    # the virus to have an infection rate of 40% and death rate of 7%.
    # The node degree of the patient zero is set to be medium.
    #print("Finding real h and T_max...")
    #df_real_h_T, h_real, T_max_real = find_real_scenario_parameters(instance_small, real_h_T_setting, "MEDIUM")
    # These are the real paramenters that have been found:
    h_real = 0.45
    T_max_real = 4
    # ------------------------------------------------------------------------
    
    # --- LAMBDA OPTIMIZATION.
    # Finding the optimal lambda in the real scenario, the lambda that 
    # provides the highest number of deaths.
    print("Finding optimal lambda...")
    lambda_optimal = find_optimal_lambda(instance_small, best_lambda_setting, h_real, T_max_real, "MEDIUM")
    # This is the optimal lambda that has been found:
    #lambda_optimal = 0.59
    # ------------------------------------------------------------------------
    
    # --- STUDY ON THE INFLUENCE OF THE PARAMETERS AND NETWORK CHARACTERSITCS.
    # Having discovered the lambda optimal, different values of T and h are
    # tested. The average simulations results, for each tested values, are 
    # returned in a DataFrame.
    # First, several T values are tested.
    #print("Analysing influence of T_max...")
    #df_T_mean, df =  influenceOf_h_T(instance_small, influenceOf_T_setting, "MEDIUM", None, False)
    #plot_influence_of_T(df_T_mean)
    # Then, several h values are tested.
    #print("Analysing influence of h...")
    #df_h_mean, df =  influenceOf_h_T(instance_small, influenceOf_h_setting, "MEDIUM", None, True)
    #plot_influence_of_h(df_h_mean)
    
    # Having fixed the optimal lambda, h real and T real, now the virus
    # behaviour is studied within the network, launching a final simulation.
    df_final_results, df_plot = final_network_simulation(instance_small, h_real, T_max_real, lambda_optimal, "MEDIUM")   
    
    # WARNING: due to the random nature of the simulation, patient zero may get ill and be removed from the network before 
    # infecting its neighbors. Therefore, in case of misleading results (2999 healthy nodes), run again the simulation.
    
    # Plotting the results obtained in the final simulation with the 
    # discovered parameters.
    plot_results_small(df_plot)
    
    # --- PLOTTING THE RESULTS AND IMPORTANT INFORMATION ABOUT THE ANALYSIS.
    # In order to plot the information, further simulations are launched, changing the instances and 
    # the neighborhood size of the patient zero node. 
    #df_final_results_big, df_plot_big = final_network_simulation(instance_big, h_real, T_max_real, lambda_optimal, "MEDIUM")
    #plot_results_big(df_plot_big)
    #df_final_results_low_deg, df_plot_low_deg = final_network_simulation(instance_small_low_deg, h_real, T_max_real, lambda_optimal, "MEDIUM")
    #plot_results_small_low(df_plot_low_deg)
    #df_final_results_high_deg, df_plot_high_deg = final_network_simulation(instance_small_high_deg, h_real, T_max_real, lambda_optimal, "MEDIUM")
    #plot_results_small_high(df_plot_high_deg)
    
    # Here, a 100 simulations are launched for each patient zero degree category for the three graphs
    # of 3000 nodes, one with lower average degree, one for the intermediate degree and one for the
    # higher degree. The results are then employed to plot the information.
    # Small instance average degree.
    #df_final_VL, df_final_L, df_final_M, df_final_H, df_final_VH = retrieve_result_dataframes(instance_small, h_real, T_max_real, lambda_optimal)

    # Small instance low degree.
    #df_final_low_deg_VL, df_final_low_deg_L, df_final_low_deg_M, df_final_low_deg_H, df_final_low_deg_VH = retrieve_result_dataframes(instance_small_low_deg, h_real, T_max_real, lambda_optimal)    
    
    # Small instance high degree.
    #df_final_high_deg_VL, df_final_high_deg_L, df_final_high_deg_M, df_final_high_deg_H, df_final_high_deg_VH = retrieve_result_dataframes(instance_small_high_deg, h_real, T_max_real, lambda_optimal)    
    
    # Plots for the network characteristics and Beta distributions (prob. of contagious and death):
    #graph_histogram(instance_small)
    #graph_histogram(instance_big)
    #plot_nodes_histogram_per_degree(instance_small)
    #plot_beta_p_q()
    
    '''
    # Retrieving the plots.
    
    plot_histogram_per_degree_small_instance(df_final_VL,\
                                            df_final_L,\
                                            df_final_M,\
                                            df_final_H,\
                                            df_final_VH,\
                                            'Ill and dead nodes per patient zero degree')
        
    plot_infected_histogram_per_degree(df_final_VL,df_final_low_deg_VL,df_final_high_deg_VL,\
                                        df_final_L,df_final_low_deg_L,df_final_high_deg_L,\
                                        df_final_M,df_final_low_deg_M,df_final_high_deg_M,\
                                        df_final_H,df_final_low_deg_H,df_final_high_deg_H,\
                                        df_final_VH,df_final_low_deg_VH,df_final_high_deg_VH)
        
    plot_dead_histogram_per_degree(df_final_VL,df_final_low_deg_VL,df_final_high_deg_VL,\
                                    df_final_L,df_final_low_deg_L,df_final_high_deg_L,\
                                    df_final_M,df_final_low_deg_M,df_final_high_deg_M,\
                                    df_final_H,df_final_low_deg_H,df_final_high_deg_H,\
                                    df_final_VH,df_final_low_deg_VH,df_final_high_deg_VH)
    '''
    # ------------------------------------------------------------------------------------------
