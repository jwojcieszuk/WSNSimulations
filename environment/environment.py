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

    def simulate_direct_communication(self, routing_protocol):
        setattr(self.network, 'routing_protocol', routing_protocol)
        self.network.routing_protocol.setup_phase(self.network.nodes)
        # self.plot_environment()
        round = 0
        while True:
            logging.info("Current round: %s", round)
            self.network.routing_protocol.sensing_phase(self.network)
            self.network.routing_protocol.transmission_phase(self.network)
            round += 1
            if self.check_network_life() is False:
                logging.info("Basic Communication: Network is dead after %s rounds. Base Station received %s messages.", round,
                             self.network.base_station.packets_received_count)
                break
        self.network.restore_initial_state()

    def simulate_leach(self, routing_protocol):
        setattr(self.network, 'routing_protocol', routing_protocol)
        counter = 0
        # self.plot_environment()
        heads = self.network.routing_protocol.setup_phase(self.network, counter)
        self.plot_environment()
        self.network.routing_protocol.sensing_phase(self.network)
        self.network.routing_protocol.transmission_phase(self.network, heads)
        self.network.pre_round_initialization()
        # logging.info("Base station received %s messages", self.network.base_station.packets_received_count)
        round = 0
        while True:
            heads = self.network.routing_protocol.setup_phase(self.network, counter)
            # self.plot_environment()
            self.network.routing_protocol.sensing_phase(self.network)
            self.network.routing_protocol.transmission_phase(self.network, heads)
            logging.info("Base station received %s messages", self.network.base_station.packets_received_count)
            self.network.pre_round_initialization()

            if self.check_network_life() is False:
                logging.info("LEACH: Network is dead after %s rounds. Base Station received %s messages.", round,
                             self.network.base_station.packets_received_count)
                break
            round += 1

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
