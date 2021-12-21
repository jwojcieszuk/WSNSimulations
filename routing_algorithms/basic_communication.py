import config as cfg
import logging

from routing_algorithms.factory import RoutingAlgorithm


class BasicCommunication(RoutingAlgorithm):

    def pre_communication(self, network):
        for node in network:
            node.next_hop = cfg.BS_ID

