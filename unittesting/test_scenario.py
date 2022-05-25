import unittest

from run import run_scenario


class TestScenarioJSON(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = {
            "test": {
                "algorithms": ["DirectCommunication", "Leach"],
                "metrics": ["alive_nodes_num"],
                "num_of_nodes": 50,
                "initial_node_energy": 0.5,
                "base_station_location": [50, 50],
                "bits_per_message": 2000,
                "x_axis_bounds": [0, 50],
                "y_axis_bounds": [0, 50],
                "desired_clusters_percentage": 10
            }
        }

    def test_unsupported_metric(self):
        scenario_name = "test"
        self.scenario[scenario_name]["metrics"] = ["invalid_metric"]

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_unsupported_algorithm(self):
        scenario_name = "test"
        self.scenario[scenario_name]["algorithms"] = ["invalid_algorithm"]

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_big_num_of_nodes(self):
        scenario_name = "test"
        self.scenario[scenario_name]["num_of_nodes"] = 1001

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_big_initial_node_energy(self):
        scenario_name = "test"
        self.scenario[scenario_name]["initial_node_energy"] = 20

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_small_num_of_nodes(self):
        scenario_name = "test"
        self.scenario[scenario_name]["num_of_nodes"] = -10

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_small_initial_node_energy(self):
        scenario_name = "test"
        self.scenario[scenario_name]["initial_node_energy"] = 0

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_big_bits_per_message(self):
        scenario_name = "test"
        self.scenario[scenario_name]["bits_per_message"] = 10001

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_small_bits_per_message(self):
        scenario_name = "test"
        self.scenario[scenario_name]["bits_per_message"] = 99

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_big_desired_clusters_percentage(self):
        scenario_name = "test"
        self.scenario[scenario_name]["desired_clusters_percentage"] = 95

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_small_desired_clusters_percentage(self):
        scenario_name = "test"
        self.scenario[scenario_name]["desired_clusters_percentage"] = 0

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)

    def test_too_small_max_rounds(self):
        scenario_name = "test"
        self.scenario[scenario_name]["max_rounds"] = 0

        with self.assertRaises(NotImplementedError):
            run_scenario(self.scenario[scenario_name], scenario_name)
