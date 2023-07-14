# -*- coding: utf-8 -*-
"""
BMSim simulator
Created on Sat Feb 15 14:59:46 2020
@author Zohreh Hosseinkhani
  the core of the simulator is an event driven simulator. 
  the event with minimum time in the events array is executed then the current time of
  the simulator is updated to event's time.
  in the while true, there are some if conditions that check the events and do some works for executing each event.
  after executing each event, this event creates a new event, and the new event with its time
  is added to the events' array.
"""
import math
import time
import copy
import numpy as np
import random
import logging
import sys
from random import randint
from node import node
from friend_poll_message import friend_poll_message
from friend_updte import friend_update
from heartbeat_message import heartbeat_message
from message import message
from logger import setup_logger
from scan37 import Scan_function37
from scan38 import Scan_function38
from scan39 import Scan_function39
from initializer import *
from Network_Updater import *
from destinations import F_destination

##########################################################################
while True:  # events are executed in order of their time
    if round(Time) >= Show_progress:  # the simulator shows the percentage of simulation progress after
        # each Show_progress_interval
        print("progress", round((Time/EXECUTION_TIME)*100, 2))
        Show_progress = Show_progress + Show_progress_interval
    if round(Time) >= next_update:  # the simulator calls the Network_Updator module after each update_mobility_interval
        nodes, Center_node,reception_ratio = update_configurations_models(reception_ratio,nodes, NUMBER_NODES, nodes[i_node].NODE_RANGE,
                                                          NUMBER_RELAY_NODE, NUMBER_RELAY_G_NODE, ENVIRONMENT, Gar)
        next_update = next_update + update_mobility_interval
    if Time >= EXECUTION_TIME:  # the end of the simulation that is determined by the EXECUTION_TIME
        for i_l in range(NUMBER_NODES):
            if TOTAL_LOG == 0:
                print(max_seq[i_l])
                logger.info("%s", max_seq[i_l])  # the maximum sequence number for each node is
                # required for calculating PDR
            # some data is logged for estimating nodes' energy consumption at the end of the simulation
            nodes[i_l].Sleep_Time = EXECUTION_TIME - (nodes[i_l].Scan_Time + nodes[i_l].Switch_Time +
                                                     nodes[i_l].Transmit_Time + nodes[i_l].init_time)
            energy_log.info("%s   %s   %s   %s    %s", i_l, nodes[i_l].Scan_Time,
                            nodes[i_l].Switch_Time, nodes[i_l].Transmit_Time, nodes[i_l].Sleep_Time)
        break
    #########################################################################
    # in this event, the node generates a heartbeat message and advertises it on channel 37 
    if all_event[i_node][NODE_EVENT] == HEARTBEAT_EVENT_Adv37:
        for il in range(NUMBER_NODES):
            destination.append(il)  # determining the heartbeat message's destination
        destination.remove(Center_node)
        # destination.remove(nodes[5].LOW_POWER_ID)
        TTL = 127  # the TTL of the heartbeat message is set to 127
        # creating the heartbeat message
        message_generation1 = heartbeat_message(i_node, destination, nodes[i_node].feature, TTL, TTL)
        nodes[i_node].message = message_generation1
        nodes[i_node].message.generation_time = copy.deepcopy(Time)  # the message generation time is saved 
        nodes[i_node].advertising_37(nodes[i_node].message)  # advertising the heartbeat message on channel 37
        nodes[i_node].advertisetag37 = 1
        nodes[i_node].h_seq_number += 1  # the last sequence number for this node is increased 
        nodes[i_node].message.seq_number = nodes[i_node].h_seq_number  # the message sequence number is equal to
        # the last sequence number for this node
        nodes[i_node].time_heartbeat = all_event[i_node][NODE_TIME]
        nodes[i_node].h_last_seq_number[i_node] = nodes[i_node].h_seq_number
        all_event[i_node][NODE_TIME] += Advertise_time  # this event takes time as much as Advertise_time
        nodes[i_node].Transmit_Time += Advertise_time   # the transmitting time of the node is increased
        # as much as Advertise_time
        all_event[i_node][NODE_EVENT] = SWITCH_37TO38  # the next event that this event creates is SWITCH_37TO38
        destination = []
        # logging some information about heartbeat messages 
        if heartbeat_log == 1:
            logger[i_node].info("(heartbeat generate)    %s    %s    %s    %s", i_node, round(Time, 2),
                                nodes[i_node].message.destination,
                                nodes[i_node].message.seq_number)
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time
        # in the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ####################################################################################
    # in this event, the node generates a request [friend poll] message in low-power nodes and advertises
    # it on channel 37
    elif all_event[i_node][NODE_EVENT] == SEND_POLL:
        destination_f = []
        destination_f.append(nodes[i_node].friend_Id)  # determining the friend node as the friend poll
        # message's destination
        message_generation2 = friend_poll_message(i_node, destination_f)  # creating the friend poll message
        nodes[i_node].message = message_generation2
        nodes[i_node].message.generation_time = copy.deepcopy(Time)  # the message generation time is saved
        nodes[i_node].advertising_37(nodes[i_node].message)  # advertising the friend poll message on channel 37
        nodes[i_node].advertisetag37 = 1
        if nodes[i_node].not_receive == 0:  # updating the acknowledgment of low-power messages
            nodes[i_node].low_power_ack += 1  # when the message is received the acknowledgment is increased
            nodes[i_node].message.acknowledge = nodes[i_node].low_power_ack
        else:
            nodes[i_node].message.acknowledge = nodes[i_node].low_power_ack  # when the message is not received the
            # acknowledgment is the previous acknowledgment
        all_event[i_node][NODE_TIME] += Advertise_time  # this event takes time as much as Advertise_time
        nodes[i_node].Transmit_Time += Advertise_time  # the transmitting time of the node is
        # increased as much as Advertise_time
        all_event[i_node][NODE_EVENT] = SWITCH_37TO38  # the next event that this event creates is SWITCH_37TO38
        destination_f = []
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time in
        # the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ######################################################################################
    # in this event, the node generates a main message and advertises it on channel 37
    elif all_event[i_node][NODE_EVENT] == GENERATION_EVENT_Adv37:
        # Transmission Interval is used when there are re-transmissions in the generator nodes
        nodes[i_node].Transmission_Interval = (nodes[i_node].Ntis+1)*10 + random.randint(1, 10)
        if nodes[i_node].n_count == 0:  # first transmission
            # in this function, the node's destinations and TTL are determined
            destination1, data, TTL = F_destination(NUMBER_NODES, Center_node, nodes[i_node].node_TTL)
            message_generation = message(TTL, i_node, destination1, data)  # creating the main message
            nodes[i_node].Gen_cache.append(message_generation)  # the packet is appended to the generation cache 
            nodes[i_node].message = copy.deepcopy(nodes[i_node].Gen_cache[0])
            nodes[i_node].seq_number += 1  # the last sequence number for this node is increased
            max_seq[i_node] = nodes[i_node].seq_number  # the maximum sequence number for each node is
            # required for calculating PDR
            nodes[i_node].Gen_cache[0].seq_number = nodes[i_node].seq_number  # the message sequence number is equal to
            # the last sequence number for this node
            nodes[i_node].last_seq_number[i_node] = nodes[i_node].seq_number  # the last sequence number for
            # this node is updated
            nodes[i_node].last_generation_time = all_event[i_node][NODE_TIME]  # last_generation_time is used for
            # determining the time of next packet generation
            nodes[i_node].Gen_cache[0].generation_time = copy.deepcopy(Time)   # the message generation time is saved
            destination1 = []
            # logging some information about generated messages
            if TOTAL_LOG == 1:
                logger[i_node].info("(generate)    %s    %s    %s    %s", i_node,
                                    round(nodes[i_node].Gen_cache[0].generation_time, 2),
                                    message_generation.destination, nodes[i_node].Gen_cache[0].seq_number)
        nodes[i_node].message = copy.deepcopy(nodes[i_node].Gen_cache[0]) 
        nodes[i_node].advertising_37(nodes[i_node].message)  # advertising the generated message on channel 37
        nodes[i_node].advertisetag37 = 1
        # logging some information about advertising 
        if TOTAL_LOG == 1:
            detail_log.info("advertisetag37 %s node %s at Time %s with seq %s ", nodes[i_node].advertisetag37, i_node,
                            nodes[i_node].message.generation_time, nodes[i_node].message.seq_number)
        nodes[i_node].last_T_generation = all_event[i_node][NODE_TIME]  # last_T_generation is used for determining
        # the time of next packet retransmissions
        all_event[i_node][NODE_TIME] += Advertise_time  # this event takes time as much as Advertise_time
        nodes[i_node].Transmit_Time += Advertise_time  # the transmitting time of the node is
        # increased as much as Advertise_time
        all_event[i_node][NODE_EVENT] = SWITCH_37TO38  # the next event that this event creates is SWITCH_37TO38
        nodes[i_node].n_count += 1  # this variable is used for counting the retransmissions in the generator nodes
        if nodes[i_node].n_count >= (nodes[i_node].Network_Transmit_Count+1): # end of the retransmissions
            nodes[i_node].n_count = 0  # resetting the variable that counts the retransmissions
            nodes[i_node].Gen_cache.remove(nodes[i_node].Gen_cache[0])  # the packet is removed from
            # the generation cache
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time in
        # the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ###########################################
    # in this event, the friend node advertises the low-power node's packets on channel 37
    elif all_event[i_node][NODE_EVENT] == FRIEND_RELAY:
        if len(nodes[i_node].friend_queue) == 0:  # if there are not any packets in the friend queue, the friend node
            # sends the friend update message
            nodes[i_node].message = copy.deepcopy(friend_update(i_node, [nodes[i_node].LOW_POWER_ID]))
            nodes[i_node].message.friend_update = 1
            nodes[i_node].previous_ack = 1
        else:  # if there are packets in the friend queue, the friend node sends the first packet
            nodes[i_node].friend_queue[0].destination = [nodes[i_node].LOW_POWER_ID]
            nodes[i_node].message = copy.deepcopy(nodes[i_node].friend_queue[0])
            # logging some information about friendship mechanism
            if TOTAL_LOG == 1:
                detail_log.info("friend node  %s sends at Time %s desti %s ", i_node, all_event[i_node][NODE_TIME],
                                nodes[i_node].friend_queue[0].destination)
        nodes[i_node].advertising_37(nodes[i_node].message)  # advertising the low-power node's packet on channel 37
        nodes[i_node].advertisetag37 = 1
        all_event[i_node][NODE_EVENT] = SWITCH_37TO38  # the next event that this event creates is SWITCH_37TO38
        all_event[i_node][NODE_TIME] += Advertise_time  # this event takes time as much as Advertise_time
        nodes[i_node].Transmit_Time += Advertise_time  # the transmitting time of the node is increased
        # as much as Advertise_time
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time in
        # the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ###########################################
    # in this event, the relay node advertises its buffer's packets on channel 37 
    elif all_event[i_node][NODE_EVENT] == RELAY_EVENT_Adv37:
        # Relay Retransmission Interval is used when there are re-transmissions in the relay nodes
        nodes[i_node].Relay_Retransmission_Interval = (nodes[i_node].Rris + 1) * 10 + random.randint(1, 10)
        if nodes[i_node].r_count == 0:  # first transmission
            nodes[i_node].last_relay_time = all_event[i_node][NODE_TIME]  # last_relay_time is used for determining
            # the time of the next packet relaying
        nodes[i_node].message = copy.deepcopy(nodes[i_node].buffer[0])  # the advertising packet is
        # the first packet in the relay node buffer
        nodes[i_node].advertising_37(nodes[i_node].message)  # advertising the buffer's packet on channel 37
        if nodes[i_node].message.friend_poll == 0: 
            nodes[i_node].message.TTL -= 1  # decreasing packets' TTL in main and heartbeat messages
        nodes[i_node].advertisetag37 = 1
        # logging some information about relayed messages
        if TOTAL_LOG == 1 and nodes[i_node].message.friend_poll == 0:
            logger[i_node].info("(advertise)    %s    %s    %s    %s", i_node, round(Time, 2),
                                nodes[i_node].message.source,
                                nodes[i_node].message.seq_number)
            detail_log.info("advertisetag37 %s node %s at Time %s with seq %s ", nodes[i_node].advertisetag37, i_node,
                            all_event[i_node][NODE_TIME], nodes[i_node].message.seq_number)
        nodes[i_node].last_T_relay = all_event[i_node][NODE_TIME]  # last_T_relay is used for determining the time
        # of the next packet retransmissions in the relay nodes
        nodes[i_node].r_count += 1  # this variable is used for counting the retransmissions in the relay nodes
        if nodes[i_node].r_count >= (nodes[i_node].Relay_Retransmit_Count+1):  # end of the retransmissions
            nodes[i_node].r_count = 0  # resetting the variable that counts the retransmissions
            nodes[i_node].buffer.remove(nodes[i_node].buffer[0])  # the packet is removed from the relay node buffer
        all_event[i_node][NODE_EVENT] = SWITCH_37TO38  # the next event that this event creates is SWITCH_37TO38
        all_event[i_node][NODE_TIME] += Advertise_time  # this event takes time as much as Advertise_time
        nodes[i_node].Transmit_Time += Advertise_time  # the transmitting time of the node is increased
        # as much as Advertise_time
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time
        # in the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ##############################################
    # in this event, the node switches between channel 37 and channel 38
    elif all_event[i_node][NODE_EVENT] == SWITCH_37TO38:
        nodes[i_node].advertisetag37 = 0
        # logging some information about advertising  
        if TOTAL_LOG == 1:
            detail_log.info("advertisetag37 %s node %s at Time %s", nodes[i_node].advertisetag37, i_node,
                            all_event[i_node][NODE_TIME])
        all_event[i_node][NODE_TIME] += SWITCH_TIME  # this event takes time as much as SWITCH_TIME
        nodes[i_node].Switch_Time += SWITCH_TIME   # the switch time of the node is increased as much as SWITCH_TIME
        all_event[i_node][NODE_EVENT] = AD38_EVENT  # the next event that this event creates is AD38_EVENT
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time
        # in the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ###################################################
    
    # in this event, the node advertises the packets on channel 38 
    elif all_event[i_node][NODE_EVENT] == AD38_EVENT:
        nodes[i_node].advertising_38(nodes[i_node].message)  # advertising the packet on channel 38
        nodes[i_node].advertisetag38 = 1
        # logging some information about advertising
        if TOTAL_LOG == 1:
            detail_log.info("advertisetag38 %s node %s at Time %s", nodes[i_node].advertisetag38, i_node,
                            all_event[i_node][NODE_TIME])
        all_event[i_node][NODE_TIME] += Advertise_time  # this event takes time as much as Advertise_time
        nodes[i_node].Transmit_Time += Advertise_time  # the transmitting time of the node is
        # increased as much as Advertise_time
        all_event[i_node][NODE_EVENT] = SWITCH_38TO39  # the next event that this event creates is SWITCH_38TO39
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time
        # in the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ###########################################
    # in this event, the node switches between channel 38 and channel 39
    elif all_event[i_node][NODE_EVENT] == SWITCH_38TO39:
        nodes[i_node].advertisetag38 = 0
        # logging some information about advertising
        if TOTAL_LOG == 1:
            detail_log.info("advertisetag38 %s node %s at Time %s", nodes[i_node].advertisetag38, i_node,
                            all_event[i_node][NODE_TIME])
        all_event[i_node][NODE_TIME] += SWITCH_TIME  # this event takes time as much as SWITCH_TIME
        nodes[i_node].Switch_Time += SWITCH_TIME  # the switch time of the node is increased as much as SWITCH_TIME
        all_event[i_node][NODE_EVENT] = AD39_EVENT   # the next event that this event creates is AD39_EVENT
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))   # the event that has minimum time
        # in the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ###################################################
    # in this event, the node advertises the packets on channel 39
    elif all_event[i_node][NODE_EVENT] == AD39_EVENT:
        nodes[i_node].advertising_39(nodes[i_node].message)  # advertising the packet on channel 39
        nodes[i_node].advertisetag39 = 1
        # logging some information about advertising
        if TOTAL_LOG == 1:
            detail_log.info("advertisetag39 %s node %s at Time %s", nodes[i_node].advertisetag39, i_node,
                            all_event[i_node][NODE_TIME])
        all_event[i_node][NODE_TIME] += Advertise_time  # this event takes time as much as Advertise_time
        nodes[i_node].Transmit_Time += Advertise_time  # the transmitting time of the node is increased
        # as much as Advertise_time
        all_event[i_node][NODE_EVENT] = AD39_EVENT_End  # the next event that this event creates is AD39_EVENT_End
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time in
        # the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ###########################################
    #  in this event, the next event after advertising is determined  
    elif all_event[i_node][NODE_EVENT] == AD39_EVENT_End:
        nodes[i_node].advertisetag39 = 0
        # logging some information about advertising
        if TOTAL_LOG == 1:
            detail_log.info("advertisetag39 %s node %s at Time %s", nodes[i_node].advertisetag39, i_node,
                            all_event[i_node][NODE_TIME])
        all_event[i_node][NODE_TIME] += 0.001  # this event takes time as much as 0.001 ms
        if nodes[i_node].L_scan == SCAN37_EVENT:  # The previous scanning channel determines the next scanning channel 
            scan_event = SCAN38_EVENT
        elif nodes[i_node].L_scan == SCAN38_EVENT:
            scan_event = SCAN39_EVENT
        elif nodes[i_node].L_scan == SCAN39_EVENT:
            scan_event = SCAN37_EVENT
        elif nodes[i_node].L_scan == SCAN37_C_EVENT:
            scan_event = SCAN37_C_EVENT
        elif nodes[i_node].L_scan == SCAN38_C_EVENT:
            scan_event = SCAN38_C_EVENT
        elif nodes[i_node].L_scan == SCAN39_C_EVENT:
            scan_event = SCAN39_C_EVENT
        if nodes[i_node].SCAN_WINDOW == nodes[i_node].SCAN_INTERVAL: 
            next_Time_scan = all_event[i_node][NODE_TIME]  # the time of the next scanning is equal to current time
        elif nodes[i_node].SCAN_WINDOW < nodes[i_node].SCAN_INTERVAL:
            # calculating the time of the next scanning
            next_Time_scan = nodes[i_node].last_t_scan + (nodes[i_node].SCAN_INTERVAL-nodes[i_node].SCAN_WINDOW)
        for i_b in range(BUFFER_SIZE):  # discarding the packets that have TTL number one or lower
            if len(nodes[i_node].buffer) < 1:
                break
            if nodes[i_node].buffer[0].friend_poll == 0:
                if nodes[i_node].buffer[0].TTL < 2:
                    nodes[i_node].buffer.remove(nodes[i_node].buffer[0])
                    if len(nodes[i_node].buffer) < 1:
                        break
        """ determining the time of the next created event by the advertising 39 event 
         the events, heartbeat, relay, generation, retransmissions, and friend, low power events 
         are repeated during the simulation.
         in this part, first, the time of each event is determined and then compared with others,
          and the event with the minimum time is chosen as the next event """
        # time of the next heartbeat event
        heartbeat_time = nodes[i_node].time_heartbeat + nodes[i_node].Heartbeat_period
        # time of the next relay event
        relay_Time = nodes[i_node].last_relay_time + nodes[i_node].Advertise_Interval + random.randint(1, 10)
        # time of the next generation event
        Generat_Time = nodes[i_node].last_generation_time + nodes[i_node].GENERATION_INTERVAL
        # time of the next retransmission event in the relay nodes
        r_time1 = nodes[i_node].last_T_relay + nodes[i_node].Relay_Retransmission_Interval
        # time of the next retransmission event in the generator nodes
        G_time1 = nodes[i_node].last_T_generation + nodes[i_node].Transmission_Interval
        # time of the next sending request[friend poll ] event in the low-power nodes
        Poll_time = nodes[i_node].last_poll_time + lowpower_Poll_interval
        """ if there is retransmission in the relay and generator nodes, the interval
         is determined based on Ntis and Rtis
        otherwise is determined based on advertising interval """  
        if nodes[i_node].r_count > 0:  # this variable is used for counting the retransmissions in the relay nodes  
            r_time = r_time1   
        else:
            r_time = relay_Time  
        if nodes[i_node].n_count > 0:  # this variable is used for counting the retransmissions in the generator nodes 
            G_time = G_time1  
        else:
            G_time = Generat_Time  
        #***** finding the event with minimum time for creating the next event in the nodes with different features***#
        if nodes[i_node].feature == LOW_POWER:
            if nodes[i_node].message.friend_poll == 1:
                next_time = all_event[i_node][NODE_TIME] + Receive_Delay
                nodes[i_node].Low_Scan_Time = next_time  # Low_Scan_Time determines the first time that
                # the low-power node starts to scan
                all_event[i_node][NODE_EVENT] = scan_event
            elif G_time < Poll_time:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            elif G_time > Poll_time:
                next_time = Poll_time
                all_event[i_node][NODE_EVENT] = SEND_POLL
        elif nodes[i_node].feature == JUST_RELAY:  
            if heartbeat_time < next_Time_scan and heartbeat_time < r_time and nodes[i_node].Heartbeat_period > 0:  
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
                # in the relay event, it is necessary to check the capacity of the node buffer
            elif len(nodes[i_node].buffer) >= 1 and r_time < next_Time_scan:
                next_time = r_time
                all_event[i_node][NODE_EVENT] = RELAY_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == JUST_GENERATION or nodes[i_node].feature == FRIEND_NODE:  
            if nodes[i_node].Heartbeat_period > 0:
                min_time = min(heartbeat_time, G_time, next_Time_scan)
            else:
                min_time = min(G_time, next_Time_scan)
            if nodes[i_node].feature == FRIEND_NODE and min_time > nodes[i_node].response_friend_time:
                next_time = nodes[i_node].response_friend_time
                all_event[i_node][NODE_EVENT] = FRIEND_RELAY
                """ the response_friend_time get value when the friend node receives the request[friend pull ] 
                from the low-power node in scan 37-38-39 function
                 this value just is a initialization value """
                nodes[i_node].response_friend_time = nodes[i_node].response_friend_time + \
                                                     Receive_Delay + random.randint(0, Receive_window) + 100000
            elif heartbeat_time == min_time and nodes[i_node].Heartbeat_period > 0:
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif G_time < next_Time_scan:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == RELAY_AND_GENERATION or nodes[i_node].feature == FRIEND_RELAY_NODE:   
            if nodes[i_node].Heartbeat_period > 0 and len(nodes[i_node].buffer) >= 1:
                # in the relay event, it is necessary to check the capacity of the node buffer
                min_time = min(heartbeat_time, r_time, G_time, next_Time_scan)
            elif len(nodes[i_node].buffer) >= 1:
                min_time = min(r_time, G_time, next_Time_scan)
            else:
                min_time = min(G_time, next_Time_scan)
            if nodes[i_node].feature == FRIEND_RELAY_NODE and min_time > nodes[i_node].response_friend_time:
                next_time = nodes[i_node].response_friend_time
                all_event[i_node][NODE_EVENT] = FRIEND_RELAY
                """ the response_friend_time get value when the friend node receives the pull request from 
                the low-power node in scan 37-38-39 function
                 this value just is a initialization value """ 
                nodes[i_node].response_friend_time = nodes[i_node].response_friend_time + \
                                                     Receive_Delay + random.randint(0, Receive_window) + 100000
            elif heartbeat_time == min_time and nodes[i_node].Heartbeat_period > 0:  
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif min_time == r_time and len(nodes[i_node].buffer) >= 1:
                next_time = r_time
                all_event[i_node][NODE_EVENT] = RELAY_EVENT_Adv37
            elif next_Time_scan > G_time:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == SINK_NODE:
            if heartbeat_time < next_Time_scan and nodes[i_node].Heartbeat_period > 0:
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        #*********** end of finding the event with minimum time ***************#
        # the next_time variable is the time of the event that has the minimum time
        if all_event[i_node][NODE_TIME] < next_time:
            # if the next_time was after the current time, the next event's time is the next_time
            all_event[i_node][NODE_TIME] = next_time
        else:
            # if the next_time was before the current time, the next event's time is the current time
            # that means the node has been busy at next_time time and when the node finished the previous event,
            # the node has to start the new event.
            all_event[i_node][NODE_TIME] = all_event[i_node][NODE_TIME]
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))  # the event that has minimum time
        # in the events array is chosen as the next event
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    #########################################
        """the scanning process for the first time starts with SCAN37_EVENT, SCAN38_EVENT, and SCAN39_EVENT.
         then it continues with SCAN37_C_EVENT, SCAN38_C_EVENT, and SCAN39_C_EVENT events after each event the event
          that has the minimum time is determined
        all scan events take time as much as SCAN_STEP =0.2 ms which is the smallest events time in the events array """
    elif all_event[i_node][NODE_EVENT] == SCAN37_EVENT:
        nodes[i_node].first_time_scan = Time  # the beginning of the scan window is saved 
        all_event[i_node][NODE_TIME], all_event[i_node][NODE_EVENT] = \
            Scan_function37(nodes, i_node, all_event, NODE_TIME, NODE_EVENT, reception_ratio, logger, Time)
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))
        Time = all_event[i_node][NODE_TIME]
    ###########################################
    elif all_event[i_node][NODE_EVENT] == SCAN38_EVENT:
        nodes[i_node].first_time_scan = Time
        all_event[i_node][NODE_TIME], all_event[i_node][NODE_EVENT] = \
            Scan_function38(nodes, i_node, all_event, NODE_TIME, NODE_EVENT, reception_ratio, logger, Time)
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))
        Time = all_event[i_node][NODE_TIME]
    ########################################
    elif all_event[i_node][NODE_EVENT] == SCAN39_EVENT:
        nodes[i_node].first_time_scan = Time
        all_event[i_node][NODE_TIME], all_event[i_node][NODE_EVENT] =\
            Scan_function39(nodes, i_node, all_event, NODE_TIME, NODE_EVENT, reception_ratio, logger, Time)
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))
        Time = all_event[i_node][NODE_TIME]
    #########################################
    elif all_event[i_node][NODE_EVENT] == SCAN37_C_EVENT:
        p = all_event[i_node][NODE_TIME]  # this variable is used for determining the end of the scanning event  
        all_event[i_node][NODE_TIME], all_event[i_node][NODE_EVENT] = \
            Scan_function37(nodes, i_node, all_event, NODE_TIME, NODE_EVENT, reception_ratio, logger, Time)
        # discarding the packets that have TTL number one or lower 
        for i_b in range(BUFFER_SIZE):
            if len(nodes[i_node].buffer) < 1:
                break
            if nodes[i_node].buffer[0].friend_poll == 0:
                if nodes[i_node].buffer[0].TTL < 2:
                    nodes[i_node].buffer.remove(nodes[i_node].buffer[0])
                    if len(nodes[i_node].buffer) < 1:
                        break
        """ determining the time of the next created event by the SCAN37_C_EVEN event 
         the events, heartbeat, relay, generation, retransmissions, and friend, low power events are repeated during 
         the simulation.
        in this part, first, the time of each event is determined and then compared with others, and the event with
         the minimum time is chosen as the next event """
        scan_event = SCAN37_C_EVENT  # in this event, the next scan event is SCAN37_C_EVENT
        next_Time_scan = all_event[i_node][NODE_TIME]  # in this event, the next scan event time is the current time
        # because the node did not scan as much as the scan window
        if all_event[i_node][NODE_TIME] == p:  # in this condition, the node is at the end of the scan window
            # the next event that this event creates is SCAN38_EVENT
            scan_event = SCAN38_EVENT
            nodes[i_node].last_t_scan = all_event[i_node][NODE_TIME]
            # the time of the next scanning event
            next_Time_scan = nodes[i_node].last_t_scan + (nodes[i_node].SCAN_INTERVAL - nodes[i_node].SCAN_WINDOW)
        heartbeat_time = nodes[i_node].time_heartbeat + nodes[i_node].Heartbeat_period  # the time of the next heartbeat event
        # the time of the next relay event
        relay_Time = nodes[i_node].last_relay_time + nodes[i_node].Advertise_Interval + random.randint(1, 10)
        # time of the next generation event
        Generat_Time = nodes[i_node].last_generation_time + nodes[i_node].GENERATION_INTERVAL
        # time of the next retransmission event in the relay nodes
        r_time1 = nodes[i_node].last_T_relay + nodes[i_node].Relay_Retransmission_Interval
        # time of the next retransmission event in the generator nodes
        G_time1 = nodes[i_node].last_T_generation + nodes[i_node].Transmission_Interval
        """if there is retransmission in the relay and generator nodes,
         the interval is determined based on Ntis and Rtis
         otherwise is determined based on advertising interval """
        if nodes[i_node].r_count > 0:  # this variable is used for counting the retransmissions in the relay nodes
            r_time = r_time1  
        else:
            r_time = relay_Time 
        if nodes[i_node].n_count > 0:  # this variable is used for counting the retransmissions in the generator nodes
            G_time = G_time1 
        else:
            G_time = Generat_Time  
        #****** finding the event with minimum time for creating the next event in the nodes with different features **#
        if nodes[i_node].feature == JUST_RELAY:  
            if heartbeat_time < next_Time_scan and heartbeat_time < r_time and nodes[i_node].Heartbeat_period > 0:  
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif len(nodes[i_node].buffer) >= 1 and r_time < next_Time_scan:  # in the relay event, it is necessary to
                # check the capacity of the node buffer
                next_time = r_time
                all_event[i_node][NODE_EVENT] = RELAY_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == JUST_GENERATION or nodes[i_node].feature == FRIEND_NODE: 
            if nodes[i_node].Heartbeat_period > 0:
                min_time = min(heartbeat_time, G_time, next_Time_scan)
            else:
                min_time = min(G_time, next_Time_scan)
            if nodes[i_node].feature == FRIEND_NODE and min_time > nodes[i_node].response_friend_time:
                next_time = nodes[i_node].response_friend_time
                all_event[i_node][NODE_EVENT] = FRIEND_RELAY
                """ the response_friend_time get value when the friend node receives the pull request from the 
                low-power node in scan 37-38-39 function
                this value just is a initialization value """
                nodes[i_node].response_friend_time = nodes[i_node].response_friend_time + Receive_Delay +\
                                                     random.randint(0, Receive_window) + 100000
            elif heartbeat_time == min_time and nodes[i_node].Heartbeat_period > 0:
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif G_time < next_Time_scan:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == RELAY_AND_GENERATION or nodes[i_node].feature == FRIEND_RELAY_NODE:  
            if nodes[i_node].Heartbeat_period > 0 and len(nodes[i_node].buffer) >= 1:
                min_time = min(heartbeat_time, r_time, G_time, next_Time_scan)
            elif len(nodes[i_node].buffer) >= 1:
                min_time = min(r_time, G_time, next_Time_scan)
            else:
                min_time = min(G_time, next_Time_scan)
            if nodes[i_node].feature == FRIEND_RELAY_NODE and min_time > nodes[i_node].response_friend_time:
                next_time = nodes[i_node].response_friend_time
                all_event[i_node][NODE_EVENT] = FRIEND_RELAY
                """ the response_friend_time get value when the friend node receives the pull request from the low-power
                 node in scan 37-38-39 function
                this value just is a initialization value """
                nodes[i_node].response_friend_time = nodes[i_node].response_friend_time + Receive_Delay \
                                                     + random.randint(0, Receive_window) + 100000
            elif heartbeat_time == min_time and nodes[i_node].Heartbeat_period > 0: 
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif min_time == r_time and len(nodes[i_node].buffer) >= 1:
                next_time = r_time
                all_event[i_node][NODE_EVENT] = RELAY_EVENT_Adv37
            elif next_Time_scan > G_time:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event

        elif nodes[i_node].feature == SINK_NODE:
            if heartbeat_time < next_Time_scan and nodes[i_node].Heartbeat_period > 0:
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        #********** end of finding the event with minimum time ***********#
        elif nodes[i_node].feature == LOW_POWER:
            # when the next event is SEND_POLL or GENERATION_EVENT_Adv37 the times were set in the scan37-38-39 function
            # so the times are placed in the array and next_time variable.
            if all_event[i_node][NODE_EVENT] == SEND_POLL or all_event[i_node][NODE_EVENT] == GENERATION_EVENT_Adv37:
                all_event[i_node][NODE_EVENT] = all_event[i_node][NODE_EVENT]
                next_time = all_event[i_node][NODE_TIME]
            else:  # otherwise, the end of Receive Window is checked
                #  Low_Scan_Time determines the first time that the low-power node starts to scan
                remain1 = all_event[i_node][NODE_TIME]-nodes[i_node].Low_Scan_Time  # the low power node scanned
                # as much as the remain1
                if Receive_window <= remain1:
                    # that means until the end of receive window the low-power node did not receive the packet
                    # therefore after sleep_time sends a sending pull request
                    next_time = all_event[i_node][NODE_TIME] + sleep_time
                    all_event[i_node][NODE_EVENT] = SEND_POLL
                    nodes[i_node].not_receive = 1
                else:
                    all_event[i_node][NODE_EVENT] = scan_event
                    next_time = all_event[i_node][NODE_TIME]
        # the next_time variable is the time of the event that has the minimum time        
        if all_event[i_node][NODE_TIME] < next_time:
            # if the next_time was after the current time, the next event's time is next_time
            all_event[i_node][NODE_TIME] = next_time
        else:
            all_event[i_node][NODE_TIME] = all_event[i_node][NODE_TIME]  # if the next_time was before the current time,
            # the next event's time is the current time
            # that means the node has been busy at next_time and when the node finished the previous event,
            # the node has to start the new event.
        nodes[i_node].L_scan = SCAN37_C_EVENT
        # the previous scanning channel is saved for determining the next scanning channel
        if all_event[i_node][NODE_TIME] == p:  # in this condition, the node is at the end of the scan window
            nodes[i_node].L_scan = SCAN37_C_EVENT/10 # the previous scanning channel is saved for
            # determining the next scanning channel
        # the event that has minimum time in the events array is chosen as the next event
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))
        Time = all_event[i_node][NODE_TIME]  # the current time of the simulator is updated to the event's time
    ###############################################
        """this event is almost similar to the SCAN37_C_EVENT event please for comments reference the SCAN37_C_EVENT
        for giving more freedom to the developer in future development we preferred to write them in the separate events
         """
    elif all_event[i_node][NODE_EVENT] == SCAN38_C_EVENT:
        p = all_event[i_node][NODE_TIME]
        all_event[i_node][NODE_TIME], all_event[i_node][NODE_EVENT] = \
            Scan_function38(nodes, i_node, all_event, NODE_TIME, NODE_EVENT, reception_ratio, logger, Time)
        for i_b in range(BUFFER_SIZE):
            if len(nodes[i_node].buffer) < 1:
                break
            if nodes[i_node].buffer[0].friend_poll == 0:
                if nodes[i_node].buffer[0].TTL < 2:
                    nodes[i_node].buffer.remove(nodes[i_node].buffer[0])
                    if len(nodes[i_node].buffer) < 1:
                        break
        scan_event = SCAN38_C_EVENT
        next_Time_scan = all_event[i_node][NODE_TIME]
        if all_event[i_node][NODE_TIME] == p:
            scan_event = SCAN39_EVENT
            nodes[i_node].last_t_scan = all_event[i_node][NODE_TIME]
            next_Time_scan = nodes[i_node].last_t_scan + (nodes[i_node].SCAN_INTERVAL - nodes[i_node].SCAN_WINDOW)
        heartbeat_time = nodes[i_node].time_heartbeat + nodes[i_node].Heartbeat_period
        relay_Time = nodes[i_node].last_relay_time + nodes[i_node].Advertise_Interval + random.randint(1, 10)  
        Generat_Time = nodes[i_node].last_generation_time + nodes[i_node].GENERATION_INTERVAL 
        r_time1 = nodes[i_node].last_T_relay + nodes[i_node].Relay_Retransmission_Interval
        G_time1 = nodes[i_node].last_T_generation + nodes[i_node].Transmission_Interval
        if nodes[i_node].r_count > 0:  
            r_time = r_time1 
        else:
            r_time = relay_Time 
        if nodes[i_node].n_count > 0:  
            G_time = G_time1  
        else:
            G_time = Generat_Time 

        if nodes[i_node].feature == JUST_RELAY: 
            if heartbeat_time < next_Time_scan and heartbeat_time < r_time and nodes[i_node].Heartbeat_period > 0:  
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif len(nodes[i_node].buffer) >= 1 and r_time < next_Time_scan:
                next_time = r_time
                all_event[i_node][NODE_EVENT] = RELAY_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == JUST_GENERATION or nodes[i_node].feature == FRIEND_NODE:  
            if nodes[i_node].Heartbeat_period > 0:
                min_time = min(heartbeat_time, G_time, next_Time_scan)
            else:
                min_time = min(G_time, next_Time_scan)
            if nodes[i_node].feature == FRIEND_NODE and min_time > nodes[i_node].response_friend_time:
                next_time = nodes[i_node].response_friend_time
                all_event[i_node][NODE_EVENT] = FRIEND_RELAY
                nodes[i_node].response_friend_time = nodes[i_node].response_friend_time + \
                                                     Receive_Delay+random.randint(0, Receive_window) + 100000
            elif heartbeat_time == min_time and nodes[i_node].Heartbeat_period > 0:
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif G_time < next_Time_scan:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == RELAY_AND_GENERATION or nodes[i_node].feature == FRIEND_RELAY_NODE:  
            if nodes[i_node].Heartbeat_period > 0 and len(nodes[i_node].buffer) >= 1:
                min_time = min(heartbeat_time, r_time, G_time, next_Time_scan)
            elif len(nodes[i_node].buffer) >= 1:
                min_time = min(r_time, G_time, next_Time_scan)
            else:
                min_time = min(G_time, next_Time_scan)
            if nodes[i_node].feature == FRIEND_RELAY_NODE and min_time > nodes[i_node].response_friend_time:
                next_time = nodes[i_node].response_friend_time
                all_event[i_node][NODE_EVENT] = FRIEND_RELAY
                nodes[i_node].response_friend_time = nodes[i_node].response_friend_time+Receive_Delay +\
                                                     random.randint(0, Receive_window)+100000
            elif heartbeat_time == min_time and nodes[i_node].Heartbeat_period > 0:  
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif min_time == r_time and len(nodes[i_node].buffer) >= 1:
                next_time = r_time
                all_event[i_node][NODE_EVENT] = RELAY_EVENT_Adv37
            elif next_Time_scan > G_time:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event

        elif nodes[i_node].feature == SINK_NODE:
            if heartbeat_time < next_Time_scan and nodes[i_node].Heartbeat_period > 0:
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == LOW_POWER:
            if all_event[i_node][NODE_EVENT] == SEND_POLL or all_event[i_node][NODE_EVENT] == GENERATION_EVENT_Adv37:
                all_event[i_node][NODE_EVENT] = all_event[i_node][NODE_EVENT]
                next_time = all_event[i_node][NODE_TIME]
            else:
                remain1 = all_event[i_node][NODE_TIME]-nodes[i_node].Low_Scan_Time
                if Receive_window <= remain1:
                    next_time = all_event[i_node][NODE_TIME] + sleep_time
                    all_event[i_node][NODE_EVENT] = SEND_POLL
                    nodes[i_node].not_receive = 1
                else:
                    all_event[i_node][NODE_EVENT] = scan_event
                    next_time = all_event[i_node][NODE_TIME]

        if all_event[i_node][NODE_TIME] < next_time:
            all_event[i_node][NODE_TIME] = next_time
        else:
            all_event[i_node][NODE_TIME] = all_event[i_node][NODE_TIME]
        nodes[i_node].L_scan = SCAN38_C_EVENT
        if all_event[i_node][NODE_TIME] == p:
            nodes[i_node].L_scan = SCAN38_C_EVENT/10
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))
        Time = all_event[i_node][NODE_TIME]
    ####################################################
        """this event is almost similar to the SCAN37_C_EVENT event please for comments reference the SCAN37_C_EVENT
        for giving more freedom to the developer in future development we preferred to write them in the separate events
         """
    elif all_event[i_node][NODE_EVENT] == SCAN39_C_EVENT:
        p = copy.deepcopy(all_event[i_node][NODE_TIME])
        all_event[i_node][NODE_TIME], all_event[i_node][NODE_EVENT] = \
            Scan_function39(nodes, i_node, all_event, NODE_TIME, NODE_EVENT, reception_ratio, logger, Time)
        for i_b in range(BUFFER_SIZE):
            if len(nodes[i_node].buffer) < 1:
                break
            if nodes[i_node].buffer[0].friend_poll == 0:
                if nodes[i_node].buffer[0].TTL < 2:
                    nodes[i_node].buffer.remove(nodes[i_node].buffer[0])
                    if len(nodes[i_node].buffer) < 1:
                        break
        scan_event = SCAN39_C_EVENT
        next_Time_scan = all_event[i_node][NODE_TIME]
        if all_event[i_node][NODE_TIME] == p:
            nodes[i_node].last_t_scan = all_event[i_node][NODE_TIME]
            scan_event = SCAN37_EVENT
            next_Time_scan = nodes[i_node].last_t_scan + (nodes[i_node].SCAN_INTERVAL - nodes[i_node].SCAN_WINDOW)
        heartbeat_time = nodes[i_node].time_heartbeat + nodes[i_node].Heartbeat_period
        relay_Time = nodes[i_node].last_relay_time + nodes[i_node].Advertise_Interval + random.randint(1, 10) 
        Generat_Time = nodes[i_node].last_generation_time + nodes[i_node].GENERATION_INTERVAL  
        r_time1 = nodes[i_node].last_T_relay + nodes[i_node].Relay_Retransmission_Interval
        G_time1 = nodes[i_node].last_T_generation + nodes[i_node].Transmission_Interval
        if nodes[i_node].r_count > 0:  
            r_time = r_time1  
        else:
            r_time = relay_Time  
        if nodes[i_node].n_count > 0:  
            G_time = G_time1 
        else:
            G_time = Generat_Time 
        if nodes[i_node].feature == JUST_RELAY:  
            if heartbeat_time < next_Time_scan and heartbeat_time < r_time and nodes[i_node].Heartbeat_period > 0: 
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif len(nodes[i_node].buffer) >= 1 and r_time < next_Time_scan:
                next_time = r_time
                all_event[i_node][NODE_EVENT] = RELAY_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == JUST_GENERATION or nodes[i_node].feature == FRIEND_NODE:  
            if nodes[i_node].Heartbeat_period > 0:
                min_time = min(heartbeat_time, G_time, next_Time_scan)
            else:
                min_time = min(G_time, next_Time_scan)
            if nodes[i_node].feature == FRIEND_NODE and min_time > nodes[i_node].response_friend_time:
                next_time = nodes[i_node].response_friend_time
                all_event[i_node][NODE_EVENT] = FRIEND_RELAY
                nodes[i_node].response_friend_time = nodes[i_node].response_friend_time+Receive_Delay\
                                                     + random.randint(0, Receive_window)+100000
            elif heartbeat_time == min_time and nodes[i_node].Heartbeat_period > 0:
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif G_time < next_Time_scan:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == RELAY_AND_GENERATION or nodes[i_node].feature == FRIEND_RELAY_NODE:  
            if nodes[i_node].Heartbeat_period > 0 and len(nodes[i_node].buffer) >= 1:
                min_time = min(heartbeat_time, r_time, G_time, next_Time_scan)
            elif len(nodes[i_node].buffer) >= 1:
                min_time = min(r_time, G_time, next_Time_scan)
            else:
                min_time = min(G_time, next_Time_scan)

            if nodes[i_node].feature == FRIEND_RELAY_NODE and min_time > nodes[i_node].response_friend_time:
                next_time = nodes[i_node].response_friend_time
                all_event[i_node][NODE_EVENT] = FRIEND_RELAY
                nodes[i_node].response_friend_time = nodes[i_node].response_friend_time + Receive_Delay +\
                                                     random.randint(0, Receive_window) + 100000
            elif heartbeat_time == min_time and nodes[i_node].Heartbeat_period > 0:  
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            elif min_time == r_time and len(nodes[i_node].buffer) >= 1:
                next_time = r_time
                all_event[i_node][NODE_EVENT] = RELAY_EVENT_Adv37
            elif next_Time_scan > G_time:
                next_time = G_time
                all_event[i_node][NODE_EVENT] = GENERATION_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == SINK_NODE:
            if heartbeat_time < next_Time_scan and nodes[i_node].Heartbeat_period > 0:
                next_time = heartbeat_time
                all_event[i_node][NODE_EVENT] = HEARTBEAT_EVENT_Adv37
            else:
                next_time = next_Time_scan
                all_event[i_node][NODE_EVENT] = scan_event
        elif nodes[i_node].feature == LOW_POWER:
            if all_event[i_node][NODE_EVENT] == SEND_POLL or all_event[i_node][NODE_EVENT] == GENERATION_EVENT_Adv37:
                all_event[i_node][NODE_EVENT] = all_event[i_node][NODE_EVENT]
                next_time = all_event[i_node][NODE_TIME]
            else:
                remain1 = all_event[i_node][NODE_TIME]-nodes[i_node].Low_Scan_Time
                if Receive_window <= remain1:
                    next_time = all_event[i_node][NODE_TIME] + sleep_time
                    all_event[i_node][NODE_EVENT] = SEND_POLL
                    nodes[i_node].not_receive = 1
                else:
                    all_event[i_node][NODE_EVENT] = scan_event
                    next_time = all_event[i_node][NODE_TIME]

        if all_event[i_node][NODE_TIME] < next_time:
            all_event[i_node][NODE_TIME] = next_time
        else:
            all_event[i_node][NODE_TIME] = all_event[i_node][NODE_TIME]
        nodes[i_node].L_scan = SCAN39_C_EVENT
        if all_event[i_node][NODE_TIME] == p:
            nodes[i_node].L_scan = SCAN39_C_EVENT/10
        i_node = all_event.index(min((x for x in all_event), key=lambda k: k[0]))
        Time = all_event[i_node][NODE_TIME]
    ##################################################################


