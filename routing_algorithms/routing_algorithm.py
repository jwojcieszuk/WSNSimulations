class RoutingAlgorithm(object):
    """
        This is an interface for all implementations of routing algorithms
    """
    def pre_communication(self, network):
        pass

    # def setup_phase(self, network, round_nb=None):
    #     """This method is called before every round. It only redirects to
    #     protected methods."""
    #     if round_nb == 0:
    #         self._initial_setup(network)
    #     else:
    #         self._setup_phase(network)
    @staticmethod
    def broadcast(network):
        network.broadcast_next_hop()
