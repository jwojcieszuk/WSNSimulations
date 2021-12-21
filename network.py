import logging
from node import Node, NodeTypes
import config as cfg


class Network(list):
    """
        This class handles whole network (sensor nodes, base station)
    """
    def __init__(self, init_nodes=None):
        super().__init__()
        logging.debug('Instantiating nodes...')
        if init_nodes:
            self.extend(init_nodes)
        else:
            nodes = [Node(i, self) for i in range(0, cfg.NODES_NUMBER)]
            self.extend(nodes)
            # last node in nodes is the base station
            base_station = NodeTypes.base_station
            base_station.pos_x = cfg.BS_POS_X
            base_station.pos_y = cfg.BS_POS_Y
            self.append(base_station)

        self._dict = {}
        for node in self:
            self._dict[node.id] = node

        # self.perform_two_level_comm = 1
        self.round = 0
        # self.centroids = []
        self.routing_protocol = None
        # self.sleep_scheduler_class = None

        # self.initial_energy = self.get_remaining_energy()
        # self.first_depletion = 0
        # self.per30_depletion = 0
        self.energy_spent = []

    def simulate(self):

