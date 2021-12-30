import config as cfg
import numpy as np

from energy_source import PluggedIn, Battery


class Node:
    def __init__(self, node_id, parent=0):
        self.pos_x = np.random.uniform(0, 250)
        self.pos_y = np.random.uniform(0, 250)

        if node_id == cfg.BS_ID:
            self.energy_source = PluggedIn(self)
        else:
            self.energy_source = Battery(self)

        self.node_id = node_id
        self.network_handler = parent
        self.next_hop = 0
        self.contains_data = False

    def setup_base_station(self):
        self.node_id = cfg.BS_ID
        self.pos_x = cfg.BS_X
        self.pos_y = cfg.BS_Y

    def transmit_data(self):
        pass

    def sense_environment(self):
        self.contains_data = True

    def __repr__(self):
        return "X: " + str(self.pos_x)\
               + " Y: " + str(self.pos_y)\
               + " ID: " + str(self.node_id)\
               + " Next hop: " + str(self.next_hop)\
               + " data: " + str(self.contains_data)

