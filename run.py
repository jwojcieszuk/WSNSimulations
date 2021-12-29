"""
Base communication (Direct communication)
    1. create network
    2. deploy nodes(sensors, base station) in a 2D plane - each node XY coordinates, ID
    3. communicate with nodes - send some random packets periodically from each node
    4. perform data aggregation and processing in base station


model energy consumption

LEACH

"""
from network import Network
from routing_algorithms.basic_communication import BasicCommunication


def run():
    # basic communication scenario
    network = Network(routing_protocol=BasicCommunication)
    for node in network:
        print(node)

    network.simulate()
    network.print_nodes()


if __name__ == "__main__":
    run()

