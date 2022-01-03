class RoutingAlgorithm(object):
    """
        This is an interface for all implementations of routing algorithms
    """
    @staticmethod
    def setup_initial_hops(network):
        pass

    # def setup_phase(self, environment, round_nb=None):
    #     """This method is called before every round. It only redirects to
    #     protected methods."""
    #     if round_nb == 0:
    #         self._initial_setup(environment)
    #     else:
    #         self._setup_phase(environment)
    @staticmethod
    def broadcast(network):
        network.broadcast_next_hop()
