
""" 
 this function is almost similar to the scan37 function please for comments reference the scan37 function
 for giving more freedom to the developer in future development we preferred to write them in the separate functions 
"""
from initializer import *
import random 
def Scan_function38(nodes, i, all_event, NODE_TIME, NODE_EVENT, reception_ratio, logger, Time):
    if Time < nodes[i].first_time_scan+nodes[i].SCAN_WINDOW:
        Num_AD_nodes = 0
        if TOTAL_LOG == 1:
            detail_log.info("scan38 node %s at Time %s ", i, all_event[i][NODE_TIME])
        for j in range(len(nodes[i].neighbors)):
            if nodes[nodes[i].neighbors[j]].advertisetag38 == 1:
                Num_AD_nodes += 1
                Advertise_node = nodes[i].neighbors[j]
        if Num_AD_nodes == 1:
            nodes[i].scanchannel38(nodes[Advertise_node].channel38)
            f = nodes[i].ID in nodes[i].cache[len(nodes[i].cache)-1].destination
            if random.randint(0, 100) > reception_ratio[nodes[i].ID][Advertise_node]:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache)-1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN38_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            if f == False and nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 1:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache)-1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN38_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            if nodes[i].feature == LOW_POWER or nodes[i].feature == SINK_NODE and f == False:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache)-1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN38_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            if (nodes[i].feature == LOW_POWER and nodes[i].friend_Id != Advertise_node) and f == True:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache)-1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN38_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            L = nodes[i].LOW_POWER_ID in nodes[i].cache[len(nodes[i].cache)-1].destination
            if(nodes[i].feature == JUST_GENERATION or (nodes[i].feature == FRIEND_NODE and L == False)) and f == False\
                    and nodes[i].cache[len(nodes[i].cache)-1].heartbeat == 0 and \
                    nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 0:
                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache)-1])
                all_event[i][NODE_TIME] += SCAN_STEP
                all_event[i][NODE_EVENT] = SCAN38_C_EVENT
                nodes[i].Scan_Time += SCAN_STEP
                return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            if nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 0:
                if nodes[i].cache[len(nodes[i].cache)-1].heartbeat == 0:
                    comp_temp = nodes[i].last_seq_number[nodes[i].cache[len(nodes[i].cache)-1].source]
                else:
                    comp_temp = nodes[i].h_last_seq_number[nodes[i].cache[len(nodes[i].cache)-1].source]
                if nodes[i].cache[len(nodes[i].cache)-1].seq_number > comp_temp:
                    if nodes[i].cache[len(nodes[i].cache)-1].heartbeat == 0:
                        nodes[i].last_seq_number[nodes[i].cache[len(nodes[i].cache)-1].source] = \
                            nodes[i].cache[len(nodes[i].cache)-1].seq_number
                    else:
                        nodes[i].h_last_seq_number[nodes[i].cache[len(nodes[i].cache)-1].source] = \
                            nodes[i].cache[len(nodes[i].cache)-1].seq_number
                else:
                    nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache)-1])
                    all_event[i][NODE_TIME] += SCAN_STEP
                    all_event[i][NODE_EVENT] = SCAN38_C_EVENT
                    nodes[i].Scan_Time += SCAN_STEP
                    return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
            if nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 0 or \
                    nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 1:
                    if len(nodes[i].buffer) < BUFFER_SIZE:
                        nodes[i].buffer.append(nodes[i].cache[len(nodes[i].cache)-1])
                        f = nodes[i].ID in nodes[i].buffer[len(nodes[i].buffer)-1].destination
                        if TOTAL_LOG == 1 and ((nodes[i].feature == JUST_RELAY) or
                                               (nodes[i].feature == RELAY_AND_GENERATION) or
                                               (nodes[i].feature == FRIEND_RELAY_NODE)) and f == False and\
                                nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 0:
                            logger[i].info('(relay)    %s    %s    %s    %s    %s    %s    %s', Advertise_node,
                                           nodes[i].buffer[len(nodes[i].buffer)-1].source, round(Time, 2),
                                           nodes[i].buffer[len(nodes[i].buffer)-1].seq_number,
                                           round(nodes[i].buffer[len(nodes[i].buffer)-1].generation_time, 2),
                                           nodes[i].buffer[len(nodes[i].buffer)-1].TTL, len(nodes[i].buffer))
                        if nodes[i].feature == FRIEND_NODE or nodes[i].feature == FRIEND_RELAY_NODE:
                            f = nodes[i].LOW_POWER_ID in nodes[i].buffer[len(nodes[i].buffer)-1].destination
                            if f == True:
                                    nodes[i].friend_queue.append(nodes[i].buffer[len(nodes[i].buffer)-1])
                                    nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer)-1])
                                    all_event[i][NODE_TIME] += SCAN_STEP
                                    all_event[i][NODE_EVENT] = SCAN38_C_EVENT
                                    nodes[i].Scan_Time += SCAN_STEP
                                    return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                        f = nodes[i].ID in nodes[i].buffer[len(nodes[i].buffer)-1].destination
                        if f == True:  # the packet is received by destination
                              if TOTAL_LOG == 1 and nodes[i].buffer[len(nodes[i].buffer)-1].heartbeat == 0 and\
                                      nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 0:
                                  logger[i].info('(main)    %s    %s    %s    %s    %s',
                                                 nodes[i].buffer[len(nodes[i].buffer)-1].source,
                                                 nodes[i].buffer[len(nodes[i].buffer)-1].seq_number,
                                                 round(nodes[i].buffer[len(nodes[i].buffer)-1].generation_time, 2),
                                                 nodes[i].ID, round(Time, 2),
                                                 )
                              if TOTAL_LOG == 1 and nodes[i].buffer[len(nodes[i].buffer)-1].heartbeat == 1 and \
                                      nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 0:
                                  logger[i].info('(heartbeat)    %s    %s    %s    %s    %s    %s    %s',
                                                 nodes[i].buffer[len(nodes[i].buffer)-1].source,
                                                 nodes[i].buffer[len(nodes[i].buffer)-1].seq_number,
                                                 round(nodes[i].buffer[len(nodes[i].buffer)-1].generation_time, 2),
                                                 nodes[i].ID, round(Time, 2),
                                                 nodes[i].minhop, nodes[i].maxhop)
                              if TOTAL_LOG == 0 and nodes[i].cache[len(nodes[i].cache)-1].friend_poll == 0 and \
                                      nodes[i].buffer[len(nodes[i].buffer)-1].heartbeat == 0:
                                  logger.info('%s    %s    %s    %s    %s', nodes[i].buffer[len(nodes[i].buffer)-1].source,
                                                     nodes[i].ID, round(Time, 2),
                                              nodes[i].buffer[len(nodes[i].buffer)-1].seq_number,
                                                     round(nodes[i].buffer[len(nodes[i].buffer)-1].generation_time, 2))

                              if (nodes[i].feature == FRIEND_NODE or nodes[i].feature == FRIEND_RELAY_NODE) and\
                                      nodes[i].buffer[len(nodes[i].buffer)-1].friend_poll == 1:
                                  nodes[i].response_friend_time = all_event[i][NODE_TIME]+Receive_Delay +\
                                                                  random.randint(0, Receive_window)
                                  all_event[i][NODE_TIME] += SCAN_STEP
                                  all_event[i][NODE_EVENT] = SCAN38_C_EVENT
                                  nodes[i].Scan_Time += SCAN_STEP
                                  if nodes[i].previous_ack < nodes[i].buffer[len(nodes[i].buffer)-1].acknowledge:
                                      if len(nodes[i].friend_queue) >= 1:
                                          nodes[i].friend_queue.remove(nodes[i].friend_queue[0])
                                      nodes[i].previous_ack = nodes[i].buffer[len(nodes[i].buffer)-1].acknowledge
                                  nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer)-1])
                                  return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                              if nodes[i].feature == LOW_POWER:
                                  if nodes[i].buffer[len(nodes[i].buffer)-1].friend_update == 1:
                                      nodes[i].buffer[len(nodes[i].buffer)-1].friend_update = 0
                                      nodes[i].low_power_ack = 0
                                      nodes[i].not_receive = 0
                                      Generat_Time = nodes[i].last_generation_time+nodes[i].GENERATION_INTERVAL
                                      scan_time_low = all_event[i][NODE_TIME] - nodes[i].Low_Scan_Time
                                      remain_receive_window = Receive_window-scan_time_low
                                      nodes[i].last_poll_time = all_event[i][NODE_TIME] + sleep_time + \
                                                                remain_receive_window
                                      Poll_time = nodes[i].last_poll_time+lowpower_Poll_interval
                                      if Generat_Time < Poll_time:
                                        all_event[i][NODE_TIME] = Generat_Time
                                        all_event[i][NODE_EVENT] = GENERATION_EVENT_Adv37
                                        nodes[i].Scan_Time += SCAN_STEP
                                        nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer)-1])
                                        return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                                      else:
                                        all_event[i][NODE_TIME] = Poll_time
                                        all_event[i][NODE_EVENT] = SEND_POLL
                                        nodes[i].Scan_Time += SCAN_STEP
                                        nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer)-1])
                                        return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                                  else:
                                      nodes[i].not_receive = 0
                                      scan_time_low = all_event[i][NODE_TIME]-nodes[i].Low_Scan_Time
                                      remain_receive_window = Receive_window-scan_time_low
                                      all_event[i][NODE_TIME] += sleep_time+remain_receive_window
                                      all_event[i][NODE_EVENT] = SEND_POLL
                                      nodes[i].Scan_Time += SCAN_STEP
                                      if nodes[i].buffer[len(nodes[i].buffer)-1].heartbeat == 0:
                                          nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer)-1])
                                          return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                              if nodes[i].buffer[len(nodes[i].buffer)-1].heartbeat == 1:
                                  hop = nodes[i].buffer[len(nodes[i].buffer)-1].initTTL-\
                                        nodes[i].buffer[len(nodes[i].buffer)-1].TTL + 1
                                  nodes[i].five_hop.append(hop)
                                  if len(nodes[i].five_hop) > 5:
                                      nodes[i].five_hop.pop(0)
                                  nodes[i].minhop = min(nodes[i].five_hop)
                                  nodes[i].maxhop = max(nodes[i].five_hop)
                                  nodes[i].node_TTL = nodes[i].minhop+R_h
                                  if nodes[i].feature == LOW_POWER:
                                      all_event[i][NODE_TIME] += sleep_time
                                      all_event[i][NODE_EVENT] = SEND_POLL
                                      nodes[i].Scan_Time += SCAN_STEP
                                      nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer)-1])
                                      return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
                                  if nodes[i].feature == JUST_GENERATION:
                                      nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer)-1])
                              if len(nodes[i].buffer) > 0:
                                  if len(nodes[i].buffer[len(nodes[i].buffer)-1].destination) == 1:
                                      nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                                  elif nodes[i].feature != RELAY_AND_GENERATION and nodes[i].feature != JUST_RELAY\
                                          and nodes[i].feature != FRIEND_RELAY_NODE:
                                      nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                        else:
                            if nodes[i].feature == JUST_GENERATION:
                                nodes[i].buffer.remove(nodes[i].buffer[len(nodes[i].buffer) - 1])
                                nodes[i].cache.remove(nodes[i].cache[len(nodes[i].cache) - 1])

        all_event[i][NODE_TIME] += SCAN_STEP
        nodes[i].Scan_Time += SCAN_STEP
        all_event[i][NODE_EVENT] = SCAN38_C_EVENT
    return all_event[i][NODE_TIME], all_event[i][NODE_EVENT]
############################################

