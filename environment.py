import random

from network import Network

class Environment:
    """
        This class simulates behaviour of an environment that is deployed in some area.
        Basically, it sends some impulse on a 2D plane and sensors deployed in certain area
        receives packets with data.
        One network with multiple
    """
    def __init__(self):
        self.network = Network()

    def simulate_routing(self, routing_protocol):
        self.network.set_routing_protocol(routing_protocol)
        self.network.routing_protocol.setup_initial_hops(self.network)

        self.simulate_events()

    def simulate_events(self):
        node = random.choice(self.network)
        node.sense_environment()




