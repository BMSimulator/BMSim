""" Settings of the BM network is specified in this file.
It can be used for plugging in static models and using static algorithms
 at the network design time.
 """
import random
import networkx as nx
import numpy as np
from node import node
import pymobility
from pymobility.models.mobility import random_waypoint
from logger import setup_logger
import logging
from detect_neighbor import detect_neighbor
from choice_feature import choice_feature
import matplotlib.pyplot as plt
import math
from pylab import plot, show, savefig, xlim, figure, \
                 ylim, legend, boxplot, setp, axes

#############global variables##################
global update_mobility_interval, lowpower_Poll_interval
global BUFFER_SIZE, reception_ratio
global NUMBER_NODES, ENVIRONMENT, NUMBER_RELAY_NODE, NUMBER_RELAY_G_NODE
global heartbeat_log, logger, energy_log, mobility_flag, R_h, x, y, next_update, Relay_Node, Relay_G_Node
global NETWORK_TTL, PACKET_LENGTH, EXECUTION_TIME, TOTAL_LOG, BYTE, DATA_RATE, SCAN_STEP, SWITCH_TIME
global Advertise_time, Receive_Delay, sleep_time, Receive_window, destination, max_seq
global GENERATION_EVENT_Adv37, HEARTBEAT_EVENT_Adv37, RELAY_EVENT_Adv37, AD38_EVENT, AD39_EVENT, AD39_EVENT_End
global SCAN37_EVENT, SCAN38_EVENT, SCAN39_EVENT, SCAN37_C_EVENT, SCAN38_C_EVENT, SCAN39_C_EVENT, SWITCH_37TO38
global SWITCH_38TO39, SEND_POLL, FRIEND_RELAY, NODE_TIME, NODE_EVENT, Time, i_node
global SINK_NODE, JUST_RELAY, JUST_GENERATION, RELAY_AND_GENERATION, LOW_POWER, FRIEND_RELAY_NODE, FRIEND_NODE
global nodes, Center_node, Center_node_static, Show_progress_interval, Show_progress
#########################################
#######  initial settings ##############
###### deployment setting ###########
NUMBER_NODES = 11  # the number of nodes in the network
x = []  # the positions of nodes in the network
y = []
# x = [35, 39, 11, 12, 11, 1, 30, 9, 22, 40, 21]
# y = [6, 1, 43, 24, 32, 2, 17, 25, 7, 25]

##################grid deployment ############
for i17 in range(
        int(NUMBER_NODES / math.sqrt(NUMBER_NODES)) + 5):
    for j17 in range(int(NUMBER_NODES / math.sqrt(NUMBER_NODES))):
        # x = random.randint(1,ENVIRONMENT)
        x.append(9 * i17)
        # y = random.randint(1,ENVIRONMENT)
        y.append(9 * j17)
##############################################

ENVIRONMENT = 25  # the dimension of the environment (square) i meters that the network nodes are spread in it

NUMBER_RELAY_NODE = int(1/3*NUMBER_NODES)  # number of nodes with relay feature in the network
NUMBER_RELAY_G_NODE = int(1/6*NUMBER_NODES)  # number of nodes with relay and generator features in the network
NODE_RANGE = 11.26  # the communication range of the nodes, assumin a unit disk model
EXECUTION_TIME = 30000  # the execution time of the simulator in milliseconds
#####loging##
"""when TOTAL_LOG is one, each node has a separate log file
 with detailed data about its operations during network simulation. 
when TOTAL_LOG is zero, there is one log file for all network nodes.
 In this file, the data needed for calculating performance metrics are logged
"""
TOTAL_LOG = 0
heartbeat_log = 0  # when set to one, some information in detailed log files in each node about
# the heartbeat messages is logged
##############network setting#############
R_h = 2  # used in determining TTL by heartbeat message, this variable is added to min hop for determining the TTL  
mobility_flag = 0  # mobility flag determines the number of mobility updates during the simulation
update_flag = 0  # update flag determines the presence of run-time adjustment
# for parameters and models during the simulation
BUFFER_SIZE = 6  # the size of the nodes' buffer
Show_progress_interval = EXECUTION_TIME/100  # the resolution (%) of the simulation progress
update_mobility_interval = 1000  # The interval for calling the Network_updator module (in milisecond) 
NETWORK_TTL = NUMBER_NODES  # the initial value for the network's TTL if the user
# does not want to use the heartbeat message
#######lowpower and friend #####
Receive_Delay = 10  # the Receive Delay parameter in friendship mechanismb (ms)
sleep_time = 5      # the sleep time in friendship mechanism (ms)
Receive_window = 98  # the Receive window parameter in friendship mechanism( ms)
lowpower_Poll_interval = 4000  # the request[friend poll] interval parameter in friendship mechanism (ms)
#####################
logger = []
energy_log = []
destination = []
max_seq = []
Gar = nx.Graph()
Relay_Node = []
Relay_G_Node = []
Show_progress = 0
Show_progress = 0 + Show_progress_interval
next_update = 0
next_update = 0 + update_mobility_interval
#########initialize nodes#######################
nodes = []
for i1 in range(NUMBER_NODES):  
    nodes.append(node(i1, x[i1], y[i1]))  # the positions of the nodes are add to them
    # the positions of the nodes are added to the network topology
    Gar.add_node(nodes[i1].ID, pos=(nodes[i1].Xposition, nodes[i1].Yposition))
