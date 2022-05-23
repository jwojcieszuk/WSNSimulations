import unittest
from run import run_scenario


class TestRoutingAlgorithmGeneral(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = {
            "test": {
                "algorithms": [],
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


