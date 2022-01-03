import random
import matplotlib.pyplot as plt
import config as cfg
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
        self.network.routing_protocol.setup_initial_hops(self.network)
        self.plot_environment()

        for round in range(cfg.ROUNDS):
            self.simulate_events()
            self.network.transmit_data()

    def simulate_events(self):
        node = random.choice(self.network)
        node.sense_environment()

    def plot_environment(self):
        logging.info("Plotting deployed environment...")
        x_coordinates = []
        y_coordinates = []
        for node in self.network:
            x_coordinates.append(node.pos_x)
            y_coordinates.append(node.pos_y)
        bs_x = self.network.base_station.pos_x
        bs_y = self.network.base_station.pos_y
        plt.scatter(bs_x, bs_y, c="red")
        plt.scatter(x_coordinates, y_coordinates, 250)
        plt.show()

