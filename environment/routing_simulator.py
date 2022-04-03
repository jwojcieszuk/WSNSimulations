import matplotlib.pyplot as plt
import logging

from decorators import run_once
from environment.network import Network
from routing_algorithms.routing_algorithm import RoutingAlgorithm
from routing_algorithms.direct_communication import DirectCommunication
from routing_algorithms.leach import Leach
from routing_algorithms.leach_c import LeachC
from metrics import RoutingAlgorithmMetrics


class RoutingSimulator:
    """
        This class simulates behaviour of an environment that is deployed in some field.
        Basically, it sends some impulse on a 2D plane and sensors deployed in certain area
        receives packets with data.
    """

    def __init__(self, num_of_nodes: int, initial_node_energy: float):
        self.network = Network(num_of_nodes, initial_node_energy)
        self.plot_environment("Deployed network")
        # each node informs base station about its location
        self.network.notify_position()
        self.routing_algorithm = None

    def simulate(self, routing_algorithm: RoutingAlgorithm, simulation_logger) -> RoutingAlgorithmMetrics:
        setattr(self, 'routing_algorithm', routing_algorithm)
        round_num, alive_nodes_num, avg_energy_dissipation = list(), list(), list()
        round_counter = 0
        plot_environment = run_once(self.plot_environment)

        while True:
            simulation_logger.info(f'{routing_algorithm.__repr__()} Running round: {round_counter} ')
            self._run_round(round_counter, plot_environment)
            round_num.append(round_counter)
            avg_energy_dissipation.append(self.network.avg_energy_dissipation())
            alive_nodes_num.append(len(self.network.get_alive_nodes()))

            if not self.check_network_life():
                simulation_logger.info(f'{routing_algorithm.__repr__()}: Network is dead after {round_counter} rounds')
                break

            round_counter += 1

        self.network.restore_initial_state()

        return RoutingAlgorithmMetrics(round_num, alive_nodes_num, avg_energy_dissipation, routing_algorithm.__repr__())

    def _run_round(self, round_counter: int, plot_enviornment_once):
        if isinstance(self.routing_algorithm, DirectCommunication):
            self.routing_algorithm.setup_phase(self.network.nodes)
            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network)
            self.network.reset_nodes()

        elif isinstance(self.routing_algorithm, LeachC):
            avg_energy = self.network.base_station.calculate_avg_energy(self.network.nodes)
            heads = self.routing_algorithm.setup_phase(self.network, round_counter, avg_energy)
            if plot_enviornment_once.has_run is False:
                plot_enviornment_once("LeachC")
            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network, heads)
            self.network.reset_nodes()

        elif isinstance(self.routing_algorithm, Leach):
            heads = self.routing_algorithm.setup_phase(self.network, round_counter)
            if plot_enviornment_once.has_run is False:
                plot_enviornment_once("Leach")
            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network, heads)
            self.network.reset_nodes()

    def check_network_life(self):
        if len(self.network.get_alive_nodes()) <= 5:
            return False
        return True

    def plot_environment(self, title):
        logging.info("Plotting deployed environment...")
        for node in self.network.nodes:
            x_coordinates = node.pos_x
            y_coordinates = node.pos_y
            if node.is_head:
                plt.scatter(x_coordinates, y_coordinates, color=node.color, s=500)
            else:
                plt.scatter(x_coordinates, y_coordinates, color=node.color, s=50)

        bs_x = self.network.base_station.pos_x
        bs_y = self.network.base_station.pos_y
        plt.scatter(bs_x, bs_y, c="blue", s=100)
        # plt.scatter(x_coordinates, y_coordinates, 250)
        plt.title(title)
        plt.show()
