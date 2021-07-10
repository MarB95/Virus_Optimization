# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta
from matplotlib.ticker import MaxNLocator

# Given the time evolution of the network in the final simulation (having fixed
# h, T and lambda), and stored in a Dataframe, a plot is generated, reporting the
# amount of healthy, contagious, ill, dead and recovered people over time.
def plot_results_small_high(df_plot_high_deg):
    x = range(df_plot_high_deg.shape[1])
    plt.figure(figsize=(22, 19))
    plt.plot(x, df_plot_high_deg.loc["healthy"], "C2", label="Healthy", linewidth=5.0)
    plt.plot(x, df_plot_high_deg.loc["contagious"],  "C8", label="Contagious", linewidth=5.0)
    plt.plot(x, df_plot_high_deg.loc["ill"], "C3", label="Ill", linewidth=5.0)
    plt.plot(x, df_plot_high_deg.loc["dead"], "C7", label="Dead", linewidth=5.0)
    plt.plot(x, df_plot_high_deg.loc["recovered"], "C0", label="Recovered", linewidth=5.0)
    plt.rcParams.update({"font.size": 22})
    plt.xticks(x)
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    plt.title("Simulation for graph of 3000 nodes with higher average degree", fontsize=30)
    plt.xlabel("Time (1 unit = 2 days)", fontsize=30)
    plt.ylabel("Number of nodes", fontsize=30)
    plt.legend(loc="upper right", fontsize=30)
    plt.show()
    
def plot_results_small_low(df_plot_low_deg):
    x = range(df_plot_low_deg.shape[1])
    plt.figure(figsize=(22, 19))
    plt.plot(x, df_plot_low_deg.loc["healthy"], "C2", label="Healthy", linewidth=5.0)
    plt.plot(x, df_plot_low_deg.loc["contagious"],  "C8", label="Contagious", linewidth=5.0)
    plt.plot(x, df_plot_low_deg.loc["ill"], "C3", label="Ill", linewidth=5.0)
    plt.plot(x, df_plot_low_deg.loc["dead"], "C7", label="Dead", linewidth=5.0)
    plt.plot(x, df_plot_low_deg.loc["recovered"], "C0", label="Recovered", linewidth=5.0)
    plt.rcParams.update({"font.size": 22})
    plt.xticks(x)
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    plt.title("Simulation for graph of 3000 nodes with lower average degree", fontsize=30)
    plt.xlabel("Time (1 unit = 2 days)", fontsize=30)
    plt.ylabel("Number of nodes", fontsize=30)
    plt.legend(loc="upper right", fontsize=30)
    plt.show()

def plot_results_big(df_plot_big):
    x = range(df_plot_big.shape[1])
    plt.figure(figsize=(40, 19))
    plt.plot(x, df_plot_big.loc["healthy"], "C2", label="Healthy", linewidth=5.0)
    plt.plot(x, df_plot_big.loc["contagious"],  "C8", label="Contagious", linewidth=5.0)
    plt.plot(x, df_plot_big.loc["ill"], "C3", label="Ill", linewidth=5.0)
    plt.plot(x, df_plot_big.loc["dead"], "C7", label="Dead", linewidth=5.0)
    plt.plot(x, df_plot_big.loc["recovered"], "C0", label="Recovered", linewidth=5.0)
    plt.rcParams.update({"font.size": 22})
    plt.xticks(x)
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    plt.title("Simulation for graph of 10000 nodes", fontsize=30)
    plt.xlabel("Time (1 unit = 2 days)", fontsize=30)
    plt.ylabel("Number of nodes", fontsize=30)
    plt.legend(loc="upper right", fontsize=30)
    plt.show()
    
