import logging
import configuration as cfg
from environment.node import Node, BaseStation


class Network:
    def __init__(self, num_of_nodes):
        logging.info('Deploying nodes...')

        self.nodes = [Node(i, self) for i in range(1, num_of_nodes)]
        self.base_station = BaseStation()
        self.network_dict = {node.node_id: node for node in self.nodes}
        self.routing_protocol = None
        self.network_life = True

    def get_base_station(self):
        return self.get_node_by_id(cfg.BS_ID)

    def get_node_by_id(self, node_id):
        if node_id == cfg.BS_ID:
            return self.base_station

        return self.network_dict[node_id]

    def get_alive_nodes(self):
        alive_nodes = list()
        for node in self.nodes:
            if node.alive:
                alive_nodes.append(node)

        return alive_nodes

    def print_nodes(self):
        for node in self.nodes:
            print(node)

    def reset_nodes(self):
        for node in self.nodes:
            node.pre_round_initialization()

    def restore_initial_state(self):
        for node in self.nodes:
            node.restore_initial_state()
        self.base_station = BaseStation()

    def notify_position(self):
        """Every node transmit its position directly to the base station."""
        for node in self.get_alive_nodes():
            node.transmit_data(self.base_station)

    def avg_energy_dissipation(self):
        return sum([node.dissipated_energy for node in self.nodes])/len(self.nodes)
