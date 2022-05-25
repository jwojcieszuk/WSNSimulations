import math
import unittest

from environment.network import Network
from routing_algorithms.leach_c import LeachC
import configuration as cfg


class TestLeachC(unittest.TestCase):
    """
        Test cases ensuring that LEACH-C implementation works as assumed.
    """
    def setUp(self) -> None:
        self.leachc = LeachC("LeachC")
        self.desired_clusters_num = 5
        self.initial_node_energy = 0.2
        setattr(cfg, 'P', self.desired_clusters_num / 100)

        self.network = Network(
            num_of_nodes=100,
            initial_node_energy=self.initial_node_energy,
            simulation_logger=None,
            bs_x=50,
            bs_y=50
        )

    def test_setup_phase(self):
        """
            Setup phase should not increase total energy dissipation.
            Also, it should create as many clusters as required by "desired_clusters_percentage".
            Finally, each node should have destination node assigned
        """
        avg_energy = self.network.base_station.calculate_avg_energy(self.network.get_alive_nodes(), self.network.base_station)

        old_energy_dissipation = self.network.total_energy_dissipation()

        heads = self.leachc.setup_phase(self.network, 0, avg_energy)

        new_energy_dissipation = self.network.total_energy_dissipation()

        # verify if energy dissipation increases after setup phase
        self.assertEqual(old_energy_dissipation, new_energy_dissipation)

        # verify if setup phase creates desired clusters num
        self.assertEqual(len(heads), self.desired_clusters_num)

        # verify if each node in the network has destination node assigned after setup phase
        for node in self.network.nodes:
            # -2 value means that node does not have destination node assigned
            self.assertNotEqual(node.next_hop, -2)

    def test_sensing_phase(self):
        """
            Sensing phase on a network with all nodes alive should make each node contain data.
        """
        self.leachc.sensing_phase(self.network)

        for node in self.network.nodes:
            self.assertEqual(node.contains_data, True)

    def test_average_energy_transmission(self):
        """
            In leach-c during setup phase each node transmits its energy level to the base station,
            so after this operation each node energy should be below initial node energy.
        """
        self.network.base_station.calculate_avg_energy(
            self.network.get_alive_nodes(),
            self.network.base_station
        )
        for node in self.network.nodes:
            self.assertNotEqual(node.energy_source.energy, self.initial_node_energy)

    def test_transmission_phase(self):
        """
            Base station after transmission phase in first round should receive 100 packets.
        """
        avg_energy = self.network.base_station.calculate_avg_energy(
            self.network.get_alive_nodes(),
            self.network.base_station
        )
        heads = self.leachc.setup_phase(self.network, 0, avg_energy)
        self.leachc.sensing_phase(self.network)
        self.leachc.transmission_phase(self.network, heads)

        self.assertEqual(self.network.base_station.received_packets, 100)

    def test_simulated_annealing_algorithm(self):
        """
            Simulated annealing algorithm should decrease energy consumption in each round.
            Comparison is done by forming clusters randomly and calculating energy dissipation,
            and by forming clusters with the use of simulated annealing algorithm.
        """
        avg_energy = self.network.base_station.calculate_avg_energy(self.network.get_alive_nodes(), self.network.base_station)

        alive_nodes = self.network.get_alive_nodes()

        clusters_num = math.floor(len(alive_nodes) * cfg.P)

        dissipated_energy_list = list()
        for node in self.network.nodes:
            dissipated_energy_list.append(node.dissipated_energy)

        sum_energy_random_approach = 0
        sum_energy_simulated_annealing_approach = 0
        for i in range(30):
            self.network.restore_for_annealing(dissipated_energy_list)
            heads = self.leachc.setup_phase(self.network, 0, avg_energy)
            self.leachc.sensing_phase(self.network, not_consume=True)
            self.leachc.transmission_phase(self.network, heads, not_consume=True)
            sum_energy_simulated_annealing_approach += self.network.total_energy_dissipation()

            self.network.restore_for_annealing(dissipated_energy_list)
            heads = self.leachc._elect_cluster_heads(self.network.get_alive_nodes(), avg_energy, clusters_num)
            self.leachc._form_clusters(heads, alive_nodes)
            self.leachc.sensing_phase(self.network, not_consume=True)
            self.leachc.transmission_phase(self.network, heads, not_consume=True)
            sum_energy_random_approach += self.network.total_energy_dissipation()

        difference = sum_energy_random_approach-sum_energy_simulated_annealing_approach
        print(f'Random sum{sum_energy_random_approach}, difference: {difference}')
        self.assertTrue(sum_energy_random_approach > sum_energy_simulated_annealing_approach)

