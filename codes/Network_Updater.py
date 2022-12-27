""" with this function, the user can adjust some run time parameters and models. 
--for plugging in dynamic models and using dynamic algorithms in the network run-time 
you can use the Network_Updater.py file
-- for parameters adjustment in the network run-time, you can use the Network_Updater.py file
"""
from detect_neighbor import detect_neighbor
from choice_feature import choice_feature
import pymobility
from pymobility.models.mobility import random_waypoint
import networkx as nx
import random
import matplotlib.pyplot as plt
from pylab import plot, show, savefig, xlim, figure, \
                 ylim, legend, boxplot, setp, axes
from initializer import *

def update_configurations_models(nodes, NUMBER_NODES, NODE_RANGE, NUMBER_RELAY_NODE, NUMBER_RELAY_G_NODE, ENVIRONMENT,Gar):
    global mobility_flag   # mobility flag determines the number of mobility updates during the simulation
    global update_flag  # update flag determines the presence of run-time adjustment for parameters
    # and models during the simulation
    ###################### our mobility model####################
    if mobility_flag > 0:
        mobility_flag += 1
        Gar = nx.Graph()
        positions = next(rw)
        for i1 in range(NUMBER_NODES):  # the positions of the nodes come from pymobility model
            nodes[i1].Xposition = positions[i1][0]
            nodes[i1].Yposition = positions[i1][1]
            # the positions of the nodes add to the network topology graph
            Gar.add_node(nodes[i1].ID, pos=(nodes[i1].Xposition, nodes[i1].Yposition))
    ###########################detecting neighbor#######################################
        for node_source in range(NUMBER_NODES):
            # by calling the detect_neighbor function the neighbors of each node is determined
            neighbor = detect_neighbor(node_source, NODE_RANGE, NUMBER_NODES, nodes, Gar)
            nodes[node_source].neighbors = neighbor
    ########## drawing network topology#################
        # print(nx.info(Gar))
        # fig = figure()
        # nx.draw(Gar, with_labels=True)
        # plt.savefig("mobility"+str(mobility_flag-1)+'.png', dpi=200, bbox_inches='tight')
####### Our run time algorithms for determining relay and center nodes ########
    if update_flag > 0:
        # we use the closeness centrality characteristic in the network topology for choosing the sink node 
        closeness = nx.closeness_centrality(Gar)  
        Sink = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:1]
        Center_node = Sink[0][0]
        # we use the betweenness centrality characteristic in the network topology for choosing the relay nodes
        Betweenness = nx.betweenness_centrality(Gar)
        best_Relay = sorted(Betweenness.items(), key=lambda x: x[1], reverse=True)[:NUMBER_RELAY_NODE]
        best_G_Relay = sorted(Betweenness.items(), key=lambda x: x[1], reverse=True)[NUMBER_RELAY_NODE:NUMBER_RELAY_G_NODE
                                                                                                       + NUMBER_RELAY_NODE]
        for j1 in range(NUMBER_RELAY_NODE):
            Relay_Node.append(best_Relay[j1][0])
        for j1 in range(NUMBER_RELAY_G_NODE):
            Relay_G_Node.append(best_G_Relay[j1][0])
    ####################choosing feature#######################################
    # with this part, the user can use algorithms  to determine the features of
        # the nodes during the simulation as run time updates
        for i_f in range(NUMBER_NODES):  
            choice_feature(nodes, i_f, Center_node, Relay_Node, Relay_G_Node)
        #################### run time parameters adjustment ###################
        # BMSim has the capability to adjust some important network parameters during the simulation
        global BUFFER_SIZE, reception_ratio
        for i_up in range(NUMBER_NODES):
            nodes[i_up].Heartbeat_period = 0
            nodes[i_up].GENERATION_INTERVAL = 1000
            nodes[i_up].Relay_Retransmit_Count = 0
            nodes[i_up].Network_Transmit_Count = 0
            nodes[i_up].Rris = 1
            nodes[i_up].Ntis = 1
            nodes[i_up].SCAN_WINDOW = 30
            nodes[i_up].SCAN_INTERVAL = 30
            nodes[i_up].Advertise_Interval = 20
        nodes[Center_node].Heartbeat_period = 0
        BUFFER_SIZE = 6
        NETWORK_TTL = NUMBER_NODES
        #############choosing a dynamic model for reception_ratio ##############
        reception_ratio = [[100 for x in range(NUMBER_NODES)] for y in range(NUMBER_NODES)]
    else:
        Center_node = Center_node_static
    return nodes, Center_node
