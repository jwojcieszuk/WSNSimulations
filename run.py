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

from routing_algorithms.basic_communication import BasicCommunication
from environment.environment import Environment, Plotter
from routing_algorithms.leach import Leach


def run():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    env = Environment()
    x1, y1 = env.simulate(BasicCommunication)
    x2, y2 = env.simulate_leach(Leach)
    plt.plot(x1, y1, 'r', x2, y2, '--b')
    plt.show()


if __name__ == "__main__":
    run()

