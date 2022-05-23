import shutil
import unittest

from environment.network import Network
from routing_algorithms.leach_c import LeachC
from run import run_scenario, setup_logger
import configuration as cfg


class TestLeachC(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = {
            "test": {
                "algorithms": ["LeachC"],
                "metrics": [],
                "num_of_nodes": 50,
                "initial_node_energy": 0.5,
                "base_station_location": [50, 50],
                "bits_per_message": 2000,
                "x_axis_bounds": [0, 50],
                "y_axis_bounds": [0, 50],
                "desired_clusters_percentage": 10,
                "max_rounds": 5
            }
        }

    def test_setup_phase(self):
        leachc = LeachC("LeachC")
        desired_clusters_num = 5
        setattr(cfg, 'P', desired_clusters_num / 100)

        network = Network(
            num_of_nodes=100,
            initial_node_energy=0.2,
            simulation_logger=None,
            bs_x=50,
            bs_y=50
        )

        avg_energy = network.base_station.calculate_avg_energy(network.get_alive_nodes(), network.base_station)

        old_energy_dissipation = network.total_energy_dissipation()

        heads = leachc.setup_phase(network, 0, avg_energy)

        new_energy_dissipation = network.total_energy_dissipation()

        # verify if energy dissipation increases after setup phase
        self.assertEqual(old_energy_dissipation, new_energy_dissipation)

        # verify if setup phase creates desired clusters num
        self.assertEqual(len(heads), desired_clusters_num)

        # verify if each node in the network has destination node assigned after setup phase
        for node in network.nodes:
            self.assertNotEqual(node.next_hop, -2)



