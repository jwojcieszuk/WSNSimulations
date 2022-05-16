from dataclasses import dataclass


@dataclass
class RoutingAlgorithmMetrics:
    rounds_num: list[int]
    alive_nodes_num: list[int]
    avg_energy_dissipation: list[float]
    received_packets: int
    algorithm_name: str
    first_dead_node: int
    total_energy_dissipation: int
    dead_nodes_num: list[int]
