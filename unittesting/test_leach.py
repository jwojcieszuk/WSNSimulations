import unittest

from environment.network import Network
from routing_algorithms.leach import Leach
import configuration as cfg


class TestLeach(unittest.TestCase):
    """
        Test cases ensuring that LEACH implementation works as assumed.
    """
    def setUp(self) -> None:
        self.leach = Leach("Leach")
        self.initial_node_energy = 0.5
        desired_clusters_num = 5
        setattr(cfg, 'P', desired_clusters_num / 100)
        setattr(cfg, 'target_field_x_axis', [0, 100])
        setattr(cfg, 'target_field_y_axis', [0, 100])

        self.network = Network(
            num_of_nodes=100,
            initial_node_energy=self.initial_node_energy,
            simulation_logger=None,
            bs_x=50,
            bs_y=50
        )

    def test_setup_phase(self):
        """
            Setup phase in leach should not drain any energy of the nodes.
            It also checks whether each node has its destination node assigned,
        """
        old_energy_dissipation = self.network.total_energy_dissipation()

        self.leach.setup_phase(self.network, 0)

        new_energy_dissipation = self.network.total_energy_dissipation()

        # verify if energy dissipation increases after setup phase
        self.assertEqual(old_energy_dissipation, new_energy_dissipation)

        # verify if each node in the network has destination node assigned after setup phase
        for node in self.network.nodes:
            self.assertNotEqual(node.next_hop, -2)

    def test_sensing_phase(self):
        """
            Sensing phase on a network with all nodes alive should make each node contain data.
        """
        self.leach.sensing_phase(self.network)

        for node in self.network.nodes:
            self.assertEqual(node.contains_data, True)

    def test_transmission_phase(self):
        """
            After sensing phase, each node contains data,
            so during data transmission phase each node should consume some energy
            Also, base station after transmission phase in first round should receive 100 packets.
        """
        heads = self.leach.setup_phase(self.network, 0)
        self.leach.sensing_phase(self.network)
        self.leach.transmission_phase(self.network, heads)

        for node in self.network.nodes:
            self.assertNotEqual(node.energy_source.energy, self.initial_node_energy)

        self.assertEqual(self.network.base_station.received_packets, 100)

