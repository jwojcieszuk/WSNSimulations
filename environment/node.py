import logging

import configuration as cfg
import numpy as np

from decorators import _alive_node_only, _cluster_head_only
from environment.energy_source import Battery
from utils import Colors, euclidean_distance


class Node:
    def __init__(self, node_id, energy, simulation_logger, parent=0):
        self.node_id = node_id
        self.network_handler = parent
        self.pos_x = np.random.uniform(cfg.target_field_x_axis[0], cfg.target_field_x_axis[1])
        self.pos_y = np.random.uniform(cfg.target_field_x_axis[0], cfg.target_field_x_axis[1])
        self.energy_source = Battery(self, energy)
        self.next_hop = 0
        self.contains_data = False
        self.alive = True
        self.color = None
        self.is_head = False
        self.re_elect = 0
        self.dissipated_energy = 0
        self.received_packets = 0
        self.sensed_packets = 0
        self.logger = simulation_logger
        self.reelect_round_num = 0

    @_alive_node_only
    def transmit_data(self, destination_node, bits=cfg.k):
        energy_cost = self._calculate_energy_cost(destination_node, bits)
        if energy_cost == 0:
            return

        self.dissipated_energy += energy_cost
        self.energy_source.consume(energy_cost)
        if self.is_head:
            destination_node.receive_data(packets=self.received_packets+self.sensed_packets)
        else:
            destination_node.receive_data(packets=self.sensed_packets)
        self.received_packets = 0
        self.sensed_packets = 0
        self.contains_data = False

    def receive_data(self, packets):
        # energy dissipated by a node for the reception ERx(k) of a message of k bits
        if self.is_head:
            energy_cost = (cfg.E_ELEC+cfg.E_DA) * cfg.k
        else:
            energy_cost = cfg.E_ELEC * cfg.k
        self.dissipated_energy += energy_cost
        self.energy_source.consume(energy_cost)
        self.received_packets += packets
        self.contains_data = True

    def _calculate_energy_cost(self, destination_node, bits):
        distance = euclidean_distance(self, destination_node)
        if self.is_head:
            energy = (cfg.E_ELEC+cfg.E_DA) * cfg.k + cfg.E_AMP * bits * distance ** 2
        else:
            energy = cfg.E_ELEC * cfg.k + cfg.E_AMP * bits * distance ** 2
        if self.energy_source.energy < energy:
            self.battery_dead()
            return 0

        return energy

    def battery_dead(self):
        self.logger.info(f'Node {self.node_id} is dead.')
        self.alive = False
        self.energy_source.energy = 0
        self.color = Colors.BLACK

    @_alive_node_only
    def sense_environment(self):
        # logging.info(f'Node {self.node_id} sensing data. Energy level:{self.energy_source.energy}')
        self.contains_data = True
        # energy dissipated by a node for the reception ERx(k) of a message of k bits
        energy_cost = cfg.E_ELEC * cfg.k
        self.dissipated_energy += energy_cost
        self.energy_source.consume(energy_cost)
        self.sensed_packets = 1

    def __repr__(self):
        return "X: " + str(self.pos_x)\
               + " Y: " + str(self.pos_y)\
               + " ID: " + str(self.node_id)\
               + " Next hop: " + str(self.next_hop)\
               + " contains data: " + str(self.contains_data)\
               + " energy: " + str(self.energy_source.energy)\
               + " is head: " + str(self.is_head)

    def pre_round_initialization(self):
        self.next_hop = 0
        self.contains_data = False
        self.color = None
        self.is_head = False
        self.sensed_packets = 0
        # self.dissipated_energy = 0

    def restore_initial_state(self, initial_node_energy):
        self.energy_source = Battery(self, initial_node_energy)
        self.next_hop = 0
        self.contains_data = False
        self.alive = True
        self.color = None
        self.is_head = False
        self.dissipated_energy = 0
        self.sensed_packets = 0
        self.received_packets = 0

    @_cluster_head_only
    def aggregate_data(self):
        # number of bits to be sent increase while forwarding messages
        energy = cfg.E_DA * cfg.HEADER
        self.energy_source.consume(energy)

    @_cluster_head_only
    def announce_entire_network(self, nodes):
        for node in nodes:
            energy_cost = self._calculate_energy_cost(node, 100)
            if energy_cost == 0:
                return

            self.dissipated_energy += energy_cost
            self.energy_source.consume(energy_cost)
            node.receive_data(packets=0)


class BaseStation:
    def __init__(self, pos_x, pos_y):
        self.node_id = cfg.BS_ID
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.received_packets = 0

    def __repr__(self):
        return "Base station" +\
               " ID: " + str(self.node_id)+\
               " X:" + str(self.pos_x) +\
               " Y:" + str(self.pos_y)

    def receive_data(self, packets):
        self.received_packets += packets

    def calculate_avg_energy(self, nodes, base_station):
        for node in nodes:
            node.transmit_data(base_station, 10)

        return sum([node.energy_source.energy for node in nodes])/len(nodes)