def plot_results_small(df_plot):
    x = range(df_plot.shape[1])
    plt.figure(figsize=(40, 19))
    plt.plot(x, df_plot.loc["healthy"], "C2", label="Healthy", linewidth=5.0)
    plt.plot(x, df_plot.loc["contagious"],  "C8", label="Contagious", linewidth=5.0)
    plt.plot(x, df_plot.loc["ill"], "C3", label="Ill", linewidth=5.0)
    plt.plot(x, df_plot.loc["dead"], "C7", label="Dead", linewidth=5.0)
    plt.plot(x, df_plot.loc["recovered"], "C0", label="Recovered", linewidth=5.0)
    plt.rcParams.update({"font.size": 22})
    plt.xticks(x)
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    plt.title("Simulation for graph of 3000 nodes with intermediate average degree", fontsize=30)
    plt.xlabel("Time (1 unit = 2 days)", fontsize=30)
    plt.ylabel("Number of nodes", fontsize=30)
    plt.legend(loc="upper right", fontsize=30)
    plt.show()

def plot_single_result(df_plot):
    x = range(df_plot.shape[1])
    plt.figure(figsize=(40, 19))
    plt.plot(x, df_plot.loc["healthy"], "C2", label="Healthy", linewidth=5.0)
    plt.plot(x, df_plot.loc["contagious"],  "C8", label="Contagious", linewidth=5.0)
    plt.plot(x, df_plot.loc["ill"], "C3", label="Ill", linewidth=5.0)
    plt.plot(x, df_plot.loc["dead"], "C7", label="Dead", linewidth=5.0)
    plt.plot(x, df_plot.loc["recovered"], "C0", label="Recovered", linewidth=5.0)
    plt.rcParams.update({"font.size": 22})
    plt.xticks(x)
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    plt.title("Simulation for graph of 3000 nodes with intermediate average degree", fontsize=30)
    plt.xlabel("Time (1 unit = 2 days)", fontsize=30)
    plt.ylabel("Number of nodes", fontsize=30)
    plt.legend(loc="upper right", fontsize=30)
    plt.show()
    
# Plotting the degree distribution of the 10000 nodes graph.    
def graph_histogram(instance_big):
    pl = instance_big.pl
    # Plotting node degree histogram.
    degrees = [len(node.neighborhood) for node in pl]
    plt.figure(figsize=(18,15))
    labels, counts = np.unique(degrees, return_counts=True)
    plt.bar(labels, counts, align='center')
    plt.gca().set_xticks(labels)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title("Node degree distribution in the network of 10000 nodes", fontsize=30)
    plt.xlabel("Node degree", fontsize=24)
    plt.ylabel("Number of nodes", fontsize=24)
 
# Plotting the alpha and beta distributions.
def plot_beta_p_q():
    a_p = 5
    b_p = 5
    a_q = 2
    b_q = 30
    plt.figure(figsize=(18,15))
    x = np.linspace(beta.ppf(0, a_p, b_p),
                beta.ppf(1, a_p, b_p), 100)
    plt.plot(x, beta.pdf(x, a_p, b_p),
       'b-', lw=5, alpha=0.6, label=r'$\alpha$ pdf, a = 5, b = 5')
    x = np.linspace(beta.ppf(0, a_q, b_q),
                beta.ppf(1, a_q, b_q), 100)
    plt.plot(x, beta.pdf(x, a_q, b_q),
       'r-', lw=5, alpha=0.6, label=r'$\beta$ pdf, a = 2, b = 30')
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.xlabel("x", fontsize=28)
    plt.ylabel("Beta(a,b)", fontsize=28)
    plt.legend(fontsize=34)

# Plotting the occurrences for each degree category in the graph of 3000 nodes.
def plot_nodes_histogram_per_degree(instance_small):
    pl = instance_small.pl
    fig = plt.figure(figsize=(22, 19))
    ax = fig.add_subplot(111)
    
    counter_very_low = 0
    counter_low = 0
    counter_medium = 0
    counter_high = 0
    counter_very_high = 0
    for node in pl:
        if node.degree_cat == "VERY LOW":
            counter_very_low = counter_very_low + 1
        elif node.degree_cat == "LOW":
            counter_low = counter_low + 1
        elif node.degree_cat == "MEDIUM":
            counter_medium = counter_medium + 1
        elif node.degree_cat == "HIGH":
            counter_high = counter_high + 1
        else: counter_very_high = counter_very_high + 1
    
    ## the data
    N = 5
    low_deg = [counter_very_low,\
               counter_low,\
               counter_medium,\
               counter_high,\
               counter_very_high]
    
    ## necessary variables
    ind = np.arange(N) # the x locations for the groups
    width = 0.40 # the width of the bars
    
    ## the bars
    rects1 = ax.bar(ind, low_deg, width,
                    color='#1f77b4')
    
    # axes and labels
    #ax.set_xlim(-width,len(ind)+width)
    #.set_ylim(0,45)
    ax.set_ylabel('Number of nodes', fontsize=35)
    ax.set_title('Degree category distribution', fontsize=35)
    xTickMarks = ['VERY LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY HIGH']
    ax.set_xticks(ind)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=30)
    plt.yticks(fontsize=26)
    
    
    plt.show()

