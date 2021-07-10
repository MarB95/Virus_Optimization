# -*- coding: utf-8 -*-

import random
import logging
import math
import pandas as pd

# This method is used to launch a simulation having fixed a triplet (h, T, lambda).
# This simulation is used to discover h and T real and the optimal lambda.
def simulation(log_file, real_h_T_setting, lambd, h, T_max, pl, SIM_LIM, patient_zero_degree=None, first_node_id=None, flag_optimal=False, flag_final_simulation=False):
    
    log_name = "./logs/" + log_file
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        force=True,
        filemode='w'
        # The format specifies the format of each line of the log, an example is
        # 14:14:27 INFO starting simulation...
    )
    
    random.seed(random.choice(range(3000)))
    
    # Retrieve the maximum T value from the real scenario settings.
    #T_max = real_h_T_setting["T_max"]
    
    # Retrieve the simulation duration from instance.
    SIM_LIM = SIM_LIM
    
    # Retrieve the list of nodes populating the graph from instance.
    nodes = pl
    
    # Retrieve the wanted percentage of contage from the real scenario settings.
    perc_contage = real_h_T_setting["perc_contage"]
    
    # Retrieve the wanted percentage of deaths from the real scenario settings.
    perc_deaths = real_h_T_setting["perc_deaths"]
    
    
    for node in nodes:
        node.t = -1
        node.t_ill = 0
        node.state = "HEALTHY"
        node.p = 0
        node.q = 0
        node.viral_q = 0

    # Evaluating the average degree and std deviation of the degree of the 
    # nodes belonging to the graph.
    #mean_degree, std_degree = instance.getMeanStdGraphDegree()
    
    '''
    # To not display the figure.
    plt.ioff()
    fig = plt.figure(figsize=(8,5))
    nx.draw(G, pos=pos, node_color=[color_state_map.get(node.state)
                    for node in nodes], with_labels=True, node_size=500, font_color='white')
    '''
    
    # Initializing empty list for contagious and ill nodes.
    contagious_nodes = []
    ill_nodes = []
    dead_nodes = []
    recovered_nodes = []
    
    logging.info(f"Starting the simulation with h={h}, T_max={T_max}, lambda={lambd}...")
    
    # Starting the simulation from t=0.    
    for t in range(SIM_LIM):
        
        flag_event = False
        logging.info(f"Timestamp t={t}:")
        # Set the first node as contagious at random, like if we were in t = 0.
        if t == 0:
            # Selecting as patient zero a node that satisfies the provided degree.
            if first_node_id==None:
                contagious_node = random.choice([node for node in nodes if node.degree_cat == patient_zero_degree])
                #contagious_node = random.choice(nodes)
            else:
                contagious_node = nodes[first_node_id]
            contagious_node.state = "CONTAGIOUS"
            contagious_node.t = contagious_node.t + 1
            contagious_node.p = contagious_node.alpha*(1 - math.exp(-lambd*contagious_node.t))
            contagious_node.viral_q = 1 - math.exp(-lambd*contagious_node.t)
            contagious_nodes.append(contagious_node.id)
            logging.info(f"Node {contagious_node.id} is set to CONTAGIOUS.")
            continue
            
        for node in nodes:
            # In case the current node is either healthy, dead or recovered, it cannot infect
            # other nodes, hence we skip this node.
            if node.state == "HEALTHY" or node.state == "DEAD" or node.state == "RECOVERED":
                continue
            # Otherwise, continue.
            elif node.state == "CONTAGIOUS":
                # Updating the p, viral quantity and local timestamp of the contagious node/person
                # for the current timestamp.
                node.t = node.t + 1
                node.p = node.alpha*(1 - math.exp(-lambd*node.t))
                node.viral_q = 1 - math.exp(-lambd*node.t)
                
                # If the viral quantity exceedes the threshold, the node becomes ill. We change its
                # state, append its id to the ill list and add a penalty to the timestamps to heal.
                if node.viral_q >= h:
                    node.state = "ILL"
                    node.t_ill = node.t_ill + 1
                    node.q = node.beta*(1 - math.exp(-lambd*node.t_ill))
                    ill_nodes.append(node.id)
                    contagious_nodes.remove(node.id)
                    logging.info(f"Node {node.id}'s viral quantity exceeded h, it is now ILL.")
                    flag_event = True
                    
                else:
                    # Once the node is contagious, and didn't get ill already, we have to check whether 
                    # its neighbors become contagious too or not
                    for neighbor in node.neighborhood:
                        # If the node is not already contagious and it gets infected, 
                        # it becomes contagious.
                        if nodes[neighbor].state == "HEALTHY" and random.random() < node.p:
                            # Now that the node/person is contagious its parameters p, q, viral quantity
                            # are initialized
                            nodes[neighbor].state = "CONTAGIOUS"
                            nodes[neighbor].t = nodes[neighbor].t + 1
                            nodes[neighbor].p = nodes[neighbor].alpha*(1 - math.exp(-lambd*nodes[neighbor].t))
                            nodes[neighbor].viral_q = 1 - math.exp(-lambd*nodes[neighbor].t)
                            # We append the new contagious node id to the list.
                            contagious_nodes.append(nodes[neighbor].id)
                            logging.info(f"Node {neighbor} is now CONTAGIOUS, it has been infected by node {node.id}.")
                            flag_event = True
            
            # If the node is ill...
            elif node.state == "ILL":
                node.t_ill = node.t_ill + 1
                node.q = node.beta*(1 - math.exp(-lambd*node.t_ill))
                
                # Checking if the node can die, if the probability is higher tha its q.
                if random.random() < node.q:
                    node.state = "DEAD"
                    dead_nodes.append(node.id)
                    ill_nodes.remove(node.id)
                    logging.info(f"Node {node.id} is DEAD because of the virus.")
                    flag_event = True
                    
                # If the node stays alive for T_max timestamps, it's considered healed and it's removed
                # from the lists of contagious and ill nodes.
                elif node.t_ill > T_max:
                    node.state = "RECOVERED"
                    recovered_nodes.append(node.id)
                    ill_nodes.remove(node.id)
                    logging.info(f"Node {node.id} has been countagious for {T_max} timestamps, it is now RECOVERED.")    
                    flag_event = True
                    
        # Just to print something in case of no event occurred during the current timestamp.            
        if flag_event == False:
            logging.info(f'{"No events occurred."}')
        
        '''
        plt.ioff()
        plt.figure(figsize=(8,5))
        nx.draw(G, pos=pos, node_color=[color_state_map.get(node.state)
                    for node in nodes], with_labels=True, node_size=500, font_color='white')
        plt.savefig(str(t)+'.png')
        '''
        
        # If either all the nodes are recovered or all the nodes are dead or all the nodes are 
        # either recovered or dead, stop the simulation; no changes can occur.
        if len(recovered_nodes) == len(nodes) or len(dead_nodes) == len(nodes) or\
            (len(recovered_nodes)+len(dead_nodes)) == len(nodes) or\
                (len(contagious_nodes) == 0 and len(ill_nodes) == 0):
                break
    
    # End of the simulation.
    logging.info(f'{"Simulation has ended."}')
    logging.shutdown()
    
    # Finding the average iterations to die.
    iterations_to_die = 0
    for node in nodes:
        if node.state == "DEAD":
            iterations_to_die = iterations_to_die + node.t_ill
    
    # Here, some simulation stats are evaluated by observing the state of the
    # nodes, individually.
    counter_contagious = 0
    counter_ill = 0
    counter_deaths = 0
    counter_healthy = 0
    counter_recovered = 0
     
    for node in nodes:
        if node.state == "HEALTHY":
            counter_healthy = counter_healthy + 1
        elif node.state == "DEAD":
            counter_deaths = counter_deaths + 1
            counter_contagious = counter_contagious + 1
            counter_ill = counter_ill + 1
        elif node.state == "RECOVERED":
            counter_recovered = counter_recovered + 1
            counter_contagious = counter_contagious + 1
            counter_ill = counter_ill + 1
        elif node.state == "CONTAGIOUS":
            counter_contagious = counter_contagious + 1
        elif node.state == "ILL":
            counter_ill = counter_ill + 1
            counter_contagious = counter_contagious + 1
    
    # Returning the simulation stats, dividing the case in which no deaths
    # occurred from the case in which deaths occurr. To avoid division by
    # zero in the stats.
    if flag_optimal:
        return({"N_nodes": len(nodes), \
                    "lambda": lambd, \
                    "h": h, \
                    "T_max": T_max, \
                    "total_healthy": counter_healthy, \
                    "total_contagious": counter_contagious, \
                    "total_ill": counter_ill, \
                    "total_dead": counter_deaths, \
                    "total_recovered": counter_recovered
                    })
    else:
        perc_ill = float(round(counter_ill/len(nodes), 2))
        perc_contagious = float(round(counter_contagious/len(nodes), 2))
        perc_dead = float(round(counter_deaths/len(nodes), 2))
        
        diff_contage = abs(counter_contagious - int(len(nodes)*perc_contage))
        diff_deaths = abs(counter_deaths - int(len(nodes)*perc_deaths))
    
        if counter_deaths == 0:
            return({"N_nodes": len(nodes), \
                    "lambda": lambd, \
                    "h": h, \
                    "T_max": T_max, \
                    "total_healthy": counter_healthy, \
                    "total_contagious": counter_contagious, \
                    "total_ill": counter_ill, \
                    "total_dead": counter_deaths, \
                    "total_recovered": counter_recovered, \
                    "contagious_percentage": perc_contagious, \
                    "ill_percentage": perc_ill, \
                    "death_percentage": perc_dead, \
                    "avg_iterations_to_die": 0, \
                    "diff_contage": diff_contage,\
                    "diff_deaths": diff_deaths, \
                    "sum_of_diffs": diff_contage + diff_deaths
                    })
        else:
            return({"N_nodes": len(nodes), \
                    "lambda": lambd, \
                    "h": h, \
                    "T_max": T_max, \
                    "total_healthy": counter_healthy, \
                    "total_contagious": counter_contagious, \
                    "total_ill": counter_ill, \
                    "total_dead": counter_deaths, \
                    "total_recovered": counter_recovered, \
                    "contagious_percentage": perc_contagious, \
                    "ill_percentage": perc_ill, \
                    "death_percentage": perc_dead, \
                    "avg_iterations_to_die": float(round(iterations_to_die/counter_deaths,2)), \
                    "diff_contage": diff_contage, \
                    "diff_deaths": diff_deaths, \
                    "sum_of_diffs": diff_contage + diff_deaths
                    })

