import logging
from node import Node, NodeTypes
import config as cfg


class Network(list):
    """
        This class handles operations of the whole network.
        
    """

    def __init__(self, init_nodes=None):
        logging.log('Instantiating nodes...')
        super().__init__()

        nodes = [Node(i, self) for i in range(0, cfg.NODES_NUMBER)]
        self.extend(nodes)

        base_station = NodeTypes.base_station
        base_station.pos_x = cfg.BS_POS_X
        base_station.pos_y = cfg.BS_POS_Y
        self.append(base_station)

        self._dict = {}
        for node in self:
            self._dict[node.id] = node

        self.round = 0
        self.routing_protocol = None

        # self.initial_energy = self.get_remaining_energy()
        # self.first_depletion = 0
        self.energy_spent = []


def simulate(self):
    pass
