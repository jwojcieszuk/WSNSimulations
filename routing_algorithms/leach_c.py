from routing_algorithms.routing_algorithm import RoutingAlgorithm
import configuration as cfg
from utils import euclidean_distance


class LeachC(RoutingAlgorithm):
    def setup_phase(self, network, round_num=None, avg_energy=0):
        """
            During setup phase cluster heads are elected and clusters are formed.
        """
        # logging.info('LEACH: Advertisement Phase...')

        alive_nodes = network.get_alive_nodes()

        cluster_heads = self._elect_cluster_heads(alive_nodes, round_num, avg_energy)
        self._form_clusters(cluster_heads, alive_nodes)

        return cluster_heads

    def _elect_cluster_heads(self, alive_nodes, round_num, avg_energy):
        cluster_heads = list()
        i, j = 0, 0

        while len(cluster_heads) != cfg.CLUSTERS_NUM:
            node = alive_nodes[i]
            if node.energy_source.energy >= avg_energy:
                node.next_hop = cfg.BS_ID
                # node.color = Colors.colors_list[j]
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
            # node.color = nearest_head.color
            # nearest_head.cluster_nodes.append(node)

    @staticmethod
    def transmission_phase(network, heads):
        # logging.info('Transmission phase for LEACH')
        # send data to cluster_heads
        alive_nodes = network.get_alive_nodes()
        for node in alive_nodes:
            if node.is_head:
                continue
            node.transmit_data(network.network_dict[node.next_hop])

        # send data from cluster_heads to the BS
        for head in heads:
            head.transmit_data(network.get_node_by_id(head.next_hop))
