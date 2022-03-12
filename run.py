"""
Base communication (Direct communication)
    1. create environment
    2. deploy nodes(sensors, base station) in a 2D plane - each node XY coordinates, ID

    3. communicate with nodes - send some random packets periodically from each node
    4. perform data aggregation and processing in base station

"""


import logging
import sys

import matplotlib.pyplot as plt
from routing_algorithms.leach_c import LeachC

from routing_algorithms.direct_communication import DirectCommunication
from environment.environment import Environment
from routing_algorithms.leach import Leach


def run():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    env = Environment()
    rounds1, alive_nodes1, avg_energy_dissipation1 = env.simulate(DirectCommunication())
    rounds2, alive_nodes2, avg_energy_dissipation2 = env.simulate(LeachC())
    rounds3, alive_nodes3, avg_energy_dissipation3 = env.simulate(Leach())
    plt.plot(rounds1, alive_nodes1, 'r', label="Direct Communication")
    plt.plot(rounds2, alive_nodes2, '--b', label="LEACH-C")
    plt.plot(rounds3, alive_nodes3, 'g', label="LEACH")
    plt.ylabel("Number of nodes alive")
    plt.xlabel("Rounds")
    plt.legend(loc="lower left")
    plt.show()

    plt.plot(rounds1, avg_energy_dissipation1, 'r', label="Direct Communication")
    plt.plot(rounds2, avg_energy_dissipation2, '--b', label="LEACH-C")
    plt.plot(rounds3, avg_energy_dissipation3, 'g', label="LEACH")
    plt.ylabel("Average energy dissipation")
    plt.xlabel("Rounds")
    plt.legend(loc="lower left")

    plt.show()


if __name__ == "__main__":
    run()

