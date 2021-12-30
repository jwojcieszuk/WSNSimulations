"""
Base communication (Direct communication)
    1. create network
    2. deploy nodes(sensors, base station) in a 2D plane - each node XY coordinates, ID

    3. communicate with nodes - send some random packets periodically from each node
    4. perform data aggregation and processing in base station


model energy consumption

LEACH

"""
import logging
import sys

from routing_algorithms.basic_communication import BasicCommunication
from environment import Environment

def run():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    env = Environment()
    env.simulate_routing(BasicCommunication)
    for node in env.network:
        print(node)

    # network.print_nodes()


if __name__ == "__main__":
    run()

