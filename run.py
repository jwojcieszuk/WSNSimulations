"""
Base communication (Direct communication)
    1. create environment
    2. deploy nodes(sensors, base station) in a 2D plane - each node XY coordinates, ID

    3. communicate with nodes - send some random packets periodically from each node
    4. perform data aggregation and processing in base station

"""


import logging
import sys

from routing_algorithms.basic_communication import BasicCommunication
from environment.environment import Environment
from routing_algorithms.leach import Leach


def run():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    env = Environment()
    env.simulate_direct_communication(BasicCommunication)
    env.simulate_leach(Leach)
    # for node in env.network.nodes:
    #     print(node)

    # environment.print_nodes()


if __name__ == "__main__":
    run()

