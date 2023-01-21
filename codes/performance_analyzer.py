# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 20:01:19 2020
this file calculates performance metrics (PDR, Latency and burst packet loss) in the network also plots diagrams for them
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from collections import Counter 

from pylab import plot, show, savefig, xlim, figure, \
                 ylim, legend, boxplot, setp, axes

allNums = []
total = []
source_node = []
receive_time = []
seq_number = []
generation_time = []
network_PDR = []
network_latency = []
network_burst_packet_loss = []
node = []
nodes = []
latency = []
seq = []
nodes_PDR = []
nodes_PDR1 = []
source = []
burst_packet_loss = []
burst_packet_loss_mean = []
burst_packet_loss_all = []
all_latency = []
network_PDR_mean = []
all_latency_mean = []
NUMBER_NODES = 11
relay_node = 1  # number of nodes that do not generate any packet
ax = axes()
# the maximum sequence number for each node is required for calculating PDR
max_seq = [0 for x in range(NUMBER_NODES)] 
# reading the network_detail log file and saving it in the total array
with open('network_detail'+'.log', "r+") as f:
    data = f.readlines()
    for line in data:
        allNums += line.strip().split("    ")
    for num in allNums:
        if num == '':
            continue
        else:
            total.append(float(num))
# saving the maximum sequence number for each node
for i_m in range(NUMBER_NODES):
    max_seq[NUMBER_NODES-i_m-1] = total[len(total)-1]
    total.pop(len(total)-1)
print(max_seq)
# saving source node, receiving time, sequence number, and generation time in the separated arrays  
for i in range(0, len(total), 5):
    source_node.append(total[i])

for i1 in range(2, len(total), 5):
    receive_time.append(total[i1])

for i2 in range(3, len(total), 5):
    seq_number.append(total[i2])

for i3 in range(4, len(total), 5):
    generation_time.append(total[i3])
total = []
j = 0
# adding source node, receiving time, sequence number, and generation time to the node array,
# index of the array is node number
while j < NUMBER_NODES:
    for i4 in range(len(source_node)):
        if source_node[i4] == j:
            node.append([source_node[i4], generation_time[i4], receive_time[i4], seq_number[i4]])
    nodes.append(node)
    node = []
    j += 1
# calculating latency 
for s in range(NUMBER_NODES):
    for d in range(len(nodes[s])):
        latency.append(nodes[s][d][2]-nodes[s][d][1])  # receive time - generation time
    if len(latency) == 0:
        latency.append(0)
    all_latency.append(latency)
    if np.mean(latency) > 0:
        all_latency_mean.append(np.mean(latency))
    else:
        all_latency_mean.append(0)
    latency = []
# calculating burst packet loss
for s1 in range(NUMBER_NODES):
    for d1 in range(len(nodes[s1])):
        seq.append(nodes[s1][d1][3])
        if d1 >= (len((nodes[s1]))-1):
            burst_packet_loss.append(0)
        else:
            burst_packet_loss.append((nodes[s1][d1+1][3]-nodes[s1][d1][3])-1) # sequence number (n+1) - sequence number (n)
    if len(burst_packet_loss) == 0:
        burst_packet_loss.append(0)
    burst_packet_loss_all.append(burst_packet_loss)
    # calculating the mean of burst packet loss
    if np.mean(burst_packet_loss) > 0:
        burst_packet_loss_mean.append(np.mean(burst_packet_loss))
    else:
        burst_packet_loss_mean.append(0)
    # calculating PDR 
    if max_seq[s1] != 0:
        PDR = (len(Counter(seq).keys())/max_seq[s1]) * 100
    else:
        PDR = 0
    nodes_PDR.append(PDR)
    seq = []
    burst_packet_loss = []
# the figure of the nodes' PDR
df2 = DataFrame(nodes_PDR)
df2.plot(kind='bar')
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("PDR", fontsize=10)
plt.savefig('PDR.pdf', dpi=200)
print("------------------------------------------")
print("nodes PDR ", nodes_PDR)
print("------------------------------------------")
print("average latency in each node", all_latency_mean)

# removing the nodes with the relay feature from the nodes array for calculating average PDR and Latency  
# because these nodes do not generate any packet 
for iv in range(relay_node):
    for i91 in range(len(nodes_PDR)):
        if nodes_PDR[i91] <= 0.0:
            nodes_PDR.remove(nodes_PDR[i91])
            break
for iv1 in range(relay_node):
    for i911 in range(len(all_latency_mean)):
        if all_latency_mean[i911] <= 0.0:
            all_latency_mean.remove(all_latency_mean[i911])
            break
# the boxplot figure of the nodes' PDR
network_PDR.append(nodes_PDR)
df21 = DataFrame(network_PDR)
df21 = df21.T
df21.plot.box(patch_artist=True)
plt.xlabel("network", fontsize=10)
plt.ylabel("PDR (%)", fontsize=10)
plt.savefig('PDR_boxplot.pdf', dpi=200)

