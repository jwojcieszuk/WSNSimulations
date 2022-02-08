import matplotlib.pyplot as plt
import logging

from environment.network import Network


class Environment:
    """
        This class simulates behaviour of an environment that is deployed in some area.
        Basically, it sends some impulse on a 2D plane and sensors deployed in certain area
        receives packets with data.
    """

    def __init__(self):
        self.network = Network()

    def simulate(self, routing_protocol):
        setattr(self.network, 'routing_protocol', routing_protocol)
        x_coordinates, y_coordinates = list(), list()
        round = 0

        while True:
            self.network.routing_protocol.setup_phase(self.network.nodes)
            # logging.info("Current round: %s", round)
            self.network.routing_protocol.sensing_phase(self.network)
            self.network.routing_protocol.transmission_phase(self.network)
            self.network.pre_round_initialization()
            x_coordinates.append(round)
            y_coordinates.append(len(self.network.get_alive_nodes()))
            if self.check_network_life() is False:
                logging.info("Basic Communication: Network is dead after %s rounds. Base Station received %s messages.", round,
                             self.network.base_station.packets_received_count)
                break
            round += 1

        self.network.restore_initial_state()
        return x_coordinates, y_coordinates

    def simulate_leach(self, routing_protocol):
        setattr(self.network, 'routing_protocol', routing_protocol)
        x_coordinates = list()
        y_coordinates = list()
        round = 0
        while True:
            heads = self.network.routing_protocol.setup_phase(self.network, round)
            # self.plot_environment()
            self.network.routing_protocol.sensing_phase(self.network)
            self.network.routing_protocol.transmission_phase(self.network, heads)
            # logging.info("Base station received %s messages", self.network.base_station.packets_received_count)
            self.network.pre_round_initialization()

            if self.check_network_life() is False:
                logging.info("LEACH: Network is dead after %s rounds. Base Station received %s messages.", round,
                             self.network.base_station.packets_received_count)
                break
            x_coordinates.append(round)
            y_coordinates.append(len(self.network.get_alive_nodes()))
            round += 1

        return x_coordinates, y_coordinates

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
        plt.legend(loc="upper left")
        plt.show()


class Plotter:
    def __init__(self):
        self.x_coordinates = list()
        self.y_coordinates = list()

    def plot_nodes_alive_vs_network_lifetime(self):
        plt.plot(self.x_coordinates, self.y_coordinates)

    @staticmethod
    def show_plot():
        plt.show()
