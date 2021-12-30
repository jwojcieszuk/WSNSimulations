import logging
from node import Node
import config as cfg


class Network(list):
    """
        This class handles operations of the whole network.
        Instantiating nodes, base station.
    """

    def __init__(self):
        super().__init__()
        logging.info('Instantiating nodes...')

        nodes = [Node(i, self) for i in range(0, cfg.NODES_NUMBER)]
        self.extend(nodes)
        base_station = Node(cfg.BS_ID)
        base_station.pos_x = cfg.BS_X
        base_station.pos_y = cfg.BS_Y
        self.append(base_station)


    # def simulate(self):
    #     """
    #     simulation for basic scenario
    #     init communication in order to setup next hop for each node
    #
    #     """
    #     self.routing_protocol.init_communication(self)
    #
    #     #send packets to 5 random nodes

    def broadcast_next_hop(self):
        base_station = self.get_base_station()
        if base_station:
            base_station.transmit_data()

    def get_base_station(self):
        return self.get_node_by_id(cfg.BS_ID)

    def get_node_by_id(self, node_id):
        return self.network_dict[node_id]

    def print_nodes(self):
        for node in self:
            print(node)

    def set_routing_protocol(self, routing_protocol):
        self.routing_protocol = routing_protocol