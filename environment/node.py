import functools
import logging
import configuration as cfg
import numpy as np

from environment.energy_source import Battery
from utils import Colors, euclidean_distance


class Node:
    def __init__(self, node_id, parent=0):
        self.node_id = node_id
        self.network_handler = parent
        self.pos_x = np.random.uniform(10, 210)
        self.pos_y = np.random.uniform(10, 210)
        self.energy_source = Battery(self)
        self.next_hop = 0
        self.contains_data = False
        self.alive = True
        self.color = None
        self.is_head = False
        self.packets_received_count = 0
        self.cluster_nodes = list()

    def __call__(self, obj, o, o1):
        if obj is None:
            return obj

    def _alive_node_only(func):
        @functools.wraps(func)
        def wrapper(node, *args, **kwargs):
            if node.alive:
                func(node, *args, **kwargs)
            elif node.energy_source.energy == 0:
                # logging.info("Node %s is not alive! Cannot sense data.", node.node_id)
                pass
        return wrapper

    @_alive_node_only
    def transmit_data(self, destination_node):
        energy_cost = self._calculate_energy_cost(destination_node)
        self.energy_source.consume(energy_cost)

        # if transmitting node is cluster head, transmit aggregated packet count
        # if ordinary node, transmit 1 packet
        if self.is_head:
            destination_node.receive_data(self.packets_received_count)
        else:
            destination_node.receive_data(1)
        self.packets_received_count = 0
        self.contains_data = False

    def _calculate_energy_cost(self, destination_node):
        distance = euclidean_distance(self, destination_node)
        energy = cfg.E_ELEC * cfg.k + cfg.Eamp * cfg.k * distance ** 2
        if self.energy_source.energy < energy:
            self.energy = 0
            self.battery_dead()

        return energy

    def battery_dead(self):
        self.alive = False
        self.energy_source.energy = 0
        self.color = Colors.BLACK

    @_alive_node_only
    def sense_environment(self):
        # logging.info("Node %s sensing data. Energy level: %s", self.node_id, self.energy_source.energy)
        # self.energy_source.consume(cfg.RECEIVER_ENERGY_COST)
        self.contains_data = True
        # energy dissipated by a node for the reception ERx(k) of a message of k bits
        energy_cost = cfg.E_ELEC * cfg.k
        self.energy_source.consume(energy_cost)

    def __repr__(self):
        return "X: " + str(self.pos_x)\
               + " Y: " + str(self.pos_y)\
               + " ID: " + str(self.node_id)\
               + " Next hop: " + str(self.next_hop)\
               + " contains data: " + str(self.contains_data)\
               + " energy: " + str(self.energy_source.energy)\
               + " is head: " + str(self.is_head)\
               + " packets counts: " + str(self.packets_received_count)

    def aggregate_data(self):
        for node in self.cluster_nodes:
            node.transmit_data(self)

    def receive_data(self, packets_num):
        # energy dissipated by a node for the reception ERx(k) of a message of k bits
        energy_cost = cfg.E_ELEC * cfg.k
        self.energy_source.consume(energy_cost)
        self.contains_data = True
        self.packets_received_count += packets_num

    def pre_round_initialization(self):
        self.next_hop = 0
        self.contains_data = False
        self.color = None
        self.is_head = False

    def restore_initial_state(self):
        self.energy_source = Battery(self)
        self.next_hop = 0
        self.contains_data = False
        self.alive = True
        self.color = None
        self.is_head = False
        self.packets_received_count = 0


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

    def receive_data(self, packets_num):
        self.packets_received_count += packets_num

    @staticmethod
    def calculate_avg_energy(nodes):
        return sum([node.energy_source.energy for node in nodes])/cfg.NODES_NUM
