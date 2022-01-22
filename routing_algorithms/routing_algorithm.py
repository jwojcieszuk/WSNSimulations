class RoutingAlgorithm(object):
    """
        This is an interface for all implementations of routing algorithms
    """
    @staticmethod
    def setup_phase(network):
        pass

    @staticmethod
    def broadcast(network):
        network.broadcast_next_hop()
