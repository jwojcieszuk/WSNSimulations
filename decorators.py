import functools
import logging


def _alive_node_only(func):
    @functools.wraps(func)
    def wrapper(node, *args, **kwargs):
        if node.alive:
            func(node, *args, **kwargs)
        elif node.energy_source.energy == 0:
            # logging.info("Node %s is not alive! Cannot sense data.", node.node_id)
            pass

    return wrapper
