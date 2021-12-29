import config as cfg
import logging

from routing_algorithms.factory import RoutingAlgorithm


class BasicCommunication(RoutingAlgorithm):
    """
        In basic communication each node next hop is base station ID
    """
    @staticmethod
    def init_communication(network):
        for node in network:
            node.next_hop = cfg.BS_ID

