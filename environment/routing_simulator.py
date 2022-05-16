import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import logging

from decorators import run_once
from environment.network import Network
from routing_algorithms.routing_algorithm import RoutingAlgorithm
from routing_algorithms.direct_communication import DirectCommunication
from routing_algorithms.leach import Leach
from routing_algorithms.leach_c import LeachC
from metrics import RoutingAlgorithmMetrics
import configuration as cfg


class RoutingSimulator:
    """
        This class simulates behaviour of an environment that is deployed in a random field.
    """

    def __init__(self, num_of_nodes: int, initial_node_energy: float, simulation_logger: logging):
        self.network = Network(num_of_nodes, initial_node_energy, simulation_logger)
        self.plot_environment("Deployed network")
        self.logger = simulation_logger

        self.routing_algorithm = None

    def simulate(self, routing_algorithm: RoutingAlgorithm, simulation_logger) -> RoutingAlgorithmMetrics:
        logging.info(f'Simulating routing algorithm: {routing_algorithm.__repr__()}...')
        setattr(self, 'routing_algorithm', routing_algorithm)
        setattr(self, 'logger', simulation_logger)
        round_num, alive_nodes_num, avg_energy_dissipation, dead_nodes_num = list(), list(), list(), list()
        round_counter = 0
        # each node informs base station about its location
        self.network.notify_position()

        plot_environment = run_once(self.plot_environment)
        log_dead_node_once = run_once(self.log_dead_node_once)
        first_dead_node = 0

        while True:
            simulation_logger.info(f'{routing_algorithm.__repr__()} Running round: {round_counter}. '
                                   f'Nodes alive: {len(self.network.get_alive_nodes())}')

            node_dead_round = self._run_round(round_counter, plot_environment, log_dead_node_once)
            round_num.append(round_counter)
            avg_energy_dissipation.append(self.network.avg_energy_dissipation())
            alive_nodes_num.append(len(self.network.get_alive_nodes()))
            dead_nodes_num.append(len(self.network.nodes) - len(self.network.get_alive_nodes()))

            # if this variable is not None, it contains round number of first dead node
            if node_dead_round:
                first_dead_node = node_dead_round

            if not self.check_network_life():
                logging.info(f'{routing_algorithm.__repr__()}: Network is dead after {round_counter} rounds')
                simulation_logger.info(f'{routing_algorithm.__repr__()}: Network is dead after {round_counter} rounds')
                break

            round_counter += 1

        base_station_received_packets = self.network.base_station.received_packets
        total_energy_dissipation = self.network.total_energy_dissipation()
        self.network.restore_initial_state()

        return RoutingAlgorithmMetrics(
            rounds_num=round_num,
            alive_nodes_num=alive_nodes_num,
            avg_energy_dissipation=avg_energy_dissipation,
            received_packets=base_station_received_packets,
            first_dead_node=first_dead_node,
            total_energy_dissipation=total_energy_dissipation,
            dead_nodes_num=dead_nodes_num,
            algorithm_name=routing_algorithm.__repr__()
        )

    def _run_round(self, round_counter: int, plot_environment_once, log_dead_node_once):
        first_dead_node = 0

        if isinstance(self.routing_algorithm, DirectCommunication):
            self.routing_algorithm.setup_phase(self.network.nodes)
            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network)

            if len(self.network.get_alive_nodes()) < len(self.network.nodes):
                if log_dead_node_once.has_run is False:
                    first_dead_node = round_counter
                    log_dead_node_once(round_counter)

            self.network.reset_nodes()

        elif isinstance(self.routing_algorithm, LeachC):
            avg_energy = self.network.base_station.calculate_avg_energy(self.network.get_alive_nodes(), self.network.base_station)
            heads = self.routing_algorithm.setup_phase(self.network, round_counter, avg_energy)

            if plot_environment_once.has_run is False:
                plot_environment_once("Deployed network divided by clusters in first round  - LeachC")

            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network, heads)

            if len(self.network.get_alive_nodes()) < len(self.network.nodes):
                if log_dead_node_once.has_run is False:
                    first_dead_node = round_counter
                    log_dead_node_once(round_counter)
            self.network.reset_nodes()

        elif isinstance(self.routing_algorithm, Leach):
            heads = self.routing_algorithm.setup_phase(self.network, round_counter)

            if plot_environment_once.has_run is False:
                plot_environment_once("Deployed network divided by clusters in first round - Leach")

            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network, heads)

            if len(self.network.get_alive_nodes()) < len(self.network.nodes):
                if log_dead_node_once.has_run is False:
                    first_dead_node = round_counter
                    log_dead_node_once(round_counter)

            self.network.reset_nodes()

        return first_dead_node if first_dead_node != 0 else None

    def check_network_life(self):
        if len(self.network.get_alive_nodes()) == 0:
            return False
        return True

    def plot_environment(self, title):
        bs_x = self.network.base_station.pos_x
        bs_y = self.network.base_station.pos_y
        plt.scatter(bs_x, bs_y, c="blue", s=300, marker='^')
        blue_base_station = mlines.Line2D([], [], color='blue', marker='^', linestyle='None',
                                          markersize=10, label='Base station')
        if 'Leach' in title:
            black_x_marker = mlines.Line2D([], [], color='black', marker='x', linestyle='None',
                                           markersize=10, label='Cluster-heads')

            plt.legend(handles=[black_x_marker, blue_base_station])
        else:
            plt.legend(handles=[blue_base_station])

        for node in self.network.nodes:
            x_coordinates = node.pos_x
            y_coordinates = node.pos_y
            if node.is_head:
                plt.scatter(x_coordinates, y_coordinates, color=node.color, s=150,
                            marker='x')
            else:
                plt.scatter(x_coordinates, y_coordinates, color=node.color, s=10)

        plt.title(title)
        # plt.legend(bbox_to_anchor=(1, 0.5), loc='center left')
        # lgd = plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.6))

        filename = title.replace(" ", "_").lower()
        plt.savefig(f'./results/{filename}.png')
        if cfg.show_plots:
            plt.show()
        plt.clf()

    def log_dead_node_once(self, round_counter):
        logging.info(f'First dead node in round {round_counter}')