for i_r in range(NUMBER_NODES):
    ########## node setting ###########
    nodes[i_r].SCAN_INTERVAL = 30
    nodes[i_r].SCAN_WINDOW = 30
    nodes[i_r].Relay_Retransmit_Count = 0
    nodes[i_r].Network_Transmit_Count = 0
    nodes[i_r].Rris = 1
    nodes[i_r].Ntis = 1
    nodes[i_r].Advertise_Interval = 20
    nodes[i_r].GENERATION_INTERVAL = 1000
    nodes[i_r].Relay_Retransmission_Interval = (nodes[i_r].Rris + 1) * 10 + random.randint(1, 10)
    # Relay_Retransmission_Interval
    nodes[i_r].Transmission_Interval = (nodes[i_r].Ntis + 1) * 10 + random.randint(1, 10)  # Transmission_Interval
    ##########Initial value ##############
    nodes[i_r].cache = []
    nodes[i_r].buffer = []
    nodes[i_r].keynet = []
    nodes[i_r].channel37 = 0
    nodes[i_r].channel38 = 0
    nodes[i_r].channel39 = 0
    nodes[i_r].advertisetag37 = 0  # these flags are used for collisions detection
    nodes[i_r].advertisetag38 = 0
    nodes[i_r].advertisetag39 = 0
    nodes[i_r].message = 0
    nodes[i_r].L_scan = 8  # the last scanning channel for determining the next scanning channel 
    nodes[i_r].first_time_scan = 0  # the beginning of the scan window is saved in each node
    nodes[i_r].seq_number = 0
    nodes[i_r].h_seq_number = 0
    nodes[i_r].Gen_cache = []
    nodes[i_r].heart_cache = []
    nodes[i_r].Sleep_Time = 0  # the node sleeping time
    nodes[i_r].Scan_Time = 0  # the node scanning time
    nodes[i_r].low_power_ack = 0
    nodes[i_r].Switch_Time = 0  # the node switching time
    nodes[i_r].Transmit_Time = 0  # the node transmission time 
    nodes[i_r].node_TTL = 127  # the initial value for the nodes' TTL
    nodes[i_r].n_count = 0  # this variable is used for counting the retransmissions in the generator nodes
    nodes[i_r].r_count = 0  # this variable is used for counting the retransmissions in the relay nodes 
    nodes[i_r].minhop = 127
    nodes[i_r].maxhop = 0
    nodes[i_r].Sleep_Time = 0
    nodes[i_r].init_time = 0
    ########## Initial random value########
    # it is necessary to save the last time of executing each event, for calculating the next time of executing this event
    # the last time that the retransmission event is executed  in the relay nodes
    nodes[i_r].last_T_relay = random.randint(0, nodes[i_r].Relay_Retransmission_Interval)
    # the last time that the retransmission event is executed  in the generator nodes
    nodes[i_r].last_T_generation = random.randint(0, nodes[i_r].Transmission_Interval)
    # the last time that advertising event is executed  in the nodes
    nodes[i_r].last_relay_time = random.randint(0, nodes[i_r].Advertise_Interval)
    # the last time that scanning event is executed  in the nodes
    nodes[i_r].last_t_scan = random.randint(0, nodes[i_r].SCAN_INTERVAL)
    # the last time that sending request[friend poll] event is executed in the low-power nodes
    nodes[i_r].last_poll_time = random.randint(0, lowpower_Poll_interval)
    # the last time that the heartbeat event is executed in the nodes
    nodes[i_r].time_heartbeat = random.randint(0, 1000)
    nodes[i_r].last_seq_number = np.full(NUMBER_NODES, 0)
    nodes[i_r].h_last_seq_number = np.full(NUMBER_NODES, 0)

for i1 in range(NUMBER_NODES):
    # the last time that generation event is executed  in the generator nodes
    nodes[i1].last_generation_time = random.randint(0, nodes[i1].GENERATION_INTERVAL)

##########statice algorithms ##############
############detect neighbors ##########
# by calling the detect_neighbor function the neighbors of each node is determined
for node_source in range(NUMBER_NODES):  
    neighbor = detect_neighbor(node_source, NODE_RANGE, NUMBER_NODES, nodes, Gar)
    nodes[node_source].neighbors = neighbor
