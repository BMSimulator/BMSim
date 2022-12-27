
""" each scan function increases the simulator's current time as much as  SCAN_STEP = 0.2 ms
 after each SCAN_STEP the simulator checks all events time if there is not an event with an earlier time calls
  the scan function again
 in the scan functions if the first condition is true the node does the scan event otherwise leaves the function
 the first condition is checked, whether the simulator's current time is increased up to the scan window or not 
""" 
from initializer import *
import random
def Scan_function37(nodes, i, all_event, NODE_TIME, NODE_EVENT, reception_ratio, logger, Time):
    if Time < nodes[i].first_time_scan + nodes[i].SCAN_WINDOW:  # this is true until the end of the scan window
        Num_AD_nodes = 0  # number of advertising nodes in the node's neighborhood 
        if TOTAL_LOG == 1:
            detail_log.info("scan37 node %s at Time %s", i, all_event[i][NODE_TIME])
        for j in range(len(nodes[i].neighbors)):
            if nodes[nodes[i].neighbors[j]].advertisetag37 == 1:  # if the node advertises at this time, this
                # flag has a value of one.
                Num_AD_nodes += 1  # the number of advertising nodes in the node's neighborhood is increased 
                Advertise_node = nodes[i].neighbors[j]  # the advertising node is saved
        if Num_AD_nodes == 1:  # if just one advertising node was in this neighborhood, the network does not have
            # any collision so the node can receive the packet
            nodes[i].scanchannel37(nodes[Advertise_node].channel37)  # the node scans channel 37 
            # in the beginning, the quality of the link is checked by the reception ratio matrix
            # if the quality of the link is not enough to receive the packet, the node does not receive the packet
            # and leaves the function 
            if random.randint(0, 100) > reception_ratio[nodes[i].ID][Advertise_node]:  
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache) - 1])
                all_event[i][NODE_TIME] += SCAN_STEP  # determining the next event time 
                all_event[i][NODE_EVENT] = SCAN37_C_EVENT  # determining the next event
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            # if the message is a friend poll but the node is not its destination so the node does not receive
            # the packet and leaves the function
            f = nodes[i].ID in nodes[i].cache[len(nodes[i].cache) - 1].destination
            if f == False and nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 1:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache) - 1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN37_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            #  if the node's feature is low power or sink and the node is not the destination so the node does not
            #  receive the packet and leaves the function
            if (nodes[i].feature == LOW_POWER or nodes[i].feature == SINK_NODE) and f == False:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache) - 1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN37_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            #  if the node's feature is low power but the advertising node is not its friend  so the node does not
            #  receive the packet and leaves the function
            if (nodes[i].feature == LOW_POWER and nodes[i].friend_Id != Advertise_node) and f == True:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache) - 1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN37_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            #  if the node's feature is a generator or the node's feature is a friend, but they are not
            #  the destination nodes, the node does not receive the packet and leaves the function
            L = nodes[i].LOW_POWER_ID in nodes[i].cache[len(nodes[i].cache) - 1].destination
            if (nodes[i].feature == JUST_GENERATION or (nodes[i].feature == FRIEND_NODE and L == False))\
                    and f == False and \
                    nodes[i].cache[len(nodes[i].cache) - 1].heartbeat == 0 and\
                    nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 0:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache) - 1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN37_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            #  the sequence number is checked and updated for heartbeat and main messages 
            if nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 0:
                if nodes[i].cache[len(nodes[i].cache) - 1].heartbeat == 0:
                    # last sequence number for the source of message is saved
                    comp_temp = nodes[i].last_seq_number[nodes[i].cache[len(nodes[i].cache) - 1].source]
                else:
                    comp_temp = nodes[i].h_last_seq_number[nodes[i].cache[len(nodes[i].cache) - 1].source]
                # if the last sequence number for the source of the message is lower than the message sequence number 
                if nodes[i].cache[len(nodes[i].cache) - 1].seq_number > comp_temp:
                    # the last sequence number for the source of the message is updated by the message sequence number
                    # for the main and heartbeat message
                    if nodes[i].cache[len(nodes[i].cache) - 1].heartbeat == 0:
                        nodes[i].last_seq_number[nodes[i].cache[len(nodes[i].cache) - 1].source] = nodes[i].cache[
                            len(nodes[i].cache) - 1].seq_number
                    else:
                        nodes[i].h_last_seq_number[nodes[i].cache[len(nodes[i].cache) - 1].source] = nodes[i].cache[
                            len(nodes[i].cache) - 1].seq_number
                else:  # if the last sequence number for the source of the message is greater than
                    # the message sequence number, this message is discarded
                    nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache) - 1])
                    all_event[i][NODE_TIME] += SCAN_STEP
                    all_event[i][NODE_EVENT] = SCAN37_C_EVENT
                    nodes[i].Scan_Time += SCAN_STEP
                    return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            # this part is done for all kinds of messages
            if nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 0 or \
                    nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 1:
                if len(nodes[i].buffer) < BUFFER_SIZE:  # if the device buffer has enough capacity the message is added
                    # to the device's buffer
                    nodes[i].buffer.append(nodes[i].cache[len(nodes[i].cache) - 1])
                    f = nodes[i].ID in nodes[i].buffer[len(nodes[i].buffer) - 1].destination
                    # some data is logged in the relay nodes' log 
                    if TOTAL_LOG == 1 and ((nodes[i].feature == JUST_RELAY) or (nodes[i].feature == RELAY_AND_GENERATION)
                                           or (nodes[i].feature == FRIEND_RELAY_NODE)) \
                            and f == False and nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 0:
                        logger[i].info('(relay)    %s    %s    %s    %s    %s    %s    %s', Advertise_node,
                                       nodes[i].buffer[len(nodes[i].buffer) - 1].source, round(Time, 2),
                                       nodes[i].buffer[len(nodes[i].buffer) - 1].seq_number,
                                       round(nodes[i].buffer[len(nodes[i].buffer) - 1].generation_time, 2),
                                       nodes[i].buffer[len(nodes[i].buffer) - 1].TTL, len(nodes[i].buffer))
                    if nodes[i].feature == FRIEND_NODE or nodes[i].feature == FRIEND_RELAY_NODE:
                        f = nodes[i].LOW_POWER_ID in nodes[i].buffer[len(nodes[i].buffer) - 1].destination
                        # the friend node adds the low-power node's messages to its queue then this message is removed
                        # from its buffer and the node leaves the function
                        if f == True:
                            nodes[i].friend_queue.append(nodes[i].buffer[len(nodes[i].buffer) - 1])
                            nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                            all_event[i][NODE_TIME] += SCAN_STEP
                            all_event[i][NODE_EVENT] = SCAN37_C_EVENT
                            nodes[i].Scan_Time += SCAN_STEP
                            return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                    f = nodes[i].ID in nodes[i].buffer[len(nodes[i].buffer) - 1].destination
                    if f == True:  # the packet is received by destination
                        # received packets characteristics are logged for calculating performance metrics  
                        if (TOTAL_LOG == 1 and nodes[i].buffer[len(nodes[i].buffer) - 1].heartbeat == 0 and
                                nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 0):
                            logger[i].info('(main)    %s    %s    %s    %s    %s',
                                           nodes[i].buffer[len(nodes[i].buffer) - 1].source,
                                           nodes[i].buffer[len(nodes[i].buffer) - 1].seq_number,
                                           round(nodes[i].buffer[len(nodes[i].buffer) - 1].generation_time, 2),
                                           nodes[i].ID, round(Time, 2))
                        if (TOTAL_LOG == 1 and nodes[i].buffer[len(nodes[i].buffer) - 1].heartbeat == 1 and
                              nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 0):
                            logger[i].info('(heartbeat)    %s    %s    %s    %s    %s    %s    %s',
                                           nodes[i].buffer[len(nodes[i].buffer) - 1].source,
                                           nodes[i].buffer[len(nodes[i].buffer) - 1].seq_number,
                                           round(nodes[i].buffer[len(nodes[i].buffer) - 1].generation_time, 2),
                                           nodes[i].ID, round(Time, 2),
                                           nodes[i].minhop, nodes[i].maxhop)
                        if TOTAL_LOG == 0 and nodes[i].cache[len(nodes[i].cache) - 1].friend_poll == 0 and \
                                nodes[i].buffer[len(nodes[i].buffer) - 1].heartbeat == 0:
                            logger.info('%s    %s    %s    %s    %s',
                                           nodes[i].buffer[len(nodes[i].buffer) - 1].source, nodes[i].ID,
                                           round(Time, 2), nodes[i].buffer[len(nodes[i].buffer) - 1].seq_number,
                                           round(nodes[i].buffer[len(nodes[i].buffer) - 1].generation_time, 2))
                        # adjusting some settings related to friend nodes 
                        if ((nodes[i].feature == FRIEND_NODE or nodes[i].feature == FRIEND_RELAY_NODE) and
                                nodes[i].buffer[len(nodes[i].buffer) - 1].friend_poll == 1):
                            # updating friend response time 
                            nodes[i].response_friend_time = all_event[i][NODE_TIME] + Receive_Delay +\
                                                            random.randint(0, Receive_window)
                            all_event[i][NODE_TIME] += SCAN_STEP
                            all_event[i][NODE_EVENT] = SCAN37_C_EVENT
                            nodes[i].Scan_Time += SCAN_STEP
                            # adjusting acknowledge in friend's queue packets 
                            if nodes[i].previous_ack < nodes[i].buffer[len(nodes[i].buffer) - 1].acknowledge:
                                if len(nodes[i].friend_queue) >= 1:
                                    nodes[i].friend_queue.remove(nodes[i].friend_queue[0])
                                nodes[i].previous_ack = nodes[i].buffer[len(nodes[i].buffer) - 1].acknowledge
                            nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                            return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                        # adjusting some settings related to low power nodes
                        if nodes[i].feature == LOW_POWER:
                            if nodes[i].buffer[len(nodes[i].buffer) - 1].friend_update == 1:  # the end of a friendship 
                                nodes[i].buffer[len(nodes[i].buffer) - 1].friend_update = 0
                                nodes[i].low_power_ack = 0
                                nodes[i].not_receive = 0
                                # calculating the time of the next packet generation  and poll time in the low-power node
                                Generat_Time = nodes[i].last_generation_time + nodes[i].GENERATION_INTERVAL
                                scan_time_low = all_event[i][NODE_TIME] - nodes[i].Low_Scan_Time
                                remain_receive_window = Receive_window - scan_time_low
                                nodes[i].last_poll_time = all_event[i][NODE_TIME] + sleep_time + remain_receive_window
                                Poll_time = nodes[i].last_poll_time + lowpower_Poll_interval
                                # by comparing generation time and poll time in the low-power node is decided
                                # which one is the next event
                                if Generat_Time < Poll_time:
                                    all_event[i][NODE_TIME] = Generat_Time
                                    all_event[i][NODE_EVENT] = GENERATION_EVENT_Adv37
                                    nodes[i].Scan_Time += SCAN_STEP
                                    nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                                    return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                                else:
                                    all_event[i][NODE_TIME] = Poll_time
                                    all_event[i][NODE_EVENT] = SEND_POLL
                                    nodes[i].Scan_Time += SCAN_STEP
                                    nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                                    return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                            else:  # during a friendship
                                nodes[i].not_receive = 0
                                # the time of sending a request[friend poll] is determined as the next event   
                                scan_time_low = all_event[i][NODE_TIME] - nodes[i].Low_Scan_Time
                                remain_receive_window = Receive_window - scan_time_low
                                all_event[i][NODE_TIME] += sleep_time + remain_receive_window
                                all_event[i][NODE_EVENT] = SEND_POLL
                                nodes[i].Scan_Time += SCAN_STEP
                                if nodes[i].buffer[len(nodes[i].buffer) - 1].heartbeat == 0:
                                    nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                                    return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                        # adjusting nodes' TTL based on heartbeat messages
                        if nodes[i].buffer[len(nodes[i].buffer) - 1].heartbeat == 1:
                            # calculating the distance between the source of the heartbeat message and its destination   
                            hop = nodes[i].buffer[len(nodes[i].buffer) - 1].initTTL - nodes[i].buffer[
                                len(nodes[i].buffer) - 1].TTL + 1
                            nodes[i].five_hop.append(hop)
                            if len(nodes[i].five_hop) > 5:
                                nodes[i].five_hop.pop(0)
                            # calculating the minimum and maximum of the hops 
                            nodes[i].minhop = min(nodes[i].five_hop)
                            nodes[i].maxhop = max(nodes[i].five_hop)
                            nodes[i].node_TTL = nodes[i].minhop + R_h  # determining nodes' TTL based on minimum hop 
                            # low power and generator nodes remove the heartbeat message from their buffer
                            # after determining the TTL
                            if nodes[i].feature == LOW_POWER:
                                all_event[i][NODE_TIME] += sleep_time
                                all_event[i][NODE_EVENT] = SEND_POLL
                                nodes[i].Scan_Time += SCAN_STEP
                                nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                            if nodes[i].feature == JUST_GENERATION:
                                nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1]) 
                        # relay and destination nodes remove the packets from their buffer after receiving them   
                        if len(nodes[i].buffer) > 0:
                            if len(nodes[i].buffer[len(nodes[i].buffer) - 1].destination) == 1:
                                nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])  
                            elif nodes[i].feature != RELAY_AND_GENERATION and nodes[i].feature != JUST_RELAY and\
                                    nodes[i].feature != FRIEND_RELAY_NODE:
                                nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                    #  the generator node that is not the destination removes the packets from its buffer 
                    else:
                        if nodes[i].feature == JUST_GENERATION:
                            nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                            nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache) - 1])
        all_event[i][NODE_TIME] += SCAN_STEP
        nodes[i].Scan_Time += SCAN_STEP
        all_event[i][NODE_EVENT] = SCAN37_C_EVENT
    return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
