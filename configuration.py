from routing_algorithms.direct_communication import DirectCommunication
from routing_algorithms.leach import Leach
from routing_algorithms.leach_c import LeachC

supported_algorithms = {
    'DirectCommunication': DirectCommunication('Direct Communication'),
    'LeachC': LeachC('LeachC'),
    'Leach': Leach('Leach')
}

supported_metrics = ['alive_nodes_num', 'avg_energy_dissipation', 'received_packets', 'first_dead_node',
                     'total_energy_dissipation', 'dead_nodes_num']
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
    },
    'total_energy_dissipation': {
        'plot_type': 'bar',
        'label': 'Dissipated energy (Joules)',
        'title': 'Total energy dissipated by each protocol up to round 200',
        'legend_location': ""
    },
    'dead_nodes_num': {
        'plot_type': 'plot',
        'label': 'Number of dead nodes each round',
        'title': 'Number of dead nodes',
        'legend_location': 'upper left'
    },
}

BS_ID = -1

show_plots = False
# LEACH CONFIGURATION
# desired number of cluster heads is 5% of nodes in the network
P = float(0.1)
# CLUSTERS_NUM = P * float(NODES_NUM)


# Energy required to run circuity (both for transmitter and receiver)
E_ELEC = 50e-9  # units in Joules/bit
E_DA = 5e-9 # Joules
ETx = 50e-10  # units in Joules/bit
ERx = 50e-10  # units in Joules/bit
# Transmit Amplifier Types %
E_AMP = 100e-12  # units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
# Data Aggregation Energy

k = 2000  # units in bits
HEADER = 200
## Energy Configurations
# energy dissipated at the transceiver electronic (/bit)
# energy dissipated at the data aggregation (/bit)

target_field_x_axis = [0, 100]
target_field_y_axis = [0, 100]

