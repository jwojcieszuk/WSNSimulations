import unittest

from environment.network import Network
from routing_algorithms.leach import Leach
from run import run_scenario, setup_logger


class TestLeach(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = {
            "test": {
                "algorithms": ["Leach"],
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
        """
            setup phase in leach should not drain any energy of the nodes
            so this test make sure that simulated annealing algorithm does not dissipate any energy
            it also checks whether setup phase creates
        """
        leach = Leach("Leach")
        simulation_logger = setup_logger(f'test_leach_logger', f'./logs/scenario-test_leach.log')

        network = Network(
            num_of_nodes=50,
            initial_node_energy=0.5,
            simulation_logger=simulation_logger,
            bs_x=50,
            bs_y=50
        )
        avg_energy = network.base_station.calculate_avg_energy(network.get_alive_nodes(),
                                                               network.base_station)

        heads = leach.setup_phase(network, 0)
        print(heads)

        avg_energy_sec = network.base_station.calculate_avg_energy(network.get_alive_nodes(), network.base_station)
        print(avg_energy_sec)