#########plot network topology##########
print(nx.info(Gar))
fig = figure()
nx.draw(Gar, with_labels=True)
plt.savefig('topology.png', dpi=200, bbox_inches='tight')
# plt.show()
####### static algorithms for determining center node and relay nodes########################
# we use the closeness centrality characteristic in the network topology for choosing the sink node
closeness = nx.closeness_centrality(Gar)  
Sink = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:1]
Center_node = Sink[0][0]
Center_node_static = Center_node
# we use the betweenness centrality characteristic in the network topology for choosing the relay nodes
Betweenness = nx.betweenness_centrality(Gar) 
best_Relay = sorted(Betweenness.items(), key=lambda x: x[1], reverse=True)[:NUMBER_RELAY_NODE]
best_G_Relay = sorted(Betweenness.items(), key=lambda x: x[1], reverse=True)[
               NUMBER_RELAY_NODE:NUMBER_RELAY_G_NODE + NUMBER_RELAY_NODE]
for j1 in range(NUMBER_RELAY_NODE):
    Relay_Node.append(best_Relay[j1][0])
for j1 in range(NUMBER_RELAY_G_NODE):
    Relay_G_Node.append(best_G_Relay[j1][0])
####################choice feature############
# by calling the choice_feature function the feature of each node is determined
for i_f in range(NUMBER_NODES):
    choice_feature(nodes, i_f, Center_node, Relay_Node, Relay_G_Node)
#################### Heartbeat_period #######################################
for i_heart in range(NUMBER_NODES):
    nodes[i_heart].Heartbeat_period = 0
nodes[Center_node].Heartbeat_period = 4000
############# choose a static model for reception_ratio ##############
reception_ratio = [[100 for x in range(NUMBER_NODES)] for y in range(NUMBER_NODES)]
#############constants##############
all_event = []  # the array for saving all network events and their time
DATA_RATE = 1000
PACKET_LENGTH = 38
BYTE = 8
SCAN_STEP = 0.2  # each scan function increases the simulator's current time as much as  SCAN_STEP = 0.2 ms
SWITCH_TIME = 0.15  # when the node switches between channels, it takes time as much as SWITCH_TIME (ms)
Advertise_time = (PACKET_LENGTH * BYTE) / DATA_RATE  # when the node advertises a packet,
# it takes time as much as Advertise_time
### define events#####
GENERATION_EVENT_Adv37 = 1
HEARTBEAT_EVENT_Adv37 = 11
RELAY_EVENT_Adv37 = 2
AD38_EVENT = 3
AD39_EVENT = 4
AD39_EVENT_End = 5
SCAN37_EVENT = 6
SCAN38_EVENT = 7
SCAN39_EVENT = 8
SCAN37_C_EVENT = 60
SCAN38_C_EVENT = 70
SCAN39_C_EVENT = 80
SWITCH_37TO38 = 9
SWITCH_38TO39 = 10
SEND_POLL = 12
FRIEND_RELAY = 13
NODE_TIME = 0
NODE_EVENT = 1
### define features####
SINK_NODE = 0
JUST_RELAY = 1
JUST_GENERATION = 2
RELAY_AND_GENERATION = 3
LOW_POWER = 4
FRIEND_RELAY_NODE = 5  # FRIEND_RELAY_NODE
FRIEND_NODE = 6
#################################################
#######Initialize logging########################
# some settings for logging during the simulation
formatter = logging.Formatter('%(message)s')
energy_log = setup_logger('energy_log', 'energy' + '.log')
if TOTAL_LOG == 1:
    detail_log = setup_logger('detail_log', 'detail_log.log')
if TOTAL_LOG == 1:
    for init1 in range(NUMBER_NODES):
        logger.append(setup_logger(str(init1), str(init1) + '.log'))
else:
    logger = setup_logger('logger', 'network_detail' + '.log')
####### Initializing  events and their time ########################
for init in range(NUMBER_NODES):
    max_seq.append(0)
# the initial event times are compared with each other, and the event with the minimum time is chosen as the initial event
    if nodes[init].last_generation_time <= nodes[init].last_t_scan and \
            (nodes[init].feature == FRIEND_RELAY_NODE or nodes[init].feature == FRIEND_NODE or nodes[init].feature ==
             JUST_GENERATION or nodes[init].feature == RELAY_AND_GENERATION):
        First_time = nodes[init].last_generation_time  # determining the time of the first event in each node
        First_event = GENERATION_EVENT_Adv37  # determining the first event in each node
    elif nodes[init].feature == LOW_POWER:
        First_time = nodes[init].last_generation_time
        First_event = GENERATION_EVENT_Adv37
    else:
        First_time = nodes[init].last_t_scan
        First_event = SCAN37_EVENT
    list_node = [First_time, First_event]
    all_event.append(list_node)  # events and event's time are stored in this array
i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # The minimum time of events is specified
# then the event of this time is going to do.
Time = all_event[i_node][NODE_TIME]  # minimum time of events is selected as the simulator current time
# used in our mobility model (pymobility)
rw = random_waypoint(NUMBER_NODES, dimensions=(ENVIRONMENT, ENVIRONMENT), velocity=(0.25, 1.0), wt_max=10.0)
print("initial", all_event)

for init_t in range(NUMBER_NODES):
    nodes[init_t].init_time = all_event[init_t][0]
