import configuration as cfg
import logging


class EnergySource(object):
    def __init__(self, parent):
        self.energy = cfg.INITIAL_ENERGY
        self.node = parent

    def recharge(self):
        self.energy = cfg.INITIAL_ENERGY


class Battery(EnergySource):
    def consume(self, energy):
        if self.energy >= energy:
            self.energy -= energy
            if self.energy == 0:
                self.node.battery_dead()
            return True
        else:
            self.energy = 0
            self.node.battery_dead()
            # logging.info("node %d: battery is depleted. Cannot transmit data." % self.node.node_id)
            return False


class PluggedIn(EnergySource):
    def consume(self, energy):
        pass
