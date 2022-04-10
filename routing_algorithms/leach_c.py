import logging

import numpy as np
from matplotlib import cm

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
        clusters_num = round(len(alive_nodes) * cfg.P)
        if clusters_num == 0:
            self._set_next_hop_as_bs(alive_nodes)
            return

        cluster_heads = self._elect_cluster_heads(alive_nodes, avg_energy, clusters_num)
        self._form_clusters(cluster_heads, alive_nodes)

        return cluster_heads

    def _elect_cluster_heads(self, alive_nodes, avg_energy, clusters_num):
        cluster_heads = list()
        i, j = 0, 0
        color = iter(cm.rainbow(np.linspace(0, 1, 5)))

        while len(cluster_heads) != clusters_num:
            node = alive_nodes[i]

            if node.energy_source.energy >= avg_energy:
                node.next_hop = cfg.BS_ID
                node.color = next(color)
                node.is_head = True
                j += 1
                cluster_heads.append(node)

            i = i + 1 if i < len(alive_nodes) - 1 else 0

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
    def transmission_phase(network, heads):
        logging.info('Transmission phase for LEACH')
        # send data to cluster_heads
        alive_nodes = network.get_alive_nodes()
        for node in alive_nodes:
            if node.is_head:
                continue
            node.transmit_data(network.get_node_by_id(node.next_hop))

        if heads is None:
            return

        # send data from cluster_heads to the BS
        for head in heads:
            head.aggregate_data()
            head.transmit_data(network.get_node_by_id(head.next_hop))

    def _set_next_hop_as_bs(self, alive_nodes):
        for node in alive_nodes:
            node.next_hop = cfg.BS_ID
