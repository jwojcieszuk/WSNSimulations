import logging
from node import Node
import config as cfg


class Network(list):
    """
        This class handles operations of the whole network.
        Instantiating nodes, base station.
    """

    def __init__(self, routing_protocol=None):
        logging.info('Instantiating nodes...')
        super().__init__()

        nodes = [Node(i, self) for i in range(0, cfg.NODES_NUMBER)]
        self.extend(nodes)

        base_station = Node(cfg.BS_ID)
        base_station.pos_x = cfg.BS_X
        base_station.pos_y = cfg.BS_Y
        self.append(base_station)

        self.routing_protocol = routing_protocol

    def simulate(self):
        self.routing_protocol.init_communication(self)

    def broadcast_next_hop(self):


    def print_nodes(self):
        for node in self:
            print(node)