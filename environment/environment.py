import matplotlib.pyplot as plt
import logging

from environment.network import Network
from routing_algorithms.direct_communication import DirectCommunication
from routing_algorithms.leach import Leach
from routing_algorithms.leach_c import LeachC


class Environment:
    """
        This class simulates behaviour of an environment that is deployed in some field.
        Basically, it sends some impulse on a 2D plane and sensors deployed in certain area
        receives packets with data.
    """

    def __init__(self):
        self.network = Network()
        # each node informs base station about its location
        self.network.notify_position()
        self.routing_algorithm = None

    def simulate(self, routing_algorithm):
        setattr(self, 'routing_algorithm', routing_algorithm)
        x_coordinates, y_coordinates = list(), list()
        # energy_dissipation_y = list()
        round_counter = 0
        while True:
            self._run_round(round_counter)
            x_coordinates.append(round_counter)
            y_coordinates.append(self.network.avg_energy_dissipation())
            # y_coordinates.append(len(self.network.get_alive_nodes()))
            if self.check_network_life() is False:
                logging.info("%s: Network is dead after %s rounds",
                             type(self.routing_algorithm), round_counter)
                break
            round_counter += 1

        self.network.restore_initial_state()
        return x_coordinates, y_coordinates

    def _run_round(self, round_counter):
        if isinstance(self.routing_algorithm, DirectCommunication):
            self.routing_algorithm.setup_phase(self.network.nodes)
            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network)
            self.network.reset_nodes()

        elif isinstance(self.routing_algorithm, LeachC):
            avg_energy = self.network.base_station.calculate_avg_energy(self.network.nodes)
            heads = self.routing_algorithm.setup_phase(self.network, round_counter, avg_energy)
            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network, heads)
            self.network.reset_nodes()

        elif isinstance(self.routing_algorithm, Leach):
            heads = self.routing_algorithm.setup_phase(self.network, round_counter)
            self.routing_algorithm.sensing_phase(self.network)
            self.routing_algorithm.transmission_phase(self.network, heads)
            self.network.reset_nodes()

    def check_network_life(self):
        for node in self.network.nodes:
            if node.alive:
                return True
        return False

    def plot_environment(self):
        logging.info("Plotting deployed environment...")
        for node in self.network.nodes:
            x_coordinates = node.pos_x
            y_coordinates = node.pos_y
            if node.is_head:
                plt.scatter(x_coordinates, y_coordinates, c=node.color, s=500, label=str(node.node_id))
            else:
                plt.scatter(x_coordinates, y_coordinates, c=node.color, s=50)

        bs_x = self.network.base_station.pos_x
        bs_y = self.network.base_station.pos_y
        plt.scatter(bs_x, bs_y, c="blue", s=100)
        # plt.scatter(x_coordinates, y_coordinates, 250)
        plt.legend(loc="upper right")
        plt.show()