# This method is exclusively used tu launch the final simulation having fixed
# the triplet (h, T, lambda) that jointly satisfies the virus targets and
# maximizes the amount the deaths among the nodes of the network.
def final_simulation(log_file, lambd, h, T_max, pl, SIM_LIM, patient_zero_degree=None, first_node_id=None):
    
    log_name = "./logs/" + log_file
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        force=True,
        filemode='w'
        # The format specifies the format of each line of the log, an example is
        # 14:14:27 INFO starting simulation...
    )
    
    random.seed(random.choice(range(100)))
    
    # Retrieve the simulation duration from instance.
    SIM_LIM = SIM_LIM
    
    # Retrieve the list of nodes populating the graph from instance.
    nodes = pl
    
    for node in nodes:
        node.t = -1
        node.t_ill = 0
        node.state = "HEALTHY"
        node.p = 0
        node.q = 0
        node.viral_q = 0

    # Initializing empty list for contagious and ill nodes.
    contagious_nodes = []
    ill_nodes = []
    dead_nodes = []
    recovered_nodes = []
    
    # Initializing the lists and counters used to plot healthy, ill, recovered and dead curves.
    # for each timestamp of the simulation a value must be added to each of these
    # lists.
    plot_healthy_nodes = []
    plot_contagious_nodes = []
    plot_ill_nodes = []
    plot_recovered_nodes = []
    plot_dead_nodes = []
    plot_healthy_counter = len(pl)
    plot_contagious_counter = 0
    plot_ill_counter = 0
    plot_recovered_counter = 0
    plot_dead_counter = 0
    
    logging.info(f"Starting the simulation with h={h}, T_max={T_max}, lambda={lambd}...")
    
    # Starting the simulation from t=0.    
    for t in range(SIM_LIM):
        
        flag_event = False
        logging.info(f"Timestamp t={t}:")
        # Set the first node as contagious at random, like if we were in t = 0.
        if t == 0:
            # Selecting as patient zero a node that satisfies the provided degree.
            if first_node_id==None:
                contagious_node = random.choice([node for node in nodes if node.degree_cat == patient_zero_degree])
                #contagious_node = random.choice(nodes)
            else:
                contagious_node = rnodes[first_node_id]
                
            contagious_node.state = "CONTAGIOUS"
            contagious_node.t = contagious_node.t + 1
            contagious_node.p = contagious_node.alpha*(1 - math.exp(-lambd*contagious_node.t))
            contagious_node.viral_q = 1 - math.exp(-lambd*contagious_node.t)
            contagious_nodes.append(contagious_node.id)
            logging.info(f"Node {contagious_node.id} is set to CONTAGIOUS.")
            
            # Updating and appending counters for the plot.
            plot_healthy_counter = plot_healthy_counter - 1
            plot_contagious_counter = plot_contagious_counter + 1
            plot_healthy_nodes.append(plot_healthy_counter)
            plot_contagious_nodes.append(plot_contagious_counter)
            plot_ill_nodes.append(plot_ill_counter)
            plot_recovered_nodes.append(plot_recovered_counter)
            plot_dead_nodes.append(plot_dead_counter)
            continue
            
        for node in nodes:
            # In case the current node is either healthy, dead or recovered, it cannot infect
            # other nodes, hence we skip this node.
            if node.state == "HEALTHY" or node.state == "DEAD" or node.state == "RECOVERED":
                continue
            # Otherwise, continue.
            elif node.state == "CONTAGIOUS":
                # Updating the p, viral quantity and local timestamp of the contagious node/person
                # for the current timestamp.
                node.t = node.t + 1
                node.p = node.alpha*(1 - math.exp(-lambd*node.t))
                node.viral_q = 1 - math.exp(-lambd*node.t)
                
                # If the viral quantity exceedes the threshold, the node becomes ill. We change its
                # state, append its id to the ill list and add a penalty to the timestamps to heal.
                if node.viral_q >= h:
                    node.state = "ILL"
                    node.t_ill = node.t_ill + 1
                    node.q = node.beta*(1 - math.exp(-lambd*node.t_ill))
                    ill_nodes.append(node.id)
                    contagious_nodes.remove(node.id)
                    logging.info(f"Node {node.id}'s viral quantity exceeded h, it is now ILL.")
                    flag_event = True
                    
                    # Updating counters for the plot.
                    plot_ill_counter = plot_ill_counter + 1
                    plot_contagious_counter = plot_contagious_counter - 1
                    
                else:
                    # Once the node is contagious, and didn't get ill already, we have to check whether 
                    # its neighbors become contagious too or not
                    for neighbor in node.neighborhood:
                        # If the node is not already contagious and it gets infected, 
                        # it becomes contagious.
                        if nodes[neighbor].state == "HEALTHY" and random.random() < node.p:
                            # Now that the node/person is contagious its parameters p, q, viral quantity
                            # are initialized
                            nodes[neighbor].state = "CONTAGIOUS"
                            nodes[neighbor].t = nodes[neighbor].t + 1
                            nodes[neighbor].p = nodes[neighbor].alpha*(1 - math.exp(-lambd*nodes[neighbor].t))
                            nodes[neighbor].viral_q = 1 - math.exp(-lambd*nodes[neighbor].t)
                            # We append the new contagious node id to the list.
                            contagious_nodes.append(nodes[neighbor].id)
                            logging.info(f"Node {neighbor} is now CONTAGIOUS, it has been infected by node {node.id}.")
                            flag_event = True
                            
                            # Updating counters for the plot.
                            plot_contagious_counter = plot_contagious_counter + 1
                            plot_healthy_counter = plot_healthy_counter - 1
            
            # If the node is ill...
            elif node.state == "ILL":
                node.t_ill = node.t_ill + 1
                node.q = node.beta*(1 - math.exp(-lambd*node.t_ill))
                
                # Checking if the node can die, if the probability is higher tha its q.
                if random.random() < node.q:
                    node.state = "DEAD"
                    dead_nodes.append(node.id)
                    ill_nodes.remove(node.id)
                    logging.info(f"Node {node.id} is DEAD because of the virus.")
                    flag_event = True
                    
                    # Updating counters for the plot.
                    plot_ill_counter = plot_ill_counter - 1
                    plot_dead_counter =plot_dead_counter + 1
                    
                # If the node stays alive for T_max timestamps, it's considered healed and it's removed
                # from the lists of contagious and ill nodes.
                elif node.t_ill > T_max:
                    node.state = "RECOVERED"
                    recovered_nodes.append(node.id)
                    ill_nodes.remove(node.id)
                    logging.info(f"Node {node.id} has been countagious for {T_max} timestamps, it is now RECOVERED.")    
                    flag_event = True
                    
                    # Updating counters for the plot.
                    plot_ill_counter = plot_ill_counter - 1
                    plot_recovered_counter = plot_recovered_counter + 1
                    
        # Just to print something in case of no event occurred during the current timestamp.            
        if flag_event == False:
            logging.info(f'{"No events occurred."}')
        
        # Appending counters to the lists for the plot.
        plot_healthy_nodes.append(plot_healthy_counter)
        plot_contagious_nodes.append(plot_contagious_counter)
        plot_ill_nodes.append(plot_ill_counter)
        plot_recovered_nodes.append(plot_recovered_counter)
        plot_dead_nodes.append(plot_dead_counter)
        
        # If either all the nodes are recovered or all the nodes are dead or all the nodes are 
        # either recovered or dead, stop the simulation; no changes can occur.
        if len(recovered_nodes) == len(nodes) or len(dead_nodes) == len(nodes) or\
            (len(recovered_nodes)+len(dead_nodes)) == len(nodes) or\
                (len(contagious_nodes) == 0 and len(ill_nodes) == 0):
                break
    
    # End of the simulation.
    logging.info(f'{"Simulation has ended."}')
    logging.shutdown()
    
    # Here, some simulation stats are evaluated by observing the state of the
    # nodes, individually.
    counter_contagious = 0
    counter_ill = 0
    counter_deaths = 0
    counter_healthy = 0
    counter_recovered = 0
     
    for node in nodes:
        if node.state == "HEALTHY":
            counter_healthy = counter_healthy + 1
        elif node.state == "DEAD":
            counter_deaths = counter_deaths + 1
            counter_contagious = counter_contagious + 1
            counter_ill = counter_ill + 1
        elif node.state == "RECOVERED":
            counter_recovered = counter_recovered + 1
            counter_contagious = counter_contagious + 1
            counter_ill = counter_ill + 1
        elif node.state == "CONTAGIOUS":
            counter_contagious = counter_contagious + 1
        elif node.state == "ILL":
            counter_ill = counter_ill + 1
            counter_contagious = counter_contagious + 1
    
    # Creating a dateframe including the lists to be plotted.
    df_plot = pd.DataFrame([plot_healthy_nodes, plot_contagious_nodes, plot_ill_nodes, plot_recovered_nodes, plot_dead_nodes],\
                           index=['healthy', 'contagious', 'ill', 'recovered', 'dead'])
    
    # Returning the simulation stats, dividing the case in which no deaths
    # occurred from the case in which deaths occurr. To avoid division by
    # zero in the stats.
    return({"N_nodes": len(nodes), \
                "lambda": lambd, \
                "h": h, \
                "T_max": T_max, \
                "total_healthy": counter_healthy, \
                "total_contagious": counter_contagious, \
                "total_ill": counter_ill, \
                "total_dead": counter_deaths, \
                "total_recovered": counter_recovered
                }, df_plot)
