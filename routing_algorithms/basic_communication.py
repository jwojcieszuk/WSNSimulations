import configuration as cfg
import logging

from routing_algorithms.routing_algorithm import RoutingAlgorithm


class BasicCommunication(RoutingAlgorithm):
    """
        In basic communication each node next hop is base station ID
    """
    @staticmethod
    def setup_phase(nodes):
        # logging.info('Setting up inital hops for Basic Communication..')
        for node in nodes:
            node.next_hop = cfg.BS_ID

    @staticmethod
    def transmission_phase(network, heads=None):
        # logging.info('Transmission phase for Basic Communication..')
        alive_nodes = network.get_alive_nodes()
        for node in alive_nodes:
            node.transmit_data(network.get_node_by_id(node.next_hop))
