import logging
import configuration as cfg
import numpy as np

from decorators import alive_node
from environment.energy_source import Battery


class Node:
    def __init__(self, node_id, parent=0):
        self.node_id = node_id
        self.network_handler = parent
        self.pos_x = np.random.uniform(0, 250)
        self.pos_y = np.random.uniform(0, 250)
        self.energy_source = Battery(self)
        self.next_hop = 0
        self.contains_data = False
        self.alive = True
        self.color = None
        self.is_head = False

    def transmit_data(self, destination_node):
        if self.contains_data:
            self.energy_source.consume(1)
            destination_node.receive_data()
            self.contains_data = False

    def battery_dead(self):
        self.alive = False

    @alive_node
    def sense_environment(self):
        logging.info("Node %s sensing data. Energy level: %s", self.node_id, self.energy_source.energy)
        self.contains_data = True

    def __repr__(self):
        return "X: " + str(self.pos_x)\
               + " Y: " + str(self.pos_y)\
               + " ID: " + str(self.node_id)\
               + " Next hop: " + str(self.next_hop)\
               + " contains data: " + str(self.contains_data)\
               + " energy: " + str(self.energy_source.energy)\
               + " is head: " + str(self.is_head)\



class BaseStation:
    def __init__(self):
        self.node_id = cfg.BS_ID
        self.pos_x = cfg.BS_X
        self.pos_y = cfg.BS_Y
        self.packets_received_count = 0

    def __repr__(self):
        return "Base station" +\
               " ID: " + str(self.node_id)+\
               " X:" + str(self.pos_x) +\
               " Y:" + str(self.pos_y) +\
                " packets_received_count: " + str(self.packets_received_count)

    def receive_data(self):
        self.packets_received_count += 1

