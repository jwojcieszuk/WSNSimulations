import logging
import math

import numpy as np

import configuration as cfg


class Leach:
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

    @staticmethod
    def advertisement_phase(network, round_num, prev_heads=None):
        logging.info('LEACH: Advertisement Phase...')

        alive_nodes = network.get_alive_nodes()

        threshold = cfg.P / (1 - cfg.P * (math.fmod(round_num, 1 / cfg.P)))

        cluster_heads = list()
        i = 0
        while len(cluster_heads) != cfg.CLUSTERS_NUM:
            node = alive_nodes[i]
            random_num = np.random.uniform(0, 1)
            if random_num < threshold:
                node.next_hop = cfg.BS_ID
                cluster_heads.append(node)

            i = i + 1 if i < len(alive_nodes) - 1 else 0



