import logging
import math
import copy
import random

import numpy as np
from matplotlib import cm
from numpy.random import rand

from routing_algorithms.routing_algorithm import RoutingAlgorithm
import configuration as cfg
from utils import euclidean_distance, Colors


class LeachC(RoutingAlgorithm):
    def setup_phase(self, network, round_num=None, avg_energy=0):
        """
            During setup phase cluster heads are elected and clusters are formed.
        """
        # logging.info('LEACH: Advertisement Phase...')

        alive_nodes = network.get_alive_nodes()
        clusters_num = math.floor(len(alive_nodes) * cfg.P)
        if clusters_num == 0:
            self._set_next_hop_as_bs(alive_nodes)
            return

        cluster_heads = self._simulated_annealing_algorithm(network, avg_energy, clusters_num)
        if cluster_heads == 0:
            self._set_next_hop_as_bs(alive_nodes)
            return
        # form clusters in original network
        original_heads = self._form_clusters_original(network, cluster_heads)
        # cluster_heads = self._elect_cluster_heads(alive_nodes, avg_energy, clusters_num)

        return original_heads

    def _form_clusters_original(self, network, best_heads):
        color = iter(cm.rainbow(np.linspace(0, 1, len(best_heads))))
        j = 0
        original_heads = list()

        for head in best_heads:
            original_node = network.get_node_by_id(head.node_id)
            original_node.next_hop = cfg.BS_ID
            original_node.color = next(color)
            original_node.is_head = True
            original_heads.append(original_node)
            j += 1

        self._form_clusters(original_heads, network.get_alive_nodes())

        return original_heads

    @staticmethod
    def _elect_cluster_heads(alive_nodes, avg_energy, clusters_num):
        cluster_heads = list()
        i, j = 0, 0

        # nodes with energy level higher or equal than average
        eligible_nodes = [node for node in alive_nodes if node.energy_source.energy >= avg_energy]

        if len(eligible_nodes) == 0:
            return list()

        while len(cluster_heads) != clusters_num:
            node = random.choice(eligible_nodes)
            eligible_nodes.remove(node)
            node.next_hop = cfg.BS_ID
            node.is_head = True
            j += 1
            cluster_heads.append(node)

        return cluster_heads

    @staticmethod
    def _form_clusters(cluster_heads, alive_nodes):
        for node in alive_nodes:
            if node in cluster_heads:
                continue
            nearest_head = cluster_heads[0]

            for cluster_head in cluster_heads[1:]:
                if euclidean_distance(node, nearest_head) > euclidean_distance(node, cluster_head):
                    nearest_head = cluster_head

            node.next_hop = nearest_head.node_id
            node.color = nearest_head.color
            # nearest_head.cluster_nodes.append(node)

    @staticmethod
    def transmission_phase(network, heads, not_consume=False):
        # send data to cluster_heads
        alive_nodes = network.get_alive_nodes()
        for node in alive_nodes:
            if node.is_head:
                continue
            node.transmit_data(network.get_node_by_id(node.next_hop), not_consume=not_consume)

        if heads is None:
            return

        # send data from cluster_heads to the BS
        for head in heads:
            # head.aggregate_data()
            head.transmit_data(network.get_node_by_id(head.next_hop), not_consume=not_consume)

    @staticmethod
    def _set_next_hop_as_bs(alive_nodes):
        for node in alive_nodes:
            node.next_hop = cfg.BS_ID

    def _simulated_annealing_algorithm(self, network, avg_energy, clusters_num):
        """
            Implementation based on: https://machinelearningmastery.com/simulated-annealing-from-scratch-in-python/
        """
        copied_network = copy.deepcopy(network)
        dissipated_energy_list = list()

        for node in copied_network.nodes:
            dissipated_energy_list.append(node.dissipated_energy)

        alive_nodes = copied_network.get_alive_nodes()

        best_heads = self._elect_cluster_heads(alive_nodes, avg_energy, clusters_num)
        if len(best_heads) == 0:
            return list()
        best_energy_usage = self.calculate_energy_usage(copied_network, best_heads)
        print(f'Initial best energy usage={best_energy_usage}')

        temp = 10
        cooling_rate = 0.03
        round_number = 0

        curr_heads, curr_energy_usage = best_heads, best_energy_usage
        while temp > 1:
            copied_network.restore_for_annealing(dissipated_energy_list)

            round_number += 1

            candidate_heads = self._elect_cluster_heads(copied_network.get_alive_nodes(), avg_energy, clusters_num)
            if len(candidate_heads) == 0:
                break

            self._form_clusters(candidate_heads, copied_network.get_alive_nodes())
            candidate_energy_usage = self.calculate_energy_usage(copied_network, candidate_heads)

            if candidate_energy_usage < best_energy_usage:
                best_heads, best_energy_usage = candidate_heads, candidate_energy_usage

            diff = candidate_energy_usage - curr_energy_usage

            # temperature for current epoch
            t = temp / float(round_number)

            # metropolis acceptance criterion
            metropolis = np.exp(-diff / t)

            if diff < 0 or rand() < metropolis:
                curr_heads, curr_energy_usage = candidate_heads, candidate_energy_usage

            temp *= 1 - cooling_rate

        print(f'Best energy usage={best_energy_usage}')
        return best_heads

    def calculate_energy_usage(self, network, heads):
        self.sensing_phase(network, True)
        self.transmission_phase(network, heads, True)
        return network.total_energy_dissipation()
