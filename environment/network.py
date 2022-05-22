import logging
import configuration as cfg
from environment.node import Node, BaseStation


class Network:
    def __init__(self, num_of_nodes, initial_node_energy, simulation_logger, bs_x, bs_y):
        logging.info('Deploying nodes...')

        self.nodes = [
            Node(
                node_id=i, parent=self,
                energy=initial_node_energy,
                simulation_logger=simulation_logger
            ) for i in range(0, num_of_nodes)
        ]
        self.bs_x = bs_x
        self.bs_y = bs_y
        self.base_station = BaseStation(bs_x, bs_y)
        self.network_dict = {node.node_id: node for node in self.nodes}
        self.routing_protocol = None
        self.network_life = True
        self.initial_node_energy = initial_node_energy

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

    def restore_for_annealing(self, dissipated_energy_list):
        i = 0
        for node in self.nodes:
            node.restore_for_annealing(dissipated_energy_list[i])
            i += 1

    def restore_initial_state(self):
        for node in self.nodes:
            node.restore_initial_state(self.initial_node_energy)
        self.base_station = BaseStation(self.bs_x, self.bs_y)

    def notify_position(self):
        """Every node transmit its position directly to the base station."""
        for node in self.get_alive_nodes():
            node.transmit_data(self.base_station)

    def avg_energy_dissipation(self):
        return sum([node.dissipated_energy for node in self.nodes])/len(self.nodes)

    def total_energy_dissipation(self):
        return sum([node.dissipated_energy for node in self.nodes])

