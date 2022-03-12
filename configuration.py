import math

# NETWORK CONFIGURATION
BS_X = 0
BS_Y = 250.0
BS_ID = -1

INITIAL_ENERGY = 0.5  # Jules
NODES_NUM = 100

# LEACH CONFIGURATION
# desired number of cluster heads is 5% of nodes in the network
P = float(0.05)
CLUSTERS_NUM = P * float(NODES_NUM)

# Energy model

# Energy required to run circuity (both for transmitter and receiver)
E_ELEC = 50 * 10 ** (-9)  # units in Joules/bit
ETx = 50 * 10 ** (-9)  # units in Joules/bit
ERx = 50 * 10 ** (-9)  # units in Joules/bit
# Transmit Amplifier Types %
Eamp = 100e-12  # units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
# Data Aggregation Energy
EDA = 5 * 10 ** (-9)  # units in Joules/bit

k = 4000  # units in bits



## Energy Configurations
# energy dissipated at the transceiver electronic (/bit)
# energy dissipated at the data aggregation (/bit)
E_DA = 5e-9 # Joules
# energy dissipated at the power amplifier (supposing a multi-path
# fading channel) (/bin/m^4)
E_AMP = 50e-9
E_MP = 0.0013e-12 # Joules
# energy dissipated at the power amplifier (supposing a line-of-sight
# free-space channel (/bin/m^2)
E_FS = 10e-12 # Joules
THRESHOLD_DISTANCE = 50 # meters