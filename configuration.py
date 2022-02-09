import math
# NETWORK CONFIGURATION
BS_X = 125.0
BS_Y = 125.0
BS_ID = -1

INITIAL_ENERGY = 10000
NODES_NUM = 500
ROUNDS = 1

# number of nodes for sensing phase
SENSING_NODES_NUM = int(0.05 * NODES_NUM)


# LEACH CONFIGURATION
# desired number of cluster heads is 5% of nodes in the network
P = float(0.05)
CLUSTERS_NUM = P * float(NODES_NUM)
