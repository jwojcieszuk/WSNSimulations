import configuration as cfg
import random


class RoutingAlgorithm:
    """
        This is an interface for all implementations of routing algorithms
    """
    @staticmethod
    def setup_phase(*args, **kwargs):
        pass

    @staticmethod
    def transmission_phase(*args, **kwargs):
        pass

    @staticmethod
    def sensing_phase(network):
        for node in network.nodes:
            node.sense_environment()
