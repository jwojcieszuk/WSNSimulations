from routing_algorithms.direct_communication import DirectCommunication
from routing_algorithms.leach import Leach
from routing_algorithms.leach_c import LeachC

supported_algorithms = {
    'DirectCommunication': DirectCommunication('Direct Communication'),
    'LeachC': LeachC('LeachC'),
    'Leach': Leach('Leach')
}

supported_metrics = ['alive_nodes_num', 'avg_energy_dissipation', 'received_packets', 'first_dead_node']
metrics_plot_configuration = {
    'alive_nodes_num': {
        'plot_type': 'plot',
        'label': 'Number of alive nodes',
        'title': 'Number of alive nodes compared with round numbers',
        'legend_location': 'upper right'
    },
    'avg_energy_dissipation': {
        'plot_type': 'plot',
        'label': 'Average energy dissipation per node',
        'title': 'Average energy dissipation per node compared with round numbers',
        'legend_location': 'lower right'
    },
    'received_packets': {
        'plot_type': 'bar',
        'label': 'Packets',
        'title': 'Total number of data packets delivered to Base Station',
        'legend_location': ""
    },
    'first_dead_node': {
        'plot_type': 'bar',
        'label': 'Round',
        'title': 'First dead node',
        'legend_location': ""
    }
}

# NETWORK CONFIGURATION
BS_X = 0
BS_Y = 250
BS_ID = -1

show_plots = False
# LEACH CONFIGURATION
# desired number of cluster heads is 5% of nodes in the network
P = float(0.05)
# CLUSTERS_NUM = P * float(NODES_NUM)


# Energy required to run circuity (both for transmitter and receiver)
E_ELEC = 50 * 10 ** (-9)  # units in Joules/bit
E_DA = 5e-9 # Joules
ETx = 50 * 10 ** (-9)  # units in Joules/bit
ERx = 50 * 10 ** (-9)  # units in Joules/bit
# Transmit Amplifier Types %
E_AMP = 100e-12  # units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
# Data Aggregation Energy

k = 2000  # units in bits
HEADER = 200
## Energy Configurations
# energy dissipated at the transceiver electronic (/bit)
# energy dissipated at the data aggregation (/bit)
