""" this function determines the nodes features.
 you can use algorithms or models for determining features in this function 
 Based on network topology the id of the node is passed to this function for determining node features
 """
def choice_feature(nodes, i1, Center_node, Relay_Node, Relay_G_Node):
    #  0 sink node
    # 1 just rely node
    #  2 just generator node
    #  3 relay and generator 
    #  4 low power node
    #  5 friend and relay node
    #  6 friend node
    if i1 == Center_node: 
        nodes[i1].feature = 0
    else:
        for i in range(len(Relay_Node)):  # Based on network topology we choose the nodes' feature 
            if i1 == Relay_Node[i]:
                nodes[i1].feature = 3
                break
            else:
                nodes[i1].feature = 3
            """ when the node feature is low power or friend nodes, it is vital to choose LOW_POWER_ID and friend_Id 
            after determining the nodes feature  """
    # an example of giving feature to low-power and friend nodes
    # nodes[8].feature = 4
    # nodes[5].feature = 5
    # nodes[5].LOW_POWER_ID = 8
    # nodes[8].friend_Id = 5
    # an example of giving feature to low-power and friend nodes
#   nodes[8].feature=4
#   nodes[13].feature=4
#   nodes[12].feature=5
#   nodes[7].feature=6
#   nodes[7].LOW_POWER_ID=8
#   nodes[12].LOW_POWER_ID=13
#   nodes[8].friend_Id=7
#   nodes[13].friend_Id=12

        
        # for i in range(len(Relay_G_Node)):
        #     if(i1==Relay_G_Node[i]):
        #         nodes[i1].feature=3
        #         break
        #     else:
        #         nodes[i1].feature=1
##########################################################################
