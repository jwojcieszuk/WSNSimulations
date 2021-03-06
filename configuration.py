import json
import math

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

supported_radio_propagation_models = ['free_space', 'free_space_and_multipath']
metrics_plot_configuration = {
    'alive_nodes_num': {
        'plot_type': 'plot',
        'label': 'Number of alive nodes',
        'title': 'Number of alive nodes compared with round numbers',
        'legend_location': 'lower left'
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
# id of the base station
BS_ID = -1

show_plots = False

# Energy required to run circuity (both for transmitter and receiver)
E_ELEC = 50e-9  # units in Joules/bit
E_TX = 50e-9  # units in Joules/bit
E_RX = 50e-9  # units in Joules/bit
# Transmit Amplifier Types %
E_AMP = 100e-12  # units in Joules/bit/m^2 (amount of energy spent by the amplifier to transmit the bits)
# Data Aggregation Energy
E_DA = 5e-9 # Joules
HEADER = 200

E_FS = 10e-12
E_MP = 0.0013e-12
DISTANCE_THRESHOLD = math.sqrt(E_FS/E_MP)

k = 0
P = 0
radio_propagation_model = ""

with open('scenario.json', 'r') as scenario_file:
    data = json.load(scenario_file)

    for scenario_name in data.keys():
        scenario = data[scenario_name]

    k = scenario["bits_per_message"]
    globals()['k'] = k
    p = scenario["desired_clusters_percentage"]/100
    globals()['P'] = p
    globals()['radio_propagation_model'] = data[scenario_name]["radio_propagation_model"]

target_field_x_axis: list[int] = []
target_field_y_axis: list[int] = []




