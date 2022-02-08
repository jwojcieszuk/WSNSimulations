import configuration as cfg
import random


class RoutingAlgorithm:
    """
        This is an interface for all implementations of routing algorithms
    """
    @staticmethod
    def setup_phase(network):
        pass

    @staticmethod
    def broadcast(network):
        network.broadcast_next_hop()

    @staticmethod
    def sensing_phase(network):
        for node in network.nodes:
            node.sense_environment()
