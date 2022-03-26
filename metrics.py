from dataclasses import dataclass


@dataclass
class RoutingAlgorithmMetrics:
    rounds_num: list[int]
    alive_nodes_num: list[int]
    avg_energy_dissipation: list[float]
    algorithm_name: str