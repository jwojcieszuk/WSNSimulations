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


def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)
    wrapper.has_run = False
    return wrapper