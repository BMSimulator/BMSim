

""" in this function, the node's destinations are determined
 you can use this function, if you have algorithms for determining network TTL also nodes' data. 
in this function, you can choose one destination or a group of destinations or choose them based on the algorithms """
import random
def F_destination(NUMBER_NODES, Center_node, NETWORK_TTL):
    destination_c = []
    destination_c.append(Center_node)
    data = random.randint(1, 100)
    TTL = NETWORK_TTL
    return destination_c, data, TTL
