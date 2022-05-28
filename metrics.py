from dataclasses import dataclass, field


@dataclass
class RoutingAlgorithmMetrics:
    rounds_num: list[int] = field(default_factory=list)
    alive_nodes_num: list[int] = field(default_factory=list)
    avg_energy_dissipation: list[float] = field(default_factory=list)
    received_packets: int = 0
    algorithm_name: str = ""
    first_dead_node: int = 0
    total_energy_dissipation_200: int = 0
    dead_nodes_num: list[int] = field(default_factory=list)
    received_packets_round_30: int = 0
