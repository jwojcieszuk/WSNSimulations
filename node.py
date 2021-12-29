
import numpy as np

class Node:
    def __init__(self, node_id, parent=0):
        self.pos_x = np.random.uniform(0, 250)
        self.pos_y = np.random.uniform(0, 250)
        #
        # if id == cf.BSID:
        #     self.energy_source = PluggedIn(self)
        # else:
        #     self.energy_source = Battery(self)

        self.id = node_id
        self.network_handler = parent
        self.next_hop = 0


    def transmit_data(self):
        pass

    def sense_environment(self):
        pass

    def __repr__(self):
        return "X: " + str(self.pos_x)\
               + " Y: " + str(self.pos_y)\
               + " ID: " + str(self.id)\
               + " Next hop: " + str(self.next_hop)
