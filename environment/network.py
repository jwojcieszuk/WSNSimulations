import logging
import config as cfg
from environment.node import Node, BaseStation


class Network:
    """
        This class handles operations of the whole environment.
        Deploying nodes, base station.
    """

    def __init__(self):
        logging.info('Deploying nodes...')

        self.nodes = [Node(i, self) for i in range(0, cfg.NODES_NUMBER)]
        self.base_station = BaseStation()
        self.network_dict = {node.node_id: node for node in self.nodes}
        self.routing_protocol = None
        self.network_life = True

    def transmit_data(self):
        for node in self.nodes:
            destination_node = self.get_node_by_id(node.next_hop)
            node.transmit_data(destination_node)

    def get_base_station(self):
        return self.get_node_by_id(cfg.BS_ID)

    def get_node_by_id(self, node_id):
        if node_id == cfg.BS_ID:
            return self.base_station

        return self.network_dict[node_id]

    def print_nodes(self):
        for node in self.nodes:
            print(node)
