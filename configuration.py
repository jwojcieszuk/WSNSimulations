import math
# NETWORK CONFIGURATION
BS_X = 125.0
BS_Y = 125.0
BS_ID = -1

INITIAL_ENERGY = 5
NODES_NUMBER = 100
ROUNDS = 1

# LEACH CONFIGURATION
# desired number of cluster heads is 5% of nodes in the network
P = float(0.05)
CLUSTERS_NUM = P * float(NODES_NUMBER)
