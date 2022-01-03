import config as cfg
import logging

from routing_algorithms.routing_algorithm import RoutingAlgorithm


class BasicCommunication(RoutingAlgorithm):
    """
        In basic communication each node next hop is base station ID
    """
    @staticmethod
    def setup_initial_hops(network):
        logging.info('Setting up inital hops for Basic Communication..')
        for node in network:
            node.next_hop = cfg.BS_ID

