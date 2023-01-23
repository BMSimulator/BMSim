

""" in this function, the node's neighbors within the specified communication range is detected.
 the neighbors' nodes are added to the network graph and neighbor array.
 nodes range is determined by the user.
"""
import math
def detect_neighbor(node_source, NODE_RANGE, NUMBER_NODES, nodes, Gar):
    r = NODE_RANGE
    neighbor = []
    for node_neighbor in range(NUMBER_NODES):
        xsec = abs(nodes[node_neighbor].Xposition-nodes[node_source].Xposition)
        ysec = abs(nodes[node_neighbor].Yposition-nodes[node_source].Yposition)
        r_n = xsec**2 + ysec**2
        r_neighbor = math.sqrt(r_n)
        if r_neighbor < r:  # neighbors are determined based on the positions of the nodes in the environment
            Id2 = nodes[node_neighbor].ID
            Id1 = nodes[node_source].ID
            if Id2 != Id1:
                neighbor.append(Id2)
                Gar.add_edge(Id1, Id2)
    return neighbor