network_PDR_mean.append(np.mean(nodes_PDR))
print("------------------------------------------")
print("average PDR in the network", network_PDR_mean)
# the boxplots figure of the nodes' burst packet loss
df3 = DataFrame(burst_packet_loss_all)
df3.fillna(0, inplace = True)
df3 = df3.T
df3.plot.box(grid='True')
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("Burst Packet Loss", fontsize=10)
plt.savefig('burst_packet_loss_boxplot.pdf', dpi=200)

network_burst_packet_loss.append(burst_packet_loss_mean)
print("------------------------------------------")
print("average burst packet loss in each node", network_burst_packet_loss)
print("------------------------------------------")
# the figure of the mean of the nodes' burst packet loss
df23 = DataFrame(burst_packet_loss_mean)
df23.plot(kind='bar')
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("Mean Burst Packet Loss", fontsize=10)
plt.savefig('mean_burst_packet_loss.pdf', dpi=200)

# the boxplot figure of the mean of the nodes' Latency
network_latency.append(all_latency_mean)
df5 = DataFrame(network_latency)
df5 = df5.T
df5.plot.box(patch_artist=True)
plt.xlabel("network", fontsize=10)
plt.ylabel("latency (ms)", fontsize=10)
plt.savefig('latency_boxplot.pdf', dpi=200)

# the boxplots figure of the nodes' Latency
df4 = DataFrame(all_latency)
df4.fillna(0, inplace = True)
df4 = df4.T
df4.plot.box(patch_artist=True)
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("Latency (ms)", fontsize=10)
plt.savefig('latency.pdf', dpi=200)

#--------------------------------------------------------------------------------------------------------------------

voltage = 3  # V
C_tx = 8.45  # mA
C_rx = 13.9
C_sw = 3.66
C_sleep = 0.015
NUMBER_NODES = 50
relay_node = 1
allNums = []
total = []
scan_time = []
switch_time = []
sleep_time = []
transmit_time = []
scan_energy = []
sleep_energy = []
switch_energy = []
transmit_energy = []
# reading the energy log file and saving it in the total array
with open('energy.log', "r+") as f:
    data = f.readlines()
    for line in data:
        allNums += line.strip().split("   ")
    for num in allNums:
        if num == '':
            continue
        else:
            total.append(float(num))
# saving the scan time, switch time, and transmit time in the separated arrays
# calculating scan energy, switch energy and transmit energy

for i in range(1, len(total), 5):
    scan_time.append(total[i])
    scan_energy.append(total[i] * (C_rx * voltage)/1000)

dfs = DataFrame(scan_energy)
dfs.plot(kind='bar')
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("Scanning Energy (mJ)", fontsize=10)
plt.savefig('scan_energy.pdf', dpi=200)
print("---------------------------------------")
print("scanning energy in each node", scan_energy)

for i1 in range(2, len(total), 5):
    switch_time.append(total[i1])
    switch_energy.append(total[i1]*(C_sw * voltage)/1000)
print("---------------------------------------")
print("switching energy in each node", switch_energy)

df_sw = DataFrame(switch_energy)
df_sw.plot(kind='bar')
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("Switching Energy (mJ)", fontsize=10)
plt.savefig('switch_energy.pdf', dpi=200)

for i2 in range(3, len(total), 5):
    transmit_time.append(total[i2])
    transmit_energy.append(total[i2]*(C_tx * voltage)/1000)
print("---------------------------------------")
print("transmitting energy in each node", transmit_energy)

df_t = DataFrame(transmit_energy)
df_t.plot(kind='bar')
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("Transmitting Energy (mJ)", fontsize=10)
plt.savefig('transmit_energy.pdf', dpi=200)

for i3 in range(4, len(total), 5):
    sleep_time.append(total[i3])
    sleep_energy.append(round(total[i3] * (C_sleep * voltage)/1000, 4))
print("---------------------------------------")
print("sleeping energy in each node", sleep_energy)

df_sl = DataFrame(sleep_energy)
df_sl.plot(kind='bar')
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("Sleeping Energy (mJ)", fontsize=10)
plt.savefig('sleep_energy.pdf', dpi=200)


# calculating the network energy consumption
total_energy = [scan_energy[en1] + transmit_energy[en1] + switch_energy[en1] + sleep_energy[en1]
                for en1 in range(len(scan_energy))]
print("---------------------------------------")
print("total energy in each node", total_energy)

df_total = DataFrame(total_energy)
df_total.plot(kind='bar')
plt.xlabel("Node Number", fontsize=10)
plt.ylabel("Total Energy (mJ)", fontsize=10)
plt.savefig('total_energy.pdf', dpi=200)

network_energy = sum(scan_energy) + sum(transmit_energy) + sum(switch_energy) + sum(sleep_energy)

print("---------------------------------------")
print("network energy consumption (mJ)", network_energy)
