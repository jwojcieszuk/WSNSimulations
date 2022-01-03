import logging
import config as cfg
from environment.node import Node, BaseStation


class Network(list):
    """
        This class handles operations of the whole environment.
        Deploying nodes, base station.
    """

    def __init__(self):
        super().__init__()
        logging.info('Deploying nodes...')

        nodes = [Node(i, self) for i in range(0, cfg.NODES_NUMBER)]
        self.extend(nodes)
        self.base_station = BaseStation()
        self.network_dict = {node.node_id: node for node in self}
        self.routing_protocol = None

    def transmit_data(self):
        for node in self:
            if node.node_id == cfg.BS_ID:
                continue
            destination_node = self.get_node_by_id(node.next_hop)
            node.transmit_data(destination_node)

    # def broadcast_next_hop(self):
    #     base_station = self.get_base_station()
    #     if base_station:
    #         base_station.transmit_data()

    def get_base_station(self):
        return self.get_node_by_id(cfg.BS_ID)

    def get_node_by_id(self, node_id):
        if node_id == cfg.BS_ID:
            return self.base_station

        return self.network_dict[node_id]

    def print_nodes(self):
        for node in self:
            print(node)
