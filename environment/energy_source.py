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
                self.energy = 0
                self.node.battery_dead()
        else:
            logging.info("node %d: battery is depleted." % self.node.node_id)



class PluggedIn(EnergySource):
    def consume(self, energy):
        pass
