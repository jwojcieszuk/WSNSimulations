import unittest

from run import run_scenario


class TestScenarioJSON(unittest.TestCase):

    def test_unsupported_metric(self):
        scenario_name = "test"
        invalid_metric_scenario = {
            scenario_name: {
                "algorithms": ["DirectCommunication", "Leach"],
                "metrics": ["invalid_metric"],
                "num_of_nodes": 50,
                "initial_node_energy": 0.5
            }
        }
        with self.assertRaises(NotImplementedError):
            run_scenario(invalid_metric_scenario[scenario_name], scenario_name)

    def test_unsupported_algorithm(self):
        scenario_name = "test"

        invalid_algorithm_scenario = {
            scenario_name: {
                "algorithms": ["invalid"],
                "metrics": ["first_dead_node"],
                "num_of_nodes": 50,
                "initial_node_energy": 0.5
            }
        }
        with self.assertRaises(NotImplementedError):
            run_scenario(invalid_algorithm_scenario[scenario_name], scenario_name)

    def test_too_big_num_of_nodes(self):
        scenario_name = "test"

        invalid_algorithm_scenario = {
            scenario_name: {
                "algorithms": ["Leach"],
                "metrics": ["first_dead_node"],
                "num_of_nodes": 1000,
                "initial_node_energy": 0.5
            }
        }
        with self.assertRaises(NotImplementedError):
            run_scenario(invalid_algorithm_scenario[scenario_name], scenario_name)

    def test_too_big_initial_node_energy(self):
        scenario_name = "test"

        invalid_algorithm_scenario = {
            scenario_name: {
                "algorithms": ["Leach"],
                "metrics": ["first_dead_node"],
                "num_of_nodes": 50,
                "initial_node_energy": 15
            }
        }
        with self.assertRaises(NotImplementedError):
            run_scenario(invalid_algorithm_scenario[scenario_name], scenario_name)

    def test_too_small_num_of_nodes(self):
        scenario_name = "test"

        invalid_algorithm_scenario = {
            scenario_name: {
                "algorithms": ["Leach"],
                "metrics": ["first_dead_node"],
                "num_of_nodes": -10,
                "initial_node_energy": 0.5
            }
        }
        with self.assertRaises(NotImplementedError):
            run_scenario(invalid_algorithm_scenario[scenario_name], scenario_name)

    def test_too_small_initial_node_energy(self):
        scenario_name = "test"

        invalid_algorithm_scenario = {
            scenario_name: {
                "algorithms": ["Leach"],
                "metrics": ["first_dead_node"],
                "num_of_nodes": -10,
                "initial_node_energy": 0.5
            }
        }
        with self.assertRaises(NotImplementedError):
            run_scenario(invalid_algorithm_scenario[scenario_name], scenario_name)
