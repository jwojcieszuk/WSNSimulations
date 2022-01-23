import random
import matplotlib.pyplot as plt
import configuration as cfg
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

    def simulate_routing(self, routing_protocol):
        setattr(self.network, 'routing_protocol', routing_protocol)
        self.network.routing_protocol.setup_phase(self.network.nodes)
        # self.plot_environment()
        round = 0
        while(True):
            self.simulate_event()
            self.network.transmit_data()
            round += 1
            if not self.check_network_life():
                logging.info("Network is dead after %s rounds. Base Station received %s messages.", round, self.network.base_station.packets_received_count)
                break

    def simulate_leach(self, routing_protocol):
        setattr(self.network, 'routing_protocol', routing_protocol)
        counter = 0
        heads = self.network.routing_protocol.advertisement_phase(self.network, counter)
        self.plot_environment()

        # while counter < cfg.ROUNDS:
        #     heads = self.network.routing_protocol.advertisement_phase(self.network, counter, heads)
        #     counter += 1
        #     # cluster_heads broadcasts an advertisement message to the rest of the nodes
        #
        #     self.plot_environment()

    def simulate_event(self):
        node = random.choice(self.network.nodes)
        node.sense_environment()

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
                plt.scatter(x_coordinates, y_coordinates, c=node.color, s=500)
            else:
                plt.scatter(x_coordinates, y_coordinates, c=node.color, s=50)

        bs_x = self.network.base_station.pos_x
        bs_y = self.network.base_station.pos_y
        plt.scatter(bs_x, bs_y, c="blue", s=100)
        # plt.scatter(x_coordinates, y_coordinates, 250)
        plt.show()