# Plotting the number of ill and dead nodes for different values of T.
def plot_influence_of_T(df_T_mean):
    T = [int(a) for a in list(df_T_mean.T_max.to_numpy())]
    contages = list(df_T_mean.total_contagious.to_numpy())
    deaths = list(df_T_mean.total_dead.to_numpy())
    plt.figure(figsize=(22,19))
    fig, axs = plt.subplots(2)
    fig.subplots_adjust(hspace=0.7)
    axs[0].plot(T, contages, 'tab:orange')
    axs[1].plot(T, deaths, 'tab:red')
    axs[0].set_title('Number of infected for different T')
    axs[1].set_title('Number of deaths for different T')
    #fig.tight_layout()
    axs[0].xaxis.set_major_locator(MaxNLocator(integer=True))
    axs[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    for ax in axs.flat:
        ax.set(xlabel='T', ylabel='Nodes')
    axs[0].grid()
    axs[1].grid()
    plt.show()
    
# Plotting the number of ill and dead nodes for different values of h.        
def plot_influence_of_h(df_h_mean):
    h = list(df_h_mean.h.to_numpy())
    contages = list(df_h_mean.total_contagious.to_numpy())
    deaths = list(df_h_mean.total_dead.to_numpy())
    plt.figure(figsize=(22,19))
    fig, axs = plt.subplots(2)
    fig.subplots_adjust(hspace=0.7)
    axs[0].plot(h, contages, 'tab:orange')
    axs[1].plot(h, deaths, 'tab:red')
    axs[0].set_title('Number of infected for different h')
    axs[1].set_title('Number of deaths for different h')
    #fig.tight_layout()
    #axs[0].xaxis.set_major_locator(MaxNLocator(integer=True))
    #axs[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    for ax in axs.flat:
        ax.set(xlabel='h', ylabel='Nodes')
    axs[0].grid()
    axs[1].grid()
    plt.show()

# Plotting the linearity between the 3000 and 10000 nodes networks.
def plot_linear_behaviour(df_plot, df_plot_big):
    healthy_diff = abs(df_plot_big.loc["healthy"] / df_plot.loc["healthy"]).fillna(0)
    contagious_diff = abs(df_plot_big.loc["contagious"] / df_plot.loc["contagious"]).fillna(0)
    ill_diff = abs(df_plot_big.loc["ill"] / df_plot.loc["ill"]).fillna(0)
    dead_diff = abs(df_plot_big.loc["dead"] / df_plot.loc["dead"]).fillna(0)
    recovered_diff = abs(df_plot_big.loc["recovered"] / df_plot.loc["recovered"]).fillna(0)
    
    x = range(df_plot_big.shape[1])
    plt.figure(figsize=(22, 19))
    plt.plot(x, healthy_diff, "C2", label="Healthy", linewidth=5.0)
    plt.plot(x, contagious_diff,  "C8", label="Contagious", linewidth=5.0)
    plt.plot(x, ill_diff, "C3", label="Ill", linewidth=5.0)
    plt.plot(x, dead_diff, "C7", label="Dead", linewidth=5.0)
    plt.plot(x, recovered_diff, "C0", label="Recovered", linewidth=5.0)
    plt.rcParams.update({"font.size": 22})
    plt.xticks(x)
    plt.xticks(fontsize=26)
    plt.yticks(fontsize=26)
    plt.title("Linearity between 10000 nodes graph and 3000 nodes graph simulations", fontsize=30)
    plt.xlabel("Time (1 unit = 2 days)", fontsize=30)
    plt.ylabel("Ratio", fontsize=30)
    plt.legend(loc="upper right", fontsize=30)
    plt.show()

# Plotting the histogram for the dead nodes for the 3000 nodes network with
# average degree, with std.
def plot_dead_histogram_per_degree_small_instance(df_final_VL,\
                                                df_final_L,\
                                                df_final_M,\
                                                df_final_H,\
                                                df_final_VH):
    fig = plt.figure(figsize=(22, 19))
    ax = fig.add_subplot(111)
    
    ## the data
    N = 5
        
    medium_deg_con = [int(df_final_VL.total_ill.mean()),\
                  int(df_final_L.total_ill.mean()),\
                  int(df_final_M.total_ill.mean()),\
                  int(df_final_H.total_ill.mean()),\
                  int(df_final_VH.total_ill.mean())]
        
    
    medium_deg_con_std = [float(df_final_VL.total_ill.std()),\
               float(df_final_L.total_ill.std()),\
               float(df_final_M.total_ill.std()),\
               float(df_final_H.total_ill.std()),\
               float(df_final_VH.total_ill.std())]
        
    medium_deg_dead = [int(df_final_VL.total_dead.mean()),\
                  int(df_final_L.total_dead.mean()),\
                  int(df_final_M.total_dead.mean()),\
                  int(df_final_H.total_dead.mean()),\
                  int(df_final_VH.total_dead.mean())]
        
    
    medium_deg_dead_std = [float(df_final_VL.total_dead.std()),\
               float(df_final_L.total_dead.std()),\
               float(df_final_M.total_dead.std()),\
               float(df_final_H.total_dead.std()),\
               float(df_final_VH.total_dead.std())]
    
    ## necessary variables
    ind = np.arange(N) # the x locations for the groups
    width = 0.30 # the width of the bars
    
    ## the bars
    
    rects1 = ax.bar(ind, medium_deg_con, width,
                        color='#2796e3',
                        yerr=medium_deg_con_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    rects2 = ax.bar(ind+width, medium_deg_dead, width,
                        color='#d43bff',
                        yerr=medium_deg_dead_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    
    # axes and labels
    #ax.set_xlim(-width,len(ind)+width)
    #.set_ylim(0,45)
    ax.set_ylabel('Number of nodes', fontsize=35)
    ax.set_title('Ill and dead nodes per patient zero degree', fontsize=35)
    xTickMarks = ['VERY LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY HIGH']
    ax.set_xticks(ind+0.1)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=30)
    plt.yticks(fontsize=26)
    
    ax.legend( (rects1[0], rects2[0]), \
              ('Ill nodes', 'Dead nodes',), fontsize=30,\
               loc="upper right", bbox_to_anchor=(1.27, 1))
    
    plt.show()

# Plotting the histogram for the dead nodes for the 3000 nodes network with
# lower average degree, with std.
def plot_dead_histogram_per_degree_small_instance_low_def(df_final_low_deg_VL,\
                                                          df_final_low_deg_L,\
                                                          df_final_low_deg_M,\
                                                          df_final_low_deg_H,\
                                                          df_final_low_deg_VH):
    fig = plt.figure(figsize=(22, 19))
    ax = fig.add_subplot(111)
    
    ## the data
    N = 5
        
    medium_deg_con = [int(df_final_low_deg_VL.total_ill.mean()),\
                  int(df_final_low_deg_L.total_ill.mean()),\
                  int(df_final_low_deg_M.total_ill.mean()),\
                  int(df_final_low_deg_H.total_ill.mean()),\
                  int(df_final_low_deg_VH.total_ill.mean())]
        
    
    medium_deg_con_std = [float(df_final_low_deg_VL.total_ill.std()),\
               float(df_final_low_deg_L.total_ill.std()),\
               float(df_final_low_deg_M.total_ill.std()),\
               float(df_final_low_deg_H.total_ill.std()),\
               float(df_final_low_deg_VH.total_ill.std())]
        
    medium_deg_dead = [int(df_final_low_deg_VL.total_dead.mean()),\
                  int(df_final_low_deg_L.total_dead.mean()),\
                  int(df_final_low_deg_M.total_dead.mean()),\
                  int(df_final_low_deg_H.total_dead.mean()),\
                  int(df_final_low_deg_VH.total_dead.mean())]
        
    
    medium_deg_dead_std = [float(df_final_low_deg_VL.total_dead.std()),\
               float(df_final_low_deg_L.total_dead.std()),\
               float(df_final_low_deg_M.total_dead.std()),\
               float(df_final_low_deg_H.total_dead.std()),\
               float(df_final_low_deg_VH.total_dead.std())]
    
    ## necessary variables
    ind = np.arange(N) # the x locations for the groups
    width = 0.30 # the width of the bars
    
    ## the bars
    
    rects1 = ax.bar(ind, medium_deg_con, width,
                        color='#2796e3',
                        yerr=medium_deg_con_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    rects2 = ax.bar(ind+width, medium_deg_dead, width,
                        color='#d43bff',
                        yerr=medium_deg_dead_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    
    # axes and labels
    #ax.set_xlim(-width,len(ind)+width)
    #.set_ylim(0,45)
    ax.set_ylabel('Number of nodes', fontsize=35)
    ax.set_title('Ill and dead nodes per patient zero degree', fontsize=35)
    xTickMarks = ['VERY LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY HIGH']
    ax.set_xticks(ind+0.1)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=30)
    plt.yticks(fontsize=26)
    
    ax.legend( (rects1[0], rects2[0]), \
              ('Ill nodes', 'Dead nodes',), fontsize=30,\
               loc="upper right", bbox_to_anchor=(1.27, 1))
    
    plt.show()

# Plotting the histogram for the dead nodes for the 3000 nodes network with
# higher average degree, with std.
def plot_dead_histogram_per_degree_small_instance_high_def(df_final_high_deg_VL,\
                                                          df_final_high_deg_L,\
                                                          df_final_high_deg_M,\
                                                          df_final_high_deg_H,\
                                                          df_final_high_deg_VH):
    fig = plt.figure(figsize=(22, 19))
    ax = fig.add_subplot(111)
    
    ## the data
    N = 5
        
    medium_deg_con = [int(df_final_high_deg_VL.total_ill.mean()),\
                  int(df_final_high_deg_L.total_ill.mean()),\
                  int(df_final_high_deg_M.total_ill.mean()),\
                  int(df_final_high_deg_H.total_ill.mean()),\
                  int(df_final_high_deg_VH.total_ill.mean())]
        
    
    medium_deg_con_std = [float(df_final_high_deg_VL.total_ill.std()),\
               float(df_final_high_deg_L.total_ill.std()),\
               float(df_final_high_deg_M.total_ill.std()),\
               float(df_final_high_deg_H.total_ill.std()),\
               float(df_final_high_deg_VH.total_ill.std())]
        
    medium_deg_dead = [int(df_final_high_deg_VL.total_dead.mean()),\
                  int(df_final_high_deg_L.total_dead.mean()),\
                  int(df_final_high_deg_M.total_dead.mean()),\
                  int(df_final_high_deg_H.total_dead.mean()),\
                  int(df_final_high_deg_VH.total_dead.mean())]
        
    
    medium_deg_dead_std = [float(df_final_high_deg_VL.total_dead.std()),\
               float(df_final_high_deg_L.total_dead.std()),\
               float(df_final_high_deg_M.total_dead.std()),\
               float(df_final_high_deg_H.total_dead.std()),\
               float(df_final_high_deg_VH.total_dead.std())]
    
    ## necessary variables
    ind = np.arange(N) # the x locations for the groups
    width = 0.30 # the width of the bars
    
    ## the bars
    
    rects1 = ax.bar(ind, medium_deg_con, width,
                        color='#2796e3',
                        yerr=medium_deg_con_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    rects2 = ax.bar(ind+width, medium_deg_dead, width,
                        color='#d43bff',
                        yerr=medium_deg_dead_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    
    # axes and labels
    #ax.set_xlim(-width,len(ind)+width)
    #.set_ylim(0,45)
    ax.set_ylabel('Number of nodes', fontsize=35)
    ax.set_title('Ill and dead nodes per patient zero degree', fontsize=35)
    xTickMarks = ['VERY LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY HIGH']
    ax.set_xticks(ind+0.1)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=30)
    plt.yticks(fontsize=26)
    
    ax.legend( (rects1[0], rects2[0]), \
              ('Ill nodes', 'Dead nodes',), fontsize=30,\
               loc="upper right", bbox_to_anchor=(1.27, 1))
    
    plt.show()

# Plotting histogram of infected nodes per degree category for the 3 networks.    
def plot_infected_histogram_per_degree(df_final_VL,df_final_low_deg_VL,df_final_high_deg_VL,\
                              df_final_L,df_final_low_deg_L,df_final_high_deg_L,\
                              df_final_M,df_final_low_deg_M,df_final_high_deg_M,\
                              df_final_H,df_final_low_deg_H,df_final_high_deg_H,\
                              df_final_VH,df_final_low_deg_VH,df_final_high_deg_VH):
    fig = plt.figure(figsize=(22, 19))
    ax = fig.add_subplot(111)
    
    ## the data
    N = 5
    low_deg = [int(df_final_low_deg_VL.total_ill.mean()),\
               int(df_final_low_deg_L.total_ill.mean()),\
               int(df_final_low_deg_M.total_ill.mean()),\
               int(df_final_low_deg_H.total_ill.mean()),\
               int(df_final_low_deg_VH.total_ill.mean())]
    
    high_deg = [int(df_final_high_deg_VL.total_ill.mean()),\
               int(df_final_high_deg_VL.total_ill.mean()),\
               int(df_final_high_deg_VL.total_ill.mean()),\
               int(df_final_high_deg_VL.total_ill.mean()),\
               int(df_final_high_deg_VL.total_ill.mean())]
        
    medium_deg = [int(df_final_VL.total_ill.mean()),\
                  int(df_final_L.total_ill.mean()),\
                  int(df_final_M.total_ill.mean()),\
                  int(df_final_H.total_ill.mean()),\
                  int(df_final_VH.total_ill.mean())]
        
    low_deg_std = [float(df_final_low_deg_VL.total_ill.std()),\
               float(df_final_low_deg_L.total_ill.std()),\
               float(df_final_low_deg_M.total_ill.std()),\
               float(df_final_low_deg_H.total_ill.std()),\
               float(df_final_low_deg_VH.total_ill.std())]
    
    high_deg_std = [float(df_final_high_deg_VL.total_ill.std()),\
               float(df_final_high_deg_L.total_ill.std()),\
               float(df_final_high_deg_M.total_ill.std()),\
               float(df_final_high_deg_H.total_ill.std()),\
               float(df_final_high_deg_VH.total_ill.std())]
    
    medium_deg_std = [float(df_final_VL.total_ill.std()),\
               float(df_final_L.total_ill.std()),\
               float(df_final_M.total_ill.std()),\
               float(df_final_H.total_ill.std()),\
               float(df_final_VH.total_ill.std())]
    
    ## necessary variables
    ind = np.arange(N) # the x locations for the groups
    width = 0.20 # the width of the bars
    
    ## the bars
    rects1 = ax.bar(ind, low_deg, width,
                    color='#19e631',
                    yerr=low_deg_std,
                    error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    rects2 = ax.bar(ind+width, medium_deg, width,
                        color='#e6e619',
                        yerr=medium_deg_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    rects3 = ax.bar(ind+2*width, high_deg, width,
                        color='#e63819',
                        yerr=high_deg_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    # axes and labels
    #ax.set_xlim(-width,len(ind)+width)
    #.set_ylim(0,45)
    ax.set_ylabel('Contagious nodes', fontsize=35)
    ax.set_title('Contagious nodes per degree', fontsize=35)
    xTickMarks = ['VERY LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY HIGH']
    ax.set_xticks(ind+width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=30)
    plt.yticks(fontsize=26)
    
    ## add a legend
    ax.legend( (rects1[0], rects2[0], rects3[0]), \
              ('Low degree', 'Intermediate degree', 'High degree',), fontsize=30,\
               loc="upper right", bbox_to_anchor=(1.37, 1))
    
    plt.show()
    
# Plotting histogram of dead nodes per degree category for the 3 networks.        
def plot_dead_histogram_per_degree(df_final_VL,df_final_low_deg_VL,df_final_high_deg_VL,\
                              df_final_L,df_final_low_deg_L,df_final_high_deg_L,\
                              df_final_M,df_final_low_deg_M,df_final_high_deg_M,\
                              df_final_H,df_final_low_deg_H,df_final_high_deg_H,\
                              df_final_VH,df_final_low_deg_VH,df_final_high_deg_VH):
    fig = plt.figure(figsize=(22, 19))
    ax = fig.add_subplot(111)
    
    ## the data
    N = 5
    low_deg = [int(df_final_low_deg_VL.total_dead.mean()),\
               int(df_final_low_deg_L.total_dead.mean()),\
               int(df_final_low_deg_M.total_dead.mean()),\
               int(df_final_low_deg_H.total_dead.mean()),\
               int(df_final_low_deg_VH.total_dead.mean())]
    
    high_deg = [int(df_final_high_deg_VL.total_dead.mean()),\
               int(df_final_high_deg_L.total_dead.mean()),\
               int(df_final_high_deg_M.total_dead.mean()),\
               int(df_final_high_deg_H.total_dead.mean()),\
               int(df_final_high_deg_VH.total_dead.mean())]
        
    medium_deg = [int(df_final_VL.total_dead.mean()),\
                  int(df_final_L.total_dead.mean()),\
                  int(df_final_M.total_dead.mean()),\
                  int(df_final_H.total_dead.mean()),\
                  int(df_final_VH.total_dead.mean())]
        
    low_deg_std = [float(df_final_low_deg_VL.total_dead.std()),\
               float(df_final_low_deg_L.total_dead.std()),\
               float(df_final_low_deg_M.total_dead.std()),\
               float(df_final_low_deg_H.total_dead.std()),\
               float(df_final_low_deg_VH.total_dead.std())]
    
    high_deg_std = [float(df_final_high_deg_VL.total_dead.std()),\
               float(df_final_high_deg_L.total_dead.std()),\
               float(df_final_high_deg_M.total_dead.std()),\
               float(df_final_high_deg_H.total_dead.std()),\
               float(df_final_high_deg_VH.total_dead.std())]
    
    medium_deg_std = [float(df_final_VL.total_dead.std()),\
               float(df_final_L.total_dead.std()),\
               float(df_final_M.total_dead.std()),\
               float(df_final_H.total_dead.std()),\
               float(df_final_VH.total_dead.std())]
    
    ## necessary variables
    ind = np.arange(N) # the x locations for the groups
    width = 0.20 # the width of the bars
    
    ## the bars
    rects1 = ax.bar(ind, low_deg, width,
                    color='#19e631',
                    yerr=low_deg_std,
                    error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    rects2 = ax.bar(ind+width, medium_deg, width,
                        color='#e6e619',
                        yerr=medium_deg_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    rects3 = ax.bar(ind+2*width, high_deg, width,
                        color='#e63819',
                        yerr=high_deg_std,
                        error_kw=dict(elinewidth=2,ecolor='#000000'))
    
    # axes and labels
    #ax.set_xlim(-width,len(ind)+width)
    #.set_ylim(0,45)
    ax.set_ylabel('Dead nodes', fontsize=35)
    ax.set_title('Dead nodes per degree', fontsize=35)
    xTickMarks = ['VERY LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY HIGH']
    ax.set_xticks(ind+width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=30)
    plt.yticks(fontsize=26)
    
    ## add a legend
    ax.legend( (rects1[0], rects2[0], rects3[0]), \
              ('Low degree', 'Intermediate degree', 'High degree',), fontsize=30,\
               loc="upper right", bbox_to_anchor=(1.37, 1))
    
    plt.show()
    
