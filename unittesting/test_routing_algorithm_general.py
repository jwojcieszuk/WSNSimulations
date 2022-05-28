import copy
import unittest

from environment.routing_simulator import RoutingSimulator
from run import run_scenario, setup_logger
import configuration as cfg


class TestRoutingAlgorithmGeneral(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = {
            "test": {
                "algorithms": [],
                "metrics": [],
                "num_of_nodes": 50,
                "initial_node_energy": 0.2,
                "base_station_location": [50, 50],
                "bits_per_message": 2000,
                "x_axis_bounds": [0, 50],
                "y_axis_bounds": [0, 50],
                "desired_clusters_percentage": 10,
                "max_rounds": 5,
                "radio_propagation_model": "free_space"
            }
        }
        setattr(cfg, 'target_field_x_axis', [0, 100])
        setattr(cfg, 'target_field_y_axis', [0, 100])

    def test_number_of_received_packets(self):
        """
            Each algorithm is simulated for 5 rounds, so none of the nodes should die
            as a result, in each case, base station should receive 250 packets (50 nodes, 5 rounds, each node 1 sends 1 packet)
        """
        self.scenario["test"]["algorithms"] = ["DirectCommunication", "Leach", "LeachC"]
        self.scenario["test"]["metrics"] = ["received_packets"]

        metrics = run_scenario(self.scenario["test"], "test")
        received_packets_list = [metric.received_packets for metric in metrics]
        expected_packets_list = [250, 250, 250]
        self.assertListEqual(received_packets_list, expected_packets_list)

    def test_network_reset_after_algorithm(self):
        """
            Test if after one algorithm from the scenario has finished running, if the network is initial state,
            before running next algorithm
        """
        simulation_logger = setup_logger(f'test_network_reset_logger', f'./logs/scenario-test_network_reset.log')
        env = RoutingSimulator(
            num_of_nodes=self.scenario['test']['num_of_nodes'],
            initial_node_energy=self.scenario['test']['initial_node_energy'],
            simulation_logger=simulation_logger,
            bs_location=self.scenario['test']['base_station_location']
        )

        coordinates_of_nodes_pre_simulation = list()
        for node in env.network.nodes:
            coordinates_of_nodes_pre_simulation.append((node.pos_x, node.pos_y))

        env.simulate(cfg.supported_algorithms["DirectCommunication"], simulation_logger)
        network_post_simulation = env.network

        # assert that each node have the same coordinates
        coordinates_of_nodes_post_simulation = list()
        for node in network_post_simulation.nodes:
            coordinates_of_nodes_post_simulation.append((node.pos_x, node.pos_y))
        self.assertEqual(coordinates_of_nodes_pre_simulation, coordinates_of_nodes_post_simulation)

        # assert that each node after simulation is restored
        self.assertEqual(len(network_post_simulation.get_alive_nodes()), 50)

        # assert that base station is reinitialized, so should have 0 received packets
        self.assertEqual(network_post_simulation.base_station.received_packets, 0)

        # assert that each node have energy restored to the initial
        for node in network_post_simulation.nodes:
            self.assertEqual(node.energy_source.energy, self.scenario['test']['initial_node_energy'])

