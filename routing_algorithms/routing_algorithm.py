import configuration as cfg
import random


class RoutingAlgorithm:
    """
        This is an interface for all implementations of routing algorithms
    """
    def __init__(self, name):
        self._name = name

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

    def __repr__(self):
        return self._name
