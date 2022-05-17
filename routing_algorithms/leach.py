import logging
import math

import numpy as np
from matplotlib import cm

import configuration as cfg
from routing_algorithms.routing_algorithm import RoutingAlgorithm
from utils import euclidean_distance, Colors


class Leach(RoutingAlgorithm):
    """
        LEACH is a self-organizing, adaptive clustering protocol
        that uses randomization to distribute the energy load evenly
        among the sensors in the network. In LEACH, the nodes
        organize themselves into local clusters, with one node act-
        ing as the local base station or cluster-head. If the cluster-
        heads were chosen a priori and fixed throughout the system
        lifetime, as in conventional clustering algorithms, it is easy
        to see that the unlucky sensors chosen to be cluster-heads
        would die quickly, ending the useful lifetime of all nodes
        belonging to those clusters

        The operation of LEACH is broken up into rounds,
        where each round begins with a set-up phase, when the clus-
        ters are organized, followed by a steady-state phase, when
        data transfers to the base station occur. In order to mini-
        mize overhead, the steady-state phase is long compared to
        the set-up phase.

        Based on Energy-Efficient Communication Protocol for Wireless Microsensor Networks
        paper by Wendi Rabiner Heinzelman, Anantha Chandrakasan, and Hari Balakrishnan
    """

    def setup_phase(self, network, round_num=None):
        """
            During setup phase cluster heads are elected and clusters are formed.
        """
        # logging.info('LEACH: Advertisement Phase...')

        alive_nodes = network.get_alive_nodes()
        clusters_num = math.floor(len(alive_nodes) * cfg.P)
        if clusters_num == 0:
            self._set_next_hop_as_bs(alive_nodes)
            return

        cluster_heads = self._elect_cluster_heads(alive_nodes, round_num, clusters_num)
        self._form_clusters(cluster_heads, alive_nodes)

        return cluster_heads

    @staticmethod
    def _elect_cluster_heads(alive_nodes, round_num, clusters_num):
        threshold = cfg.P / (1 - cfg.P * (math.fmod(round_num, 1 / cfg.P)))
        reelect_round_num = 1/cfg.P

        if threshold == cfg.P:
            for node in alive_nodes:
                node.reelect_round_num = 0

        color = iter(cm.rainbow(np.linspace(0, 1, clusters_num)))
        cluster_heads = list()

        # nodes_can_be_reelected = [node for node in alive_nodes if node.reelect_round_num <= round_num]
        # if len(nodes_can_be_reelected) < clusters_num:
        #     pass

        i, j = 0, 0
        while len(cluster_heads) != clusters_num:
            node = alive_nodes[i]
            random_num = np.random.uniform(0, 1)

            if random_num < threshold and node.reelect_round_num <= round_num:
                node.next_hop = cfg.BS_ID
                node.color = next(color)
                node.is_head = True
                node.reelect_round_num = round_num + reelect_round_num
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
        alive_nodes = network.get_alive_nodes()
        # nodes transmit data to cluster_heads
        # or directly to base station if heads==0
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
