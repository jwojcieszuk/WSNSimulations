import logging
import math

import numpy as np
from matplotlib import cm

import configuration as cfg
from routing_algorithms.routing_algorithm import RoutingAlgorithm
from utils import euclidean_distance, Colors


class Leach(RoutingAlgorithm):
    """
        Based on Energy-Efficient Communication Protocol for Wireless Microsensor Networks
        paper by Wendi Rabiner Heinzelman, Anantha Chandrakasan, and Hari Balakrishnan
    """

    def setup_phase(self, network, round_num=None):
        """
            During setup phase cluster heads are elected and clusters are formed.
        """
        alive_nodes = network.get_alive_nodes()
        clusters_num = math.floor(len(alive_nodes) * cfg.P)
        if clusters_num == 0:
            self._set_next_hop_as_bs(alive_nodes)
            return

        cluster_heads = self._elect_cluster_heads(alive_nodes, round_num)
        if not cluster_heads:
            self._set_next_hop_as_bs(alive_nodes)
            return

        self._form_clusters(cluster_heads, alive_nodes)

        return cluster_heads

    @staticmethod
    def _elect_cluster_heads(alive_nodes, round_num):
        threshold = cfg.P / (1 - cfg.P * (math.fmod(round_num, 1 / cfg.P)))
        reelect_round_num = 1/cfg.P

        if threshold == cfg.P:
            for node in alive_nodes:
                node.reelect_round_num = 0

        # if round_num == 0:
        #     color = iter(cm.rainbow(np.linspace(0, 1, clusters_num+10)))

        cluster_heads = list()

        j = 0
        for node in alive_nodes:
            random_num = np.random.uniform(0, 1)
            if random_num < threshold and node.reelect_round_num <= round_num:
                node.next_hop = cfg.BS_ID

                # if round_num == 0:
                #     node.color = next(color)

                node.is_head = True
                node.reelect_round_num = round_num + reelect_round_num
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
    def transmission_phase(network, heads):
        alive_nodes = network.get_alive_nodes()
        for node in alive_nodes:
            if node.is_head:
                continue
            node.transmit_data(network.get_node_by_id(node.next_hop))

        if heads is None:
            return

        for head in heads:
            head.aggregate_data()
            head.transmit_data(network.get_node_by_id(head.next_hop))

    @staticmethod
    def _set_next_hop_as_bs(alive_nodes):
        for node in alive_nodes:
            node.next_hop = cfg.BS_ID
